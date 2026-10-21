context: subagent (Claude Code headless on the owner's PC, fresh context)
confirmed_scope: The exact integer Farkas certificate result/cert_129_2_43_sh.json (quantum weight-enumerator LP with Rains shadow rows) proves no [[129,2,43]] qubit stabilizer (additive) code exists, which lowers the claim-time codetables.de upper bound for [[129,2]] from 43 to at most 42, and 43 is not implied by the standard propagation rules applied to the other live cells of the saved claim-time table.

What I ran (real output):
- python -I check/check_cert.py result/cert_129_2_43_sh.json printed "VERIFIED [[129,2,43]] shadow=True: value=873 digits, max column coefficient <= 0, 42+2+42 multipliers", exit code 0. It matches check/checker_output.txt.
- I read check/check_cert.py in full. It uses only integer arithmetic. Its LP rows are the right ones: A_0=1, sum A = 2^(n-k), A_j=B_j for 1<=j<=d-1 (here d=43), A_j<=B_j for j>=d, and Rains shadow Sh_j>=0. The Farkas rule it checks is sound: every column coefficient <= 0, positive value, equality multipliers of any sign, inequality multipliers nonnegative, and the index ranges are validated.
- check/parse_table.py then check/propagate.py on data/qubit_table_full_n1-256.html printed "[25, 43] 43" for cell (129,2). The closure under R1, R2 and R3 is 43, so 42 is not implied by other live cells. The script also reported that 1075 live cells sit above their implied value, which is the known weakness of the table for n>100 and does not affect this cell.
- data/QECC_q4_n129_k2_claimtime.html (saved claim-time page) shows "lower bound: 25, upper bound: 43" for [[129,2]]. The page states "additive quantum codes" and that upper bounds for n>100 are weak.

Reasoning:
- The success criterion needs an exact Farkas certificate of the quantum weight-enumerator LP, checked in integer arithmetic by an independent script, for a cell with 101<=n<=256. It also needs d to equal the live upper bound, and the new bound must not follow from propagation. Every item holds. n=129 is in range, d=43 equals the saved live upper bound, and the certificate is exact and verified.
- Hidden quantifiers: the proof covers stabilizer/additive codes only. It does not cover non-additive codes. The table is explicitly for additive codes, and the criterion says stabilizer, so this does not stretch the claim. I confined the confirmed scope to the saved claim-time table, because I made no live fetch. The checker is the claimant's own script, but its logic is short and I audited it above. The null model (propagation) gives 43, not 42. The shadow constraints are valid for any stabilizer code, including k>0.
- Residual limit: I did not independently re-derive the Krawtchouk and shadow formulas against the papers. They match the standard Calderbank-Rains-Shor-Sloane and Rains forms as stated in the docstring.

pass: true
