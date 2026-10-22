# Novelty skeptic: C(36,5,3) <= 812
context: subagent (fresh executor, saw only claim/)

## Status source (fetched once, no retries, User-Agent "V3R1T4S-skeptic", no cookies)
- URL: https://coveringrepository.com/download_archive_vkt.aspx
- Fetch time: 2026-10-20T23:14:58Z (request start) to 2026-10-20T23:14:59Z, HTTP 200, 171735 bytes
- sha256 of response: 3bc895193b208e9b712af53f0c1fdc3b1785a3e16ff39d87b932b4bbb4f331f7 (matches the author's snapshot)
- Row (line 415): `36 05 03 03 821`, so the live plain (m=t=3) value is 821

## LJCR
- https://dmgordon.org/covering-designs/ HTTP 200 at 2026-10-20T23:15:09Z (landing page; per-cell pages not on this host anymore)
- https://raw.githubusercontent.com/dmgordo/LJCR/main/coverings/coverdata.json HTTP 200 at 2026-10-20T23:15:18Z (6517686 bytes):
  C(36,5,3) size 821, low_bd 756; history 920 -> 889 (LJCR, 2008-12) -> 871 (Dambmann, 2008-12-23) -> 821 (Anastasios Tampakis, 2009-01-01)
- Web search result for ljcr.dmgordon.org/cover/show_cover.php?k=5&t=3&v=36 shows the title "756 <= C(36,5,3) <= 821"
- The root URL https://raw.githubusercontent.com/dmgordo/LJCR/main/coverdata.json returned 404; the file lives under coverings/.

## Repo elder-plinius/V3R1T4S (gh CLI, read-only, about 2026-10-20T23:15:28Z)
- TROPHY_CASE.md (100 lines): no match for 36,5,3 / C(36 / 36 5 3
- All PRs, open and closed (588, titles and bodies): no match for 36[ ,_]5[ ,_]3, v=36 or C(36
- gh search prs/issues "36,5,3" in repo: none

## Literature and hobbyist search (last 24 months)
- GitHub code search "C(36,5,3)" and "36,5,3 covering": no results
- GitHub repos matching "covering designs" updated since 2024-10-20 (hectorfarahani/covering-designs, TheEslabonGroup/covering-designs, gooverdian/covering-designs-finder, Meliwat/covering-hunt, WynandVStaden/covering-design-records, plus thebrockchain/covering-designs): file trees and READMEs have no (36,5,3) entry
- Web searches ("covering design C(36,5,3) new upper bound 2025 2026", "C(36,5,3) 812/815/818/820", "arXiv 2025 2026 covering designs C(v,5,3)"): no claim below 821; the only recent related item is a C(19,5,3) lower-bound note
- The arXiv API query (export.arxiv.org, recent "covering design") hung with no output and was stopped. arXiv coverage relies on web search only.

## Sanity (independent)
- Object sha256 f7a9401c...6b23 matches. My own checker: 812 blocks, 812 distinct, all 5-subsets of 1..36, 0 of 7140 triples uncovered. Schonheim bound 756 <= 812.

## Verdict
812 < 821 (coveringrepository live, LJCR GitHub). No lower or equal value was found in the repo, its PRs, GitHub or the literature, so this strictly beats everything known.
pass: true
