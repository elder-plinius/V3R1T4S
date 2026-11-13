#!/bin/sh
set -eu
receipt="$(mktemp)"
trap 'rm -f "$receipt"' EXIT HUP INT TERM
python3 verify-it-yourself/check_exact.py object/CANDIDATE_M8734.txt --n 25 --d 6 --w 11 --count 8734 --sha256 f9f280613ee2a5c500220a9f022d35d83264a14f96d940c9a517a15cebdf6fde --output "$receipt"
printf '%s\n' PASS
