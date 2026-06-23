# UI Configuration Guide

This guide explains how to configure the Moscow Air Quality Monitoring integration using the Home Assistant web interface.

## Overview

The integration supports a simple, user-friendly configuration flow through the Home Assistant UI. You can add multiple monitoring stations, and each station will automatically detect which gases it measures and create the appropriate sensors.

## Configuration Flow

### Step 1: Access the Integration Setup

1. Open Home Assistant in your web browser
2. Navigate to **Settings** → **Devices & Services**
3. Click the **+ Add Integration** button
4. In the search box, type "Moscow Air Quality Monitoring"
5. Click on the integration when it appears

### Step 2: Enter Station Details

You'll see a configuration form with the following fields:

#### Station URL (Required)
- Enter the full URL of the monitoring station page from mosecom.mos.ru
- Example: `https://mosecom.mos.ru/m1-6-moskvorechye-saburovo/`
- The URL must start with `http://` or `https://`
- The integration will validate that the URL is accessible

#### Location Name (Optional)
- Enter a custom name for this monitoring location
- If left blank, the name will be automatically extracted from the URL
- Example: If you enter "Home Station", sensors will be named `sensor.mosecom_home_station_co`
- If left blank for URL `https://mosecom.mos.ru/m1-6-moskvorechye-saburovo/`, it becomes "Moskvorechye Saburovo"

### Step 3: Validation and Gas Detection

After you submit the form:

1. The integration will attempt to connect to the monitoring station
2. If successful, it will parse the page to detect which gases are measured
3. You'll see a confirmation showing which gases were detected
4. Example: "Available gases: CO, NO2, CH4, PM10, NO, H2S"

### Step 4: Complete Setup

1. Review the detected gases
2. Click **Finish** to complete the setup
3. The integration will create sensors for each detected gas
4. Each gas will have two sensors: one for mg/m³ and one for % ПДК

## Adding Multiple Stations

You can add multiple monitoring stations to monitor different locations:

### Why Add Multiple Stations?

- Monitor air quality at different locations (home, work, school)
- Compare air quality across different areas of Moscow
- Some stations measure different gases than others
- Create comprehensive air quality monitoring network

### How to Add Multiple Stations

1. Follow the same configuration flow for each station
2. Each station must have a unique URL
3. Each station will be added as a separate integration instance
4. Each station will have its own set of sensors based on the gases it measures

### Example: Multiple Station Setup

**Station 1: Home Location**
- URL: `https://mosecom.mos.ru/m1-6-moskvorechye-saburovo/`
- Name: "Home"
- Detected gases: CO, NO2, CH4, PM10, NO, H2S
- Creates 12 sensors

**Station 2: Work Location**
- URL: `https://mosecom.mos.ru/ploshhad-gagarina/`
- Name: "Work"
- Detected gases: C6H5OH, SO2, CH2O, C6H6, O3, NO2, C8H8, C7H8
- Creates 16 sensors

**Station 3: School Location**
- URL: `https://mosecom.mos.ru/butovo/`
- Name: "School"
- Detected gases: CO, NO2, PM10
- Creates 6 sensors

Total: 3 integration instances, 34 sensors

## Finding Station URLs

### Method 1: Using the Mosecom Website

1. Go to [https://mosecom.mos.ru](https://mosecom.mos.ru)
2. You'll see a map of Moscow with monitoring stations
3. Click on a station marker to see its details
4. Click on the station name or "More details" link
5. Copy the URL from your browser's address bar
6. Use this URL in the integration configuration

### Method 2: Direct URL Navigation

If you know the station identifier, you can construct the URL directly:

- Format: `https://mosecom.mos.ru/<station-identifier>/`
- Example: `https://mosecom.mos.ru/m1-6-moskvorechye-saburovo/`

### Popular Station URLs

Here are some commonly used monitoring stations:

- **Moskvorechye-Saburovo**: `https://mosecom.mos.ru/m1-6-moskvorechye-saburovo/`
- **Gagarin Square**: `https://mosecom.mos.ru/ploshhad-gagarina/`
- **Butovo**: `https://mosecom.mos.ru/butovo/`
- **Kurkino**: `https://mosecom.mos.ru/kurkino/`
- **Marfino**: `https://mosecom.mos.ru/marfino/`
- **Biryulyovo**: `https://mosecom.mos.ru/biryulyovo/`

## Managing Configured Stations

### Viewing All Stations

1. Go to **Settings** → **Devices & Services**
2. Look for "Moscow Air Quality Monitoring" in the integrations list
3. You'll see the number of configured stations (e.g., "Moscow Air Quality Monitoring (3)")
4. Click on it to see all individual station entries

### Station Information

Each station entry shows:
- Station name
- Number of sensors
- Status (connected/disconnected)
- Last update time

### Reconfiguring a Station

1. Go to **Settings** → **Devices & Services**
2. Find the station you want to reconfigure
3. Click on the station entry
4. Click the **Configure** button
5. Update the URL or name as needed
6. Click **Submit** to save changes

### Removing a Station

1. Go to **Settings** → **Devices & Services**
2. Find the station you want to remove
3. Click on the station entry
4. Click the three dots (⋮) in the top right corner
5. Select **Delete**
6. Confirm the deletion
7. All sensors for that station will be removed

## Error Handling

### Invalid URL Format

**Error**: "Invalid URL format"

**Solution**: 
- Make sure the URL starts with `http://` or `https://`
- Check for typos in the URL
- Ensure the URL is complete (don't forget the trailing slash)

### Cannot Connect

**Error**: "Failed to connect to the monitoring station"

**Solution**:
- Verify the URL is correct by opening it in a web browser
- Check your internet connection
- Ensure the mosecom.mos.ru website is accessible
- Try again later if the website is temporarily down

### Already Configured

**Error**: "This monitoring station is already configured"

**Solution**:
- Each station URL can only be added once
- If you want to reconfigure, use the "Configure" option on the existing entry
- If you want to remove and re-add, delete the existing entry first

### Unknown Error

**Error**: "Unknown error occurred"

**Solution**:
- Check the Home Assistant logs for detailed error messages
- Try again after a few minutes
- Ensure you're using a compatible version of Home Assistant

## Tips and Best Practices

### Naming Conventions

- Use descriptive names for your locations: "Home", "Work", "School"
- Avoid special characters in names
- Shorter names create shorter sensor entity IDs
- Consistent naming makes automations easier to write

### Station Selection

- Choose stations closest to your locations of interest
- Consider which gases are most important to you
- Some stations measure more gases than others
- Check the station page on mosecom.mos.ru to see what's measured

### Performance Considerations

- Each station updates independently every 5 minutes
- Adding many stations won't significantly impact performance
- Each station creates 2 sensors per detected gas
- Consider your needs when adding multiple stations

### Automation Examples

**Monitor high CO levels at home:**
```yaml
automation:
  - alias: "High CO at Home"
    trigger:
      - platform: numeric_state
        entity_id: sensor.mosecom_home_co
        above: 5
    action:
      - service: notify.mobile_app_your_phone
        data:
          message: "High CO level at home: {{ states('sensor.mosecom_home_co') }} mg/m³"
```

**Compare air quality between locations:**
```yaml
sensor:
  - platform: template
    sensors:
      best_air_quality_location:
        friendly_name: "Best Air Quality Location"
        value_template: >
          {% if states('sensor.mosecom_home_co_pdk')|float < states('sensor.mosecom_work_co_pdk')|float %}
            Home
          {% else %}
            Work
          {% endif %}
```

## Troubleshooting

### Integration Not Appearing in Search

1. Make sure the integration files are in the correct directory
2. Restart Home Assistant
3. Clear your browser cache
4. Try refreshing the integrations page

### Sensors Not Showing Up

1. Check that the integration was successfully added
2. Look at the integration description to see which gases were detected
3. If no gases were detected, the station might not be reporting data
4. Check Home Assistant logs for errors

### Sensors Showing "Unknown"

1. Wait for the first data update (up to 5 minutes)
2. Check if the monitoring station website is accessible
3. Try reloading the integration
4. Check Home Assistant logs for connection errors

### Wrong Location Name

1. Go to the integration configuration
2. Click "Configure" on the station entry
3. Update the location name
4. Submit the changes
5. Note: This won't rename existing sensors, only new ones

## Support

For additional help:
- Check the main README.md for general information
- Review the DYNAMIC_GAS_DETECTION.md for details on gas detection
- Check Home Assistant logs for detailed error messages
- Visit the GitHub repository for issues and feature requests