context: subagent (Claude Code headless on the owner's PC, fresh context)

# REPRODUCE verdict, claim [[129,2]] upper bound 43 -> 42

## Definition I checked against (quoted from the docstring of check/check_cert.py, which I read only for the LP definition and the certificate format)
"E0: A_0 = 1; E1: sum_i A_i = 2^(n-k); Q_j: sum_i K_j(i) A_i - 2^(n-k) A_j = 0 for 1 <= j <= d-1; G_j: same expression >= 0 for d <= j <= n; H_j: sum_i (-1)^i K_j(i) A_i >= 0 for 0 <= j <= n (shadow)". Farkas rule: integer multipliers (Q free sign, G and H nonnegative) with every column coefficient c_i <= 0 and u_E0 + u_E1 2^(n-k) > 0 give infeasibility.

I re-derived the proof step: for feasible A >= 0, value = sum_i c_i A_i - sum v_G G(A) - sum v_H H(A) (the Q rows vanish), and this is <= 0 when all c_i <= 0 and G, H >= 0, contradicting value > 0. The constraints themselves are the standard ones (A_0=1, |S|=2^(n-k), MacWilliams B_j, A_j=B_j below d, A_j<=B_j, Rains shadow >= 0), so the argument is valid.

## What I ran
1. My own checker (scratch script my_check.py, written before reading the author's code). It builds K_j(i) independently as the z^j coefficient of (1+3z)^(n-i)(1-z)^i by polynomial multiplication, not the author's binomial sum. It asserts: n,k,d = 129,2,43, shadow true; u_Q indices are exactly 1..42; v_G indices are {45, 46} (inside d..n); v_H has 42 indices inside 0..n; all v_G and v_H >= 0; value u_E0 + u_E1 * 2^127 > 0; and for each of the 130 columns i = 0..129 the combined coefficient c_i <= 0 (asserted for every column; the maximum is 0). Output: "all columns <=0 ... OK".
2. python3 -I check/check_cert.py result/cert_129_2_43_sh.json printed: "VERIFIED [[129,2,43]] shadow=True: value=873 digits, max column coefficient <= 0, 42+2+42 multipliers", exit code 0. Its output has the same md5 as check/checker_output.txt, so the output is deterministic and matches the saved file.
3. Table: sha256 of data/QECC_q4_n129_k2_claimtime.html is 19c28eb589e7dc3562d188b951a584ff23a27b333e04fe8b07ae03a9f901e551 and of data/qubit_table_full_n1-256.html is 26245491ba119789eb338424ade4e6b5a74dd46e12df7cec47dd79845de4b0b6, both matching CLAIM.md. The claim-time page reads "Bounds on [[129,2]] lower bound: 25 upper bound: 43".
4. Propagation, with my own table parser and closure (33152 cells parsed): (129,2)=25-43; neighbours (129,1)=27-43, (130,2)=26-44, (128,3)=25-43 (so R3 gives 44). Iterating R1, R2, R3 to a fixpoint gives 43 at (129,2). The author's parse_table.py and propagate.py also give [25, 43] and 43. So the new bound 42 is not implied by other live cells under these rules.

## Reasoning and caveats
The certificate is a complete exact object (one JSON file, all multipliers present), it passes two independent exact integer checks, and the checker does not depend on sampling because all 130 columns and all multiplier constraints are tested. Nothing was non-deterministic. I did not and could not re-fetch the live table (no web access, as instructed); I relied on the saved claim-time page. Rains-style shadow constraints for stabilizer codes are the standard published ones (quant-ph/9611001), and the sign/index conventions used in the checker match the generating-function definition of K_j(i) I used independently.

pass: true
