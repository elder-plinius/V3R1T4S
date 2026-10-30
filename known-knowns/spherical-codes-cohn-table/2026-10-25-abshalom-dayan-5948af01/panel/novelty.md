role: novelty
context: subagent (Agent tool, fresh context, model claude-opus-5-5), saw only claim/ and its own fetches

novelty: CONFIRMED. c* of object/code_6_575.txt is 0.792679835684486880498... It is strictly below the live (6, 575) cosine 0.792780236785 by 0.00010040110051312, which clears the 1e-10 margin. No table row, arXiv paper of the last 24 months, Zenodo table, TROPHY_CASE entry or pull request reaches c*.

injection_suspected: none found (I grepped the claim's text files and inputs for instruction-like phrases and got no hits)

## 1. Status source: one plain fetch per page (work-novelty/fetch.log)

User-Agent "V3R1T4S-research-agent (honest single fetch)", no retries, no cookies.

| time (UTC, date -u) | URL | HTTP | bytes | sha256 | saved as |
|---|---|---|---|---|---|
| 2026-10-25T00:14:17Z | https://spherical-codes.org/ | 200 | 4668624 | c9b6cbda3999e093af0dfc96c62c8c256771508892b7c8ad2cb06688dc832ee9 | work-novelty/index.html |
| 2026-10-25T00:14:19Z | https://spherical-codes.org/plain | 200 | 377860 | b46c6a6bee5f5514540d176e8e43a804004ec28b0724c1b022bfc2c03a316b6b | work-novelty/plain.csv |

Both responses are the real table and not a challenge page (title "Table of spherical codes", 15301 /plain lines). The results are in work-novelty/rows_live.out, from my own parser work-novelty/rows.py.

- Index row (6, 575), verbatim: `<td>6</td> <td><a href="/data/6/575">575</a></td> <td>0.792780236785</td> <td>Pavlos Moros, 2026.</td>`. It has no `&ast;` (star False) and does not contain "needs more optimization".
- /plain line: `6,575,0.792780236785`.
- Propagated bar: 1753 rows have d' <= 6 and N' >= 575 across the index and /plain. The minimum cosine is the (6, 575) row itself, 0.792780236785, in both the index and /plain. Index and /plain agree on every such row they share; only (6, 990) is index-only.
- Compared with the claim-moment pages (inputs/table/), the only /plain change is at (18, 783) and (18, 784) (work-novelty/plain_diff_vs_claimmoment.out). Every row with d' <= 6 and N' >= 575 is unchanged (work-novelty/rows_diff.out).

## 2. c* recomputed (work-novelty/cstar.py, output work-novelty/cstar_claim.out)

- The file has 575 points with 6 coordinates each, every coordinate written with 26 significant digits.
- Every vector was normalised and all 165025 pairs computed in mpmath at 50 digits. Result: c* = 0.792679835684486880498265789805 at pair (387, 496), 0-based. This matches the claim's 0.7926798356844868804983.
- 2801 pairs lie within 1e-14 of c*.
- bar - c* = 0.00010040110051312 >= 1e-10: True.
- Exact-rational check against 0.792780236785 - 1e-10: I checked exactly the 3039 pairs whose float cosine exceeds that value minus 1e-3; the remaining pairs clear it by a float margin of at least 1.0046e-3. Result: every pair passes (True).
- Control: the posted table code (inputs/posted_6_575.txt) has a float max cosine of 0.792780236784080 (work-novelty/posted_float.out), consistent with the table's 12-decimal value 0.792780236785.

## 3. Literature, last 24 months (since 2024-10-25)

My own arXiv API searches are logged in work-novelty/fetch.log, and the window listing is in work-novelty/arxiv_list.out and work-novelty/arxiv_list_packing.out.

| search | time | HTTP | totalResults |
|---|---|---|---|
| all:"spherical code" OR all:"spherical codes" (max 200; all 154 returned, oldest 2002) | 00:15:47Z | 200 | 154 |
| all:Tammes (200 newest, back to 2020-05-19) | 00:15:52Z | 200 | 474 |
| (spherical code(s) OR Tammes OR "kissing number") AND all:575 | 00:15:58Z | 200 | 0 |
| abstract phrases ("table of spherical codes", "spherical cap packing", ...) | 00:16:06Z | 200 | 2 |
| abs:sphere AND packing AND points AND (angle OR angular OR cosine) | 00:16:39Z | 200 | 10 (2 in window, unrelated) |
| id_list of the 6 papers the claim names | 00:16:16Z | 200 | 6 |

- None of the in-window entries mentions 575.
- The only dimension-6 flag is 2606.18984, a kissing arrangement in R^12.
- The in-window spherical-code entries are bounds (Delsarte rate 2610.21263, SDP and complete-positivity hierarchies 2609.34845 and 2309.13854v4), communications or ML uses, T-avoiding codes from lattices, noncommutative codes, ImprovEvolve (d = 8..16), PackingStar (kissing numbers) and 2610.19988.
- Latest versions are unchanged from the claim's reads: 2610.19988v1, 2602.10233v2, 2511.13391v5, 2512.25037v2, 2606.18984v2 and 2411.16038v1 (work-novelty/arxiv_ids_versions.out).
- In the claim's saved HTMLs, every "575" in ImprovEvolve sits inside digits of other numbers (for example 0.65575 at D = 9, N = 838). PackingStar's single "575" is K(16, 3/8) >= 575, a dimension-16 bound (work-novelty/html_575_context.out).

arXiv:2610.19988 (Vahteristo): I re-read the Zenodo record https://zenodo.org/api/records/23270586 once, at 2026-10-25T00:16:57Z (HTTP 200, sha256 e53194a2dcea1eb710a790e21af8067afba1c8558b9d508b730a345c4f410c9c). It shows version 1.0, relations.version index 0 with is_last True, and it is byte-identical to the claim's copy (work-novelty/zenodo_summary.out).

The md5 sums of the claim's combined, per_instance and global JSON files all match the record. For (D = 6, N = 575) the three tables give the following (work-novelty/vahteristo.out):

| table | cos at (6, 575) |
|---|---|
| combined | 0.7932289977343617 |
| per_instance | 0.7932322927113262 |
| global | 0.7932389659189362 |

In each table the minimum over D <= 6 and N >= 575 (1800 entries) is the (6, 575) entry, and 0 entries have cos <= c* + 1e-10.

## 4. Repository checks

- TROPHY_CASE.md (raw main branch, 2026-10-25T00:17:21Z, HTTP 200, sha256 b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1): 0 lines match spherical, 575, Cohn or Tammes (work-novelty/trophy_grep.out). It lists no spherical-code results.
- Pull requests, from plain GitHub API requests (work-novelty/fetch.log): open pages 1-4 returned 100, 100, 100 and 43 PRs, page 5 was empty (2 bytes), all HTTP 200; closed page 1 returned 100, HTTP 200. Scan output: work-novelty/prs_open_scan.out and work-novelty/prs_closed_scan.out.
  - Open PRs for spherical-codes-cohn-table claim other rows: (25, 650), (25, 651), (31, 65), (30, 64), (30, 62), (29, 60), (28, 59), (27, 56), (6, 526), and 24 rows in d = 7.
  - No open or closed PR claims (6, 575) or mentions 575 together with dimension 6. (6, 526) cannot give a 575-point code, and d = 7 codes do not embed in R^6.

## 5. Caveats

- The improvement is a local polish of Pavlos Moros's posted code; the claim discloses and credits this.
- The table is live and edited during the day. My fetch, 00:14:17Z, is about 10 minutes after the claim moment and shows the same (6, 575) row.
- Not checked: uploads not yet posted to the table, and literature outside arXiv beyond the Zenodo record and repository checks above.

pass: true
