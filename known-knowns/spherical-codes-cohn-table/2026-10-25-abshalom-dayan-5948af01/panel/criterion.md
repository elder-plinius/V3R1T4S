role: criterion
context: subagent (Agent tool, fresh context, model claude-opus-5-5), saw only claim/

# Criterion verdict: spherical-codes-cohn-table, (d, N) = (6, 575)

Bottom line: on a literal reading, every conjunct of the success criterion holds on the files saved in claim/. I wrote my
own checks first (work-criterion/my_cstar.py, my_table.py, my_arxiv.py, my_vahteristo.py) and ran the claim's checkers
only afterwards (work-criterion/claim_checkers.out). The two agree on every number. No network requests were made.
Verdict written at 2026-10-25T00:25:44Z (work-criterion/verdict_time.out).

injection_suspected: none (case-insensitive scan of the claim's text files, checkers, object and /plain found no
instruction-like text; work-criterion/misc_checks.out, grep exit 1)

## Conjunct by conjunct

| # | conjunct (criterion wording) | verdict | evidence (my own output unless noted) |
|---|---|---|---|
| 1 | (d, N) row present in the live /plain | holds for the saved claim-moment /plain | `6,575,0.792780236785` in inputs/table/plain.csv; 15302 rows, 0 duplicate keys; the cosine has 12 decimals (work-criterion/my_table.out) |
| 2 | coordinates given to >= 20 digits | holds | 575 lines x 6 tokens = 3450 coordinates, every one with 26 significant digits (min 26, max 26, 0 below 20); every token equals `%.25e` of its binary64 value, as CLAIM.md says (work-criterion/my_cstar_object.out, misc_checks.out). c* is computed from the decimals as written |
| 3 | c* after normalising in mpmath at 50 digits | holds | c* = 0.7926798356844868804982657898051971213375 at pair (387, 496) (0-based), all 165025 pairs at mp.dps = 50; to 22 significant digits 0.7926798356844868804983, the value CLAIM.md states (my_cstar_object.out) |
| 4 | STRICTLY LOWER than the table's 12-decimal cosine by at least 1e-10 | holds | 0.792780236785 - c* = 0.00010040110051311950173 >= 1e-10. Exact rationals, no square roots: the 3039 pairs with double-precision cosine above 0.792780236785 - 1e-3 all satisfy <x,y>^2 < B^2 |x|^2 |y|^2 with B = 0.792780236785 - 1e-10; the largest double-precision cosine among the other pairs is 0.7917756107121842 (my_cstar_object.out) |
| 5 | HTML index row has NO '&ast;' | holds for the saved claim-moment index | 1 index row for (6, 575): `<td>6</td> <td><a href="/data/6/575">575</a></td> <td>0.792780236785</td> <td>Pavlos Moros, 2026.</td>`; no `&ast;`, `*`, `&#42;` or U+2217 in it. Null model for the detector: the same parser finds 32 starred rows (page count of `&ast;` is 33, the extra one in the legend), first (3, 7) (my_table.out) |
| 6 | row does NOT contain 'needs more optimization' | holds for the saved claim-moment index | not in the row (nor 'optimiz', 'converg'); the same parser finds the label on 4181 other rows (page count 4182, the extra one in the legend) (my_table.out) |
| 7 | not superseded by a newer arXiv result for (6, 575) | holds within what the saved files can show (limits below) | arXiv:2610.19988, the only saved paper covering (6, 575): md5 of all three Zenodo tables matches the record; (6, 575) cos = 0.7932289977343617 (combined), 0.7932322927113262 (per_instance), 0.7932389659189362 (global), all above the table and above c*; each table's minimum over D <= 6, N' >= 575 (1800 entries) is that (6, 575) entry, none at or below c* + 1e-10 (work-criterion/my_vahteristo.out). Saved feeds: 112 distinct entries published or revised on or after 2024-10-24; my regex finds '575' in none; the only 'dimension 6' hit is 2606.18984 (kissing arrangements in R^12); the 'new codes' hits are 2610.19988, 2602.10233 (ImprovEvolve, cells only in d = 8..16 per the claim's checker), 2609.25288 (Rado's covering problem) and 2609.03736 (binary-code LP bound), none a (6, 575) code (work-criterion/my_arxiv.out, abstracts.out). PackingStar's 6-dimensional configurations are 6d27k3, 6d54k1, 6d60k1, 6d72k1, and its one '575' is K(16, 3/8) in Table S12 (work-criterion/papers_575.out). 2411.16038 full text has no '575' (papers_575.out) |
| 8 | not a kissing configuration (9 <= d <= 23 and c* <= 0.5) | holds | d = 6 is outside 9..23, and c* is about 0.7927 > 0.5 |
| 9 | propagated bar d' <= 6, N' >= 575 | holds | /plain: 1752 such rows, minimum is (6, 575) itself at 0.792780236785, next (6, 576) 0.792901252907; HTML index: 1753 rows, same minimum; no row at or below c* + 1e-10; the best row with d' < 6 is (5, 575) at 0.868336821301 (my_table.out). Same result in arXiv:2610.19988's three tables (conjunct 7) |
| 10 | table cosine "re-fetched live immediately before claiming" | holds, on self-reported fetch times consistent with file times | TABLE_RECORD.md and FETCH_RECORDS.md give 2026-10-25T00:04:42Z (index, sha256 5f44f00d...) and 00:04:44Z (/plain, sha256 cab1729e...); the saved files hash to those values (work-criterion/hashes_and_stats.txt). File mtimes: inputs/table/index.html and plain.csv 00:04:45Z, the five claim .md files 00:04:47Z, inputs/arxiv/arxiv_read.out 00:05:01Z, expected_output.txt 00:05:02Z; the other 30 files all predate 00:04:42Z (object 2026-10-24T23:24:07Z, last checker edit 00:01:23Z, last input 00:01:41Z) (work-criterion/times.out, misc_checks.out). The claim-moment pages are byte-identical to the 23:45:04Z read (same sha256), and claim/'s rows_changed.py finds 0 changed rows between them |

Control (null model for the gain): the posted table code inputs/posted_6_575.txt has c* =
0.792780236784079685713553639621036420522 at pair (163, 256), which is 9.2031428644636037896e-13 below 0.792780236785
(less than 1e-10), and the exact check fails at (163, 256) (work-criterion/my_cstar_posted.out). The table rounds upward
to 12 decimals (e.g. /plain lists (3, 9) as 0.333333333334 for cosine 1/3), so the posted code reproduces the row and
does not clear the bar; the claimed code does. A second baseline, arXiv:2610.19988's dedicated per-instance annealing,
stays above both the table and c* (conjunct 7).

## Hidden quantifiers and stretched definitions

- "flags as unconverged" (partial win p2): the criterion makes this the literal text 'needs more optimization' on the
  live row, and the claim-moment row does not carry it, so on the criterion's wording this is a claim, not p2. In
  substance the posted code was unconverged: only 1 pair lies within 1e-14 of its maximum, against 2801 for the
  claimed code (my_cstar_posted.out, my_cstar_object.out), and arXiv:2610.19988's snapshot of 2026-09-23 shows the earlier
  (6, 575) entry 0.795870898081 as "Henry Cohn, 2026, needs more optimization." (my_vahteristo.out). The gain comes
  from a local polish of an unlabelled entry that had not converged. A reader who goes by the spirit of p2 rather
  than its wording could object; I decide literally.
- "coordinates given to >= 20 digits": the 26 digits are binary64 values expanded with `%.25e`, so beyond about 17
  digits they carry no extra optimisation precision. The criterion asks only for the digits given, and c* is computed
  from the file as written, so this is not a stretch.
- "N vectors": 575 distinct rows (my_cstar_object.out). CLAIM.md says 12 of them are rattlers; that does not affect
  the maximum cosine.

## What the saved files cannot show

- The row's live state after 2026-10-25T00:04:44Z. The table is edited during the day: 7 rows changed between
  22:54:03Z and 00:04:42Z, none with d' <= 6 and N' >= 575 (claim checker, claim_checkers.out). I made no fetch.
- The fetch times themselves: the log (data/live_fetch.log) is not in claim/. The times are self-reported and agree
  with the file mtimes and the recorded sha256.
- arXiv coverage: the feeds are keyword searches over metadata ("spherical code(s)", "Tammes", and those AND 575), as
  the criterion prescribes. They miss papers that post codes under other words (sphere packing, point
  configurations, Riesz or Thomson energy) without those terms, and they are truncated: 100 of 154 results (oldest
  returned first submitted 2015-09-17) and 100 of 474 (oldest 2023-07-31). So an older paper revised recently
  outside those 100 is not covered. Full texts were read only for 2610.19988 (its tables), 2602.10233, 2511.13391v5
  and 2411.16038v1. The feeds were fetched 2026-10-24T22:57:47Z to 23:02:12Z (self-reported), before the table read,
  on a Saturday (work-criterion/times.out).
- arXiv:2610.19988's `cos` values are the author's double-precision maxima; its coordinate files were not saved. The
  margins (at least 5.491620e-04 above c*, claim_checkers.out) are far beyond double-precision error.

confirmed_scope: The 575 vectors in object/code_6_575.txt (26 significant digits per coordinate), each normalised in mpmath at 50 digits, have maximum pairwise cosine c* = 0.7926798356844868804983 (22 significant digits), which is 0.00010040110051 (at least 1e-10, confirmed with exact rationals) below the cosine 0.792780236785 of the (6, 575) row in the /plain and HTML index pages saved in claim/ (logged as fetched at 2026-10-25T00:04:42Z and 00:04:44Z, 3 to 5 seconds before the claim files were written at 00:04:47Z), a row that in those saved pages has no '&ast;' and no 'needs more optimization', is the lowest of all listed rows with d' <= 6 and N' >= 575, and is not matched at or below c* by arXiv:2610.19988's three tables or by any paper in the saved arXiv keyword feeds; not confirmed are the row's live state after that fetch, the fetch times beyond their agreement with file times and sha256, and arXiv papers outside those keyword feeds.

pass: true
