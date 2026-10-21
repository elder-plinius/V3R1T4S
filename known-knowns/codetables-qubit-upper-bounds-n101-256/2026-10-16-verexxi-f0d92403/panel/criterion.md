context: subagent (Claude Code headless on the owner's PC, fresh context)
confirmed_scope: Within the exact quantum weight-enumerator LP with shadow constraints (A_0=1, sum A=2^(n-k), A_j=B_j for 1<=j<d, A_j<=B_j for j>=d, shadow>=0), the integer Farkas certificates in result/ verify (checked by check/check_cert.py) that no [[177,1,58]] and no [[177,1,59]] qubit stabilizer code exists, so the upper bound at (177,1) drops from the table value 59 (snapshot in data/) to at most 57, and propagation closure of the saved table at (177,1) is 59, so this is not implied by neighbouring cells in that snapshot.

## Reasoning
Criterion: for a qubit cell with 101<=n<=256, an exact Farkas certificate of the weight-enumerator LP (with shadow where used) for d = live upper bound, checked in exact integers by an independent script, lowering the bound by >=1, and not implied by propagation.

Commands run (inside the claim folder):
- `python3 -I check/check_cert.py result/cert_177_1_58_sh.json` -> `VERIFIED [[177,1,58]] shadow=True: value=1884 digits, max column coefficient <= 0, 57+2+58 multipliers`, rc=0
- `python3 -I check/check_cert.py result/cert_177_1_59_sh.json` -> `VERIFIED [[177,1,59]] shadow=True: value=2197 digits ...`, rc=0
- I read check/check_cert.py in full: standard library only, integer arithmetic, correct Krawtchouk K_j(i), correct Farkas rule (all column coefficients <= 0, positive value, inequality multipliers nonnegative, index ranges enforced). The LP rows are the standard CRSS/Rains constraints.
- Mutation null tests on the checker: changing d to 57 -> `False, u_Q index outside 1..d-1`; dropping the shadow multipliers v_H -> `False, column 60 has positive combined coefficient` (so the shadow constraints are genuinely needed, not decorative); perturbing u_E0 by 10^3000 -> rejected. The checker is not a rubber stamp.
- Hidden-quantifier check: the criterion asks d equal to the live upper bound (59): the 59 certificate verifies, matching the literal reading. The 58 certificate is sound for the stronger claim: any [[177,1,59]] code also satisfies the d=58 LP rows (A_58=B_58 implies A_58<=B_58), so infeasibility at d=58 rules out all d>=58, giving upper bound <= 57. The claim wording (57) is consistent with this.
- Table: data/QECC_q4_n177_k1_claimtime.html contains "Bounds on [[177,1]]"; CLAIM.md records lower 35, upper 59. I cannot re-fetch live (not permitted); "live immediately before claiming" is taken from the recorded fetch (2026-10-16T21:01:30Z, HTTP 200) with hash, which I cannot independently confirm for freshness.
- Propagation: parse_table.py + propagate.py on data/qubit_table_full_n1-256.html -> table (177,1)=[35,59], closure 59. Neighbours: (178,1)=[35,60], (176,2)=[34,59], (177,2)=[34,59], (176,1)=[35,59], (179,1)=[35,61]. R2 gives <=60, R3 gives <=60 (59+1), so 57 is not implied by other cells. Note: the script reports 1075 table cells above their implied closure, showing the table is loose elsewhere, but not at (177,1).

## Residual caveats (do not change the verdict)
- The "independent script" is written by the claimant, though it is separate from any LP solver and simple enough that I audited it; the LP formulation itself (shadow form, impure codes allowed via A<=B) is standard.
- Freshness of the table at claim time is unverifiable from the folder alone.
- Not peer reviewed; scope is stabilizer (additive) qubit codes only.

pass: true
