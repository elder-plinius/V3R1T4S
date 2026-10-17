context: subagent (Claude Code headless on the owner's PC, fresh context)

# REPRODUCE verdict for the claim: no [[128,5,42]] qubit stabilizer code, so the upper bound is at most 41

## Own checker, written before reading the author's code
I wrote my own checker from the LP definition. The definition, as stated in CLAIM.md and REPRODUCE.md:
- Variables are A_0..A_n >= 0.
- B_j = 2^-(n-k) sum_i K_j(i) A_i, with K_j(i) = sum_s (-1)^s 3^(j-s) C(i,s) C(n-i,j-s).
- Sh_j = 2^-(n-k) sum_i (-1)^i K_j(i) A_i.
- Constraints: A_0 = 1, sum A_i = 2^(n-k), A_j = B_j for 1 <= j < d, A_j <= B_j for j >= d, Sh_j >= 0.

I guessed the certificate format from the JSON key names alone: u_E0, u_E1, u_Q, v_G, v_H. Every row is multiplied by 2^(n-k) so all coefficients are integers.
- The equality rows get free-sign multipliers.
- The inequality rows (G_j for j >= d, H_j for all j) are required to be nonnegative.
- I form the column coefficients c_i, which must all be <= 0, and the right-hand side, which must be > 0.
- This is the standard Farkas argument: for feasible A >= 0, sum c_i A_i >= rhs > 0 would contradict c <= 0.

The script is check/mychk.py in my scratch space, not in the claim folder. It uses Python big integers only.

Output of my checker:
- cert_128_5_42_sh.json: Q keys are exactly 1..41, max column coefficient is 0 (<= 0), rhs > 0 (782 digits). Result: pass.
- cert_128_5_43_sh.json: max column coefficient is 0, rhs > 0 (782 digits). Result: pass.
- Index ranges for v_G (>= d) and v_H, and nonnegativity of those multipliers, were asserted and held.
- Final line printed: `True`.

Soundness of the LP, re-derived:
- The MacWilliams identity holds for the stabilizer and normalizer weight enumerators.
- A_j = B_j for j < d holds for any [[n,k,d]] stabilizer code, pure or impure.
- A_j <= B_j holds because S is contained in N.
- The Rains shadow enumerator is nonnegative.
- So infeasibility of this LP rules out [[128,5,42]]. Since [[128,5,43]] would imply a [[128,5,42]] code, ruling out 42 also rules out 43, and the upper bound drops to at most 41.

## Author's checker, run afterwards
- `python3 -I check/check_cert.py result/cert_128_5_43_sh.json` printed `VERIFIED [[128,5,43]] shadow=True: value=782 digits, max column coefficient <= 0, 41+2+41 multipliers`, exit code 0.
- `python3 -I check/check_cert.py result/cert_128_5_42_sh.json` printed `VERIFIED [[128,5,42]] shadow=True: value=782 digits, max column coefficient <= 0, 41+2+41 multipliers`, exit code 0.
- This matches check/checker_output.txt.
- Reading the author's code showed the same LP and Farkas rule as mine. It also validates index ranges and multiplier signs, and uses integer arithmetic only.

## Table record and propagation
- sha256sum of data/QECC_q4_n128_k5_claimtime.html is 8c721d4d79ff6172421d20ce629c1eee19f20b1f4093e65bd21d06c4d0ad24e7, which matches CLAIM.md.
- sha256sum of data/qubit_table_full_n1-256.html is 26245491ba119789eb338424ade4e6b5a74dd46e12df7cec47dd79845de4b0b6, which matches CLAIM.md.
- The saved single-cell page text reads "Bounds on [[128,5]] ... lower bound: 24 upper bound: 43".
- I wrote my own regex parse of the full table (33152 cells) and my own R1/R2/R3 closure over cells with k >= 1. It gave U(128,5) = 43 live and closure 42. The neighbours are U(127,6) = 42, U(128,4) = 43, U(129,5) = 43.
- The author's parse_table.py and propagate.py also ran: 33152 cells parsed; 32896 cells with k >= 1.
- The closure (42) is above the claimed new bound (41), so 41 is not implied by propagation from other live cells.
- A final convenience command in my run failed with a file-not-found error. I had mixed a POSIX scratch path with a Windows Python path, and propagate.py had written its output elsewhere. The closure value itself came from my own independent computation, so this does not affect the result.

## Not done
- No web access, so the live table was not re-fetched. I relied on the saved claim-time page, as the task instructed.
- The certificate is deterministic exact integer data, so non-determinism is not a concern. Both runs gave identical results.

## Conclusion
Both certificates verify in exact integer arithmetic under an independently written checker and under the author's checker. The LP is the correct one. The recorded table state is consistent with the saved files. The claimed bound of at most 41 is not implied by the propagation rules.

pass: true
