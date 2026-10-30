#!/bin/sh
set -eu
DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$DIR"
python3 verify-it-yourself/check_gupta_clusters.py object/gupta_zn_cd_5_records_and_780_audit.json
