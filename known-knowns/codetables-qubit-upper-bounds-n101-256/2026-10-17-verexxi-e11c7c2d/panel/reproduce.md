context: subagent (Claude Code headless on the owner's PC, fresh context)

# REPRODUCE skeptic verdict for the claim: no [[175,3,57]] qubit stabilizer code (upper bound at most 56, live table 59)

## What I did
1. Read CLAIM.md and REPRODUCE.md. Before reading any author code I looked only at the certificate JSON structure
   (result/cert_175_3_57_sh.json: fields n,k,d,shadow,u_E0,u_E1,u_Q,v_G,v_H) and tried to write my own checker.
   My first attempt guessed the row conventions wrongly (I had E0/E1 swapped and the G inequality in the wrong direction)
   and failed; I then read the docstring of check/check_cert.py to get the exact convention (the row definitions are in the
   docstring, not code that would bias a re-derivation) and wrote a second, independent checker (not copied from the author's
   code, scratch file outside the claim folder).
2. Definition I checked against (quoted from the check/check_cert.py docstring, and consistent with Calderbank-Rains-Shor-Sloane
   and Rains' shadow paper): A_0..A_n >= 0 is the stabilizer weight distribution, K_j(i) = sum_s (-1)^s 3^(j-s) C(i,s) C(n-i,j-s),
   B_j = 2^-(n-k) sum_i K_j(i) A_i, shadow S_j = 2^-(n-k) sum_i (-1)^i K_j(i) A_i >= 0; constraints A_0 = 1, sum A_i = 2^(n-k),
   A_j = B_j for 1 <= j <= d-1, A_j <= B_j for j >= d, S_j >= 0. All of these are valid for any [[n,k,d]] stabilizer code
   (d is a lower bound on min weight of N\S, so the equality rows for j < d are correct also for degenerate codes and for codes
   with larger distance), so infeasibility of the LP rules out every [[175,3,d']] code with d' >= 57.
3. My checker: exact big-integer arithmetic. Sanity asserts on my Krawtchouk function (K_5(0) = 3^5 C(175,5);
   sum_j K_j(0) = 4^175; sum_j K_j(7) = 0), index-range asserts (u_Q in 1..d-1, v_G in d..n, v_H in 0..n), non-negativity of v_G and v_H,
   then for each column i compute c_i = u_E1 + u_E0[i==0] + sum_j (u_Qj + v_Gj)(K_j(i) - 2^(n-k)[i==j]) + (-1)^i sum_j v_Hj K_j(i),
   and the value u_E0 + u_E1 * 2^(n-k).
   Farkas argument re-derived by me: for feasible A >= 0, sum_i c_i A_i = u_E0*A_0 + u_E1*sum A + sum u_Q*Q + sum v_G*G + sum v_H*H
   = value + (terms >= 0 since Q = 0, G >= 0, H >= 0), hence value = sum c_i A_i - (nonneg) <= 0 whenever all c_i <= 0 and A >= 0.
   A positive value is therefore a contradiction, so the LP is infeasible.
4. Real output of my checker:
   - cert_175_3_57_sh.json: "d 57 Qkeys 56 full 1..d-1: True G [59, 60] Hn 58 H range 0 61 / positive columns 0 zero columns 1 / value>0 True digits 1525"
   - cert_175_3_59_sh.json: "d 59 Qkeys 56 full 1..d-1: False G [59, 60] Hn 58 H range 0 61 / positive columns 0 zero columns 1 / value>0 True digits 1525"
     (multipliers on rows 57,58 are present as Q rows; indices are all within the allowed ranges, so the d = 59 certificate is a legitimate certificate on its own.)
5. Author's checker run by me: `python3 -I check/check_cert.py result/cert_175_3_59_sh.json` -> "VERIFIED [[175,3,59]] shadow=True: value=1525 digits, max column coefficient <= 0, 56+2+58 multipliers";
   `python3 -I check/check_cert.py result/cert_175_3_57_sh.json` -> "VERIFIED [[175,3,57]] shadow=True: value=1525 digits, max column coefficient <= 0, 56+2+58 multipliers", exit code 0.
   Matches check/checker_output.txt. Both of my runs and the author's runs agree, and everything is pure integer arithmetic, so there is no non-determinism.
6. Table record: sha256 of data/QECC_q4_n175_k3_claimtime.html = 100faa6c5f8e72cfbb25bd0c033727fbd08ed9af57991177286c3106a26ef37e and of
   data/qubit_table_full_n1-256.html = 26245491ba119789eb338424ade4e6b5a74dd46e12df7cec47dd79845de4b0b6, both exactly as stated in CLAIM.md.
   The saved cell page text reads "Bounds on [[175,3]] lower bound: 34 upper bound: 59". The full table row for n=175, k=3 reads 34-59.
7. Propagation check with my own parser and closure (rules d(n,k) <= d(n,k-1) for k >= 2, d(n,k) <= d(n+1,k), d(n,k) <= d(n-1,k+1)+1,
   iterated to a fixpoint over all 33152 parsed cells): live (175,3) upper = 59, closure = 58. Neighbouring live values: (175,2)=59, (176,2)=59, (176,3)/(177,3) around 58-59.
   Hence 56 (and 57, 58 as well) is not implied by other live cells; the claimed bound of 56 is strictly below the propagation closure of 58.
   This agrees with check/propagation_check.txt (closure 58).

## Reasoning
The certificate verifies independently in exact integer arithmetic under my own implementation of the definition, the Farkas derivation holds, the LP constraints
(including Rains' shadow non-negativity) are valid for qubit stabilizer codes, the saved table data match the claimed hashes and values, and the new bound is not obtained by
the standard propagation rules. The d = 59 (literal live upper bound) certificate also verifies. I did not make a live web request (not permitted); the claim-time page is the saved record.
Limits: I did not re-fetch the live table, so "live immediately before claiming" is taken from the saved page only.

## Files (relative to claim folder)
result/cert_175_3_57_sh.json, result/cert_175_3_59_sh.json, check/check_cert.py, check/checker_output.txt, check/propagation_check.txt,
data/QECC_q4_n175_k3_claimtime.html, data/qubit_table_full_n1-256.html

pass: true
