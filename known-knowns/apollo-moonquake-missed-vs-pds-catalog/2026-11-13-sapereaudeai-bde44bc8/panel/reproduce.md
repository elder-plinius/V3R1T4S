# REPRODUCE skeptic: p1 claim, A38 member on S14 MH1/MH2, 1971-05-13 (rebuilt package, glitch catalogue named)

context: subagent (Agent tool, fresh context; third REPRODUCE instance on this claim/ after two were killed by an API outage)

Everything below was judged from claim/ only. The bundle was read in place and nothing in it was modified; every run of
the author's code used a copy of claim/ (waveforms read in place, read-only) in my own scratch folder outside claim/.

## Definitions checked against (quoted)

Bank p1 (CLAIM.md, verbatim): "A new member of a catalogued nest seen on a single station with CC >= 0.6 and the null
test passed (single-station detections are weaker evidence)."

Readings (prereg/PREREG.md, PREREG.v12 and inherited rules):
- "R4'': best single-channel NCC (S14 MH1 or MH2) at the D14 peak >= 0.6."
- "D14 = mean single-channel NCC over MH1/MH2 (both valid)."
- Null (run1_PREREG.md): "C0 (bank-literal for one station): the frozen templates correlated with the time-reversed
  data of every scanned 1971 day (each day's arrays reversed in time), full span." "C1..C400: 400 phase-randomised
  templates (for each control, one set of uniformly random Fourier phases, seed 20261112 + k, applied to all three
  components' template spectra so the inter-component phase relations are kept; amplitude spectra unchanged),
  correlated with the forward 1971 data, full span, same statistic." "p1/claim null: real candidate D must exceed the
  full-span maximum of D in every control C0..C400 (401 controls)." Span (PREREG.v12): "1971 days 36-365".
- Detector (run1_PREREG.md and run1_PREREG.v2.md): "Daily arrays at 6.625 Hz on a uniform grid from record start
  times; -1 samples and missing records are gaps. Demean, gap samples set to zero after filtering and flagged
  invalid." "Despike: Hampel filter, window 7 samples, ... max(3 DU, 5 x 1.4826 x running MAD)." "each day span is
  divided in the frequency domain by the running mean of its amplitude spectrum over 0.1 Hz before band-passing."
  "FROZEN: band 0.25-1.0 Hz (4-pole zero-phase Butterworth), whitening 0.1 Hz, decimation 2 (3.3125 Hz), L = 450 s
  (1491 samples)". "D is defined only where >= 2 of 3 components have >= 90% valid samples in the window." "Onset =
  window start + 30 s."
- R6: "a candidate is not new if any row of any table of the PDS catalogue data directory has a time within +/- 5 min
  of the candidate onset, or if the onset lies between a levent row's signal start and its stop time (column E; 9999 =
  continues to the next event)."
- Checks: "Gap: >= 99% valid samples on every used component in [onset - 10 min, onset + window + 10 min]; no record
  timing discontinuity"; glitch (PREREG.v9): "a spike above 8 x MAD in the raw window is allowed only if D without that
  channel stays above the null maximum; both template halves must correlate positively; thermal: |solar elevation at
  the station| > 12 deg."
- Gates (prereg/a38_glitch_check_lens_PREREG_frozen_2026-11-13T055912Z.md, verbatim): "G1: no catalogued S14 ACC-Spike
  interval (Liu, Xiao and Li 2025; copies in data/lit_acc, sha256 in PREREG.md) overlaps the 450 s window." "G2: mute
  +/- 5 s every overlapping catalogued spike and every raw sample flagged by the frozen glitch rule (|x - median| > 8 x
  max(MAD, 0.5)); NCC over unmuted samples, best lag within +/- 10 s; pass if best CC >= 0.6 and D > 0.2868." G1 is
  restricted to S14 MH1 or MH2 by the gate definitions file it applies (prereg/run_2026-11-13-0552_PREREG_gate_definitions.md).

## 1. Detection, recomputed with my own code (written before I read the author's code)

My own SEED 2.4 / Steim2 reader (every record's reverse-integration constant checks), my own day arrays (samples
placed by record start time on a 6.625 Hz grid from 00:00:00, -1 = gap), my own preprocessing from the prose above
(mean demean, Hampel 7, whitening 0.1 Hz, scipy butter(4) band-pass 0.25-1.0 Hz run forward and backward,
decimation by 2 taking even samples) and my own sliding NCC, applied to waveforms/s14/xa.s14.00.mh{1,2}.1971.133.0.mseed
and the frozen templates frozen/s14_A38_1971_templates.npz (zero-mean, unit-norm, 2 x 1491).

| quantity | mine (prose reading) | mine (frozen-code choices) | claimed |
|---|---|---|---|
| window start | index 222513 of the 3.3125 Hz day grid = 18:39:33.736 UTC | same | 18:39:33.735 (truncated from .7358) |
| onset | 18:40:03.736 | same | 18:40:03.735 |
| NCC MH1 | 0.72692 | 0.72677 | 0.7268 (0.726768) |
| NCC MH2 | 0.75672 | 0.75672 | 0.7567 (0.756719) |
| D (two-channel mean) | 0.74182 | 0.74174 | 0.7417 (0.741743) |
| best lag within +/- 10 s | 0 | 0 | 0 |
| valid fraction in window | 1.000 / 1.000 | 1.000 / 1.000 | 1.0 / 1.0 |

The window is also the maximum of D over the whole of day 133 in my scan. "Frozen-code choices" are the author's
readings of open details (median demean, gaps filled with the median before the Hampel filter, whitening width
max(3, int(0.1/df)) bins, re-zeroing after whitening, invalid samples dilated by +/- 20 s, span = day plus the head of
the next day); they move D by 8e-5. Sensitivity noted, not a failure: with a 2nd-order prototype (literally 4 poles
for a band-pass) my D is 0.7208 (0.7039 / 0.7377), still >= 0.6 on both channels; the frozen code uses butter(4).

Other properties of the object, from my own code:
- Half-template correlations (Pearson per half): MH1 0.7283 / 0.7275, MH2 0.7576 / 0.7564; half-D 0.7430 / 0.7419
  (candidate.json 0.74318 / 0.74183). Both positive.
- Raw 450 s window (2981 samples from 6.625 Hz index 445026): median 477 / 501, MAD 4 / 6 counts (claimed 4.0 / 6.0);
  samples with |x - median| > 8 x max(MAD, 0.5): 0 / 0 (claimed 0 / 0); old rule max|x - mean|/MAD 6.22 / 6.20 < 8.
  My raw window equals package/object/g2_raw_window.csv sample for sample.
- Gap: valid fraction 1.00000 on both channels in [onset - 10 min, onset + 450 s + 10 min]; largest record timing
  gap or overlap on the whole day 1.1e-6 s (no discontinuity).
- Thermal (prereg formula, Meeus mean elongation): solar elevation at S14 61.26 deg (candidate.json 61.264).
- Provenance of the template: day 133 is not among the 11 catalogued 1971 A38 events, so the stack is not circular.
  My own correlation of the frozen template with those events gives D 0.66-0.80 for 1971-106 13:43, 187 10:55,
  297 11:08, 324 09:28 and 351 09:35, and 0.49 for 270 04:12. A plain stack of my own windows of the first five
  correlates 0.9999 (MH1) / 0.9975 (MH2) with the frozen template.

## 2. Null (C0 and C1..C400, full span 1971 days 36-365)

Reused (verified, not taken on trust): an earlier REPRODUCE instance's scratch output, outside claim/: its own
full-span null over days 36-365 (one JSON line per day) and the code that made it.
- Code review: its reader and preprocessing are its own and import nothing from claim/code/. It takes from the
  author's documented code the RNG convention for the phase randomisation (default_rng(20261112 + k).uniform(0, 2 pi,
  M//2 + 1), DC phase 0) and the frozen preprocessing choices listed in section 1, and it says so in its docstring. It
  uses float64 full-length FFT correlation instead of the author's float32 overlap-save blocks.
- Completeness: 330 records, days 36-365 each exactly once, rev_max present on every day, 400 control maxima on every
  day, no None entries. The author's results/null_A38_1971.jsonl passes the same completeness test.
- Agreement with my own code: I wrote my own null (own reader, own preprocessing, float64 FFT; same RNG convention,
  implemented by me) and ran it on 10 days: 133 (the candidate), 50 (largest C0), 351 (largest control, C367), 106
  and 187 (next largest controls), 160 (second largest C0), 365 (last day, uses the 1972-001 file), and 253, 95 and 37
  (among the gappiest days). On all 10 days my C0 and all 400 control maxima equal the earlier instance's values
  exactly and the author's to within 5e-6 (the author rounds to 5 decimals). Same best control on every day.
- Agreement with the author over the full span: largest difference between the earlier instance's 330 x 400 daily
  control maxima and results/null_A38_1971.jsonl is 5.3e-6; C0 differs by at most 1.5e-8.

Full-span maxima (from the verified earlier output; agree with results/ and package/object/null_full_span_maxima.csv):

| control | recomputed | claimed |
|---|---|---|
| C0 time-reversed | 0.212373 (day 50) | 0.21237 |
| best of C1..C400 | 0.286793 (C367, day 351) | 0.28679 |
| D of the candidate | 0.741743 | 0.7417 |

D exceeds all 401 full-span maxima (margin 0.455). package/object/null_daily_maxima.csv agrees with the recomputed
daily maxima to 1e-5 on all 330 rows.

Robustness of the null to the prose reading. The frozen code dilates invalid samples by +/- 20 s, which the prose does
not mention, so I also ran a complete second null with my own code under the prose reading only (day-only span, mean
demean, no re-zero after whitening, no dilation; same templates, controls, statistic and 90%-valid rule). This is a
different null, not a fourth run of the frozen one. It covers all 330 days 36-365: C0 plus 400 controls on every day,
no missing entries, gappiest days first, and the three days that were computed twice gave identical records.
- Full-span maxima under the prose reading: C0 0.21240 (day 50), best control 0.28674 (C367, day 351); D of the
  candidate under the same reading 0.74182. The candidate beats all 401 controls under both readings.
- The reading matters only near gaps: per-day control maxima move by up to 0.116 (day 36), 0.095 (day 37) and 0.083
  (day 38), but those days stay far below the full-span maxima.

## 3. PDS catalogue +/- 5 min (data/catalog/, my own parser)

All 11 tables listed in data/catalog/collection_data_inventory.csv are present, and each file's size equals the size in
the saved directory listing data/catalog_data_index_2026-11-13T083957Z.html (identical to data/catalog_data_index.html).
levent.1008weber.csv sha256 f95743b2...b0b9b93c as stated. I parsed every dated row: levent (13057 rows), gagnepian
2006, lognonne 2003 (three malformed 9-digit dates, none in 1971), nakamura 1979 SM locations, nakamura 1983 AI
locations, M arrivals and SM arrivals (13239 dated rows). The other four tables (AI arrivals, 2005 DM arrivals and
locations, weber 2011 S picks) carry no event times.
- Rows within +/- 5 min of the onset: none. Nearest: levent 71-133 16:03 (157.06 min before), 71-134 00:30 (349.94 min
  after), 71-133 11:51 (409.06 min before). These equal candidate.json's nearest_catalogue_rows_min (157.1, 349.9,
  409.1).
- Onset inside a levent start-stop span (9999 = to the next event): no. No span overlaps the 450 s window. The latest
  span before ends at 16:40 (120.06 min before the onset); that is CLAIM.md's "nearest 120 min" (package/README.md says
  it precisely: the nearest row starts 157 min before, its stop time is 120 min before).
- Not checked by me: the live re-fetch (NOVELTY's task) and the literature lists.

## 4. Glitch-catalogue gates G1 and G2 (data/lit_acc/, my own code)

- sha256: data/lit_acc/S14_ACC-Spike_MH1_all.csv 78e91b83...b6ac0a1 and S14_ACC-Spike_MH2_all.csv 1219c0fa...3bc9f9,
  equal to the values in CLAIM.md, the gate prereg chain and data/glitch_catalogue_record/members_sha256.txt.
- G1 on the full files (52458 MH1 rows, 50810 MH2 rows, both "00" and "01" trace ids): intervals overlapping
  [18:39:33.736, +450 s]: 0. Nearest start after the onset: MH1 +7347.962 s, MH2 +3013.925 s (claimed 7347.963,
  3013.925; the 1 ms difference is the onset's sub-ms digits). Last end before the window: MH1 -35349.094 s, MH2
  -32440.868 s (claimed -35349.093, -32440.867). Pass.
- Extract rule: my own extraction of every row whose start lies in 1971-02-05..1971-12-31 gives 9361 MH1 and 11394 MH2
  rows, equal row for row to package/object/glitch_catalogue_s14_acc_spike_mh{1,2}_1971d036-365.csv.
- G2: no overlapping spike and no rule-flagged raw sample, so nothing is muted; the NCC over unmuted samples is the
  plain NCC: 0.7268 / 0.7567, D 0.7417 at best lag 0 within +/- 10 s; best CC >= 0.6 and D > 0.2868. Pass.
- Context, disclosed in the claim and confirmed in the copies: the MH2 file has no interval between 09:39:22.9 and
  19:30:17.7 UTC on 1971-05-13 (a coverage hole of the catalogue that contains the window), so G1 passes in a stretch
  where the catalogue lists nothing at all. That limits what G1 can show; it is not a reproduction mismatch.

## 5. The author's commands (claim/REPRODUCE.md), rerun by me from a copy of claim/

Interpreter: the venv Python with -I; V3_WORKERS=4, OMP_NUM_THREADS=1; waveforms read in place.
- Step 1: all 667 entries of waveforms/SHA256SUMS_waveforms.txt OK (667 mseed files present).
- Step 2 (all 25 nests): out/templates.npz is byte-identical to frozen/s14_multinest_1971_templates.npz (sha256
  3b920aa0...cad2d64); its A38 slice equals frozen/s14_A38_1971_templates.npz.
- Step 3 (forward scan, days 36-365, 25 nests): 330 day records, identical to results/s14_multinest_scan_1971.jsonl
  on every day apart from the run-time field; day 133 A38 peak: window start 1971-05-13T18:39:33.735849Z, D 0.7417,
  0.7268 / 0.7567.
- Step 4 (seeds): out/seeds/seeds_summary.json byte-identical to results/seeds_summary.json; A38: 1904 peaks, one new
  seed with CC >= 0.6, the candidate (onset 1971-05-13T18:40:03.735Z, best CC 0.7567, D 0.7417). Cross-check from the
  verified independent null (forward daily maxima): every other 1971 day whose A38 maximum exceeds 0.6 is a catalogued
  event (1971-106, 187, 297 11:10, 324, 351, and 1971-160 17:05, a levent type-C row starting 17:05).
- Step 5 (fast_null.py) on days 133, 351 and 50: rev_max and all 400 ctrl_max identical to results/null_A38_1971.jsonl.
  Step 5b (score_scan.py, day 133, 400 controls): identical C0 and controls; its forward peak is window start
  1971-05-13T18:39:33.735849Z, D 0.74174, channels 0.7268 / 0.7567.
- Step 6 (seed checks, seeds file restricted to nest 38, nullmax {"38": 0.28679}): out/checks.json equal to
  results/seed_checks_final.json (gap ok, glitch ok, halves 0.7432 / 0.7418, thermal ok at 61.3 deg, no catalogue
  or Onodera match).
- Step 7 (gates): out/glitch_gates_A38.json byte-identical to results/glitch_gates_A38.json.
- Step 8 (object extracts): all five files IDENTICAL by sha256 to package/object/ (window_and_template.csv,
  null_full_span_maxima.csv, null_daily_maxima.csv, g2_raw_window.csv, g2_prepped_window_pm10s.csv).
- Step 9 (catalogue extracts): both files byte-identical to package/object/glitch_catalogue_*.csv. The survey commands
  need the Zenodo archive, which is not in claim/; not rerun (descriptive only).
- Step 10 (package checker): last line PASS.
- I did not rerun the 330-day null with the author's code: results/rebuild_rerun_checks.txt reports such a rerun, and
  the earlier REPRODUCE instance's independent null plus my 10-day check cover it.

## 6. Package checker (package/verify-it-yourself/check_p1.py) on clean and corrupted copies

Clean copy: PASS; three runs give byte-identical output (deterministic); sha256sum -c package/SHA256SUMS: all OK.
Corrupted copies I made ("re-signed" = OBJECT_SHA256.txt, and for extracts also candidate.json's hashes, rewritten to
match the corruption so that the hash check alone cannot catch it):

| corruption | checker | package SHA256SUMS |
|---|---|---|
| last digit of one data sample, not re-signed | FAIL (sha256) | FAIL |
| last digit of one data sample, re-signed | PASS (change 1e-12, below the 2e-4 tolerance) | FAIL |
| 500 data samples sign-flipped, re-signed | FAIL (NCC differs) | FAIL |
| template x 2, re-signed | FAIL (not unit-norm) | FAIL |
| window truncated to 999 rows, re-signed | FAIL | FAIL |
| one control raised to 0.75, re-signed | FAIL (D not above every control) | FAIL |
| one control row deleted, re-signed | FAIL (< 401 controls) | FAIL |
| C0 raised to 0.80, re-signed | FAIL | FAIL |
| candidate.json ncc_mh1 = 0.80, re-signed | FAIL | FAIL |
| nearest catalogue row set to 3 min, re-signed | FAIL | FAIL |
| spike interval overlapping the window added to the MH2 extract, re-signed | FAIL (G1) | FAIL |
| same, not re-signed | FAIL (sha256) | FAIL |
| nearest MH2 spike after the onset removed, re-signed | FAIL (G1 nearest differs) | FAIL |
| 1973 row appended to the MH1 extract, re-signed | FAIL (extraction rule) | FAIL |
| raw sample set to 5000 in the G2 raw window, re-signed | FAIL (G2 flags) | FAIL |
| noise added to the prepped G2 window, re-signed | FAIL (G2 NCC) | FAIL |
| object/null_daily_maxima.csv deleted | FAIL | FAIL |
| object/candidate.json deleted | FAIL (no traceback; ends in FAIL) | FAIL |
| candidate.json garbled, re-signed | FAIL | FAIL |
| an object CSV converted to CRLF | FAIL (sha256) | FAIL |
| README.md edited (not an object file) | PASS (outside the checker's scope) | FAIL |

Every material corruption fails. The two PASS rows are by design: the checker verifies numbers to a tolerance and
covers object/ only; the package-wide SHA256SUMS catches both.

## 7. Mismatches and doubts

- No numeric mismatch: every claimed number I could recompute agrees to its printed precision.
- Wording, "the S14 stack of six catalogued 1971 A38 deep-moonquake events" (CLAIM.md, README, candidate.json "6
  aligned catalogued 1971 A38 events"): I ran the author's builder for A38. It has six members by the pre-registered
  D >= 0.3 rule (1971-106 13:43, 187 10:55, 242 14:41, 297 11:08, 324 09:28, 351 09:35), but 242 14:41's windows
  fail the PREREG.v11 glitch screen (max|x|/rms > 8) on both channels and are left out. So each channel's stack is the
  mean of five events, and my five-event stack reproduces the frozen template (0.9999 / 0.9975). "Six members" is the
  prereg's own term and the template is the frozen one, so this is not a reproduction failure. A precise statement
  would be "six members, five contributing to each channel after the glitch screen". (The claim's original panel file
  original_panel/reproduce.md reports that a prose-written builder gave a different stack and CC 0.593; I did not
  re-litigate template construction, which the frozen builder defines and which reproduces byte for byte.)
- Code hashes: claim/code/tools/apollo_lib.py (76fda262...) and code/scripts/score_scan.py (be09787d...) differ from
  the sha256 values frozen in prereg/run1_PREREG.v2.md (d0b56748..., e7cfe2ab...). package/how-we-built-it/CHANGES_AFTER_FREEZE.md
  says only machine-specific paths were rewritten. I cannot check that from claim/ alone. My independent
  implementation reproduces the detection, and the frozen-code null to 5e-6, so whatever the shipped code does matches
  what the claim reports. The +/- 20 s gap dilation lives in this file and is not in the prose definition (see the
  robustness line in section 2).
- CLAIM.md's "(nearest 120 min)" is the stop time of the nearest row, not a row time (nearest row time: 157 min). Both
  are far outside +/- 5 min.
- Scope limits: catalogue tables were checked as saved copies, not re-fetched; the inter-station shift control of the
  bank criterion and the cross-nest look-elsewhere question are criterion matters and were not judged here.

## What I reused, what I recomputed

- Reused after verification: one earlier REPRODUCE instance's scratch output, outside claim/, namely its full-span
  null (330 days, C0 + 400 controls). Verification (section 2): its code is independent of claim/code/; the file is
  complete; it agrees exactly with my own code on 10 days (including day 133, the C0-max day and the best-control
  day) and to 5e-6 with the author's file on all 330 x 401 entries. I did not use the second earlier instance's outputs
  or its rerun of the author's commands; I reran the commands myself. I read no draft verdict or notes from either
  earlier folder.
- Recomputed with my own code: the Steim2 decoding of day 133, the detection (NCC per channel, D, lag, window
  start/onset), the half-template, gap, raw-glitch and thermal checks, the 10-day frozen-reading null, the complete
  330-day prose-reading null, the PDS catalogue +/- 5 min and span check over every dated row of every table, G1 and G2
  from the full data/lit_acc copies and their sha256, the extract rule, the template's member provenance, and the
  checker corruption suite.
- Rerun of the author's code: REPRODUCE.md steps 1-10 except the 330-day null and the three survey commands that need
  the Zenodo archive. Every output is identical to the saved one.

## Verdict

Reproduced. Every claimed value agrees, and my own code recomputes every in-scope number to its printed precision:
- the detection: 0.7268 / 0.7567, D 0.7417, window 18:39:33.736, lag 0;
- the null: C0 0.21237, best control 0.28679, D above all 401 full-span maxima, also under the prose reading;
- the catalogue check: no row within +/- 5 min, and the onset is in no levent span;
- G1 and G2: both pass, numbers as claimed, from catalogue copies whose sha256 match.

The author's commands reproduce byte for byte. The package checker passes clean and fails every material corruption,
and it is deterministic. Doubts, none of which is a mismatch: the template is described as a stack of six events but
five contribute to each channel (the sixth member is screened out by the pre-registered glitch screen), and the
wording should say so; two shipped code files differ from the frozen sha256 values (disclosed as path rewrites, not
checkable from claim/, numbers reproduced independently anyway); CLAIM.md's "nearest 120 min" is a stop time.

pass: true
