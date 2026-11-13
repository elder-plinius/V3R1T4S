# PREREG.v2: detector freeze (frozen 2026-11-12T19:18:57Z)

Written before any 1971 waveform was read or scanned (the 1971 S12 files were downloading; none had been
opened). PREREG.md stays in force; this file fixes the free parameters PREREG.md left to the 1972 dev data, and
lists every design change made on dev, openly.

## Changes against PREREG.md's detector design, all decided on 1972 dev data only

1. Despike (added): Hampel filter, window 7 samples, a sample is replaced by the running median when it deviates by
   more than max(3 DU, 5 x 1.4826 x running MAD). Reason: isolated telemetry spikes up to ~900 DU on dev days.
2. Spectral whitening (added): each day span is divided in the frequency domain by the running mean of its
   amplitude spectrum over 0.1 Hz before band-passing. Reason: the peaked-mode resonance near 0.42-0.45 Hz made the
   reversed-data null heavy (daily maxima 0.18-0.21); whitening brought theta(1/day) to about 0.10 and raised
   dev recall. (0.02 Hz and 0.1 Hz gave the same LOO recall; 0.1 Hz kept for its higher median LOO D.)
3. Reference event for the first template: largest positive A1 + A2 catalogue amplitude (PREREG.md said "largest
   catalogue amplitude"; this fixes the cross-station ambiguity): 1972-017 04:12.
4. Template window: L seconds starting 30 s before the onset picked on the stack envelope (first time the 5 s
   smoothed sum of squared component stacks exceeds 4 x its median over the first 60 s of a window that starts
   120 s before the aligned start). On S12 this pick is the S arrival (dev median detection onset minus catalogued
   start = +93 s), well inside the +/- 5 min recovery window of R1.
5. Alignment search +/- 240 s around the catalogued start, 4 iterations, members D >= 0.3 (21 of 54 dev events).
6. Stations: S12 only (MH1, MH2, MHZ, location 00). The rule written in attempts/evaluator-first/NOTES.md before
   the comparison finished: S12+S14 only if S12-only dev leave-one-out recall < 0.90. It was 53/54.

## Chosen configuration (rule in NOTES.md: best LOO recall, ties by median LOO D, then shorter L)

Dev grid (attempts/evaluator-first/out/dev/grid_s12_summary.txt), LOO recall at each config's own theta:
0.25-1.0 Hz: 300 s 50/54, 450 s 53/54 (median LOO D 0.304), 600 s 52/54; 0.3-1.2 Hz: 300 s 49/54, 450 s 53/54
(0.286), 600 s 53/54 (0.269); 0.4-1.5 Hz: 300 s 46/54, 450 s 52/54, 600 s 53/54 (0.225).

- FROZEN: band 0.25-1.0 Hz (4-pole zero-phase Butterworth), whitening 0.1 Hz, decimation 2 (3.3125 Hz),
  L = 450 s (1491 samples), S12 MH1/MH2/MHZ, D defined where >= 2 components have >= 90% valid samples.
- FROZEN templates: attempts/evaluator-first/frozen/A1_s12_dev1972_templates.npz
  sha256 4b0794805c2d8b720bd68363df0a120c29ecd0337c9247b54a5ade0ce5e6b635 (21 stacked 1972 A1 events).
- FROZEN threshold theta = 0.10897762490606308 (time-reversed dev data, declustered +/- 5 min, <= 1 per scanned
  day; 46.9 scanned day-equivalents).
- Detection onset = window start + 30 s. Recovery (R1): onset within +/- 300 s of the catalogued start.

## Frozen code (sha256)

- tools/mseed_steim2.py b8434322c0be937af454f4ba72d52106451b315ff51a74d4bcff692fd60c1db7
- tools/apollo_lib.py d0b567480e32a856dea331fcced501b1727c5ecf6f97c64f96d7ca9a2c8070d9
- tools/evlib.py 385b25276852a70df7c30be26aeb088ad551e666519959036bb216627cee11bc
- tools/scan.py 9f749a685c78f031eaa8c4b56b2e22d150cbb06a9e7461dcd455f28e76956e82
- tools/catalog_check.py 9308f3bd86d40b034224734733c7e89aff705dd85ec984a04fbdfa7036173e49
- tools/ephem.py 1e127e7ae84471436cd545ed08945b8331af697febd9ec853f396fc7caa450c1
- attempts/evaluator-first/code/score_scan.py e7cfe2abb05225f6ea99bc3e3c6636c7475aa3291f04ec329d70fef06aa4a69f
- attempts/evaluator-first/code/score_p2.py 3612f0679e9a311f5ca6b8c570bada648acbdf788be3cd25317d6eb66ff315df
- attempts/evaluator-first/code/candidates.py 8d7df9d797e8680bf7be802b9fb8d2e5bf6e062989c31f83d57b5f393a5aedc0

## Scoring run (unchanged from PREREG.md)

- score_scan.py FROZEN 1971 1 365 -> one JSON line per day: forward declustered peaks (>= 0.05) with per-channel
  CC, coverage per minute, time-reversed peaks and maximum (C0), and the daily maxima of 400 phase-randomised
  template controls (seeds 20261112 + k, k = 1..400).
- score_p2.py: R1/R2 recovery at theta, R3 false-alarm rate (C0 at theta per scanned day), chance recovery of
  catalogue times shifted by 1-10 days (200 draws), recall/false-alarm curve. p2 met if R2-primary recall >= 0.90.
- candidates.py: R4-R6 and the gap, glitch and thermal checks for forward detections above every control's
  full-span maximum.
- Any bug fix to the frozen code after this point is listed in the report with its effect, and if it changes a
  scored number the number is reported both ways.
