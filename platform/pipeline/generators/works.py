"""
Generate works.json from parsed and normalized input data.
Computes DLP status, cost per km, and red flags for each work.
"""

import logging
from datetime import date

from pipeline.normalizers.dates import parse_date
from pipeline.normalizers.currency import parse_currency
from pipeline.utils.config import compute_dlp_status, get_dlp_duration, TODAY

logger = logging.getLogger(__name__)


def _infer_work_type(description):
    """Infer work type from the description text."""
    if not description:
        return "asphalting"

    desc_lower = description.lower()

    if "white" in desc_lower and "top" in desc_lower:
        return "whiteTopping"
    if "concrete" in desc_lower and "pav" in desc_lower:
        return "concretePaving"
    if "resurf" in desc_lower:
        return "resurfacing"
    if "pothole" in desc_lower:
        return "potholeRepair"
    if "drain" in desc_lower:
        return "drainRepair"
    if "footpath" in desc_lower:
        return "footpath"
    if "asphalt" in desc_lower:
        return "asphalting"
    if "tar" in desc_lower and "road" in desc_lower:
        return "asphalting"

    return "asphalting"


def _compute_cost_per_km(sanctioned_cost, length_km):
    """Compute cost per km, handling missing data."""
    if sanctioned_cost and length_km and float(length_km) > 0:
        return round(float(sanctioned_cost) / float(length_km))
    return None


def _detect_work_red_flags(work, median_cost_per_km=None):
    """Detect red flags for a single work record."""
    flags = []

    # delayed: completion > 6 months past stipulated
    stipulated = work.get("stipulatedCompletionDate")
    actual = work.get("actualCompletionDate")
    if stipulated and actual:
        try:
            stip_date = date.fromisoformat(stipulated)
            act_date = date.fromisoformat(actual)
            delay_days = (act_date - stip_date).days
            if delay_days > 180:
                flags.append("severeDelay")
            elif delay_days > 30:
                flags.append("delayed")
        except (ValueError, TypeError):
            pass

    # costOverrun: actual > 1.2x sanctioned
    sanctioned = work.get("sanctionedCost")
    paid = work.get("actualPaid")
    if sanctioned and paid:
        try:
            if float(paid) > float(sanctioned) * 1.2:
                flags.append("costOverrun")
        except (ValueError, TypeError):
            pass

    # costOutlier: cost per km > 2x median
    cost_per_km = work.get("costPerKm")
    if cost_per_km and median_cost_per_km and median_cost_per_km > 0:
        try:
            if float(cost_per_km) > 2 * median_cost_per_km:
                flags.append("costOutlier")
        except (ValueError, TypeError):
            pass

    return flags


def build_work_record(raw, zone_id, ward_number, rti_id=None, road_info=None):
    """
    Build a single work record from raw parsed data.

    Args:
        raw: Dict from the parser with raw field values.
        zone_id: The zone ID prefix (e.g. 'blr-sth').
        ward_number: The ward number (int).
        rti_id: The RTI application ID (optional).
        road_info: Dict with roadId, roadName, lengthKm if matched.

    Returns:
        A dict matching the works.json schema.
    """
    job_code = raw.get("jobCode", "")
    description = raw.get("nameOfWork") or raw.get("description", "")
    work_type = raw.get("workType") or _infer_work_type(description)

    # Parse costs
    sanctioned_cost = parse_currency(raw.get("woCost") or raw.get("sanctionedCost"))
    actual_paid = parse_currency(raw.get("amountPaid") or raw.get("actualPaid"))

    # Parse dates
    wo_date = parse_date(raw.get("woDate"))
    completion_date = parse_date(
        raw.get("completionDate") or raw.get("actualCompletionDate")
    )
    dlp_start = parse_date(raw.get("dlpStartDate"))
    dlp_end = parse_date(raw.get("dlpEndDate"))
    commencement = parse_date(raw.get("commencementDate"))
    stipulated = parse_date(raw.get("stipulatedCompletionDate"))

    # If DLP start is missing but completion date is available, use that
    if not dlp_start and completion_date:
        dlp_start = completion_date

    # If DLP end is missing but DLP start is available, compute from surface type
    dlp_duration = get_dlp_duration(work_type)
    if not dlp_end and dlp_start:
        try:
            start = date.fromisoformat(dlp_start)
            end_year = start.year + dlp_duration
            # Handle Feb 29 edge case
            try:
                end = date(end_year, start.month, start.day)
            except ValueError:
                end = date(end_year, start.month, start.day - 1)
            dlp_end = end.isoformat()
        except (ValueError, TypeError):
            pass

    # Compute DLP status
    dlp_status = compute_dlp_status(dlp_end)

    # Road info
    road_id = None
    length_km = None
    if road_info:
        road_id = road_info.get("roadId")
        length_km = road_info.get("lengthKm")

    # Cost per km
    cost_per_km = _compute_cost_per_km(sanctioned_cost, length_km)

    # Contractor info
    contractor_name = raw.get("contractor") or raw.get("contractorName", "")
    contractor_id = raw.get("contractorId")

    # Build the work record
    work = {
        "jobCode": job_code,
        "roadId": road_id,
        "description": description,
        "workType": work_type,
        "contractorId": contractor_id,
        "contractorName": contractor_name,
        "woNumber": raw.get("woNumber"),
        "woDate": wo_date,
        "sanctionedCost": sanctioned_cost,
        "actualPaid": actual_paid,
        "tenderNumber": raw.get("tenderNumber"),
        "bidCount": raw.get("bidCount"),
        "commencementDate": commencement,
        "stipulatedCompletionDate": stipulated,
        "actualCompletionDate": completion_date,
        "fundingSource": raw.get("fundingSource"),
        "dlpStartDate": dlp_start,
        "dlpEndDate": dlp_end,
        "dlpDurationYears": dlp_duration,
        "dlpStatus": dlp_status,
        "certifyingOfficials": [],
        "performanceGuarantee": None,
        "costPerKm": cost_per_km,
        "redFlags": [],
        "dataSource": {
            "rtiId": rti_id,
            "responseDate": None,
        },
    }

    # Add check measurement officer if present
    cm_officer = raw.get("checkMeasurementOfficer")
    if cm_officer:
        work["certifyingOfficials"].append({
            "name": str(cm_officer).strip(),
            "designation": "",
            "role": "checkMeasurement",
        })

    # Detect red flags (costOutlier is deferred until we have median)
    work["redFlags"] = _detect_work_red_flags(work)

    return work


def generate_works(raw_records, zone_id, ward_number, rti_id=None, road_lookup=None):
    """
    Generate a list of work records from raw parsed data.

    Args:
        raw_records: List of dicts from the parser.
        zone_id: The zone ID prefix (e.g. 'blr-sth').
        ward_number: The ward number (int).
        rti_id: RTI application ID.
        road_lookup: Dict mapping road names to road info dicts.

    Returns:
        A list of work record dicts matching the works.json schema.
    """
    works = []

    for raw in raw_records:
        road_info = None
        if road_lookup:
            # Try to match by road name from the description or explicit roadName field
            road_name = raw.get("roadName") or raw.get("nameOfWork", "")
            if road_name in road_lookup:
                road_info = road_lookup[road_name]

        work = build_work_record(
            raw, zone_id, ward_number,
            rti_id=rti_id,
            road_info=road_info,
        )
        works.append(work)

    # Second pass: compute median cost per km and add costOutlier flags
    cost_per_km_values = [
        w["costPerKm"] for w in works
        if w["costPerKm"] is not None and w["costPerKm"] > 0
    ]

    if cost_per_km_values:
        sorted_costs = sorted(cost_per_km_values)
        mid = len(sorted_costs) // 2
        if len(sorted_costs) % 2 == 0:
            median = (sorted_costs[mid - 1] + sorted_costs[mid]) / 2
        else:
            median = sorted_costs[mid]

        for work in works:
            extra_flags = _detect_work_red_flags(work, median_cost_per_km=median)
            for flag in extra_flags:
                if flag not in work["redFlags"]:
                    work["redFlags"].append(flag)

    logger.info("Generated %d work records", len(works))
    return works
