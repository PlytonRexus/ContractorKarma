"""
Normalize road names: canonicalize to title case, strip extra whitespace,
manage aliases, and match against known roads.
"""

import json
import logging
import os
import re

from pipeline.utils.fuzzyMatch import fuzzy_match

logger = logging.getLogger(__name__)

# Common abbreviations to expand for canonical form
ABBREVIATIONS = {
    r"\brd\b": "Road",
    r"\bst\b": "Street",
    r"\bave\b": "Avenue",
    r"\bdr\b": "Drive",
    r"\bcr\b": "Cross",
    r"\bmn\b": "Main",
    r"\bblk\b": "Block",
    r"\bjn\b": "Jayanagar",
    r"\bbtm\b": "BTM",
    r"\birr\b": "IRR",
    r"\bext\b": "Extension",
}


def canonicalize_road_name(name):
    """
    Canonicalize a road name:
      - Strip leading/trailing whitespace
      - Collapse multiple whitespace to single space
      - Title case
      - Expand common abbreviations

    Args:
        name: Raw road name string.

    Returns:
        Canonicalized road name string.
    """
    if not name:
        return ""

    cleaned = str(name).strip()

    # Collapse multiple whitespace
    cleaned = " ".join(cleaned.split())

    # Title case first
    cleaned = cleaned.title()

    # Expand abbreviations (case-insensitive match, replace with proper case)
    for pattern, replacement in ABBREVIATIONS.items():
        cleaned = re.sub(pattern, replacement, cleaned, flags=re.IGNORECASE)

    return cleaned


def load_known_roads(ward_data_dir):
    """
    Load known roads from a ward's roads.json file.

    Args:
        ward_data_dir: Path to the ward data directory.

    Returns:
        A list of dicts with keys: roadId, roadName, aliases.
    """
    roads_path = os.path.join(ward_data_dir, "roads.json")
    known = []

    if not os.path.isfile(roads_path):
        logger.warning("Roads file not found: %s", roads_path)
        return known

    try:
        with open(roads_path, "r", encoding="utf-8") as f:
            roads = json.load(f)

        for road in roads:
            known.append({
                "roadId": road.get("roadId", ""),
                "roadName": road.get("roadName", ""),
                "aliases": road.get("aliases", []),
            })
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning("Failed to load roads file %s: %s", roads_path, exc)

    logger.info("Loaded %d known roads from %s", len(known), roads_path)
    return known


def match_road(raw_name, known_roads, threshold=80):
    """
    Match a raw road name against known roads using fuzzy matching.
    Checks both the canonical roadName and all aliases.

    Args:
        raw_name: The raw road name to match.
        known_roads: List of dicts from load_known_roads().
        threshold: Minimum fuzzy match score (0-100).

    Returns:
        A dict with:
            roadId (str or None): The matched road ID.
            roadName (str): The canonical road name.
            matchScore (int): The best fuzzy match score.
            matched (bool): Whether a match was found.
    """
    if not raw_name or not known_roads:
        return {
            "roadId": None,
            "roadName": canonicalize_road_name(raw_name),
            "matchScore": 0,
            "matched": False,
        }

    canonical = canonicalize_road_name(raw_name)

    # Build a flat list of (road_dict, candidate_string) pairs
    candidates = []
    for road in known_roads:
        candidates.append((road, road["roadName"]))
        for alias in road.get("aliases", []):
            candidates.append((road, alias))

    # Extract just the strings for fuzzy matching
    candidate_strings = [c[1] for c in candidates]

    best, score = fuzzy_match(canonical, candidate_strings, threshold=threshold)

    if best is not None:
        # Find the road dict that this string belongs to
        for road, candidate_str in candidates:
            if candidate_str == best:
                logger.debug(
                    "Matched road '%s' -> '%s' (id=%s, score=%d)",
                    raw_name, road["roadName"], road["roadId"], score,
                )
                return {
                    "roadId": road["roadId"],
                    "roadName": road["roadName"],
                    "matchScore": score,
                    "matched": True,
                }

    logger.info("No road match for '%s' above threshold %d", raw_name, threshold)
    return {
        "roadId": None,
        "roadName": canonical,
        "matchScore": 0,
        "matched": False,
    }
