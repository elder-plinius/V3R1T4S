context: subagent (fresh context, spawned as the criterion skeptic)
# CRITERION verdict — N=4405, polished01.txt (2026-11-23 run)

Judge: independent criterion skeptic. Own code only
(`v3judge/judge_recompute.py`, mpmath 50 digits + numpy float64
screening). The run's `checker.py` was NOT read or reused; the run's
`check50_polished01.log` was NOT read. All Packomania pages re-fetched
live by this judge with UA `V3R1T4S-criterion-judge`.

## Claim file
- `runs/2026-11-23-0200/attempts/deep-polish-4405/output/polished01.txt`
- sha256: `304553619c7866b38cec7895a662ea20470c9a9e9a7d9bf76d94e046d8a94bc6`
- 4405 data rows, indices 1..4405, 30-decimal coordinates.
- Posted seed `runs/2026-11-23-0200/data/cci4405.txt`
  sha256 `98f2b10dfc1f0dda4e4bdf4ff9f892de95d5e95d3bd13ea6b8af62f5739df1a1`
  (matches PREREG).

## Live fetches (this judge, 2026-11-23 ~02:17 MST)
| page | URL | sha256 | vs scout copy |
|---|---|---|---|
| radius.txt | https://packomania.com/cci/txt/radius.txt | `bbbf290022342473e79e5e465f939f020f6fe97d0c69ea904599e2463293d4a7` | BYTE-IDENTICAL |
| cci.html | https://packomania.com/cci/ | `8a984a6111c2f142edc1b43b58697c77e75a90a268dcc952dc175dc94962d904` | BYTE-IDENTICAL |
| pending-requests.html | https://packomania.com/pending-requests.html | `43140abeddb1a0cd14ba6f19fb6a25198624d01da6dc5bc93074520b75b5cfca` | BYTE-IDENTICAL |
| cci4405.txt | https://packomania.com/cci/txt/cci4405.txt | `98f2b10dfc1f0dda4e4bdf4ff9f892de95d5e95d3bd13ea6b8af62f5739df1a1` | BYTE-IDENTICAL to posted seed |

Note: `https://packomania.com/cci/pending-requests.html` 404s; the live
pending page sits at the site root (`/pending-requests.html`), as the
scout used. Live radius.txt line 2730: `4405 0.014190212053` — the
operative 12-decimal bar. Live HTML table ends at N=3877 (largest row
seen); no row for 4405.

## (a) Radius at 50 digits — PASS
- Float64 screening of all 9,699,810 pairs: min pair distance/2 =
  0.014193819376049377, pair (4129, 4393); max |c| = 0.9858039379093655
  (index 4393) -> boundary term 1-max|c| = 0.01419606209063451.
- 50-digit recompute of all 9 terms within 2e-9 (float64) of the
  minimum, plus the 5 largest-|c| boundary terms, directly from the
  raw decimal strings. Lowest 50-digit terms:
  - pair (4129, 4393): 0.01419381937604937731901147206751 (binding)
  - pair (3895, 4129): 0.01419399336524014060614088844691
  - boundary (4393):  0.01419606209063444555312875054406
- **r\* = 0.01419381937604937731901147206751**, binding pair (4129, 4393).
  Gap to the next term: 1.739891908e-07.
- Coverage: float64 distance error is ~1e-17 absolute here; the 2e-9
  collection window is ~100x smaller than the 1.74e-07 gap to the next
  term, and the nearest boundary term sits 2.24e-06 above r\*. No term
  could have been missed.
- **margin r\* - r_table = +3.607323049e-06** vs live bar 0.014190212053.
  Bar is 1e-11; margin clears it by a factor of ~360,732.
- Claimed margin +3.607e-06 (lens report, double precision, recomputed
  from the saved file) agrees with my 50-digit value to its printed
  precision (difference -3.2e-10 is the claim's 4-significant-figure
  rounding, not a discrepancy).

## (b) Non-isometry vs posted seed — PASS
- Full sorted pairwise-distance multisets (9,699,810 distances each),
  computed independently for claim and seed:
  - max |difference| = 0.0024262175482762383 (sorted rank 302540)
  - median |difference| = 0.0004289574008948249
  - entries differing by >1e-9: 9,699,802 of 9,699,810
  - entries differing by >1e-12: all 9,699,810
- The multisets differ overwhelmingly: the configuration is NOT
  isometric to the posted seed. (The seed is 12-decimal, so isometry
  would have shown agreement to ~1e-12; observed differences are
  ~1e-3.)

## (c) No newer History-of-updates line for N=4405 — PASS
- Live cci.html is byte-identical to the scout copy, so NO history line
  newer than the scout exists at all. Independently confirmed: the
  string `4405` does not occur anywhere in the History-of-updates
  section (the 15 `4405` hits in the full page are digit substrings
  inside other rows' radius values, e.g. 0.044055154599).
- Newest entries remain: 22-Nov-2026 Specht wave (N=259..998) and the
  21-Nov-2026 Patankar/Desfontaines bundles (N up to ~1586 in the
  listed ranges). None lists N=4405. Last update: 22-Nov-2026.

## (d) N outside every live cci pending range — PASS
- Live pending page (byte-identical to scout): the only cci lines are
  Vidit Patankar 652–3943 (15-Oct-2026) and Karl Desfontaines 126–4141
  (03-Nov-2026). 4405 is outside both.

## 12-decimal vs 30-decimal table subtlety
- Live 12-decimal bar: 0.014190212053. Archived 30-decimal value
  (PREREG): 0.014190212052536014904153227050. Live minus archived =
  +4.63985e-13: the live bar is HIGHER, i.e. stricter, as the PREREG
  states. (The archived value itself is taken from the PREREG; the
  archived `data/radius30.txt` is 12-decimal and carries no N=4405 row,
  so it cannot independently confirm the 30-decimal figure — but it
  does not need to: the operative bar is the live value, verified
  directly from live radius.txt.)
- Margin vs the archived value would be +3.607323513e-06 — also far
  above the 1e-11 bar. The claim clears the stricter live bar.
- `mp.nstr(..., 31)` printing: values were compared at full 50-digit
  precision internally; 31-significant-digit printing truncates at
  ~1e-31 relative (~1e-33 absolute at these magnitudes), 22 orders of
  magnitude below the 1e-11 bar. It leaves no gap that could matter.
  (The 2026-11-18 lesson concerned float-rounded %.30f prints, ~7e-19
  off; mp.nstr from a true 50-digit value is far tighter, and the
  margin here is 3.6e-06, not borderline.)

## Scope guard — SATISFIED
- One carrier: polished01.txt only. The lens report states polished03
  (+2.038e-06, also above the bar) "stays banked, not bundled (scope
  guard: one carrier per claim)". No 2026-11-23 outbox package exists
  yet (outbox ends at 2026-11-20), so nothing has been bundled; the
  packaging step must still carry only polished01.
- Narrow-walk condition: the verified above-bar claim supersedes the
  walk per the PREREG; the lens report records the walk as not run.
  Consistent.

## Margin-reporting rule — SATISFIED
- The reported margin (+3.607e-06) is recomputed from the saved file,
  and my independent recompute from the same saved file reproduces it
  (+3.607323049e-06). No tracked value was carried through unrecomputed.

## Verdict
- (a) PASS — margin +3.607323049e-06 >= 1e-11 (factor ~360,732).
- (b) PASS — sorted pairwise-distance multisets differ decisively.
- (c) PASS — no newer history line; no 4405 in the updates section.
- (d) PASS — 4405 outside Patankar 652–3943 and Karl 126–4141.
- Scope guard and margin-reporting rule both satisfied.

pass: true
