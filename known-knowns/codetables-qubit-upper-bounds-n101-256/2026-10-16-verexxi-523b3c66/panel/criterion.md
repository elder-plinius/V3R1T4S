context: subagent (Claude Code headless on the owner's PC, fresh context)
confirmed_scope: Two exact-integer Farkas certificates for the quantum weight-enumerator LP with Rains shadow constraints (cert_142_2_48_sh.json for d=48, cert_142_2_47_sh.json for d=47) verify in check/check_cert.py, so no qubit stabilizer code [[142,2,47]] (hence none with d>=47, including the snapshot upper bound 48) exists, lowering the upper bound of cell (142,2) from the table value 48 (record in data/QECC_q4_n142_k2_claimtime.html) to at most 46, and propagation over the saved full table gives closure 48 at (142,2), so the bound is not implied by other cells in that saved snapshot; I did not re-fetch the live table.

## Reasoning
Criterion needs: (a) cell 101<=n<=256 (142,2 ok); (b) proof for d = live upper bound (48) lowering by >=1; (c) exact Farkas certificate of the LP with MacWilliams, A_i<=B_i, A_i=B_i for 0<i<d, nonnegativity, shadow nonnegativity; (d) checked in exact integer arithmetic by a separate script; (e) not implied by propagation.

(a,b) data/QECC_q4_n142_k2_claimtime.html states upper bound 48. cert_142_2_48_sh.json has d=48 = the literal live bound, so the literal reading is met (bound becomes <=47). The d=47 certificate gives <=46. The d=47 result follows the same LP rows with d=47; since a d=47 nonexistence rules out d=48 too, no hidden quantifier gap.

(c,d) Command: python3 -I check/check_cert.py result/cert_142_2_48_sh.json and the 47 one. Output:
  VERIFIED [[142,2,48]] shadow=True: value=1087 digits, max column coefficient <= 0, 47+2+45 multipliers
  VERIFIED [[142,2,47]] shadow=True: value=1040 digits, max column coefficient <= 0, 46+2+47 multipliers
I read the checker: standard library, Python big integers, no floats; it enforces multiplier index ranges and sign of inequality multipliers, positive value, and every column coefficient <= 0. The LP rows are the standard valid constraints (A_j=B_j for j<d holds for any stabilizer code including degenerate; shadow >= 0 is Rains' theorem). Null/tamper models I ran: changing d to 46 -> "FAILED ... u_Q index outside 1..d-1"; removing the shadow multipliers (v_H) -> "FAILED ... column 49 has positive combined coefficient". So the checker is not vacuous and the shadow constraints are essential to the result (consistent with the claim naming "_sh").

(e) Command: parse_table.py then propagate.py on data/qubit_table_full_n1-256.html, then print: "[30, 48] 48". Neighbours (from check/propagation_check.txt): R1 (142,1) -> 48, R2 (143,2) -> 49, R3 (141,3)+1 -> 48. So the implied bound is 48, and 46 or 47 is not implied. The table is visibly not propagation-closed elsewhere (1075 cells above closure), but not at this cell.

## Residual caveats
- The checker is by the same author as the certificate (independence is of script, not of person); I did not run an external LP solver.
- I could not re-fetch the live table (no web access allowed); freshness rests on the saved record timestamps (2026-10-16T21:00:27Z).
- No claim beyond cell (142,2); the LP and shadow rule are from the cited published sources and are not new theory.

pass: true
