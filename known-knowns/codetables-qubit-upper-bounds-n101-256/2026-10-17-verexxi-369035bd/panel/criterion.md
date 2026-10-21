context: subagent (Claude Code headless on the owner's PC, fresh context)

# Criterion skeptic verdict, [[167,2]]

## What I did and real output
- Read CLAIM.md, REPRODUCE.md and the full source of check/check_cert.py.
- Ran: python3 -I check/check_cert.py result/cert_167_2_57_sh.json
  Output: VERIFIED [[167,2,57]] shadow=True: value=1374 digits, max column coefficient <= 0, 54+2+54 multipliers (exit 0)
- Ran: python3 -I check/check_cert.py result/cert_167_2_55_sh.json
  Output: VERIFIED [[167,2,55]] shadow=True: value=1374 digits, max column coefficient <= 0, 54+2+54 multipliers (exit 0)
- Ran check/parse_table.py then check/propagate.py on data/qubit_table_full_n1-256.html and printed the cell and its closure.
  Output: [33, 57] 56. The neighbours are (166,3) = [32,56], (168,2) = [33,57], (167,1) = [33,57], (167,3) = [32,57].
  check/propagation_check.txt agrees: closure of the live table at (167,2) is 56.
- The saved claim-time page data/QECC_q4_n167_k2_claimtime.html contains "Bounds on [[167,2]]". The claim records upper bound 57 for it. I did not re-fetch it (no web access allowed).

## Reasoning
- The checker is small and uses exact integers only. I read the Farkas rule against its docstring.
  - Each column coefficient is computed as an integer sum and must be <= 0.
  - The value u_E0 + u_E1*2^(n-k) must be > 0.
  - Equality-row multipliers may have any sign, and the inequality multipliers G and H are checked non-negative.
  - Index ranges are enforced (Q for 1..d-1, G for d..n).
- The LP is the standard one:
  - A_0 = 1.
  - The A_i sum to 2^(n-k).
  - A_j = B_j below d, with the MacWilliams transform.
  - A_j <= B_j for j >= d.
  - Rains shadow coefficients >= 0.
  This matches the criterion's list of constraints, with shadow nonnegativity explicitly allowed ("where used").
- Both certificates verify. The d=55 certificate shows no [[167,2,55]] code exists, so d <= 54. That also rules out d = 57, the literal live upper bound. The d=57 certificate is a relabelling of the d=55 one: rows with 55 <= j < 57 move from inequality to equality with the same multipliers. The checker accepts it on its own, which is the literal reading of the criterion.
- The claim does not rely on a hidden quantifier. The criterion asks for a proof for d equal to the live upper bound (57), and this is covered. The stronger statement for d=55 gives the new bound 54 (a drop of 3). It is not a partial win dressed up as a full one.
- Null model and subsumption:
  - The propagation closure of all live cells at (167,2) is 56, computed from the full table with R1, R2 and R3.
  - A bound of 54 (and also the bound of 56 for d=57) is not implied by other live cells.
  - The live 57 sits above its own closure of 56, but the claimed 54 is below the closure, so the claim is not subsumed.
- Residual caveats:
  - I did not independently re-derive the LP theory, but it is the standard Calderbank-Rains-Shor-Sloane plus Rains shadow LP.
  - The table page is a saved fetch, not a live one.
  - I did not check that the table has no uncited non-LP upper bound for this cell. The saved page shows 57.

confirmed_scope: Using exact integer Farkas certificates that check_cert.py verifies, no qubit stabilizer code [[167,2,d]] exists for d >= 55 (including the live table upper bound d = 57 recorded at claim time), so the upper bound for [[167,2]] is at most 54, below the propagation closure of 56 from the saved full table.

pass: true
