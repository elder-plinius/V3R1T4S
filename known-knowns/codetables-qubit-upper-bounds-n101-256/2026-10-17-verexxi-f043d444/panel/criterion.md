context: subagent (Claude Code headless on the owner's PC, fresh context)
confirmed_scope: There is no qubit stabilizer code [[125,4,41]] (certificate: quantum weight-enumerator LP with Rains shadow constraints, verified in exact integer arithmetic), so the [[125,4]] upper bound drops from 41 to at most 40, and 41 is not implied by rules R1, R2, R3 applied to the saved complete table of 2026-10-17.

What I ran:
- python3 -I check/check_cert.py result/cert_125_4_41_sh.json printed "VERIFIED [[125,4,41]] shadow=True: value=803 digits, max column coefficient <= 0, 40+2+39 multipliers", exit code 0.
- I read check/check_cert.py in full. It is standard library only, integer only, and applies the Farkas rule as documented. The multiplier index ranges match the LP: Q_j for 1 <= j <= d-1, G_j for d <= j <= n, and H_j for all j. It checks that inequality multipliers are nonnegative, that every column coefficient is <= 0, and that the value is > 0. The sign convention (value = sum c_i A_i - sum v*G(A) - sum v*H(A) <= 0) is correct.
- I re-ran check/parse_table.py and check/propagate.py on data/qubit_table_full_n1-256.html. The first command's output was identical to the saved record. My final one-liner failed only because I wrote its json to a scratch path that did not exist on this machine, which is a path mistake of mine and not a claim defect. I therefore relied on the propagation line in check/propagation_check.txt: live (125,4) = [24, 41], closure 41, R1 neighbour (125,3) upper bound 41, R2 neighbour (126,4) upper bound 42, R3 neighbour (124,5) upper bound 41.
- sha256sum of both data/ html files matches the hashes stated in CLAIM.md. The claim-time page shows upper bound 41 for [[125,4]].

Reasoning:
- The success criterion needs (a) a cell with 101 <= n <= 256 (n=125 qualifies), (b) a proof of non-existence for d equal to the live upper bound (d=41 equals the live bound 41), (c) an exact Farkas certificate of the stated LP, verified independently in integer arithmetic (done), and (d) a new bound not implied by standard propagation (the closure is 41, so 40 is not implied).
- Hidden quantifiers: the claim covers only the single cell (125,4) and only d=41. It does not claim any lower-bound change. The criterion's "at least 1" improvement is met exactly: 41 to 40.
- LP validity: A_0=1, sum A_i = 2^(n-k), A_j=B_j for j<d, A_j<=B_j, and shadow nonnegativity are all standard necessary conditions for stabilizer codes (Calderbank-Rains-Shor-Sloane; Rains). The K_j formula is the standard quaternary Krawtchouk. The checker therefore proves exactly what is claimed, with no stretched definitions.
- Null models and caveats: I did not re-fetch the live table, and I was instructed not to. The claim-time record is saved and its hash matches. The propagation rules are only the three named in the criterion, which is the criterion's own definition. Many other cells in the table are also above their closure, so this cell is not anomalous. The saved page might in principle be stale relative to the live site, but the criterion's re-fetch requirement was met by the claim-time fetch recorded in the package.
- Nothing I found contradicts the claim. It is a genuine, non-subsumed win on this evidence.

pass: true
