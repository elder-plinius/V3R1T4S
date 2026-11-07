#!/bin/sh
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
PINNED_COMMIT="0dcac107d15adc34dc646242d222f21ae7d32699"

if [ -x /opt/homebrew/bin/python3 ]; then
    PY=/opt/homebrew/bin/python3
else
    PY=python3
fi

CLEANUP_DIR=""
cleanup() {
    if [ -n "$CLEANUP_DIR" ] && [ -d "$CLEANUP_DIR" ]; then
        rm -rf "$CLEANUP_DIR"
    fi
}
trap cleanup EXIT INT TERM

if [ -z "${POLYTOF_DIR:-}" ] || [ ! -d "${POLYTOF_DIR}" ]; then
    CLEANUP_DIR="$(mktemp -d)"
    POLYTOF_DIR="$CLEANUP_DIR/polytof"
    git clone --quiet https://github.com/ZIB-IOL/polytof.git "$POLYTOF_DIR"
    git -C "$POLYTOF_DIR" checkout --quiet "$PINNED_COMMIT"
fi

ACTUAL_COMMIT="$(git -C "$POLYTOF_DIR" rev-parse HEAD)"
if [ "$ACTUAL_COMMIT" != "$PINNED_COMMIT" ]; then
    echo "Commit mismatch: expected $PINNED_COMMIT, got $ACTUAL_COMMIT"
    echo "FAIL"
    exit 1
fi

"$PY" -B "$DIR/verify.py" --polytof-dir "$POLYTOF_DIR"
