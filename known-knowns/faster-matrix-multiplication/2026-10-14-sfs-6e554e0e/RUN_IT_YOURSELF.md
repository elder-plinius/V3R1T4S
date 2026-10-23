From the package root run `sh verify-it-yourself/run_checks.sh`. Requires Python3.8+ and a POSIX shell, no packages or network. Expected last line: PASS. Corrupt object bytes fail the hash check; independent exact tensor and operation checks also run.

To rebuild from pinned inputs, change into how-we-built-it and run `python3 rebuild.py`. Expected last line: REBUILD PASS. This step downloads the pinned public source files, verifies their hashes and replays the discovery code. A saved cache can be passed with --source-cache. The frozen object verifier needs no network.
