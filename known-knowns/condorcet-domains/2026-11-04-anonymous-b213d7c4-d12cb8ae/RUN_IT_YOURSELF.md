From this folder, with Python 3.10+ standard library:

    sh verify-it-yourself/run_checks.sh

Expected last line: PASS. This counts all orders twice and runs positive/negative and exhaustive small-case calibrations. No network access is needed. On the validation laptop the full portable check took about 2 seconds; hardware varies.

To reproduce the winning assignment from frozen inputs, with a C++17 compiler:

    python3 how-we-built-it/regenerate.py ../condorcet-replay-new

The output directory must be new and outside this package. Expected last line: PASS and regenerated SHA256 d12cb8aee658a8e3657c8607ba722531604366ba65a97f8fd357aea7d482131e. This faithfully replays the saved successful finite search with relative CPU/wall caps and no expired run deadline. It makes no new optimization or exclusion claim. Compilation and native replay took about 2 seconds in the validation environment.
