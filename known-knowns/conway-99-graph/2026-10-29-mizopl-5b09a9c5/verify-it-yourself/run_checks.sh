#!/bin/sh
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
python3 -B "$DIR/verify.py"
