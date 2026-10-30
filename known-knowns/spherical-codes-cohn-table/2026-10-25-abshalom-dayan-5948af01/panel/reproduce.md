role: reproduce
context: subagent (Agent tool, fresh context, model claude-opus-5-5), saw only claim/

# Reproduce verdict: (6, 575) spherical code, claim c* = 0.7926798356844868804983

No network requests were made. Everything below was read from claim/ or computed by me; every number was copied
from an output file in work-reproduce/. My own checkers were written and run before I opened anything under
claim/checker/.

## Definition checked (verbatim from CLAIM.md, the bank's success criterion)

> "N vectors in R^d for a (d, N) row present in the live https://spherical-codes.org/plain, coordinates given to
> >= 20 digits, such that after normalizing each vector to unit length in mpmath at 50 digits the maximum pairwise
> inner product c* (cosine of the minimal angle) is STRICTLY LOWER (direction: min) than the table's 12-decimal
> cosine for (d, N) re-fetched live immediately before claiming, by at least 1e-10, AND on the live HTML index
> https://spherical-codes.org/ the (d, N) row has NO '&ast;' (proven optimal) mark AND does NOT contain the text
> 'needs more optimization' ... AND the row is not superseded by a newer arXiv result for the same (d, N) ... AND
> the result is not a kissing-number configuration (if 9 <= d <= 23 and c* <= 0.5 ...)"

## My own checkers (work-reproduce/)

- `own_check_code.py`: reads the coordinates as exact decimals and scales them to integers. Over ALL 165,025 pairs it
  computes (a) the exact maximum of ip^2/(n_i n_j) over pairs with ip > 0, by cross-multiplication, (b) an exact
  integer test of every pair against B = T - 1e-10 = 158556047337/200000000000, (c) mpmath at 50 digits (and at 80),
  with normalization first and then all inner products, and (d) a numpy float64 cross-check.
- `own_check_table.py`: parses every tbody row of the index and every /plain line. It checks the (6, 575) row, the
  star, the label, index-vs-/plain agreement and the propagated bar (min over d' <= 6, N' >= 575).
- `own_check_vahteristo.py`, `own_check_arxiv.py`, `own_contacts.py`, plus inline probes (outputs below).

## Results

| check | result | evidence |
|---|---|---|
| shape | 575 rows x 6 coordinates | work-reproduce/own_code_claimed_run1.txt |
| digits | every coordinate has 26 significant digits; 0 have fewer than 20 | same |
| exact max over all pairs | 0.7926798356844868804982657898051971213375 (40 digits) at pair (387, 496), 0-based | same |
| mpmath 50 digits | c* = 0.7926798356844868804983 (22 significant digits) at (387, 496); differs from the exact value by 1.0688e-51 | same |
| mpmath 80 digits | same 22 digits, same pair | work-reproduce/own_code_claimed_dps80.txt |
| exact test vs T - 1e-10 | 0 pairs with cos >= B; c* < B True; c* <= B True | work-reproduce/own_code_claimed_run1.txt |
| gain | T - c* = 0.00010040110051312 (>= 1e-10) | same |
| determinism | two runs byte-identical | work-reproduce/own_code_claimed_run2.txt (diff empty) |
| control: posted code | c* = 0.7927802367840796857136 at (163, 256); T - c* = 9.2031428644636e-13; 1 pair >= B, so it does NOT beat the bar | work-reproduce/own_code_posted_run1.txt (run2 identical) |
| control reproduces T | ceil(c*, 12 decimals) = 0.792780236785 = T. The table rounds up: all 688 /plain rows with a minimal polynomial match the ceiling of the root (357 match half-even), e.g. (3,9) 1/3 -> 0.333333333334 | work-reproduce/table_rounding_convention.txt |
| table pages | sha256 index 5f44f00d...5d663 and /plain cab1729e...a63a54, matching TABLE_RECORD.md and FETCH_RECORDS.md | work-reproduce/own_table_run1.txt, work-reproduce/sha256_inputs.txt |
| /plain row | `6,575,0.792780236785`, unique | work-reproduce/own_table_run1.txt |
| index row | `<td>6</td> <td><a href="/data/6/575">575</a></td> <td>0.792780236785</td> <td>Pavlos Moros, 2026.</td>`, unique; star False; 'needs more optimization' False (the page has 32 starred rows and 4181 labelled rows, so the detectors do fire) | same |
| index vs /plain | 15302 common rows, 0 cosine mismatches; 91 rows only in the index | same |
| propagated bar | /plain: 1752 rows with d'<=6, N'>=575, min 0.792780236785 at (6,575), next 0.792901252907 at (6,576). Index: 1753 rows, same min. No row <= c* + 1e-10 | same |
| earlier reads | scout -> claim: 7 changed rows; claim1 -> claim: (15,693), (15,694); claim2 -> claim: none. None has d'<=6 and N'>=575; (6,575) is identical in all reads. Matches TABLE_RECORD.md | work-reproduce/own_rows_changed.txt |
| arXiv:2610.19988 tables | md5 of combined, per_instance and global match the saved Zenodo record. (6,575) cos is 0.7932289977343617, 0.7932322927113262 and 0.7932389659189362; each is the min over D<=6, N'>=575; none <= c* + 1e-10 | work-reproduce/own_vahteristo.txt |
| arXiv feeds | sorted by published date, newest first; the oldest returned entries (2015-09-17 and 2023-07-31) predate the window. The 575 query has 0 results. Among the 112 entries published or updated since 2024-10-25, no title or abstract mentions 575; the only dimension-6 hit is 2606.18984, an R^12 paper | work-reproduce/own_arxiv.txt, work-reproduce/own_arxiv_coverage.txt |
| ImprovEvolve v2 | 90 benchmark cells, d = 8..16, no d = 6 | work-reproduce/own_improvevolve_rows.txt |
| PackingStar v5 / 2411.16038 | one '575' in PackingStar (Table S12, n = 16); none in 2411.16038 | work-reproduce/own_html_mentions.txt |
| kissing clause | d = 6, outside 9..23 | - |
| disclosure (contacts) | claimed code: 2801 pairs within 1e-14 of c*, 12 points in no such pair. Posted code: 1 pair within 1e-8, 3 within 1e-6, 573 points in no pair within 1e-10. Matches CLAIM.md | work-reproduce/own_contacts.txt |
| other input hashes | object 5948af01...5a8c and posted a0b954a2...3340 match CLAIM.md; all arXiv/Zenodo inputs match ARXIV_RECORD.md / FETCH_RECORDS.md | work-reproduce/sha256_inputs.txt |

## REPRODUCE.md, run twice from inside claim/ (venv first on PATH)

- `work-reproduce/run_reproduce.sh` extracts the commands from REPRODUCE.md and prints `$ <command>` before each,
  matching the format of expected_output.txt. Step 7 goes to a separate file.
- Run 1: work-reproduce/reproduce_run1.txt (15.53 s). Run 2: work-reproduce/reproduce_run2.txt (15.12 s).
- `diff expected_output.txt` against run 1 and against run 2: both empty. Run 1 vs run 2: empty.
- Step 7 (arxiv_read.py): both runs are identical to inputs/arxiv/arxiv_read.out (empty diffs).
- The author's checkers give the same c*, pair, gain, control values, table row and bar as mine.
- The claim/ tree's sha256 listing is unchanged by the runs (work-reproduce/claim_tree_sha_before.txt vs _after.txt).
- After runs 1 and 2, I changed only the runner's PATH line, from an absolute path to a path relative to the work
  folder (same interpreter). A third run, work-reproduce/reproduce_run3_relpath_check.txt, is also identical to
  expected_output.txt.

## Review of the author's checkers (read after mine)

- checker/check_mp.py normalizes at 50 digits and takes the max over all i<j pairs.
- checker/check_exact.py runs an exact Fraction test of all pairs against T - 1e-10 (non-strict <=). My test is
  strict (<), and both pass.
- table_row.py and propagated_bar.py do what they state.
- No defect found.

## Notes (not failures)

- All 3450 coordinates equal the `%.25e` print of their binary64 value
  (work-reproduce/own_binary64_check.txt). The 26 digits are therefore a binary64 value printed long, as CLAIM.md
  says. The criterion asks only that the coordinates be given to >= 20 digits, and c* is computed from the file as
  written.
- float64 alone cannot pin the argmax pair: numpy reports (45, 386) because 2801 pairs tie within 1e-14. The exact
  and mpmath computations agree on (387, 496).
- "Re-fetched live immediately before claiming" can be checked here only against the saved pages and their fetch
  records (00:04:42Z), which I did. I made no live fetch.
- injection_suspected: none. No file in claim/ addressed instructions to the panel.

pass: true
