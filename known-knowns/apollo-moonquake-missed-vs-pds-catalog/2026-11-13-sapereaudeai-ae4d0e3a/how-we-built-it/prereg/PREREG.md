# PREREG: the second A100-like S14 + S16 candidate, 1973-10-30 02:25:51.5 UTC (claim run a100_1030_claim_run_2026-11-13-1615)

written: 2026-11-13T16:21Z (date -u), before any number below marked "new" was computed. The exact freeze time is
the line "frozen_utc:" at the end.

null_test: required

## Criterion

The bank's success criterion and partial wins, verbatim, are in target.md. The claim sought is the full criterion
(deep-moonquake branch). Nothing below changes a bank clause; the readings are the ones fixed before the S14 + S16
scan (run 2026-11-12-1842 PREREG.md, v4, v5, v14, v15) and reused, unchanged, by the confirmed claim of the same lens
(fullwin_panel_2026-11-13-0909/claim/prereg/).

## The object (fixed by the earlier scan; not re-chosen here)

- Nest A100 stack of the 12-nest S14 + S16 stacks (frozen/nets25_1973.npz; the A100 entry is byte-identical to
  frozen/nets25_1973_A100.npz), channels S14 MH1/MH2 and S16 MH1/MH2, frozen pipeline (despike, 0.1 Hz whitening,
  0.25-1.0 Hz, decimation 2 to 3.3125 Hz on the midnight-anchored grid, phase 0), L = 450 s.
- Window start 1973-10-30T02:25:21.509Z, onset (window start + 30 s) 02:25:51.509Z, MiniSEED Earth-received time;
  station lags from the common lag: S14 -1.509 s (-5 samples), S16 -0.906 s (-3 samples).

## Already known before this prereg (from earlier runs; not presented as new)

Dt 0.29806; NCC S14 MH1 0.4936, MH2 0.6211, S16 MH1 0.6196, MH2 -0.0235; R8 0.71 s vs nest median 0.82 s; phase
161.5 deg in [46.7, 318.3]; solar elevation S14 -65.6, S16 -32.4 deg; gap check passed; no Onodera window; nearest
PDS row 85.9 min (tables of 04:29Z); Knapmeyer-Endrun and Hammer 2015: nearest row -89.3 h; reference events within
+/- 24 h of 10-30 had S16 MH2 response r2 <= 0.08 (six values, a3_decision.txt of the earlier claim); the S12 + S14
lens (PREREG.v14) found this event at Dt 0.360 above its A100 null 0.203 (S12 0.514, S14 0.366); the earlier full-span
A100 null over 1973: time-reversed 0.1574, best of 400 shifts 0.1906. Lens history: PREREG.v15 (S14 + S16, frozen
03:40:56Z) was written after the PREREG.v14 (S12 + S14) results, in which this event was the strongest new A100
detection.

## Gates (all must pass to go to the panel)

- N0, the bank null, computed in this run (new): rerun the whole 12-nest S14 + S16 lag-tolerant scan of all 365 days
  of 1973 with C0 (all channels time-reversed) and C1..C400 (S16 rolled by 3600 + 180 k s), with the frozen code
  (tools/code/scripts/lagtol_scan_1416.py, one process, V3_WORKERS=1) on the same waveforms (sha256 checked against
  the earlier claim's SHA256SUMS_waveforms.txt). Full-span maximum per control: C0 = max over days of rev_max, Ck =
  max over days of shift_max[k-1]. real = Dt of the A100 forward peak whose window start lies within +/- 10 s of
  02:25:21.509 on day 303 in this rerun. Pass: real > every one of the 401 A100 control maxima. Also reported:
  byte-identity of this rerun with the saved scan, the candidate's rank among all 1973 A100 forward peaks.
- R6: no row of any of the 12 PDS tables as fetched in this run (16:15-16:16Z) within +/- 5 min of the onset or the
  window start (minute resolution: +59 s allowed), and neither time inside a levent start-stop span; also no Onodera
  SP window containing or within +/- 5 min of them. The NOVELTY skeptic re-fetches the tables live.
- R7: best single-channel NCC >= 0.5 at S14 and at S16, each at its own best lag (station-mean argmax) within +/- 7
  samples of the common lag. R8: ATT-corrected S16-minus-S14 arrival difference within 2 s of the nest's median over
  its catalogued 1973 events above the null (tools/code/scripts/att_check_1416.py). R9: anomalistic phase inside
  [46.7, 318.3] deg. Gap (>= 99% valid, no timing discontinuity in [onset - 10 min, onset + 450 s + 10 min]), thermal
  (|solar elevation| > 12 deg at both stations), frozen glitch rule (spike > 8 x MAD allowed only if Dt without that
  channel stays above the null maximum; both template halves positive at each station).
- G1/G2 (Liu, Xiao and Li 2025, lunar_ACC v1.0.1, Zenodo 15715187; data/lit_acc with SHA256SUMS.txt, the copies
  verified by the earlier claim against the record's md5). Same design as the confirmed claim. G1: list every
  catalogued Spike, Step-Up or Step-Down interval on MH1 or MH2 (MHZ reported only) that overlaps the S14 window
  [02:25:21.509 - 1.509 s, + 450 s] or the S16 window [02:25:21.509 - 0.906 s, + 450 s]; an overlap sends the window
  to G2. G2: mute +/- 5 s around every overlapping catalogued interval and every raw sample flagged by the frozen
  rule (|x - median| > 8 x max(MAD, 0.5)), on all channels of that station, template and data alike; NCC over unmuted
  samples, each station at its best lag within +/- 7 samples of the common lag. Pass: best single-channel NCC >= 0.5 at
  both stations and Dt > the N0 best control. G2 is computed and reported whether or not G1 finds an overlap.
  Coverage reported: catalogue entries per station on 1973 days 302-304, nearest entries to the onset.
- Novelty lists N1-N3: Knapmeyer-Endrun and Hammer 2015 Tables S1-S3 (no row with onset within +/- 5 min of the onset
  or window start, none spanning them), Bulow et al. 2005 Table 2 (no entry within +/- 6 min), Onodera SP windows
  (R6). NOVELTY also searches 2025-2026 lists and this repo, and treats the first claim (package
  2026-11-13-[credit]-9ff1c507, which mentions this event as not claimed) as our own prior work.
- Attribution DEFENDED: none of C1, C2, C3, C6, C6b below holds. An inconclusive test does not take attribution away;
  it is reported.

## Attribution tests (attacks; each can take the attribution away)

- A1 / C1 (twelve stacks): score the candidate window against all 12 frozen stacks, frozen Dt, maximum over window
  starts within +/- 10 min of 02:25:21.509; per-channel NCC at each station's best lag; each nest's own null maximum
  from N0. C1 holds if a nest X != A100 has Dt_X above its own N0 null maximum, R7 at both stations and Dt_X > Dt_A100
  of this window, and also passes R8 and R9 for X (computed only if the first three hold). Reported: whether A100 is
  the only stack above its own null here.
- A2 / C2 (lag side lobes): A100 station means over +/- 30 s of the common lag. C2 holds if at either station the
  maximum over +/- 30 s lies more than 7 samples from the common lag and exceeds the maximum within +/- 7 samples by
  more than 0.05. Reported: the six highest lags per station and the margin between the in-window maximum and the
  best value outside +/- 7 samples.
- A2a (moveout): Nakamura 2005 S picks, 16S - 14S per nest; nests within 2 s and 5 s of A100 (known from the earlier
  claim: A35, A244, A7 within 5 s); their reverse-search scores under A5.
- A3 / C3 (S16 MH2 state at this date, re-derived): the frozen A3 rule of the earlier claim
  (prereg/PREREG_fullwin.md there), unchanged, with t0 = 02:25:51.509 on 1973-10-30: r2 = (R_MH2 - 1)/(R_MH1 - 1);
  reference events = levent rows within +/- 12 h (extended to +/- 48 h on a side with none). Both nearest references
  <= 0.25: MH2 unresponsive, no contradiction. Both >= 0.5 and the candidate's r2 < 0.25 (or R_MH2 < 1.2 if r2 is
  undefined): C3 holds. Else inconclusive. Descriptive (A3b): for each catalogued 1973 A100 event, its forward-scan
  S16 MH1 and MH2 NCC next to the median r2 of reference events within +/- 24 h, to show whether catalogued A100
  events in MH2-dead periods look like this candidate.
- A5 / C6 / C6b (reverse search): template = this candidate's own preprocessed window, S14 MH1/MH2 cut at -5
  samples and S16 MH1 (variant b) or S16 MH1/MH2 (variant a) at -3 samples from 02:25:21.509; frozen Dt over all 365
  days of 1973 (+/- 7 samples per station), declustered peaks (+/- 5 min) with Dt >= 0.10, peaks within +/- 10 min of
  the candidate excluded. Each 1973 levent deep moonquake (T2 = A) scores the largest Dt of the peaks whose onset
  (window start + 30 s) lies in [start - 5 min, start + 10 min]. Variant b decides if A3 finds MH2 unresponsive,
  else variant a. Baseline: 3000 random 15-min windows (seed 20261113), at least 30 min from any levent row.
  - C6 holds if the 10 highest-scoring catalogued deep moonquakes include no A100 event and one other nest holds >= 3
    of them while that nest is < 30% of all scored 1973 deep moonquakes.
  - C6b holds if an event of A35, A244 or A7 (moveout within 5 s of A100) scores above every A100 event and above the
    random-window 99th percentile.
  - Support level (reported in the claim, not a gate): SUPPORTED if >= 2 of the top 10 are A100 events (A100 is 14 of
    the 998 catalogued 1973 deep moonquakes; >= 2 in the top 10 has probability below 0.01 under random ranking),
    WEAK if exactly 1, NONE if 0.
  - Reported: the reverse-search score at the time of the first claimed event (1973-11-26), as mutual similarity of
    the two uncatalogued events, explicitly not as independent confirmation.
- A6 (specificity of the bank tests, reported; sets wording): from N0's A100 forward peaks, each 1973 levent deep
  moonquake (T2 = A) gets the peak with onset in [start - 5 min, start + 10 min]. Count the non-A100 events with Dt
  above the N0 A100 best control, R7 (best channel >= 0.5 at both stations) and R9 (phase in [46.7, 318.3]); same
  for the A100 events. If k >= 1 non-A100 events pass, the claim must say "the bank's membership tests are not
  specific to A100: k of N catalogued non-A100 1973 deep moonquakes also pass them against the A100 stack".
- A4 (phase, descriptive): the 1973 A100 sequence and the candidate's spacing from 10-02 and 12-23 (and 11-26,
  our own first claim, not independent).

## Multiplicity (reported in the claim's scope sentence and headline, not in a footnote)

- What the per-template full-span null bounds (fixed reading): P(the A100 template's largest chance coincidence over
  1973 reaches x), whichever peak it is. It therefore covers choosing the second of several A100 peaks, and the joint
  statement "neither of the two claimed A100 events is a chance coincidence" is bounded by the value for the weaker
  one. It does not bound: the choice among 12 templates; the choice among station pairs and lenses; attribution
  errors (real events of other sources matching the stack), which A1-A6 address.
- M1 (new; max-T family-wise null over the 12 templates of this scan): for each nest n and control k (k = 0..400),
  M[n,k] = full-span maximum from N0. med_n = median_k M[n,k], s_n = 1.4826 x median_k |M[n,k] - med_n|,
  z[n,k] = (M[n,k] - med_n) / s_n, T[k] = max_n z[n,k]. Candidate z_c = (real - med_A100) / s_A100.
  p_FW = (1 + #{k : T[k] >= z_c}) / 402. Reported with the per-template bound 1/402 and the Bonferroni bound 12/402.
- M2 (model-based, labelled as extrapolation): a GEV fit (scipy.stats.genextreme.fit) to the 401 A100 control
  maxima; tail probability at real; Sidak over 12 templates; Bonferroni over every full-criterion two-station
  template-year scan of the parent run (counted in M3).
- M3 (count, read after the freeze from the parent run's lens reports and build logs): number of two-station
  template-year scans in run 2026-11-12-1842 that could have produced a full-criterion claim, with the 1973 subset
  (expected: A1 S14 + S16; 13 nests S12 + S14; 12 nests S14 + S16). Empirical Bonferroni bound = count / 402.
- M4 (descriptive): status of the other R7 candidates of the scan (11-26 claimed; 01-30 in an Onodera SP window: its
  Onodera row) and of the fourth new above-null A100 detection (04-22, fails R7).
- Wording rule: the scope sentence states the per-template result and at least the 12-template family-wise result
  (p_FW, or 12/402 if larger), and the claim text states the parent-run Bonferroni bound and the lens history (S14 +
  S16 designed after this event was the strongest new A100 detection on S12 + S14).

## Robustness (reported, not gated)

- D1 (decimation phase): rebuild the A100 S14 + S16 stack with the frozen builder (tools/code/scripts/
  net25_build_1416.py logic, nest 100 only) on the other decimation phase (raw samples 1, 3, 5, ... instead of
  0, 2, 4, ...), and compute the candidate's per-channel NCC and Dt with each station's lag within +/- 7 samples of
  the best common lag within +/- 10 s of the window start, on that grid.
- S12 (third station): the frozen S12 + S14 A100 stack of lens lagtol-25nests-1973 (tools/frozen/
  nets25_1973_s12s14.npz), its statistic (S12 mean over >= 2 valid channels, S14 mean over >= 1, +/- 7 samples, min),
  maximum within +/- 10 min of 02:26:50.264 (that lens's window start); per-channel NCC; compared with that lens's
  null 0.203 (its stdout; its null is not rerun here). S14 is shared with the claim, so this is supporting, not
  independent, for S14.

## What follows

- All gates pass and attribution DEFENDED: build claim/ (object, code, frozen stacks, results, data, waveforms,
  REPRODUCE.md, CLAIM.md citing the first claim as prior work and stating the multiplicity numbers), run the
  three-skeptic panel (fresh contexts: reproduce, novelty, criterion), gate, package only on CONFIRMED_*.
- Otherwise: NOT confirmed, no panel; report.md and the run report say which test failed. A clean negative is a
  result.

## Escape hatches (declared now)

- A data window that cannot be read (missing file, < 99% valid) makes that test inconclusive, not a contradiction.
- C3 with no reference event within +/- 48 h on a side: inconclusive.
- If the 12-nest N0 rerun cannot finish within 75 min wall clock, N0 uses an A100-only rerun (same code, same
  data) and M1 uses the saved 12-nest scan of the lens for the other 11 nests; disclosed.
- A5 if the reverse scan cannot finish within 60 min: C6/C6b inconclusive, partial results reported.
- D1 and S12 failures to run are reported, not gated.

frozen_utc: 2026-11-13T16:22:21Z (file completed; the header time 16:21Z is when writing started)
