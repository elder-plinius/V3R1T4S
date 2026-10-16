# VERDICT (novelty skeptic)

context: subagent (same VM)

## Primary table fetch (single request, no retries)
- URL: https://codetables.de/QECC.php?q=4&n=164&k=1
- UTC time: 2026-10-16T20:01:22Z
- HTTP status: 200
- Value shown: "Bounds on [[164,1]] ... lower bound: 33 upper bound: 55"
- sha256: 05af667ae6d87dc678a5e544b752ab7fa3c57ed28cbeca31608a71766b2ab1d8 (file live_QECC_q4_n164_k1.html, 110105 bytes; identical bytes to the claim-time snapshot data/QECC_q4_n164_k1_claimtime.html)

## Claim
Upper bound for [[164,1]] lowered from 55 to at most 53 (no [[164,1,54]]). This is a strict improvement of 2 over the live table (55) if valid. Validity of the certificate is the job of other skeptics, not this one.

## Searches and findings
- Web searches (last 24 months, arXiv/web) for qubit stabilizer-code distance upper bounds at n > 100, LP / shadow-enumerator bounds, and "[[164,1]]" with bound 53/54: nothing found. Hits were only classical work (Calderbank-Rains-Shor-Sloane, Rains shadow enumerators, 1997 quantum-code size bounds), EA-code LP bounds (arXiv 1602.00413, small n), SDP for EA codeword-stabilized codes (arXiv 2311.07111), and the 2024/2025 Monte Carlo / belief-propagation distance estimate paper (arXiv 2402.06481, Entropy 2025), which estimates distances of specific code families and proves no impossibility. None gives a bound at or below 55 (let alone 53) for [[164,1]], and none gives a qubit LP with shadow constraints for n > 100.
- data/TROPHY_CASE_pinned_9b1d444.md (pinned 9b1d444): six result families (degree-diameter graphs, constant-weight codes incl. Delsarte LP bounds, matrix multiplication, Lehmer, VNN-COMP, RobustBench) plus cipher commitments. No quantum/qubit/stabilizer entry and no mention of [[164,1]] or codetables QECC. Nothing ties or beats the claim.
- Open pull requests of elder-plinius/V3R1T4S (web search only, no GitHub tools): three searches returned no PR touching quantum codes, codetables or [[164,1]]. The search engine does not index that repo's PR list (a launch post reportedly cites ~200 PRs), so this check is a search-limited negative, not an exhaustive scan.
- Propagation (from the claim's own check/propagation_check.txt, consistent with the fetched live cell): (165,1) upper 55; (163,2) upper 55, so d(163,2)+1 = 56; none implies <= 53. The new bound is not implied by propagation from other live cells.

## Conclusion
Strictly better than the live table (55 -> <= 53) and than everything found. No tie, no prior record found. Caveat: the open-PR check was web-search only and could not enumerate the PR list.

pass: true
