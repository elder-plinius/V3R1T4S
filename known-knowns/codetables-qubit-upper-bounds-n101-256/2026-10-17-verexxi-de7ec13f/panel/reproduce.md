context: subagent (Claude Code headless on the owner's PC, fresh context)

# REPRODUCE verdict for the claim "no [[192,2,64]] qubit stabilizer code, upper bound at most 63"

## 1. Own checker, written from the definition before reading the author's code

Definition used (Calderbank-Rains-Shor-Sloane quant-ph/9608006 and Rains quant-ph/9611001, as restated in REPRODUCE.md):
stabilizer weight distribution A_0..A_n, |S| = 2^(n-k) = M; B_j = (1/M) sum_i K_j(i) A_i;
shadow Sh_j = (1/M) sum_i (-1)^i K_j(i) A_i; K_j(i) = sum_s (-1)^s 3^(j-s) C(i,s) C(n-i,j-s).
Constraints for an [[n,k,d]] code: A_0 = 1, sum A_i = M, A_j = B_j for 1 <= j < d, A_j <= B_j for j >= d, Sh_j >= 0, A >= 0.

I read only the JSON data (fields n,k,d,u_E0,u_E1,u_Q,v_G,v_H), not check/check_cert.py, and wrote my own script
(outside the folder, temporary). It builds, with Python big integers, the combination
 u_E0*(A_0 = 1) + u_E1*(sum A_i = M) + sum_j u_Q[j]*M*(B_j - A_j = 0) + sum_j v_G[j]*M*(B_j - A_j >= 0) + sum_j v_H[j]*M*(Sh_j >= 0)
and tests: every column coefficient (for A_0..A_192) is <= 0, and the right-hand side u_E0 + u_E1*M is > 0.
A nonnegative A would then give LHS <= 0 < RHS, so the LP is infeasible (Farkas). Multipliers on the inequality rows
must be >= 0: v_G and v_H are all positive (checked). The equality rows are sign-free.
I first tried all 8 sign conventions for the three row groups (the sign convention of the file was not given to me);
exactly one convention works: Q rows as M*(B_j - A_j), G rows as M*(B_j - A_j) >= 0, H rows as M*Sh_j >= 0 with positive
multipliers (the Q-row sign is free for equalities, G and H signs are the natural ones). Real output:

 sq sg sh : max col <= 0 ?, number of positive columns
 1 1 1 False 129 / 1 1 -1 False 131 / 1 -1 1 False 129 / 1 -1 -1 False 68
 -1 1 1 True 0 / -1 1 -1 False 64 / -1 -1 1 False 62 / -1 -1 -1 False 64

For the working convention, for result/cert_192_2_64_sh.json and result/cert_192_2_65_sh.json:
 "rhs>0 True max col True zero cols 1 rhs bits 7101" (both files).
Kernel sanity: K_1(i) = 3(n-i)-i for all i holds, and sum_j K_j(0) = 4^n holds.
Index ranges: u_Q has keys 1..63 (all = equalities for j < 64, all within 1 <= j < d), v_G has keys 66, 67 (both >= d),
v_H has 60 keys among 1..62, all multipliers nonnegative where required. The d = 65 certificate uses the same
multipliers and is also valid (it needs only a subset of the equalities for j < 65, so it is a valid certificate for d = 65).

LP soundness (re-derived): Sh(x,y) = (1/M) A(x+3y, y-x) gives the factor (-1)^i on K_j(i); B = (1/M) A(x+3y, x-y) is the
MacWilliams transform for |S| = 2^(n-k); A_j = B_j for j < d and A_j <= B_j (since S is contained in its normalizer)
are the standard conditions; so a certificate for d = 64 rules out every stabilizer code with distance >= 64, hence
the upper bound is at most 63.

## 2. Author's checker

 python3 -I check/check_cert.py result/cert_192_2_65_sh.json -> VERIFIED [[192,2,65]] shadow=True: value=2138 digits, max column coefficient <= 0, 63+2+60 multipliers (exit code 0)
 python3 -I check/check_cert.py result/cert_192_2_64_sh.json -> VERIFIED [[192,2,64]] shadow=True: value=2138 digits, max column coefficient <= 0, 63+2+60 multipliers (exit code 0)
 check/checker_output.txt contains the same two lines. My independent check agrees with it.

## 3. Table record and propagation

- sha256 of data/QECC_q4_n192_k2_claimtime.html = 20940479cbdff12078de1b0cba4cc0b756a9af457a6aaa441cd741e58415ff76
 and of data/qubit_table_full_n1-256.html = 26245491ba119789eb338424ade4e6b5a74dd46e12df7cec47dd79845de4b0b6;
 both match CLAIM.md. The saved cell page reads "Bounds on [[192,2]] ... lower bound: 37, upper bound: 65"; the full table
 cell n=192,k=2 reads 37-65. (I made no web request; the live re-fetch cannot be checked by me, I rely on the saved record.)
- Rules R1 d(n,k)<=d(n,k-1) (k>=2), R2 d(n,k)<=d(n+1,k), R3 d(n,k)<=d(n-1,k+1)+1 are the standard valid ones.
 Rerun of check/parse_table.py and check/propagate.py: "cells 33152 n-range 1 256", "cells k>=1: 32896 live > implied: 1075";
 live (192,2) = [37, 65], closure = 64 (via R3 from (191,3), whose own closure is 63). Neighbours: (192,1) closure 65,
 (193,2) closure 65, (192,3) closure 64. So the other live cells imply at most 64 and do NOT imply 63.
 Note: the live 65 itself is already non-tight (propagation gives 64), but the claimed 63 is strictly below that, so the
 new bound is not implied by propagation and lowers the live bound by 2.

## 4. Reasoning

The certificate is an exact integer Farkas dual, verified independently by my own from-the-definition script and by the
author's script, deterministic across runs (exit code 0, identical outputs). The propagation check reproduces the
claimed numbers [37, 65] and 64. Claim: no [[192,2,64]] code, upper bound at most 63, not implied by propagation,
and the d = 65 (live bound) certificate also exists and verifies. All checks are exhaustive over all 193 columns and all
multipliers, not samples. No mismatch, no missing object, no non-determinism found.

pass: true
