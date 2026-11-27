# A210662 row 29 — the 17 cells beyond the published columns (2026-11-08-nukewire-40ffe1fc)

## What

The 17 integers T(29,k) for k=12..28 of OEIS A210662 (monomer-dimer tiling
counts of the 29 x k board) — the cells of row 29 beyond the entry's
published columns k=1..11 — are correct as claimed (two-run CRT verified with
all 378 published cells and the 27-cell row-28 anchor reproduced,
from-definition exact DP confirmation for k=12..15, growth on the published
trajectory below Finch's constant), meeting bank partial win p2 for target
square-grid-lattice-gas-exact-counts-oeis.

## Check it yourself

From this folder (Python 3.8+, standard library only, ~15-30 min):

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS`. The checker recomputes published cells with its
own exact DP, CRT-verifies every published, anchor and claimed cell from
EACH of the two independent residue records, and proves all 44 CRT moduli
prime and disjoint.

## Compared to

OEIS A210662, live b-file https://oeis.org/A210662/b210662.txt — fetched
2026-11-08T19:49Z, 20:12Z, 20:40Z and 21:10Z (all HTTP 200, all
byte-identical, sha256
05d85498be37eb57e7c52bb4119f70296891026c270432c8502ccf79dd9ddf7d): 378
terms = rows 1..27 only; rows 28-29 absent. The entry's FORMULA line (fetched
2026-11-08T21:15Z, snapshot in the-record-we-beat/) maps columns 1-11 and
the diagonal to A000045, A030186, A033506..A033514 and A028420, and nothing
beyond: no published column sequence exists for k >= 12.

## Not claimed

- The eleven row-29 cells k = 1..11: already published as terms of the
  cross-referenced column sequences (k=1,2,3,4,7,8,9,10,11) or mechanically
  derivable from the published generating functions of A033508/A033509
  (k=5,6; Perepechko 2013). Our two-run values agree with those sources
  exactly (how-we-built-it/row29_crosspublished_context.json) — external
  confirmation of the computation, not claim material.
- T(29,29) = a(29) of A028420 (a separate main-criterion object).
- Row 28: open PR #960 by the same author (this claim's j=28 column
  reproduces its object exactly wherever covered — used here as the anchor).
- Growth constant precision beyond the frozen trajectory test: the bank's
  literal 1e-3 parenthetical on W is unattainable at these board sizes even
  for published cells (disclosed; the fitted W = 1.9318762 sits 8.34e-3
  below Finch's 1.9402139258; every claimed root is below W and within the
  frozen tolerance, worst deviation 1.19e-3 vs 3.19e-2).

## Credits

- Steven R. Finch's two-dimensional monomer-dimer constant
  W = 1.9402139258 (the growth reference, as used by OEIS A028420's entry
  and our a(28) package).
- R. H. Hardin (column identifications on the A210662 entry), Liang Kai and
  Alois P. Heinz (the published 378-term triangle), Sergei Perepechko (the
  A033508/A033509 generating functions), Ronald C. Read (the classical
  narrow-array method this computation extends), and the OEIS editors.
- The bank target and two-run criterion: elder-plinius/V3R1T4S,
  target square-grid-lattice-gas-exact-counts-oeis.
