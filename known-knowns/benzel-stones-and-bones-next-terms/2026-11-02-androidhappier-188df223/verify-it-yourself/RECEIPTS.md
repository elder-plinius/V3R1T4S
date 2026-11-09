# Receipts: real output of run_checks.sh

Command, from a clean copy of this package folder: `sh verify-it-yourself/run_checks.sh` (default NMAX=14).
Machine: x86_64 Linux, 8 cores, cc (Debian 14.2.0-19), Python 3.13.5. The first line is the UTC start time; the last line
(exit code and elapsed seconds) was added by the wrapper that captured the output.

```
2026-11-02T07:47:33Z
== 1. object/VALUE.txt: hash vs INDEX.csv, pinned evidence and programs
ok   object/VALUE.txt sha256 188df22331bd9b546e473501977f50e762690706bf28a3fad4cd04e7bf712445 matches INDEX.csv
ok   221 pinned files match
ok
== 2. saved run outputs vs VALUE.txt (n=20 runs A and B, published-term runs, checkpoint test)
ok   n=20 run A (benzZQ.c): 225354012176304818, exit 0, overflow 0
ok   n=20 run B (benzB64.c): 225354012176304818, exit 0, overflow 0
ok   benzZQ.c saved runs: 35 published terms reproduced
ok   benzB128.c saved runs: 32 published terms reproduced
ok   checkpoint-resume test (16,28) gives A364416(16)
ok   saved indep_check outputs: 18 terms
ok
== 3. fresh definition-level count (indep_check.py: memoized exact cover, no transfer matrix), n = 3..11
ok   18 fresh values equal the published terms
ok
== 4. fresh runs of the two n=20 programs (benzZQ.c, benzB64.c) on published terms, n = 3..14
ok   48 fresh values equal the published terms
ok
summary: A364417(20) = 225354012176304818 (two independent programs, saved runs verified; published terms reproduced fresh)
PASS
exit=0 elapsed_s=63
```
