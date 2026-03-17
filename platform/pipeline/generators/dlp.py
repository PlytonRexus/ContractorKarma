"""
Generate dlp.json from works data.
Computes summary counts of DLP statuses (active, expiringSoon, expired, unknown).
"""

import logging

from pipeline.utils.config import compute_dlp_status, TODAY

logger = logging.getLogger(__name__)


def generate_dlp(works, ward_slug):
    """
    Generate dlp.json data from a list of works.

    Args:
        works: List of work record dicts.
        ward_slug: The ward slug string (e.g. '176-btm-layout').

    Returns:
        A dict matching the dlp.json schema with summary counts and items list.
    """
    items = []
    counts = {
        "active": 0,
        "expiringSoon": 0,
        "expired": 0,
        "unknown": 0,
    }

    for work in works:
        dlp_end = work.get("dlpEndDate")
        dlp_status = compute_dlp_status(dlp_end)

        # Update the work's dlpStatus to be consistent
        counts[dlp_status] = counts.get(dlp_status, 0) + 1

        item = {
            "jobCode": work.get("jobCode"),
            "roadId": work.get("roadId"),
            "roadName": _extract_road_name(work),
            "contractorId": work.get("contractorId"),
            "contractorName": work.get("contractorName"),
            "dlpStartDate": work.get("dlpStartDate"),
            "dlpEndDate": work.get("dlpEndDate"),
            "dlpDurationYears": work.get("dlpDurationYears"),
            "dlpStatus": dlp_status,
        }
        items.append(item)

    result = {
        "wardSlug": ward_slug,
        "generatedAt": TODAY.isoformat(),
        "summary": {
            "totalWorks": len(works),
            "active": counts["active"],
            "expiringSoon": counts["expiringSoon"],
            "expired": counts["expired"],
            "unknown": counts["unknown"],
        },
        "items": items,
    }

    logger.info(
        "Generated DLP data for %s: %d total, %d active, %d expiringSoon, %d expired",
        ward_slug, len(works), counts["active"], counts["expiringSoon"], counts["expired"],
    )
    return result


def _extract_road_name(work):
    """Extract road name from a work record's description."""
    desc = work.get("description", "")
    if not desc:
        return ""

    # Try to extract from "Asphalting of <road name>" pattern
    parts = desc.split(" of ", 1)
    if len(parts) == 2:
        return parts[1].strip()

    return desc
