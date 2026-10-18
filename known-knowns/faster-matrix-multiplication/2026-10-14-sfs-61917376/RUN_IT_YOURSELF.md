From this package directory run `sh verify-it-yourself/run_checks.sh`. Requires Python3.8+ and a POSIX shell, no packages or network. Expected final line: PASS. The frozen hash, exact integer tensor, every basis pair and operation counts are checked; corrupted object bytes are rejected.

From how-we-built-it run `python3 rebuild.py`. Expected final line: REBUILD PASS. This reconstructs the saved selected decisions and verifies the 486-addition circuit without external dependencies or network. Full discovery-history replay is unavailable and unclaimed.
