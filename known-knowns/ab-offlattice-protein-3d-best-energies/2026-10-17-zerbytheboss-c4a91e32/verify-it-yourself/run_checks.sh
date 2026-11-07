#!/bin/sh
set -eu
DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$DIR"
python3 verify-it-yourself/check_ab_protein.py object/ab_3d_records_F89_2EWH_1CRN_1PCH.json
