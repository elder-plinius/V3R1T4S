#!/bin/sh
# Verifies the five exact certificates in ../object with standard-library Python (3.9+). Do not run Python with -O.
set -e
cd "$(dirname "$0")"
out=$(python3 verify_completeness.py ../object)
echo "$out" | tail -3
echo "$out" | grep -q "FULL_GAME_COMPLETENESS: PASS" && echo PASS
