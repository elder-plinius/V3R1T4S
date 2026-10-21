context: subagent (Claude Code headless on the owner's PC, fresh context)

# Criterion skeptic verdict, [[173,2]]

## What I ran (inside the claim folder, Python standard library)
- python3 -I check/check_cert.py result/cert_173_2_59_sh.json
  -> VERIFIED [[173,2,59]] shadow=True: value=1415 digits, max column coefficient <= 0, 56+2+56 multipliers (exit 0)
- python3 -I check/check_cert.py result/cert_173_2_57_sh.json
  -> VERIFIED [[173,2,57]] shadow=True: value=1415 digits, max column coefficient <= 0, 56+2+56 multipliers (exit 0)
- python3 -I check/parse_table.py data/qubit_table_full_n1-256.html parsed.json, then check/propagate.py parsed.json closure.json
  -> cells 33152, n-range 1..256; entry for (173,2) = [34, 59]; propagation closure at (173,2) = 58
  -> neighbours: R1 (173,1) [34,59]; R2 (174,2) [34,59]; R3 (172,3) [33,58] so R3 gives 58+1 = 59 at best, closure 58.
- grep of data/QECC_q4_n173_k2_claimtime.html: "lower bound 34", "upper bound 59" (matches the table record in CLAIM.md).
- I read check/check_cert.py in full: the LP rows (A_0=1, sum A = 2^(n-k), A_j=B_j for 1<=j<d, A_j<=B_j for j>=d, shadow >= 0) are the standard CRSS plus Rains shadow constraints; the Farkas rule (all column coefficients <= 0, positive value) is stated and implemented in exact integers with sign checks on multipliers (equalities free, inequalities nonnegative) and index-range checks.

## Reasoning
- Criterion: for some qubit cell with 101<=n<=256, an exact Farkas certificate of the weight-enumerator LP (with shadow allowed) that no [[n,k,d]] exists for d = live upper bound, independently checked in exact arithmetic, and the new bound not implied by propagation of other live cells.
- Literal reading (d = live upper bound 59): result/cert_173_2_59_sh.json verifies. Its derivation (relabelling G_j to Q_j for 57<=j<59, same multipliers) is sound, since an equality row implies the corresponding inequality, and the checker verifies it on its own.
- The stronger claim (upper bound 56) follows from the d=57 certificate: any code of distance >= 57 satisfies the d=57 LP rows (A_j=B_j for j<57, A_j<=B_j for j>=57, shadow), so nonexistence of the d=57 LP solution excludes d = 57, 58, 59. The upper bound therefore drops from 59 to 56, a reduction of 3 (criterion needs at least 1). No hidden quantifier: the claim concerns one cell, with a single verified certificate; no stretched definition (shadow is explicitly allowed by the criterion).
- Null model / subsumption: the closure of all live cells under the three stated rules at (173,2) is 58, so 56 (and even 58) is not implied by neighbours; the win is not subsumed. Also, the 1072 other cells listed as live > implied for n>100 show the table is not propagation-closed, which does not weaken this cell: its closure value 58 is still strictly above 56.
- Residual caveats: I did not re-fetch the live table (not permitted), so freshness rests on the saved claim-time page; the checker is by the same author as the certificate, though it is short, standard-library only, and I read it. The Krawtchouk/shadow conventions match the cited literature and the docstring.

confirmed_scope: For the qubit cell [[173,2]], the saved claim-time codetables.de upper bound 59 is lowered to at most 56, because the exact integer Farkas certificates result/cert_173_2_57_sh.json (and result/cert_173_2_59_sh.json for the literal d=59) of the quantum weight-enumerator LP with Rains shadow constraints verify under check/check_cert.py, and the propagation closure of the saved full table at (173,2) is 58, so the bound is not implied by other cells.

pass: true
