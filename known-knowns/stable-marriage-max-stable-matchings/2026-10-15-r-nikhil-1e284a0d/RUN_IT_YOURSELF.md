From this folder, with Python3 and C++17/C11 compilers:

    sh verify-it-yourself/run_checks.sh

Expected last line: PASS. The command rebuilds the preference file and completely counts all stable matchings, checking every leaf for a blocking pair. Allow roughly a minute depending on hardware.

Rebuild only:

    python3 verify-it-yourself/rebuild.py object/construction.word rebuilt.prefs
    cmp object/object.prefs rebuilt.prefs

Replay the discovery and fresh random-start calibration:

    python3 how-we-built-it/search/replay.py

Expected last line: PASS. Allow several minutes depending on hardware. No network or nonstandard Python package is needed.
