import os

class Color:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'

def get_ping_color(delay):
    if delay < 800:
        return Color.GREEN
    elif delay < 1000:
        return Color.YELLOW
    else:
        return Color.RED

def save_results_to_file(results_file, pings):
    with open(results_file, 'w') as file:
        for config, address, delay in sorted(pings, key=lambda x: x[2]):
            config = config[:-2].strip()
            file.write(f"{address} | Ping: {delay:.2f} ms | {config}\n")

def extract_configs(input_file, output_file):
    configs = []
    with open(input_file, 'r') as infile:
        for line in infile:
            parts = line.split("|")
            config = parts[2][:-2]
            configs.append(config)
    with open(output_file, 'w') as outfile:
        for config in configs:
            outfile.write(config + '\n')

def load_previous_results(results_file):
    pings = []
    if os.path.exists(results_file):
        with open(results_file, 'r') as file:
            for line in file:
                parts = line.split("|")
                if len(parts) == 3:
                    address = parts[0].strip()
                    delay = float(parts[1].replace("ms", "").replace("Ping:", "").strip())
                    config = parts[2]
                    pings.append((config, address, delay))
    return pings

def save_last_line(last_line_file, line_num):
    with open(last_line_file, 'w') as file:
        file.write(str(line_num))

def read_last_line(last_line_file):
    if os.path.exists(last_line_file):
        with open(last_line_file, 'r') as file:
            return int(file.read().strip())
    return 0
