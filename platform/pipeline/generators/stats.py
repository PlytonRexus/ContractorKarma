"""
Generate stats/summary.json with platform-wide aggregates.
Also generates contractor and ward rankings.
"""

import json
import logging
import os
from collections import defaultdict

from pipeline.utils.config import TODAY, compute_dlp_status

logger = logging.getLogger(__name__)


def compute_summary(all_works, all_roads, all_contractors, all_red_flags, city_count=1, zone_count=0, ward_count=0):
    """
    Compute platform-wide summary statistics.

    Args:
        all_works: List of all work dicts.
        all_roads: List of all road dicts.
        all_contractors: List of contractor summary dicts.
        all_red_flags: List of red flag dicts.
        city_count: Number of cities.
        zone_count: Number of zones with data.
        ward_count: Number of wards with data.

    Returns:
        A dict matching the stats/summary.json schema.
    """
    total_sanctioned = 0
    total_paid = 0
    dlp_counts = {"active": 0, "expiringSoon": 0, "expired": 0, "unknown": 0}
    works_delayed = 0

    for work in all_works:
        sanctioned = work.get("sanctionedCost")
        if sanctioned:
            total_sanctioned += float(sanctioned)

        paid = work.get("actualPaid")
        if paid:
            total_paid += float(paid)

        dlp_status = compute_dlp_status(work.get("dlpEndDate"))
        dlp_counts[dlp_status] = dlp_counts.get(dlp_status, 0) + 1

        # Check for delays
        stipulated = work.get("stipulatedCompletionDate")
        actual = work.get("actualCompletionDate")
        if stipulated and actual and actual > stipulated:
            works_delayed += 1

    # Count unique officials
    officials = set()
    for work in all_works:
        for official in work.get("certifyingOfficials", []):
            name = official.get("name")
            if name:
                officials.add(name)

    total_works = len(all_works)
    delay_pct = round((works_delayed / total_works * 100), 1) if total_works > 0 else 0
    avg_cost = round(total_sanctioned / total_works) if total_works > 0 else 0

    return {
        "generatedAt": TODAY.isoformat(),
        "totalCities": city_count,
        "totalZones": zone_count,
        "totalWards": ward_count,
        "totalRoads": len(all_roads),
        "totalWorks": total_works,
        "totalContractors": len(all_contractors),
        "totalOfficials": len(officials),
        "financials": {
            "totalSanctionedCost": total_sanctioned,
            "totalActualPaid": total_paid,
            "avgCostPerWork": avg_cost,
        },
        "dlp": {
            "active": dlp_counts["active"],
            "expiringSoon": dlp_counts["expiringSoon"],
            "expired": dlp_counts["expired"],
        },
        "performance": {
            "worksDelayed": works_delayed,
            "delayPercentage": delay_pct,
            "redFlagsTotal": len(all_red_flags),
        },
    }


def compute_contractor_rankings(contractors_dir):
    """
    Generate contractor rankings from contractor data files.

    Args:
        contractors_dir: Path to the contractors data directory.

    Returns:
        A dict matching the stats/contractor-rankings.json schema.
    """
    rankings = []

    if not os.path.isdir(contractors_dir):
        return {"generatedAt": TODAY.isoformat(), "rankings": rankings}

    for filename in sorted(os.listdir(contractors_dir)):
        if not filename.endswith(".json") or filename == "index.json":
            continue

        file_path = os.path.join(contractors_dir, filename)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            stats = data.get("stats", {})
            rankings.append({
                "contractorId": data.get("contractorId"),
                "legalName": data.get("legalName"),
                "performanceGrade": stats.get("performanceGrade"),
                "performanceScore": stats.get("performanceScore", 0),
                "totalWorks": stats.get("totalWorks", 0),
                "worksDelayed": stats.get("worksDelayed", 0),
                "dlpViolations": stats.get("dlpViolations", 0),
                "totalSanctionedValue": stats.get("totalSanctionedValue", 0),
            })
        except (json.JSONDecodeError, OSError) as exc:
            logger.warning("Failed to load contractor for ranking: %s", exc)

    # Sort by performance score descending
    rankings.sort(key=lambda x: x.get("performanceScore", 0), reverse=True)

    return {"generatedAt": TODAY.isoformat(), "rankings": rankings}


def compute_ward_rankings(data_dir):
    """
    Generate ward rankings from all ward data directories.

    Args:
        data_dir: Path to the root data directory.

    Returns:
        A dict matching the stats/ward-rankings.json schema.
    """
    rankings = []
    cities_dir = os.path.join(data_dir, "cities")

    if not os.path.isdir(cities_dir):
        return {"generatedAt": TODAY.isoformat(), "rankings": rankings}

    for city_slug in os.listdir(cities_dir):
        zones_dir = os.path.join(cities_dir, city_slug, "zones")
        if not os.path.isdir(zones_dir):
            continue

        for zone_slug in os.listdir(zones_dir):
            wards_dir = os.path.join(zones_dir, zone_slug, "wards")
            if not os.path.isdir(wards_dir):
                continue

            for ward_slug in os.listdir(wards_dir):
                ward_dir = os.path.join(wards_dir, ward_slug)
                if not os.path.isdir(ward_dir):
                    continue

                ward_ranking = _compute_single_ward_ranking(ward_slug, ward_dir)
                if ward_ranking:
                    rankings.append(ward_ranking)

    # Sort by transparency score descending
    rankings.sort(key=lambda x: x.get("transparencyScore", 0), reverse=True)

    return {"generatedAt": TODAY.isoformat(), "rankings": rankings}


def _compute_single_ward_ranking(ward_slug, ward_dir):
    """Compute ranking data for a single ward."""
    works_path = os.path.join(ward_dir, "works.json")
    roads_path = os.path.join(ward_dir, "roads.json")

    works = []
    roads = []

    if os.path.isfile(works_path):
        try:
            with open(works_path, "r", encoding="utf-8") as f:
                works = json.load(f)
        except (json.JSONDecodeError, OSError):
            pass

    if os.path.isfile(roads_path):
        try:
            with open(roads_path, "r", encoding="utf-8") as f:
                roads = json.load(f)
        except (json.JSONDecodeError, OSError):
            pass

    if not works:
        return None

    # Extract ward number and name from slug
    parts = ward_slug.split("-", 1)
    ward_number = int(parts[0]) if parts[0].isdigit() else 0
    ward_name = parts[1].replace("-", " ").title() if len(parts) > 1 else ward_slug

    total_spending = sum(
        float(w.get("sanctionedCost", 0) or 0) for w in works
    )

    works_delayed = sum(
        1 for w in works
        if (w.get("stipulatedCompletionDate") and
            w.get("actualCompletionDate") and
            w["actualCompletionDate"] > w["stipulatedCompletionDate"])
    )

    red_flag_count = sum(
        len(w.get("redFlags", [])) for w in works
    )

    # Transparency score: higher is better
    # Based on data completeness, on-time delivery, and fewer red flags
    total = len(works)
    on_time_rate = (total - works_delayed) / total if total > 0 else 0
    flag_penalty = min(red_flag_count / max(total, 1), 1.0)
    transparency_score = round(on_time_rate * 0.7 + (1 - flag_penalty) * 0.3, 2)

    return {
        "wardSlug": ward_slug,
        "wardName": ward_name,
        "wardNumber": ward_number,
        "totalRoads": len(roads),
        "totalWorks": total,
        "totalSpending": total_spending,
        "worksDelayed": works_delayed,
        "redFlagCount": red_flag_count,
        "transparencyScore": transparency_score,
    }
