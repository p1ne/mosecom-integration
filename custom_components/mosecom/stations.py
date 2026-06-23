"""Station data fetching and parsing for Moscow Air Quality Monitoring integration."""
from __future__ import annotations

import logging
import re
import ssl
from typing import Any

try:
    import aiohttp
except ImportError:
    aiohttp = None

_LOGGER = logging.getLogger(__name__)

# Create SSL context that doesn't verify certificates (for mosecom.mos.ru)
SSL_CONTEXT = ssl.create_default_context()
SSL_CONTEXT.check_hostname = False
SSL_CONTEXT.verify_mode = ssl.CERT_NONE



async def fetch_stations(hass) -> list[dict[str, Any]]:
    """Fetch all stations from both regular and special stations pages."""
    if aiohttp is None:
        _LOGGER.error("aiohttp is not available")
        return []
    stations = []
    
    try:
        async with aiohttp.ClientSession() as session:
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
            
    except Exception as err:
        _LOGGER.error("Error fetching stations: %s", err)
    
    return stations


async def _fetch_page_stations(session, url: str) -> list[dict[str, Any]]:
    """Fetch stations from a specific page."""
    stations = []
    
    try:
        async with session.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            },
            ssl=SSL_CONTEXT,
        ) as response:
            if response.status != 200:
                _LOGGER.error("Error fetching %s: status %d", url, response.status)
                return stations
            
            html_content = await response.text()
            stations = _parse_stations_page(html_content)
            
    except Exception as err:
        _LOGGER.error("Error fetching %s: %s", url, err)
    
    return stations


def _parse_stations_page(html_content: str) -> list[dict[str, Any]]:
    """Parse stations from HTML content."""
    stations = []
    
    # Look for station rows in the allstan-item-row divs
    # Pattern to match station rows with name, address, and extract district from CSS class
    row_pattern = r'<div class="allstan-item-row ([^"]*?)(?:-row)?">.*?<div class="row-title">\s*<a href="([^"]*)"[^>]*>\s*<img[^>]*>\s*([^<]*)\s*</a>\s*</div>\s*<div class="row-address">\s*<img[^>]*>\s*([^<]*)\s*</div>'
    matches = re.findall(row_pattern, html_content, re.DOTALL)
    
    for district_class, url, name, address in matches:
        # Clean up the data
        clean_name = name.strip()
        clean_address = _clean_address(address)
        
        # Extract district from CSS class (e.g., 'tsao-row' -> 'ЦАО')
        clean_district = _extract_district_from_class(district_class)
        
        # Make URL absolute if needed
        if url.startswith('/'):
            full_url = f"https://mosecom.mos.ru{url}"
        elif not url.startswith('http'):
            full_url = f"https://mosecom.mos.ru/{url}"
        else:
            full_url = url
        
        # Only add if we have a valid URL and name
        if clean_name and full_url:
            stations.append({
                "name": clean_name,
                "address": clean_address,
                "district": clean_district,
                "url": full_url
            })
    
    # If no stations found with the specific pattern, try the general approach
    if not stations:
        _LOGGER.info("Trying general approach to find stations")
        general_pattern = r'<a[^>]*href="(https?://mosecom\.mos\.ru/[^"]*)"[^>]*>([^<]+)</a>'
        general_matches = re.findall(general_pattern, html_content, re.DOTALL)
        
        for url, name in general_matches:
            # Filter out navigation links
            if any(skip in name.lower() for skip in ['карта', 'главная', 'контакты', 'о проекте', 'новости']):
                continue
                
            clean_name = name.strip()
            if clean_name and '/m' in url:  # Station URLs typically contain /m followed by station ID
                stations.append({
                    "name": clean_name,
                    "address": "",
                    "district": "",
                    "url": url
                })
    
    return stations


def _extract_district_from_class(css_class: str) -> str:
    """Extract district name from CSS class."""
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
    
    # Extract district code from class (e.g., 'tsao-row' -> 'tsao')
    district_code = css_class.split('-')[0] if '-' in css_class else css_class
    
    return district_mapping.get(district_code, "")


def _clean_address(address: str) -> str:
    """Clean address by removing Moscow prefixes."""
    if not address:
        return ""
    
    clean_address = address.strip()
    
    # Remove common Moscow prefixes
    prefixes = [
        'город Москва,',
        'г. Москва,',
        'г Москва,',
        'Москва,',
        'г.',
    ]
    
    for prefix in prefixes:
        if clean_address.startswith(prefix):
            clean_address = clean_address[len(prefix):].strip()
            break
    
    # Clean up extra whitespace and punctuation at the start
    clean_address = re.sub(r'^[,\.\s]+', '', clean_address)
    
    return clean_address
