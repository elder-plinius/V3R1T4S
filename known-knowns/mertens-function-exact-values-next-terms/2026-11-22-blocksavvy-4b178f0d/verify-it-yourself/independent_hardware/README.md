# Independent-hardware full-tier receipt

Single-threaded `FULL=1` run of this package's `verify-it-yourself/check.py` on hardware other than the machine that produced the certificate and the three original full sieves.

- Hardware: Apple M1 iMac (8-core, 8 GB)
- OS: macOS 27.2 (Build 26B123), Darwin 27.2.0 arm64
- Compiler: Apple clang 21.0.0 (clang-2100.4.1.1); `mu_check.c` compiled with `cc -O2` (no OpenMP)
- Run: single-threaded `FULL=1` recompute of all 3301 blocks from k = 1
- Started: 2026-11-22 18:08:48 UTC (12:08:48 PM CST)
- Finished: 2026-11-22 19:00:28 UTC (1:00:28 PM CST); wall time about 52 minutes
- Last line: `PASS`
- Object: a(18) = 330055906058, M = -262144; recomputed blocks match the certificate (3301 blocks; mismatches: [])

See `full_env.txt` and `full_run.log` in this folder. The log is also copied into `../RECEIPTS.md`.
