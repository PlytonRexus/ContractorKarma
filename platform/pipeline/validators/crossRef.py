"""
Cross-reference validators.
Validate job code prefixes match ward numbers, and road IDs exist.
"""

import json
import logging
import os

from pipeline.normalizers.jobCode import parse_job_code

logger = logging.getLogger(__name__)


def validate_job_code_ward(record, expected_ward_number):
    """
    Validate that a record's job code prefix matches the expected ward number.

    Args:
        record: A dict with at least a 'jobCode' key.
        expected_ward_number: The ward number (int) that all job codes should start with.

    Returns:
        A dict with:
            valid (bool): Whether the check passed.
            error (str or None): Error message if invalid.
    """
    job_code = record.get("jobCode")
    if not job_code:
        return {"valid": False, "error": "Missing jobCode"}

    parsed = parse_job_code(job_code)
    if parsed is None:
        return {"valid": False, "error": f"Invalid jobCode format: '{job_code}'"}

    if parsed["ward"] != int(expected_ward_number):
        return {
            "valid": False,
            "error": (
                f"Job code '{job_code}' has ward prefix {parsed['ward']}, "
                f"expected {expected_ward_number}"
            ),
        }

    return {"valid": True, "error": None}


def validate_road_id_exists(record, known_road_ids):
    """
    Validate that a record's roadId exists in the set of known road IDs.

    Args:
        record: A dict with at least a 'roadId' key.
        known_road_ids: A set or list of valid road ID strings.

    Returns:
        A dict with:
            valid (bool): Whether the check passed.
            error (str or None): Error message if invalid.
    """
    road_id = record.get("roadId")
    if not road_id:
        # Not necessarily an error -- new roads will not have IDs yet
        return {"valid": True, "error": None}

    if road_id not in known_road_ids:
        return {
            "valid": False,
            "error": f"Road ID '{road_id}' not found in known roads",
        }

    return {"valid": True, "error": None}


def load_known_road_ids(ward_data_dir):
    """
    Load the set of known road IDs from a ward's roads.json.

    Args:
        ward_data_dir: Path to the ward data directory.

    Returns:
        A set of road ID strings.
    """
    roads_path = os.path.join(ward_data_dir, "roads.json")
    if not os.path.isfile(roads_path):
        logger.warning("Roads file not found for cross-ref: %s", roads_path)
        return set()

    try:
        with open(roads_path, "r", encoding="utf-8") as f:
            roads = json.load(f)
        return {r.get("roadId") for r in roads if r.get("roadId")}
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning("Failed to load roads for cross-ref: %s", exc)
        return set()


def cross_validate_records(records, expected_ward_number, ward_data_dir):
    """
    Run cross-reference validation on a list of records.

    Args:
        records: List of work record dicts.
        expected_ward_number: The expected ward number.
        ward_data_dir: Path to the ward data directory.

    Returns:
        A dict with:
            valid_count (int): Number of records that passed.
            error_count (int): Number of records with errors.
            errors (list): List of dicts with jobCode and error message.
    """
    known_road_ids = load_known_road_ids(ward_data_dir)

    results = {
        "valid_count": 0,
        "error_count": 0,
        "errors": [],
    }

    for record in records:
        job_code = record.get("jobCode", "unknown")

        ward_check = validate_job_code_ward(record, expected_ward_number)
        if not ward_check["valid"]:
            results["error_count"] += 1
            results["errors"].append({
                "jobCode": job_code,
                "error": ward_check["error"],
            })
            continue

        road_check = validate_road_id_exists(record, known_road_ids)
        if not road_check["valid"]:
            results["error_count"] += 1
            results["errors"].append({
                "jobCode": job_code,
                "error": road_check["error"],
            })
            continue

        results["valid_count"] += 1

    return results
