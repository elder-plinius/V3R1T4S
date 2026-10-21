# Criterion skeptic verdict: [[115,4]]

context: subagent (Claude Code headless on the owner's PC, fresh context)

## What I did
- Read CLAIM.md, REPRODUCE.md and check/check_cert.py (about 85 lines, standard library, integer arithmetic only).
- Ran `python3 -I check/check_cert.py result/cert_115_4_39_sh.json`. Output: `VERIFIED [[115,4,39]] shadow=True: value=666 digits, max column coefficient <= 0, 37+2+36 multipliers`, exit code 0.
- Ran `python3 -I check/check_cert.py result/cert_115_4_38_sh.json`. Output: `VERIFIED [[115,4,38]] shadow=True: value=666 digits, max column coefficient <= 0, 37+2+36 multipliers`, exit code 0.
- Ran check/parse_table.py and check/propagate.py on data/qubit_table_full_n1-256.html. Results: live (115,4) = [24, 39], closure at (115,4) = 38, neighbours (114,5) = [23, 38], (116,4) = [24, 39], (115,3) = [25, 39]. A bound of 37 is therefore not implied by propagation. The 39 and 38 certificates both pass.
- Checked the saved claim-time page: it states upper bound 39 for [[115,4]].

## Reasoning
- The checker's LP matches the criterion. It includes A_0 = 1, sum A_i = 2^(n-k), MacWilliams rows linking A and B, A_j = B_j for 1 <= j < d, A_j <= B_j for j >= d, A_j >= 0, and Rains shadow nonnegativity.
- The Farkas rule (all column coefficients <= 0 with a positive value) is implemented correctly in exact integers. The multiplier sign constraints and index ranges are enforced.
- Literal reading of the criterion: a proof that d equal to the live upper bound (39) is impossible. cert_115_4_39_sh.json verifies on its own. The stronger d = 38 certificate also verifies, and it excludes d = 39 as well, since a [[115,4,39]] code would give distance >= 38. The new bound of 37 lowers the live bound by 2.
- Hidden quantifiers: the cell is within 101 <= n <= 256, and the proof is a Farkas certificate checked by a separate script. The relabelling used to derive the 39 certificate from the 38 one is legitimate, because the rows have identical coefficients and A_38 = B_38 holds when d = 39.
- Not subsumed: propagation over the full saved live table gives 38, which is strictly above 37, and the live table says 39.
- Limitation: the claim-time table snapshot is taken as given. I could not re-fetch it, and I had no access to do so.

confirmed_scope: Within the saved claim-time codetables.de table (upper bound 39 for [[115,4]]), exact-integer Farkas certificates of the weight-enumerator LP with shadow constraints rule out qubit stabilizer codes [[115,4,38]] and [[115,4,39]], giving an upper bound of at most 37 that is not implied by propagation from the other saved cells (their closure is 38).

pass: true
