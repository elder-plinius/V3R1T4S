# Novelty report, cell kings-a247413-d33

context: Claude Code subagent, fresh context

Claim read: 33 decimals of the A247413 constant, 1.342643951124601297851730161875740 (README.md). Bar: D >= (DATA terms) + 4.

## Fetches (one plain GET each, curl with the honest user agent; the log is not shipped in this package)
- Primary: https://oeis.org/search?q=id:A247413&fmt=json, 2026-10-19T01:44:50Z, HTTP 200, sha256 12c0e72579f0e422ddf1a43bfb25eda74756be01107b7bfcee3d8af08da40ef8 (identical to the hash the author recorded). Value read: DATA = 1,3,4,2,6,4,3,9,5,1,1,2,4,6,0,1,2,9 = 18 terms, revision 30, last edit 2026-05-30T16:40:43-04:00; the only extension note is "a(14)-a(18) computed by Kai Liang, added by Vaclav Kotesovec, Oct 24 2025". So D must be >= 22; the claim has 33. No b-file or longer value listed.
- the trophy-case file, 2026-10-19T01:44:50Z, 200, sha256 b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1: no mention of kings, A247413 or hard-core entropy.
- Pull requests pages 1-5 (sha256 values in my fetch log, not shipped), all 200, 470 PRs read by title (numbers up to 480). None concerns the king graph, A247413, kings entropy or A063443; I filtered titles and the first 3000 characters of every body for king/247413/hard-core/kappa/entropy/independent and none matched on this target. No competing PR by anyone.
- known-knowns directory, 200: 20 folders, none on kings or lattice-gas constants. No merged folder for this target.
- arXiv API, four queries (all 200, hashes in my fetch log, not shipped): (1) "king graph" AND "independent set": only Liang 2505.12776 (2025-05-19), Liang 2507.04007 (2025-07-05) and an unrelated odd-independence paper (2025-10-02); (2) "hard square" AND "king": Liang 2507.04007, Pettersen et al. 2014 (CTM upper bounds on hard squares), a 2014 capacities paper; (3) "non-attacking kings": nothing newer than 2024 and nothing relevant; (4) "hard-core" AND "next-nearest" AND "entropy": nothing newer than 2022, no digit table for the king constant.
- Literature record from the folder (not refetched): Liang's bracket 1.34264395112460129 7851 to 1.34264395112460129 8092 is 21 decimals; the claim's value lies inside it. No source found with 22 or more decimals, none with 33.

## Assessment
The best published value known to me and to the folder is Liang's 21-decimal bracket (OEIS shows 17). The claim's 33 decimals strictly exceed it, and exceed the D >= 22 bar. No competing PR or trophy entry exists. Limits of this search: the arXiv API queries are narrow, no general web search was made (rules forbid a browser), and a private or very new unindexed value cannot be excluded; I found none. The OEIS "more" keyword and the author's earlier search for the 21-term extension returning "No results" are consistent with no longer published value.

novelty: strictly beats all known (33 decimals vs 21-decimal published bracket; 18 OEIS terms)
unresolved: Google Scholar / MathWorld / Finch tables not fetched (no general web search allowed); a MathWorld hard-square-type page could list a few more decimals but it is unlikely to hold 33.

pass: true
