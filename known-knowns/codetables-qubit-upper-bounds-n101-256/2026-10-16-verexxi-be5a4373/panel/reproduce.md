context: subagent (Claude Code headless on the owner's PC, fresh context)

# REPRODUCE panel report, claim [[159,2,52]] nonexistence (upper bound <= 51)

Note on order: the certificate JSON has an opaque format (u_E0, u_E1, u_Q, v_G, v_H), so I had to read the LP definition in the docstring of check/check_cert.py to know the semantics. I did not read its code logic before writing my own checker. My checker was written from the docstring definition (LP rows: A_0=1; sum A_i = 2^(n-k); A_j=B_j for 1<=j<=d-1; A_j<=B_j for d<=j<=n; shadow Sh_j>=0; all scaled by 2^(n-k)), and I cross-checked the definition against the literature form (Sh(x,y) = A(x+3y, y-x)/|S|, which gives Sh_j = 2^-(n-k) sum (-1)^i K_j(i) A_i; B_j via quaternary MacWilliams with |N| = 2^(n+k)).

## 1. Own independent checker (not the author's code)
Kept outside the claim folder. Differences from the author's code: Krawtchouk K_j(i) is built as the coefficient of y^j in (1+3y)^(n-i) (1-y)^i by polynomial multiplication (not the binomial sum), spot-checked against the explicit sum at 5 points; all multipliers parsed from the JSON; index ranges (u_Q in 1..d-1, v_G in d..n, v_H in 0..n), v_G>=0, v_H>=0, positive value u_E0 + u_E1*2^(n-k), and every one of the n+1 = 160 column coefficients <= 0 checked in Python big integers.

Command: python3 -I mychk.py result/cert_159_2_52_sh.json result/cert_159_2_53_sh.json
Output:
  result/cert_159_2_52_sh.json (True, (True, 'val>0', 'maxcol<=0', 51, 2, 52, ...))
  result/cert_159_2_53_sh.json (True, (True, 'val>0', 'maxcol<=0', 52, 2, 53, ...))
Multiplier counts: d=52: 51 u_Q (indices 1..51), v_G at {54, 55}, 52 v_H; d=53: 52 u_Q, v_G at {55, 56}, 53 v_H. All v_G, v_H nonnegative (min values positive).

Sanity check of my LP definition on a code that exists, the [[5,1,3]] stabilizer (A = 1,0,0,0,15,0): 2^(n-k)*B = [16,0,0,480,240,288], 2^(n-k)*Sh = [16,0,0,480,240,288], so A_j=B_j for j<3, A_j<=B_j for j>=3, Sh>=0. The definitions behave correctly.

## 2. Author's checker, run twice (determinism)
Command (run twice each): python3 -I check/check_cert.py result/cert_159_2_53_sh.json ; python3 -I check/check_cert.py result/cert_159_2_52_sh.json
  VERIFIED [[159,2,53]] shadow=True: value=1238 digits, max column coefficient <= 0, 52+2+53 multipliers   (rc=0, both runs)
  VERIFIED [[159,2,52]] shadow=True: value=1527 digits, max column coefficient <= 0, 51+2+52 multipliers   (rc=0, both runs)
This matches check/checker_output.txt exactly. No non-determinism observed.

## 3. Proof-step rederivation
For feasible A>=0: sum_i c_i A_i = value + sum v_G*G(A) + sum v_H*H(A) with G,H>=0 (equalities contribute 0). With all c_i <= 0 the left side is <= 0 while value > 0, so the right side is > 0: contradiction. Row identities (E0, E1, Q_j, G_j, H_j) agree with the LP above, including the shared MacWilliams row for equality and inequality forms. The code covers all D>=52 as well (a code of distance D>=52 satisfies the d=52 constraints), so nonexistence of [[159,2,52]] gives upper bound <= 51. The d=53 certificate (the literal live bound) also verifies.

## 4. Propagation check (own parser, regex over the saved table, data/qubit_table_full_n1-256.html)
sha256 of both saved HTML files match the claimed hashes (bf8570d7...7652 and 26245491...b6). Own parse: 33152 cells; live (159,2) upper = 53, (158,3)=53, (159,1)=53, (160,2)=54. Own closure under R1 (k>=2), R2, R3 over cells k>=1: closure at (159,2) = 53 (output: "closure (159,2): 53"). So 51 (or 52) is not implied by other live cells. The claim-time page data/QECC_q4_n159_k2_claimtime.html shows "lower bound: 31, upper bound: 53".

## Not done
No live re-fetch of codetables.de (no web access in this role); freshness of the 53 rests on the saved files. No LP solver rerun to find a certificate (not required; exact verification is the check).

No mismatches, missing objects or non-determinism found.

pass: true
