context: subagent (Claude Code headless on the owner's PC, fresh context)
confirmed_scope: No qubit stabilizer code [[213,2,71]] exists (certified by an exact integer Farkas certificate of the weight-enumerator LP with Rains shadow constraints), so the upper bound for the qubit cell [[213,2]] is at most 70 against a claim-time table upper bound of 71, and this value is not implied by the table's other cells under the rules R1, R2 and R3.

## What I ran (real output)
- `python3 -I check/check_cert.py result/cert_213_2_71_sh.json` printed: `VERIFIED [[213,2,71]] shadow=True: value=2622 digits, max column coefficient <= 0, 70+2+71 multipliers`, exit code 0.
- `python3 -I check/parse_table.py data/qubit_table_full_n1-256.html parsed.json` and `python3 -I check/propagate.py parsed.json closure.json`. Result: live (213,2) = [41, 71]; closure at (213,2) = 71. The neighbouring live cells are (213,1) = [42,71] (R1 gives 71), (214,2) = [42,72] (R2 gives 72) and (212,3) = [41,71] (R3 gives 72). So no propagation rule yields 70.
- sha256sum of data/QECC_q4_n213_k2_claimtime.html and data/qubit_table_full_n1-256.html matched the hashes stated in CLAIM.md. The saved page for the cell reads "Bounds on [[213,2]]" with upper bound 71.

## Reasoning
- I read the checker source. It uses integers only. The Farkas logic is sound: the combination of rows equals sum_i c_i A_i, the sum of the equality rows contributes u_E0 + u_E1*2^(n-k) (value), and G and H are nonnegative. With every c_i <= 0 and value > 0, the system is infeasible over A >= 0. It enforces index ranges (Q only for j<d, G only for j>=d), nonnegative multipliers on inequalities, and that shadow multipliers are only allowed when the shadow flag is set.
- The LP rows (A_0=1, sum A = 2^(n-k), A_j=B_j for j<d, A_j<=B_j for j>=d, Sh_j>=0) are the standard valid constraints for any additive code with distance at least d. They therefore rule out every d >= 71 code, not only exactly 71, so the upper bound drops to 70.
- Hidden quantifiers: the criterion needs some cell with 101<=n<=256 (213 qualifies), d equal to the live upper bound (71 equals 71), a drop of at least 1, an exact certificate checked independently, and non-subsumption. All five hold. Caveats: this is one cell, and the saved page is a snapshot; I could not re-fetch it live and was told not to. The independence of the checker rests on its being a separate small script, and I read it myself.
- Null model and subsumption: the propagation check uses the full saved table with all three rules, and the closure stays at 71.

pass: true
