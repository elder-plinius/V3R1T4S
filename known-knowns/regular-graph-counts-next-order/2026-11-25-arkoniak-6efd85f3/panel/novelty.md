# Novelty verdict (partial win p1, regular-graph-counts-next-order)

## Sources checked (UTC, HTTP)
- https://arxiv.org/abs/2609.31407 : 2026-11-25T01:53:29Z, 200. Title "Exact counting of unlabeled quartic graphs by permutation-cycle aggregation", citation_date 2026/09/25. Single fetch, no retry.
- https://oeis.org/A006820/b006820.txt : 2026-11-25T01:53:30Z, 200. Last line "28 567437240683788292989".
- https://oeis.org/A033301/b033301.txt : 2026-11-25T01:53:30Z, 200. Last line "28 567437704731717802783".
- (claim/data/*.fetch_utc show the claimant's own fetches at 2026-11-25T01:49:20Z, all 200; consistent with mine.)
- https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md : ~2026-11-25T01:54Z, WebFetch OK (no HTTP code exposed). No mention of quartic, A006820, A033301, Cheng Xu or regular-graph-counts-next-order.
- https://github.com/elder-plinius/V3R1T4S/tree/main/known-knowns : ~01:54Z, WebFetch OK. About 50 folders, none on regular/quartic graph counts.
- https://github.com/elder-plinius/V3R1T4S/pulls?q=is:pr regular-graph-counts-next-order : ~01:54Z, WebFetch OK. Two open PRs, both by Arkoniak, Nov 23 2026: #1225 "A006822(25)" and #1224 "A002851(21)". Neither is the quartic 29..50 recomputation.
- https://github.com/elder-plinius/V3R1T4S/pulls?q=is:pr quartic OR A006820 OR A033301 OR Cheng : ~01:54Z, WebFetch OK. 7 PRs returned (#1225, #1224, #1176, #523, #333, #202, #160), none about quartic counts. `gh` is not installed, so PR lists came via WebFetch only. Results are page-summarised, not raw.
- Two WebSearch queries (standard mode, ~01:54Z, no HTTP code exposed) on independent verification, quartic/4-regular counts at orders 29..50, Cheng Xu, Meringer, genreg, OEIS b-file extension.

## Results
(a) Status source readable: yes. claim/novelty/cx_2609.31407.txt: Table 4 "Computed unrestricted unlabeled quartic graph counts for 29<=n<=50. These orders are beyond the A033301 snapshot through order 28." Table 5 "Connected ... counts for 29<=n<=50", with a row for n=50 (...155436974703908469745127193896366774959634104). Both tables go to order 50 as claimed. The paper says disconnected counts agree with A033483 only through n=33, so n=34..50 had no outside check.

(b) Earlier independent recomputation of orders 29..50: none found. Search results returned only the Cheng-Xu paper itself, the older Kimberley/GENREG work (to order 22) and the parallel-enumeration paper (arXiv 1907.12455, order 23). No arXiv, OEIS or code-hosting hit for a second computation of these values. This is absence of evidence from a limited web search, not proof.

(c) OEIS b-files: both still end at n=28 (quotes above), so the orders 29..50 values are not in OEIS.

(d) Repo: this partial win is not in TROPHY_CASE.md or known-knowns/, and no open or closed PR files it. Only the sibling claims #1224 and #1225 (different sequences) exist for this target.

Caveats: novelty here is only "first independent recomputation of a published table". It is not a new record value. The tie-is-not-a-record rule applies to record values and does not apply to a named partial win. The PR search is limited to what GitHub's search returned.

context: subagent (fresh, general-purpose)
pass: true
