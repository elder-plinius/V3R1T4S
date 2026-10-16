# REPRODUCE skeptic report: claim q142-2 (no [[142,2,47]] qubit stabilizer code)

context: subagent (Claude Code headless on the owner's PC, fresh context)

## Method
Definition quoted from CLAIM.md/REPRODUCE.md: LP over A_0..A_n >= 0 with A_0 = 1, sum A_i = 2^(n-k), A_j = B_j (1 <= j < d), A_j <= B_j (j >= d), shadow Sh_j >= 0, B_j = 2^-(n-k) sum_i K_j(i) A_i, Sh_j = 2^-(n-k) sum_i (-1)^i K_j(i) A_i, K_j(i) = sum_s (-1)^s 3^(j-s) C(i,s) C(n-i,j-s). Farkas: sign-free multipliers on equalities, nonnegative on inequalities, every column coefficient <= 0, positive value.

I first inspected only the certificate JSON structure (keys u_E0, u_E1, u_Q, v_G, v_H) and wrote my own checker (scratch file, own Krawtchouk routine, big-integer arithmetic, own index-range and sign checks). My first attempt had the sign of the equality rows flipped relative to the author's and failed; after that I read check/check_cert.py and aligned the row convention (equality rows are sign-free, so this only changes the multiplier sign convention, not the LP). So my checker is independent in code but not in the row sign convention. It additionally asserts u_Q indices are exactly 1..d-1, v_G indices in d..n, v_H in 0..n, v_G and v_H >= 0.

## Results (real output)
My checker, tuple = (n,k,d, all columns <= 0, value > 0, #u_Q, #v_G, #v_H, digits of value, v_G indices, u_Q indices == 1..d-1):
    result/cert_142_2_47_sh.json (142, 2, 47, True, True, 46, 2, 47, 1040, [49, 50], True)
    result/cert_142_2_48_sh.json (142, 2, 48, True, True, 47, 2, 45, 1087, [50, 51], True)
Author's checker, fresh run with python3 -I:
    VERIFIED [[142,2,47]] shadow=True: value=1040 digits, max column coefficient <= 0, 46+2+47 multipliers   (exit 0)
    VERIFIED [[142,2,48]] shadow=True: value=1087 digits, max column coefficient <= 0, 47+2+45 multipliers (exit 0)
Output matches check/checker_output.txt line for line (only line order differs).
Determinism: two repeated runs of both checkers gave identical output hashes.
Negative control: halving v_G[49] in a copy makes both checkers fail (author's: "column 48 has positive combined coefficient"; mine: columns-<=0 False). So the check is not vacuous.
Certificate file hashes: cert_142_2_47_sh.json sha256 523b3c66c1216627fa177d4bddec4e6b1c7f32b6ac13015745bb7ce4070d2ed0; cert_142_2_48_sh.json sha256 49efcec747b300c6c03d877d2ded5aa015e022d707594c51237a8218a4a4c7be.

## Proof-step re-derivation
- Constraints are valid for any qubit stabilizer code with distance >= 47: A_0 = 1; |S| = 2^(n-k); B is the normalizer enumerator by MacWilliams; N\S has minimum weight >= d so A_j = B_j for j < d (also valid for impure codes); A_j <= B_j since S is contained in N; shadow enumerator coefficients are nonnegative (Rains). Nonexistence of d=47 thus also excludes all d >= 47 (constraints only use distance >= 47).
- Farkas step: for feasible A >= 0, sum_i c_i A_i <= 0 with c_i <= 0, while the combination of the equalities/inequalities equals value > 0 minus nonnegative terms; contradiction. Verified in exact integers (both checkers) with columns 0..142 all <= 0 and value > 0.
- Matched the success criterion's LP ingredients (MacWilliams link, A_i <= B_i, A_i = B_i below d, nonnegativity, shadow).

## Table / propagation
- data/ file sha256: QECC_q4_n142_k2_claimtime.html 66fef426...bde8d and qubit_table_full_n1-256.html 26245491...de4b0b6, both match the claimed hashes.
- My own regex on the saved full table: (142,2) = 30-48, (142,1) = 30-48, (143,2) = 30-49, (141,3) = 27-47. Saved single-cell page text: "Bounds on [[142,2]] ... lower bound: 30 upper bound: 48".
- Author's parse_table.py + propagate.py run: "cells 33152 n-range 1 256"; "cells k>=1: 32896  live > implied: 1075  of which n>100: 1072  n<=100: 3"; (142,2) -> parsed [30, 48], closure 48. Propagation rules give d(142,2) <= min(48 via R1 from (142,1), 49 via R2, 47+1 = 48 via R3 from (141,3)) = 48, so 46 is not implied by other live cells.

## Limits (honest)
- I did not re-fetch the live table (no web access allowed), so "live immediately before claiming" is only verifiable from the saved files, which are internally consistent and hash-matched.
- The criterion literally asks for a proof against d equal to the live bound (48); cert_142_2_48 verifies, and cert_142_2_47 verifies the stronger claim (upper bound 46, a drop of 2).
- Note the saved table has 1075 cells strictly above their propagation closure; this does not affect this claim.

## Conclusion
Both certificates verify exactly under my own independent checker and the author's, deterministically; a tampered copy fails; propagation does not imply the new bound.

pass: true
