# Novelty verdict

context: subagent (same VM)

## Status fetch (one plain request, no retries)
- URL: https://codetables.de/QECC.php?q=4&n=152&k=1
- UTC fetch time: 2026-10-16T19:57:55Z (from `date -u`, taken just before the single curl request)
- HTTP status: 200 (no challenge page, no block)
- Saved page: live/QECC_q4_n152_k1_live.html (94888 bytes)
- sha256 (sha256sum): d03ffa956a2bf8c67ef4d4cd7ff402c86bc7ffff5d0f2189578489dd0167b0d1
- Value read: "Bounds on [[152,1]]  lower bound: 33  upper bound: 51" (same bytes as the claim-time copy data/QECC_q4_n152_k1_claimtime.html; the table has not moved).
- Claimed bound: upper bound at most 49 (no [[152,1,50]] code), which is strictly below the live 51 (and below the neighbour-derived values: check/propagation_check.txt shows (152,1) from (153,1) is 51, from (151,2)+1 is at most 52; the claimed 49 is not implied).

## TROPHY_CASE.md (pinned 9b1d444, data/TROPHY_CASE_pinned_9b1d444.md)
Read the 100-line file; grep for quantum/QECC/stabilizer/shadow/codetables: no hits. Families listed are degree-diameter graphs, constant-weight codes, matrix multiplication, Lehmer, VNN-COMP, RobustBench, cipher commitments. No quantum code row, nothing at or below 49 for [[152,1]].

## Searches (web only, no GitHub tools) and what they showed
1. "linear programming bound qubit stabilizer codes shadow enumerator upper bound minimum distance n > 100 arXiv 2025": nothing for qubit stabilizer LP at n > 100. Hits were EA-code LP papers (arXiv 1602.00413, small n), SDP for EA CWS codes (2311.07111, small n), arXiv 2601.19848 "Theory of low-weight quantum codes" (read abstract: LP with generator-weight constraints, exact for n <= 9, IBM 127-qubit example only as architecture illustration, no shadow constraints, no [[152,1]] bound).
2. '"[[152,1" quantum code upper bound distance': nothing giving an upper bound for [[152,1]]. Hits: Monte Carlo/BP distance upper bounds for specific codes (arXiv 2402.06481, not a table bound), Kasai ITA2026 (qLDPC family), Magma handbook (binary codes only to n=35).
3. "elder-plinius V3R1T4S pull request qubit stabilizer code codetables upper bound Farkas certificate": no open pull request or page found mentioning this repository and a quantum-code bound. Found arXiv 2603.19901 "SDP bounds on quantum codes: rational certificates" (Angles Munne, Huber, March 2026; read abstract: improves 18 bounds for n-qubit codes with 6 <= n <= 19, rational infeasibility certificates; no n > 100, nothing on codetables.de entries for n = 152). Also Lean-QEC (2605.16523, formalization of distances of qLDPC codes; not a bound on [[152,1]]).
4. "improved upper bounds quantum codes qubit stabilizer linear programming shadow large length codetables new bounds 2025 2026": no new 2025-2026 codetables update or new qubit stabilizer upper bounds for large n; only older LP/shadow material (Rains 1996 shadow bounds, LP solved numerically for n <= 32).

Limits: this is a web search of limited depth, GitHub was deliberately not used for the pull-request search, and search hits that were only abstracts were not read in full. No source found that gives an upper bound at or below 49 for [[152,1]] or that runs the qubit LP with shadow constraints for n > 100. I make no judgement here on whether the certificate is correct (that belongs to other skeptics); only that, if correct, 49 strictly beats the live table value 51 and everything I could find.

novelty: strictly beats live table (51) and all found literature, no tie.

pass: true
