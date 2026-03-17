"""
Parse Indian currency strings into numeric values.
Handles formats like:
  - "18.5 Lakhs" -> 1850000
  - "2.3 Cr" -> 23000000
  - "Rs. 1,50,000" -> 150000
  - "1850000" -> 1850000
  - "18,50,000" -> 1850000
"""

import logging
import re

logger = logging.getLogger(__name__)

# Multiplier keywords (case-insensitive)
MULTIPLIERS = {
    "cr": 10000000,
    "crore": 10000000,
    "crores": 10000000,
    "l": 100000,
    "lac": 100000,
    "lacs": 100000,
    "lakh": 100000,
    "lakhs": 100000,
    "k": 1000,
    "thousand": 1000,
    "thousands": 1000,
}

# Regex to extract the numeric part and optional multiplier
_CURRENCY_PATTERN = re.compile(
    r"^\s*(?:rs\.?|inr|rupees?)?\s*"   # Optional Rs. / INR / Rupee prefix
    r"([-+]?[\d,]+(?:\.\d+)?)"         # Number with optional commas and decimals
    r"\s*"
    r"(\w+)?"                           # Optional multiplier word
    r"\s*$",
    re.IGNORECASE,
)


def parse_currency(value):
    """
    Parse an Indian currency string or number into a numeric value (float).

    Args:
        value: A string like "18.5 Lakhs", "Rs. 1,50,000", or a number.

    Returns:
        A float representing the amount in base units (rupees).
        Returns None if the value cannot be parsed.
    """
    if value is None:
        return None

    # If already a number, return as float
    if isinstance(value, (int, float)):
        return float(value)

    raw = str(value).strip()
    if not raw:
        return None

    match = _CURRENCY_PATTERN.match(raw)
    if not match:
        # Try a last-resort: strip everything non-numeric and parse
        digits_only = re.sub(r"[^\d.\-+]", "", raw)
        if digits_only:
            try:
                return float(digits_only)
            except ValueError:
                pass

        logger.warning("Could not parse currency value: '%s'", value)
        return None

    number_str = match.group(1)
    multiplier_str = match.group(2)

    # Remove Indian-style commas (e.g., 1,50,000 or 1,500,000)
    number_str = number_str.replace(",", "")

    try:
        amount = float(number_str)
    except ValueError:
        logger.warning("Could not parse number from currency value: '%s'", value)
        return None

    # Apply multiplier if present
    if multiplier_str:
        multiplier_key = multiplier_str.lower()
        if multiplier_key in MULTIPLIERS:
            amount *= MULTIPLIERS[multiplier_key]
        else:
            logger.warning(
                "Unknown currency multiplier '%s' in value '%s'; treating as plain number",
                multiplier_str, value,
            )

    return amount


def format_currency(amount, use_lakhs=False):
    """
    Format a numeric amount as a human-readable Indian currency string.

    Args:
        amount: Numeric amount in rupees.
        use_lakhs: If True, format in lakhs/crores notation.

    Returns:
        Formatted string, e.g. "18.50 Lakhs" or "1,85,000".
    """
    if amount is None:
        return ""

    amount = float(amount)

    if use_lakhs:
        if amount >= 10000000:
            return f"{amount / 10000000:.2f} Cr"
        elif amount >= 100000:
            return f"{amount / 100000:.2f} Lakhs"
        elif amount >= 1000:
            return f"{amount / 1000:.2f} K"
        else:
            return f"{amount:.2f}"

    # Indian number system formatting (e.g. 1,85,000)
    if amount < 0:
        return "-" + format_currency(-amount)

    int_part = int(amount)
    decimal_part = amount - int_part

    s = str(int_part)
    if len(s) <= 3:
        formatted = s
    else:
        last_three = s[-3:]
        remaining = s[:-3]
        # Group remaining digits in pairs from right
        groups = []
        while remaining:
            groups.append(remaining[-2:])
            remaining = remaining[:-2]
        groups.reverse()
        formatted = ",".join(groups) + "," + last_three

    if decimal_part > 0:
        decimal_str = f"{decimal_part:.2f}"[1:]  # Remove leading 0
        formatted += decimal_str

    return formatted
