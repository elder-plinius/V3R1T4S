# Criterion skeptic verdict: [[33,7,15;12]]_3 claim

context: subagent (Claude Agent tool, model claude-opus-5-5), given only claim/

**Bottom line: PASS.** The matrix S in claim/object/eaqecc_33_7_15_12.json meets every clause of the full success
criterion, checked literally. It is a non-catalytic EAQECC with (n,k,c) = (33,7,12) and exact distance d = 15. The
cell [[33,7,14-23;12]]_3 is listed on the live page I fetched myself, so d is strictly above d_lower = 14 and at most
d_upper = 23. I found no stretched definition, hidden quantifier, capped search or catalytic reading. No cell the
table's own rules derive from listed entries already reaches 15 at (33,7,12). This is a win on the full criterion,
not on partial win p1 or p2.

My own code is in work-criterion/mine/: prep.py, bz.c, prep3.py, bz3.c, check_min.py, and the brute-force
validators test_bz.py and test_bz3.py. My fetch is in work-criterion/fetched/.

## Clause by clause

| Clause | Required | What I checked (own code unless said) | Found |
|---|---|---|---|
| Explicit generator matrix | exact, over GF(3) with 2n columns (or GF(9)) | S in the JSON: shape and entries | 38 x 66, every entry in {0,1,2}, rows (x\|z); file sha256 5713c745...787256 matches CLAIM.md |
| s independent generators | s = rank S | mine/prep.py, GF(3) elimination | rank(S) = 38 = number of rows, so s = 38 |
| c = rank(S J S^T)/2, c >= 1 | J = [[0,I],[-I,0]] | I built the 38 x 38 commutation matrix with x.z' - z.x', checked it is antisymmetric, and took its GF(3) rank | rank 24, so c = 12 (>= 1, not the excluded c = 0 case) |
| k = n - s + c | | arithmetic | 33 - 38 + 12 = 7, matching the claimed (n,k,c) = (33,7,12) |
| span(S)^perp in full | | symplectic null space of S | dim N = 28 = 2n - s, every basis vector orthogonal to all 38 rows |
| Isotropic part I = span(S) ∩ N | | two ways: from the kernel of the commutation matrix, and from dim S + dim N - dim(S+N) | dim I = 14 both ways (= s - 2c) |
| d exact = min weight of N \ I | exhaustive, not sampled | (a) I verified that N is invariant under T:(x_i,z_i) -> (z_i, x_i+z_i), and T^2 = T + 1, so N = phi(C) for a GF(9)-linear [33,14] code C with symplectic weight equal to Hamming weight. My own two-disjoint-information-set Brouwer-Zimmermann (mine/bz.c) enumerated every message of weight <= 7 in set 1 and <= 6 in set 2: 1006817254 + 107139046 nodes, exactly sum C(14,t)8^(t-1). Minimum found = 15, and every word not enumerated has weight >= 8 + 7 = 15. So d(C) = 15. (b) A GF(3)-only additive version that uses no GF(9) structure (mine/bz3.c) gives the same: 4027269016 + 428556184 nodes, exactly matching the formula, min 15, bound 15. Both programs agreed with brute force on random small codes with 0 failures (test_bz.py, test_bz3.py). (c) mine/check_min.py rebuilt 40 of the weight-15 words directly as GF(3) vectors: all 40 have symplectic weight 15, are orthogonal to every row of S, and are NOT in span(S), so none is in I | min weight over all of N is 15, so min over N \ I >= 15. Weight-15 vectors in N \ I exist, so d = 15 exactly. Isotropic vectors are not counted (the lower bound covers all of N, a superset). The author's witness (checkers/witness.py, support {0,11,14,...,27}) also passes my independent check: weight 15, in N, not in span(S) |
| Cell of the live table, re-fetched | listed cell (n,k,c) | One GET at 2026-10-24T21:29:07Z (finished 21:29:08Z), HTTP 200, 628039 bytes, sha256 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c, footer "Last change: 10.07.2025" (fetched/RECORD.txt). These are the same bytes as the claim's own fetch at 19:55:15Z (table/RECORD.md), about 10 minutes before the package was assembled (20:05Z file times) | Cell is listed verbatim: `[[33,7,14-23;12]]<sub>3</sub>`, title "lengthening of [[27,7,14;12]] from arXiv:2207.05647" |
| d > d_lower and d <= d_upper | strict | 15 > 14; 15 <= 23 | met |
| Non-catalytic | table setting | The page states it lists the non-catalytic setting. Here c is the plain ebit count rank(SJS^T)/2 and k = n - s + c, with no ebits recycled | met |

## Hidden-quantifier and null-model checks

- **Same (n,k,c) as claimed?** Yes, (33,7,12), computed from S alone. The author's G9 spans exactly my C:
  ranks 14, 14, and 14 for their union.
- **Exhaustive search, not capped?** Yes. Node counts equal the closed-form totals, and the stopping bound
  (8 + 7 = 15) reaches the minimum found.
- **Already covered by the table?** No. The table's propagation rules give at most 14 at (33,7,12):
  - lengthening of [[32,7,14-23;12]] gives 14;
  - subcode of [[33,8,14-22;12]] gives 14;
  - puncturing of [[34,7,14-24;12]] gives 13;
  - the c = 10 cell is [[33,7,13-23;10]].

  The lower cell [[33,7,15-24;14]] needs 2 more ebits (entangled pairs).
- **Consistency with the table's upper bounds?** Codes derived from this one stay within the listed upper bounds:
  - [[33,6,15;12]] against <= 25;
  - [[34,7,15;12]] against <= 24;
  - [[32,7,14;12]] against <= 23;
  - [[32,8,14;12]] against <= 21.

  So the claimed code does not contradict any listed upper bound.
- **Is d = 15 a random-code effect?** No. For a random GF(9) [33,14] code the Gilbert-Varshamov estimate is
  roughly 10 to 11. A distance of 15 is consistent with the structured Hermitian-curve AG construction described.
  The author's rebuild command (rebuild/build_x_lead.py) reproduces the object byte for byte (same sha256).
- **Author's tools, run as a cross-check only:**
  - gf9info prep prints n=33 s=38 c=12 k=7 dim_N=28 dim_I=14;
  - both witness tools print weight 15 outside the isotropic part;
  - bz64 prints d=15 with words=4027269016.

  All of these agree with my own results. I did not run the author's 15-25 CPU-minute subset test, because my
  two exhaustive programs already settle d exactly.
- injection_suspected: none. No instruction-like text in the fetched page or in claim/.

confirmed_scope: The 38 x 66 GF(3) stabilizer matrix S in object/eaqecc_33_7_15_12.json has 38 independent rows, c = rank(S J S^T)/2 = 12 and k = n - s + c = 7 at n = 33, and the minimum symplectic weight of span(S)^perp outside span(S) ∩ span(S)^perp is exactly 15, strictly above d_lower = 14 and at most d_upper = 23 of the cell [[33,7,14-23;12]]_3 listed on https://eaqecc.codetables.de/qutrit.php as fetched at 2026-10-24T21:29:07Z (HTTP 200, sha256 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c).

pass: true
