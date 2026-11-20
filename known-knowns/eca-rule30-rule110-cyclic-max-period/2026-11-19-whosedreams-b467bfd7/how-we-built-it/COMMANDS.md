# Commands (as the search was run, and as this packaging run checked it)

The two C programs, the build/run/self-test scripts, and the 2026-11-03 small-n groundwork were sent out as a source package whose sha256 was:

```
49d1e492f7d6852d13c47a6d5c8284535f1fc9d538a7c00b9c54729f5d63e04f
```

Sources in this folder are byte-identical to that package's impl1/maxcycle.c, impl2/maxcycle.c, build.sh, run.sh, selftest.sh and scripts/selftest_run.sh. Credit in that original package README said anonymous in places; this claim package credits whosedreams.

## Build
From this folder, with a C11 compiler:

```
./build.sh
```

That compiles impl1/maxcycle and impl2/maxcycle at -O3.

## Self-test (already done; log packaged)
The original self-test compared against OEIS b-files fetched at groundwork time (those third-party files are not packaged). After placing current b-files at data/b334497.txt and data/b204371.txt:

```
./selftest.sh
```

Expected last line: `SELFTEST: PASS`. The shipped log is selftest/selftest.log: 120 OK lines, no BUG or MISMATCH lines. A334497(25..30) from both programs:

| n | both programs |
|--:|--------------:|
| 25 | 588425 |
| 26 | 312156 |
| 27 | 240300 |
| 28 | 249165 |
| 29 | 1466066 |
| 30 | 374265 |

## Exhaustive n=37 run (already done; results packaged)
On a Ryzen 9900X machine with about 53 GB under WSL2:

```
RULE=110 N=37 IMPL=1 WORKDIR=work/r110_n37 ./run.sh
RULE=110 N=37 IMPL=2 WORKDIR=work/r110_n37 ./run.sh
```

Result lines (also in results/):

```
rule=110 n=37 max_period=4403 witness=0x1c7dbbb23e time_sec=1699.3565 impl=1
rule=110 n=37 max_period=4403 witness=0x1c7dbbb23e time_sec=11946.5399 impl=2
```

impl1 used a 16 GiB bitset (about 28.3 minutes). impl2 used a 32 GiB colour array (about 3.32 hours). Each job is single-threaded.

## Held-out width (this packaging run)
Both programs were recompiled from the same sources and run at Rule 110, n=31, under nice -n 19. Peak RSS was 263740 kB (impl1) and 525956 kB (impl2), under the 8 GiB cap and under half of the free memory on that machine. Outputs are in heldout/:

```
rule=110 n=31 max_period=2759 witness=0x3f647ff8 time_sec=30.6107 impl=1
rule=110 n=31 max_period=2759 witness=0x3f647ff8 time_sec=337.9002 impl=2
```

Both match the listed OEIS term A204371(31)=2759. Wall times: impl1 2026-11-18 20:27:30–20:28:01 ET (America/New_York, UTC-5); impl2 2026-11-18 20:28:17–20:33:55 ET.

## Witness period (this packaging run)
From the package root:

```
sh verify-it-yourself/run_checks.sh
```

Expected last line: PASS. Output is in verify-it-yourself/RECEIPTS.md, captured 2026-11-18 20:35:40 ET (America/New_York, UTC-5).
