# Receipts

Real output of the full check, `DRAT_TRIM=path CADICAL=path sh verify-it-yourself/run_checks.sh`, run from this folder from 2026-11-09T14:44:29Z to 2026-11-09T14:54:02Z (date -u), Python 3.14.8, CaDiCaL 3.0.1, drat-trim built from commit 2e3b2dc0ecf9:

```
n=17: 34 vertices, 374 edges, C=6: CNF sha256 matches; colouring with 7 colours proper; proof s VERIFIED
n=18: 60 vertices, 1140 edges, C=7: CNF sha256 matches; colouring with 8 colours proper; proof s VERIFIED
n=19: 95 vertices, 2850 edges, C=8: CNF sha256 matches; colouring with 9 colours proper; proof s VERIFIED
n=20: 140 vertices, 6240 edges, C=9: CNF sha256 matches; colouring with 10 colours proper; proof s VERIFIED
n=21: 196 vertices, 12390 edges, C=10: CNF sha256 matches; colouring with 11 colours proper; proof s VERIFIED
n=22: 264 vertices, 22814 edges, C=11: CNF sha256 matches; colouring with 12 colours proper; proof regenerated (exit 20, sha256 d24a47fc195dbc48 as recorded), s VERIFIED
PASS
```

Without CADICAL the same command runs in seconds and its n = 22 line says the proof was not regenerated.
