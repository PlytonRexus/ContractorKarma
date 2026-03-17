"""
Parse Excel (.xlsx) and CSV files into a list of dicts.
Handles column name normalization and alternate column name mappings.
"""

import logging
import os

import pandas as pd

logger = logging.getLogger(__name__)

# Mapping from normalized (lowercased, stripped) column names to our camelCase keys.
# Multiple alternate names can map to the same key.
COLUMN_MAP = {
    # jobCode
    "job code": "jobCode",
    "jobcode": "jobCode",
    "job_code": "jobCode",
    "job no": "jobCode",
    "job no.": "jobCode",
    "sl. no. (job code)": "jobCode",
    # nameOfWork / description
    "name of work": "nameOfWork",
    "nameofwork": "nameOfWork",
    "name_of_work": "nameOfWork",
    "work name": "nameOfWork",
    "description": "nameOfWork",
    "work description": "nameOfWork",
    "particulars": "nameOfWork",
    "particulars of work": "nameOfWork",
    # contractor
    "contractor": "contractor",
    "contractor name": "contractor",
    "name of contractor": "contractor",
    "agency": "contractor",
    "name of agency": "contractor",
    "contractor/agency": "contractor",
    # woNumber
    "wo number": "woNumber",
    "wonumber": "woNumber",
    "wo no": "woNumber",
    "wo no.": "woNumber",
    "work order number": "woNumber",
    "work order no": "woNumber",
    "work order no.": "woNumber",
    # woDate
    "wo date": "woDate",
    "wodate": "woDate",
    "work order date": "woDate",
    "date of wo": "woDate",
    "date of work order": "woDate",
    # woCost / sanctionedCost
    "wo cost": "woCost",
    "wocost": "woCost",
    "sanctioned cost": "woCost",
    "sanctioned amount": "woCost",
    "estimated cost": "woCost",
    "work order cost": "woCost",
    "tender cost": "woCost",
    "amount (rs.)": "woCost",
    "amount": "woCost",
    "cost": "woCost",
    # completionDate
    "completion date": "completionDate",
    "completiondate": "completionDate",
    "date of completion": "completionDate",
    "actual completion date": "completionDate",
    "actual completion": "completionDate",
    "completed on": "completionDate",
    # dlpStartDate
    "dlp start date": "dlpStartDate",
    "dlpstartdate": "dlpStartDate",
    "dlp start": "dlpStartDate",
    "dlp from": "dlpStartDate",
    "guarantee start": "dlpStartDate",
    # dlpEndDate
    "dlp end date": "dlpEndDate",
    "dlpenddate": "dlpEndDate",
    "dlp end": "dlpEndDate",
    "dlp to": "dlpEndDate",
    "dlp upto": "dlpEndDate",
    "guarantee end": "dlpEndDate",
    # amountPaid
    "amount paid": "amountPaid",
    "amountpaid": "amountPaid",
    "actual paid": "amountPaid",
    "paid amount": "amountPaid",
    "amount paid (rs.)": "amountPaid",
    "total paid": "amountPaid",
    # checkMeasurementOfficer
    "check measurement officer": "checkMeasurementOfficer",
    "checkmeasurementofficer": "checkMeasurementOfficer",
    "cm officer": "checkMeasurementOfficer",
    "check measurement": "checkMeasurementOfficer",
    "recording officer": "checkMeasurementOfficer",
    "ae/aee": "checkMeasurementOfficer",
    # Extra useful columns
    "tender number": "tenderNumber",
    "tender no": "tenderNumber",
    "tender no.": "tenderNumber",
    "bid count": "bidCount",
    "no of bids": "bidCount",
    "no. of bids": "bidCount",
    "number of bids": "bidCount",
    "road name": "roadName",
    "name of road": "roadName",
    "road": "roadName",
    "surface type": "surfaceType",
    "type of work": "workType",
    "work type": "workType",
    "length (km)": "lengthKm",
    "length km": "lengthKm",
    "length": "lengthKm",
    "width (m)": "widthM",
    "width m": "widthM",
    "width": "widthM",
    "funding source": "fundingSource",
    "source of fund": "fundingSource",
    "stipulated completion date": "stipulatedCompletionDate",
    "stipulated completion": "stipulatedCompletionDate",
    "expected completion": "stipulatedCompletionDate",
    "commencement date": "commencementDate",
    "date of commencement": "commencementDate",
    "start date": "commencementDate",
}

# The expected output columns
EXPECTED_COLUMNS = [
    "jobCode", "nameOfWork", "contractor", "woNumber", "woDate",
    "woCost", "completionDate", "dlpStartDate", "dlpEndDate",
    "amountPaid", "checkMeasurementOfficer",
]


def _normalize_column_name(col):
    """Strip whitespace, lowercase, collapse multiple spaces."""
    normalized = " ".join(str(col).strip().lower().split())
    return normalized


def _map_columns(df):
    """
    Rename DataFrame columns from raw (possibly messy) names to our
    canonical camelCase keys using the COLUMN_MAP lookup.
    Columns that don't match any mapping are kept as-is (lowercased).
    """
    rename_map = {}
    for raw_col in df.columns:
        normalized = _normalize_column_name(raw_col)
        if normalized in COLUMN_MAP:
            rename_map[raw_col] = COLUMN_MAP[normalized]
        else:
            # Keep unrecognized columns with their normalized name
            rename_map[raw_col] = normalized

    df = df.rename(columns=rename_map)

    # Deduplicate: if multiple raw columns mapped to the same key, keep first non-null
    seen = {}
    drop_cols = []
    for col in df.columns:
        if col in seen:
            # Merge: fill NaN in original from duplicate
            df[seen[col]] = df[seen[col]].fillna(df[col])
            drop_cols.append(col)
        else:
            seen[col] = col

    if drop_cols:
        # pandas may have duplicate column names; drop by position
        logger.warning("Duplicate mapped columns found and merged: %s", drop_cols)

    return df


def parse_file(file_path):
    """
    Parse an Excel (.xlsx) or CSV file into a list of dicts.

    Args:
        file_path: Path to the input file.

    Returns:
        A list of dicts, one per row. Keys are camelCase field names.
        Missing columns will have None values.

    Raises:
        FileNotFoundError: If file does not exist.
        ValueError: If file format is not supported.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Input file not found: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()

    if ext in (".xlsx", ".xls"):
        logger.info("Parsing Excel file: %s", file_path)
        df = pd.read_excel(file_path, engine="openpyxl")
    elif ext == ".csv":
        logger.info("Parsing CSV file: %s", file_path)
        df = pd.read_csv(file_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}. Expected .xlsx, .xls, or .csv")

    # Drop completely empty rows
    df = df.dropna(how="all").reset_index(drop=True)

    if df.empty:
        logger.warning("Input file is empty after removing blank rows: %s", file_path)
        return []

    logger.info("Read %d rows and %d columns from %s", len(df), len(df.columns), file_path)

    # Map column names
    df = _map_columns(df)

    # Ensure all expected columns exist (fill with None if missing)
    for col in EXPECTED_COLUMNS:
        if col not in df.columns:
            logger.warning("Expected column '%s' not found in input; will be None", col)
            df[col] = None

    # Convert to list of dicts, replacing NaN with None
    records = df.where(df.notna(), None).to_dict(orient="records")

    # Convert any remaining numpy/pandas types to native Python types
    clean_records = []
    for record in records:
        clean = {}
        for k, v in record.items():
            if v is not None and hasattr(v, "item"):
                # numpy scalar -> Python native
                v = v.item()
            clean[k] = v
        clean_records.append(clean)

    logger.info("Parsed %d records from %s", len(clean_records), file_path)
    return clean_records
