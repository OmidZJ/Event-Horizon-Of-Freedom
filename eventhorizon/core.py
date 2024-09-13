import json
import random
import subprocess
import urllib.parse
import httpx
import time
import speedtest
import logging
from .utils import Color, get_ping_color, save_results_to_file, extract_configs, load_previous_results, save_last_line, read_last_line

# تنظیمات logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

xraypath = "xray.exe"

# Function to convert VLESS link to Xray configuration
def v2ray_to_xray_config(v2ray_url):
    try:
        scheme, rest = v2ray_url.split("://")
        parts = rest.split("?")
        uuid_address = parts[0].split("@")
        uuid = uuid_address[0]
        address_port = uuid_address[1].split(":")
        server_address = address_port[0]
        port = address_port[1]

        params = parts[1].split("&")
        encryption = next((p.split("=")[1] for p in params if p.startswith('encryption=')), 'none')
        security = next((p.split("=")[1] for p in params if p.startswith('security=')), 'none')
        sni = next((p.split("=")[1] for p in params if p.startswith('sni=')), '')
        type_ = next((p.split("=")[1] for p in params if p.startswith('type=')), 'tcp')
        host = next((p.split("=")[1] for p in params if p.startswith('host=')), '')
        header_type = next((p.split("=")[1] for p in params if p.startswith('headerType=')), 'none')

        path_encoded = next((p.split("=")[1] for p in params if p.startswith('path=')), '')
        path = urllib.parse.unquote(path_encoded)

        config = {
            "inbounds": [
                {
                    "port": random.randint(10000, 60000),  # Random port for SOCKS5 proxy
                    "protocol": "socks",
                    "listen": "127.0.0.1",
                    "settings": {
                        "auth": "noauth",  # No authentication required
                        "udp": True,
                        "timeout": 300
                    }
                }
            ],
            "outbounds": [
                {
                    "protocol": "vless",
                    "settings": {
                        "vnext": [
                            {
                                "address": server_address,
                                "port": int(port),
                                "users": [
                                    {
                                        "id": uuid,
                                        "encryption": encryption
                                    }
                                ]
                            }
                        ]
                    },
                    "streamSettings": {
                        "network": type_,
                        "security": security,
                        "tlsSettings": {
                            "serverName": sni
                        },
                        "wsSettings": {
                            "path": path,
                            "headers": {
                                "Host": host
                            }
                        },
                        "tcpSettings": {
                            "header": {
                                "type": header_type
                            }
                        }
                    }
                }
            ]
        }
        return config
    except Exception as e:
        logging.error(f"Error converting VLESS URL to Xray config: {e}")
        raise

# Function to run the Xray core
def run_xray(xray_path, config_path):
    try:
        process = subprocess.Popen([xray_path, '-c', config_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return process
    except Exception as e:
        logging.error(f"Error running Xray: {e}")
        return None

# Function to test ping through the proxy
def test_proxy_ping(proxy_port):
    proxies = {
        "http://": f"socks5://127.0.0.1:{proxy_port}",
        "https://": f"socks5://127.0.0.1:{proxy_port}"
    }

    try:
        start_time = time.time()
        with httpx.Client(proxies=proxies, timeout=1) as client:
            client.get('https://google.com')
            delay = (time.time() - start_time) * 1000
            return delay / 2  # Convert to milliseconds
    except httpx.RequestError as e:
        logging.error(f"Error in proxy ping test: {e}")
        return -1

# Function to test speed using Speedtest
def test_speed(proxy_port):
    proxies = {
        "http": f"socks5://127.0.0.1:{proxy_port}",
        "https": f"socks5://127.0.0.1:{proxy_port}"
    }

    try:
        st = speedtest.Speedtest()
        st.get_best_server()

        logging.info("Testing download speed...")
        download_speed = st.download() / 10**6  # Convert to Mbps
        logging.info(f"Download Speed: {download_speed:.2f} Mbps")

        logging.info("Testing upload speed...")
        upload_speed = st.upload() / 10**6  # Convert to Mbps
        logging.info(f"Upload Speed: {upload_speed:.2f} Mbps")

    except Exception as e:
        logging.error(f"Error in speed test: {e}")

# Main function
def main(v2ray_file, results_file, last_line_file, output_file):
    try:
        urls = []
        with open(v2ray_file, 'r') as file:
            urls = [line.strip() for line in file]

        last_line = read_last_line(last_line_file)
        pings = load_previous_results(results_file)

        for i, v2ray_url in enumerate(urls):
            if i < last_line:
                continue

            config = v2ray_to_xray_config(v2ray_url)
            config_path = "xray_config.json"
            with open(config_path, "w") as f:
                json.dump(config, f, indent=4)

            xray_process = run_xray(xraypath, config_path)
            if not xray_process:
                continue

            proxy_port = config['inbounds'][0]['port']
            server_address = config['outbounds'][0]['settings']['vnext'][0]['address']
            delay = test_proxy_ping(proxy_port)
            if delay != -1:
                ping_color = get_ping_color(delay)
                logging.info(f"Address: {server_address} - {ping_color}Ping: {delay:.2f} ms{Color.RESET}")
                pings.append((v2ray_url, server_address, delay))

            xray_process.terminate()
            save_last_line(last_line_file, i + 1)
            save_results_to_file(results_file, pings)
            extract_configs(results_file, output_file)

        best_configs = sorted(pings, key=lambda x: x[2])[:3]
        logging.info("\nTop 3 configurations based on ping:")
        for url, address, delay in best_configs:
            ping_color = get_ping_color(delay)
            logging.info(f"Address: {address} - {ping_color}Ping: {delay:.2f} ms{Color.RESET}")

        for url, address, _ in best_configs:
            logging.info(f"\nTesting speed for Address: {address}")
            config = v2ray_to_xray_config(url)
            config_path = "xray_config.json"
            with open(config_path, "w") as f:
                json.dump(config, f, indent=4)

            xray_process = run_xray(xraypath, config_path)
            if not xray_process:
                continue

            proxy_port = config['inbounds'][0]['port']
            test_speed(proxy_port)
            xray_process.terminate()

    except Exception as e:
        logging.error(f"Error in main function: {e}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Test and configure VLESS links with Xray.')
    parser.add_argument('v2ray_file', type=str, help='Path to the VLESS links file')
    parser.add_argument('results_file', type=str, help='File to save ping results')
    parser.add_argument('last_line_file', type=str, help='File to save the last tested line number')
    parser.add_argument('output_file', type=str, help='File to save the best configurations')

    args = parser.parse_args()
    main(args.v2ray_file, args.results_file, args.last_line_file, args.output_file)
