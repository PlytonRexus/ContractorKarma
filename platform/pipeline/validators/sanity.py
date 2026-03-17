"""
Sanity validators for work records.
Check logical consistency of costs, dates, and amounts.
"""

import logging
from datetime import date

from pipeline.normalizers.dates import parse_date

logger = logging.getLogger(__name__)

# If actual paid exceeds this multiple of sanctioned cost, raise a warning
COST_OVERRUN_WARNING_FACTOR = 1.5


def validate_record(record):
    """
    Run all sanity checks on a single work record.

    Args:
        record: A dict representing a work record with keys like
                sanctionedCost, actualPaid, woDate, completionDate, etc.

    Returns:
        A dict with:
            valid (bool): True if no errors (warnings are ok).
            errors (list): List of error message strings.
            warnings (list): List of warning message strings.
    """
    errors = []
    warnings = []

    job_code = record.get("jobCode", "unknown")

    # 1. Cost must be positive
    sanctioned_cost = record.get("sanctionedCost") or record.get("woCost")
    if sanctioned_cost is not None:
        try:
            cost_val = float(sanctioned_cost)
            if cost_val <= 0:
                errors.append(f"[{job_code}] Sanctioned cost must be > 0, got {cost_val}")
        except (ValueError, TypeError):
            errors.append(f"[{job_code}] Invalid sanctioned cost: {sanctioned_cost}")
    else:
        warnings.append(f"[{job_code}] Missing sanctioned cost")

    # 2. Completion date after WO date
    wo_date_str = parse_date(record.get("woDate"))
    completion_date_str = parse_date(
        record.get("actualCompletionDate") or record.get("completionDate")
    )

    if wo_date_str and completion_date_str:
        wo_date = date.fromisoformat(wo_date_str)
        completion_date = date.fromisoformat(completion_date_str)
        if completion_date < wo_date:
            errors.append(
                f"[{job_code}] Completion date ({completion_date_str}) "
                f"is before WO date ({wo_date_str})"
            )

    # 3. DLP end after DLP start
    dlp_start_str = parse_date(record.get("dlpStartDate"))
    dlp_end_str = parse_date(record.get("dlpEndDate"))

    if dlp_start_str and dlp_end_str:
        dlp_start = date.fromisoformat(dlp_start_str)
        dlp_end = date.fromisoformat(dlp_end_str)
        if dlp_end <= dlp_start:
            errors.append(
                f"[{job_code}] DLP end date ({dlp_end_str}) "
                f"is not after DLP start date ({dlp_start_str})"
            )

    # 4. Actual paid should not exceed sanctioned cost by too much
    actual_paid = record.get("actualPaid") or record.get("amountPaid")
    if sanctioned_cost is not None and actual_paid is not None:
        try:
            cost_val = float(sanctioned_cost)
            paid_val = float(actual_paid)

            if cost_val > 0 and paid_val > cost_val * COST_OVERRUN_WARNING_FACTOR:
                warnings.append(
                    f"[{job_code}] Actual paid ({paid_val}) exceeds "
                    f"{COST_OVERRUN_WARNING_FACTOR}x sanctioned cost ({cost_val})"
                )
        except (ValueError, TypeError):
            pass

    # 5. Stipulated completion date after WO date (if present)
    stipulated_str = parse_date(record.get("stipulatedCompletionDate"))
    if wo_date_str and stipulated_str:
        wo_date = date.fromisoformat(wo_date_str)
        stipulated = date.fromisoformat(stipulated_str)
        if stipulated < wo_date:
            warnings.append(
                f"[{job_code}] Stipulated completion ({stipulated_str}) "
                f"is before WO date ({wo_date_str})"
            )

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
    }


def validate_all(records):
    """
    Run sanity checks on all records.

    Args:
        records: List of work record dicts.

    Returns:
        A dict with:
            total (int): Total records checked.
            valid_count (int): Records with no errors.
            error_count (int): Records with at least one error.
            all_errors (list): All error messages.
            all_warnings (list): All warning messages.
    """
    all_errors = []
    all_warnings = []
    error_count = 0

    for record in records:
        result = validate_record(record)
        all_errors.extend(result["errors"])
        all_warnings.extend(result["warnings"])
        if not result["valid"]:
            error_count += 1

    for err in all_errors:
        logger.error("Sanity error: %s", err)
    for warn in all_warnings:
        logger.warning("Sanity warning: %s", warn)

    return {
        "total": len(records),
        "valid_count": len(records) - error_count,
        "error_count": error_count,
        "all_errors": all_errors,
        "all_warnings": all_warnings,
    }
