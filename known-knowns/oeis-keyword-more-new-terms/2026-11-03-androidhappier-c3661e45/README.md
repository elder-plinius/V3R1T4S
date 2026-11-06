# A131449 row 6: organic (increasing) labelings of rooted ordered trees with 6 non-root vertices (first missing term T(6,2) = 360)

## What

Confirmed scope, quoted word for word from panel/gate.md:

> A131449 flattened index 66 (row 6, m=2) = 360, the first index missing from DATA/b-file, computed and agreed by two independent programs that reproduce all 66 existing terms; full row 6 = claim/object/ROW6.txt as the non-increasing listing (the convention every existing row follows). Criterion verdict for the panel: CONFIRMED (not partial) -- no criterion element fails and the order assumption does not affect the claimed term.

(In this package the row-6 file is object/ROW6.txt; the claim folder's claim/object/ROW6.txt is the same bytes.)

OEIS A131449 (Wolfdieter Lang, August 2007) is the irregular triangle "number of organic (also called increasing)
labelings of rooted ordered trees": row n has one entry for each of the Catalan(n) rooted ordered trees with n
non-root vertices, the number of ways to label the non-root vertices 1..n so that labels increase along every path
from the root. The entry gives rows 0..5 and the first entry of row 6 (66 terms, indices 0..65, offset 0,3, keyword
nonn,more,tabf). This folder adds the rest of row 6, starting at the first missing index:

    T(6,2) = 360                     (flattened index 66)
    row 6 (132 entries, non-increasing): 720,360,360,360,360,360,240,240,240,240,180,... (object/ROW6.txt)

The objects are object/VALUE.txt (360) and object/ROW6.txt (row 6 including the DATA term 720, comma separated;
sha256 c3661e45bbff1f5a2fb05098c2940739a0d096689e593c1095142858cb66f120). Checks: 132 = Catalan(6) entries, sum
10395 = (2*6-1)!! = A001147(6) (the entry's row-sum comment), neither used by the programs to build the row.

Row-order convention (disclosed): %N does not define the order of the trees within a row. Every existing row 0..5 is
non-increasing, and Lang's linked file lists rows 3..5 in non-increasing value with isomorphism-class bars; the run's
self-break script reproduces Lang's row-5 class grouping exactly under that order. T(6,2) = 360 needs only "largest
first": 720 (the star) is the unique maximum and 360 is the next value (5 ordered trees: one 2-chain and four leaves
under the root). The other row-6 positions are stated as the non-increasing listing; the multiset itself is
order-free.

How the row was obtained (sources in how-we-built-it/):
- Program A (how-we-built-it/pA_py/progA.py, Python): hook formula n!/prod h(v) on Dyck words, h = subtree size.
- Program B (how-we-built-it/pB_c/progB.c, C, no shared code, no hook formula): per tree, a bitmask DP counting the
  orders in which vertices can be removed leaf by leaf (= increasing labelings).
- Both reproduce all 66 DATA terms and print byte-identical rows 0..7 (how-we-built-it/outputs/). Negative fixtures
  (one entry per unordered rooted class; n! per tree) do not reproduce DATA (how-we-built-it/self-break/).
- The reproduce skeptic's own brute force over all n! label permutations (panel/reproduce_checker.py), the criterion
  skeptic's re-run and the gate's re-run give the same row 6.

## Check it yourself

From this folder:

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS`. Rough laptop time: under 1 s. Requirements: Python 3 (standard library only); a C compiler
is optional (step 4). The script checks the sha256 of both object files, then runs verify-it-yourself/verify_a131449.py,
a checker written for this package from the definition with a third method (nested-tuple trees, recursive multinomial
count): indices 0..65 must equal DATA, row lengths Catalan(n), row sums (2n-1)!!, row 6 equal to object/ROW6.txt and
index 66 equal to 360. A negative control (no increasing condition) must not reproduce DATA. With a C compiler it also
builds Program B and compares row 6. Real output: verify-it-yourself/RECEIPTS.md.

## Compared to

| source | cell | value | this package | fetched (UTC) |
|---|---|---|---|---|
| OEIS A131449 (revision #12, Aug 29 2019), DATA, b-file, history, drafts, value searches | T(6,2), flattened index 66 (and row 6) | absent (DATA and synthesized b-file end at index 65 = T(6,1) = 720; keyword nonn,more,tabf; no pending draft; contextual value searches of the row-6 head: no results) | 360 (row 6 as above) | 2026-11-03T21:53:52Z-21:54:53Z (claim time); about 2026-11-03T21:58Z (panel); 2026-11-03T22:01:20Z-22:01:21Z (gate) |

URL: https://oeis.org/A131449 (b-file https://oeis.org/A131449/b131449.txt, history
https://oeis.org/history?seq=A131449). The fetch record is in the-record-we-beat/TABLE_SNAPSHOT.md.

## Not claimed

- Only row 6 of A131449 (index 66 and the non-increasing listing of row 6). Programs A and B also print row 7 (in
  how-we-built-it/outputs/); that by-product was not judged by the panel and is not claimed here.
- The within-row order beyond "largest first" is the convention of rows 0..5, not a definition stated in %N; an editor
  choosing another order (e.g. by isomorphism class) could move positions after index 66, not T(6,2) = 360.
- Programs A and B were written by the same contributor in the same run; their independence is in language and
  algorithm (hook formula vs removal-order DP). verify_a131449.py was written for this package after the gate.
- The value 360 = 6!/2 is predictable by hand from the hook formula (disclosed in PREREG); it is computed here, not
  inferred. A search for 360 alone is uninformative; the contextual searches are the meaningful ones.
- The table check is as of the fetch times above. Nothing was submitted to the OEIS, and no pull request was opened.
- The OEIS pages and Lang's files are not shipped (third-party content); their URLs, times and sha256 are in
  the-record-we-beat/. how-we-built-it/self-break/fixtures.py reads the OEIS b-file, which must be fetched to rerun it.
- panel/ holds the four panel files plus the reproduce skeptic's checker, copied as written.

## Credits

- Wolfdieter Lang: the sequence A131449, its definition, rows 0..5 and T(6,1) = 720, and the linked files "First 6
  rows" and the n = 5 tree figure, https://oeis.org/A131449; N. J. A. Sloane and other OEIS editors (later edits/approvals).
- The OEIS Foundation, https://oeis.org; related entries A000108 (row lengths), A001147 (row sums), A000081.
- V3R1T4S kit (target bank, panel protocol, checker gate): https://github.com/elder-plinius/V3R1T4S
- Contributor: GitHub CharanRayudu (https://github.com/CharanRayudu).
