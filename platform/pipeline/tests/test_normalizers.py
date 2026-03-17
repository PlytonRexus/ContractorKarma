"""Tests for pipeline normalizers."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from normalizers.currency import parse_currency
from normalizers.dates import parse_date
from normalizers.jobCode import parse_job_code, validate_job_code


class TestCurrencyParser:
    def test_lakhs(self):
        assert parse_currency("18.5 Lakhs") == 1850000.0

    def test_crores(self):
        assert parse_currency("2.3 Cr") == 23000000.0

    def test_plain_number(self):
        assert parse_currency("1800000") == 1800000.0

    def test_comma_formatted(self):
        assert parse_currency("18,00,000") == 1800000.0

    def test_rs_prefix(self):
        result = parse_currency("Rs. 50,000")
        assert result == 50000.0

    def test_none_input(self):
        assert parse_currency(None) is None

    def test_empty_string(self):
        assert parse_currency("") is None


class TestDateParser:
    def test_dd_mm_yyyy(self):
        assert parse_date("15/03/2024") == "2024-03-15"

    def test_dd_dash_mm_dash_yyyy(self):
        assert parse_date("15-03-2024") == "2024-03-15"

    def test_iso_format(self):
        assert parse_date("2024-03-15") == "2024-03-15"

    def test_none_input(self):
        assert parse_date(None) is None


class TestJobCodeParser:
    def test_valid_job_code(self):
        result = parse_job_code("150-23-000042")
        assert result is not None
        assert result["ward"] == 150
        # year is returned as full year (2023)
        assert result["year"] == 2023

    def test_invalid_format(self):
        result = parse_job_code("ABC123")
        assert result is None

    def test_validation_matching_ward(self):
        result = validate_job_code("150-23-000042", 150)
        assert result["valid"] is True

    def test_validation_mismatched_ward(self):
        result = validate_job_code("149-23-000042", 150)
        assert result["valid"] is False
