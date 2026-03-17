"""
Generate roads.json from parsed works data.
Groups works by road, computes latest DLP status, total spending, and works count.
"""

import logging
from datetime import date

from pipeline.utils.config import compute_dlp_status, TODAY

logger = logging.getLogger(__name__)


def _build_road_from_works(road_id, road_works, existing_road=None):
    """
    Build a single road record by aggregating data from all works on that road.

    Args:
        road_id: The road ID string.
        road_works: List of work dicts for this road.
        existing_road: Existing road record dict (if updating).

    Returns:
        A dict matching the roads.json schema.
    """
    # Start from existing road data or create new
    road = {}
    if existing_road:
        road = dict(existing_road)

    road["roadId"] = road_id

    # Try to get road name from works descriptions or existing data
    if not road.get("roadName"):
        for work in road_works:
            desc = work.get("description", "")
            if desc:
                # Try to extract road name from "Asphalting of <road name>"
                # Common pattern: "<workType> of <road name>"
                parts = desc.split(" of ", 1)
                if len(parts) == 2:
                    road["roadName"] = parts[1].strip()
                    break
                else:
                    road["roadName"] = desc
                    break

    # Defaults for fields that may not exist yet
    road.setdefault("aliases", [])
    road.setdefault("roadClass", "ward")
    road.setdefault("surfaceType", _infer_surface_type(road_works))
    road.setdefault("lengthKm", None)
    road.setdefault("widthM", None)
    road.setdefault("osmWayId", None)

    # Compute aggregate stats
    total_spending = 0
    total_works = len(road_works)

    # Find the latest DLP info (most recent dlpEndDate)
    latest_dlp_end = None
    latest_contractor = None

    for work in road_works:
        cost = work.get("sanctionedCost")
        if cost is not None:
            total_spending += float(cost)

        dlp_end = work.get("dlpEndDate")
        if dlp_end:
            if latest_dlp_end is None or dlp_end > latest_dlp_end:
                latest_dlp_end = dlp_end
                latest_contractor = work.get("contractorName")

    road["currentDlpStatus"] = compute_dlp_status(latest_dlp_end)
    road["currentDlpEnd"] = latest_dlp_end
    road["currentContractor"] = latest_contractor
    road["totalWorksCount"] = total_works
    road["totalSpending"] = total_spending
    road["lastUpdated"] = TODAY.isoformat()

    return road


def _infer_surface_type(works):
    """Infer road surface type from its works."""
    for work in works:
        work_type = work.get("workType", "")
        if "concrete" in work_type.lower() or "white" in work_type.lower():
            return "concrete"
    return "asphalt"


def generate_roads(works, existing_roads=None):
    """
    Generate roads.json data from a list of works.

    Args:
        works: List of work record dicts (from works generator).
        existing_roads: List of existing road dicts (optional, for updating).

    Returns:
        A list of road record dicts matching the roads.json schema.
    """
    # Index existing roads by roadId
    existing_by_id = {}
    if existing_roads:
        for road in existing_roads:
            rid = road.get("roadId")
            if rid:
                existing_by_id[rid] = road

    # Group works by roadId
    works_by_road = {}
    unmatched_works = []

    for work in works:
        road_id = work.get("roadId")
        if road_id:
            works_by_road.setdefault(road_id, []).append(work)
        else:
            unmatched_works.append(work)

    if unmatched_works:
        logger.warning(
            "%d works have no roadId and will not appear in roads.json",
            len(unmatched_works),
        )

    # Build road records
    roads = []

    # Process roads that have works
    for road_id, road_works in sorted(works_by_road.items()):
        existing = existing_by_id.pop(road_id, None)
        road = _build_road_from_works(road_id, road_works, existing_road=existing)
        roads.append(road)

    # Keep existing roads that had no new works (preserve them)
    for road_id, existing in sorted(existing_by_id.items()):
        existing["lastUpdated"] = TODAY.isoformat()
        roads.append(existing)

    logger.info("Generated %d road records", len(roads))
    return roads
