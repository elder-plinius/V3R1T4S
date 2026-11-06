# A331783(21) = 10950456: locally disjoint rooted semi-identity trees with 21 vertices

## What

Confirmed scope, quoted word for word from panel/gate.md:

> For the live OEIS entry A331783 (locally disjoint rooted semi-identity trees with n unlabeled vertices; keyword nonn,more; offset 1; DATA and the synthesized b-file end at a(20) = 4242226, with no links, extensions, or pending drafts; re-fetched 2026-11-03T21:22Z), the claim is A331783(21) = 10950456, using the entry's own definition (name, comments and Mathematica disjunsQ code: one branch, or non-leaf branches pairwise distinct and every two branches equal or with empty intersection, applied recursively). n = 21 is the first missing index, A331783 is not excluded by the bank, the bank criterion is quoted verbatim, PREREG predates all programs, two independently written claim programs (C id-set backtracking, Go literal partition x tuple transcription) plus the reproduce skeptic's own C checker and the criterion skeptic's literal Python transcription all reproduce a(1..20) = DATA and give 10950456, and OEIS value searches for 10950456 and 4242226,10950456 return no results. By-products a(22..23) are out of scope.

The correctness of the count itself was checked by the REPRODUCE skeptic (panel/reproduce.md): its own C checker
(panel/reproduce_checker.c), written from the definition before it read the authors' code, and the authors' Programs A
and B give a(1..20) = DATA and a(21) = 10950456. The criterion skeptic also wrote a literal Python transcription of the
entry's Mathematica code (panel/criterion_lit.py), which gives the same 21 values.

OEIS A331783 (Gus Wiseman, January 2020) is the "Number of locally disjoint rooted semi-identity trees with n
unlabeled vertices": a rooted tree is semi-identity if the non-leaf branches of every vertex are pairwise distinct
(leaf branches may repeat), and locally disjoint if no two distinct branches of any vertex share a common branch. The
entry gives a(1..20) = 1, 1, 2, 4, 8, 17, 37, 83, 191, 450, 1076, 2610, 6404, 15875, 39676, 99880, 253016, 644524,
1649918, 4242226 (offset 1,3) and carries keyword more. This folder adds the next term:

    A331783(21) = 10950456

The object is object/VALUE.txt, the single line `A331783(21) = 10950456` (sha256
17dff06626c3c02e2d547f5d180ce2ec5f658153433a495413f4f62c8d21683f).

How the number was obtained (sources in how-we-built-it/):
- Program A (how-we-built-it/pA_c/progA.c, C): a tree is a set of distinct non-leaf trees (strictly increasing ids)
  with pairwise disjoint branch-type sets, checked with a mark array, the remaining vertices being leaf children.
- Program B (how-we-built-it/pB_go/main.go, Go, no shared code): a literal transcription of the entry's Mathematica
  ldrsi/disjunsQ: for every integer partition of n-1, every multiset of trees with those sizes is tested with disjunsQ
  (sorted-list merge test for empty intersection).
- Program C (how-we-built-it/pC_py/progC.py, Python with sympy, n <= 11): Matula-Goebel numbers tested against the
  A331682 rule; gives A000081 and a(1..11) = DATA.
- A and B print a(1..20) = DATA and a(21) = 10950456 (how-we-built-it/outputs/). Without the disjointness test both give
  1, 1, 2, 4, 8, 18, 41, ... (semi-identity trees, A306200), so the test is live.

## Check it yourself

From this folder:

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS`. Rough laptop time: about 5 s, about 300 MB RAM. Requirements: Python 3 (standard library
only); a C compiler is optional (step 4). The script checks the sha256 of object/VALUE.txt, then runs
verify-it-yourself/verify_a331783.py, a checker written for this package from the definition (sets of distinct
non-leaf branches with pairwise disjoint branch-type sets, built size by size; plus a literal transcription of the
entry's disjunsQ that must agree for n <= 11): it must give a(1..20) = DATA and a(21) equal to the value in
object/VALUE.txt. A negative control without local disjointness must not reproduce DATA. With a C compiler it also
builds Program A and requires its output to match for n = 1..21. Real output: verify-it-yourself/RECEIPTS.md.

## Compared to

| source | cell | value | this package | fetched (UTC) |
|---|---|---|---|---|
| OEIS A331783 (revision #6, Feb 02 2020), DATA, b-file, history, drafts, value search | a(21) | absent (DATA and b-file end at a(20) = 4242226; keyword nonn,more; no pending draft; value searches 10950456 and 4242226,10950456: no results) | 10950456 | 2026-11-03T20:04:59Z-20:06:47Z (claim time); 2026-11-03T21:19Z-21:20Z (panel); 2026-11-03T21:22:21Z (gate) |

URL: https://oeis.org/A331783 (b-file https://oeis.org/A331783/b331783.txt, history
https://oeis.org/history?seq=A331783). The fetch record is in the-record-we-beat/TABLE_SNAPSHOT.md.

## Not claimed

- Only one cell, A331783(21). Program A was also run to n = 23 in the run; those by-products were not judged by the
  panel, are not shipped and are not claimed here.
- Programs A, B and C were written by the same contributor in the same run. Their independence is in language and
  algorithm (id-set backtracking vs. partition x tuple transcription). The reproduce skeptic's checker is independent
  code but the same algorithm family as Program A (it says so in panel/reproduce.md); Program B and the criterion
  skeptic's literal transcription are the algorithmically different confirmations. verify_a331783.py was written for
  this package after the gate.
- Related sequences: A316473 (locally disjoint rooted trees, extended in 2026 by R. P. P. McKone) and A316471
  (locally disjoint rooted identity trees) are different cells with different values; neither holds 10950456
  (panel/novelty.md). The same contributor has a separate run on A316471; it does not print or claim A331783 terms.
- The table check is as of the fetch times above. Nothing was submitted to the OEIS, and no pull request was opened.
- The OEIS pages fetched are not shipped (third-party content); their URLs, times and sha256 are in the-record-we-beat/.
- panel/ holds the four panel files plus the reproduce skeptic's checker and the criterion skeptic's literal
  transcription, copied as written. The scratch-folder paths under /workspace/ that the skeptics mention are their own
  temporary copies, not paths needed for checking.

## Credits

- Gus Wiseman: the sequence A331783, its definition, Mathematica code and terms a(1..20), https://oeis.org/A331783,
  and the Matula-Goebel characterization A331682, https://oeis.org/A331682; Susanna Cuyler, editor who approved
  revision #6.
- The OEIS Foundation, https://oeis.org; related entries A316471, A316473 (R. P. P. McKone's 2026 extension), A306200,
  A000081.
- V3R1T4S kit (target bank, panel protocol, checker gate): https://github.com/elder-plinius/V3R1T4S
- Contributor: GitHub CharanRayudu (https://github.com/CharanRayudu).
