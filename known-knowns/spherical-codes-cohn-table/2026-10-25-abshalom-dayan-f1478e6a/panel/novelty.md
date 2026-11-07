role: novelty
context: subagent (Agent tool, fresh context, model claude-opus-5-5), saw only claim/ and its own fetches

# Novelty verdict: spherical-codes-cohn-table, (6, 256)

Bottom line: the claimed code beats the live (6, 256) row by 3.3246854559e-5. The row has no star and no
"needs more optimization" label. Nothing I could find (the live table with the propagated bar, arXiv:2610.19988's
three tables, arXiv searches over the last 24 months, TROPHY_CASE.md, and all open and closed pull requests)
reaches c*. injection_suspected: none (claim/ text files were scanned for instruction-like text and none was
found; claim/ was treated as data throughout).

## 1. Status source: one plain fetch each (work-novelty/fetch.log)

User-Agent "V3R1T4S-research-agent (honest single fetch)", one request per URL, no retries, no cookies. There were
no blocks or challenge pages.

| UTC time | URL | HTTP | bytes | sha256 | saved as |
|---|---|---|---|---|---|
| 2026-10-25T06:33:58Z | https://spherical-codes.org/ | 200 | 4668044 | 69a54be57593369dd9d36002a32107c342e0441b1c6298c2d3c5617a538472ea | work-novelty/index.html |
| 2026-10-25T06:34:00Z | https://spherical-codes.org/plain | 200 | 377006 | 7d965100bfb54727ec3eaa4ef7e23558b5c048eca94b6b6281b3f02c80669f62 | work-novelty/plain.csv |

Both sha256 values equal those of claim/ inputs/table/index.html and inputs/table/plain.csv
(work-novelty/claim_sha.out). The table is byte-identical to the claim-moment read (2026-10-25T06:26:36Z).

The (6, 256) row in my fetch (work-novelty/bar.out, work-novelty/index_row_6_256.html):
- /plain: `6,256,0.704931969352` (no minimal polynomial).
- HTML index: one row, cosine 0.704931969352, credited "Pavlos Moros, 2026.". There is no `&ast;` and no
  "needs more optimization" in the row. The only other index line containing "6/256" is the (26, 256) row.
- Index and /plain agree on every shared cosine (0 mismatches). The index has 90 rows that /plain lacks; of
  those, only (6, 990) has d' <= 6 and N' >= 256.

## 2. c*, computed independently (work-novelty/my_cstar.py, outputs in work-novelty/cstar*.out)

This is my own script, not the claim's checker. It normalises each of the 256 vectors in
object/code_6_256.txt (26 significant digits per coordinate) with mpmath at 50 digits and evaluates all 32640
pairs.
- c* = 0.704898722497441001473280277007, at pair (55, 247) (0-based). The second-largest value is
  0.7048987224974409985369538435522741725505, at pair (22, 30). This matches the claim's 0.7048987224974410014733.
- A numpy float64 cross-check gives a maximum of 0.7048987224974411, with 1331 pairs within 1e-12 of the maximum
  (work-novelty/cstar_numpy.out).
- Gain over the live row: 0.704931969352 - c* = 3.3246854559e-5, which is at least 1e-10.
- An exact rational check (Fractions from the decimal strings, squared comparison) finds every pair strictly
  below the bar 0.704931969352 - 1e-10, with 0 violations.
- Kissing clause: d = 6 lies outside 9..23, so the clause does not apply.

## 3. Propagated bar (work-novelty/my_bar.py, work-novelty/bar.out)

Deleting points or zero-padding means a (6, 256) claim must clear the minimum cosine over all rows with
d' <= 6 and N' >= 256.
- /plain: 2966 such rows. The minimum is (6, 256) itself at 0.704931969352; next come (6, 257) 0.705350637779
  and (6, 258) 0.705825097762. No row is at or below c* + 1e-10.
- HTML index: 2967 such rows, with the same minimum. No row is at or below c* + 1e-10.

## 4. arXiv:2610.19988 (Vahteristo) and its Zenodo data

- Zenodo record re-read once: https://zenodo.org/api/records/23270586 at 2026-10-25T06:35:18Z, HTTP 200,
  sha256 e53194a2dcea1eb710a790e21af8067afba1c8558b9d508b730a345c4f410c9c. The record is byte-identical to the
  claim's copy. It has version 1.0, relation index 0 with is_last True, and was created and updated on
  2026-10-14 (work-novelty/zenodo_check.out).
- The md5 sums of the saved tables in claim/inputs/arxiv_2610.19988/ match the record: combined
  a417aa84aad94965b411f0137875fc87, per_instance e4ca6b46f8a58eaa33627d809eb9c338, global
  5e589a279b2db9aa40e30326f6d9281c, README e28aecc8fa28740ab985eed8252d908b (work-novelty/zenodo_md5_local.out).
- My read of all three tables (work-novelty/vahteristo.out). Each has 29670 entries and 3076 entries with
  D <= 6 and N >= 256. In every table the minimum over those entries is the (6, 256) entry itself:

  | table | (6, 256) cos | margin above c* |
  |---|---|---|
  | combined | 0.7049931928409804 | 9.447034e-05 |
  | per_instance | 0.7050249538274573 | 1.262313e-04 |
  | global | 0.7053373293588499 | 4.386069e-04 |

  None of the three tables is at or below c* + 1e-10.
- My arXiv feed lists 2610.19988 as v1, updated 2026-10-14 (work-novelty/arxiv_read.out).

## 5. Literature, last 24 months (window from 2024-10-25)

Six arXiv API searches of my own, all sorted by lastUpdatedDate, so papers revised inside the window are included
too. Each was fetched once with HTTP 200; time and sha256 are in work-novelty/fetch.log, and the parse is in
work-novelty/my_arxiv.py and work-novelty/arxiv_read.out.

| feed | query | totalResults | returned | in window | oldest updated returned |
|---|---|---|---|---|---|
| q1 | "spherical code(s)" | 154 | 154 | 37 | 2002-03-06 |
| q2 | Tammes | 474 | 200 | 77 | 2020-08-12 |
| q3 | (spherical code, Tammes, kissing number or sphere packing) AND (256, dimension 6, six dimensions or six-dimensional) | 15 | 15 | 4 | 2006-05-07 |
| q4 | kissing number(s) or configuration(s) | 132 | 132 | 39 | 1994-05-13 |
| q5 | AlphaEvolve, FunSearch, OpenEvolve, ShinkaEvolve, LLM-guided or evolutionary coding agent, AND sphere, spherical, kissing or packing | 20 | 20 | 18 | 2023-11-22 |
| q6 | points on a sphere, spherical (cap) packing, AND minimal distance, angle, packing or Cohn | 27 | 27 | 8 | 1994-05-13 |

Every feed reaches back past the window start, so the window is fully covered for these queries. There are 169
unique in-window entries, and 13 were flagged for 256, dimension 6 or new codes. The 256 hits are 2411.04916 and
2603.10425, kissing numbers in dimensions 17 to 21 and 19, where 256 is the size of an improvement. The dimension-6
hits are 2606.18984 (R^12 arrangements built from 60-point blocks in R^6) and 2609.12640 (contact-graph polytopes,
dimensions 5 to 7). The "new codes" hits are 2610.19988 (section 4), kissing or Kakeya results in other dimensions
(2608.23691, 2606.10402, 2607.20359, 2608.13906), and circle-packing or unrelated work (2609.05093, 2609.25288,
2609.03736, 2601.18005). I read the abstracts of the discovery-system papers (work-novelty/abstracts_selected.txt).
None names a code in dimension 6 or lower with 256 or more points.
- ImprovEvolve (2602.10233v2, the claim's saved HTML; the sha256 matches the claim's record,
  work-novelty/lit_html_sha.out): my own parse finds 90 table rows, 10 each in d = 8..16, and none in d <= 6
  (work-novelty/improvevolve_rows.out).
- PackingStar (2511.13391v5, the claim's saved HTML): the named configurations in d <= 6 are (2, 6), (4, 9),
  (4, 24), (6, 27), (6, 54), (6, 60) and (6, 72), so at most 72 points. "Tammes" does not occur
  (work-novelty/packingstar_check.out).

## 6. This repo: TROPHY_CASE.md and pull requests

- TROPHY_CASE.md (https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md,
  2026-10-25T06:37:14Z, HTTP 200, sha256 b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1):
  0 matches each for "spherical", "cohn", "tammes", "kissing", "packing", "6, 256" and "6,256"
  (work-novelty/trophy_grep.out). It has no spherical-code row.
- Open pull requests, pages 1 to 5 (2026-10-25T06:37:32Z to 06:37:58Z, all HTTP 200): 100, 100, 100 and 48 PRs,
  then page 5 empty (`[]`). Closed pull requests, page 1 as instructed, plus pages 2 to 4 for full coverage
  (06:38:03Z to 06:39:02Z, all HTTP 200): 100, 100, 100 and 48 PRs. That is 696 unique PRs scanned
  (work-novelty/my_prs.py, work-novelty/prs_all.out).
- 23 PRs mention spherical codes or Cohn (work-novelty/prs_spherical_list.out). None claims (6, 256); the regex for
  (6, 256), 6_256 and 6x256 had 0 hits. The only pairs with d' <= 6 and N' >= 256 named in any PR title or body are
  (6, 525), (6, 526) and (6, 527), in #231 (closed) and #364 (open). Their claimed values are
  c* = 0.786430618545 and 0.786427532330, far above c*, so deleting points from those codes cannot reach c*.

## Decision

| condition | result |
|---|---|
| c* beats the live row by at least 1e-10 | yes: gain 3.3246854559e-5; exact check passes at the bar (row - 1e-10) |
| live row unstarred and unlabelled | yes (fetch 2026-10-25T06:33:58Z, byte-identical to the claim-moment read) |
| nothing known reaches c* (table with propagated bar, 2610.19988 in all three tables, ImprovEvolve, PackingStar, arXiv 24 months, TROPHY_CASE, PRs) | yes: the nearest is the table row itself, 3.32e-5 above c* |
| tie? | no: strictly lower |

Limits:
- Most in-window papers were judged by title and abstract only.
- Venues outside arXiv were not searched; examples are the SSRN preprint behind the earlier (6, 256) row and
  live agent leaderboards such as EinsteinArena. The SSRN preprint's (6, 256) value is in any case above the
  current row according to 2610.19988's snapshots.
- The gain comes from a local polish of the posted code, which the claim discloses and credits. That does not
  change the novelty: the polished code strictly beats every value known.

pass: true
