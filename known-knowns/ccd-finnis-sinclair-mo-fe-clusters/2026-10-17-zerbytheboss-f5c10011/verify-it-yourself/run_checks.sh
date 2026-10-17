#!/bin/sh
set -eu
DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$DIR"
python3 verify-it-yourself/check_fs_clusters.py object/fs_mo_fe_11_records_and_196_audit.json
