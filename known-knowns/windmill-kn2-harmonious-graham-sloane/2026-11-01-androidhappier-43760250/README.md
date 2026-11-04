# The windmill K_8^(2) is not harmonious (Graham-Sloane conjecture, case n = 8; open in DS6, 28th ed.)

## What

Confirmed scope, quoted word for word from panel/gate.md:

> For n = 8, the windmill K_8^(2) (15 vertices, 56 edges) has no harmonious labeling mod 56: two independent exhaustive programs in claim/ (checkers/wsearch.c and checkers/mitm.py), plus a third unpruned enumerator written by this reviewer, each find exactly 449,472 eight-element subsets of Z_56 containing 0 with 28 distinct pair sums and zero valid pairs, using only the translation reduction f(c) = 0, which is proved and checked by brute force at n = 4; the DS6 28th edition (Oct 30, 2025) and the literature found do not already decide this case.

A graph with q edges is harmonious (Graham and Sloane 1980) if its vertices can be given distinct labels in Z_q so
that the q edge sums f(u)+f(v) mod q are pairwise distinct. The windmill K_n^(2) is two copies of K_n that share one
vertex: 2n-1 vertices and q = n(n-1) edges. Graham and Sloane conjectured that K_n^(2) is harmonious if and only if
n = 4, and proved it for n odd and n = 6. Liu (1994) and Levine (1983) excluded further n, but not n = 8. Gallian's
Dynamic Survey DS6 (28th edition, Oct 30, 2025), Table 2, still lists the case as open ("m = 2, H? iff n = 4").
This folder decides n = 8 (15 vertices, q = 56): there is no harmonious labeling. That agrees with the conjecture.

The object is object/DECISION.txt (sha256 4376025039cb3b56a2ab755a9220f65111fb9ff3aea2340a64c1b4e0becba26e). It
states the decision, the only reduction used, every expected count for n = 3..8, and pins the sha256 of the run's
captured outputs (object/evidence/) and of the checker programs shipped in verify-it-yourself/.

Why the search is exhaustive (full argument: how-we-built-it/REPRODUCE_run.md):
- Translation is the only reduction. If f is harmonious, so is f - f(c): labels stay distinct and every edge sum
  moves by the same constant -2f(c), which permutes Z_56. So one may assume f(c) = 0. No multiplication by units
  and no swap of the two cliques is used.
- With f(c) = 0, a labeling is exactly an ordered pair (A, B) of 8-subsets of Z_56 that both contain 0, meet only
  in 0, each have 28 distinct pair sums, and have disjoint sum sets (28 + 28 = 56, so the sum sets partition Z_56).
- P1 (verify-it-yourself/wsearch.c) backtracks over A, then over B. P2 (verify-it-yourself/mitm.py) lists every
  admissible 8-set once and joins sets whose sum masks are complementary. Partial sets are rejected only when a pair
  sum repeats, which no extension can repair. Both find 449,472 admissible 8-sets and 0 pairs.
- Controls: both programs find exactly the 48 ordered pairs at n = 4. An unreduced brute force over all injective
  labelings of K_4^(2) finds 20,736 = 48 x 12 x 3! x 3!. That shows the reduction loses nothing and the search finds
  labelings when they exist. n = 3, 5, 6 and 7 come out not harmonious, as Graham and Sloane proved.

## Check it yourself

From this folder:

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS`. Rough laptop time: about 1 minute with a C compiler (P2 needs about 0.75 GB of
memory). It needs Python 3 (standard library only). A C compiler with unsigned __int128 (gcc or clang on 64-bit) is
optional; without it, P1 is skipped and P2 plus the controls still decide. The script reruns both searches from
scratch for n = 3..8, the unreduced n = 4 brute force, an independent enumeration of the n = 4 solutions, and
label-checker controls, then compares every number with object/DECISION.txt. Real output:
verify-it-yourself/RECEIPTS.md.

## Compared to

| source | cell | value | this package | fetched (UTC) |
|---|---|---|---|---|
| Gallian, A Dynamic Survey of Graph Labeling DS6 (28th ed., Oct 30, 2025), Table 2 "windmills" and Section 2.4 | harmonious K_n^(2), n = 8 | open: "m = 2, H? iff n = 4 [1249]; not H if m = 2, n odd or 6 [1249]" | decided: not harmonious | 2026-11-01T23:43:30Z (scout); 2026-11-02T00:22:54Z (panel); 2026-11-02T00:26:45Z (packaging), unchanged |
| Graham and Sloane, SIAM J. Algebraic Discrete Methods 1 (1980) 382-404, Theorem 20 | same | not covered (proved: n = 4 harmonious; n odd and n = 6 not) | decided: not harmonious | 2026-11-01T23:44:38Z |

URL: https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS6. The fetch record (times, HTTP status,
headers, hashes, quoted text) is in the-record-we-beat/TABLE_SNAPSHOT.md.

## Not claimed

- Only n = 8. The conjecture is not proved. The other open cases (n = 10, 16, 18, 20, 26, 32, 34, 36, 40, 50 up
  to 50, by the bank's reading of Liu's condition) are untouched. The partial wins p1 (n = 10) and p2 are not claimed.
- This is a computer search, not a proof by hand and not a DRAT/LRAT-certified SAT result. It is branch (b) of the
  criterion: an exhaustive search by two independent programs, plus a third unpruned enumerator in the panel.
- P1 and P2 were written in the same run by the same contributor and share the f(c) = 0 reduction. Independence
  rests on separate code paths and languages, the proved reduction, the n = 4 brute force, and the reviewer's own
  program (panel/criterion.md, panel/reproduce.md).
- The mod-14 and mod-28 obstructions in object/evidence/ (mod_projection_n8.txt, mod_multiset_n8.txt) and P3
  (wjoin.c) are supporting evidence only. Their programs are in how-we-built-it/ and are not rerun by run_checks.sh.
- Literature novelty is as recorded in panel/novelty.md. Levine (1983) and Liu (1994) were read only through their
  abstracts and DS6's quotation. An unindexed earlier decision of n = 8 cannot be ruled out.

## Credits

- Ronald L. Graham and N. J. A. Sloane: the definition of harmonious graphs, the windmill conjecture, and the cases
  n odd, n = 4 and n = 6 (On additive bases and harmonious graphs, SIAM J. Algebraic Discrete Methods 1 (1980)
  382-404): https://fanchung.ucsd.edu/ron/papers/80_07_harmonious.pdf
- Joseph A. Gallian: A Dynamic Survey of Graph Labeling, Electronic Journal of Combinatorics DS6, which records the
  open case we compared against: https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS6
- E. Levine: On a harmonious graph conjecture, Discrete Mathematics 46 (1983) 99-101 (n must be a sum of two squares).
- B. Liu: Sums of squares and labels of graphs, Math. Practice Theory (1994) 25-29 (as cited in DS6, ref. 2153).
- D. F. Hsu: Harmonious labelings of windmill graphs and related graphs, J. Graph Theory (1982) (K_4^(m)).
- V3R1T4S kit (target bank, panel protocol, checker gate): https://github.com/elder-plinius/V3R1T4S
- Contributor: credited through the GitHub account that submits this folder.
