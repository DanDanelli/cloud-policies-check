"""Unit tests for CKV_CUSTOM_001: Enforce mandatory tags."""

import unittest
from checks.terraform.enforce_tags import check
from checkov.common.models.enums import CheckResult


class TestEnforceMandatoryTags(unittest.TestCase):
    """Tests for the EnforceMandatoryTags custom check."""

    def test_pass_all_tags_present(self):
        """PASS: All required tags are present."""
        config = {
            "tags": [{
                "Environment": "prd",
                "Owner": "team-alpha@company.com",
                "Project": "project-alpha",
                "CostCenter": "CC-1234",
                "ManagedBy": "terraform",
            }]
        }
        result = check.scan_resource_conf(conf=config)
        self.assertEqual(result, CheckResult.PASSED)

    def test_fail_missing_owner_tag(self):
        """FAIL: Missing Owner tag."""
        config = {
            "tags": [{
                "Environment": "prd",
                "Project": "project-alpha",
                "CostCenter": "CC-1234",
                "ManagedBy": "terraform",
            }]
        }
        result = check.scan_resource_conf(conf=config)
        self.assertEqual(result, CheckResult.FAILED)

    def test_fail_no_tags(self):
        """FAIL: No tags at all."""
        config = {}
        result = check.scan_resource_conf(conf=config)
        self.assertEqual(result, CheckResult.FAILED)

    def test_fail_empty_tags(self):
        """FAIL: Empty tags dict."""
        config = {"tags": [{}]}
        result = check.scan_resource_conf(conf=config)
        self.assertEqual(result, CheckResult.FAILED)


if __name__ == "__main__":
    unittest.main()
