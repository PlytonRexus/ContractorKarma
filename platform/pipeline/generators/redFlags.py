"""
Detect and generate red flags across works and contractors.
Red flag types:
  - repeatFailure: road resurfaced within 2 years
  - costOutlier: cost-per-km > 2x median
  - dlpSpending: public money spent on road under DLP
  - contractorDominance: >50% works in one ward
  - severeDelay: completion >6 months past deadline
  - costOverrun: actual > 1.2x sanctioned
"""

import json
import logging
import os
from collections import defaultdict
from datetime import date

from pipeline.utils.config import TODAY

logger = logging.getLogger(__name__)

# Gap threshold (in days) for repeat failure detection
REPEAT_FAILURE_MAX_GAP_DAYS = 730  # 2 years


def _detect_repeat_failures(all_works):
    """
    Detect roads that were resurfaced within 2 years of a previous completion.

    Args:
        all_works: List of all work dicts across all wards.

    Returns:
        List of red flag dicts.
    """
    flags = []

    # Group works by roadId
    by_road = defaultdict(list)
    for work in all_works:
        road_id = work.get("roadId")
        if road_id:
            by_road[road_id].append(work)

    flag_counter = 0
    for road_id, road_works in by_road.items():
        # Sort by completion date
        dated_works = []
        for w in road_works:
            comp = w.get("actualCompletionDate")
            if comp:
                try:
                    dated_works.append((date.fromisoformat(comp), w))
                except (ValueError, TypeError):
                    pass

        dated_works.sort(key=lambda x: x[0])

        for i in range(1, len(dated_works)):
            prev_date, prev_work = dated_works[i - 1]
            curr_date, curr_work = dated_works[i]

            # Check the WO date of the new work vs completion of previous
            curr_wo = curr_work.get("woDate")
            if curr_wo:
                try:
                    curr_wo_date = date.fromisoformat(curr_wo)
                    gap_days = (curr_wo_date - prev_date).days
                    if 0 < gap_days < REPEAT_FAILURE_MAX_GAP_DAYS:
                        gap_months = gap_days // 30
                        flag_counter += 1
                        flags.append({
                            "flagId": f"rf-auto-{flag_counter:03d}",
                            "type": "repeatFailure",
                            "severity": "high",
                            "description": (
                                f"Road resurfaced within {gap_months} months of previous work"
                            ),
                            "roadId": road_id,
                            "roadName": _extract_road_name(curr_work),
                            "contractorId": curr_work.get("contractorId"),
                            "contractorName": curr_work.get("contractorName"),
                            "details": {
                                "previousWork": prev_work.get("jobCode"),
                                "previousCompletion": prev_date.isoformat(),
                                "newWork": curr_work.get("jobCode"),
                                "newWoDate": curr_wo,
                                "gapMonths": gap_months,
                            },
                        })
                except (ValueError, TypeError):
                    pass

    return flags


def _detect_cost_outliers(all_works):
    """
    Detect works where cost-per-km exceeds 2x the median.

    Args:
        all_works: List of all work dicts.

    Returns:
        List of red flag dicts.
    """
    flags = []

    costs = [
        w["costPerKm"] for w in all_works
        if w.get("costPerKm") and w["costPerKm"] > 0
    ]

    if len(costs) < 3:
        return flags

    sorted_costs = sorted(costs)
    mid = len(sorted_costs) // 2
    if len(sorted_costs) % 2 == 0:
        median = (sorted_costs[mid - 1] + sorted_costs[mid]) / 2
    else:
        median = sorted_costs[mid]

    threshold = median * 2
    flag_counter = 0

    for work in all_works:
        cpk = work.get("costPerKm")
        if cpk and cpk > threshold:
            flag_counter += 1
            deviation_pct = round(((cpk - median) / median) * 100)
            flags.append({
                "flagId": f"rf-cost-{flag_counter:03d}",
                "type": "costOutlier",
                "severity": "high",
                "description": (
                    f"Sanctioned cost is {deviation_pct}%+ above median for similar works"
                ),
                "roadId": work.get("roadId"),
                "roadName": _extract_road_name(work),
                "contractorId": work.get("contractorId"),
                "contractorName": work.get("contractorName"),
                "details": {
                    "jobCode": work.get("jobCode"),
                    "sanctionedCost": work.get("sanctionedCost"),
                    "costPerKm": cpk,
                    "medianCostPerKm": median,
                    "deviationPct": deviation_pct,
                },
            })

    return flags


def _detect_dlp_spending(all_works):
    """
    Detect cases where public money is being spent on a road still under DLP
    (the previous contractor should fix it for free).

    Args:
        all_works: List of all work dicts.

    Returns:
        List of red flag dicts.
    """
    flags = []

    # Group by roadId
    by_road = defaultdict(list)
    for work in all_works:
        road_id = work.get("roadId")
        if road_id:
            by_road[road_id].append(work)

    flag_counter = 0
    for road_id, road_works in by_road.items():
        sorted_works = sorted(
            road_works,
            key=lambda w: w.get("woDate") or "9999",
        )

        for i in range(1, len(sorted_works)):
            prev = sorted_works[i - 1]
            curr = sorted_works[i]

            # Check if previous work's DLP is still active when new work started
            prev_dlp_end = prev.get("dlpEndDate")
            curr_wo_date = curr.get("woDate")

            if prev_dlp_end and curr_wo_date:
                try:
                    dlp_end = date.fromisoformat(prev_dlp_end)
                    wo_start = date.fromisoformat(curr_wo_date)

                    if wo_start < dlp_end:
                        flag_counter += 1
                        flags.append({
                            "flagId": f"rf-dlp-{flag_counter:03d}",
                            "type": "dlpSpending",
                            "severity": "high",
                            "description": (
                                "New work ordered while previous work is still under DLP guarantee"
                            ),
                            "roadId": road_id,
                            "roadName": _extract_road_name(curr),
                            "contractorId": curr.get("contractorId"),
                            "contractorName": curr.get("contractorName"),
                            "details": {
                                "previousWork": prev.get("jobCode"),
                                "previousDlpEnd": prev_dlp_end,
                                "previousContractor": prev.get("contractorName"),
                                "newWork": curr.get("jobCode"),
                                "newWoDate": curr_wo_date,
                            },
                        })
                except (ValueError, TypeError):
                    pass

    return flags


def _detect_contractor_dominance(all_works):
    """
    Detect contractors that have >50% of works in any single ward.

    Args:
        all_works: List of all work dicts (must have 'wardSlug' or 'jobCode').

    Returns:
        List of red flag dicts.
    """
    flags = []

    # Group works by ward (extract ward number from jobCode)
    ward_contractors = defaultdict(lambda: defaultdict(int))
    ward_totals = defaultdict(int)
    contractor_names = {}

    for work in all_works:
        job_code = work.get("jobCode", "")
        cid = work.get("contractorId")
        if not cid or not job_code:
            continue

        parts = job_code.split("-")
        if len(parts) >= 1:
            ward = parts[0]
            ward_contractors[ward][cid] += 1
            ward_totals[ward] += 1
            contractor_names[cid] = work.get("contractorName", "")

    flag_counter = 0
    for ward, contractors in ward_contractors.items():
        total = ward_totals[ward]
        if total < 4:
            # Not enough works to make a meaningful assessment
            continue

        for cid, count in contractors.items():
            pct = (count / total) * 100
            if pct > 50:
                flag_counter += 1
                flags.append({
                    "flagId": f"rf-dom-{flag_counter:03d}",
                    "type": "contractorDominance",
                    "severity": "medium",
                    "description": (
                        f"Contractor has {pct:.0f}% of works in ward {ward}"
                    ),
                    "roadId": None,
                    "roadName": None,
                    "contractorId": cid,
                    "contractorName": contractor_names.get(cid, ""),
                    "details": {
                        "ward": ward,
                        "contractorWorks": count,
                        "wardTotalWorks": total,
                        "dominancePct": round(pct, 1),
                    },
                })

    return flags


def _detect_severe_delays(all_works):
    """
    Detect works completed more than 6 months past the stipulated deadline.

    Args:
        all_works: List of all work dicts.

    Returns:
        List of red flag dicts.
    """
    flags = []
    flag_counter = 0

    for work in all_works:
        stipulated = work.get("stipulatedCompletionDate")
        actual = work.get("actualCompletionDate")

        if not stipulated or not actual:
            continue

        try:
            stip_date = date.fromisoformat(stipulated)
            act_date = date.fromisoformat(actual)
            delay_days = (act_date - stip_date).days

            if delay_days > 180:
                flag_counter += 1
                flags.append({
                    "flagId": f"rf-delay-{flag_counter:03d}",
                    "type": "severeDelay",
                    "severity": "medium",
                    "description": (
                        f"Work completed {delay_days} days past stipulated date"
                    ),
                    "roadId": work.get("roadId"),
                    "roadName": _extract_road_name(work),
                    "contractorId": work.get("contractorId"),
                    "contractorName": work.get("contractorName"),
                    "details": {
                        "jobCode": work.get("jobCode"),
                        "stipulatedCompletion": stipulated,
                        "actualCompletion": actual,
                        "delayDays": delay_days,
                    },
                })
        except (ValueError, TypeError):
            pass

    return flags


def _detect_cost_overruns(all_works):
    """
    Detect works where actual paid > 1.2x sanctioned cost.

    Args:
        all_works: List of all work dicts.

    Returns:
        List of red flag dicts.
    """
    flags = []
    flag_counter = 0

    for work in all_works:
        sanctioned = work.get("sanctionedCost")
        actual = work.get("actualPaid")

        if not sanctioned or not actual:
            continue

        try:
            s = float(sanctioned)
            a = float(actual)

            if s > 0 and a > s * 1.2:
                overrun_pct = round(((a - s) / s) * 100, 1)
                flag_counter += 1
                flags.append({
                    "flagId": f"rf-overrun-{flag_counter:03d}",
                    "type": "costOverrun",
                    "severity": "high",
                    "description": (
                        f"Actual paid is {overrun_pct}% above sanctioned cost"
                    ),
                    "roadId": work.get("roadId"),
                    "roadName": _extract_road_name(work),
                    "contractorId": work.get("contractorId"),
                    "contractorName": work.get("contractorName"),
                    "details": {
                        "jobCode": work.get("jobCode"),
                        "sanctionedCost": s,
                        "actualPaid": a,
                        "overrunPct": overrun_pct,
                    },
                })
        except (ValueError, TypeError):
            pass

    return flags


def _extract_road_name(work):
    """Extract road name from a work's description."""
    desc = work.get("description", "")
    parts = desc.split(" of ", 1)
    if len(parts) == 2:
        return parts[1].strip()
    return desc


def generate_red_flags(all_works):
    """
    Run all red flag detectors on a collection of works.

    Args:
        all_works: List of all work record dicts across all wards.

    Returns:
        A dict matching the red-flags/flags.json schema.
    """
    all_flags = []

    all_flags.extend(_detect_repeat_failures(all_works))
    all_flags.extend(_detect_cost_outliers(all_works))
    all_flags.extend(_detect_dlp_spending(all_works))
    all_flags.extend(_detect_contractor_dominance(all_works))
    all_flags.extend(_detect_severe_delays(all_works))
    all_flags.extend(_detect_cost_overruns(all_works))

    # Re-number all flags sequentially
    for i, flag in enumerate(all_flags, start=1):
        flag["flagId"] = f"rf-{i:03d}"

    result = {
        "generatedAt": TODAY.isoformat(),
        "totalFlags": len(all_flags),
        "flags": all_flags,
    }

    logger.info("Generated %d red flags", len(all_flags))
    return result
