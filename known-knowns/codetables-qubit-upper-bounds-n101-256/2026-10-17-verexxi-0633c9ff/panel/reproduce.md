context: subagent (Claude Code headless on the owner's PC, fresh context)

# REPRODUCE skeptic verdict: [[110,2]], claim "no [[110,2,37]] stabilizer code"

## What I did
1. Read CLAIM.md and REPRODUCE.md. Looked at result/cert_110_2_37_sh.json only as data. It holds n=110, k=2, d=37, shadow=true, u_E0, u_E1, u_Q (indices 1..36), v_G (indices 39, 40), v_H (35 indices, 0..39 excluding 1 and 3). Before reading the checker body I read only its docstring (the definition of the LP). I then wrote my own checker, which uses no code from check/check_cert.py.
2. My checker differs from the author's in these ways:
   - It builds Krawtchouk values from the generating function (1+3z)^(n-i)(1-z)^i by polynomial multiplication, not by the explicit binomial sum. It sanity-asserts K_0(i)=1 and K_j(0)=3^j C(n,j).
   - It restates the definition. The stabilizer weight distribution A_0..A_n >= 0 satisfies:
     - A_0 = 1.
     - sum A_i = 2^(n-k).
     - A_j = B_j for 1 <= j <= d-1.
     - A_j <= B_j for j >= d.
     - Shadow Sh_j >= 0 for all j.
     - B_j = 2^-(n-k) sum_i K_j(i) A_i.
     - Sh_j = 2^-(n-k) sum_i (-1)^i K_j(i) A_i.
   - It multiplies every row by 2^(n-k) = 2^108 so the coefficients are integers.
   - It checks the index ranges (u_Q in 1..36, v_G in 37..110, v_H in 0..110) and the signs (v_G >= 0, v_H >= 0).
   - For each of the 111 columns i it computes c_i, the combined coefficient (equality multipliers of any sign, inequality multipliers nonnegative), and requires c_i <= 0.
   - It requires the value u_E0 + u_E1 * 2^108 > 0.
   - Farkas argument I re-derived: for feasible A >= 0, sum c_i A_i = value + (equality rows, which are 0) + (inequality rows, which are >= 0) >= value > 0. But c_i <= 0 gives sum c_i A_i <= 0, a contradiction. So the LP has no solution, and no [[110,2,37]] code exists. A code with d >= 38 also satisfies the d=37 constraints, so none exists either.
3. Real output of my checker on result/cert_110_2_37_sh.json: every column c_i <= 0 (maximum column coefficient is exactly 0, i.e. no column positive); value > 0 with a 673-digit value; final line `OK`. Exit status 0. (My script printed "max col 0" through a clumsy expression; the pass/fail test in the loop is `t>0 -> FAIL`, which never fired.)
4. Ran `python3 -I check/check_cert.py result/cert_110_2_37_sh.json`. It printed `VERIFIED [[110,2,37]] shadow=True: value=673 digits, max column coefficient <= 0, 36+2+35 multipliers`, which matches check/checker_output.txt. I ran it twice and the md5 of the output was identical both times (bf73d9def0ceaa7ac389a53dc297290d), so it is deterministic.
5. Table and propagation, done independently:
   - sha256 of data/QECC_q4_n110_k2_claimtime.html is 9366ddf8...c2034 and of data/qubit_table_full_n1-256.html is 26245491...4b6, both matching CLAIM.md.
   - The claim-time page states "upper bound: 37" for [[110,2]]. The full table lists 24-37 for (110,2).
   - I parsed all 33152 cells with my own regex. The neighbours are (110,1)=37, (111,2)=37 and (109,3)=37, so R3 gives 38. I then ran the three propagation rules (R1 for k >= 2, R2, R3) to a fixed point over the whole table. The closure at (110,2) is 37, so 36 is not implied by other live cells.
   - This agrees with check/propagation_check.txt. I did not run check/parse_table.py or check/propagate.py.
6. No web requests were made. I rely on the saved claim-time pages, so I could not verify the live table.

## Reasoning
- The certificate is an exact integer Farkas certificate that I independently verified. The LP is the standard one (CRSS quantum MacWilliams identities plus Rains shadow) and I re-derived each constraint and the proof step.
- The success criterion needs a lowering of the upper bound that is not implied by the propagation rules. I confirmed 37 -> 36 is not implied by the saved table.
- No mismatch, missing object or non-determinism found. The one limit is that live-table freshness cannot be checked offline (it is covered by the claim-time page and its hashes).

pass: true
