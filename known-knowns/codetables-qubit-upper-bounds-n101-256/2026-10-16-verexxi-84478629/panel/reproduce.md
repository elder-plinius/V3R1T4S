context: subagent (Claude Code headless on the owner's PC, fresh context)

# REPRODUCE panel report for claim: no [[200,2,66]] qubit stabilizer code (upper bound <= 65)

## Method
Before reading check/check_cert.py I derived the checker from the definition quoted in the claim (REPRODUCE.md step 2):
A_0=1; sum A_i = 2^(n-k); A_j=B_j for 1<=j<d; A_j<=B_j for j>=d; Sh_j>=0; B_j = 2^-(n-k) sum_i K_j(i) A_i,
Sh_j = 2^-(n-k) sum_i (-1)^i K_j(i) A_i, K_j(i)=sum_s (-1)^s 3^(j-s) C(i,s) C(n-i,j-s).
Farkas argument re-derived by me: with u_E0,u_E1 free, u_Q free (j in 1..d-1), v_G,v_H >= 0, if every column
c_i = u_E0[i=0] + u_E1 + sum u_Q(K_j(i)-2^(n-k)[i=j]) + sum v_G(K_j(i)-2^(n-k)[i=j]) + sum v_H (-1)^i K_j(i) is <= 0
then for any feasible A>=0: sum c_i A_i <= 0, but sum c_i A_i = u_E0 + u_E1*2^(n-k) + (equalities = 0) + (inequalities >= 0)
>= value, so value = u_E0 + u_E1*2^(n-k) > 0 is a contradiction. The argument is sound. Index/sign ranges
(Q in 1..d-1, G in d..n, H in 0..n, v >= 0) are asserted by my script. Exact Python integers throughout, no floats.
Constraint validity: A_j=B_j below d and A_j<=B_j are standard; the shadow is Rains'. An [[n,k,d']] code with d'>66
also satisfies the d=66 constraints, so the d=66 certificate excludes all d>=66.
Sanity of my formulas: the [[5,1,3]] code A=(1,0,0,0,15,0) gives B=(1,0,0,30,15,18) and Sh=B, all >=0 as expected.

## My own checker (written independently, then run)
    $ python3 -I mychk.py result/cert_200_2_66_sh.json
    result/cert_200_2_66_sh.json n,k,d 200 2 66 cols>0: 0 max col sign: 0 value>0: True nQ,nG,nH 65 2 66
    OK
    $ python3 -I mychk.py result/cert_200_2_67_sh.json
    result/cert_200_2_67_sh.json n,k,d 200 2 67 cols>0: 0 max col sign: 0 value>0: True nQ,nG,nH 66 2 66
    OK
All 201 columns have coefficient <= 0 (maximum exactly 0), value > 0, all v multipliers nonnegative.
Negative control: lowering u_E1 by 10^3000 in the 66 certificate -> "max col sign: -1 value>0: False / FAIL".
Changing d to 60 -> rejected (Q index assertion). So the checker does discriminate.

## Author's checker (run after mine)
    $ python3 -I check/check_cert.py result/cert_200_2_66_sh.json
    VERIFIED [[200,2,66]] shadow=True: value=2417 digits, max column coefficient <= 0, 65+2+66 multipliers   (rc=0)
    $ python3 -I check/check_cert.py result/cert_200_2_67_sh.json
    VERIFIED [[200,2,67]] shadow=True: value=2342 digits, max column coefficient <= 0, 66+2+66 multipliers   (rc=0)
Output matches check/checker_output.txt. Two repeated runs gave identical output hash (deterministic).

## Propagation / novelty
Saved file data/QECC_q4_n200_k2_claimtime.html: sha256 83407f40...fd60b8 (matches CLAIM.md), shows lower 39, upper 67.
data/qubit_table_full_n1-256.html: sha256 26245491...de4b0b6 (matches CLAIM.md).
My own parse (33152 distinct cells) and closure under R1 (k>=2), R2, R3 over all k>=1 cells:
    raw (200,2): 39-67 ; neighbours (200,1)=67 (201,2)=67 (199,3)=67 -> R3 gives 68
    closure (200,2): 67 implied<=65? False
Author's scripts: parse_table.py + propagate.py reproduce "[39, 67] 67" for (200,2). So 65 is not implied by other
live cells (as stored in the saved table).

## Limitations
I was forbidden to open websites, so I could not re-fetch the live cell; the "live bound is 67" is confirmed only from
the saved, hash-matching snapshot. The success criterion's live re-fetch is for the owner/other panelists. Nothing
else mismatched: no missing object, no non-determinism, no failed check.

## Verdict
Both certificates are exact valid Farkas infeasibility certificates by an independently written exact-integer check;
the bound is not implied by propagation on the saved table. Reproduction confirmed.

pass: true
