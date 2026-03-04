"""Unit tests for CKV_CUSTOM_002: Deny public S3 buckets."""

import unittest
from checks.terraform.deny_public_s3 import check
from checkov.common.models.enums import CheckResult


class TestDenyPublicS3(unittest.TestCase):
    """Tests for the DenyPublicS3 custom check."""

    def test_pass_all_blocks_enabled(self):
        """PASS: All public access block settings enabled."""
        config = {
            "block_public_acls": [True],
            "block_public_policy": [True],
            "ignore_public_acls": [True],
            "restrict_public_buckets": [True],
        }
        result = check.scan_resource_conf(conf=config)
        self.assertEqual(result, CheckResult.PASSED)

    def test_fail_missing_block_public_policy(self):
        """FAIL: block_public_policy not set."""
        config = {
            "block_public_acls": [True],
            "ignore_public_acls": [True],
            "restrict_public_buckets": [True],
        }
        result = check.scan_resource_conf(conf=config)
        self.assertEqual(result, CheckResult.FAILED)

    def test_fail_block_set_to_false(self):
        """FAIL: One block explicitly set to false."""
        config = {
            "block_public_acls": [True],
            "block_public_policy": [False],
            "ignore_public_acls": [True],
            "restrict_public_buckets": [True],
        }
        result = check.scan_resource_conf(conf=config)
        self.assertEqual(result, CheckResult.FAILED)


if __name__ == "__main__":
    unittest.main()
