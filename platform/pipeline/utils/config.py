"""
City-specific configuration for the Contractor Karma pipeline.
Zone names, ward number ranges, DLP defaults by surface type.
"""

import os
from datetime import date

# Base data directory, resolved relative to this file's location
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")

# Reference date for DLP status calculations
TODAY = date(2026, 3, 17)

# Number of days before DLP expiry to flag as "expiringSoon"
DLP_EXPIRING_SOON_DAYS = 180

# Default DLP duration (in years) by surface type
DLP_DEFAULTS = {
    "asphalt": 3,
    "concrete": 5,
    "concretePaving": 5,
    "whiteTopping": 5,
    "potholeRepair": 1,
    "drainRepair": 2,
    "footpath": 3,
}

# Zone abbreviation map  (zoneSlug -> zoneId prefix used in road IDs)
ZONE_ABBREV = {
    "mahadevapura": "mhd",
    "south": "sth",
    "east": "est",
    "west": "wst",
    "yelahanka": "ylk",
    "dasarahalli": "dsh",
    "bommanahalli": "bmh",
    "rajarajeshwari-nagar": "rrn",
}

# City configurations
CITIES = {
    "bengaluru": {
        "cityId": "bengaluru",
        "cityName": "Bengaluru",
        "state": "Karnataka",
        "municipalBody": "BBMP",
        "cityPrefix": "blr",
        "totalZones": 8,
        "totalWards": 243,
        "zones": {
            "mahadevapura": {
                "zoneId": "blr-mhd",
                "zoneName": "Mahadevapura",
                "wardRange": (149, 164),
            },
            "south": {
                "zoneId": "blr-sth",
                "zoneName": "South",
                "wardRange": (161, 188),
            },
            "east": {
                "zoneId": "blr-est",
                "zoneName": "East",
                "wardRange": (57, 84),
            },
            "west": {
                "zoneId": "blr-wst",
                "zoneName": "West",
                "wardRange": (85, 113),
            },
            "yelahanka": {
                "zoneId": "blr-ylk",
                "zoneName": "Yelahanka",
                "wardRange": (1, 28),
            },
            "dasarahalli": {
                "zoneId": "blr-dsh",
                "zoneName": "Dasarahalli",
                "wardRange": (29, 56),
            },
            "bommanahalli": {
                "zoneId": "blr-bmh",
                "zoneName": "Bommanahalli",
                "wardRange": (189, 216),
            },
            "rajarajeshwari-nagar": {
                "zoneId": "blr-rrn",
                "zoneName": "Rajarajeshwari Nagar",
                "wardRange": (113, 148),
            },
        },
    }
}


def get_city_config(city_slug):
    """Return configuration dict for a city, or None if unknown."""
    return CITIES.get(city_slug)


def get_zone_config(city_slug, zone_slug):
    """Return configuration dict for a zone within a city, or None."""
    city = CITIES.get(city_slug)
    if city is None:
        return None
    return city["zones"].get(zone_slug)


def get_zone_id(city_slug, zone_slug):
    """Return the zoneId (e.g. 'blr-sth') for the given city + zone slugs."""
    zone = get_zone_config(city_slug, zone_slug)
    if zone is None:
        return None
    return zone["zoneId"]


def get_ward_data_dir(city_slug, zone_slug, ward_slug):
    """Return the absolute path to a ward's data directory."""
    return os.path.join(
        os.path.abspath(DATA_DIR),
        "cities", city_slug, "zones", zone_slug, "wards", ward_slug,
    )


def get_contractors_dir():
    """Return the absolute path to the contractors data directory."""
    return os.path.join(os.path.abspath(DATA_DIR), "contractors")


def get_stats_dir():
    """Return the absolute path to the stats data directory."""
    return os.path.join(os.path.abspath(DATA_DIR), "stats")


def get_search_dir():
    """Return the absolute path to the search data directory."""
    return os.path.join(os.path.abspath(DATA_DIR), "search")


def get_red_flags_dir():
    """Return the absolute path to the red-flags data directory."""
    return os.path.join(os.path.abspath(DATA_DIR), "red-flags")


def compute_dlp_status(dlp_end_date_str, reference_date=None):
    """
    Compute the DLP status given an end date string (YYYY-MM-DD).
    Returns one of: 'active', 'expiringSoon', 'expired', 'unknown'.
    """
    if not dlp_end_date_str:
        return "unknown"

    ref = reference_date or TODAY

    try:
        end_date = date.fromisoformat(dlp_end_date_str)
    except (ValueError, TypeError):
        return "unknown"

    if end_date < ref:
        return "expired"

    days_remaining = (end_date - ref).days
    if days_remaining <= DLP_EXPIRING_SOON_DAYS:
        return "expiringSoon"

    return "active"


def get_dlp_duration(surface_type):
    """Return the default DLP duration in years for a given surface type."""
    return DLP_DEFAULTS.get(surface_type, 3)
