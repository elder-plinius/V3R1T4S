context: subagent (Claude Code headless on the owner's PC, fresh context)

# REPRODUCE panel report, claim q133-2 ([[133,2,44]] nonexistence, bound 45 -> at most 43)

## Method
Read CLAIM.md and REPRODUCE.md, and only the certificate JSON layout (key names and sizes) plus the LP statement in the docstring of check/check_cert.py, which defines the multiplier convention. I then wrote my own checker from the LP definition (A_0=1; sum A_i = 2^(n-k); A_j=B_j for 1<=j<d; A_j<=B_j for j>=d; shadow Sh_j>=0; B_j = 2^-(n-k) sum_i K_j(i) A_i with K_j(i)=sum_s (-1)^s 3^(j-s) C(i,s) C(n-i,j-s)). My checker computes c_i for every column i=0..133 in exact Python integers, requires every c_i<=0, requires the right-hand side value u_E0 + u_E1*2^(n-k) > 0, and range-checks indices and signs (u_Q on 1..d-1 free sign, v_G on d..n >=0, v_H on 0..n >=0). Only after that did I run the author's check/check_cert.py. I did not read the body of check_cert.py beyond its docstring.

## Results (real output)
My checker, both certificates:

    cert_133_2_44_sh.json n,k,d 133 2 44 cols c_i>0: 0 value>0: True nQ 43 nG 2 nH 42
    cert_133_2_45_sh.json n,k,d 133 2 45 cols c_i>0: 0 value>0: True nQ 44 nG 2 nH 44
    MYCHECK VERIFIED        (exit 0)

Author's checker (python3 -I check/check_cert.py ...), exit 0:

    VERIFIED [[133,2,45]] shadow=True: value=934 digits, max column coefficient <= 0, 44+2+44 multipliers
    VERIFIED [[133,2,44]] shadow=True: value=899 digits, max column coefficient <= 0, 43+2+42 multipliers

Both match check/checker_output.txt. Output is byte-identical across two repeated runs of each checker (md5 compared), so no non-determinism.

Negative controls on my checker (all correctly rejected, exit 1): u_E1 perturbed (value>0 fails: MYCHECK FAILED), d changed to 43 (index range assertion fails), a v_H multiplier made negative (sign assertion fails).

LP soundness sanity: the known codes [[5,1,3]] (A=1+15x^4) and [[7,1,3]] (A=1+21x^4+42x^6) satisfy my encoding of all LP constraints (equalities below d, A<=B, shadow >=0): "known code satisfies LP: True" for both. So the LP rows are not over-restrictive on real codes. The proof step is Farkas: for any feasible A>=0, value = sum c_i A_i - sum v_G G(A) - sum v_H H(A) - (equality terms, zero) <= 0, contradicting value>0. Re-derived; it is valid, and the 44 certificate covers degenerate codes too (A_j=B_j only for j<d, A_j<=B_j for j>=d).

## Table and propagation
- sha256 of data/QECC_q4_n133_k2_claimtime.html = a2919c39...fb9c and data/qubit_table_full_n1-256.html = 26245491...4b0b6, both matching CLAIM.md. The saved cell page shows "lower bound: 26, upper bound: 45".
- Independent parse (my own regex, 33152 cells, n 1..256): (133,2) = 26-45. Neighbours' upper bounds: (133,1)=45, (134,2)=45, (132,3)=45 (R3 gives 46). My own closure under R1,R2,R3 gives 45 at (133,2); the bound 43 is not implied by any other live cell.
- Author's pipeline (parse_table.py, propagate.py) gives "[26, 45] 45" as expected.

## Limits
I was not permitted to open any website, so I could not re-fetch the live table; the "live" status rests on the saved, hash-matching snapshot (page footer "Last change: 10.06.2024"). The checks above (certificate validity, both d=44 and d=45, determinism, propagation non-implication on the saved full table) all reproduce exactly. No mismatch, missing object or non-determinism found.

pass: true
