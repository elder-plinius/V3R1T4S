# Recorded comparison, with explicit evidence limitations

## GitHub repository cell (reproducible immutable source)

- URL: https://github.com/elder-plinius/V3R1T4S/blob/7aca3835635e5323b48cdf3b5b59fcde502cab28/known-knowns/bigger-codes/INDEX.csv
- Branch/commit: `main` pinned to `7aca3835635e5323b48cdf3b5b59fcde502cab28`.
- UTC retrieved from connected GitHub file API in this run: 2026-10-14T02:29:20Z. (Original prior pinned fetch was independently recorded.)
- Request outcome: content returned successfully. Raw HTTP status and headers were not exposed by the GitHub tool and are **not independently known**; no status code is invented.
- Git blob SHA-1: `a9116526aef533c26eb7bfb5417bcf55a6e4fee1`.
- SHA-256 of the exact decoded source INDEX.csv UTF-8 bytes (computed from the connector response): `e7ed745ea3299877231732acb040b97d5e7953c04ef7a76f228856d3b92e2ff7`.
- Row: `"A(34,8,7)",34,8,7,602,601,601Bo-1175,1175,1,601,1,Echols 600,Jordan Boisclair [Bo] archive code a34.8.7.601H,exact LNS polish,codes/A34_8_7_602.txt,1a1d0958047e78b8d29752ccb0210518b170663b6862f84d57669c7b0c02d81e`.
- Claim: 603 > 602, one-word increase.

## Primary external table (web content, raw-body hash unavailable)

- URL: https://aeb.win.tue.nl/codes/Andw.html
- UTC queried: 2026-10-14T02:29:20Z.
- Tool response: page text returned and indexed, but raw HTTP status, response headers and exact raw HTML bytes unavailable in this environment. **No page-body SHA-256 can be honestly reported from this retrieval.**
- Exact displayed cell: d=8, w=7, n=34, `601` (source marker `Bo`) - 1175 upper bound. Verified against the web page's table at the check time.
- Mirror cell: mathematically A(34,8,27)=A(34,8,7) by bitwise complementation; check any separately reported mirror value during fresh-context novelty review.
- Novelty: the authoring session found no larger indexed construction in exact-parameter searches. Not a complete literature or priority check; arXiv:2608.13906 and arXiv:2607.19550 remain required comparison sources for the independent NOVELTY reviewer.

To obtain strict primary-page evidence, a fresh reviewer should fetch the page once using an honest client, record UTC, HTTP status, headers, raw response-body SHA-256, cell and mirror cell, and check newer publications. No challenge bypass or spoofed headers should be used. Replace this provisional note *only through an authenticated independent review*, not through invented values.

## William Echols published explicit code

- Immutable URL: https://github.com/williamechols/cwc-seeded-tabu-search/blob/4f0bf18b094fb15c3634001ea8aed847e8353d1c/codes/34_8_7_600.txt
- Verified via connected GitHub file API in this document-preparation session (not by an isolated NOVELTY skeptic).
- Git blob SHA-1: `2e076dccb635d45218b841a31d2ff2341b80fc3c`.
- File contains exactly 600 lines, 34 binary characters per line, with one trailing newline, length 21,000 characters.
- 600 < 603. Repository `README.md` identifies the published code filenames as `{n}_{d}_{w}_{M}.txt`.
- Distinction: comparison against this published code does not establish completeness of all literature or current record priority.
