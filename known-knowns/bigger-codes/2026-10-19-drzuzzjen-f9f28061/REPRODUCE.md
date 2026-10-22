# Reproduce mathematical validity only

Python3.10+ standard library; no installation, NumPy or Numba needed.

POSIX: `sh verify-it-yourself/run_checks.sh`

Windows or POSIX directly:
`python verify-it-yourself/check_exact.py object/CANDIDATE_M8734.txt --n 25 --d 6 --w 11 --count 8734 --sha256 f9f280613ee2a5c500220a9f022d35d83264a14f96d940c9a517a15cebdf6fde --output receipt.json`

Direct command exits0 and emits JSON with pass:true, pairs_checked38137011 and min_distance6. The sh wrapper additionally prints PASS. Receipt output is a new user-generated file, not part of the immutable input manifest.

The portable copy preserves mathematical checks. It makes Unix resource reporting optional, normalises Linux ru_maxrss to bytes, and removes the OS-specific process-count limit. Windows RAM telemetry is unavailable and recorded null; Windows execution has not been tested. This does not assert cross-platform runtime evidence. No searches or worker processes are launched. The original independent checker and verdict remain unchanged outside this bundle; portability edits are separately diffed and calibrated by Publisher and are not a new independent panel review.
