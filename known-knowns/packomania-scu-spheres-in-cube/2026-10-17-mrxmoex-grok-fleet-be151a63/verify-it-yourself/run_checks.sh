#!/bin/sh
cd "$(dirname "$0")/.." && exec python3 verify-it-yourself/repro_scu_errata.py "$@"
