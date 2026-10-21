context: subagent (Claude Code headless on the owner's PC, fresh context)

# REPRODUCE report, claim q230-3 ([[230,3,75]] nonexistence)

## Method
Per the instruction, I first read only CLAIM.md and REPRODUCE.md and inspected the JSON key structure of the certificates. I then wrote my own checker from the LP definition quoted in check/check_cert.py's docstring (the definition: A_0=1, sum A_i = 2^(n-k), A_j=B_j for 1<=j<d, A_j<=B_j for j>=d, shadow Sh_j>=0, with B_j = 2^-(n-k) sum_i K_j(i) A_i, Sh_j = 2^-(n-k) sum_i (-1)^i K_j(i) A_i, K_j(i)=sum_s (-1)^s 3^(j-s) C(i,s) C(n-i,j-s)). Only after that did I read the author's check/check_cert.py and compare. My first draft had a wrong guess about row scaling and sign conventions (it reported failure); I corrected it to the definition, rewrote it cleanly in a private temp directory, and reran everything. (The shared temp area had a file-name collision with another process, so the final results below come from a fresh uniquely named directory.)

## Re-derivation of the Farkas step
Take equalities E0 (A_0 - 1 = 0), E1 (sum A_i - 2^(n-k) = 0), Q_j (rows with sign-free multipliers), and inequality rows G_j, H_j >= 0 with multipliers >= 0. For any feasible A >= 0:
u_E0 + u_E1 * 2^(n-k) = sum_i c_i A_i - sum vG*G(A) - sum vH*H(A) <= 0 when every column coefficient c_i <= 0. A certificate with positive value therefore contradicts feasibility. The Q_j range 1..d-1, G_j range d..n and H_j range 0..n are the right index sets. Sanity checks of the definitions I ran: for the [[5,1,3]] stabilizer weight distribution 1+15x^4, the formula gives B = 1,0,0,30,15,18 (the known normalizer enumerator) and Sh = the same (nonnegative); and sum_j K_j(i) = 4^n [i=0] for n=8 for all i.

## My checker (written from the definition, exact integers)
Command: python3 -I chk.py result/cert_230_3_75_sh.json result/cert_230_3_77_sh.json
Output (real):
result/cert_230_3_75_sh.json n,k,d= 230 3 75 multiplier sets |Q|,|G|,|H|= 74 4 74 domains ok: True max column coeff <=0: True (max=0) value>0: True value digits 3163
result/cert_230_3_77_sh.json n,k,d= 230 3 77 multiplier sets |Q|,|G|,|H|= 76 3 75 domains ok: True max column coeff <=0: True (max=0) value>0: True value digits 2462
RESULT [True, True]  (exit 0)

Determinism: two runs on the 75 certificate gave identical output hash (26f9238e5f2f9a59dff624b7cca9cd64 both times).

## Author's checker, run as in REPRODUCE.md
python3 -I check/check_cert.py result/cert_230_3_75_sh.json
VERIFIED [[230,3,75]] shadow=True: value=3163 digits, max column coefficient <= 0, 74+4+74 multipliers   (exit 0)
python3 -I check/check_cert.py result/cert_230_3_77_sh.json
VERIFIED [[230,3,77]] shadow=True: value=2462 digits, max column coefficient <= 0, 76+3+75 multipliers   (exit 0)
Identical to check/checker_output.txt. The author's code matches the definition (same sign conventions as mine, bounds checks, nonnegativity of G/H multipliers enforced). Remark: a d=75 certificate also excludes every d>=75 (the d=75 constraints are implied by any code of distance >=75), so the upper bound is at most 74, which lowers the live bound 77 by 3.

## Table and propagation (saved files only, no web access)
sha256 of data/QECC_q4_n230_k3_claimtime.html begins ac4e69556df8a90aafeb and of data/qubit_table_full_n1-256.html begins 26245491ba119789eb33, matching CLAIM.md. The saved single-cell page states lower bound 44, upper bound 77 for [[230,3]].
My own parser and closure (rules d(n,k)<=d(n,k-1) for k>=2, d(n,k)<=d(n+1,k), d(n,k)<=d(n-1,k+1)+1, applied to a fixpoint over all k>=1 cells):
cells 33152 U(230,3)= 77 {(230, 2): 77, (231, 3): 77, (229, 4): 77}
closure U(230,3)= 77
The author's check/parse_table.py + check/propagate.py also ran (33152 cells, n range 1..256) and agree. So 74 is not implied by other live cells.

## Limits
I could not re-fetch the live codetables.de page (no web access permitted), so "live at claim time" rests on the saved, hash-matching files. The certificates, the checker, the propagation check and determinism all reproduced exactly with no mismatch.

pass: true
