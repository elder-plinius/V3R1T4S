# VERDICT (novelty skeptic)

context: subagent (same VM)

## Live status fetch (one request, no retries)
- URL: https://codetables.de/QECC.php?q=4&n=154&k=1
- UTC time: 2026-10-16T20:01:22Z
- HTTP status: 200
- Value shown: "Bounds on [[154,1]]_2: lower bound 33, upper bound 52"
- File: live_QECC_q4_n154_k1.html, sha256 beef68a113abb7963fdb5df6a47650868541d2a4d57c41b02dc8d8f46ed7d4a5 (byte-identical to the claim-time copy; page footer "Last change: 10.06.2024")
- The page notes: "For n>100, the upper bounds on qubit codes are weak (and not necessarily monotone in k)."
- Propagation (check/propagation_check.txt, computed from the claim-time full table): live (154,1) = [33,52]; (155,1) = [33,53]; (153,2)+1 gives 51+1 = 52. Table closure is 52, so a bound of 50 is not implied by propagation. I did not re-fetch the full table (only one request allowed).

## Claim compared
Claim: no [[154,1,51]] qubit stabilizer code, so d <= 50 (table 52, i.e. 2 below). Checker output in check/checker_output.txt reports VERIFIED for d=51 and d=52 with shadow=True. I did not re-run the checker (correctness is for the other skeptics).

## Searches (web only, no GitHub tools)
1. LP / shadow-enumerator bounds for qubit stabilizer codes, n>100, recent years: only Lai-Ashikhmin 2016 (arXiv 1602.00413, entanglement-assisted, n<=20), SDP-bounds papers (arXiv 2311.07111; arXiv 2603.19901 Anglès Munné-Huber, n-qubit codes 6<=n<=19, code size), arXiv 2601.19848 (low-weight codes), a 2025 Entropy/arXiv 2402.06481 Monte Carlo distance upper bound for specific codes (not a theoretical bound). None gives a bound for [[154,1]] or any qubit LP-with-shadow result for n>100.
2. "[[154,1,51]]" / "[[154,1" upper bound: no hit.
3. Open pull requests of elder-plinius/V3R1T4S (web search only, two queries): nothing found. This is a weak negative (search engines index PR pages poorly); I could not inspect the PR list directly.
4. Local data/TROPHY_CASE_pinned_9b1d444.md: 0 matches for quantum/stabilizer/QECC/codetables; no qubit-code row, nothing at or below d=50 for [[154,1]]. Its Delsarte-LP rows are for constant-weight codes only.

## Findings
- Nothing known (live table 52, literature of the last 24 months, trophy case, searchable PRs) gives an upper bound for [[154,1]] at or below 50. The claim strictly beats the table (52 -> 50), not a tie, and is not implied by propagation.
- Caveats: absence in search is not proof; open-PR check limited to web search; novelty is conditional on the certificate being correct (not assessed here).

pass: true
