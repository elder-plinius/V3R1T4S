#!/bin/sh
set -eu
DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
python3 "$DIR/check_dzugutov_clusters.py" "$DIR/../object/dzugutov_zetterling_20_records_and_502_audit.json"
