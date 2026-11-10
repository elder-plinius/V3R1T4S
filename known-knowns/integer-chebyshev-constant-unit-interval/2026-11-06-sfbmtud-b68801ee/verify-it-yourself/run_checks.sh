#!/bin/sh
script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd) || {
    printf '%s\n' 'Cannot locate verification runner.' 'FAIL'
    exit 1
}
if ! command -v python3 >/dev/null 2>&1; then
    printf '%s\n' 'Python 3 is required.' 'FAIL'
    exit 1
fi
PYTHONOPTIMIZE=0 PYTHONDONTWRITEBYTECODE=1 python3 -S "$script_dir/run_checks.py"
