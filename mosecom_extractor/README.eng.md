# Moscow Air Quality Monitoring - Python Script for Data Extraction

This Python script extracts air quality data from the official Moscow Air Quality Monitoring website (mosecom.mos.ru).

## Features

- Fetch current air quality data from a specified station
- Support for different output formats:
  - Short gas names (default)
  - Long gas names
  - Data for a specific gas type only
- Support for different measurement units:
  - % PDK (default)
  - mg/m³
- Historical data extraction (limited by website)
- Support for all Moscow monitoring stations

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python mosecom_extractor.py [OPTIONS] STATION_URL
```

### Options

- `-h`, `--help`: Show help
- `-f {short,long}`, `--format {short,long}`: Output format (short/long)
- `-g GAS_TYPE`, `--gas GAS_TYPE`: Get data for a specific gas only
- `-u {parts,mg/m3}`, `--unit {parts,mg/m3}`: Measurement unit (parts/mg/m3)
- `-d DATE`, `--date DATE`: Date for historical data (in DD.MM.YYYY format)

### Examples

```bash
# Get current data in short names format (default)
python mosecom_extractor.py https://mosecom.mos.ru/m1-6-moskvorechye-saburovo/

# Get current data in long names format
python mosecom_extractor.py -f long https://mosecom.mos.ru/m1-6-moskvorechye-saburovo/

# Get data for NO2 only
python mosecom_extractor.py -g NO2 https://mosecom.mos.ru/m1-6-moskvorechye-saburovo/

# Get data in mg/m³
python mosecom_extractor.py -u mg/m3 https://mosecom.mos.ru/m1-6-moskvorechye-saburovo/

# Get historical data for a specific date
python mosecom_extractor.py -d 01.06.2026 https://mosecom.mos.ru/m1-6-moskvorechye-saburovo/
```

## Supported Gas Types

- CO (Carbon Monoxide)
- NO2 (Nitrogen Dioxide)
- CH4 (Methane)
- PM10 (Particulate Matter PM10)
- NO (Nitric Oxide)
- H2S (Hydrogen Sulfide)
- C6H5OH (Phenol)

## License

This project is licensed under the MIT License.