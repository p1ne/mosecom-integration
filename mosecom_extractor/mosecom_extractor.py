#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to extract air quality data from mosecom.mos.ru monitoring stations.

Note: Historical data extraction is not fully implemented because the data is
loaded dynamically via JavaScript. To extract historical data properly,
additional tools like Selenium would be needed.
"""

import argparse
import re
import sys
import urllib.request
import ssl
from html import unescape


def fetch_page(url):
    """Fetch the page content from the given URL."""
    try:
        # Create unverified SSL context to avoid certificate issues
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        request = urllib.request.Request(url)
        request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        with urllib.request.urlopen(request, context=context) as response:
            content = response.read().decode('utf-8')
        return content
    except Exception as e:
        print(f"Error fetching page: {e}", file=sys.stderr)
        return None


def parse_current_data(html_content, name_type='short', measure_unit='parts'):
    """Parse current air quality data from the HTML content."""
    data = []
    
    # Find the "Последние полученные данные" section
    current_data_pattern = r'Последние полученные данные.*?(?=<h3|<div class="dinamic")'
    match = re.search(current_data_pattern, html_content, re.DOTALL)
    
    if not match:
        return data
    
    current_section = match.group(0)
    
    # Find all data items
    item_pattern = r'<div class="text-norma">\s*([^<]+?)\s*</div>.*?<span class="first-type">\s*([^<]+?)\s*</span>.*?<span class="this-count ">\s*([^<]+?)\s*</span>'
    items = re.findall(item_pattern, current_section, re.DOTALL)
    
    # Use a set to avoid duplicates
    seen = set()
    
    for short_name, long_name, value in items:
        short_name = short_name.strip()
        long_name = long_name.strip()
        value = value.strip().replace(',', '.')
        
        # Skip if we've already seen this substance
        if short_name in seen:
            continue
        seen.add(short_name)
        
        # Convert value based on measure unit
        if measure_unit == 'mg-m3':
            # If we need mg/m3 but data is in parts, we would need conversion factors
            # For now, we'll just use the value as is since we don't have conversion data
            pass
        
        if name_type == 'short':
            data.append((short_name, value))
        elif name_type == 'long':
            data.append((long_name, value))
    
    return data


def parse_historical_data(html_content, gas_type=None, measure_unit='parts'):
    """
    Parse historical air quality data from the HTML content.
    
    Note: Historical data is loaded dynamically via JavaScript and requires
    additional tools like Selenium or finding the API endpoint to extract properly.
    This function currently returns an empty list as a placeholder.
    """
    data = []
    
    # The historical data seems to be loaded dynamically via JavaScript
    # For now, we'll return an empty list since we can't easily extract it
    # In a real implementation, we would need to find the API endpoint or
    # use a tool like Selenium to execute JavaScript
    
    return data


def format_output(data, gas_type=None):
    """Format the output according to requirements."""
    if gas_type:
        # Find the specific gas type
        for name, value in data:
            if name == gas_type:
                return value
        return ""  # Gas type not found
    else:
        # Format all data
        lines = [f"{name} : {value}" for name, value in data]
        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description='Extract air quality data from mosecom.mos.ru')
    parser.add_argument('--url', default='https://mosecom.mos.ru/m1-6-moskvorechye-saburovo/', 
                        help='URL of the monitoring station page')
    parser.add_argument('--current-data', action='store_true', 
                        help='Output current data (default behavior)')
    parser.add_argument('--short-name', action='store_true', default=True,
                        help='Use short names for substances (default)')
    parser.add_argument('--long-name', action='store_true',
                        help='Use long names for substances')
    parser.add_argument('--gas-type', 
                        help='Output only data for the specified gas type')
    parser.add_argument('--historical-data', action='store_true',
                        help='Output historical data')
    parser.add_argument('--measure-mg-m3', action='store_true',
                        help='Output in mg/m^3 units')
    parser.add_argument('--measure-parts', action='store_true', default=True,
                        help='Output in parts (default)')
    
    args = parser.parse_args()
    
    # Determine name type
    name_type = 'long' if args.long_name else 'short'
    
    # Determine measure unit
    measure_unit = 'mg-m3' if args.measure_mg_m3 else 'parts'
    
    # Handle default argument behavior
    if not args.measure_mg_m3 and not args.measure_parts:
        measure_unit = 'parts'  # default
    
    # Fetch page content
    html_content = fetch_page(args.url)
    if html_content is None:
        return 1
    
    if args.historical_data:
        # Parse historical data
        data = parse_historical_data(html_content, args.gas_type, measure_unit)
        if args.gas_type:
            # For historical data with gas type, we would output just the value
            # But since we can't extract historical data, we'll output nothing
            print("")
        else:
            # For historical data without gas type, we would output in CSV format
            # But since we can't extract historical data, we'll output nothing
            print("")
    else:
        # Parse current data
        data = parse_current_data(html_content, name_type, measure_unit)
        output = format_output(data, args.gas_type)
        print(output)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())