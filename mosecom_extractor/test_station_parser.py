#!/usr/bin/env python3
"""Test script for station parser."""

import sys
import os

# Add the custom_components directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'custom_components'))

from mosecom.stations import _parse_stations_page, _extract_district_from_class
from mosecom.stations import _clean_address

def test_district_extraction():
    """Test district extraction function."""
    print("Testing district extraction...")
    
    test_cases = [
        ("tsao-row", "ЦАО"),
        ("sao-row", "САО"),
        ("svao-row", "СВАО"),
        ("vao-row", "ВАО"),
        ("yuvao-row", "ЮВАО"),
        ("yuao-row", "ЮАО"),
        ("yuzao-row", "ЮЗАО"),
        ("zao-row", "ЗАО"),
        ("szao-row", "СЗАО"),
        ("zelen-row", "ЗелАО"),
        ("tinao-row", "ТиНАО"),
        ("unknown", ""),
    ]
    
    for css_class, expected in test_cases:
        result = _extract_district_from_class(css_class)
        status = "✓" if result == expected else "✗"
        print(f"{status} {css_class} -> {result} (expected: {expected})")

def test_address_cleaning():
    """Test address cleaning function."""
    print("\nTesting address cleaning...")
    
    test_cases = [
        ("город Москва, 4-я Тверская-Ямская улица, дом 26/8", "4-я Тверская-Ямская улица, дом 26/8"),
        ("г. Москва, улица Хамовнический Вал, дом 24", "улица Хамовнический Вал, дом 24"),
        ("г Москва, Светлый проезд, дом 12", "Светлый проезд, дом 12"),
        ("Москва, Полярная улица, дом 10", "Полярная улица, дом 10"),
        ("г. Новомарьинская улица, дом 7", "Новомарьинская улица, дом 7"),
        ("улица Бутлерова, дом 15", "улица Бутлерова, дом 15"),
    ]
    
    for address, expected in test_cases:
        result = _clean_address(address)
        status = "✓" if result == expected else "✗"
        print(f"{status} {address} -> {result} (expected: {expected})")

def test_station_parsing():
    """Test station parsing with sample HTML."""
    print("\nTesting station parsing...")
    
    # Read the stations page HTML
    try:
        with open('stations_page.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        print("stations_page.html not found, skipping parsing test")
        return
    
    stations = _parse_stations_page(html_content)
    
    print(f"Found {len(stations)} stations")
    
    # Print first 5 stations as examples
    for i, station in enumerate(stations[:5]):
        print(f"{i+1}. {station['name']} - {station['district']} - {station['address'][:50]}... - {station['url']}")
    
    # Check if we have any stations with empty data
    empty_names = [s for s in stations if not s['name']]
    empty_urls = [s for s in stations if not s['url']]
    
    print(f"\nStations with empty names: {len(empty_names)}")
    print(f"Stations with empty URLs: {len(empty_urls)}")

if __name__ == "__main__":
    test_district_extraction()
    test_address_cleaning()
    test_station_parsing()