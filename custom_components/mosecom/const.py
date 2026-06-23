"""Constants for the Moscow Air Quality Monitoring integration."""
from homeassistant.const import CONF_URL, CONF_NAME

DOMAIN = "mosecom"

# Configuration keys
CONF_STATION = "station"

# All possible gas types and their properties
GAS_TYPES = {
    "CO": {
        "name": "Carbon Monoxide",
        "name_ru": "Оксид углерода",
        "unit_mg_m3": "mg/m³",
        "unit_pdk": "% ПДК",
    },
    "NO2": {
        "name": "Nitrogen Dioxide",
        "name_ru": "Диоксид азота",
        "unit_mg_m3": "mg/m³",
        "unit_pdk": "% ПДК",
    },
    "CH4": {
        "name": "Methane",
        "name_ru": "Метан",
        "unit_mg_m3": "mg/m³",
        "unit_pdk": "% ПДК",
    },
    "PM10": {
        "name": "PM10",
        "name_ru": "Взвешенные частицы PM10",
        "unit_mg_m3": "mg/m³",
        "unit_pdk": "% ПДК",
    },
    "NO": {
        "name": "Nitric Oxide",
        "name_ru": "Оксид азота",
        "unit_mg_m3": "mg/m³",
        "unit_pdk": "% ПДК",
    },
    "H2S": {
        "name": "Hydrogen Sulfide",
        "name_ru": "Сероводород",
        "unit_mg_m3": "mg/m³",
        "unit_pdk": "% ПДК",
    },
    "C6H5OH": {
        "name": "Phenol",
        "name_ru": "Фенол",
        "unit_mg_m3": "mg/m³",
        "unit_pdk": "% ПДК",
    },
    "SO2": {
        "name": "Sulfur Dioxide",
        "name_ru": "Диоксид серы",
        "unit_mg_m3": "mg/m³",
        "unit_pdk": "% ПДК",
    },
    "CH2O": {
        "name": "Formaldehyde",
        "name_ru": "Формальдегид",
        "unit_mg_m3": "mg/m³",
        "unit_pdk": "% ПДК",
    },
    "C6H6": {
        "name": "Benzene",
        "name_ru": "Бензол",
        "unit_mg_m3": "mg/m³",
        "unit_pdk": "% ПДК",
    },
    "O3": {
        "name": "Ozone",
        "name_ru": "Озон",
        "unit_mg_m3": "mg/m³",
        "unit_pdk": "% ПДК",
    },
    "C8H8": {
        "name": "Styrene",
        "name_ru": "Стирол",
        "unit_mg_m3": "mg/m³",
        "unit_pdk": "% ПДК",
    },
    "C7H8": {
        "name": "Toluene",
        "name_ru": "Толуол",
        "unit_mg_m3": "mg/m³",
        "unit_pdk": "% ПДК",
    },
}

# Sensor types
SENSOR_TYPE_MG_M3 = "mg_m3"
SENSOR_TYPE_PDK = "pdk"