"""
Deduplication validator.
Checks if job codes already exist in existing ward data to prevent duplicates.
"""

import json
import logging
import os

logger = logging.getLogger(__name__)


def load_existing_job_codes(ward_data_dir):
    """
    Load all existing job codes from a ward's works.json.

    Args:
        ward_data_dir: Path to the ward data directory.

    Returns:
        A set of job code strings.
    """
    works_path = os.path.join(ward_data_dir, "works.json")
    if not os.path.isfile(works_path):
        logger.info("No existing works.json found at %s (new ward)", ward_data_dir)
        return set()

    try:
        with open(works_path, "r", encoding="utf-8") as f:
            works = json.load(f)
        codes = {w.get("jobCode") for w in works if w.get("jobCode")}
        logger.info("Loaded %d existing job codes from %s", len(codes), works_path)
        return codes
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning("Failed to load existing works: %s", exc)
        return set()


def find_duplicates(new_records, existing_job_codes):
    """
    Check which new records have job codes that already exist.

    Args:
        new_records: List of new work record dicts (each must have 'jobCode').
        existing_job_codes: Set of existing job code strings.

    Returns:
        A dict with:
            duplicates (list): List of dicts with jobCode and description
                               of each duplicate found.
            duplicate_count (int): Number of duplicates found.
            new_count (int): Number of genuinely new records.
    """
    duplicates = []
    new_count = 0

    for record in new_records:
        job_code = record.get("jobCode")
        if not job_code:
            continue

        if job_code in existing_job_codes:
            duplicates.append({
                "jobCode": job_code,
                "description": record.get("nameOfWork") or record.get("description", ""),
            })
            logger.warning("Duplicate job code found: %s", job_code)
        else:
            new_count += 1

    return {
        "duplicates": duplicates,
        "duplicate_count": len(duplicates),
        "new_count": new_count,
    }


def check_internal_duplicates(records):
    """
    Check for duplicate job codes within the input records themselves.

    Args:
        records: List of work record dicts.

    Returns:
        A dict with:
            duplicates (list): List of job codes appearing more than once.
            has_duplicates (bool): Whether any internal duplicates were found.
    """
    seen = {}
    duplicates = []

    for record in records:
        job_code = record.get("jobCode")
        if not job_code:
            continue

        if job_code in seen:
            if job_code not in duplicates:
                duplicates.append(job_code)
            logger.warning("Internal duplicate job code: %s (appears multiple times in input)", job_code)
        else:
            seen[job_code] = True

    return {
        "duplicates": duplicates,
        "has_duplicates": len(duplicates) > 0,
    }


def deduplicate_records(new_records, ward_data_dir):
    """
    Full deduplication check: both internal and against existing data.

    Args:
        new_records: List of new work record dicts.
        ward_data_dir: Path to the ward data directory.

    Returns:
        A dict with:
            internal_duplicates (list): Job codes duplicated within the input.
            existing_duplicates (list): Records whose job codes already exist.
            clean_records (list): Records that are not duplicates.
    """
    # Check internal duplicates
    internal = check_internal_duplicates(new_records)

    # Load existing and check external duplicates
    existing_codes = load_existing_job_codes(ward_data_dir)
    external = find_duplicates(new_records, existing_codes)

    # Build list of clean (non-duplicate) records
    seen = set()
    clean_records = []
    duplicate_codes = {d["jobCode"] for d in external["duplicates"]}

    for record in new_records:
        job_code = record.get("jobCode")
        if not job_code:
            # Keep records without job codes (will fail other validation)
            clean_records.append(record)
            continue

        if job_code in duplicate_codes:
            continue

        if job_code in seen:
            # Internal duplicate -- skip second occurrence
            continue

        seen.add(job_code)
        clean_records.append(record)

    return {
        "internal_duplicates": internal["duplicates"],
        "existing_duplicates": external["duplicates"],
        "clean_records": clean_records,
    }
