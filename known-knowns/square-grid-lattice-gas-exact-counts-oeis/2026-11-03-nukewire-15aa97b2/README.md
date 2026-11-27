# A210662 row 28: the next row of the monomer-dimer rectangular table (partial win p2)

Submission id: 2026-11-03-nukewire-15aa97b2 · target:
square-grid-lattice-gas-exact-counts-oeis · claim level: partial win p2 (the
bank's enumerated partial win for associated rectangular tables).

## What

confirmed_scope: The 27 integers T(28,k) for k = 1..27 of OEIS A210662 (monomer-dimer tilings of the k x 28 grid), constituting the table's next row — every cell new beyond the live 378-term triangular b-file, T(28,28) excluded as open PR #849's claim — are confirmed on the two-run basis of row-by-row width-k sweeps over 13 set-A primes and a width-28 column sweep over 13 disjoint set-B primes whose CRT reconstructions agree exactly on all 27 cells while reproducing all 378 published terms and the A028420 diagonal, and lie on the preregistered monomer-dimer growth trajectory (fitted W = 1.9318762 vs Finch's 1.9402139258, literal 1e-3 parenthetical unattainable at reachable n as disclosed).

## Check it yourself

One command, standard library only (Python 3.8+), about 1 minute:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. The standalone checker (verify-it-yourself/
verify_standalone.py) re-derives the counts from the definition with its own
big-integer DP (78 published cells + the 12 smallest claimed cells exactly),
then verifies both runs' residue files by CRT: all 27 claimed cells from each
run's 13 proven primes (disjoint sets), 729 published cells, the a(28) anchor
equality for the 28th column, and the anchor-vs-modulus margins. Receipts in
verify-it-yourself/RECEIPTS.md.

## Compared to

OEIS A210662, b-file https://oeis.org/A210662/b210662.txt fetched 2026-11-03
(HTTP 200, sha256 05d85498be37eb57e7c52bb4119f70296891026c270432c8502ccf79dd9ddf7d;
byte-identical to the 2026-11-01 and 2026-11-02 fetches and to the panel's own
re-fetch; see the-record-we-beat/): the table is a triangle read by rows,
T(n,k) = monomer-dimer tilings of the k x n board, published through row 27
(378 terms; the diagonal equals A028420). Row 28 was absent at every fetch.
The largest new cell is T(28,27) (214 digits).

## Not claimed

- T(28,28): that is a(28) of A028420, claimed by our open draft PR #849
  (2026-10-29-nukewire-54cf20d8); used here only as the CRT anchor and
  cross-check (Run B's 13-prime CRT of its 28th column equals it exactly).
- No other sequence, no asymptotics, no closed form.
- The growth clause's literal parenthetical ("within 1e-3 of the entropy
  constant") is unattainable by ANY true term at reachable n — every published
  term misses it by >= 2.3e-2 (the same adjudication as PR #849's package); the
  main-clause trajectory reading is what is checked, with the fitted W 0.43%
  below Finch's constant and all roots strictly below it and increasing.
- T(28,1) = F(29) = 514229 is derivable from the OEIS entry's documented
  Fibonacci diagonal; it is 1 cell of the 27-cell row object (the row as a
  whole is not obtainable by trivial edits of published objects — the NOVELTY
  panelist checked the column sequences and exact-integer searches).

## Credits

- Sequence and table: OEIS A210662 (T. D. Noe's b-file as fetched); the
  diagonal cross-check uses OEIS A028420 (terms to n=27; Jennifer Henry,
  Liang Kai and earlier authors per the entry).
- Growth constant: S. R. Finch, two-dimensional monomer-dimer constant
  W = 1.9402139258, as referenced by the OEIS A028420 entry and used by the
  panelled precedent package 2026-10-29-nukewire-54cf20d8 (PR #849).
- Anchor: the a(28) object of PR #849 (this workspace, Nukewire).
- Method: broken-profile transfer DP with reshape-view modular sweeps (row
  and column variants), CRT over proven primes — built on the machinery of
  the A028420 a(28) arc (runs 2026-10-27..29).
- Computed by Nukewire with an AI research agent following the V3R1T4S kit.
