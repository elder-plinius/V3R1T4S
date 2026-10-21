context: subagent (Claude Code headless on the owner's PC, fresh context)

# REPRODUCE verdict for the claim: no [[173,2,57]] qubit stabilizer code (upper bound 56, live table 59)

## What I did
1. Read CLAIM.md and REPRODUCE.md. Before reading any author code I inspected the certificates' structure
   (result/cert_173_2_57_sh.json and result/cert_173_2_59_sh.json: keys n,k,d,shadow,u_E0,u_E1,u_Q,v_G,v_H, big-integer strings).
2. Wrote my own independent checker from the definition (not shown the author's check/check_cert.py first).
   Definition used: for an [[n,k,d]] stabilizer code with stabilizer weight distribution A_i (A_0 = 1, sum A_i = 2^(n-k) = M),
   K_j(i) = sum_s (-1)^s 3^(j-s) C(i,s) C(n-i,j-s); M*B_j = sum_i K_j(i) A_i (normalizer, MacWilliams);
   M*Sh_j = sum_i (-1)^i K_j(i) A_i >= 0 (Rains shadow); A_j = B_j for 1 <= j < d; A_j <= B_j for j >= d; A >= 0.
   Farkas: integer multipliers u (free) on the equalities and v >= 0 on the inequalities such that the combination has every
   column coefficient <= 0 while the right-hand side u_E0 + u_E1*M is > 0.
3. Sanity-tested my K/B/shadow formulas on the [[5,1,3]] code (A = 1,0,0,0,15,0): B = 1,0,0,30,15,18, shadow = same, as expected.
4. Ran my checker (big-integer arithmetic, no floats) on both certificates. Real output:
   - cert_173_2_57_sh.json: Q keys 1..56 (56), G keys [59, 60], H keys 0..62 (56); v_G >= 0 True, v_H >= 0 True;
     with the sign convention Q-row = (B_j - A_j)*M, G-row = (B_j - A_j)*M, H-row = M*Sh_j: max column coefficient <= 0 True, RHS > 0 True. VALID.
   - cert_173_2_59_sh.json: same multipliers/keys; VALID by the same test.
   Other sign combinations fail, which shows the test is not vacuous. The certificate uses equalities only for j <= 56 and
   inequalities at j = 59, 60 (both >= 57), so it applies to any code with d >= 57, hence rules out [[173,2,57]] and also 58, 59.
5. Ran the author's REPRODUCE steps: `python -I check/check_cert.py` on both certificates: both print
   "VERIFIED [[173,2,...]] shadow=True: value=1415 digits, max column coefficient <= 0, 56+2+56 multipliers", exit code 0; output
   identical on repeated runs (md5 of two runs equal), and identical to check/checker_output.txt (determinism confirmed).
6. Table record: sha256 of data/QECC_q4_n173_k2_claimtime.html = 19e8a7b6...9a02f and of data/qubit_table_full_n1-256.html = 26245491...de4b0b6, both matching CLAIM.md.
   The page says "Bounds on [[173,2]]  lower bound: 34 ... upper bound 59" (parsed table gives [34, 59]).
7. Propagation: ran check/parse_table.py and check/propagate.py in a scratch directory; the result for (173,2) is `[34, 59] 58`, i.e. the closure
   of other live cells gives 58 > 56, so the claimed bound 56 is not implied by the propagation rules. Neighbours: (173,1)=59, (172,2)=58, (172,3)=58, (174,2)=59.

## Reasoning
The certificate is an exact integer Farkas infeasibility proof, independently confirmed by my own from-definition checker for the LP
with MacWilliams and shadow constraints. No missing objects, no mismatch, no non-determinism. The claim lowers the table bound 59 to
at most 56 (by at least 1), the new bound is not implied by propagation. Not re-fetched live (no web access allowed); relied on the saved claim-time page as instructed.
Minor note: the d=59 certificate is a relabelling of the d=57 one, and is valid on its own.

pass: true
