# Criterion skeptic verdict: [[33,9,14;12]]_3 claim

Bottom line: PASS. The stabilizer matrix S in claim/object/eaqecc_33_9_14_12.json literally meets the full success
criterion (not a partial win). Recomputed from S alone: s = 36 independent generators, c = rank(S J S^T)/2 = 12,
k = 33 - 36 + 12 = 9. The exact minimum symplectic weight on span(S)^perp minus the isotropic part is d = 14. The
cell (33,9,12) of the live qutrit table, which I re-fetched once (HTTP 200), reads [[33,9,13-21;12]]_3, so
13 < 14 <= 21. The cell is listed, c >= 1, and the setting is non-catalytic. No listed neighbouring cell already
implies d >= 14 there.

context: subagent (Claude Agent tool, model claude-opus-5-5), given only claim/

## What I ran (my own code, in mine/)

- mine/params.py (numpy, exact GF(3) arithmetic, no code shared with claim/checkers) computes:
  - s, c and k;
  - N = {v : S J v^T = 0};
  - I = span(S) ∩ N, by the Zassenhaus algorithm;
  - whether N is invariant under M(x|z) = (z | x+z), with M^2 = M + 1 checked;
  - a GF(9) generator matrix (written to mine/G9_mine.txt);
  - the full weight distribution of I, by enumerating all 3^12 of its vectors.
- mine/bz9.c is my own Brouwer-Zimmermann program over GF(9). It uses disjoint information sets and exhaustive
  enumeration of messages up to a weight. Its lower bound counts only full-rank sets.
- mine/count14.c does an exact count of codewords of weight <= 14. It splits the words by their weight on
  information set 1: words with weight <= 7 there are taken from set 1, and words with weight >= 8 from set 2 at
  t <= 6.
- mine/check_witness.py checks a witness directly against S: S J v^T = 0, v not in span(S), and its symplectic
  weight.
- mine/consistency.py checks that the JSON's G9 and D9 are consistent with S.
- mine/parse_table.py reads the fetched table: the cell text only, not the title attributes.
- I also ran the author's cheap steps 1, 2-prep, 3, 4-prep and 5 (outputs in mine/author_run/). I did not rerun the
  author's long exhaustive loops: infoset.c for m = 19, 20 and subset_ea64.c for W = 13, 14. My verdict does not
  rest on them.

## Clause by clause

1. **Explicit exact generator matrix over GF(3), symplectic form, 2n columns.**
   S is 36 x 66 and every entry is in {0,1,2}. The JSON hash is
   059282c383e7d059867ecd1a1ec51d54197af25b2c6a320dd26b150ac1a99391, the same as stated in CLAIM.md. The author's
   rebuild (step 1) reproduces a byte-identical object (same sha256).
   Extra consistency checks (mine/consistency.py):
   - S equals [phi(r), phi(w r)] for the rows r of D9, in order.
   - G9 has rank 15 and is Hermitian-orthogonal to D9 (which has rank 18).
   - RREF(G9) equals the RREF of the code I derived from S's symplectic dual.
   Met.

2. **s independent generators.** rank_GF(3)(S) = 36 = the number of rows, so the rows are independent and s = 36.
   Met.

3. **c = rank(S J S^T)/2, c >= 1.** With J = [[0,I],[-I,0]], S J S^T is antisymmetric and has rank 24, so c = 12.
   Met.

4. **k = n - s + c.** 33 - 36 + 12 = 9, the same as claimed. The (n,k,c) = (33,9,12) I recomputed equals the
   claimed values and the JSON fields (n=33, k=9, c=12, d=14). Met.

5. **d computed exactly as the minimum weight on span(S)^perp outside span(S) ∩ span(S)^perp.**
   - Dimensions: dim N = 30 and dim I = 12, which equals s - 2c. Also dim(span S + N) = 54 = 36 + 30 - 12.
   - GF(9) structure: N is invariant under M, and I is too. So psi(x_i, z_i) = x_i + w z_i maps N onto a GF(9)-linear
     [33,15] code C, and symplectic weight equals Hamming weight. The GF(9) span of the derived rows maps back to the
     30-dimensional N.
   - Lower bound d >= 14: bz9 found two disjoint full-rank information sets (columns 0-14 and 15-29) and a
     rank-3 remainder (columns 30-32). It enumerated every message of weight <= 6 on both full sets
     (354065966 projective words). The lower bound is 7 + 7 = 14, the upper bound found is 14, and the output reads
     `RESULT d=14 (exact: lower 14 >= upper 14)` (3.01 s).
   - Independent exact count (count14, 2040962606 words, 50 s): it found 0 words of weight < 14, and 10404
     projective weight-14 words on 10404 distinct supports. The 10404 matches the author's separate GF(3) subset
     count in REPRODUCE.md.
   - Isotropic vectors are not counted: the minimum nonzero weight of I is 18 (full distribution
     {0:1, 18:8, 19:32, ...}). So no vector of weight <= 17 in N lies in I, and every weight-14 vector of N is in
     N minus I.
   - Witness: the weight-14 word from bz9 maps to v with S J v^T = 0 and v not in span(S), with symplectic weight
     14 and support {0,1,3,4,5,6,9,12,13,14,16,30,31,32}. My checker confirms the author's two witnesses (the GF(3)
     vector and the GF(9) word) in the same way. The author's bz64 independently prints d=14.
   - The search is not sampled or capped. The lower-bound argument is complete: a word that was not enumerated has
     weight >= 7 on each of two disjoint information sets.
   - Conclusion: d = 14 exactly. Met.

6. **A listed cell of the live table, re-fetched immediately before the verdict.**
   - My fetch: one plain curl GET of https://eaqecc.codetables.de/qutrit.php, User-Agent "V3R1T4S-research-agent
     (honest single fetch)", no retries. Started 2026-10-24T22:29:54Z and ended 2026-10-24T22:29:55Z (`date -u`).
     HTTP 200, 628039 bytes, sha256 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c. This is
     byte-identical to the author's copy from 19:55Z (claim/table/). The footer reads "Last change: 10.07.2025".
     Saved as fetched/qutrit.php, with fetched/qutrit.headers.txt and fetched/fetch_log.txt.
   - The cell is listed, verbatim: `[[33,9,13-21;12]]<sub>3</sub>`, with title "lengthening of [[27,9,13;12]]
     increasing dimension of [[27,8,13;11]] from arXiv:2207.05647".
   - The parser found 3888 cell entries and no duplicate (n,k,c). The row n=33, k=9 matches claim/table/RECORD.md.
   - The claim package records no separate claim timestamp. The cell was unchanged on the live page at my fetch,
     2.5 h after the author's fetch.
   - No injected instructions were found in the page or in claim/.
   - Met, as of my fetch.

7. **d > d_lower and d <= d_upper.** 14 > 13 and 14 <= 21. Met.

8. **Non-catalytic, c >= 1, c = 0 excluded.** The page defines c as "number of required maximally entangled pairs
   of qudits (non-catalytic setting)", and says that it does not consider the catalytic rule. The claim uses the plain
   formula k = n - s + c, with no catalytic trade-off. c = 12. Met.

## Null models and subsumption

- **Neighbouring cells under the page's own one-step propagation rules.** None gives d >= 14 at (33,9,12):

  | Rule | Source cell | Source bounds | Implied bound at (33,9,12) |
  |---|---|---|---|
  | subcode | (33,10,12) | 13-19 | 13 |
  | lengthening | (32,9,12) | 13-20 | 13 |
  | quantum shortening | (34,8,12) | 14-23 | 13 |
  | increasing dimension | (33,8,11) | 13-22 | 13 |
  | length reduction | (34,9,11) | 13-21 | 13 |
  | puncturing | (34,9,12) | not listed | none |

- **Better listed codes.** No listed cell has n <= 33, k >= 9, c <= 12 and d_lower >= 14.
- **The c = 13 cell.** It reads 14-21, but it uses more ebits, so it does not imply the claimed c = 12 code.
- **Naive closure.** I also closed the whole table under the six rules naively, without their side conditions
  (mine/closure.py). It gives an absurd 27 > d_upper = 21 at the target, through repeated "increasing dimension"
  from [[36,1,27;1]]. So the rules carry side conditions, and this closure says nothing either way. I did not use
  it.
- **The win is genuine, not a partial win.** d exceeds d_lower, which is a full-criterion win, not p1 or p2.
- **Limit.** Subsumption was checked only against the live table, not against literature outside it.

confirmed_scope: The 36 x 66 GF(3) stabilizer matrix S in claim/object/eaqecc_33_9_14_12.json (sha256 059282c383e7d059867ecd1a1ec51d54197af25b2c6a320dd26b150ac1a99391) defines a non-catalytic qutrit EAQECC with s = 36, c = 12, k = 9 and exact minimum distance d = 14 (minimum symplectic weight on span(S)^perp outside span(S) ∩ span(S)^perp), which is strictly greater than d_lower = 13 and at most d_upper = 21 for the listed cell [[33,9,13-21;12]]_3 of https://eaqecc.codetables.de/qutrit.php as fetched at 2026-10-24T22:29:54Z (HTTP 200, sha256 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c).

pass: true
