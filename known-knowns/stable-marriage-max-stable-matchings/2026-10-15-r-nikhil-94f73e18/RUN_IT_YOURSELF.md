From this folder, with Python3 and C++17/C11 compilers:

    sh verify-it-yourself/run_checks.sh

Expected last line: PASS, normally a few seconds. This uses the fresh REPRODUCE reviewer's independent exact memoized checker, with saved hashes, byte-exact reconstruction, controls, and complete candidate/predecessor counts.

For the original full assignment enumeration, checking every leaf for blocking pairs:

    sh verify-it-yourself/run_full_checks.sh

Expected last line: PASS. The completed package run took846.206seconds on the loaded host; its output is retained in verify-it-yourself/FULL_ENUMERATION_RECEIPT.md.

Rebuild only:

    python3 verify-it-yourself/rebuild.py object/construction.word rebuilt.prefs
    cmp object/object.prefs rebuilt.prefs

Replay discovery and the earlier fresh random-start calibration:

    python3 how-we-built-it/search/replay.py

Expected last line: PASS. The fresh panel complete replay took873.926seconds. No network or nonstandard Python package is needed.
