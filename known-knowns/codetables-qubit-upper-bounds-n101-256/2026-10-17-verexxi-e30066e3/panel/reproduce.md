# REPRODUCE skeptic report, q115-2: no [[115,2,39]] qubit stabilizer code (shadow LP, exact Farkas certificate)
context: subagent (Claude Code on the owner's PC, fresh context, Sonnet)

## Scope and order of work
- I used only the claim package (claim/) and my scratch folder (work/, a sibling of claim/). Python 3.14.4, every script run as `python -I`.
- Order: (1) read CLAIM.md and REPRODUCE.md, looked at the certificate and the data files; (2) wrote my own exact-integer checker (work/my_check.py) from the LP definition, and my own table parser plus propagation closure (work/my_prop.py), WITHOUT opening anything in check/; (3) only then ran and read the shipped scripts and compared.
- Inventory: all 11 files named in CLAIM.md and REPRODUCE.md are present (CLAIM.md, REPRODUCE.md, result/cert_115_2_39_sh.json, check/check_cert.py, check/checker_output.txt, check/parse_table.py, check/propagate.py, check/propagation_check.txt, data/QECC_q4_n115_k2_claimtime.html, data/qubit_table_full_n1-256.html, data/TROPHY_CASE_pinned_9b1d444.md). Listing run at 2026-10-17T05:25:44Z.

## Hashes (sha256sum output)
- result/cert_115_2_39_sh.json: e30066e3f9730417e8b296b85c3274b1343d0df848b862b93b2b8bdf929527d4 (44002 bytes)
- data/QECC_q4_n115_k2_claimtime.html: 29968216baaba12c154cba958db46710334c45fb045b682c07f8705575a9f5c3 (equals the hash stated in CLAIM.md)
- data/qubit_table_full_n1-256.html: 26245491ba119789eb338424ade4e6b5a74dd46e12df7cec47dd79845de4b0b6 (equals the hash stated in CLAIM.md)
- check/check_cert.py: 3c4e89d40124f80751290db7b9190387cdbd6590d4fd48f25ac9c7e996cf3fe4
- check/checker_output.txt: 271097600012319a03bfe83bc08cf0a678415a2389d1465321dacb94e1f31894
- check/parse_table.py: c6240ecb3a0566061273ac3e6ea1e8b84d6eadf42958a91a3f817b559f929be9
- check/propagate.py: 9b488d90445fce3a2f87dbcbcb7b4d0dd6d87ec6c075d33d5ab988b4542dd742
- check/propagation_check.txt: 72da68d63c6b184d0654a092bbfd936f469dd5e6d888f4dd4051b119752bf94d
- data/TROPHY_CASE_pinned_9b1d444.md: cdfe852481ba85e35ccbc386d64ce88de92a56eb73d1ec3e44cdc9a3b86345ad. A grep of it for quantum, QECC, codetables, stabiliz, shadow, farkas and [[ found no row about quantum codes (the only hit for 115 is inside the number 11156 of a constant-weight-code row). So no earlier trophy-case entry exists for this cell. I treated that file as context data only.

## The object
result/cert_115_2_39_sh.json has n=115, k=2, d=39, shadow=true and integer multipliers (decimal strings of about 550 to 600 digits): u_E0 (positive), u_E1 (negative), u_Q for j=1..38 (38 entries, all negative, free sign allowed), v_G for j=41 only (1 entry, positive), v_H for j=1 and 3..37 (36 entries, all positive). So it uses the equalities E0, E1, Q_1..Q_38, one A_j-below-B_j row (j=41) and 36 shadow rows.

## 1. My own checker, written from the definition (before reading check/)
Definition used (REPRODUCE.md and CLAIM.md): columns A_0..A_n (n=115), M = 2^(n-k) = 2^113. B_j = (1/M) sum_i K_j(i) A_i, Sh_j = (1/M) sum_i (-1)^i K_j(i) A_i, K_j(i) = sum_s (-1)^s 3^(j-s) C(i,s) C(n-i,j-s). Constraints: A_0 = 1; sum A_i = M; A_j = B_j for j from 1 up to d-1; A_j at most B_j for j at least d; Sh_j at least 0 for all j. Farkas rule: free-sign multipliers on equalities, nonnegative on inequalities, every column coefficient of the combination at most 0, right-hand side positive.
Command (from claim/): `python -I ../work/my_check.py result/cert_115_2_39_sh.json`, run at 2026-10-17T05:31:35Z (1.3 s).
- Krawtchouk table (116 x 116) computed two ways, the closed binomial sum and the coefficient of z^j in (1+3z)^(n-i) (1-z)^i by repeated polynomial multiplication: identical in every entry. Also K_j(0) = 3^j C(n,j) and sum_j K_j(i) = 4^n for i=0, else 0: hold.
- Certificate structure: u_Q keys are exactly 1..38; the v_G key 41 is at least d=39; all inequality multipliers are nonnegative.
- RESULT with the conventions of the shipped docstring (E0 as A_0 = 1 and E1 as sum A_i = M left unscaled, Q_j as sum_i K_j(i) A_i - M A_j = 0, G_j the same expression at least 0, H_j as sum_i (-1)^i K_j(i) A_i at least 0): 116 of 116 columns have coefficient at most 0 (115 strictly negative, column 0 exactly 0), right-hand side u_E0 + u_E1 * 2^113 is positive with 600 decimal digits. FARKAS VALID.
- Second route (work/my_detail.py): the same combination recomputed on the unscaled rational LP (Fractions, multipliers rescaled by M where the row was scaled): identical column coefficients and right-hand side to the integer route. sha256 of the right-hand side as a decimal string: 0828efb5287f3aaf82e2c59013fa0b179b5dddfa91b4d3cc82a61e4ed0886b85. Largest column coefficient magnitude has 600 digits, smallest nonzero one has 479 digits.
- Convention note (documentation nit, see section 9): my first reading of REPRODUCE.md step 2 ("rows multiplied by 2^(n-k)", applied also to E0 and E1, with Q written as A_j minus B_j) does NOT verify (114 of 116 columns at most 0). The certificate verifies when E0 and E1 are the plain rows and Q is written B_j minus A_j, which is what the docstring of check/check_cert.py states. This changes nothing mathematically: scaling an equality row, or flipping its sign, only rescales its free multiplier, and positive scaling of an inequality row keeps its multiplier nonnegative, so all variants describe the same feasible set. The inequality directions (B_j at least A_j, Sh_j at least 0) were never varied.

## 2. Are my LP rows true for real stabilizer codes? (re-deriving the proof steps)
Command (from claim/): work/val_small.py run through python -I, at 2026-10-17T05:33:09Z (2 s). For each code it enumerates the stabilizer S, the normalizer N (all Paulis commuting with S) and the shadow set {u : symplectic product of u and c equals weight(c) mod 2 for every c in S} directly, then compares with the formulas and tests every row family (E0, E1, Q, G, H) built by the same row function used on the certificate, for every d from 1 up to the true distance.
- 360 random stabilizer codes (n = 2..7, every k from 1 to n; 253 of them have odd-weight stabilizer elements, so the (-1)^i shadow signs are exercised) plus [[5,1,3]] (A = 1,0,0,0,15,0; B = 1,0,0,30,15,18, the known values), [[7,1,3]] (A = 1,0,0,0,21,0,42,0; B = 1,0,0,21,21,126,42,45) and the one-qubit code with stabilizer Z (A = 1,1; B = 1,1; shadow weights 0,2, i.e. the shadow is {X,Y}).
- Every code satisfied: M*B_j equals sum_i K_j(i) A_i exactly, M*Sh_j equals sum_i (-1)^i K_j(i) A_i exactly, A_j at most B_j, all equality rows exact, all inequality rows nonnegative. No violation.
- Hand re-derivation (agrees): sum over weight-j Paulis u of (-1)^(symplectic product of u and c) is K_j(i) for c of weight i (each of the s coordinates of supp(c) inside supp(u) gives -1, each of the j-s coordinates outside gives 3 choices). Hence B_j (MacWilliams) and Sh_j (counting u with product equal to weight(c) mod 2 for all c in S; weight mod 2 is additive on a commuting S) are the stated sums, and Sh_j is a count so it is at least 0. A_j at most B_j because S is inside N; A_j = B_j below the distance by definition of d (degenerate codes included); A_0 = 1 and sum A_i = |S| = 2^(n-k).
- Farkas step, re-derived: for any feasible A at least 0, sum_i c_i A_i = (u_E0*1 + u_E1*M) + sum v_G*G(A) + sum v_H*H(A), because the equality rows cancel exactly. With every c_i at most 0 the left side is at most 0, while the right side is at least the positive value. Contradiction, so the LP is infeasible.
- A certificate for d=39 also excludes every code with distance 39 or more (those satisfy the d=39 rows), so the upper bound on d for [[115,2]] is at most 38.

## 3. Shipped checker (REPRODUCE.md step 1)
Command (from claim/): `python -I check/check_cert.py result/cert_115_2_39_sh.json`, run at 2026-10-17T05:35:50Z, exit code 0, 0.27 s. Output line starts with VERIFIED [[115,2,39]] shadow=True: value=600 digits and ends with 38+1+36 multipliers. sha256 of the whole output: 271097600012319a03bfe83bc08cf0a678415a2389d1465321dacb94e1f31894, identical to check/checker_output.txt (and to a second run). After reading it: its docstring defines exactly the LP above (E0, E1, Q_j, G_j, H_j with the same K_j(i), Rains shadow with (-1)^i), tests every one of the 116 columns, requires the value to be positive and all inequality multipliers nonnegative, and states the same proof. No difference from my checker in the LP, the rule, or the verdict.

## 4. Tamper tests (is either checker vacuous?)
Command (from claim/): `python -I ../work/tamper.py`, 11 cases, both checkers run on each. Both agreed on all 11. Rejected by both: u_E0 plus 1 (column 0 turns positive), one v_H negated, all shadow multipliers dropped (so the certificate really needs the shadow rows), k changed to 3, one u_Q sign flipped, v_G[41] removed, u_E1 plus 1, and the certificate read as d=38 (u_Q[38] dropped). Accepted by both: untouched, u_E0 minus 1 (still valid), and the same multipliers read as d=40 (a weaker statement that must still hold).

## 5. Propagation check (REPRODUCE.md step 3)
Command (from claim/), run at 2026-10-17T05:36:36Z: `python -I check/parse_table.py data/qubit_table_full_n1-256.html ../work/parsed.json`, then `python -I check/propagate.py ../work/parsed.json ../work/closure.json`, then the one-line python print from REPRODUCE.md. Output: cells 33152, n-range 1 256; 32896 cells with k at least 1; 1075 cells whose live upper bound is above their own implied bound (1072 with n above 100, 3 with n at most 100); final line `[25, 39] 39`, exactly the expected output.
My independent parse (by row and column position, cross-checked with each cell's title attribute): 33152 cells, 0 mismatches, lower at most upper in every cell, identical [lower, upper] to the shipped parse on all 33152 cells. My closure (rules R1, R2, R3 as in CLAIM.md, iterated to a fixed point over the whole table) equals the shipped closure on all 32896 cells with k at least 1 (0 differences); (115,2) closes to 39.
Details found:
- Sources for (115,2): R1 from (115,1) = 39; R2 from (116,2) = 39; R3 from (114,3) = 38, plus 1 gives 39. Live k=2 upper bounds for n = 108..122 are 36, 37, 37, 37, 37, 38, 38, 39, 39, 39, 39, 39, 40, 41, 41.
- With the (115,2) entry itself removed (what the OTHER live cells imply for it): 39. With the extra rule d(n,k) at most d(n-1,k)+1 added: 39, and 39 again with the own entry removed. So 38 is not implied by any other live cell.
- Rule R3 is valid for pure codes only; it was applied anyway, which makes the test stricter for the claim, and the result is still 39.
- The live table has anomalies elsewhere (for example (68,16) is listed 27 between neighbours 19 and 18, and 1075 cells sit above their implied bound); they are included in the closure and do not change the value at (115,2).
- Lower-bound side (no live construction contradicts the claim): propagating all live lower bounds with R1, R2 and the aggressive pure-only R3 gives 25 at (115,2), far below 38; no cell of the live table has a propagated lower bound above its live upper bound.

## 6. Live status (REPRODUCE.md step 4)
- `curl -s -o live_q4_n115_k2.html -w ...` on https://codetables.de/QECC.php?q=4&n=115&k=2, started 2026-10-17T05:34:52Z: HTTP 200, 54957 bytes, sha256 29968216baaba12c154cba958db46710334c45fb045b682c07f8705575a9f5c3, byte-identical to data/QECC_q4_n115_k2_claimtime.html. Page text: lower bound 25, upper bound 39.
- `curl` on https://www.codetables.de/QECC/Tables_color.php?q=4&n0=1&n1=256&k0=0&k1=256, started 2026-10-17T05:35:04Z, finished 2026-10-17T05:35:41Z: HTTP 200, 5547032 bytes, sha256 26245491ba119789eb338424ade4e6b5a74dd46e12df7cec47dd79845de4b0b6, `cmp` says byte-identical to data/qubit_table_full_n1-256.html.
So as of about five hours after the claim-time fetch the live upper bound for [[115,2]] is still 39, and the saved data are exactly what the site serves. (The claim-time timestamps in CLAIM.md themselves cannot be re-checked; the identical bytes now are the evidence.)

## 7. Determinism
Second runs, at 2026-10-17T05:38:16Z: my checker output byte-identical to its first run; shipped parse_table.py and propagate.py outputs byte-identical across two runs (parsed.json sha256 1f6b123968ef827e93f9e33c8dbfb87da4e28e2e418b821005857fd0cb16a78b, closure.json sha256 a1310128645030ed4a72f86a8d87570140e392d7655cfe842f922607791b5e3b); my propagation script output byte-identical across two runs; the shipped certificate checker output identical across two runs. No floating point anywhere in the decision (Python integers and Fractions only).

## 8. Reasoning
The decisive object is exact: all 116 columns of the Farkas combination were evaluated in big integers by two separate checkers (mine written from the definition first, then the shipped one) and by two arithmetic routes in mine, with no sampling. The LP those checkers share is the correct relaxation: each row family was re-derived by hand and validated against brute-force enumeration of real stabilizer codes, including codes with odd-weight elements that exercise the shadow signs. The certificate is not vacuous (tamper tests) and genuinely depends on the shadow rows and on the single G_41 row. The conclusion that no [[115,2,39]] stabilizer code exists, hence the upper bound for [[115,2]] is at most 38, follows. The table cell was still 39 live when I fetched it, and the new value 38 is not implied by R1 to R3 (or by the extra rule) applied to all other live cells, nor contradicted by any live lower bound.

## 9. Caveats (none changes the verdict)
- Documentation nit: REPRODUCE.md step 2 says the certificate's rows are "the LP rows multiplied by 2^(n-k)". That is only true for the rows that contain the 1/M factors (Q, G, H); E0 and E1 are used unscaled and Q is oriented as B_j minus A_j, exactly as the docstring of check/check_cert.py says. A reader following the prose literally (as I first did) will not reproduce the verification until they use the docstring conventions. Mathematically immaterial (see section 1).
- I did not search the literature beyond the live table; the success criterion in CLAIM.md is the live-table comparison, and that is what I checked.
- About 30 tool calls were used.

pass: true
