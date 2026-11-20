# Run it yourself

1. `sh verify-it-yourself/run_checks.sh` (expect PASS). It downloads https://github.com/MarioVanhoucke/MMLIB-Multi-Mode-Resource-Constrained-Project-Library/releases/download/v2.1/MMLIB_v2_1.zip (sha256 4f6f5318fcbc01943ec74dfbf8b16afc25b65759963666f631d6cdd2f242fecd) to a temporary folder.
2. To re-run the search (results vary by seed and machine; the claim is the saved schedules): install how-we-built-it/requirements.txt (Python 3.12), place the release's MMLIB+ instances as the code expects (how-we-built-it/phaseA/code/phaseA_bench.py and how-we-built-it/search/code/data.py name their paths), and run the search programs in how-we-built-it/search/code (hybrid_v2.py, hybrid_v3.py, hybrid_v31_warm.py, hybrid_v32_warm.py, overnight_v32.py, pilot_4w_and_ref1.py); their logs are in how-we-built-it/search/logs.
3. The warm-start evidence: how-we-built-it/lead-agent-checks/warm_start_edits*.py (OR-Tools) re-time the posted modes of the 8 warm-started instances.
