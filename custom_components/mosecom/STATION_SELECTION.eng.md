# Station Selection Feature

## Overview

The Moscow Air Quality Monitoring integration includes a station selection interface that allows users to choose monitoring stations from a comprehensive list.

## Features

### Station List
- **Automatic fetching**: Stations are automatically fetched from:
  - Regular stations: https://mosecom.mos.ru/stations/
  - Special stations: https://mosecom.mos.ru/special-stations/
- **Rich display**: Each station shows:
  - Station name
  - District abbreviation
  - Clean address

## Station Data Format

Each station in the list contains:

```python
{
    "name": "М1-6 (Москворечье-Сабурово)",
    "district": "ЮАО",
    "address": "ул. Москворечье, д. 24",
    "url": "https://mosecom.mos.ru/m1-6-moskvorechye-saburovo/"
}
```

## Address Processing

The integration automatically cleans addresses by:

1. **Removing Moscow prefixes**:
   - "город Москва, "
   - "г. Москва, "
   - "г Москва, "
   - "Москва, "
   - "г. "

2. **Cleaning punctuation**: Removes leading commas and periods

3. **Result**: Clean address like "ул. Москворечье, д. 24" instead of "г. Москва, ул. Москворечье, д. 24"

## User Interface

### Configuration Flow

1. **Initial Load**: Integration fetches all stations from both pages
2. **Station Selection**: User sees combo box with all available stations
3. **Validation**: Selected station is validated before creating integration

### Station Display Format

In the combo box, each station is displayed as:

```
М1-6 (Москворечье-Сабурово) (ЮАО) - ул. Москворечье, д. 24
```

## Technical Implementation

### Station Fetching

```python
async def fetch_stations(hass) -> list[dict[str, Any]]:
    """Fetch all stations from both regular and special stations pages."""
    stations = []
    
    # Fetch regular stations
    regular_stations = await _fetch_page_stations(
        session,
        "https://mosecom.mos.ru/stations/"
    )
    stations.extend(regular_stations)
    
    # Fetch special stations
    special_stations = await _fetch_page_stations(
        session,
        "https://mosecom.mos.ru/special-stations/"
    )
    stations.extend(special_stations)
    
    return stations
```

### HTML Parsing

The stations page HTML is parsed using regex patterns to extract:
- Station name
- District (converted from CSS class names to short format)
- Address (cleaned of Moscow prefixes)
- URL

The parser correctly handles the complex HTML structure of the stations pages:
- District-based sections with class `allstan-item`
- Table sections with class `allstan-item-table`
- Rows with class `allstan-item-row`
- Station data in `row-title` and `row-address` divs
- District information in CSS class names (e.g., `tsao-row`, `sao-row`)

### District Mapping

District information is extracted from CSS class names:

```python
district_mapping = {
    "tsao": "ЦАО",
    "sao": "САО",
    "svao": "СВАО",
    "vao": "ВАО",
    "yuvao": "ЮВАО",
    "yuao": "ЮАО",
    "yuzao": "ЮЗАО",
    "zao": "ЗАО",
    "szao": "СЗАО",
    "zelen": "ЗелАО",
    "tinao": "ТиНАО"
}
```

## Configuration Schema

The config flow uses the following schema:

```python
STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_STATION): vol.In(station_options),
        vol.Optional(CONF_NAME, default=""): str,
    }
)
```

## Error Handling

### Connection Errors
- If station list cannot be fetched, shows error message
- User can retry

### Validation Errors
- Station must be selected from the list
- Selected station URL must be accessible
- Duplicate stations are prevented

## Benefits

1. **User-friendly**: No need to manually find and copy URLs
2. **Comprehensive**: All available stations in one place
3. **Accurate**: Station data fetched directly from official source

## Migration Notes

### Version 3.0.0 Changes

- **Simplified interface**: Removed district and special station filters
- **Migration**: Existing integrations continue to work but new ones must use station selection
- **Backward compatibility**: Old URL-based configuration is still supported for existing entries

### For Existing Users

- Existing integrations continue to work without changes
- To add new stations, use the new station selection interface
- No need to reconfigure existing integrations

## Troubleshooting

### Station List Not Loading

1. Check internet connection
2. Verify mosecom.mos.ru is accessible
3. Check Home Assistant logs for errors
4. Try restarting Home Assistant

### No Stations in List

1. Check if station pages are accessible
2. Try restarting Home Assistant
3. Parser successfully extracts 55 regular stations and 2 special stations

### Wrong Station Information

1. Station data comes directly from mosecom.mos.ru
2. Report incorrect information to the website administrators
3. Integration displays data as provided by the source