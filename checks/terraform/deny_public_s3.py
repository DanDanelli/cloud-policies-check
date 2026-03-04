"""
Custom Checkov check: Deny S3 buckets without public access block.

Rule ID: CKV_CUSTOM_002
Severity: CRITICAL
Categoria: A (nunca skippable)

Todo S3 bucket DEVE ter aws_s3_bucket_public_access_block configurado
com todos os 4 bloqueios habilitados.
"""

from checkov.terraform.checks.resource.base_resource_check import BaseResourceCheck
from checkov.common.models.enums import CheckResult, CheckCategories


class DenyPublicS3(BaseResourceCheck):

    def __init__(self):
        name = "Ensure S3 bucket has public access block with all settings enabled"
        id = "CKV_CUSTOM_002"
        supported_resources = ["aws_s3_bucket_public_access_block"]
        categories = [CheckCategories.GENERAL_SECURITY]
        super().__init__(
            name=name,
            id=id,
            categories=categories,
            supported_resources=supported_resources,
        )

    def scan_resource_conf(self, conf) -> CheckResult:
        required_settings = [
            "block_public_acls",
            "block_public_policy",
            "ignore_public_acls",
            "restrict_public_buckets",
        ]

        for setting in required_settings:
            value = conf.get(setting, [False])
            if isinstance(value, list):
                value = value[0] if value else False
            if not value or value == "false":
                return CheckResult.FAILED

        return CheckResult.PASSED


check = DenyPublicS3()
