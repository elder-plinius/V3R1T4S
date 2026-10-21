context: subagent (Claude Code headless on the owner's PC, fresh context)

# REPRODUCE panel report, claim q146-2 ([[146,2,48]] nonexistence)

## Method
Before opening check/check_cert.py I looked only at the certificate JSON structure (keys: n,k,d,shadow,u_E0,u_E1,u_Q[1..d-1],v_G,v_H)
and wrote my own checker from the LP definition in REPRODUCE.md / CLAIM.md:
variables A_0..A_n >= 0; K_j(i)=sum_s (-1)^s 3^(j-s) C(i,s) C(n-i,j-s); M=2^(n-k);
rows (all scaled by M, integers): A_0=1 ; sum A_i = M ; M*A_j - sum_i K_j(i) A_i = 0 (1<=j<d) ;
sum_i K_j(i) A_i - M*A_j >= 0 (j>=d, multiplier v_G >= 0) ; sum_i (-1)^i K_j(i) A_i >= 0 (shadow, multiplier v_H >= 0).
Farkas test: the multiplier combination must have every column coefficient (i=0..146) <= 0 and a strictly positive
right-hand side. Python big integers only, no floats.

Sanity of my K / B / shadow formulas: on the [[5,1,3]] code (A=1,0,0,0,15,0) my code gives B=[1,0,0,30,15,18] and
shadow=[1,0,0,30,15,18], which is the known correct result.

## Results of my own checker (my_checker.py, kept outside the claim folder)
Sign convention note: the certificate's u_Q multipliers are for the row B_j - A_j = 0 (opposite sign to my A_j - B_j row).
Equality multipliers are sign-free, so this is legitimate. I tested all 8 sign flips of the three equality groups; only
(E0 +, E1 +, Q flipped) gives max column <= 0 with rhs > 0 (and it does so for both certificates):
  cert_146_2_48_sh.json: (1, 1, -1) maxcol<=0 True  rhs>0 True
  cert_146_2_49_sh.json: (1, 1, -1) maxcol<=0 True  rhs>0 True
Also confirmed: all v_G keys >= d (48 cert: 50,51 ; 49 cert: 51,52), all v_G and v_H values nonnegative (0 negative of
either), u_Q keys cover exactly 1..d-1 (1..47 and 1..48), n,k,d fields = 146,2,48 and 146,2,49.
So the quantum LP with shadow constraints is infeasible for d=48 and d=49: no [[146,2,48]] and no [[146,2,49]] code.
Logic re-derived: a code of distance >= d has A_j=B_j for 0<j<d, A_j<=B_j for all j, Sh_j>=0, A_0=1, sum A=2^(n-k);
a nonneg combination of such rows with all column coefficients <= 0 gives LHS <= 0 while the rhs is > 0, a contradiction.

## Author's checker (run after mine)
Command: python3 -I check/check_cert.py result/cert_146_2_49_sh.json ; and the same for cert_146_2_48_sh.json
  VERIFIED [[146,2,49]] shadow=True: value=999 digits, max column coefficient <= 0, 48+2+48 multipliers   (rc=0)
  VERIFIED [[146,2,48]] shadow=True: value=1143 digits, max column coefficient <= 0, 47+2+47 multipliers  (rc=0)
Output identical to check/checker_output.txt. Determinism: two repeated runs on the 48 certificate gave identical output
(md5 766670fad1060307ed1ceb3fc5718165 both times).

## Table / propagation
- sha256 of data/QECC_q4_n146_k2_claimtime.html = e767c28e...6cad96e627 and of data/qubit_table_full_n1-256.html =
  26245491...de4b0b6, both match CLAIM.md.
- Saved record for the cell shows "Bounds on [[146,2]]" with "upper bound: 49" (live fetch itself not possible for me).
- check/parse_table.py + check/propagate.py: "cells 33152 n-range 1 256", "cells k>=1: 32896 live > implied: 1075 of which n>100: 1072";
  (146,2) live [30, 49], closure 49.
- Independent re-implementation (my own regex parse of the saved table plus a fixpoint loop over R1,R2,R3): U(146,2)=49, closure(146,2)=49.
  So the new bound 47 (and 48) is not implied by propagation from other live cells in the saved table.

## Limits of this review
I did not (and was told not to) refetch the live website, so "live upper bound 49 at claim time" rests on the saved
html files whose hashes match the claim. I did not check the table-side freshness requirement beyond that.
No mismatch, missing object, or non-determinism found.

pass: true
