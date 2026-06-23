# Moscow Air Quality Monitoring

[![GitHub](https://img.shields.io/github/license/p1ne/mosecom-integration)](https://github.com/p1ne/mosecom-integration)
[![GitHub stars](https://img.shields.io/github/stars/p1ne/mosecom-integration)](https://github.com/p1ne/mosecom-integration)

This repository contains tools for fetching and processing air quality data from the official Moscow Air Quality Monitoring website (mosecom.mos.ru).

## Contents

1. [Python Script](mosecom_extractor/README.md) - Standalone script for data extraction
2. [Home Assistant Integration](custom_components/mosecom/README.md) - Home Assistant integration for real-time air quality monitoring

## Features

- Fetch current air quality data from official monitoring stations
- Support for different output formats (short/long names, specific gas type)
- Support for different measurement units (parts, mg/m³)
- Historical data extraction (limited by website)
- Home Assistant integration for continuous monitoring
- Automatic gas type detection for each station
- Support for all Moscow monitoring stations

## Installation

### Python Script

To use the Python script, you need Python 3.6+:

```bash
cd mosecom_extractor
pip install -r requirements.txt
python mosecom_extractor.py --help
```

### Home Assistant Integration

The integration is available through HACS (Home Assistant Community Store) or can be installed manually:

1. Copy the `custom_components/mosecom` folder to your Home Assistant `custom_components` directory
2. Restart Home Assistant
3. Go to Settings → Devices & Services → Add Integration
4. Search for "Moscow Air Quality Monitoring" and follow the setup instructions

## Repository

GitHub: https://github.com/p1ne/mosecom-integration

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.