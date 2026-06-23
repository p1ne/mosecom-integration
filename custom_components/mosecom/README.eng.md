# Moscow Air Quality Monitoring Home Assistant Integration

This integration allows you to monitor air quality in Moscow in real-time using data from the official Moscow Air Quality Monitoring website (mosecom.mos.ru).

## Features

- Automatic gas type detection for each station
- Dynamic sensor creation for available gases
- Support for all Moscow monitoring stations
- Automatic data updates every 15 minutes
- Convenient station selection interface with district and address display
- Support for custom device names
- HACS (Home Assistant Community Store) compatibility

## Installation

### Through HACS (Recommended)

1. Open HACS in your Home Assistant
2. Go to "Integrations"
3. Click on the three dots in the top right corner and select "Custom repositories"
4. Add `https://github.com/p1ne/mosecom` as a repository of type "Integration"
5. Search for "Moscow Air Quality Monitoring" and install it
6. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/mosecom` folder to your Home Assistant `custom_components` directory
2. Restart Home Assistant
3. Go to Settings → Devices & Services → Add Integration
4. Search for "Moscow Air Quality Monitoring" and follow the setup instructions

## Configuration

1. Go to Settings → Devices & Services → Add Integration
2. Search for "Moscow Air Quality Monitoring"
3. Select a monitoring station from the list
4. Optionally specify a custom name for the device
5. Click "Submit"

## Sensors

Sensors are created for all available gas types at each station:
- Sensors in mg/m³ (milligrams per cubic meter)
- Sensors in % PDK (percentage of maximum permissible concentration)

Sensor names are formed according to the template:
- `sensor.[device_name]_[gas_type]_mg_m3`
- `sensor.[device_name]_[gas_type]_pdk`

## Supported Gas Types

- CO (Carbon Monoxide)
- NO2 (Nitrogen Dioxide)
- CH4 (Methane)
- PM10 (Particulate Matter PM10)
- NO (Nitric Oxide)
- H2S (Hydrogen Sulfide)
- C6H5OH (Phenol)

## Troubleshooting

### Sensors Unavailable
- Check your internet connection
- Make sure the station URL is accessible in a browser
- Check Home Assistant logs for errors

### No Data
- Some stations may not transmit data at certain times
- Check data availability on the official website

## License

This project is licensed under the MIT License.