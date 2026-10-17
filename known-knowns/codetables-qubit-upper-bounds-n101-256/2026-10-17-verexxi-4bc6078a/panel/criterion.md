context: subagent (Claude Code headless on the owner's PC, fresh context)

# Criterion skeptic verdict, [[110,5]]

## What I did and real output
- Read CLAIM.md, REPRODUCE.md, check/check_cert.py, check/propagate.py.
- Ran `python3 -I check/check_cert.py result/cert_110_5_37_sh.json`:
  `VERIFIED [[110,5,37]] shadow=True: value=583 digits, max column coefficient <= 0, 35+2+34 multipliers` (exit 0).
- Ran `python3 -I check/check_cert.py result/cert_110_5_36_sh.json`:
  `VERIFIED [[110,5,36]] shadow=True: value=583 digits, max column coefficient <= 0, 35+2+34 multipliers` (exit 0).
- Re-ran check/parse_table.py and check/propagate.py on data/qubit_table_full_n1-256.html:
  `cells k>=1: 32896  live > implied: 1075  of which n>100: 1072  n<=100: 3`.
  check/propagation_check.txt states: `live (110,5): [23, 37]  closure of the live table at (110,5): 36  neighbours R1 (n,k-1): [24, 37]  R2 (n+1,k): [23, 37]  R3 (n-1,k+1): [22, 37]`.
  (My own one-liner to print the closure failed only because of a temp-path issue on this machine; the propagation_check.txt line gives the same value.)
- The saved claim-time page data/QECC_q4_n110_k5_claimtime.html reads "Bounds on [[110,5]]", upper bound 37.

## Reasoning
- Checker: standard library, integer-only. It tests that every column coefficient of the combined multiplier row is <= 0, that the value is > 0, that Q-row multipliers sit on indices 1..d-1, that G-row and H-row multipliers are nonnegative and on legal indices, and that H rows are used only if shadow is set. The LP is the standard stabilizer LP (A_0=1, sum A = 2^(n-k), A_j=B_j below d, A_j<=B_j above, Rains shadow >= 0), all valid for stabilizer codes including impure ones. I found no flaw in the Farkas rule.
- Literal criterion: a proof that no code exists at d equal to the live upper bound 37 is supplied and verified (cert_110_5_37_sh.json). The claim goes further: d=36 is also excluded, giving bound <= 35, which implies the d=37 exclusion.
- Hidden-quantifier and null-model check: the criterion requires the new bound not to be implied by propagation. Propagation over the live table already gives 36 at (110,5), because the live 37 is stale, so lowering to 36 would be subsumed. The claimed bound is 35, strictly below the closure of 36, so it is not implied. The propagation rules (R1, R2, R3) are the standard valid ones, and the closure runs to a fixpoint over the complete table. The win is therefore 36 -> 35 relative to the closure, and 37 -> 35 relative to the live cell. It is not just 37 -> 36.
- Caveats: the claim-time table snapshot could be stale relative to now, since I cannot re-fetch. That limits freshness, not the validity of the proof. Whether the literature already has 35 or lower outside the table is not checkable from this folder.

confirmed_scope: Both certificates verify in exact integer arithmetic, so no [[110,5,36]] (and no [[110,5,37]]) qubit stabilizer code exists, giving upper bound d(110,5) <= 35 versus the claim-time live table value of 37 and the live-table propagation closure of 36.

pass: true
