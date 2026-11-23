#!/bin/sh
set -eu
DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
sh "$DIR/verify-it-yourself/run_checks.sh"
