context: subagent (Claude Code headless on the owner's PC, fresh context)

# Criterion skeptic verdict for [[180,2]]

## What I did and real output
- Read CLAIM.md, REPRODUCE.md, check/check_cert.py (full source).
- Ran: python3 -I check/check_cert.py result/cert_180_2_61_sh.json
  Output: VERIFIED [[180,2,61]] shadow=True: value=1655 digits, max column coefficient <= 0, 58+2+59 multipliers (exit 0)
- Ran: python3 -I check/check_cert.py result/cert_180_2_59_sh.json
  Output: VERIFIED [[180,2,59]] shadow=True: value=1655 digits, max column coefficient <= 0, 58+2+59 multipliers (exit 0)
- Ran check/parse_table.py then check/propagate.py on data/qubit_table_full_n1-256.html, then printed the cell and its closure.
  Output: [35, 61] 60. Neighbours (179,2), (181,2), (180,1), (180,3), (181,1), (179,3) all show upper bound 61 in the saved table.
  So the closure of live cells at (180,2) is 60. A bound of 58 (or 60) is not implied by R1/R2/R3 from other live cells.

## Reasoning
- The checker is short, integer-only, standard library. It implements: A_0=1, sum A = 2^(n-k), A_j=B_j for 1<=j<d (via MacWilliams rows), A_j<=B_j for j>=d, Rains shadow >= 0, with Krawtchouk K_j(i) computed by the explicit binomial sum. The Farkas rule (all column coefficients <= 0, positive value, equality multipliers free-signed, inequality multipliers nonnegative) is correct, and index-range and sign checks are present. I found no hidden quantifier or loophole in it.
- Literal criterion: a proof of nonexistence at d equal to the live upper bound (61), lowering the bound by at least 1. cert_180_2_61_sh.json is verified on its own and proves no [[180,2,61]] code. The stronger d=59 certificate proves the bound is at most 58. Both are valid. The 61 certificate is a relabelling of the 59 one, which is legitimate because rows G_j and Q_j have identical coefficients. This is a derivation, not a stretched definition.
- Success criterion also requires the new bound not be implied by propagation from other live cells. The closure is 60 and the new bound is 58, so it is not implied (even the weaker bound of 60 would be a lowering, but the claim is 58).
- Null-model concern: the LP bound being tighter than the table's value 61 across a wide n range is plausible, since the table's upper bounds in this region are likely older LP/propagation values without shadow constraints. No contradiction with the lower bound 35 and no sign of a checker-trivial certificate (value has 1655 digits and the checker rejects positive columns).
- Residual caveat: the live page was not re-fetched by me (no web access allowed); I relied on the saved claim-time record dated 2026-10-17 and the parsed full table.

confirmed_scope: For the qubit cell (n,k)=(180,2), the saved codetables.de record (upper bound 61, lower bound 35) is lowered, with exact integer-checked Farkas certificates of the weight-enumerator LP with Rains shadow constraints, to the statement that no [[180,2,d]] stabilizer code exists for d=59 (hence an upper bound of at most 58, and in particular none for the live bound d=61), and this bound is not implied by the standard propagation closure of the other saved table cells, which gives 60.

pass: true
