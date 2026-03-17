"""
Generate search/index.json with searchable entries for roads, contractors, and works.
"""

import json
import logging
import os

from pipeline.utils.config import TODAY

logger = logging.getLogger(__name__)


def generate_search_index(data_dir):
    """
    Generate a unified search index from all data files.

    Args:
        data_dir: Path to the root data directory.

    Returns:
        A dict matching the search/index.json schema.
    """
    entries = []

    # Collect road entries from all wards
    entries.extend(_collect_road_entries(data_dir))

    # Collect work entries from all wards
    entries.extend(_collect_work_entries(data_dir))

    # Collect contractor entries
    entries.extend(_collect_contractor_entries(data_dir))

    result = {
        "generatedAt": TODAY.isoformat(),
        "totalEntries": len(entries),
        "entries": entries,
    }

    logger.info("Generated search index with %d entries", len(entries))
    return result


def _collect_road_entries(data_dir):
    """Collect searchable road entries from all ward roads.json files."""
    entries = []
    cities_dir = os.path.join(data_dir, "cities")

    if not os.path.isdir(cities_dir):
        return entries

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
                if not os.path.isfile(roads_path):
                    continue

                try:
                    with open(roads_path, "r", encoding="utf-8") as f:
                        roads = json.load(f)

                    for road in roads:
                        entries.append({
                            "type": "road",
                            "id": road.get("roadId"),
                            "label": road.get("roadName"),
                            "aliases": road.get("aliases", []),
                            "ward": ward_slug,
                        })
                except (json.JSONDecodeError, OSError) as exc:
                    logger.warning("Failed to read roads from %s: %s", roads_path, exc)

    return entries


def _collect_work_entries(data_dir):
    """Collect searchable work entries from all ward works.json files."""
    entries = []
    cities_dir = os.path.join(data_dir, "cities")

    if not os.path.isdir(cities_dir):
        return entries

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
                if not os.path.isfile(works_path):
                    continue

                try:
                    with open(works_path, "r", encoding="utf-8") as f:
                        works = json.load(f)

                    for work in works:
                        entries.append({
                            "type": "work",
                            "id": work.get("jobCode"),
                            "label": work.get("description"),
                            "roadId": work.get("roadId"),
                            "ward": ward_slug,
                        })
                except (json.JSONDecodeError, OSError) as exc:
                    logger.warning("Failed to read works from %s: %s", works_path, exc)

    return entries


def _collect_contractor_entries(data_dir):
    """Collect searchable contractor entries from contractor files."""
    entries = []
    contractors_dir = os.path.join(data_dir, "contractors")

    if not os.path.isdir(contractors_dir):
        return entries

    for filename in sorted(os.listdir(contractors_dir)):
        if not filename.endswith(".json") or filename == "index.json":
            continue

        file_path = os.path.join(contractors_dir, filename)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            entries.append({
                "type": "contractor",
                "id": data.get("contractorId"),
                "label": data.get("legalName"),
            })
        except (json.JSONDecodeError, OSError) as exc:
            logger.warning("Failed to read contractor from %s: %s", file_path, exc)

    return entries
