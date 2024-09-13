# Event Horizon of Freedom

Event Horizon of Freedom marks the crucial moment where the barriers of repression dissolve, revealing a new realm of opportunity. Like the edge of a black hole, this threshold represents the shift from confinement to boundless potential for Iranians. We are poised at the brink of transformative change, ready to step into a future of uncharted possibilities.

---

**Event Horizon of Freedom** is a tool designed for scanning domains to identify services such as Fastly, G Core, Cloudflare, and others. It helps in analyzing and configuring proxy settings for optimized performance.

## Features
- Scans domains to detect usage of popular CDN services and proxy servers.
- Converts VLESS links to Xray configuration files.
- Tests proxy connections and measures ping and speed performance.
- Provides results and recommendations based on performance metrics.

## How to Use

1. **Prepare Your Files:**
   - `vless_links.txt`: A file containing VLESS links you want to test.
   - `ping_results.txt`: A file where ping results will be saved.
   - `last_line.txt`: A file to keep track of the last tested line number.
   - `TheBest.txt`: A file where the best configurations will be saved.

2. **Run the Tool:**
   ```bash
   python -m eventhorizon vless_links.txt ping_results.txt last_line.txt TheBest.txt
   ```

   Ensure you have all the required files in the same directory or provide their full paths.

## Requirements
- Python 3.12 or higher
- Required Python packages: `httpx`, `speedtest-cli`

## Installation
To install the required packages, you can use pip:

```bash
pip install httpx speedtest-cli
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
