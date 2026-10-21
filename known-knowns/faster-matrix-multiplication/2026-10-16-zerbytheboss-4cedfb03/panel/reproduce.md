# REPRODUCE skeptic

context: subagent (fresh context; saw only this package and kit docs, no author notes)

verdict: PASS

## Method
Wrote an independent checker from the definition, before running or reading the author's checkers. Definition used: a rank-m bilinear algorithm for <3,4,4> is m triples (U_r, V_r, W_r) with sum_r U_r[a] V_r[b] W_r[c] = 1 if (a,b,c) = (A[i][j], B[j][k], C-index of (i,k)), else 0 (Brent equations), exact over Z. Perminov layout: A is 3x4 (a = i*4+j), B is 4x4 (b = j*4+k); fresh variables are appended after the inputs (U: 12+k, V: 16+k, W: 38+k); W rows give the 12 outputs.

## Results (object/3x4x4_m38_cr124_ZT_reduced.json)
- Rank: 38 products. All 38 (U_r,V_r) pairs are distinct and nonzero; no unused fresh variables in U, V or W.
- Expansion of all straight-line programs to dense integer vectors: every expanded coefficient is in {-1, 0, 1} (ternary over Z).
- Brent equations: 12*16*12 = 2304 equations, 0 violated, in the output convention c = (k,i) (the package's convention, i.e. W indexes C transposed; this is a relabelling of outputs, not a different algorithm). Under row-major C indexing 80 of 2304 fail, so the convention matters and must be read as stated in the checker docstring; it is the cyclic Perminov/trilinear form.
- 200 random integer 3x4 by 4x4 products evaluated through the program: all 12 outputs equal A*B exactly (with C^T output order).
- Mutation test: 30 random +1 changes to a W coefficient, each caught by the Brent check (30/30). The author's own negative controls also reject.
- Addition count (own rule: each fresh or output form with t terms costs t-1): U 32 + V 36 + W 56 = 124. Matches the declared complexity.reduced = 124 (naive 240).
- Package SHA256SUMS verify OK; `sh verify-it-yourself/run_checks.sh` prints ALL CHECKS PASS (BRENT_OK brent_bad=0). Deterministic (no randomness in the claim; my random tests are only extra).

## Not checked here (other skeptics' jobs)
Whether 125 is the live record, novelty, and the criterion wording. Optimality is not claimed or tested. The count 124 is for this program's straight-line form with the stated counting rule; I did not verify Perminov's counting convention against his tool, only that it equals the plain t-1 per form rule.

## Mismatches
None.

pass: true
