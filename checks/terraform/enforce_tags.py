"""
Custom Checkov check: Enforce mandatory tags on all taggable resources.

Rule ID: CKV_CUSTOM_001
Severity: HIGH
Category: B

All resources that support tags MUST have the mandatory tags:
  - Environment (sandbox | non-prd | prd)
  - Owner (responsible team email)
  - Project (project name)
  - CostCenter (cost center)
  - ManagedBy (terraform | manual)
"""

from checkov.terraform.checks.resource.base_resource_check import BaseResourceCheck
from checkov.common.models.enums import CheckResult, CheckCategories


class EnforceMandatoryTags(BaseResourceCheck):

    REQUIRED_TAGS = ["Environment", "Owner", "Project", "CostCenter", "ManagedBy"]

    def __init__(self):
        name = "Ensure all resources have mandatory tags"
        id = "CKV_CUSTOM_001"
        supported_resources = [
            "aws_instance",
            "aws_s3_bucket",
            "aws_rds_cluster",
            "aws_db_instance",
            "aws_vpc",
            "aws_subnet",
            "aws_security_group",
            "aws_ecs_cluster",
            "aws_ecs_service",
            "aws_lambda_function",
            "aws_sqs_queue",
            "aws_sns_topic",
            "aws_kms_key",
            "aws_dynamodb_table",
            "aws_elasticache_cluster",
            "aws_efs_file_system",
            "aws_lb",
            "aws_lb_target_group",
        ]
        categories = [CheckCategories.GENERAL_SECURITY]
        super().__init__(
            name=name,
            id=id,
            categories=categories,
            supported_resources=supported_resources,
        )

    def scan_resource_conf(self, conf) -> CheckResult:
        tags = conf.get("tags", [{}])
        if isinstance(tags, list):
            tags = tags[0] if tags else {}

        if not isinstance(tags, dict):
            return CheckResult.FAILED

        for required_tag in self.REQUIRED_TAGS:
            if required_tag not in tags:
                return CheckResult.FAILED

        return CheckResult.PASSED


check = EnforceMandatoryTags()
