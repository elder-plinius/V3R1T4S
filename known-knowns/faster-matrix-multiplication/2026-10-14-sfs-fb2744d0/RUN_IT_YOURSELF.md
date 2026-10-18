From the package root run `sh verify-it-yourself/run_checks.sh`. Requires Python 3.8+ and a POSIX shell, no packages or network. Expected last line: PASS. Corrupt object bytes fail the hash check; exact tensor and operation checks run independently.

To rebuild from pinned inputs, change into how-we-built-it and run `python3 rebuild.py`. Expected last line: REBUILD PASS. That step uses public network downloads, checks every source hash, and replays the original discovery code; the verifier itself needs only object/scheme.json.
