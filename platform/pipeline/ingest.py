"""
CLI entry point for the Contractor Karma data ingestion pipeline.
Takes an input file (Excel or CSV) and processes it through:
  1. Parse -> 2. Normalize -> 3. Validate -> 4. Generate -> 5. Write

Usage:
  python -m pipeline.ingest --input data.xlsx --city bengaluru --zone south --ward 176-btm-layout --rti-id KA-RTI-2026-003
"""

import argparse
import json
import logging
import os
import sys

from pipeline.parsers.excel import parse_file
from pipeline.normalizers.jobCode import validate_job_code, normalize_job_code
from pipeline.normalizers.contractor import (
    load_known_contractors, match_contractor, normalize_contractor_name,
)
from pipeline.normalizers.roadName import load_known_roads, match_road
from pipeline.normalizers.currency import parse_currency
from pipeline.normalizers.dates import parse_date
from pipeline.validators.crossRef import cross_validate_records
from pipeline.validators.sanity import validate_all
from pipeline.validators.dedup import deduplicate_records
from pipeline.generators.works import generate_works
from pipeline.generators.roads import generate_roads
from pipeline.generators.dlp import generate_dlp
from pipeline.generators.contractors import update_contractor_files
from pipeline.generators.redFlags import generate_red_flags
from pipeline.generators.stats import (
    compute_summary, compute_contractor_rankings, compute_ward_rankings,
)
from pipeline.generators.search import generate_search_index
from pipeline.utils.config import (
    DATA_DIR, get_zone_id, get_ward_data_dir, get_contractors_dir,
    get_stats_dir, get_search_dir, get_red_flags_dir,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def _extract_ward_number(ward_slug):
    """Extract numeric ward number from a ward slug like '176-btm-layout'."""
    parts = ward_slug.split("-")
    if parts and parts[0].isdigit():
        return int(parts[0])
    return None


def _write_json(file_path, data):
    """Write data to a JSON file, creating directories as needed."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    logger.info("Wrote: %s", file_path)


def _load_json(file_path):
    """Load a JSON file, returning an empty list/dict on failure."""
    if not os.path.isfile(file_path):
        return None
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning("Failed to load %s: %s", file_path, exc)
        return None


def normalize_records(records, data_dir, zone_id, ward_data_dir):
    """
    Normalize all fields in parsed records:
    - Validate and normalize job codes
    - Match contractor names
    - Match road names
    - Parse currency values
    - Parse dates
    """
    known_contractors = load_known_contractors(data_dir)
    known_roads = load_known_roads(ward_data_dir)

    normalized = []
    warnings = []

    for record in records:
        norm = dict(record)

        # Normalize job code
        raw_job = norm.get("jobCode")
        if raw_job:
            clean_job = normalize_job_code(raw_job)
            if clean_job:
                norm["jobCode"] = clean_job
            else:
                warnings.append(f"Invalid job code: {raw_job}")

        # Match contractor
        raw_contractor = norm.get("contractor") or norm.get("contractorName")
        if raw_contractor:
            match_result = match_contractor(raw_contractor, known_contractors)
            norm["contractorName"] = match_result["canonicalName"]
            norm["contractorId"] = match_result["contractorId"]
            if not match_result["matched"]:
                norm["contractorName"] = normalize_contractor_name(raw_contractor)
                warnings.append(
                    f"Contractor not matched: '{raw_contractor}' "
                    f"(normalized to '{norm['contractorName']}')"
                )

        # Match road name (from nameOfWork description)
        raw_name = norm.get("nameOfWork") or norm.get("description", "")
        if raw_name and known_roads:
            road_result = match_road(raw_name, known_roads)
            if road_result["matched"]:
                norm["roadId"] = road_result["roadId"]
                norm["roadName"] = road_result["roadName"]

        # Parse currency fields
        for field in ["woCost", "sanctionedCost", "amountPaid", "actualPaid"]:
            if norm.get(field) is not None:
                parsed = parse_currency(norm[field])
                norm[field] = parsed

        # Parse date fields
        for field in ["woDate", "completionDate", "actualCompletionDate",
                      "dlpStartDate", "dlpEndDate", "commencementDate",
                      "stipulatedCompletionDate"]:
            if norm.get(field) is not None:
                parsed = parse_date(norm[field])
                norm[field] = parsed

        normalized.append(norm)

    if warnings:
        logger.warning("Normalization produced %d warnings", len(warnings))
        for w in warnings:
            logger.warning("  %s", w)

    return normalized


def run_pipeline(input_file, city, zone, ward, rti_id=None):
    """
    Run the full ingestion pipeline.

    Args:
        input_file: Path to the input Excel or CSV file.
        city: City slug (e.g. 'bengaluru').
        zone: Zone slug (e.g. 'south').
        ward: Ward slug (e.g. '176-btm-layout').
        rti_id: RTI application ID (optional).

    Returns:
        A dict with summary of what was processed.
    """
    data_dir = os.path.abspath(DATA_DIR)
    ward_data_dir = get_ward_data_dir(city, zone, ward)
    zone_id = get_zone_id(city, zone)
    ward_number = _extract_ward_number(ward)

    if ward_number is None:
        raise ValueError(f"Could not extract ward number from slug: {ward}")

    if zone_id is None:
        logger.warning(
            "Unknown zone '%s' for city '%s'; using fallback zone_id",
            zone, city,
        )
        zone_id = f"{city[:3]}-{zone[:3]}"

    logger.info("=" * 60)
    logger.info("Contractor Karma Data Ingestion Pipeline")
    logger.info("=" * 60)
    logger.info("Input: %s", input_file)
    logger.info("City: %s, Zone: %s, Ward: %s", city, zone, ward)
    logger.info("Zone ID: %s, Ward Number: %d", zone_id, ward_number)
    logger.info("RTI ID: %s", rti_id or "(none)")
    logger.info("Data dir: %s", data_dir)
    logger.info("-" * 60)

    # Step 1: Parse
    logger.info("Step 1: Parsing input file...")
    raw_records = parse_file(input_file)
    logger.info("Parsed %d records", len(raw_records))

    if not raw_records:
        logger.error("No records found in input file. Aborting.")
        return {"status": "error", "message": "No records found"}

    # Step 2: Normalize
    logger.info("Step 2: Normalizing fields...")
    normalized_records = normalize_records(raw_records, data_dir, zone_id, ward_data_dir)
    logger.info("Normalized %d records", len(normalized_records))

    # Step 3: Validate
    logger.info("Step 3: Validating records...")

    # 3a: Sanity checks
    sanity_result = validate_all(normalized_records)
    logger.info(
        "Sanity: %d valid, %d errors, %d warnings",
        sanity_result["valid_count"],
        sanity_result["error_count"],
        len(sanity_result["all_warnings"]),
    )

    # 3b: Cross-reference checks
    cross_result = cross_validate_records(normalized_records, ward_number, ward_data_dir)
    logger.info(
        "Cross-ref: %d valid, %d errors",
        cross_result["valid_count"], cross_result["error_count"],
    )

    # 3c: Deduplication
    dedup_result = deduplicate_records(normalized_records, ward_data_dir)
    clean_records = dedup_result["clean_records"]
    logger.info(
        "Dedup: %d clean, %d existing duplicates, %d internal duplicates",
        len(clean_records),
        len(dedup_result["existing_duplicates"]),
        len(dedup_result["internal_duplicates"]),
    )

    if not clean_records:
        logger.warning("No new records after deduplication. Nothing to write.")
        return {
            "status": "no_new_records",
            "parsed": len(raw_records),
            "duplicates": len(dedup_result["existing_duplicates"]),
        }

    # Step 4: Generate
    logger.info("Step 4: Generating output files...")

    # 4a: Generate works
    works = generate_works(
        clean_records, zone_id, ward_number,
        rti_id=rti_id,
    )

    # Merge with existing works
    existing_works_path = os.path.join(ward_data_dir, "works.json")
    existing_works = _load_json(existing_works_path)
    if existing_works and isinstance(existing_works, list):
        all_ward_works = existing_works + works
    else:
        all_ward_works = works

    # 4b: Generate roads (merge with existing)
    existing_roads_path = os.path.join(ward_data_dir, "roads.json")
    existing_roads = _load_json(existing_roads_path)
    if isinstance(existing_roads, list):
        roads = generate_roads(all_ward_works, existing_roads=existing_roads)
    else:
        roads = generate_roads(all_ward_works)

    # 4c: Generate DLP
    dlp = generate_dlp(all_ward_works, ward)

    # Step 5: Write output files
    logger.info("Step 5: Writing output files...")

    _write_json(os.path.join(ward_data_dir, "works.json"), all_ward_works)
    _write_json(os.path.join(ward_data_dir, "roads.json"), roads)
    _write_json(os.path.join(ward_data_dir, "dlp.json"), dlp)

    # Update contractor files
    contractors_dir = get_contractors_dir()
    updated_contractors = update_contractor_files(works, ward, contractors_dir)
    logger.info("Updated %d contractor files", len(updated_contractors))

    # Rebuild aggregates (stats, rankings, search index, red flags)
    logger.info("Rebuilding aggregates...")
    _rebuild_aggregates(data_dir)

    summary = {
        "status": "success",
        "parsed": len(raw_records),
        "normalized": len(normalized_records),
        "new_records": len(clean_records),
        "duplicates_skipped": len(dedup_result["existing_duplicates"]),
        "sanity_errors": sanity_result["error_count"],
        "sanity_warnings": len(sanity_result["all_warnings"]),
        "works_written": len(all_ward_works),
        "roads_written": len(roads),
        "contractors_updated": len(updated_contractors),
    }

    logger.info("=" * 60)
    logger.info("Pipeline completed successfully")
    for key, val in summary.items():
        logger.info("  %s: %s", key, val)
    logger.info("=" * 60)

    return summary


def _rebuild_aggregates(data_dir):
    """Rebuild platform-wide aggregate files after ingestion."""
    from pipeline.rebuild import rebuild_all
    rebuild_all(data_dir)


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Contractor Karma Data Ingestion Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m pipeline.ingest --input data.xlsx --city bengaluru --zone south --ward 176-btm-layout
  python -m pipeline.ingest --input works.csv --city bengaluru --zone mahadevapura --ward 150-bellandur --rti-id KA-RTI-2026-005
        """,
    )

    parser.add_argument(
        "--input", required=True,
        help="Path to input file (Excel .xlsx or CSV .csv)",
    )
    parser.add_argument(
        "--city", required=True,
        help="City slug (e.g. 'bengaluru')",
    )
    parser.add_argument(
        "--zone", required=True,
        help="Zone slug (e.g. 'south', 'mahadevapura')",
    )
    parser.add_argument(
        "--ward", required=True,
        help="Ward slug (e.g. '176-btm-layout')",
    )
    parser.add_argument(
        "--rti-id",
        help="RTI application ID (e.g. 'KA-RTI-2026-003')",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Parse and validate only, do not write output files",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Enable debug logging",
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if args.dry_run:
        logger.info("DRY RUN mode: will parse and validate but not write")
        # Parse and validate only
        raw_records = parse_file(args.input)
        logger.info("Parsed %d records", len(raw_records))

        data_dir = os.path.abspath(DATA_DIR)
        ward_data_dir = get_ward_data_dir(args.city, args.zone, args.ward)
        zone_id = get_zone_id(args.city, args.zone) or "unknown"

        normalized = normalize_records(raw_records, data_dir, zone_id, ward_data_dir)
        sanity = validate_all(normalized)

        logger.info("Sanity check: %d valid, %d errors", sanity["valid_count"], sanity["error_count"])
        for err in sanity["all_errors"]:
            logger.error("  %s", err)
        for warn in sanity["all_warnings"]:
            logger.warning("  %s", warn)

        sys.exit(0 if sanity["error_count"] == 0 else 1)

    try:
        result = run_pipeline(
            input_file=args.input,
            city=args.city,
            zone=args.zone,
            ward=args.ward,
            rti_id=args.rti_id,
        )

        if result.get("status") == "success":
            sys.exit(0)
        elif result.get("status") == "no_new_records":
            logger.warning("No new records to process")
            sys.exit(0)
        else:
            sys.exit(1)

    except FileNotFoundError as exc:
        logger.error("File not found: %s", exc)
        sys.exit(1)
    except ValueError as exc:
        logger.error("Invalid input: %s", exc)
        sys.exit(1)
    except Exception as exc:
        logger.exception("Pipeline failed with unexpected error: %s", exc)
        sys.exit(2)


if __name__ == "__main__":
    main()
