context: subagent (Claude Code headless on the owner's PC, fresh context)
confirmed_scope: The two integer Farkas certificates in result/ (shadow-enhanced quaternary-MacWilliams LP, n=133, k=2, d=44 and d=45) are valid, so no [[133,2,d]] qubit stabilizer code exists for d >= 44, which lowers the claim-time snapshot upper bound of 45 (data/QECC_q4_n133_k2_claimtime.html) to at most 43 and is not implied by the R1/R2/R3 propagation closure of the full table snapshot (data/qubit_table_full_n1-256.html).

## Reasoning

Criterion read literally: some qubit cell with 101<=n<=256 (133 qualifies), proof that no [[n,k,d]] exists at d = live upper bound (45; cert_133_2_45_sh.json does exactly this), lowering by >=1, exact Farkas certificate of the weight-enumerator LP (MacWilliams, A_i<=B_i, A_i=B_i for 0<i<d, nonnegativity, shadow), independent integer checker, and not implied by propagation. This is the full criterion, not a partial win. The d=44 certificate (bound to 43, a drop of 2) is a bonus: a d=45 code would have distance >=44, so the LP at d=44 is a valid consequence.

Hidden-quantifier hunt:
- d=44 certificate uses A_j=B_j for j<44 (distance >= 44), correct for any code of distance >= 44, pure or impure. No purity assumption.
- Shadow nonnegativity (Rains) is valid for all additive/stabilizer codes, including k>0. The checker's S_j = 2^-(n-k) sum (-1)^i K_j(i) A_i matches the stated formula.
- Multiplier sign constraints enforced (inequality multipliers >= 0, equality multipliers free, index ranges checked).
- Stabilizer codes only; the claim says "stabilizer" explicitly, and the table is for stabilizer-derived qubit bounds. Not stretched to general nonadditive codes.

Commands run (in claim folder):
$ python -I check/check_cert.py result/cert_133_2_45_sh.json
VERIFIED [[133,2,45]] shadow=True: value=934 digits, max column coefficient <= 0, 44+2+44 multipliers
$ python -I check/check_cert.py result/cert_133_2_44_sh.json
VERIFIED [[133,2,44]] shadow=True: value=899 digits, max column coefficient <= 0, 43+2+42 multipliers

Independent re-check: I wrote my own verifier (Krawtchouk via generating function coefficient of (1+3x)^(n-i)(1-x)^i, not the explicit sum used by the shipped checker) and recomputed every column coefficient from the certificate JSON:
result/cert_133_2_44_sh.json 133 2 44 positive columns 0 rhs>0 True
result/cert_133_2_45_sh.json 133 2 45 positive columns 0 rhs>0 True
Both agree with the shipped checker; the checker's docstring Farkas argument is sound (value = sum c_i A_i - sum v*G(A) - sum v*H(A) <= 0 contradicts value > 0).

Null model / propagation: re-ran check/parse_table.py and check/propagate.py on the saved full table:
cells 33152 ... live > implied: 1075 ...
[26, 45] 45   (live bounds at (133,2), closure at (133,2))
Neighbours in the saved table: (133,1) 45, (132,2) 45, (134,2) 45, (132,3) 45, (133,3) 45. R1 gives 45, R2 gives 45, R3 gives 46; nothing yields <=43. So 43 is not implied by other live cells. The claim-time cell record states "upper bound: 45" (QECC_q4_n133_k2_claimtime.html, fetched 2026-10-16T21:00:07Z per CLAIM.md).

Caveats (not disqualifying): I cannot re-fetch the live table (instructed not to); freshness rests on the saved claim-time record. The size of the improvement (45 -> 43) shows the table's bound here is simply weaker than the shadow LP, which is plausible but means a reviewer should confirm the live cell is still 45 at publication time. Certificates are huge (900+ digit values) but exactly checked, so size is irrelevant to validity.

pass: true
