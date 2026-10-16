context: subagent (Claude Code headless on the owner's PC, fresh context)
confirmed_scope: Per the claim-time table record (upper bound 67 for [[200,5]]), the exact integer Farkas certificates result/cert_200_5_67_sh.json and result/cert_200_5_65_sh.json (quantum weight-enumerator LP with MacWilliams and Rains shadow rows) show no qubit stabilizer code [[200,5,d]] exists for d >= 65 (so the upper bound is at most 64), and that bound is not implied by the propagation closure (67) of the saved complete table.

## Reasoning (role: CRITERION)

Criterion elements checked literally:
1. Cell in range: n=200, k=5, 101<=n<=256. OK.
2. d equal to the live upper bound: data/QECC_q4_n200_k5_claimtime.html (sha256 matches CLAIM.md, c008b563...) records "upper bound 67". The d=67 certificate is the literal reading. I ran:
   - `python3 -I check/check_cert.py result/cert_200_5_67_sh.json` -> `VERIFIED [[200,5,67]] shadow=True: value=2046 digits, max column coefficient <= 0, 66+2+66 multipliers` (rc=0)
   - `python3 -I check/check_cert.py result/cert_200_5_65_sh.json` -> `VERIFIED [[200,5,65]] shadow=True: value=1806 digits, max column coefficient <= 0, 64+3+64 multipliers` (rc=0)
   The lowering is therefore by at least 1 (literal), and in fact by 3 (67 -> 64).
3. Hidden-quantifier hunt: I read check/check_cert.py in full. Rows: A_0=1, sum A=2^(n-k), A_j=B_j for 1<=j<=d-1 (index range enforced), A_j<=B_j for j>=d, shadow >=0 (multipliers forced nonnegative, sign (-1)^i K_j(i)). The Farkas inference (value>0, all column coefficients <=0) is sound; arithmetic is Python ints (no floats). Checker is standard library only. The "independent script" is by the same author, so I tested its LP kernel myself: with kraw() and the [[5,1,3]] stabilizer weight distribution A=(1,0,0,0,15,0) it gives B=[1,0,0,30,15,18] and shadow [1,0,0,30,15,18], matching the known normalizer enumerator. So the MacWilliams/shadow rows are correctly formulated and the LP only uses constraints valid for every stabilizer code.
4. Not implied by propagation: I re-ran check/parse_table.py and check/propagate.py on data/qubit_table_full_n1-256.html (sha256 matches). Output: `live (200,5): [38, 67]  closure of the live table at (200,5): 67  neighbours R1 (n,k-1): [38, 67]  R2 (n+1,k): [38, 67]  R3 (n-1,k+1): [38, 67]`. Every neighbour cell has upper bound 67, so no rule gives <=66, let alone 64.
5. Null model: the claim is not a statistical result; the relevant null (certificate trivially "verifying" any d) is excluded because the checker rejects positive column coefficients and the LP reading above is correct; a d-independent flaw would have to be in the LP rows, which I validated on a known code.

Residual caveats (do not change the verdict, but bound the scope):
- I could not re-fetch the live table (no web allowed); I rely on the saved claim-time record. The criterion requires a live re-fetch immediately before claiming; the folder documents one at 2026-10-16T20:59:43Z.
- The proof covers stabilizer codes (what the criterion names); it does not by itself address non-additive codes.
- The 67 certificate being the "literal" win and the 65 certificate being a stronger bound are both verified; the claim's 64 depends on cert_200_5_65_sh.json (verified).
- Certificate is by exact rationals/integers; the huge LP optimum being outside what the table (weak upper bounds in this range) shows is plausible but unexamined by me beyond the checks above.

Verdict: meets the full success criterion for cell (200,5), with the scope above.

pass: true
