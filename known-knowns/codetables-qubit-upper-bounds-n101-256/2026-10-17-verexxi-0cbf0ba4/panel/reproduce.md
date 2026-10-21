context: subagent (Claude Code headless on the owner's PC, fresh context)

# REPRODUCE verdict for the claim: no [[155,3,51]] qubit stabilizer code (upper bound 50 vs live 53)

## What I did

1. Read CLAIM.md and REPRODUCE.md. Looked only at the certificate JSON structure (keys u_E0, u_E1, u_Q, v_G, v_H) before writing anything.
   The author's checker was read only to learn the sign and indexing convention of the multipliers, because the JSON alone does not state it.
2. Wrote my own checker from the definition, without reusing the author's code, in a scratch file outside the claim folder.
   The definition I used, from the Calderbank-Rains-Shor-Sloane quaternary MacWilliams identity and Rains's shadow theory:
   - For an [[n,k,d]] stabilizer code with stabilizer weight distribution A_i and |S| = 2^(n-k), the normalizer enumerator is
     B_j = 2^-(n-k) sum_i K_j(i) A_i.
   - The shadow enumerator is Sh_j = 2^-(n-k) sum_i (-1)^i K_j(i) A_i.
   - The constraints are A_0 = 1, sum A_i = 2^(n-k), A_j = B_j for 1 <= j < d, A_j <= B_j for j >= d (this covers every code with minimum distance at least d), Sh_j >= 0, and A_i >= 0.
   I computed the Krawtchouk polynomials K_j(i) with the 3-term recurrence in exact integers, which is a different method from the author's binomial sum.
   I asserted that the recurrence agrees with the explicit binomial formula on 30 sample (j,i) pairs.
   My checker then confirms three things in exact integer arithmetic:
   - the multipliers on inequality rows are non-negative;
   - u_E0 + u_E1 * 2^(n-k) > 0;
   - every column coefficient c_i = u_E1 + u_E0[i==0] + sum_j (u_Q,j + v_G,j)(K_j(i) - 2^(n-k)[i==j]) + sum_j v_H,j (-1)^i K_j(i) is <= 0, for all 156 columns i = 0..155.
   By Farkas' lemma these three facts mean no non-negative A satisfies the LP, so no such code exists.
3. Ran my checker and the author's checker on both certificates.
4. Independently re-parsed data/qubit_table_full_n1-256.html and computed the propagation closure with a fixpoint over the rules
   R1 d(n,k) <= d(n,k-1) for k >= 2, R2 d(n,k) <= d(n+1,k), R3 d(n,k) <= d(n-1,k+1)+1.
5. Checked the sha256 hashes and the saved claim-time page.

## Real output

My checker:

    result/cert_155_3_51_sh.json OK n,k,d= 155 3 51 value>0, all 156 columns <=0; Q 50 G 2 H 50 max col sign True mx==0? True
    result/cert_155_3_53_sh.json OK n,k,d= 155 3 53 value>0, all 156 columns <=0; Q 50 G 2 H 50 max col sign True mx==0? True

Author's checker, run with python3 -I check/check_cert.py:

    VERIFIED [[155,3,53]] shadow=True: value=1210 digits, max column coefficient <= 0, 50+2+50 multipliers
    VERIFIED [[155,3,51]] shadow=True: value=1210 digits, max column coefficient <= 0, 50+2+50 multipliers

Both checkers agree, both exit with code 0, and the output matches check/checker_output.txt.
Repeated runs give identical results.

Hashes (sha256sum):

    ad092d4b904c89212e0de366657e1b97a07d53fd7f0aa4ed045a48ca892fcfba  data/QECC_q4_n155_k3_claimtime.html
    26245491ba119789eb338424ade4e6b5a74dd46e12df7cec47dd79845de4b0b6  data/qubit_table_full_n1-256.html

Both match CLAIM.md.

The saved single-cell page reads "Bounds on [[155,3]] ... lower bound: 30 ... upper bound: 53".

My own table parse found 33152 cells with (155,3) = 30-53. The neighbouring cells are:

    (155,2)  30-53
    (155,4)  30-53
    (156,3)  30-53
    (154,4)  30-52
    (154,3)  30-52
    (156,2)  30-53

My propagation closure for (155,3) is 52, matching check/propagation_check.txt. A bound of 50 (and also 51) is therefore not implied by propagation from other live cells.

## Reasoning

- The LP I derived from the definitions matches the one the author states. The certificate is a valid Farkas dual: the column coefficients are all non-positive and the right-hand value is positive. The 1210-digit value shows the integers are large but exact.
- The d=51 LP uses G inequalities for every j >= 51, so it excludes all codes with distance at least 51. Hence the true maximum distance is at most 50.
- The d=53 certificate is a relabelling of the d=51 one. It also verifies independently, so the literal criterion (the live upper bound 53) is met too.
- The claimed bound is strictly below the propagation closure (52), so the "not implied" condition holds.
- Limitation: I had no network access, as instructed. The "live immediately before claiming" condition rests on the saved claim-time page, whose hash and content match the claim.
- No mismatch, missing object or non-determinism was found.

pass: true
