#!/bin/bash
# cloud-policies-check/scripts/run-checkov.sh
# Wrapper script for adaptive rigor by environment.
#
# Usage:
#   CHECKOV_LEVEL=non-prd ./scripts/run-checkov.sh /path/to/code
#
# The pipeline sets CHECKOV_LEVEL before calling this script.
# Valid values: sandbox | non-prd | prd
#
# Rigor reference (D-06):
#   sandbox : Only CRITICAL hard-fail (Category A)
#   non-prd : CRITICAL + HIGH hard-fail
#   prd     : CRITICAL + HIGH + MEDIUM hard-fail

set -euo pipefail

CODE_DIR="${1:-.}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/../.checkov.yml"
CHECKS_DIR="$SCRIPT_DIR/../checks/terraform/"
LEVEL="${CHECKOV_LEVEL:-sandbox}"

# Base flags
FLAGS="--config-file $CONFIG_FILE --directory $CODE_DIR"
FLAGS="$FLAGS --external-checks-dir $CHECKS_DIR"
FLAGS="$FLAGS --output cli --output junitxml --output sarif"
FLAGS="$FLAGS --output-file-path ."

case "$LEVEL" in
  sandbox)
    # Only CRITICAL hard-fail (Category A via .checkov.yml)
    FLAGS="$FLAGS --soft-fail-on HIGH --soft-fail-on MEDIUM --soft-fail-on LOW"
    ;;
  non-prd)
    # CRITICAL + HIGH hard-fail
    FLAGS="$FLAGS --soft-fail-on MEDIUM --soft-fail-on LOW"
    ;;
  prd)
    # CRITICAL + HIGH + MEDIUM hard-fail
    FLAGS="$FLAGS --soft-fail-on LOW"
    ;;
  *)
    echo "ERROR: Invalid CHECKOV_LEVEL: $LEVEL"
    echo "Accepted values: sandbox | non-prd | prd"
    exit 2
    ;;
esac

echo "============================================"
echo "  Checkov Security Scan"
echo "  Level:  $LEVEL"
echo "  Code:   $CODE_DIR"
echo "  Config: $CONFIG_FILE"
echo "============================================"

# shellcheck disable=SC2086
checkov $FLAGS
