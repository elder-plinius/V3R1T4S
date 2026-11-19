context: subagent (fresh context, spawned as the argue-against skeptic)

# ARGUE-AGAINST report — N=4315 claim, carrier polished00.txt
Skeptic lens, V3R1T4S run 2026-11-17-0200. Task received 03:20 MST, report
written 03:29 MST (~9 min wall time). All code written fresh by this lens
(fresh scripts written for this lens); no reuse of
panel/verify_claim.py or code/checker.py. All live fetches with UA
"V3R1T4S-skeptic". Nothing sent outward; verification only.

Claim under attack: polished00.txt, 4315 centers, claimed r* =
0.014324547770692870607422975127, margin +1.006e-06 over the live table
radius 0.014323541476018172725671907488 (N=4315, Eckard Specht).
polished01.txt (+9.735e-07) cited only, not bundled.

## Attack 1 — Non-isometry: FAILED (claim survives)
Recomputed the full sorted pairwise-distance multisets myself, float64,
chunked (512-row blocks), 9,307,455 distances each, carrier vs posted seed
(data/cci4315.txt, sha256 confirmed
9af86ffc1a5fcc6ba0165682e81f4576e39fe21caa31284b973164aa9f3bccc5):
- sizes 9,307,455 vs 9,307,455; identical multisets (bitwise): False
- max |diff| 6.607512e-03, mean 5.747546e-04, median 3.892677e-04
- fraction of entries differing by >1e-9: 0.999998; by >1e-12: 1.000000;
  by >1e-15: 1.000000. An isometry would leave them identical to ~1e-15.
  They differ everywhere, at O(1e-3) scale.
- Cheaper invariants agree: sorted radii |c| max diff 1.372697e-02, mean
  1.764250e-03 (carrier innermost center at 0.01025524; seed has one at
  7.83e-05); sum |c|^2 carrier 2114.927328449 vs seed 2116.072379369,
  diff 1.145050920. (My numbers reproduce panel/non_isometry.log exactly;
  an intermediate script bug that compared carrier radii against
  polished01 instead of the seed was caught and corrected before this
  report — the corrected values are the ones above.)
- Structural tell: the seed is near-degenerate (9,062 pairs within 1e-9
  of its min distance); the carrier has a UNIQUE binding pair with a
  1.034e-07 gap to the next distance. Different configuration, not a
  rigid motion, not a relabeling, not a perturbation of the seed.

## Attack 2 — Queue rule: FAILED (claim survives)
Fresh live fetch of https://packomania.com/pending-requests.html just now
(HTTP 200, 12,856 bytes, sha256
a9dc3a8cdb18979f5053a009ed906d31ff1d14d0ab078ffbc23efa3bf8da103c) —
BYTE-IDENTICAL to the scout. Complete inventory of all 69 table rows:
the only rows with problem type exactly "cci" are Vidit Patankar
15-Oct-2026, 652–3943, and Karl Desfontaines 03-Nov-2026, 126–4141.
N=4315 is outside both (3943 < 4315; 4141 < 4315). "4315" appears 0 times
anywhere in the live page. No new cci line since the scout. Even under
the most paranoid reading (types containing "cci" as a substring: ccis
76–99, ccic 55–98), 4315 is outside every one of them. The newest row
on the page (09-Nov-2026, Jean-René Denoual csqv) is a different problem
type entirely.

## Attack 3 — History: FAILED (claim survives)
Fresh live fetch of https://packomania.com/cci/cci.html just now
(HTTP 200, 1,310,659 bytes, sha256
de37305f030c7380a1f92f2039c0a5a8a937a9b81a1efa2b16c0a3652dcae5e0) —
BYTE-IDENTICAL to the scout. Newest History-of-updates line is still
11-Oct-2026, Zii Fave N=15 computer-assisted proofs; page footer also
11-Oct-2026. All 32 occurrences of "4315" in the page are radius-table
digit substrings (e.g. 0.014315… in other rows) plus the ordinary N=4315
table row itself (line 3050), whose radius matches radius.txt exactly.
Zero occurrences inside the Updates section (lines 3173–3360). No line
newer than the scout touches N=4315. Fresh live radius.txt is also
byte-identical to the scout (sha256 6c60da0a…), row 4315 =
0.014323541476018172725671907488; author.txt byte-identical too (row
4315: Eckard Specht).

## Attack 4 — Margin reality check: FAILED (claim survives), with one
## documented artifact (immaterial, see below)
Independent float64 recomputation, two routes, both from the raw file:
- Chunked full pairwise: min d = 0.028649095541385745, unique binding
  pair file rows 4061/3823, gap to 2nd-min distance 1.034e-07; wall
  1−max|c| = 0.014324649231770459 (row 4309), i.e. 1.01e-07 ABOVE the pair
  term, so the pair binds. r* = 0.014324547770692872, margin +1.006295e-06.
- cKDTree nearest-neighbour: identical min distance, agrees exactly.
- Exact 50-digit mpmath from the decimal strings (never float64):
  binding-pair d = 0.02864909554138574257518887599171585937324, so
  r* = 0.01432454777069287128759443799585792968662, margin vs the
  radius.txt table = +1.006294675e-06 = 100,629× the 1e-11 bar; margin
  vs the check50-log "table" value is the same to 10 digits. The
  ~1e-06 margin sits ~100,000× above any rounding/noise artifact class
  (float64 noise ~1e-16, mpmath noise ~1e-48, the binding gap 1e-07).
- Stale-margin check: deep_polish.log's tracked margins (+1.006e-06,
  +9.735e-07) agree with my independent recomputation at reported
  precision (float64 +1.006295e-06 / +9.734752e-07; 50-digit
  +1.006294675e-06 / +9.734751654e-07). No overstatement; the known
  stale-margin bug class is absent.
- polished01 (cited only): independent 50-digit r* =
  0.01432451495118355140807462490648055990285, margin +9.734751654e-07.
  Confirmed as a second, distinct above-bar file; not bundled.

ARTIFACT (found, bounded, does not touch the verdict): the *_check50.log
files' "50-digit" values are float64 artifacts, not true 50-digit
mpmath values. Proven by exact reproduction:
- The check50 "table" 0.014323541476018173193573979063 is exactly
  mpf(float('0.014323541476018172725671907488')) — the float64 nearest
  double to the radius.txt string (+4.679e-19 off the true table).
- The claimed carrier r* 0.014324547770692870607422975127 is exactly
  math.hypot(dx,dy)/2 in float64 for the binding pair, printed to 30
  digits — off from the true exact-decimal 50-digit r* by 6.8e-19
  (<1 double ulp). polished01's claimed r* matches its float64 hypot
  value the same way.
- Consequence: the CLAIMED r* string is wrong in the 19th significant
  digit; the true 50-digit r* is 0.01432454777069287128759443799585792968662.
  The margin is 1.006294675e-06 either way — the artifact is 12 orders
  below the margin and 7 orders below the bar, so it changes no digit
  of the claim at any reported precision. But the check50 logs should
  not be cited as 50-digit certification; the genuine 50-digit
  certification is the computation in this report (and code/checker.py,
  which parses via mp.mpf from strings — exact — unlike the check50
  script). Note: the script that wrote *_check50.log is not saved
  anywhere in the run tree (only its logs), so its provenance was
  reverse-engineered from the numbers above.
- Related looseness in PREREG: the seed "reproduces its table row at 50
  digits" is overstated as written. My exact 50-digit seed r* is
  0.01432354147601817272567190748791470644949 — table minus 8.5e-32
  (pair binds, not wall, at 50 digits; in float64 the wall appeared to
  bind by 7e-18, unresolvable there). So the seed reproduces the table
  to ~1e-31, i.e. 31 digits, not 50 — the residual is the posted
  coordinates' 30-decimal rounding, and it is 21 orders below the bar.
  The seed's check50 margin of −5.874e-31 is consistent with this.

## Attack 5 — File integrity: FAILED (claim survives)
My own loader, strict 3-fields-per-line parsing:
- carrier polished00.txt: 4315 rows, indices 1–4315 in order, all finite,
  no NaN, 4315 unique points, max|c| = 0.9856753507682295 < 1,
  sha256 1906e4fbe7ef3aa8a9c86ebe76ba832b911353290310739b8be799a235fef3a8.
- seed cci4315.txt: same checks all pass, sha256 matches the task
  statement (9af86ffc…), max|c| = 0.9856764585239819 < 1.
- polished01.txt (cited only): same checks all pass, sha256
  5e0fe431dcd9b491270efc24091ec2cc49f7ffdef7a942410ba3bcce46069969.
- Seed reproduces its table row at 50 digits to −8.5e-32 (see Attack 4).

## Verdict
All five attacks failed. The claim stands on independent recomputation:
non-isometric to the posted seed (multisets differ at O(1e-3) on 100%
of entries), outside every live cci queue range, no newer history line
touches N=4315, margin +1.006294675e-06 (100,629× the bar) certified at
true 50 digits from the exact coordinate strings, file integrity clean.
The only findings are reporting-precision artifacts in the check50 logs
(~1e-19 level) and loose "50-digit" wording in PREREG — neither affects
the claim, the margin, or the bar comparison. No "Needs you" items.

Evidence kept in a scratch folder (fresh live fetches pending-now.html,
cci-now.html, radius-now.txt, author-now.txt; skeptic_float64.py +
skeptic_float64.log; skeptic_mpmath.py + skeptic_mpmath.log;
carrier_near.json, seed_near.json).

pass: true
