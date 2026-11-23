context: subagent (fresh context, spawned as the argue-against skeptic)
# NOVELTY / ARGUE-AGAINST verdict — V3R1T4S N=4405 claim

Role: skeptic. All numbers below are from my own code (fresh script
`novelty_check.py`, float64 numpy, blocked pairwise computation) and my
own live curl fetches (UA `V3R1T4S-novelty-judge`, 2026-11-23 ~02:20 MST).
I did not read the run's panel files or reuse its checker.

## Claim under attack

- Candidate: `attempts/deep-polish-4405/output/polished01.txt`, 4405 centers
- Claimed: feasible radius r* exceeds Packomania cci table N=4405 by +3.607e-06
- Live bar (12-dec): 0.014190212053; archived bar (30-dec):
  0.014190212052536014904153227050

## Attack 1 — NON-ISOMETRY (sorted pairwise-distance multisets)

Independent computation, 9,699,810 pairs each, float64:

| quantity | candidate | posted seed |
|---|---|---|
| sha256 | 304553619c7866b38cec7895a662ea20470c9a9e9a7d9bf76d94e046d8a94bc6 | 98f2b10dfc1f0dda4e4bdf4ff9f892de95d5e95d3bd13ea6b8af62f5739df1a1 (matches claimed hash exactly) |
| rows | 4405, all finite | 4405 data rows (+5 `#` header lines) |
| min pairwise dist | 0.028387638752098755 | 0.028380424103908623 |
| min boundary gap (1−\|p\|) | 0.014196062090634509 | 0.014190212051976459 |
| r* = min(pair/2, boundary) | **0.014193819376049377** | 0.014190212051954311 |
| r* − live 12-dec bar | **+3.607323e-06** | −1.045688e-12 |
| r* − archived 30-dec bar | +3.607324e-06 | −5.817031e-13 |

Binding constraint for the candidate is the pairwise contact
(0.028387638752098755/2 = 0.014193819376049377), not the boundary
(0.014196062090634509) — the margin is a genuine interior improvement,
not a boundary rounding artifact.

Multiset comparison (sorted 9,699,810 pairwise distances, candidate vs seed):

- max |diff| = 2.426218e-03
- fraction differing by >1e-9 = 0.999999 (9,699,802 of 9,699,810)
- fraction differing by >1e-6 = 0.999456
- median |diff| = 4.289574e-04, mean |diff| = 4.574339e-04

The configurations are decisively NOT isometric — the distance multisets
differ almost everywhere, at the 1e-4 scale. **Attack 1 FAILS.**

Seed sanity check: the posted seed reproduces its own table row at rounding
level (margin −1.05e-12 vs the 12-decimal bar, consistent with 12-decimal
coordinates; the run's own 50-digit check gives −1.046e-12). The seed is
what it claims to be.

## Attack 2 — QUEUE (live pending-requests.html, HTTP 200, 12,856 bytes)

Page header date: 22-Nov-2026. Exactly two `cci`-category rows exist
(verified by grep on the raw HTML, lines 64 and 94):

- 15-Oct-2026, Vidit Patankar, cci, 193 new candidates, range **652–3943**
- 03-Nov-2026, Karl Desfontaines, cci, 487 new candidates, range **126–4141**

Neither range contains N=4405 (3943 < 4405; 4141 < 4405). The string
`4405` appears nowhere in the page. Other categories' ranges (csq up to
9996, ssp up to 100000, etc.) do not count, per the brief. **Attack 2 FAILS.**

## Attack 3 — HISTORY (live cci.html, HTTP 200, 1,020,094 bytes)

History-of-updates section (70 entries total). The newest entry is:

- **22-Nov-2026**: Eckard Specht wave, N=259..998 — matches the scout's
  newest. The two 21-Nov-2026 bundles (Patankar / Desfontaines) are also
  present. No entry newer than 22-Nov-2026 exists, and no update entry
  anywhere mentions N=4405.

Table situation: the live HTML results table has 2,691 N-rows, max N=3877
(largest 10: 3745, 3757, 3781, 3793, 3805, 3817, 3829, 3853, 3865, 3877);
N=4405 has no HTML row. The 15 raw occurrences of the substring `4405`
in cci.html are all false positives inside other numbers' decimals
(e.g. `0.063244050098`, `0.044055154599`).

Live radius.txt (HTTP 200, 53,613 bytes, 2,735 data rows, max N=5000):
row 2730 reads `4405  0.014190212053` — still the claimed value, and the
live file is byte-identical to the run's archived copy (`diff` empty).
**Attack 3 FAILS.**

## Attack 4 — FILE INTEGRITY / CHECKER

- Candidate file: sha256 304553619c… (above), 4405 lines / 4405 data rows,
  coordinates parse cleanly, all finite, max |p| = 0.98580393790936549.
- Seed file: sha256 matches the claimed value exactly; 4410 lines =
  5 `#` headers + 4405 data rows.
- Archived 30-decimal value confirmed independently: the 2026-11-22
  run's `radius30.txt` (2,735 rows, max N=5000) contains
  `4405  0.014190212052536014904153227050` — exactly the claimed value.
  (Note: this run's own `radius30.txt` is only the 2,691-row 12-decimal
  HTML-table extract, max N=3877 — it has no 4405 row, which is why the
  checker correctly uses `radius.txt` for the bar.)
- `checker.py` inspection (read-only, for flattering artifacts):
  - `feasible_radius` is the correct definition
    min(min_pair/2, 1 − max|c_i|), mpmath 50 digits, **no tolerance**.
  - `table_radius` reads `data/radius.txt` — verified byte-identical to
    the live file tonight; value 0.014190212053 for N=4405. The comment
    that the 12-decimal bar is the stricter one is correct (round12 is
    4.6e-13 higher than the 30-decimal value).
  - Beat threshold is margin ≥ 1e-11; the claimed margin (+3.607e-06)
    is ~360× that.
  - Selftest log (`data/selftest.log`) shows all four selftests passing,
    consistent with the code as read (30-dec cci100 reproduces to
    8.7e-31; 12-dec cci100 to 7.4e-15; multiset self-match; 1e-6
    perturbation collapses the margin to −4.659e-07).
  - No flattering artifact found: no wrong table value, no tolerance,
    no wrong N.
  - One observation, not a kill: `check()` itself does not run the
    isometry comparison — the docstring promises margin AND non-isometry,
    but only the margin is printed by `check()`; isometry is left to the
    panel. My independent multiset comparison above closes that gap and
    shows decisive non-isometry.

**Attack 4 FAILS.**

## Verdict

Every attack failed. The candidate is a genuinely different configuration
(multisets differ at the 1e-4 scale), its feasible radius exceeds both the
live 12-decimal bar and the archived 30-decimal bar by +3.607e-06, no
pending cci request covers N=4405, no history update touches N=4405 or
postdates 22-Nov-2026, the files are intact, and the checker is sound.

pass: true
