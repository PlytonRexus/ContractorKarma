"""Tests for pipeline validators."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from validators.sanity import validate_record


class TestSanityValidator:
    def test_valid_record(self):
        record = {
            "sanctionedCost": 1800000,
            "actualPaid": 1750000,
            "woDate": "2023-06-15",
            "actualCompletionDate": "2024-03-15",
            "dlpStartDate": "2024-03-15",
            "dlpEndDate": "2027-03-15",
        }
        result = validate_record(record)
        assert result["valid"] is True
        assert len(result["errors"]) == 0

    def test_negative_cost(self):
        record = {
            "sanctionedCost": -100,
            "actualPaid": None,
            "woDate": None,
            "actualCompletionDate": None,
            "dlpStartDate": None,
            "dlpEndDate": None,
        }
        result = validate_record(record)
        assert result["valid"] is False
        assert len(result["errors"]) > 0

    def test_completion_before_wo(self):
        record = {
            "sanctionedCost": 1800000,
            "actualPaid": None,
            "woDate": "2024-06-15",
            "actualCompletionDate": "2023-03-15",
            "dlpStartDate": None,
            "dlpEndDate": None,
        }
        result = validate_record(record)
        assert result["valid"] is False
        assert len(result["errors"]) > 0
