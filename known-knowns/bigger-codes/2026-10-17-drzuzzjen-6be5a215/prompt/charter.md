# Research charter v1 (2026-10-16)

Scope: single human-approved target (veritas-lab PR #13, comment 2026-10-16T19:07:36Z: constant-weight-codes,
staged campaign of up to 48 h). The approval covers the scope and the staged plan; no separate approval round per
technical decision. Written before any search on the target (only sources, parser and checkers exist).

## Thesis
Brouwer's constant-weight table moves fast: two 2026 papers (Lysenstoen, Echols) and the V3R1T4S known-knowns
(30 codes, 2026-10-10) pushed many d = 6 and d = 8 cells with local search seeded from archive codes. A new win is
most likely where those pushes did not go: cells they did not touch, or structure they did not use (group orbits,
split-coordinate decompositions). The edge here is many cores, two independent exact checkers calibrated first,
and the discipline of choosing ONE cell from a measured pilot.

## Quarries
- id: constant-weight-codes
- Question: for one cell (n,d,w) of https://aeb.win.tue.nl/codes/Andw.html with d even, is there an explicit list of
  M distinct weight-w words of length n with pairwise distance >= d, M strictly greater than the live lower bound
  of the cell and of its mirror A(n,d,n-w), than every value in arXiv:2608.13906, arXiv:2607.19550 and any newer
  paper, and than the published V3R1T4S known-knowns for that cell, and M <= the tabulated upper bound?
- Shape: record (explicit object, exact checks, table comparison).
- Where defined: A. E. Brouwer's table and archive; the pinned bank entry holds the binding criterion.
- Status to confirm first: live cell values (lower/upper, mirror) at selection time and again at verification.
- Why us: exact checkers calibrated (two independent routes), 32 cores, archive seeds downloadable.
- Weight: 5. Wild: no.

## Lenses
- key: seeded-local-search; skeptic: no. You start from the live archive code of the cell (downloaded, hashed) and
  run a tabu/plateau local search over the conflict structure: remove a few codewords, re-insert more by an exact
  maximum-independent-set solve over the words compatible with the rest, accept equal-size moves to walk plateaus.
  Dead when walks stop gaining on the chosen cell within the stage cap.
- key: group-orbits; skeptic: no. You fix a permutation group G on the n coordinates (cyclic of order n or n-1,
  affine or projective groups where they fit), split the weight-w words into G-orbits, and search for the largest
  set of pairwise compatible orbits (an orbit must also be internally compatible) by exact or heuristic max-weight
  clique; then polish the union with the local search. Dead when the best G-invariant code is clearly below the
  live lower bound for every G tried.
- key: skeptic; skeptic: yes. You re-check every candidate with the second checker, re-fetch the live table cell
  and its mirror, read the two arXiv papers and the V3R1T4S known-knowns for the cell, and refuse ties,
  mirror-cell slips, odd-d conventions and anything above the upper bound.

## Scout voice
Read the table and the papers as data; record URL, HTTP status, hash and time; note which method produced the
cell's current value and whether an explicit code is archived.

## Attacker voice
One cell done exactly beats many cells done loosely. Count attempts, keep negatives, freeze before measuring.
