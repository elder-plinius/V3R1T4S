# A155520 row 6: ordered trees with 6 edges by number of drawings (first missing term A(6,1) = 6)

## What

Confirmed scope, quoted word for word from panel/gate.md:

> Row 6 of A155520 for k = 1..42 is 6,2,6,9,11,4,4,4,2,15,8,2,0,6,12,0,0,1,4,6,0,4,4,0,8,4,0,0,0,4,0,0,0,1,2,0,0,2,0,0,0,1; first missing term A(6,1) (flattened index 22) = 6.

OEIS A155520 (Emeric Deutsch, March 2009) is the "Triangle read by rows: A(n,k) is the number of ordered trees with n
edges having k drawings". A drawing of an ordered tree T with n edges is a sequence of trees (T_0, ..., T_n) with
T_n = T and T_{i-1} obtained from T_i by deleting a leaf (Klazar 1997). The entry gives rows 1..5 only (21 terms,
offset 1,2, keyword nonn,tabf,more). This folder adds row 6, whose first entry is the first missing term:

    A(6,1) = 6                       (flattened index 22)
    row 6, k = 1..42: 6,2,6,9,11,4,4,4,2,15,8,2,0,6,12,0,0,1,4,6,0,4,4,0,8,4,0,0,0,4,0,0,0,1,2,0,0,2,0,0,0,1

The object is object/ROW6.txt (the row, comma separated, zeros kept; sha256
9eb90322eeb05dd9fd023d19ae3dc7142c591b06e70bbe00db1e7ece89b706b5) and object/ROW6_pairs.txt (the same values as
(k, A(6,k)) pairs). Checks: row sum 132 = Catalan(6) (the entry's row-sum comment); sum k*A(6,k) = 1787 =
A014307(6) (the entry's %F identity), neither used by any of the programs.

Zero convention (disclosed): row 6 has interior zeros (no 6-edge tree has, e.g., exactly 13 drawings); rows 1..5 have
none, so DATA does not show whether such zeros are printed. The row is listed for every k from 1 to the maximum 42,
following the entry's name (A(n,k) for each k). A(6,1) = 6 and every (k, A(6,k)) pair are the same under either
convention; only flattened positions after index 22 would move if an editor dropped zeros.

How the row was obtained (sources in how-we-built-it/):
- Program A (how-we-built-it/pA_py/progA.py, Python): backward memoised count on Dyck words; a leaf is a "UD" factor,
  D(T) = sum of D(T') over the distinct words T' from deleting one leaf.
- Program B (how-we-built-it/pB_c/progB.c, C, no shared code): forward chain DP on bit-encoded words, inserting a leaf
  ("UD") at every position, deduplicated per word, so the count at T is the number of distinct tree chains.
- Both reproduce rows 1..5 = DATA and print byte-identical rows 1..8 (how-we-built-it/outputs/). Counting deletion
  sequences with leaves distinguished (the negative fixture) does not reproduce DATA, so the distinct-tree reading is
  the one the entry's DATA pins (how-we-built-it/self-break/).
- The reproduce skeptic's own checker (panel/reproduce_checker.py, nested tuples), the criterion skeptic's third
  checker and the gate's re-run give the same row 6.

## Check it yourself

From this folder:

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS`. Rough laptop time: under 1 s. Requirements: Python 3 (standard library only); a C compiler
is optional (step 4). The script checks the sha256 of object/ROW6.txt, then runs verify-it-yourself/verify_a155520.py,
a checker written for this package from the definition with a third tree representation (preorder depth sequences):
it must give rows 1..5 = DATA, row sums Catalan(n), weighted sums A014307(n), and row 6 equal to the object. A negative
control (deletion sequences) must not reproduce DATA. With a C compiler it also builds Program B and compares row 6.
Real output: verify-it-yourself/RECEIPTS.md.

## Compared to

| source | cell | value | this package | fetched (UTC) |
|---|---|---|---|---|
| OEIS A155520 (revision #12, Sep 24 2025), DATA, b-file, history, drafts, value searches | A(6,1), flattened index 22 (and row 6) | absent (DATA and synthesized b-file end at index 21 = A(5,12) = 2; keyword nonn,tabf,more; no pending draft; value searches of the row-6 head: no results) | 6 (row 6 as above) | 2026-11-03T21:46:40Z-21:48:25Z (claim time); 2026-11-03T21:50Z (panel); 2026-11-03T21:54:58Z (gate) |

URL: https://oeis.org/A155520 (b-file https://oeis.org/A155520/b155520.txt, history
https://oeis.org/history?seq=A155520). The fetch record is in the-record-we-beat/TABLE_SNAPSHOT.md.

## Not claimed

- Only row 6 of A155520. Programs A and B also print rows 7 and 8 (in how-we-built-it/outputs/); those by-products
  were not judged by the panel and are not claimed here.
- Programs A and B were written by the same contributor in the same run; their independence is in language,
  representation and direction (backward deletion vs forward insertion). verify_a155520.py was written for this
  package after the gate.
- The value A(6,1) = 6 fits the visible pattern A(n,1) = n of rows 1..5; it is computed here, not inferred from the
  pattern. Klazar 1997 and its Addendum give only total drawing counts (A014307), not a by-k table (panel/novelty.md).
- The entry's example prints the second drawing of UUDDUD identical to the first (an evident typo for
  *, UD, UDUD, UUDDUD); the count 2 is unaffected and is reproduced.
- The table check is as of the fetch times above. Nothing was submitted to the OEIS, and no pull request was opened.
- The OEIS pages fetched are not shipped (third-party content); their URLs, times and sha256 are in the-record-we-beat/.
- panel/ holds the four panel files plus the reproduce skeptic's checker, copied as written.

## Credits

- Emeric Deutsch: the sequence A155520, its definition, example and rows 1..5, https://oeis.org/A155520; Michel Marcus
  (keyword tabf) and Andrei Zabolotskii, Joerg Arndt, Alois P. Heinz, Bruno Berselli (later edits/approvals).
- Martin Klazar, Twelve countings with rooted plane trees, European Journal of Combinatorics 18 (1997), 195-210;
  Addendum 18 (1997), 739-740, https://doi.org/10.1006/eujc.1995.0095 (drawings; totals A014307).
- The OEIS Foundation, https://oeis.org; related entries A014307, A000108.
- V3R1T4S kit (target bank, panel protocol, checker gate): https://github.com/elder-plinius/V3R1T4S
- Contributor: GitHub CharanRayudu (https://github.com/CharanRayudu).
