"""
Generate contractor data files.
Produces contractors/index.json (list of all contractors) and
per-contractor files (contractors/ctr-XXX.json) with aggregated stats.
"""

import json
import logging
import os

from pipeline.utils.config import TODAY

logger = logging.getLogger(__name__)


def aggregate_contractor_stats(works, ward_slug):
    """
    Aggregate statistics for each contractor from a list of works.

    Args:
        works: List of work record dicts.
        ward_slug: Ward slug for tracking which wards a contractor is active in.

    Returns:
        A dict mapping contractorId to stats dict.
    """
    stats = {}

    for work in works:
        cid = work.get("contractorId")
        if not cid:
            continue

        if cid not in stats:
            stats[cid] = {
                "contractorId": cid,
                "legalName": work.get("contractorName", ""),
                "totalWorks": 0,
                "totalSanctionedValue": 0,
                "worksCompletedOnTime": 0,
                "worksDelayed": 0,
                "dlpViolations": 0,
                "costPerKmValues": [],
                "wardsActive": set(),
                "workJobCodes": [],
            }

        entry = stats[cid]
        entry["totalWorks"] += 1
        entry["wardsActive"].add(ward_slug)

        # Track job codes
        job_code = work.get("jobCode")
        if job_code:
            entry["workJobCodes"].append(job_code)

        # Costs
        sanctioned = work.get("sanctionedCost")
        if sanctioned:
            entry["totalSanctionedValue"] += float(sanctioned)

        cost_per_km = work.get("costPerKm")
        if cost_per_km and cost_per_km > 0:
            entry["costPerKmValues"].append(cost_per_km)

        # Delay analysis
        stipulated = work.get("stipulatedCompletionDate")
        actual = work.get("actualCompletionDate")
        if stipulated and actual:
            if actual > stipulated:
                entry["worksDelayed"] += 1
            else:
                entry["worksCompletedOnTime"] += 1

        # DLP violations (red flags related to DLP)
        red_flags = work.get("redFlags", [])
        if "dlpSpending" in red_flags:
            entry["dlpViolations"] += 1

    return stats


def compute_performance_score(stats_entry):
    """
    Compute a performance score (0.0 to 1.0) for a contractor.

    Factors:
      - On-time completion rate (40% weight)
      - Low DLP violations (30% weight)
      - Reasonable cost per km (30% weight, relative to average)
    """
    total = stats_entry["totalWorks"]
    if total == 0:
        return 0.5

    # On-time rate
    on_time = stats_entry["worksCompletedOnTime"]
    delayed = stats_entry["worksDelayed"]
    completed = on_time + delayed
    on_time_rate = on_time / completed if completed > 0 else 0.5

    # DLP violation rate
    dlp_violations = stats_entry["dlpViolations"]
    dlp_rate = max(0, 1.0 - (dlp_violations / total))

    # Cost reasonableness (lower is better, normalized)
    # We just give a baseline here since we do not have zone averages in isolation
    cost_score = 0.7  # Default neutral score

    score = (on_time_rate * 0.4) + (dlp_rate * 0.3) + (cost_score * 0.3)
    return round(min(1.0, max(0.0, score)), 2)


def compute_performance_grade(score):
    """Map a performance score to a letter grade."""
    if score >= 0.85:
        return "A"
    elif score >= 0.70:
        return "B"
    elif score >= 0.50:
        return "C"
    else:
        return "D"


def build_contractor_file(stats_entry):
    """
    Build the full contractor JSON file content.

    Args:
        stats_entry: Aggregated stats dict for one contractor.

    Returns:
        A dict matching the contractor file schema.
    """
    avg_cost = 0
    cost_values = stats_entry.get("costPerKmValues", [])
    if cost_values:
        avg_cost = round(sum(cost_values) / len(cost_values))

    score = compute_performance_score(stats_entry)
    grade = compute_performance_grade(score)

    return {
        "contractorId": stats_entry["contractorId"],
        "legalName": stats_entry["legalName"],
        "registrationNumber": None,
        "registrationClass": None,
        "address": None,
        "stats": {
            "totalWorks": stats_entry["totalWorks"],
            "totalSanctionedValue": stats_entry["totalSanctionedValue"],
            "worksCompletedOnTime": stats_entry["worksCompletedOnTime"],
            "worksDelayed": stats_entry["worksDelayed"],
            "dlpViolations": stats_entry["dlpViolations"],
            "avgCostPerKm": avg_cost,
            "wardsActive": sorted(stats_entry["wardsActive"]),
            "performanceGrade": grade,
            "performanceScore": score,
        },
        "blacklisted": False,
        "works": stats_entry.get("workJobCodes", []),
    }


def update_contractor_files(works, ward_slug, contractors_dir):
    """
    Update contractor files on disk with new works data.
    Merges with existing contractor data if files already exist.

    Args:
        works: List of work record dicts.
        ward_slug: The ward slug.
        contractors_dir: Path to the contractors data directory.

    Returns:
        List of contractor IDs that were updated.
    """
    os.makedirs(contractors_dir, exist_ok=True)

    new_stats = aggregate_contractor_stats(works, ward_slug)
    updated_ids = []

    for cid, new_entry in new_stats.items():
        file_path = os.path.join(contractors_dir, f"{cid}.json")
        existing = None

        # Load existing data if present
        if os.path.isfile(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    existing = json.load(f)
            except (json.JSONDecodeError, OSError) as exc:
                logger.warning("Failed to load existing contractor %s: %s", cid, exc)

        if existing:
            # Merge: add new stats to existing
            existing_stats = existing.get("stats", {})
            new_entry["totalWorks"] += existing_stats.get("totalWorks", 0)
            new_entry["totalSanctionedValue"] += existing_stats.get("totalSanctionedValue", 0)
            new_entry["worksCompletedOnTime"] += existing_stats.get("worksCompletedOnTime", 0)
            new_entry["worksDelayed"] += existing_stats.get("worksDelayed", 0)
            new_entry["dlpViolations"] += existing_stats.get("dlpViolations", 0)

            existing_wards = set(existing_stats.get("wardsActive", []))
            new_entry["wardsActive"] = new_entry["wardsActive"] | existing_wards

            existing_works = existing.get("works", [])
            new_entry["workJobCodes"] = list(
                set(existing_works + new_entry.get("workJobCodes", []))
            )

            # Preserve registration info
            new_entry["legalName"] = existing.get("legalName", new_entry["legalName"])

            contractor_data = build_contractor_file(new_entry)
            contractor_data["registrationNumber"] = existing.get("registrationNumber")
            contractor_data["registrationClass"] = existing.get("registrationClass")
            contractor_data["address"] = existing.get("address")
            contractor_data["blacklisted"] = existing.get("blacklisted", False)
        else:
            contractor_data = build_contractor_file(new_entry)

        # Write to file
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(contractor_data, f, indent=2, ensure_ascii=False)

        updated_ids.append(cid)
        logger.info("Updated contractor file: %s", file_path)

    return updated_ids


def generate_contractor_index(contractors_dir):
    """
    Generate the contractors index from all contractor files.

    Args:
        contractors_dir: Path to the contractors data directory.

    Returns:
        A list of summary dicts for all contractors.
    """
    index = []

    if not os.path.isdir(contractors_dir):
        return index

    for filename in sorted(os.listdir(contractors_dir)):
        if not filename.endswith(".json") or filename == "index.json":
            continue

        file_path = os.path.join(contractors_dir, filename)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            index.append({
                "contractorId": data.get("contractorId"),
                "legalName": data.get("legalName"),
                "performanceGrade": data.get("stats", {}).get("performanceGrade"),
                "performanceScore": data.get("stats", {}).get("performanceScore"),
                "totalWorks": data.get("stats", {}).get("totalWorks"),
                "totalSanctionedValue": data.get("stats", {}).get("totalSanctionedValue"),
            })
        except (json.JSONDecodeError, OSError) as exc:
            logger.warning("Failed to load contractor for index: %s: %s", filename, exc)

    logger.info("Generated contractor index with %d entries", len(index))
    return index
