context: subagent (Claude Code headless on the owner's PC, fresh context)
confirmed_scope: For the qubit cell [[165,2]] (table record fetched 2026-10-16T21:01:09Z showing upper bound 55), the exact integer Farkas certificates in result/cert_165_2_55_sh.json and result/cert_165_2_54_sh.json (LP with MacWilliams link, A_j=B_j for 1<=j<d, A_j<=B_j, nonnegativity, shadow nonnegativity) verify and exclude every qubit stabilizer code [[165,2,d]] with d>=54, lowering the table upper bound from 55 to at most 53, and this value is not implied by the propagation rules applied to the saved table (closure at (165,2) is 55).

## Reasoning

Criterion read literally: (a) cell 101<=n<=256, qubit: (165,2) ok. (b) proof of nonexistence at d = live upper bound (55): cert_165_2_55_sh.json does exactly that; the 54 certificate is strictly stronger (a code with d>=55 also satisfies the d=54 constraint set), so no stretched definition: lowering by 2 is a superset of "at least 1". (c) exact rational (integer) Farkas dual, independent script: check/check_cert.py is standard-library integer only. (d) not implied by propagation.

Commands run (in claim folder):
- python3 -I check/check_cert.py result/cert_165_2_55_sh.json -> VERIFIED [[165,2,55]] shadow=True: value=1432 digits, max column coefficient <= 0, 54+2+55 multipliers (exit 0)
- python3 -I check/check_cert.py result/cert_165_2_54_sh.json -> VERIFIED [[165,2,54]] shadow=True: value=1569 digits, max column coefficient <= 0, 53+2+54 multipliers (exit 0)
- Read the checker: it rejects negative inequality multipliers, requires u_Q indices in 1..d-1 and v_G in d..n, requires positive value, and tests every column coefficient <= 0 in exact integers. No floats.
- Null/sanity model of the LP formulas: using check_cert.kraw, I computed B_j and shadow_j for known codes. [[5,1,3]] with A=(1,0,0,0,15,0) gave B=Sh=[1,0,0,30,15,18] (sum 64, B_1=B_2=0, all nonnegative). Steane [[7,1,3]] with A4=21,A6=42 gave B=Sh=[1,0,0,21,21,126,42,45] (sum 256). So the Krawtchouk/MacWilliams/shadow definitions are correct and real codes are feasible, i.e. the LP does not wrongly exclude real codes.
- sha256 of data/QECC_q4_n165_k2_claimtime.html and data/qubit_table_full_n1-256.html match CLAIM.md exactly (c38c91cf..., 26245491...). The cell page text is "Bounds on [[165,2]]"; the parsed full table gives [32, 55] for (165,2).
- python3 -I check/parse_table.py then check/propagate.py on the full table: (165,2) parsed [32,55], closure 55. Neighbours: R1 (165,1)=[33,55], R2 (166,2)=[32,56], R3 (164,3)=[32,55]. No neighbour has upper bound <= 54, so 53/54 is not implied by propagation (consistent with check/propagation_check.txt).

Hidden-quantifier checks: infeasibility at d=54 covers all d>=54 because any code with distance >=54 satisfies A_j=B_j for j<54 and A_j<=B_j for j>=54 plus shadow; so "upper bound <= 53" is justified for stabilizer codes, which is what the table covers. Pure/impure both covered by A_j<=B_j for j>=d. Claim does not assert anything for nonadditive codes.

Caveats: I could not and did not re-fetch the live page (instructed not to open websites), so "live immediately before claiming" rests on the saved record with hash and timestamp. Observation, not a defect: lowering (165,2) also implies (164,2) <= 53 by rule R2, which is a downstream consequence and is not what the claim asserts.

pass: true
