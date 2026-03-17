"""
Normalize and validate job codes.
Expected format: XXX-YY-NNNNNN  (ward-year-serial)
Example: 176-21-000001
"""

import logging
import re

logger = logging.getLogger(__name__)

# Regex for standard job code format: ward (2-3 digits) - year (2 digits) - serial (6 digits)
JOB_CODE_PATTERN = re.compile(r"^(\d{2,3})-(\d{2})-(\d{6})$")


def parse_job_code(job_code):
    """
    Parse a job code string into its components.

    Args:
        job_code: Raw job code string, e.g. "176-21-000001".

    Returns:
        A dict with keys: ward, year, serial, normalized.
        Returns None if the job code is invalid.
    """
    if not job_code:
        return None

    raw = str(job_code).strip()
    match = JOB_CODE_PATTERN.match(raw)

    if not match:
        logger.warning("Invalid job code format: '%s' (expected XXX-YY-NNNNNN)", raw)
        return None

    ward_str = match.group(1)
    year_str = match.group(2)
    serial_str = match.group(3)

    ward_number = int(ward_str)
    year_short = int(year_str)
    serial = int(serial_str)

    # Reconstruct the full year (20xx)
    full_year = 2000 + year_short

    # Normalize to consistent format (3-digit ward if needed, but preserve original width)
    normalized = f"{ward_number}-{year_str}-{serial_str}"

    return {
        "ward": ward_number,
        "year": full_year,
        "yearShort": year_str,
        "serial": serial,
        "normalized": normalized,
    }


def validate_job_code(job_code, expected_ward=None):
    """
    Validate a job code and optionally check that the ward prefix matches.

    Args:
        job_code: Raw job code string.
        expected_ward: Expected ward number (int or string). If provided,
                       the ward prefix in the job code must match.

    Returns:
        A dict with:
            valid (bool): Whether the job code is valid.
            parsed (dict or None): Parsed components if valid.
            errors (list): List of error messages.
            warnings (list): List of warning messages.
    """
    result = {
        "valid": True,
        "parsed": None,
        "errors": [],
        "warnings": [],
    }

    parsed = parse_job_code(job_code)

    if parsed is None:
        result["valid"] = False
        result["errors"].append(
            f"Invalid job code format: '{job_code}'. Expected XXX-YY-NNNNNN"
        )
        return result

    result["parsed"] = parsed

    # Check year is reasonable (2015-2030)
    if parsed["year"] < 2015 or parsed["year"] > 2030:
        result["warnings"].append(
            f"Job code year {parsed['year']} is outside expected range (2015-2030)"
        )

    # Check ward prefix if expected_ward is provided
    if expected_ward is not None:
        expected = int(expected_ward)
        if parsed["ward"] != expected:
            result["valid"] = False
            result["errors"].append(
                f"Job code ward prefix {parsed['ward']} does not match "
                f"expected ward {expected}"
            )

    return result


def normalize_job_code(job_code):
    """
    Return the normalized form of a job code, or None if invalid.
    """
    parsed = parse_job_code(job_code)
    if parsed is None:
        return None
    return parsed["normalized"]
