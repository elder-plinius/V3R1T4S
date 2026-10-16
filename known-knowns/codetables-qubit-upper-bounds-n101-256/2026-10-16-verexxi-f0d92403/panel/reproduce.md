context: subagent (Claude Code headless on the owner's PC, fresh context)

# REPRODUCE panel report, claim q177-1: no [[177,1,58]] qubit stabilizer code

## Own checker (written from the definition, before reading check/check_cert.py)
Definition used (from REPRODUCE.md step 2): stabilizer weight distribution A_0..A_n >= 0, |S| = 2^(n-k) = 2^176;
B_j = 2^-(n-k) sum_i K_j(i) A_i, Sh_j = 2^-(n-k) sum_i (-1)^i K_j(i) A_i,
K_j(i) = sum_s (-1)^s 3^(j-s) C(i,s) C(n-i,j-s). Constraints: A_0 = 1; sum A_i = 2^176; A_j = B_j for 1<=j<d;
A_j <= B_j for j>=d; Sh_j >= 0. My checker (own script, Python big ints, exact) rebuilt the Krawtchouk table, formed
column i coefficient = uE1 + [i=0]uE0 - sum_j uQ_j (P d_ij - K_j(i)) + sum_j vG_j (K_j(i) - P d_ij) + sum_j vH_j (-1)^i K_j(i)
with P = 2^176, and tested: all vG, vH >= 0, vG indices j>=d, all column coefficients <= 0, right-hand side uE0 + uE1*P > 0.
Farkas argument re-derived: for any feasible nonnegative A the combination c.A equals rhs plus a nonnegative quantity,
so c.A >= rhs > 0, but c <= 0 and A >= 0 force c.A <= 0. Contradiction, so the LP is infeasible. (Equality multipliers
are sign-free, so the sign of the Q block is a convention; my first run used the opposite Q sign and failed, the
flipped sign passes. The row scaling by P is a positive factor on inequality rows, hence harmless.)
Sanity of my K/B/shadow formulas: on the [[5,1,3]] code (A = 1,0,0,0,15,0) my code gives B = [1,0,0,30,15,18] and
shadow = [1,0,0,30,15,18], the known values.

My checker output (interpretation a=1,b=1, Q sign flipped):

58 a=1 b=1 max<=0 True rhs>0 True rhs<0 False maxcol sign/len 0 1
59 a=1 b=1 max<=0 True rhs>0 True rhs<0 False maxcol sign/len 0 1
(a, b = scale of the A_0=1 row and the sum A = 2^176 row; the unscaled a=b=1 form is the consistent one; the other scalings gave positive column coefficients and are not the certificate's convention.)
Certificate 58 structure: u_Q keys exactly 1..57, v_G keys {60,61}, v_H keys 0..63 (58 entries), all multipliers >=0.
Certificate 59 structure: u_Q keys exactly 1..58, v_G keys {61,62}, v_H keys 1..64 (59 entries), all multipliers >=0.
Both columns satisfy max column coefficient = 0 (<=0), rhs > 0, for d=58 and d=59.
Validity for the claim: the d=58 certificate excludes any [[177,1,d']] with d' >= 58 (A_j=B_j for j<58 holds for every
d'>=58, and A_j<=B_j, Sh_j>=0 hold always), so the bound is <=57 as claimed.

## Author's checker and steps from REPRODUCE.md (ran as given)
python3 -I check/check_cert.py result/cert_177_1_58_sh.json
VERIFIED [[177,1,58]] shadow=True: value=1884 digits, max column coefficient <= 0, 57+2+58 multipliers   (rc=0)
python3 -I check/check_cert.py result/cert_177_1_59_sh.json
VERIFIED [[177,1,59]] shadow=True: value=2197 digits, max column coefficient <= 0, 58+2+59 multipliers   (rc=0)
Output matches check/checker_output.txt. My own script run twice gave identical output (md5 equal): deterministic.

## Propagation (own script, own regex parse of data/qubit_table_full_n1-256.html, 33152 cells)
Cell (177,1) = 35-59; (178,1) upper 60; (176,2) upper 59; (177,2) upper 59. Closure under R1 (n,k-1), R2 (n+1,k), R3 (n-1,k+1)+1
over all k>=1 cells gives closure(177,1) = 59, so 57 is not implied by propagation within the saved table.
Author's propagate step outputs 59 as well (check/propagation_check.txt). The saved single-cell page
(data/QECC_q4_n177_k1_claimtime.html) shows "lower bound: 35, upper bound: 59". File hashes match CLAIM.md
(66d358ca..., 26245491...).

## Limits
I was forbidden to open websites, so the live-table recheck (immediately-before-claim freshness) could not be reproduced;
only the saved snapshots (claim-time stamps 2026-10-16) were examined. The saved HTML says "Last change: 10.06.2024".
The mathematics (certificate infeasibility and the propagation non-implication) reproduces exactly from the saved files.
The table's note that upper bounds for n>100 are weak and non-monotone is consistent with this being a genuine improvement.

pass: true
