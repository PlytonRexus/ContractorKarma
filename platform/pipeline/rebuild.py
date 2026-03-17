"""
Rebuild all derived data files from existing ward-level data.
Does not require an input file -- reads existing data/ files and regenerates:
  - stats/summary.json
  - stats/contractor-rankings.json
  - stats/ward-rankings.json
  - search/index.json
  - red-flags/flags.json

Usage:
  python -m pipeline.rebuild
  python -m pipeline.rebuild --data-dir /path/to/data
"""

import argparse
import json
import logging
import os
import sys

from pipeline.generators.redFlags import generate_red_flags
from pipeline.generators.stats import (
    compute_summary, compute_contractor_rankings, compute_ward_rankings,
)
from pipeline.generators.search import generate_search_index
from pipeline.utils.config import DATA_DIR, TODAY

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def _write_json(file_path, data):
    """Write data to a JSON file, creating directories as needed."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    logger.info("Wrote: %s", file_path)


def _load_json(file_path):
    """Load a JSON file, returning None on failure."""
    if not os.path.isfile(file_path):
        return None
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning("Failed to load %s: %s", file_path, exc)
        return None


def collect_all_works(data_dir):
    """
    Collect all work records from all ward directories.

    Returns:
        A list of all work dicts.
    """
    all_works = []
    cities_dir = os.path.join(data_dir, "cities")

    if not os.path.isdir(cities_dir):
        logger.warning("Cities directory not found: %s", cities_dir)
        return all_works

    for city_slug in sorted(os.listdir(cities_dir)):
        zones_dir = os.path.join(cities_dir, city_slug, "zones")
        if not os.path.isdir(zones_dir):
            continue

        for zone_slug in sorted(os.listdir(zones_dir)):
            wards_dir = os.path.join(zones_dir, zone_slug, "wards")
            if not os.path.isdir(wards_dir):
                continue

            for ward_slug in sorted(os.listdir(wards_dir)):
                works_path = os.path.join(wards_dir, ward_slug, "works.json")
                works = _load_json(works_path)
                if works and isinstance(works, list):
                    all_works.extend(works)
                    logger.debug(
                        "Loaded %d works from %s/%s/%s",
                        len(works), city_slug, zone_slug, ward_slug,
                    )

    logger.info("Collected %d total works across all wards", len(all_works))
    return all_works


def collect_all_roads(data_dir):
    """
    Collect all road records from all ward directories.

    Returns:
        A list of all road dicts.
    """
    all_roads = []
    cities_dir = os.path.join(data_dir, "cities")

    if not os.path.isdir(cities_dir):
        return all_roads

    for city_slug in sorted(os.listdir(cities_dir)):
        zones_dir = os.path.join(cities_dir, city_slug, "zones")
        if not os.path.isdir(zones_dir):
            continue

        for zone_slug in sorted(os.listdir(zones_dir)):
            wards_dir = os.path.join(zones_dir, zone_slug, "wards")
            if not os.path.isdir(wards_dir):
                continue

            for ward_slug in sorted(os.listdir(wards_dir)):
                roads_path = os.path.join(wards_dir, ward_slug, "roads.json")
                roads = _load_json(roads_path)
                if roads and isinstance(roads, list):
                    all_roads.extend(roads)

    logger.info("Collected %d total roads across all wards", len(all_roads))
    return all_roads


def collect_all_contractors(data_dir):
    """
    Collect all contractor records.

    Returns:
        A list of contractor summary dicts.
    """
    contractors = []
    contractors_dir = os.path.join(data_dir, "contractors")

    if not os.path.isdir(contractors_dir):
        return contractors

    for filename in sorted(os.listdir(contractors_dir)):
        if not filename.endswith(".json") or filename == "index.json":
            continue

        data = _load_json(os.path.join(contractors_dir, filename))
        if data:
            contractors.append(data)

    logger.info("Collected %d contractors", len(contractors))
    return contractors


def count_structure(data_dir):
    """Count cities, zones, and wards in the data directory."""
    cities = 0
    zones = 0
    wards = 0

    cities_dir = os.path.join(data_dir, "cities")
    if not os.path.isdir(cities_dir):
        return cities, zones, wards

    for city_slug in os.listdir(cities_dir):
        city_path = os.path.join(cities_dir, city_slug)
        if not os.path.isdir(city_path):
            continue
        cities += 1

        zones_dir = os.path.join(city_path, "zones")
        if not os.path.isdir(zones_dir):
            continue

        for zone_slug in os.listdir(zones_dir):
            zone_path = os.path.join(zones_dir, zone_slug)
            if not os.path.isdir(zone_path):
                continue
            zones += 1

            wards_dir = os.path.join(zone_path, "wards")
            if not os.path.isdir(wards_dir):
                continue

            for ward_slug in os.listdir(wards_dir):
                ward_path = os.path.join(wards_dir, ward_slug)
                if os.path.isdir(ward_path):
                    wards += 1

    return cities, zones, wards


def rebuild_all(data_dir=None):
    """
    Rebuild all derived data files from existing ward-level data.

    Args:
        data_dir: Path to the root data directory. Uses default if None.
    """
    if data_dir is None:
        data_dir = os.path.abspath(DATA_DIR)

    logger.info("=" * 60)
    logger.info("Rebuilding derived data files")
    logger.info("Data directory: %s", data_dir)
    logger.info("=" * 60)

    # Collect all data
    all_works = collect_all_works(data_dir)
    all_roads = collect_all_roads(data_dir)
    all_contractors = collect_all_contractors(data_dir)
    city_count, zone_count, ward_count = count_structure(data_dir)

    # Generate red flags
    logger.info("Generating red flags...")
    red_flags_data = generate_red_flags(all_works)
    red_flags_dir = os.path.join(data_dir, "red-flags")
    _write_json(os.path.join(red_flags_dir, "flags.json"), red_flags_data)

    # Generate summary stats
    logger.info("Generating summary stats...")
    stats_dir = os.path.join(data_dir, "stats")
    summary = compute_summary(
        all_works, all_roads, all_contractors,
        red_flags_data.get("flags", []),
        city_count=city_count,
        zone_count=zone_count,
        ward_count=ward_count,
    )
    _write_json(os.path.join(stats_dir, "summary.json"), summary)

    # Generate contractor rankings
    logger.info("Generating contractor rankings...")
    contractors_dir = os.path.join(data_dir, "contractors")
    contractor_rankings = compute_contractor_rankings(contractors_dir)
    _write_json(os.path.join(stats_dir, "contractor-rankings.json"), contractor_rankings)

    # Generate ward rankings
    logger.info("Generating ward rankings...")
    ward_rankings = compute_ward_rankings(data_dir)
    _write_json(os.path.join(stats_dir, "ward-rankings.json"), ward_rankings)

    # Generate search index
    logger.info("Generating search index...")
    search_dir = os.path.join(data_dir, "search")
    search_index = generate_search_index(data_dir)
    _write_json(os.path.join(search_dir, "index.json"), search_index)

    logger.info("=" * 60)
    logger.info("Rebuild complete")
    logger.info("  Red flags: %d", red_flags_data["totalFlags"])
    logger.info("  Works: %d, Roads: %d, Contractors: %d",
                summary["totalWorks"], summary["totalRoads"], summary["totalContractors"])
    logger.info("  Search entries: %d", search_index["totalEntries"])
    logger.info("=" * 60)


def main():
    """CLI entry point for rebuild."""
    parser = argparse.ArgumentParser(
        description="Rebuild all derived data files from existing ward-level data",
    )
    parser.add_argument(
        "--data-dir",
        help="Path to the root data directory (default: auto-detected)",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Enable debug logging",
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    data_dir = args.data_dir
    if data_dir:
        data_dir = os.path.abspath(data_dir)
    else:
        data_dir = os.path.abspath(DATA_DIR)

    if not os.path.isdir(data_dir):
        logger.error("Data directory not found: %s", data_dir)
        sys.exit(1)

    rebuild_all(data_dir)


if __name__ == "__main__":
    main()
