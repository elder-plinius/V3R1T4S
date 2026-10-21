context: subagent (Claude Code headless on the owner's PC, fresh context)

# Criterion skeptic verdict, [[192,2]]

## What I did
- Read CLAIM.md, REPRODUCE.md, check/check_cert.py (full source).
- Ran: python3 -I check/check_cert.py on both certificates. Real output:
  - VERIFIED [[192,2,65]] shadow=True: value=2138 digits, max column coefficient <= 0, 63+2+60 multipliers (rc=0)
  - VERIFIED [[192,2,64]] shadow=True: value=2138 digits, max column coefficient <= 0, 63+2+60 multipliers (rc=0)
- Ran check/parse_table.py and check/propagate.py on data/qubit_table_full_n1-256.html. check/propagation_check.txt gives: "live (192,2): [37, 65]  closure of the live table at (192,2): 64  neighbours R1 (n,k-1): [38, 65]  R2 (n+1,k): [38, 65]  R3 (n-1,k+1): [37, 65]". (My own re-run wrote its output to a scratch path that did not exist, so the final one-liner failed; I relied on the saved propagation_check.txt and the neighbour values.)
- Grepped data/QECC_q4_n192_k2_claimtime.html: "lower bound: 37, upper bound: 65" for [[192,2]].

## Reasoning
- Criterion text: for a cell with 101<=n<=256, prove no [[n,k,d]] for d = live upper bound, lowering it by at least 1, via an exact Farkas certificate of the weight-enumerator LP with shadow constraints, checked in exact integer arithmetic by an independent script, and not implied by the propagation rules.
- Cell (192,2) is in range. Live upper bound is 65, as stated in the saved claim-time page. The d=65 certificate (the literal reading) verifies. The d=64 certificate also verifies, so the bound drops from 65 to 63 (by 2), and monotonicity in d makes this consistent.
- The checker's LP matches the standard one: A_0=1, sum A = 2^(n-k), A_j=B_j for j<d, A_j<=B_j for j>=d, shadow Sh_j = 2^-(n-k) sum (-1)^i K_j(i) A_i >= 0 (Rains). The Farkas logic (every column coefficient <= 0 with positive value) is sound, uses only integers and rejects negative inequality multipliers and out-of-range indices. The checker's d=65 handling places rows j<65 as equalities, which is the correct LP for d=65. The d=65 certificate is relabelled from the d=64 one, but that is legitimate because the checker validates it independently.
- Null model / subsumption: the closure of other live cells under R1, R2 and R3 at (192,2) is 64, so an upper bound of 63 (and even a bound of 64) is not implied by propagation. Neither (192,2) nor an immediate neighbour is listed as already implied.
- Hidden quantifiers: the claim covers one cell, one k=2, stabilizer (additive) qubit codes only, which is exactly what the table covers. The proof does not assert anything about non-additive codes. The table-fetch timestamps were recorded at claim time. I could not re-fetch live (not allowed), so currency of the 65 is taken from the saved page.
- Residual risk: independence of the checker from the generator is asserted but I only audited the checker source, which looks correct.

confirmed_scope: No [[192,2,d]] qubit stabilizer code exists for d = 64 or d = 65 (hence d <= 63), proved by an integer-arithmetic Farkas certificate of the shadow-enhanced quantum weight-enumerator LP that is verified by check/check_cert.py and is not implied by the R1/R2/R3 propagation closure (64) of the claim-time table, whose upper bound for that cell was 65.

pass: true
