"""
Parse various Indian date formats and return ISO format strings (YYYY-MM-DD).
Handles:
  - DD/MM/YYYY
  - DD-MM-YYYY
  - DD-MM-YY
  - DD/MM/YY
  - DD-MMM-YYYY (e.g. 15-Mar-2024)
  - "15 March 2024"
  - pandas Timestamp objects
  - Already ISO format (YYYY-MM-DD)
"""

import logging
import re
from datetime import date, datetime

logger = logging.getLogger(__name__)

# Month name mappings (abbreviated and full)
MONTH_NAMES = {
    "jan": 1, "january": 1,
    "feb": 2, "february": 2,
    "mar": 3, "march": 3,
    "apr": 4, "april": 4,
    "may": 5,
    "jun": 6, "june": 6,
    "jul": 7, "july": 7,
    "aug": 8, "august": 8,
    "sep": 9, "sept": 9, "september": 9,
    "oct": 10, "october": 10,
    "nov": 11, "november": 11,
    "dec": 12, "december": 12,
}

# Date parsing patterns (order matters - more specific first)
_PATTERNS = [
    # YYYY-MM-DD (ISO format, already correct)
    (re.compile(r"^(\d{4})-(\d{1,2})-(\d{1,2})$"), "ymd"),
    # DD/MM/YYYY or DD-MM-YYYY
    (re.compile(r"^(\d{1,2})[/\-](\d{1,2})[/\-](\d{4})$"), "dmy4"),
    # DD/MM/YY or DD-MM-YY
    (re.compile(r"^(\d{1,2})[/\-](\d{1,2})[/\-](\d{2})$"), "dmy2"),
    # DD-MMM-YYYY (e.g. 15-Mar-2024)
    (re.compile(r"^(\d{1,2})[/\-\s](\w{3,9})[/\-\s](\d{4})$", re.IGNORECASE), "dMy4"),
    # DD-MMM-YY (e.g. 15-Mar-24)
    (re.compile(r"^(\d{1,2})[/\-\s](\w{3,9})[/\-\s](\d{2})$", re.IGNORECASE), "dMy2"),
    # "15 March 2024" or "March 15, 2024"
    (re.compile(r"^(\w{3,9})\s+(\d{1,2}),?\s+(\d{4})$", re.IGNORECASE), "Mdy4"),
]


def _expand_year(year_short):
    """Expand a 2-digit year to 4-digit. Assumes 00-49 -> 2000s, 50-99 -> 1900s."""
    y = int(year_short)
    if y < 50:
        return 2000 + y
    return 1900 + y


def _month_from_name(name):
    """Get month number from month name (abbreviated or full)."""
    return MONTH_NAMES.get(name.lower())


def parse_date(value):
    """
    Parse a date value from various formats into an ISO date string (YYYY-MM-DD).

    Args:
        value: A string, datetime, date, or pandas Timestamp.

    Returns:
        ISO format date string (YYYY-MM-DD), or None if parsing fails.
    """
    if value is None:
        return None

    # Handle datetime/date objects directly
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d")
    if isinstance(value, date):
        return value.isoformat()

    # Handle pandas Timestamp (has isoformat method)
    if hasattr(value, "isoformat") and hasattr(value, "year"):
        try:
            return value.strftime("%Y-%m-%d")
        except (ValueError, AttributeError):
            pass

    raw = str(value).strip()
    if not raw or raw.lower() in ("nan", "nat", "none", "null", "-", "n/a"):
        return None

    for pattern, fmt in _PATTERNS:
        match = pattern.match(raw)
        if not match:
            continue

        try:
            if fmt == "ymd":
                y, m, d = int(match.group(1)), int(match.group(2)), int(match.group(3))
            elif fmt == "dmy4":
                d, m, y = int(match.group(1)), int(match.group(2)), int(match.group(3))
            elif fmt == "dmy2":
                d, m = int(match.group(1)), int(match.group(2))
                y = _expand_year(match.group(3))
            elif fmt == "dMy4":
                d = int(match.group(1))
                m = _month_from_name(match.group(2))
                y = int(match.group(3))
                if m is None:
                    continue
            elif fmt == "dMy2":
                d = int(match.group(1))
                m = _month_from_name(match.group(2))
                y = _expand_year(match.group(3))
                if m is None:
                    continue
            elif fmt == "Mdy4":
                m = _month_from_name(match.group(1))
                d = int(match.group(2))
                y = int(match.group(3))
                if m is None:
                    continue
            else:
                continue

            # Validate the date
            parsed_date = date(y, m, d)
            return parsed_date.isoformat()

        except (ValueError, TypeError):
            continue

    logger.warning("Could not parse date: '%s'", value)
    return None


def parse_date_or_warn(value, field_name="date"):
    """
    Parse a date, logging a warning with context if it fails.

    Returns:
        Tuple of (iso_string_or_None, warning_message_or_None).
    """
    result = parse_date(value)
    if result is None and value is not None:
        raw = str(value).strip()
        if raw and raw.lower() not in ("nan", "nat", "none", "null", "-", "n/a"):
            warning = f"Could not parse {field_name}: '{value}'"
            return None, warning
    return result, None
