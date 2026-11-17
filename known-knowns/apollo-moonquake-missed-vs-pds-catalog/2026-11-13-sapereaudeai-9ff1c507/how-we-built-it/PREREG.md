# PREREG: attribution, glitch-catalogue and novelty-list gates for the A100-like S14 + S16 candidate (fullwin_panel)

frozen: see the line "frozen_utc:" at the end (written from `date -u`, before any new number below was computed)

null_test: required

The null test of the bank (same templates on time-reversed data and with S16 circularly shifted by >= 1 h, over all
of 1973) was run before and is unchanged: 401 controls, best control 0.1906, real 0.3433
(../full_claim_run_2026-11-13-0429/null_test.md, copied to null_test.md here). Nothing in this file changes it.

## Object (unchanged from ../full_claim_run_2026-11-13-0429/claim/)

- Onset 1973-11-26T07:46:28.641Z (MiniSEED Earth-received time), template window start 07:45:58.641Z, L = 450 s.
- Nest A100 stack of S14 MH1/MH2 + S16 MH1/MH2 (claim/frozen/nets25_1973_A100.npz), frozen pipeline
  (band 0.25-1.0 Hz, whitening 0.1 Hz, despike, decimation 2 to 3.3125 Hz, common midnight-anchored grid).
- Station lags from the common lag: S14 +1.509 s, S16 +2.113 s. Dt 0.3433; best single-channel NCC S14 MH2 0.562,
  S16 MH1 0.699; ATT-corrected S16 - S14 0.93 s vs nest median 0.82 s; anomalistic phase 157.2 deg in [46.7, 318.3].

## What is inherited and not re-decided here

The bank-required readings were fixed before the S14 + S16 scan (run 2026-11-12-1842 PREREG.md, v4, v5, v14, v15)
and were reproduced by two fresh panelists: R6 (no PDS row within +/- 5 min, onset not in a levent span), R7 (best
single-channel NCC >= 0.5 at each station at its own lag within 7 samples), R8 (ATT-corrected S16 - S14 within 2 s
of the nest's median), R9 (anomalistic phase in the nest's 95% interval), null, gap, thermal (|solar elevation| > 12
deg at both stations) and the frozen glitch rule. They stay exactly as fixed. This prereg adds only what the main
session asked for, each with the most favourable fair reading fixed now, and no extra strict gate on the bank's
clauses.

## Rule for the attribution question (fixed now)

The bank defines membership of a deep moonquake by its own tests (NCC >= 0.5 with the stack of a catalogued nest on
>= 2 stations, moveout within 2 s, phase consistent). Those are met under the fixed readings. The tests below can
only take the attribution away by a stated contradiction; an inconclusive test leaves the bank's tests in charge and
its caveat is reported. Attribution to A100 is DEFENDED if none of C1, C2, C3, C6 holds; otherwise it is NOT
defended and nothing is claimed.

- A1 / C1 (every stacked nest). Score the candidate against all 12 frozen S14 + S16 nest stacks
  (claim/frozen/nets25_1973.npz) with the frozen statistic (Dt = min of station means, each at its best lag within
  +/- 7 samples), maximum over window starts within +/- 10 min of 07:45:58.641; report Dt, per-channel NCC and lags
  per nest next to that nest's own 1973 null maximum (lagtol_candidates_1973_stdout.txt). C1 holds if a nest X other
  than A100 has Dt_X above its own null maximum, best single-channel NCC >= 0.5 at both stations, and Dt_X > 0.3433,
  and also passes R8 and R9 for X (computed only if the first three hold).
- A2 / C2 (moveout). (a) Report Delta_X = 16S - 14S from Nakamura 2005 (nakamura_2005_dm_arrivals.csv) for every
  nest with both picks, and list nests with |Delta_X - Delta_A100| <= 2 s and <= 5 s (nests the moveout cannot tell
  apart from A100). Descriptive. (b) Lag robustness: the station-mean NCC of the A100 stack at S14 and at S16,
  searched over +/- 30 s of the common lag. C2 holds if at either station the maximum over +/- 30 s lies more than
  7 samples from the common lag and exceeds the maximum within +/- 7 samples by more than 0.05.
- A3 / C3 (S16 MH2 response). In the frozen preprocessed data (preprocess(), dec 2), for S16 MH1 and MH2:
  E_sig = mean y^2 over [t0 - 60 s, t0 + 600 s]; E_noise = median of the mean y^2 of the 60 s sub-windows of
  [t0 - 25 min, t0 - 5 min]; R = E_sig / E_noise; response r2 = (R_MH2 - 1) / (R_MH1 - 1), defined when R_MH1 >= 1.5
  and both channels are >= 99% valid in both spans. t0 = catalogue start for levent rows, the onset for the candidate.
  Reference events: every levent row (any type) with t0 within +/- 12 h of the onset (extended to +/- 48 h on a side
  with none). Channel state at the candidate = r2 of the nearest reference event before and the nearest after.
  Both <= 0.25: S16 MH2 unresponsive then, the candidate's S16 MH2 null is explained (no contradiction). Both >= 0.5
  and the candidate's r2 < 0.25 (or its R_MH2 < 1.2 if its r2 is undefined): C3 holds. Anything else: inconclusive.
  Descriptive: r2 of every 1973 levent row with R_MH1 >= 1.5, as a time series, and of the catalogued A100 events.
- A4 (phase). R9 stays as fixed. Descriptive only: anomalistic phases of the catalogued A100 events and the 1973
  sequence of A100 times; no new gate.
- A5 / C6 (nests without stacks: reverse search). Template = the candidate's own preprocessed window, each station
  cut at its own lag (S14 MH1, S14 MH2 at +1.509 s; S16 MH1 at +2.113 s). Variant b (decides): S16 = MH1 alone,
  because the candidate shows no energy above noise on S16 MH2 (ratio 1.10 in the earlier REPRODUCE panel); variant a
  (all four channels) is run and reported. Scan all 365 days of 1973 forward with the frozen Dt statistic (+/- 7
  samples per station), declustered peaks (+/- 5 min) with Dt >= 0.10, excluding +/- 10 min of the candidate. Each
  1973 levent deep moonquake (T2 = A) scores the largest Dt of the peaks whose onset (window start + 30 s) lies in
  [start - 5 min, start + 10 min]. C6 holds if the 10 highest-scoring catalogued deep moonquakes include no A100
  event and one other nest holds >= 3 of them while that nest is < 30% of all scored 1973 deep moonquakes. Also
  reported: per-nest median score (nests with >= 3 scored events) and A100's rank.
- Other alternatives are reported, not gated beyond the fixed checks: thermal (fixed check), glitch (gates G below),
  the lag-tolerant statistic (C2 and the inherited null, which uses the same statistic).

## Glitch-catalogue gates G (same design as the two confirmed p1 claims, extended to S16)

Catalogue: Liu, Xiao and Li 2025 (JGR Planets 130, e2025JE009277), lunar_ACC v1.0.1 (Zenodo 15715187). One GET of
the Zenodo record API for the file checksum; the release zip already in this workspace is used only if its md5
equals the record's checksum, else one GET of the file. The S14 Spike MH1/MH2 files must be byte-identical to
../../s14-multinest-1971/a39_claim_run_2026-11-13-0552/data/lit_acc (sha256 recorded in out/).

- G1: list every catalogued interval (Spike, Step-Up, Step-Down) on S14 and on S16, components MH1 and MH2, that
  overlaps that station's template window (S14 [07:45:58.641 + 1.509 s, + 450 s], S16 [07:45:58.641 + 2.113 s,
  + 450 s]); MHZ reported only. An overlap does not fail by itself; it sends the window to G2.
- G2: mute +/- 5 s around every overlapping catalogued interval and every raw sample flagged by the frozen rule
  (|x - median| > 8 x max(MAD, 0.5)), on all channels of that station, template and data at the same samples; NCC
  over unmuted samples, each station at its best lag within +/- 7 samples of the common lag. Pass if the best
  single-channel NCC is >= 0.5 at S14 and at S16 and Dt > 0.1906. Also reported with lags within +/- 10 s.
- Coverage: if the catalogue has no S16 entries for late 1973, G1 at S16 is written "not covered" and G2 at S16 uses
  the rule-flagged samples alone. If the catalogue cannot be obtained (block, no retry), G is PENDING and nothing is
  confirmed.

## Novelty lists N (resolved input from the human)

- N1: Knapmeyer-Endrun and Hammer 2015 Tables S1-S3 (manual_downloads/knapmeyer2015, sha256 in NOTES.md there):
  re-extracted here (shipped reader, plus an independent byte-level scan of the .xls strings). Pass if no row has an
  onset within +/- 5 min of the onset or of the window start and no row's [onset, onset + duration] contains them.
- N2: Bulow et al. 2005 (manual_downloads/bulow/bulow_jgr05.pdf), Table 2 (new A1 events): pass if no entry within
  +/- 5 min (minute resolution, so +/- 6 min). Anything else in the paper that bears on attribution is reported.
- The live PDS re-fetch and the 24-month search are NOVELTY's job in the panel (kit RUN.md step 6).

## What follows

- If G, N1, N2 pass and attribution is DEFENDED: rebuild claim/ (the earlier package plus this evidence; numbers
  not changed), run the three-skeptic panel (fresh contexts), gate, package only on CONFIRMED_*.
- Otherwise: NOT confirmed, no panel, report.md says why. A clean negative is a result.

## Escape hatches (declared now)

- A data window that cannot be read (missing file, < 99% valid) makes that test inconclusive, not a contradiction.
- C3 with no reference event within +/- 48 h on a side: inconclusive.
- A5 if the scan cannot finish in 90 min wall clock: C6 inconclusive, partial results reported.
- The decimation-phase sensitivity of S14 MH2 (0.562 frozen grid, 0.468 other phase) is reported, not gated: the
  frozen grid was fixed before the scan.
frozen_utc: 2026-11-13T09:11:02Z
