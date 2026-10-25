#!/bin/sh
# SPDX-License-Identifier: AGPL-3.0-or-later
# Run from the package root: sh verify-it-yourself/run_checks.sh
cd "$(dirname "$0")/.." || exit 1
exec python3 verify-it-yourself/check.py
