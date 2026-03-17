"""
Normalize contractor names and match against known contractors.
Strips common prefixes/suffixes (M/s, Pvt Ltd, Ltd, etc.) and uses
fuzzy matching to find canonical names.
"""

import json
import logging
import os
import re

from pipeline.utils.fuzzyMatch import fuzzy_match

logger = logging.getLogger(__name__)

# Patterns to strip from contractor names for normalization
STRIP_PATTERNS = [
    r"^m/s\.?\s*",         # M/s or M/s.
    r"^m\.?s\.?\s*",       # Ms or M.S.
    r"^messrs\.?\s*",      # Messrs or Messrs.
    r"\s*pvt\.?\s*ltd\.?$", # Pvt Ltd or Pvt. Ltd.
    r"\s*private\s*limited$",
    r"\s*ltd\.?$",          # Ltd or Ltd.
    r"\s*limited$",
    r"\s*llp$",             # LLP
    r"\s*&\s*co\.?$",       # & Co or & Co.
    r"\s*\(india\)$",       # (India)
    r"\s*\(p\)\s*ltd\.?$",  # (P) Ltd
]

# Compiled patterns for efficiency
_STRIP_COMPILED = [re.compile(p, re.IGNORECASE) for p in STRIP_PATTERNS]


def strip_contractor_name(name):
    """
    Strip common prefixes and suffixes from a contractor name.
    Returns the cleaned name.
    """
    if not name:
        return ""

    cleaned = str(name).strip()

    for pattern in _STRIP_COMPILED:
        cleaned = pattern.sub("", cleaned).strip()

    # Collapse multiple whitespace
    cleaned = " ".join(cleaned.split())

    return cleaned


def normalize_contractor_name(name):
    """
    Normalize a contractor name: strip prefixes/suffixes, title case.
    """
    stripped = strip_contractor_name(name)
    if not stripped:
        return ""
    return stripped.title()


def load_known_contractors(data_dir):
    """
    Load all known contractors from the data/contractors/ directory.

    Returns:
        A list of dicts with keys: contractorId, legalName, strippedName.
    """
    contractors_dir = os.path.join(data_dir, "contractors")
    known = []

    if not os.path.isdir(contractors_dir):
        logger.warning("Contractors directory not found: %s", contractors_dir)
        return known

    for filename in os.listdir(contractors_dir):
        if not filename.endswith(".json"):
            continue

        filepath = os.path.join(contractors_dir, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            known.append({
                "contractorId": data.get("contractorId", ""),
                "legalName": data.get("legalName", ""),
                "strippedName": strip_contractor_name(data.get("legalName", "")),
            })
        except (json.JSONDecodeError, OSError) as exc:
            logger.warning("Failed to load contractor file %s: %s", filepath, exc)

    logger.info("Loaded %d known contractors", len(known))
    return known


def match_contractor(raw_name, known_contractors, threshold=85):
    """
    Match a raw contractor name against known contractors using fuzzy matching.

    Args:
        raw_name: The raw contractor name from the input file.
        known_contractors: List of dicts from load_known_contractors().
        threshold: Minimum fuzzy match score (0-100).

    Returns:
        A dict with:
            canonicalName (str): The matched legal name, or the normalized raw name.
            contractorId (str or None): The matched contractor ID, or None.
            matchScore (int): The fuzzy match score, or 0 if no match.
            matched (bool): Whether a match was found.
    """
    if not raw_name:
        return {
            "canonicalName": "",
            "contractorId": None,
            "matchScore": 0,
            "matched": False,
        }

    stripped = strip_contractor_name(raw_name)

    if not known_contractors:
        return {
            "canonicalName": str(raw_name).strip(),
            "contractorId": None,
            "matchScore": 0,
            "matched": False,
        }

    best, score = fuzzy_match(
        stripped,
        known_contractors,
        threshold=threshold,
        key="strippedName",
    )

    if best is not None:
        logger.debug(
            "Matched contractor '%s' -> '%s' (id=%s, score=%d)",
            raw_name, best["legalName"], best["contractorId"], score,
        )
        return {
            "canonicalName": best["legalName"],
            "contractorId": best["contractorId"],
            "matchScore": score,
            "matched": True,
        }

    logger.info(
        "No contractor match for '%s' (stripped: '%s') above threshold %d",
        raw_name, stripped, threshold,
    )
    return {
        "canonicalName": str(raw_name).strip(),
        "contractorId": None,
        "matchScore": 0,
        "matched": False,
    }
