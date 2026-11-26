#!/bin/sh
set -e
DIR="$(cd "$(dirname "$0")/.." && pwd)"
python3 "$DIR/verify-it-yourself/check_game.py"
