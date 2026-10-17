context: subagent (Claude Code headless on the owner's PC, fresh context)

# Criterion skeptic verdict for [[128,5]]

## What I did (real output)
- Read CLAIM.md, REPRODUCE.md, check/check_cert.py (full source), check/propagate.py.
- Ran `python3 -I check/check_cert.py result/cert_128_5_43_sh.json`:
  `VERIFIED [[128,5,43]] shadow=True: value=782 digits, max column coefficient <= 0, 41+2+41 multipliers` (rc=0)
- Ran `python3 -I check/check_cert.py result/cert_128_5_42_sh.json`:
  `VERIFIED [[128,5,42]] shadow=True: value=782 digits, max column coefficient <= 0, 41+2+41 multipliers` (rc=0)
- Ran parse_table.py and propagate.py on data/qubit_table_full_n1-256.html. Output: `cells k>=1: 32896  live > implied: 1075  of which n>100: 1072  n<=100: 3`. check/propagation_check.txt states: `live (128,5): [24, 43]  closure of the live table at (128,5): 42  neighbours R1 (n,k-1): [25, 43]  R2 (n+1,k): [24, 43]  R3 (n-1,k+1): [24, 42]`. My second command that printed the closure from a temp file failed on a path problem in my own scratch step. The provided propagation_check.txt supplies the closure value, and the propagate.py source matches it.
- Grepped data/QECC_q4_n128_k5_claimtime.html: lower bound 24, upper bound 43 (matches the claim).

## Reasoning
- The checker is short and exact (integer arithmetic only). It tests c_i <= 0 for every column and a positive value. I read the Farkas rule and the LP rows (A_0=1, sum A = 2^(n-k), A_j=B_j below d, A_j<=B_j from d, shadow >= 0). They are the standard Calderbank-Rains-Shor-Sloane and Rains constraints, correctly signed. The index-range guards are sound.
- Hidden quantifier: the criterion says the proof is for d equal to the live upper bound (43). Taken literally, the 43 certificate only gives bound <= 42, and that is already implied by propagation (closure 42), so it would be subsumed. The 42 certificate proves nonexistence of [[128,5,42]]. Any [[128,5,43]] code would give a [[128,5,42]] code, so this also excludes 43 and so covers the literal case. It lowers the bound from 43 to 41, a drop of 2, and 41 is below the propagation closure of 42. So the win is not subsumed. The 43 certificate alone would not be a win, and the claim correctly rests on the 42 one.
- Null model: the propagation rules R1, R2, R3 are valid for k>=1 and are the ones the criterion names. The closure at (128,5) is 42, so 41 is not implied. The live table is known to be non-monotone in many cells (1075 above closure), so the table 43 is just a loose entry, which does not hurt the claim.
- Caveat: the live table was not re-fetched by me (no access allowed). I rely on the claim-time page, which is saved and consistent.

confirmed_scope: The exact Farkas certificate in result/cert_128_5_42_sh.json, verified in integer arithmetic by check/check_cert.py, proves that no [[128,5,42]] qubit stabilizer code (hence no [[128,5,43]]) exists, so the upper bound for [[128,5]] drops from the claim-time table value 43 to at most 41, below the propagation closure value of 42 from other claim-time cells.

pass: true
