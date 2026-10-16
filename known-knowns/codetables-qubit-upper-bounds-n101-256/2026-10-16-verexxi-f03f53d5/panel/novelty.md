# Novelty verdict, claim [[158,1,52]] nonexistence (new upper bound d <= 51)

context: subagent (same VM)

## Live status fetch (single request, no retries)
- URL: https://codetables.de/QECC.php?q=4&n=158&k=1
- UTC time (date -u, taken immediately before the request): 2026-10-16T20:01:22Z
- HTTP status: 200 (curl exit 0, no challenge page)
- Value shown: "Bounds on [[158,1]] lower bound: 33 upper bound: 53"
- sha256 of saved file live_QECC_q4_n158_k1.html: d31b4dac0672c8edbfbd0ad60974cf6129f0b89a016a234ed4e0fc1fe4db9540
  (identical to the claim-time file's sha256, so the cell is unchanged since the claimant's fetch at 19:44:24Z)
- Claimed bound: d <= 51 (no [[158,1,52]]), which is 2 below the live 53. A strict improvement over the table.

## Propagation (from the claimant's check/propagation_check.txt, not re-derived by me)
- Neighbours: (159,1) = [33,53], (157,2) = [31,53] giving 54. Nothing implies a value below 53.

## Searches and findings
- data/TROPHY_CASE_pinned_9b1d444.md (100 lines): no [[158,1]] or qubit-code/QECC entry. Only degree-diameter, constant-weight, matrix-multiplication, etc. Delsarte LP entries concern constant-weight codes, not quantum codes.
- Web searches (last ~24 months, arXiv and web):
  - "[[158,1]] qubit stabilizer upper bound LP shadow enumerator": nothing about n=158. Results cover the method only (Rains shadow enumerators, EA-code LP 1602.00413, small-n tables).
  - "improved LP bounds qubit shadow constraints n>100": closest hits are arXiv 2408.10323 (SDP bounds on quantum codes, Aug 2024; small cases such as ((8,9,3)), ((10,5,4))), 2601.19848 (low-weight codes, n<=9), 2601.15446 (check-weight-constrained qLDPC bounds). None gives a bound for [[158,1]] or qubit LP/shadow bounds for n>100.
  - '"[[158,1" 2025 OR 2026 no code exists': no hit.
  - Open pull requests of elder-plinius/V3R1T4S, web search only (no GitHub tools): two searches returned no PR mentioning quantum codes, codetables or LP certificates. They also did not return the repository's PR list, so absence is only weakly evidenced. This is a limitation.
- Also seen: the codetables page itself says upper bounds for n>100 are weak, which is consistent with room for an LP improvement. A Zenodo record (distance-4 codes) is unrelated.

## Assessment
Nothing found at or below 51 for [[158,1]]; the live table (53) is strictly beaten by the claimed 51, and the trophy case and literature show no prior or tying result. Only the web-search-only PR check is soft. This verdict covers novelty only, not certificate correctness.

pass: true
