context: subagent (Claude Code headless on the owner's PC, fresh context)

# REPRODUCE verdict for [[185,3,61]] (claim: upper bound at most 60, live 63)

## Own checker, written before running or reading the author's code
Definition used (quoted from REPRODUCE.md, step 2): variables A_0..A_n >= 0, stabilizer weight distribution of an [[n,k,d]] code; B_j = 2^-(n-k) sum_i K_j(i) A_i; Sh_j = 2^-(n-k) sum_i (-1)^i K_j(i) A_i; K_j(i) = sum_s (-1)^s 3^(j-s) C(i,s) C(n-i,j-s). Constraints: A_0 = 1, sum A_i = 2^(n-k), A_j = B_j for 1<=j<d, A_j <= B_j for j>=d, Sh_j >= 0 (Rains shadow). Farkas: a combination with integer multipliers (free on equalities, nonnegative on inequalities) whose every column coefficient is <= 0 while the constant is > 0 is infeasible for A >= 0.

I only looked at the certificate JSON keys (u_E0, u_E1, u_Q, v_G, v_H), then wrote an independent script (my own K_j via Python big integers, rows scaled by 2^(n-k) = 2^182) that:
- asserts v_G, v_H >= 0, Q indices in 1..d-1, G indices in d..n, H indices in 0..n;
- computes, for every i in 0..185, the exact column coefficient u_E1 + [i=0] u_E0 + sum u_Q (K_j(i) - 2^182 [i=j]) + sum v_G (K_j(i) - 2^182 [i=j]) + sum v_H (-1)^i K_j(i);
- asserts every coefficient <= 0 and u_E0 + u_E1 * 2^182 > 0.

Real output:
- cert_185_3_61_sh.json: `OK d=61 all 186 column coeffs <=0 (max 0...), rhs>0 (bits 5631)`
- cert_185_3_63_sh.json: `OK d=63 all 186 column coeffs <=0 (max 0...), rhs>0 (bits 5631)`
Negative control: perturbing u_E1 by +1 gives `AssertionError: (0, 'coef positive')` (my checker rejects a broken certificate).
Note: relabelling d to 62 also passes, which is consistent because the certificate has no multipliers on rows 61 and 62 (u_Q covers 1..60, v_G covers 63..64), so the d=63 version is a genuine certificate (and a d=61 one implies the d=62 and d=63 ones by the stated monotonicity of the LP rows).

## Author's checker
`python3 -I check/check_cert.py result/cert_185_3_63_sh.json` and `.../cert_185_3_61_sh.json`:
`VERIFIED [[185,3,63]] shadow=True: value=1695 digits, max column coefficient <= 0, 60+2+59 multipliers` and the same for [[185,3,61]], exit code 0 both. Output matches check/checker_output.txt (modulo line endings).

## Table / propagation
- data/QECC_q4_n185_k3_claimtime.html sha256 b63791604a45d3cf7bd4ada4ab322fdf8888038bb1b4eaaabaa258bf551694e2 and data/qubit_table_full_n1-256.html sha256 26245491ba119789eb338424ade4e6b5a74dd46e12df7cec47dd79845de4b0b6 both match the claim. Saved page text: "Bounds on [[185,3]] ... lower bound: 36 upper bound: 63".
- Re-ran check/parse_table.py and check/propagate.py: cells 33152; (185,3) = [36, 63], closure 61.
- My own independent fixpoint (R1 d(n,k)<=d(n,k-1) for k>=2, R2 d(n,k)<=d(n+1,k), R3 d(n,k)<=d(n-1,k+1)+1, applied to all k>=1 upper bounds of the parsed table) also gives 61 for (185,3). So 60 is not implied by other live cells; neighbours give 63, 63, 63 directly and 61 only via longer chains, still above 60.
- Deterministic: repeated runs gave identical outputs.

## Reasoning and limits
The LP is the standard quantum weight-enumerator LP with Rains shadow constraints; the exact integer Farkas combination checks out in two independent implementations, so no [[185,3,61]] stabilizer code exists and the upper bound is at most 60 (strictly below the table's 63, and below the 61 implied by propagation). Both d=61 and d=63 (literal live bound) certificates verify. I did not re-fetch the live page (no web access allowed); the claim-time page saved in the folder was used. Soundness relies on the cited published LP/shadow constraints, which I re-derived as stated above.

pass: true
