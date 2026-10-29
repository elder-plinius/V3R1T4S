# REPRODUCE skeptic verdict: [[24,4,13;10]]_3 (object/eaqecc_24_4_13_10.json)

Bottom line: CONFIRMED. My own exact checker, written from the definition before I read any of the author's code,
enumerates all 3^18 - 1 = 387420488 nonzero vectors of span(S)^perp and gives s = 30, rank(S J S^T) = 20, c = 10,
k = 4 and d = 13. This matches the claimed parameters and every value REPRODUCE.md prints in steps 1 to 7. I found
no mismatch, no missing object and no non-determinism.

context: subagent (Claude Agent tool, model claude-opus-5-5), given only claim/

Run started 2026-10-25 10:59:21 UTC and the last command ran at 11:03:35 UTC (from `date -u`). Object sha256
feeeff03749ecfd57a5b84b8778a2ffe2111723da17f31a3f197d02d048c1794 (from `shasum -a 256`, same as CLAIM.md).

## Definition (quoted from CLAIM.md, success criterion)

> with s independent generators on Alice's n qutrits, c = rank(S J S^T)/2 (half the rank of the symplectic
> commutation matrix) and k = n - s + c; the minimum distance d, computed exactly as the minimum weight of vectors in
> the symplectic dual of span(S) that are not in the isotropic part span(S) ∩ span(S)^perp (the EAQECC definition
> used by Grassl), is STRICTLY GREATER (direction: max) than the table's d_lower for that (n,k,c), and d <= d_upper.

"Weight" is symplectic weight: the number of positions i with (x_i, z_i) != (0, 0). The symplectic form is
<(x|z),(x'|z')> = x.z' - z.x', which is the object's stated convention, J = [[0,I],[-I,0]].

## My checker (mine/, written before I read claim/checkers or claim/rebuild)

- `mine/prep.py`: GF(3) row reduction on S alone. It computes s = rank(S), M = S J S^T and its rank, c, k, and a
  basis of N = span(S)^perp as the right nullspace of S J. It computes I = span(S) ∩ N as {aS : aM = 0}. It asserts
  that dim I = s - rank(M), that every I vector lies in N and in span(S), and that rank(S + N) = s + dim N - dim I.
  It extends the I basis to a basis of N, with the I vectors first. It also writes P, a basis of the ordinary
  complement of span(S), so that v is in span(S) iff P v^T = 0.
- `mine/enum.c` (compiled as `enum_infoset`): visits every vector of N exactly once with a modular ternary Gray code
  (one basis vector added per step, nothing stored) and records the symplectic weight histogram. For each vector of
  weight <= 13 it decides membership in I in two independent ways (the coefficients on the non-I basis vectors are
  all zero; P v^T = 0) and counts any disagreement. It also rebuilds the vector from its coefficients and compares.
  Vectors of weight > 13 still count toward the minimum outside I through the coefficient test, so d is exact
  either way. A self-test of the bit-sliced GF(3) addition runs at startup.

## Tests of my checker

- Brute force (`mine/bruteforce_test.py`, 150 random S with n = 3 to 5, some with dependent rows, seed 20261025):
  the brute-force side tests all 3^(2n) vectors directly for symplectic orthogonality and for membership in span(S)
  by rank. It agreed with my checker on the full weight histogram of N, on the in-I and outside-I counts at every
  weight, and on d, at both W = n and W = 0. Result: `all_match=True`. The true d values were 1, 2, 3, 4 and none
  (N = I), with c > 0 and c = 0 cases.
- Seeded negatives on the real S (`mine/negatives.py`):
  - With the columns of qutrit 0 zeroed, d_EA = 1 (expected 1).
  - With S[0][0] changed, c = 11, k = 5, d_EA = 12.
  - With the last row dropped, s = 29, k = 5, d_EA = 1.
  The checker therefore catches a wrong code.
- Determinism: a second run of `enum_infoset` on the real S produced byte-identical output (sha256
  b68da63e339338077f3e2b734fbf9d057a35c5ddd7575dc2af87b9a4d07c656c, both runs).

## My results on S (whole space, no sampling)

- `n=24 rows=30 s=30 rank(SJS^T)=20 c=10 k=4 dimN=18 dimI=10`
- `nonzero vectors enumerated=387420488 (expected 387420488)`
- Weight histogram of N \ {0}: 13:5000 14:52776 15:234712 16:936480 17:3823992 18:11887736 19:29569848
  20:59578776 21:90709728 22:98857984 23:68830416 24:22933040
- `weight 13: in I 0, outside I 5000`. Both membership tests agreed on every vector (disagreements = 0,
  recompute mismatches = 0).
- `d_EA=13`. Every nonzero vector of N has weight >= 13, and the weight-13 witness is outside I. I re-checked the
  witness separately: weight 13, orthogonal to all rows of S, not in span(S).
- The run took 1.19 s with a peak RSS of 1425408 bytes (from `/usr/bin/time -l`).

Claimed (n, k, c, d) = (24, 4, 10, 13). Everything matches.

## Re-derivation of the no-search proof (mine/proof_check.py, own GF(9) arithmetic and points)

Each premise checked:

- **Field and w.** With GF(9) = GF(3)[w]/(w^2 - w - 1): w^2 = w + 1 holds, w generates GF(9)^*, and the norm
  w^4 = -1 holds.
- **Curve points.** y^3 + y = x^4 has 27 affine points. Coordinates 0, 3, 6, 11 in (x, y) order are
  (0,0), (1,2), (2,2), (3,6), as CLAIM.md states.
- **Monomials.** There are 9 monomials x^i y^j with j <= 2 and 3i + 4j <= 11. Their pole orders are
  0, 3, 4, 6, 7, 8, 9, 10, 11, all distinct, and x y^2 is the only one of order 11. The degree argument therefore
  holds: a nonzero f in L(11 P_inf) has at most 11 affine zeros, and at most 10 when its x y^2 coefficient (the 28th
  coordinate) is 0. That gives d(E_11) >= 17.
- **d(E_11) exactly.** I computed it by full enumeration of all 3^18 - 1 nonzero words of phi(E_11), length 28,
  with my enumerator: min weight 17 and histogram starting 17:41688. The premise holds exactly.
- **Puncturing and scaling.** Deleting 4 coordinates lowers any weight by at most 4, and scaling columns by w != 0
  changes no weight. The GF(3)-rank of phi(E') stays 18 (GF(9)-dimension 9), so d(E') >= 13.
- **Link to S.** For my rebuilt E', the vectors phi(E') and phi(w E') have GF(3)-rank 18 and are symplectically
  orthogonal to every row of S. Since dim N = 18, span(S)^perp = phi(E'), and symplectic weight on phi(E') equals
  Hamming weight on E'. Also, rowspace(G9) = E', and S equals phi(D9) taken as rows r, w r in order.
- **Conclusion.** d_EA >= 13 from the bound, and d_EA <= 13 from the weight-13 witness outside span(S). The proof
  is sound.

## Author's REPRODUCE.md steps (run in a copy of claim/ at author_run/, python3 -I, nice -n 10)

| Step | Ran | Result versus REPRODUCE.md |
|---|---|---|
| 1 rebuild | yes | Prints `E_11 deleted=[0, 3, 6, 11] ... [24,9] hull=5 -> [[24,4,?;10]]  S 30x48  D9 15x24`. rebuilt.json sha256 = feeeff03...1794 = object. Match |
| 2 GF(9) info sets | yes | `n=24 s=30 c=10 k=4 dim_N=18 dim_I=10 N_closed_under_w=True`, `kappa=9`. m=12: subsets 1532779/785460/385917 (sum 2704156), deficient 0/0/0. m=11: deficient 346/184/95. Match |
| 3 witnesses | yes | `symplectic_weight=13 orthogonal_to_all_rows_of_S=True in_span_S=False`. GF(9)-dimension 1, codeword `1 0 0 0 0 0 0 0 0 0 5 8 0 3 1 0 1 6 8 7 2 8 7 4`, `weight=13 in_N=True ... in_isotropic_part=False`. Match. My own code confirms both witnesses |
| 4 GF(3) subset test | yes | `n=24 s=30 c=10 k=4 dim_isotropic=10 dim_dual=18`. W=12: examined 901386/901385/901385, 0 outside I. W=13: examined 832048 x3, 208/218/199 outside I. Match |
| 5 Brouwer-Zimmermann | yes | `K=9 n=24 d=13 sets=9,9,6 maxw=5 words=1758843` with the same witness word. Match |
| 6 no-search proof | yes | `RESULT: d_EA = 13 exactly (no distance search): True`. Match |
| 7 full enumeration | yes | `rank(SJS^T)=20 c=10 k=4 dimN=18 dimI=10`, 387420488 vectors enumerated, histogram identical to mine, `weight 13: in isotropic part 0, outside 5000`, `d_EA = 13`. Match. Its witness also checks out with my code |
| 8 live table | no | Not my role, and no network was used. The saved copy table/row_24_4.txt lists `[[24,4,12-19;10]]`, so 12 < 13 <= 19 against that copy. Whether this copy matches the live page is for the other skeptics |

The counts are consistent across methods. 625 zero sets times 8 nonzero GF(9) scalars gives 5000 weight-13 vectors,
which is what both enumerations report.

## Limits and notes

- No network, no installs, no outward actions. No block, permission denial or HTTP error occurred.
- The heavy-job count was 0 or 1 before each run. Every compiled binary was named so the machine-wide count could
  see it. No background jobs were started.
- I judged only reproduction and correctness of the parameters. Novelty and the live table belong to the other
  skeptics.

pass: true
