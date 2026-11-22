# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from the claim folder with the system python3 (3.9.6, standard library only) on 2026-10-19 (UTC) on the builder's Mac Studio (M3 Ultra). Wall time 37.04 s, peak resident memory 6,451,609,600 bytes (measured with /usr/bin/time -l). The line starting `total runtime` is the checker's own timing.

```
self-test: lane sweep == dense matrix built from the definition for m = 3..8 (random 60-bit vectors)
sha256 of 5 parts and of the concatenation (4496070 bytes) verified
m=22: 96909 orbits, vector expanded (4s)
m=22: exact Collatz-Wielandt  min y/x = 2151288.2406040465664364457931...  max y/x = 2151288.2406040469632851141921...  (7s)
m=24: 352698 orbits, vector expanded (12s)
m=24: exact Collatz-Wielandt  min y/x = 8098386.0605861547433225503360...  max y/x = 8098386.0605861609646998513890...  (29s)

Theorem U (M=22 even >= 4):  h2 <= ln(maxratio_22)/22      = 0.6627989728337490653103785446301568413808505570902611073012562944345236
Theorem L (2q=22, p=2, q>=2): h2 >= (ln(minratio_24) - ln(maxratio_22))/2 = 0.662798972833713810975696920930709966574437030092702444901494435812735
ENCLOSURE  0.6627989728337138109756 <= h2 <= 0.6627989728337490653104   (width 3.525433E-14)
common decimals of the two bounds: 13  -> h2 = 0.6627989728337...  certified
CERTIFIED: 0.6627989728337 < h2 < 0.6627989728338  (13 decimals)
total runtime 37 s
PASS
```

(RECEIPTS re-run by the orchestrator after the display fix; all other lines unchanged.)
