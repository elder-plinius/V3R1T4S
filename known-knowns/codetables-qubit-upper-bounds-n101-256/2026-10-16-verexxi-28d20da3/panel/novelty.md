# Novelty verdict

context: subagent (same VM)

## Live status fetch (one plain request, no retries)
- URL: https://codetables.de/QECC.php?q=4&n=150&k=1
- UTC fetch time: 2026-10-16T18:28:09Z (from `date -u`, file fetch_time.txt)
- HTTP status: 200 (fetch_status.txt; curl stderr empty, fetch_err.txt)
- Saved page: live_QECC_q4_n150_k1.html (92464 bytes)
- sha256: 47511f9f95f6a377da769c0fb1bd811497a555cbc1b10b11c76385bb3c9dfa6c
- Value read: "Bounds on [[150,1]] ... lower bound: 33 upper bound: 51". No challenge page, no block.
- The hash equals the claim-time hash recorded in CLAIM.md (page unchanged since 18:15:30Z).
- Claimed bound: upper bound 49 (no [[150,1,50]]), i.e. 2 below the live 51. Strictly better than the live table.

## Neighbouring cells (data/qubit_table_full_n1-256.html and CLAIM.md claim-time pages)
- [[149,1]] 33-51, [[151,1]] 33-51, [[149,2]] 30-51. Propagation rules give at best 51 (d(n,k)<=d(n+1,k)) and 52 (d(n-1,k+1)+1), so 49 is not implied by neighbours.

## Repo TROPHY_CASE.md (data/TROPHY_CASE_pinned_9b1d444.md)
- Grepped for codetables, QECC, shadow, stabilizer, qubit, "[[" and 150. No quantum-code, QECC or LP-bound row. The six families are graphs, constant-weight codes (Delsarte LP only for classical codes), Lehmer, matrix multiplication, VNN-COMP, RobustBench, plus cipher commitments. Nothing covers [[150,1]].

## Open pull requests of elder-plinius/V3R1T4S
- The GitHub tool was refused (repo not configured), so I used web search only, as instructed. Two searches ("elder-plinius V3R1T4S pull requests"; "... TROPHY_CASE pull request quantum code upper bound [[150,1]]") returned no PR page for that repository and nothing about a quantum-code bound. This is weak evidence (search engines do not index PR lists well); not a verified inspection of the PR list.

## Literature, last 24 months (Oct 2024 - Oct 2026), web and arXiv searches
1. "quantum weight enumerator linear programming shadow constraints upper bound minimum distance qubit stabilizer codes n>100 [[150,1]]" -> Rains quant-ph/9611001 (1996), EA-code LP bounds arXiv 1602.00413 (2016), SDP for EA CWS codes arXiv 2311.07111 (2023). None for n>100.
2. "arXiv 2025 new upper bounds qubit stabilizer codes linear programming codetables.de ..." -> arXiv 2408.10323 (Angles Munne, Nemec, Huber, SDP bounds on quantum codes, v2 Sep 2025): fetched the abstract; concrete results only for n=7, 8, 10, no [[150,1]], no shadow LP for n>100 stated. Others (CV MacWilliams 2502.09514, Hamming-like bound 2306.00048, check-weight-constrained 2601.15446, belief-propagation Monte Carlo distance bound, Entropy 2025, XYZ stabilizer codes 2607.14988) are different settings or give no upper bound of 49 or less for [[150,1]].
3. "stabilizer codes shadow linear programming bound n up to 256 qubit upper bound distance table Grassl 2025 2026 arXiv" -> nothing giving a shadow-LP table for n>100 and nothing claiming d<=49 for [[150,1]].
- Result: no source found that gives an upper bound <=49 on d of [[150,1]] qubit stabilizer codes, or runs the qubit shadow LP for n>100.

## Caveats
- This is a novelty check only. I did not verify the Farkas certificate itself (other skeptics' job). Absence in web search is not proof of absence; Grassl's table notes its qubit upper bounds are "weak", consistent with 51 being a not-fully-optimised value.

## Conclusion
novelty: the claimed bound 49 strictly beats the live table value (51) fetched honestly at 2026-10-16T18:28:09Z, the neighbours' implied bounds (51/52), the pinned TROPHY_CASE.md (no entry), and everything I could find in the last 24 months of literature. Not a tie.
pass: true
