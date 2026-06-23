# Installation Guide for Moscow Air Quality Monitoring Integration

## Method 1: Manual Installation

1. **Download the integration files**
   - Download the entire `custom_components/mosecom` directory
   - Make sure you have all the required files:
     - `__init__.py`
     - `manifest.json`
     - `config_flow.py`
     - `const.py`
     - `coordinator.py`
     - `sensor.py`
     - `strings.json`
     - `services.yaml`
     - `hacs.json`

2. **Copy files to Home Assistant**
   - Access your Home Assistant files (via Samba, SSH, or the File Editor add-on)
   - Navigate to the `custom_components` directory
   - If it doesn't exist, create it: `mkdir custom_components`
   - Copy the `mosecom` directory into `custom_components`

3. **Restart Home Assistant**
   - Go to **Settings** → **System** → **Restart**
   - Or restart via the command line: `hassio.host.restart`

4. **Add the integration**
   - Go to **Settings** → **Devices & Services**
   - Click **Add Integration**
   - Search for "Moscow Air Quality Monitoring"
   - Click on it
   - Select a monitoring station from the list
   - Optionally provide a custom name for the device
   - Click **Submit**

## Method 2: Installation via HACS (Home Assistant Community Store)

1. **Install HACS** (if not already installed)
   - Follow the official HACS installation guide: https://hacs.xyz/docs/setup/start

2. **Add this integration to HACS**
   - Open HACS in Home Assistant
   - Go to **Settings** → **Custom Repositories**
   - Click **Add**
   - Enter the repository URL: `https://github.com/p1ne/mosecom`
   - Select category: **Integration**
   - Click **Add**

3. **Install the integration**
   - Go to **HACS** → **Integrations**
   - Find "Moscow Air Quality Monitoring"
   - Click **Download**
   - Click **Download** again to confirm
   - Wait for the installation to complete

4. **Restart Home Assistant**
   - Click **Restart** in the HACS dialog
   - Or restart manually: **Settings** → **System** → **Restart**

5. **Add the integration**
   - Follow the same steps as in Method 1, step 4

## Method 3: Installation via Terminal/SSH

1. **Access your Home Assistant via SSH**
   ```bash
   ssh homeassistant@your-home-assistant-ip
   ```

2. **Navigate to the custom_components directory**
   ```bash
   cd /home/homeassistant/.homeassistant/custom_components
   ```

3. **Clone or download the integration**
   ```bash
   # If you have git installed
   git clone https://github.com/p1ne/mosecom.git mosecom
   
   # Or download and extract manually
   wget https://github.com/p1ne/mosecom/archive/main.zip
   unzip main.zip
   mv mosecom-main mosecom
   ```

4. **Set correct permissions**
   ```bash
   chown -R homeassistant:homeassistant mosecom
   chmod -R 755 mosecom
   ```

5. **Restart Home Assistant**
   ```bash
   hassio.host.restart
   ```

6. **Add the integration** (same as Method 1, step 4)

## Station Selection

To find the URL for your desired monitoring station:

1. Visit https://mosecom.mos.ru/
2. Navigate to the monitoring station you want to monitor
3. Copy the URL from your browser's address bar
4. Use this URL when setting up the integration

Example URLs:
- https://mosecom.mos.ru/m1-6-moskvorechye-saburovo/
- https://mosecom.mos.ru/m1-1-bibirevo/
- https://mosecom.mos.ru/m1-2-losinyj-ostrov/

## Verification

After installation, verify that everything is working:

1. **Check the integration**
   - Go to **Settings** → **Devices & Services**
   - You should see "Moscow Air Quality Monitoring" in the list
   - Click on it to see the configured devices

2. **Check the sensors**
   - Go to **Settings** → **Entities**
   - Search for sensors starting with "sensor.{location_name}_, e.g., "sensor.moskvorechye_saburovo_"
   - You should see sensors for each gas type with both mg/m³ and % ПДК units

3. **Check the device**
   - Go to **Settings** → **Devices**
   - You should see a device named "Mosecom {Your Location Name}"
   - Click on it to see all associated sensors

## Troubleshooting

### Integration not appearing

1. Check that all files are in the correct location:
   ```
   /home/homeassistant/.homeassistant/custom_components/mosecom/
   ```

2. Check the Home Assistant logs:
   - Go to **Settings** → **System** → **Logs**
   - Look for errors related to "mosecom"

3. Make sure you've restarted Home Assistant after installation

### Sensors showing unavailable

1. Check that the monitoring station URL is correct
2. Verify your internet connection
3. Check if the monitoring station website is accessible
4. Look at the integration logs for specific error messages

### Permission errors

1. Make sure the files have correct permissions:
   ```bash
   chown -R homeassistant:homeassistant /home/homeassistant/.homeassistant/custom_components/mosecom
   chmod -R 755 /home/homeassistant/.homeassistant/custom_components/mosecom
   ```

### Import errors

1. Make sure all required files are present
2. Check that Python dependencies are satisfied (none required for this integration)
3. Verify that you're using a compatible version of Home Assistant (2023.1.0 or later)

## Updating the Integration

### Manual Update

1. Download the latest version of the integration
2. Replace the files in `custom_components/mosecom`
3. Restart Home Assistant

### HACS Update

1. Open HACS
2. Go to **Integrations**
3. Find "Moscow Air Quality Monitoring"
4. Click **Update**
5. Restart Home Assistant when prompted

## Uninstallation

1. **Remove the integration**
   - Go to **Settings** → **Devices & Services**
   - Find "Moscow Air Quality Monitoring"
   - Click on it
   - Click **Delete**
   - Confirm deletion

2. **Remove the files**
   - Delete the `custom_components/mosecom` directory
   - Restart Home Assistant

## Support

For issues, questions, or feature requests:
- GitHub Issues: https://github.com/p1ne/mosecom/issues
- Check the main README.md for usage examples and troubleshooting tips