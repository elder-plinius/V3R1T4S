#!/bin/sh
set -eu
exec env PYTHONDONTWRITEBYTECODE=1 python3 -B verify-it-yourself/verify_carrier.py
