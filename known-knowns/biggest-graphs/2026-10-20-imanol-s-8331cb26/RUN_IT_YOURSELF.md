# Run it yourself

From this folder, run `sh verify-it-yourself/run_checks.sh`. Requires a POSIX shell, shasum and a C++17 compiler. No network or Python dependencies are needed for verification; the last line must be `PASS`.

For construction replay, create a Python environment and install `how-we-built-it/requirements.txt`, then run `python how-we-built-it/replay.py`. This rebuilds the joint-cut intermediate and two annealing chunks. It asserts the exact final object hash. A clean temporary-copy replay passed in the pinned local environment; the actual main and three independent object checks are recorded separately in the verdicts and receipts.
