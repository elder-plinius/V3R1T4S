context: subagent (Claude Code headless on the owner's PC, fresh context)
confirmed_scope: For the qubit cell (148,2), the exact integer Farkas certificates result/cert_148_2_50_sh.json (d = 50, the live upper bound recorded 2026-10-16) and result/cert_148_2_49_sh.json (d = 49) both verify under check/check_cert.py for the shadow-augmented quantum weight-enumerator LP (stabilizer codes only), so no [[148,2,50]] (hence, by the d = 49 certificate, no [[148,2,49]]) stabilizer code exists, and the propagation closure of the saved complete table at (148,2) is 50, so the new bound of 48 is not implied by other saved cells.

## Reasoning

Criterion read literally: for some (n,k), 101<=n<=256, proof of nonexistence for d = live upper bound, with an exact Farkas certificate checked in integer arithmetic by an independent script, plus non-subsumption by the standard propagation rules. (148,2) is in range. The saved record data/QECC_q4_n148_k2_claimtime.html shows lower bound 30, upper bound 50.

Checks I ran:

1. Certificates, fresh run of `python3 -I check/check_cert.py` on each file in result/:
   - VERIFIED [[148,2,49]] shadow=True: value=1062 digits, max column coefficient <= 0, 48+2+49 multipliers (rc=0)
   - VERIFIED [[148,2,50]] shadow=True: value=1298 digits, max column coefficient <= 0, 49+2+47 multipliers (rc=0)
   So the literal criterion (d equal to the live upper bound, 50) is met, and the bound drops to at most 49; the d=49 certificate gives at most 48.

2. I read check/check_cert.py in full. It is standard library only, integer arithmetic only. The Krawtchouk polynomial K_j(i)=sum_s (-1)^s 3^(j-s) C(i,s) C(n-i,j-s) is the correct q=4 one. Constraints: A_0=1, sum A=2^(n-k), A_j=B_j for 1<=j<d (equalities, free sign multipliers), A_j<=B_j for j>=d, shadow Sh_j>=0 with the (-1)^i factor, which matches Rains' substitution A(x+3y, y-x). Index ranges are enforced and the sign of inequality multipliers is enforced; the value u_E0+u_E1*2^(n-k) must be positive and every column coefficient <= 0. This is a valid Farkas argument. The hidden-quantifier points (pure up to d-1, only A_j=B_j for j<d, which holds for every stabilizer code of distance d) are legitimate, and the claim is limited to stabilizer (additive) codes, which is what the criterion asks for.

3. Null models: flipping a shadow multiplier to negative makes the checker return (False, 'negative inequality multiplier'), so it does reject bad input. Reusing the d=50 certificate with d relabelled 51 still verifies, which is consistent (nonexistence at 51 is weaker and follows from the same inequalities).

4. Propagation: I reran check/parse_table.py and check/propagate.py on data/qubit_table_full_n1-256.html. Output: `[30, 50] 50` (live bounds, closure at (148,2)). check/propagation_check.txt shows the neighbours: R1 (148,1): 50, R2 (149,2): 51, R3 (147,3): 49 so 49+1=50. The best implied bound is 50, so a bound of 49 or 48 is not subsumed by the standard rules applied to other live cells.

5. Stretched definitions: none found. The claim says "upper bound at most 48", which needs the d=49 certificate; that certificate is separately verified. The live-fetch timing (2026-10-16T21:00:48Z) is a saved record I cannot re-fetch (not allowed), so I rely on the saved HTML.

Residual caveat: the checker was written by the claimant, so independence is by inspection only; I found it correct on inspection. Not peer reviewed; the table's own page not re-fetched by me.

pass: true
