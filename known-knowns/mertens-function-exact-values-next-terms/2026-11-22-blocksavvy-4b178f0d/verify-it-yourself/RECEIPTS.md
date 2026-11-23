# Receipts (real output, copied from the terminal)

## Quick tier: `sh verify-it-yourself/run_checks.sh` (2026-11-22, 8-core Linux box; 12 random blocks differ per run)

```
ok   object names n = 18 and |M(k)| = 2^18 (n=18, M=-262144)
compiled mu_check.c with cc -O2 -fopenmp
ok   C checker compiled
ok   C mu(1..20000) equals trial-division mu
ok   C mu(k-199..k) equals trial-division mu near the claimed k
ok   pure-Python sieve reproduces a(0..9)
ok   certificate has every block 0..3399 exactly once
ok   certificate chain gives M(100000000) = 1928 (published 1928)
ok   certificate chain gives M(1000000000) = -222 (published -222)
ok   certificate chain gives M(10000000000) = -33722 (published -33722)
ok   certificate chain gives M(100000000000) = -87856 (published -87856)
ok   first certificate block reaching 2^18 is the block holding k (3300)
quick tier: recomputing blocks [0, 9, 25, 76, 99, 377, 750, 896, 999, 1085, 1253, 1529, 1641, 1692, 2332, 2412, 2466, 2851, 3015, 3141, 3299, 3300]
ok   recomputed blocks match the certificate (22 blocks; mismatches: [])
ok   scan reproduces published a(14) = 2589994747 (first k=2589994747 M=-16384)
ok   scan reproduces published a(15) = 7613644886 (first k=7613644886 M=32768)
ok   scan reproduces published a(16) = 37725066313 (first k=37725066313 M=-65536)
ok   scan reproduces published a(17) = 108500046711 (first k=108500046711 M=131072)
ok   scan of block 3300 gives the object's k = 330055906058, M = -262144 (first k=330055906058 M=-262144)
PASS
real	0m43.095s
user	0m45.301s
sys	0m0.404s
```

## Full tier: `FULL=1 OMP_NUM_THREADS=6 nice -n 19 python3 verify-it-yourself/check.py` (2026-11-22, finished 17:54:12 UTC, about 20 min wall on 6 threads)

```
ok   object names n = 18 and |M(k)| = 2^18 (n=18, M=-262144)
compiled mu_check.c with cc -O2 -fopenmp
ok   C checker compiled
ok   C mu(1..20000) equals trial-division mu
ok   C mu(k-199..k) equals trial-division mu near the claimed k
ok   pure-Python sieve reproduces a(0..9)
ok   certificate has every block 0..3399 exactly once
ok   certificate chain gives M(100000000) = 1928 (published 1928)
ok   certificate chain gives M(1000000000) = -222 (published -222)
ok   certificate chain gives M(10000000000) = -33722 (published -33722)
ok   certificate chain gives M(100000000000) = -87856 (published -87856)
ok   first certificate block reaching 2^18 is the block holding k (3300)
FULL tier: recomputing all 3301 blocks from k = 1 (about 2 CPU-hours single-threaded)
ok   recomputed blocks match the certificate (3301 blocks; mismatches: [])
ok   recomputed chain gives M(100000000) = 1928 (published 1928)
ok   recomputed chain gives M(1000000000) = -222 (published -222)
ok   recomputed chain gives M(10000000000) = -33722 (published -33722)
ok   recomputed chain gives M(100000000000) = -87856 (published -87856)
ok   recomputed: no block before 3300 reaches |M| = 2^18 (k = 1 .. 330000000000 covered)
ok   recomputed M(330000000000) equals the certificate's
ok   scan reproduces published a(14) = 2589994747 (first k=2589994747 M=-16384)
ok   scan reproduces published a(15) = 7613644886 (first k=7613644886 M=32768)
ok   scan reproduces published a(16) = 37725066313 (first k=37725066313 M=-65536)
ok   scan reproduces published a(17) = 108500046711 (first k=108500046711 M=131072)
ok   scan of block 3300 gives the object's k = 330055906058, M = -262144 (first k=330055906058 M=-262144)
PASS
```

Corrupted-object test (one digit of object/a18.txt changed, 330055906058 -> 330055901058): last line FAIL, exit 1.

## Independent hardware, full tier: `FULL=1` on Apple M1 iMac, macOS, single-threaded (2026-11-22, started 18:08:48 UTC, finished 19:00:28 UTC, about 52 min wall)

Hardware and compiler are in verify-it-yourself/independent_hardware/ (Apple M1 iMac, macOS 27.2, Apple clang 21.0.0, `cc -O2`, no OpenMP). Raw logs: full_env.txt and full_run.log in that folder.

```
ok   object names n = 18 and |M(k)| = 2^18 (n=18, M=-262144)
compiled mu_check.c with cc -O2
ok   C checker compiled
ok   C mu(1..20000) equals trial-division mu
ok   C mu(k-199..k) equals trial-division mu near the claimed k
ok   pure-Python sieve reproduces a(0..9)
ok   certificate has every block 0..3399 exactly once
ok   certificate chain gives M(100000000) = 1928 (published 1928)
ok   certificate chain gives M(1000000000) = -222 (published -222)
ok   certificate chain gives M(10000000000) = -33722 (published -33722)
ok   certificate chain gives M(100000000000) = -87856 (published -87856)
ok   first certificate block reaching 2^18 is the block holding k (3300)
FULL tier: recomputing all 3301 blocks from k = 1 (about 2 CPU-hours single-threaded)
ok   recomputed blocks match the certificate (3301 blocks; mismatches: [])
ok   recomputed chain gives M(100000000) = 1928 (published 1928)
ok   recomputed chain gives M(1000000000) = -222 (published -222)
ok   recomputed chain gives M(10000000000) = -33722 (published -33722)
ok   recomputed chain gives M(100000000000) = -87856 (published -87856)
ok   recomputed: no block before 3300 reaches |M| = 2^18 (k = 1 .. 330000000000 covered)
ok   recomputed M(330000000000) equals the certificate's
ok   scan reproduces published a(14) = 2589994747 (first k=2589994747 M=-16384)
ok   scan reproduces published a(15) = 7613644886 (first k=7613644886 M=32768)
ok   scan reproduces published a(16) = 37725066313 (first k=37725066313 M=-65536)
ok   scan reproduces published a(17) = 108500046711 (first k=108500046711 M=131072)
ok   scan of block 3300 gives the object's k = 330055906058, M = -262144 (first k=330055906058 M=-262144)
PASS
```
