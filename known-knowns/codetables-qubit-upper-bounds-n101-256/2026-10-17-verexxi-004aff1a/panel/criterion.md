context: subagent (Claude Code headless on the owner's PC, fresh context)

## What I did
- Read CLAIM.md, REPRODUCE.md, check/check_cert.py (full source).
- Ran: python3 -I check/check_cert.py result/cert_135_6_45_sh.json
  Output: VERIFIED [[135,6,45]] shadow=True: value=898 digits, max column coefficient <= 0, 43+2+43 multipliers (exit 0)
- Ran: python3 -I check/check_cert.py result/cert_135_6_44_sh.json
  Output: VERIFIED [[135,6,44]] shadow=True: value=898 digits, max column coefficient <= 0, 43+2+43 multipliers (exit 0)
- Re-ran the propagation check (check/parse_table.py, check/propagate.py on data/qubit_table_full_n1-256.html).
  Result: live (135,6) = [25, 45]; closure under R1/R2/R3 = 44. Neighbours: (135,5) [26,45], (136,6) [26,45], (134,7) [25,43] (R3 gives 43+1 = 44).
- sha256 of data/QECC_q4_n135_k6_claimtime.html and data/qubit_table_full_n1-256.html match the values stated in CLAIM.md. The saved cell page says "Bounds on [[135,6]]", upper bound 45.

## Reasoning
- The success criterion asks for an exact Farkas certificate of the weight-enumerator LP (MacWilliams link, A_i <= B_i, A_j = B_j for 0 < j < d, nonnegativity, shadow nonnegativity), checked in exact integers by an independent script, at d equal to the live upper bound, with the new bound not implied by propagation.
- I read the checker's LP against the standard formulation. Krawtchouk K_j(i) is correct for q=4. The rows are scaled by 2^(n-k). The shadow rows use (-1)^i K_j(i), as in Rains. Equality multipliers are sign-free, inequality multipliers are checked nonnegative, index ranges are enforced, the value is required to be positive, and every column coefficient is required to be <= 0. This is a valid Farkas argument, and the arithmetic is integer-only with no hidden floats.
- Literal criterion: the d=45 certificate (d equal to the live upper bound) verifies on its own. The d=44 certificate verifies too. So the bound drops from 45 to at most 43, which is a drop of at least 1 (in fact 2).
- Null model and subsumption: the propagation closure of the live table at (135,6) is 44, driven by (134,7) at 43. The claimed 43 is strictly below that closure, so propagation from other live cells does not imply it. The live cell itself is already weak, since 45 is above the closure of 44, but the criterion compares the new bound with the propagated value. 43 beats both.
- Hidden quantifiers: the claim is stated for n=135, k=6 and stabilizer (additive) qubit codes only. It makes no statement about non-additive codes. The claim says "at most 43", which matches the evidence. The in-folder table record is a saved page, so I cannot re-check that the live page is unchanged. That is outside what I may do, and the criterion's re-fetch requirement is documented with a hash.
- One caveat: the d=45 certificate was derived from the d=44 one, but each is checked independently, so this does not matter.

confirmed_scope: No [[135,6,44]] (hence no [[135,6,45]]) qubit stabilizer code exists, by an exact integer Farkas certificate of the shadow-augmented quantum weight-enumerator LP verified by check/check_cert.py, so the upper bound on d for [[135,6]] is at most 43, which is below both the claim-time table value 45 and the propagation closure 44 from other cells.

pass: true
