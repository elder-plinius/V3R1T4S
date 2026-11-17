# Panel: REPRODUCE skeptic (p2 claim, apollo-moonquake-missed-vs-pds-catalog)

context: subagent (fresh context, Claude Code Agent tool, subagent_type reproduce)

Claim judged: CLAIM.md says that a detector built only from 1972 data (21 stacked 1972 A1 events, S12 MH1/MH2/MHZ) recovers
63 of 67 catalogued 1971 A1 events at frozen theta = 0.10898. It says the false-alarm rate is 1.196 per scanned day on
time-reversed 1971 data (400 detections over 334.54 scanned day-equivalents), and that the package is saved and re-runnable.

## 1. Independent checker, written from the definition before the author's code was read

Definitions used (quoted from prereg/PREREG.md and prereg/PREREG.v2.md):
- "Daily arrays at 6.625 Hz on a uniform grid from record start times; -1 samples and missing records are gaps. Demean,
  gap samples set to zero after filtering and flagged invalid."
- "Hampel filter, window 7 samples, a sample is replaced by the running median when it deviates by more than
  max(3 DU, 5 x 1.4826 x running MAD)"; "each day span is divided in the frequency domain by the running mean of its
  amplitude spectrum over 0.1 Hz before band-passing".
- "band 0.25-1.0 Hz (4-pole zero-phase Butterworth), whitening 0.1 Hz, decimation 2 (3.3125 Hz), L = 450 s (1491
  samples), S12 MH1/MH2/MHZ, D defined where >= 2 components have >= 90% valid samples."
- "Statistic D(t) = mean over available components of the single-channel normalised cross-correlation at common lag t."
  "Detections: local maxima of D, declustered (largest within +/- 5 min kept). Onset = window start + 30 s."
- R1: "recovered if a declustered detection (statistic >= theta) has its onset time within +/- 5 min of the catalogued
  signal start". R2: the denominator is the events scanned at some lag in that window. R3: "the rate (per day of scanned
  data) of declustered detections >= theta on ... the time-reversed data over the full 1971 span".

What I wrote myself:
- A MiniSEED Steim2 decoder, from the SEED 2.4 layout. On all 1254 files in waveforms/s12 it is bit-identical to the
  claim's code/tools/mseed_steim2.py: 704,505,096 samples equal, record start times within 1.5e-8 s, and the reverse
  integration constant matched in every record.
- The whole detector: day grid, Hampel despike, whitening, Butterworth N=4 band-pass with sosfiltfilt, decimation,
  per-channel Pearson NCC, D, true-local-maximum greedy declustering at +/-300 s, time-reversed days, and R1/R2/R3 scoring.
- It ran over all 365 days of 1971 (no sampling) with the frozen templates in frozen/A1_s12_dev1972_templates.npz. The
  npz sha256 is 4b079480...6b635, the hash frozen in PREREG.v2. The templates are zero-mean and unit-norm.

Catalogue: data/catalog/levent.1008weber.csv has sha256 f95743b2...b0b9b93c, the same as the copy I re-fetched live from
the PDS at 2026-11-12T21:33:58Z (HTTP 200, 890,253 bytes). My own parse finds 67 rows with Y=71, T2='A', N2=1, at the
same 67 times as the results/p2.md table.

## 2. Recomputed numbers next to the claimed ones

| quantity | claimed | claim's code rerun by me | my scorer on the saved scan | my independent detector |
|---|---|---|---|---|
| 1971 A1 events / scanned (R2) | 67 / 67 | 67 / 67 | 67 / 67 | 67 / 67 |
| recovered at theta (R1) | 63 | 63 | 63 | 63 |
| recall (primary and all) | 0.9403 | 0.9403 | 0.9403 | 0.9403 |
| reversed detections >= theta | 400 | 400 | 400 | 311 |
| scanned day-equivalents | 334.544 | 334.5444 | 334.5444 | 345.545 |
| false alarms per scanned day (R3) | 1.1957 | 1.1957 | 1.1957 | 0.900 |
| max reversed D over 1971 | (not stated) | 0.1376 | 0.1376 | 0.1331 |
| forward declustered detections >= theta | (not stated) | 444 (1.327/day) | 444 | 378 (1.094/day) |
| shifted-catalogue null (400 controls), best / real | 0.0484 / 0.9403 | 0.0484 / 0.9403 | - | - |
| chance recovery (200 draws), mean / max | 0.00949 / 0.0678 | identical (p2.json byte-identical) | - | - |

Per-event best D, my independent detector against results/p2.md:
- Median |difference| is 0.0025 and the 90th percentile 0.010.
- Two events change recovery status, so the recovered set differs by one swap.
- 1971-08-06 07:20 (A1 3.8, A2 13.5): claimed 0.082 (missed); mine 0.772 (recovered).
- 1971-11-04 18:15: claimed 0.1127 (recovered); mine 0.106 (missed). Both codes peak at the same lag, onset 129.5 s after
  the catalogued start, so this is a marginal event near theta.
- Missed in both: 1971-09-27 04:00 (claimed 0.083 / mine 0.084), 1971-09-30 20:33 (0.084 / 0.084) and 1971-12-18
  20:41 (0.076 / 0.077).
- In my run the best-lag onsets of recovered events mostly sit at +80 to +160 s, matching the dev offset (S arrival,
  +93 s).

## 3. Reproduction of the claim's own chain, with the shipped code copied to scratch and FFT workers set to 1

- waveforms/SHA256SUMS_waveforms.txt: all 1254 files OK. Two files were spot-checked against live PDS copies and are
  byte-identical: xa.s12.00.mhz.1971.028 and xa.s12.00.mh1.1971.218. data/pse/collection_data_seed_inventory.csv lists
  exactly 1095 S12 location-00 MH files for 1971, and all are in the package.
- code/scripts/score_scan.py over 1971 days 1-365 (forward and reversed, no template controls) reproduces
  results/scan_s12_A1_1971.jsonl exactly on all 365 days: forward peaks (times, D, per-channel CC), reversed peaks,
  scanned fractions and per-minute coverage. It is deterministic. The 400 phase-randomised controls were not rerun;
  p2 does not use them.
- code/scripts/score_p2.py gives byte-identical results/p2.json and results/p2.md from the saved scan and from my rerun.
  code/scripts/p2_null.py reproduces results/null_test.md (best control 0.0484, real 0.9403).
- code/scripts/dev_eval.py rebuilds frozen/A1_s12_dev1972_templates.npz from the 1972 dev days alone, bit-identically:
  tm, theta, the 21 members and the 54 leave-one-out values. It reads only 1972 event days (catalogue Y=72). So
  "built only from 1972 data" holds for the templates and theta.

## 4. Discrepancies and their causes

1. **Gap widening not in the prereg.** apollo_lib.preprocess marks every sample within 20 s of a gap or -1 sample as
   invalid (`pad_s=20.0`); PREREG.md/v2 do not say this. It explains 1971-08-06 07:20. A ~45 s telemetry gap sits
   535-582 s after the catalogued start. With the 20 s widening, every channel at the true lag is 87% valid, below the
   90% rule, so D is undefined there and the best remaining lag gives 0.082. Without it the window is about 91% valid
   and D = 0.77. The widening also accounts for most of the 11-day difference in scanned day-equivalents (334.5 against
   my 345.5); the claim's code also scans windows that cross midnight using the next day's head. This choice worked
   against the claim: one fewer event recovered and fewer scanned days, which raises the rate per day.
2. **Declustering differs from its own comment and from the prereg.** apollo_lib.decluster says "local maxima only" but
   declusters greedily over every sample above the floor, not over local maxima as PREREG.md says. I recounted with the
   claim's own D restricted to local maxima. The counts are unchanged: 400 reversed and 444 forward detections >= theta.
   No effect on any p2 number.
3. **False-alarm rate 1.196 against 0.900 per day.** Near theta the reversed-data tail is steep. With the claim's code
   the rate is 1.71, 1.43, 1.20, 0.94 and 0.80 per day at theta -0.002, -0.001, 0, +0.001 and +0.002. My
   implementation's tail sits about 0.0013 lower in D: my rate equals 1.1957 per day at theta - 0.00135, where my
   recall is still 63/67. My daily reversed maxima differ from the claim's by a median of -0.0003.
   So the difference comes from D-level preprocessing detail: median against mean demeaning, despike variant,
   re-zeroing after whitening, and the gap widening. Declustering is not the cause. The claimed rate is the more
   pessimistic of the two.
4. **Code hashes against PREREG.v2's frozen list.** mseed_steim2.py, evlib.py, scan.py, catalog_check.py and ephem.py
   match. apollo_lib.py, score_scan.py, score_p2.py and candidates.py do not: the frozen hashes are d0b56748...,
   e7cfe2ab..., 3612f067... and 8d7df9d7..., the shipped ones 76fda262..., be09787d..., 7d6f4f7b... and 17122406....
   The package contains no change log, although PREREG.v2 promised one for any post-freeze fix. The visible changes are
   path rewrites: the `__import__('os')` path idiom, the APOLLO_WF override, and claim-relative data paths.
   Three facts tie the shipped code to the frozen version functionally:
   - The shipped apollo_lib.py rebuilds the pre-1971 frozen templates and theta bit-identically.
   - The shipped scan reproduces the saved scan exactly.
   - My own scorer, written from R1-R3, gives the same p2 numbers as the shipped score_p2.py.
   This is a disclosure gap, not a numeric problem. The criterion skeptic may want to weigh it.

## 5. Not covered by this check

- The bank's other null, "data circularly shifted between stations by >= 1 h", is not run. The claim is single-station
  and uses the time-reversed null for its R3 rate. Whether that satisfies "a measured false-alarm rate" is a criterion
  question; numerically the rate is measured and reproduces.
- The 400 phase-randomised template controls in the saved scan (ctrl_max) were not rerun; p2 scoring does not use them.
- Candidates and p1 (code/scripts/candidates.py) were not part of this check.

## Verdict

Every claimed p2 number is reproduced exactly and deterministically: from the waveforms with the claim's code, and by my
own scoring of the saved scan. The frozen templates and threshold rebuild bit-identically from 1972 data alone. My
independent detector, written from the preregistered definitions, recovers the same count: 63 of 67 (94.0%, at least 90%;
the bar needs 61). Its false-alarm rate is 0.90 per scanned day, the same order as the claimed 1.196.

The per-event and rate differences trace to identified implementation details, the 20 s gap widening and a 0.001-level
shift in D. None of them inflates the claim. Recall stays at or above 0.91 at thresholds where the time-reversed data
give zero false alarms over all of 1971: 61/67 with the claim's code at 0.14, 63/67 with mine at 0.14. The code-hash
drift against PREREG.v2 is undisclosed, but functionally neutral by the tests above. No missing object, no
non-determinism, and no mismatch that is not explained.

pass: true
