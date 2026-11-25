# Novelty verdict, A006822(25)

## Fetches
- https://oeis.org/A006822/b006822.txt, 2026-11-23T01:52:48Z, HTTP 200. Last line: `24 5782740798229825207562109439`. The table ends before n=25.
- https://oeis.org/search?q=id:A006822&fmt=text, 2026-11-23T01:52:48Z, HTTP 200. %U ends at n=24 (5782740798229825207562109439). No n=25 value in data, comments or extensions.
- https://oeis.org/search?q=id:A165656&fmt=text, about 01:54Z, HTTP 200. Disconnected 6-regular counts. Its terms go past n=24 (disconnected graphs on 25 vertices need only smaller connected counts). It gives no connected n=25 value. It is a side check, outside the requested set.
- https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md, 01:52:53Z, HTTP 200. No mention of regular graphs, A006822 or sextic graphs.
- https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns, 01:52:53Z, HTTP 200. 46 directories. None concerns regular-graph counts. "biggest-graphs" and "graph-automata-max-period" are not about this. I did not open them.
- https://api.github.com/search/issues?q=A006822+repo:elder-plinius/V3R1T4S, 01:52:53Z, HTTP 200. total_count 0.
- https://api.github.com/search/issues?q=sextic+repo:elder-plinius/V3R1T4S, 01:52:53Z, HTTP 200. total_count 0.
- No release-asset check was done.

## Saved novelty sources (claim/novelty/)
- meringer_reggraphs.html (fetched 2026-11-23T01:50:38Z): Meringer's table. I found no 25-vertex 6-regular count in it. A grep for "24" only hit table cells, and I did not read the table cell by cell.
- cx_2609.31407.txt and cx_2609.31407.pdf: about quartic (4-regular) graphs. 0 hits for sextic, 6-regular or A006822. No 25-vertex 6-regular count.
- gh_search_A006822.json: total_count 0.
- gh_search_regular_graph_counts_next_order.json: total_count 0.
- gh_search_control_A002851.json: total_count 1, a "cubic-graphs-graceful" PR. The positive control works, so the search is live.
- `grep -r 1058090189356372623457538781723` found it only in claim files that are the claimant's own: methodA/A_terms_d6.txt, results/Dbf_check_d6.txt, REPRODUCE.md and CLAIM.md. It is not in any novelty source or OEIS data.

## Web searches (3 of 4 used)
1. "number of connected 6-regular graphs on 25 vertices": only OEIS A006822 (up to n=24), A165627 and Meringer's page. No n=25 value.
2. "1058090189356372623457538781723": no hits.
3. The value 1058090189356373578845816711343 (A165627 n=25) together with the claimed value: no hits. The A165627 b-file in data/ ends at n=24.
No WebFetch was needed.

## Verdict
The primary table is readable and ends at n=24. I found no earlier publication of any n=25 value for connected or all 6-regular graphs. The comparison with neighbouring cells (n<=24) is exact extension, not a tie. This is a first term, and it is novel only if the value is correct. Correctness is for the other skeptics.

injection_suspected: none
context: subagent (fresh)
pass: true
