# Novelty skeptic verdict

context: subagent (same VM)

## Primary status page (fetched once, no retries)
- URL: https://codetables.de/QECC.php?q=4&n=145&k=1
- UTC fetch time: 2026-10-16T19:54:33Z (live/fetch_time.txt)
- HTTP status: 200 (live/http_status.txt); no challenge page, no block
- Value read: "Bounds on [[145,1]] 2 lower bound: 33 upper bound: 49"
- Saved page: live/QECC_q4_n145_k1_live.html
- sha256: 50d08374d09ec79d0a120e630b25db0ffb33ea0151e4594074ba26392a64bf77 (from sha256sum; identical to the claim-time page hash)
- The page also states: "For n>100, the upper bounds on qubit codes are weak (and not necessarily monotone in k)."

## Comparison
Claimed bound: d <= 47 (no [[145,1,48]] code). Live table upper bound: 49. 47 < 49, strictly better by 2.
Propagation (check/propagation_check.txt, own reading): (146,1) -> 49, (144,2) -> 49 giving d(145,1) <= 50. Nothing implies 47 or 48.

## Searches and what they showed
1. WebSearch: LP / shadow enumerator bounds for qubit stabilizer codes, n > 100, 2025 and later. Found only small-length work (Rains shadow LP n <= 32 in arXiv 2009.01244; SDP bounds arXiv 2408.10323 for small codes; EA-code LP arXiv 1602.00413 n <= 15; arXiv 2601.19848 low-weight codes n <= 9; arXiv 2502.14165 quantum Delsarte LP; arXiv 2503.02222 LP for k-uniform states over qudits, q=3, n in 101..2813, not qubit). No qubit shadow LP for n > 100.
2. WebSearch: "[[145,1" upper bound distance. No source gives a [[145,1]] upper bound below 49. arXiv 2501.10163 has a formula only for M3-codes (gives 49 at n=145, a special family, not a general bound). arXiv 2610.18130 (WebFetch) covers heuristic distance upper-bound witnesses for bivariate-bicycle codes, with no LP and no [[145,1]].
3. WebSearch: elder-plinius V3R1T4S pull requests on quantum code bounds. Nothing found. Web search only, no GitHub tool used; absence of search hits does not prove the PR list is empty.
4. WebSearch: general 2025/2026 arXiv search for improved large-length qubit LP bounds with shadow constraints. Nothing found.
5. data/TROPHY_CASE_pinned_9b1d444.md (100 lines, pinned commit): grep for quantum/stabilizer/qubit/codetables/QECC gives no hits. No qubit-code entry, so no prior claim of this or a stronger bound.

## Conclusion
The claimed upper bound 47 strictly beats the live table value 49, the propagation closure, and everything found in the literature, the trophy case, and web search of open PRs. Not a tie. Caveat: this verdict covers novelty only; correctness of the certificate is for the other skeptics. I read no local file outside this folder.

pass: true
