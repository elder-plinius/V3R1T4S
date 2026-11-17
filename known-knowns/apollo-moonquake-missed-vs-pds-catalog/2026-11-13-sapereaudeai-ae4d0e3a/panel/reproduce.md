# REPRODUCE verdict: apollo-moonquake-missed-vs-pds-catalog, A100-like event 1973-10-30 02:25:51.5 UTC (S14 + S16)

context: fresh subagent started with the Claude Code Agent tool (subagent_type reproduce), one of three independent skeptics; I saw only claim/ and the panel prompt (not attempts/, the run's own PREREG.md, other panel files or other roles' work folders).

## Method

I wrote my own reader and checker from the definitions in claim/prereg/ (PREREG.md and the inherited run1_PREREG.md, .v2, .v4, .v5, .v11, .v14, .v15, fullwin_claim_PREREG_fullwin.md) and claim/data/target_bank_entry.md before opening claim/code/. The definitions are quoted at the top of each script in panel_work/reproduce/:

- rp_lib.py: MiniSEED reader (vectorised Steim2 with every record's reverse integration constant checked; float64 for ATT); day grid at 6.625 Hz from record start times, -1 = gap; demean, Hampel despike (7 samples, max(3 DU, 5 x 1.4826 x running MAD)), whitening (running mean of |X| over 0.1 Hz), 4-pole Butterworth 0.25-1.0 Hz forward-backward, gaps re-zeroed, decimation by 2 on the midnight grid (phase 0); Pearson NCC with >= 90 % valid samples per channel window; station means over valid channels (>= 1); +/- 7-sample running max; Dt = min of the two stations.
- scan_null.py: all 365 days of 1973 with the A100 stack: forward declustered peaks (+/- 5 min), C0 (all channels time-reversed within the day span) and C1..C400 (S16 circularly rolled by round((3600 + 180 k) x 3.3125) samples within the span, exact through circular correlation), and the A5 reverse search (variants b and a) in the same pass. Day span = the day plus 12000 raw samples (30.2 min) of each neighbouring day. Run time 716 s, one process.
- analyse_scan.py (N0, rank, A6, R8 inputs, C6/C6b), cand.py and cand_detail.py (candidate numbers, gap, glitch rule, G1/G2, C1, C2), c3.py (C3), r8.py (R8), checks_cat.py (R6 over every timed PDS table, Onodera, R9 interval, thermal), stack_check.py (rebuild of the A100 stack from its 5 catalogued members, both decimation phases), s12.py (S12 third station), m1.py (M1/M2 recomputed from the claimant's scan file), cmp_scans.py / cmp_partial.py (field-by-field scan comparisons). Outputs: *_out.txt next to each script.

Only afterwards did I read claim/code/ (tools/apollo_lib.py, tools/att_moveout.py, scripts/lagtol_scan_1416.py) to trace the differences listed below.

## Integrity

- claim/waveforms: sha256sum -c SHA256SUMS_waveforms.txt: 1493 of 1493 OK; listed and present file sets identical.
- claim/data/lit_acc: 18 of 18 OK against SHA256SUMS.txt.
- claim/frozen/nets25_1973.npz sha256 aa0b9b8a...b4b9009 equals claim/results/hashes_before_scan.txt; its A100 entry equals claim/frozen/nets25_1973_A100.npz exactly; templates zero-mean, unit-norm, 1491 samples.
- claim/code/tools/*.py and code/scripts/lagtol_scan_1416.py sha256 equal claim/results/hashes_before_scan.txt (and run1_PREREG.v2.md where listed).
- My Steim2 decoder found no reverse-constant mismatch in any record it read (all S14/S16 MH1/MH2 files of 1973 and 1974-001).
- The A100 stack is what it says: rebuilding a plain stack from the 5 stated catalogued members (levent 73-085 1420, 139 2252, 194 1220, 248 2148, 357 1553) with my own code gives Pearson 0.999 / 0.924 / 0.999 / 0.996 with the frozen stack on S14 MH1 / S14 MH2 / S16 MH1 / S16 MH2. The candidate day is not a member.
- Observation: claim/code/tools/__pycache__/ (4 .pyc files) was created at 17:28-17:30Z during the panel by a process that was not mine. No source file changed. To rerun the claimant's code I copied code/, frozen/nets25_1973.npz and the PDS inventory into panel_work/reproduce/ccopy/ and pointed APOLLO_WF at claim/waveforms, so nothing was written into claim/.

## The claimed event: claimant vs my independent pipeline (frozen A100 stack, day 1973-303)

| quantity | claimant | mine |
|---|---|---|
| Dt at window start 02:25:21.509 | 0.29806 | 0.29844 |
| S14 lag / S16 lag | -1.509 s / -0.906 s | -1.509 s (-5) / -0.906 s (-3) |
| S14 MH1, MH2 NCC | 0.4936, 0.6211 | 0.4991, 0.6298 |
| S16 MH1, MH2 NCC | 0.6196, -0.0235 | 0.6201, -0.0232 |
| station means S14 / S16 | 0.557 / 0.298 | 0.5645 / 0.2984 |
| C2: best station mean > 7 samples away (within +/- 30 s), S14 / S16 | 0.349 / 0.117 | 0.358 / 0.118 |
| template halves S14 / S16 | 0.597, 0.584 / 0.299, 0.299 | 0.571, 0.554 / 0.298, 0.299 |

A direct (non-FFT) NCC at those lags gives the same four values as my FFT series. With a 2-pole Butterworth instead of 4 (the "4-pole zero-phase" text is ambiguous): S14 0.474 / 0.606, S16 0.620 / -0.022, Dt 0.299. With my own stack rebuilt from the catalogued members (phase 0): Dt 0.294, S14 0.496 / 0.607, S16 0.617 / -0.028. R7 holds in every variant.

## Bank clauses (pre-registered readings), recomputed

- Null over the full searched span (N0), all 365 days, all 401 controls, my code: C0 (time-reversed) full-span max 0.13183; best of 400 shifts 0.17136 (k = 341, day 152); real 0.29844 > all 401 (margin 0.127). Claimant: C0 0.15744, best shift 0.19062, real 0.29806. PASS in both. My controls are lower; the per-day maxima of the two implementations correlate only 0.23 and the claimant's are higher on 300 of 364 days (mean +0.012). Likely cause (from reading claim/code/ after my run, not isolated by experiment): the claimant's code dilates every gap by 20 s and so invalidates more channel windows (more one-channel station means, which have heavier tails; its top control days have coverage 0.59-0.93), has no pre-midnight pad, and uses a filtered rather than an exact running MAD. None of this is fixed by the prereg text; the claimant's null is the more conservative of the two, and the real value is the same to 0.0004 in both.
- R7: best single channel S14 MH2 0.6298 (claimed 0.6211), S16 MH1 0.6201 (0.6196), each at its own lag within 7 samples. PASS.
- R8: ATT-corrected S16 - S14 for the candidate 0.715 s (claimed 0.71). Reference events = catalogued 1973 A100 events above my null: 01-03, 05-19, 07-13, 09-05, 12-23 (5; the claimant has these plus 08-09, which in my scan reaches 0.168, below my null). My values -0.48, 0.89, 0.62, -0.30, 0.95 (claimant -0.48, 0.89, 0.92, 0.74, -0.30, 0.95), median 0.618 (with 08-09 added at my lags: 0.161) vs the claimant's 0.82. |candidate - median| 0.097 s (0.554 s with 6 references). With the most literal reading of v5 ("the ATT value of the nearest sample", no within-frame offset) the candidate is 1.216 s and |diff| 0.587 s (1.048 s with 6). PASS under every variant (limit 2 s).
- R9: shortest circular arc holding 95 % (59 of 62) of all catalogued A100 events: [46.71, 318.34] deg (claimed [46.70, 318.34]); candidate mean anomaly 161.49 deg (claimed 161.49). PASS.
- Gap: 100 % valid on S14 MH1/MH2 and S16 MH1/MH2 in [onset - 10 min, onset + 450 s + 10 min]; no inter-record gap or overlap above one sample in that span. PASS.
- Thermal: solar elevation S14 -65.6 deg, S16 -32.4 deg (claimed the same; my station coordinates are my own input, not from claim/). PASS.
- Glitch rule: S14 raw window MAD = 0 DU (digitiser-level data, max |x - median| 2 DU), S16 MAD 1 DU (max 3 and 4 DU). With the frozen rule's floor, |x - median| > 8 x max(MAD, 0.5): no sample flagged on any channel. Template halves positive at both stations. PASS. See ambiguity G-1 below for the literal MAD = 0 reading.
- G1 (Liu, Xiao and Li 2025): no Spike / Step-Up / Step-Down interval on MH1, MH2 or MHZ overlaps either window; nearest S14 entry ends 1250 s before the onset (Step-Up MH1 02:04:41-02:05:01), nearest S16 entry starts 5730 s after (Step-Up MH1 04:01:21). Entries on days 302/303/304: S14 39/34/35, S16 35/24/30. All equal to the claim. G2: nothing to mute, so G2 = unmuted values, Dt 0.2984 > both nulls. PASS.
- R6: no row of levent.1008weber.csv (13057 rows) or of the other timed tables (259 rows in gagnepian_2006, lognonne_2003, nakamura_1979_sm, nakamura_1983_ai/m/sm) within +/- 5 min (+59 s) of the onset or the window start; neither time inside a levent start-stop span (9999 = to the next row). Nearest levent row 73-303 0100 (A1): start -85.9 min, stop -25.9 min. Onodera SP windows: none within 5 min; nearest S16 id 2014 at +220.1 min (S14 +347.9 min, S15 1349.9 min). Three lognonne_2003 Date values are malformed (761142313, 7704712332, 721081524), none from 1973-10. PASS on the tables as saved; the live re-fetch is NOVELTY's.

## Attribution tests (recomputed with my code)

- C1: against all 12 frozen stacks (max Dt within +/- 10 min) only A100 has NCC >= 0.5 at either station; the other 11 reach Dt 0.082-0.148 (claimed 0.082-0.145), their best single channel at most 0.470 (A201 S16 MH2). C1 does not hold.
- C2: does not hold (above table: in-window maxima are the claimed lags; outside +/- 7 samples at most 0.358 at S14 and 0.118 at S16).
- C3 (S16 MH2 state): candidate R_MH1 2.207, R_MH2 1.068, r2 0.056 (claimed 2.179, 1.050, 0.042). Nearest references: 73-303 0100 A1 r2 0.029 (claimed 0.030) and 73-303 0739 A8 r2 -0.103 (claimed -0.051); both <= 0.25, so S16 MH2 unresponsive, no contradiction. The six levent rows within +/- 24 h with defined r2: -0.103 to 0.070 (claimed -0.05 to 0.08). Same decision.
- C6 / C6b (reverse search, my scan, variant b decides): top 10 of 998 catalogued 1973 deep moonquakes = 6 A100 events (05-19 0.491, 09-05 0.482, 12-23 0.421, 01-03 0.334, 07-13 0.231, 08-09 0.165) then A418 0.148, A235 0.141, A386 0.140, A1 0.137. C6 does not hold. Random 15-min windows: 99th percentile 0.119, max 0.145 (claimed 0.127, 0.152). Best A35 0.1235, A7 0.1008, A244 no events: C6b does not hold. Variant a also has 6 A100 events in its top 10. Score near the first claimed event (11-26): 0.414 (claimed 0.402).
- A6 (my scan): against the A100 stack, null + R7 + R9 are passed by 3 of 14 catalogued A100 events and 0 of 984 other catalogued 1973 deep moonquakes (claimed the same).
- Moveout table (Nakamura 2005 S picks): A100 16S - 14S = -80 s; A35 -79, A244 -78 (within 2 s), A7 -76 (within 5 s): equal to the claim.

## Multiplicity

- M1 and M2 recomputed with my own code from claim/results/scan12_1973.jsonl: per-nest C0 / best shift / median equal to results/n0_stdout.txt for all 12 nests; A100 median 0.1603, robust sd 0.0079, z_c 17.47; family-wise maxima T: max 14.36 (A20), none >= z_c, p_FW = 1/402 = 0.0025; Bonferroni 12/402 = 0.0299, 26/402 = 0.0647, 55/402 = 0.1368; GEV shape -0.000, loc 0.1569, scale 0.0066, tail 4.655e-10, Sidak(12) 5.587e-09, x55 2.560e-08. All equal the claim. results/n0_A100_control_maxima.csv equals the maxima I derive from the scan file (max abs difference 0). Candidate rank 9 of 65910 A100 peaks and 11 above 0.19062, recounted from the scan file: equal.
- In my own scan: rank 6 of 46950 forward peaks, 9 above my null; a GEV fit to my 401 control maxima gives 4.2e-12 (model-based). The empirical per-template bound is 1/402 in both.
- M3 (the counts 55 and 26 of parent-run scans) come from parent-run build logs that are not in claim/: not checked.

## Robustness (reported, not gated)

- D1, other decimation phase, my own stack rebuild from the 5 members: Dt 0.366, S14 MH1 0.376 / MH2 0.5001 (lag -6), S16 MH1 0.747 / MH2 -0.015 (claimed with the claimant's builder: S14 MH2 0.621, S16 MH1 0.587, Dt 0.282). With my rebuild the S14 best channel sits at the 0.5 threshold on the other grid.
- S12 third station with the frozen S12 + S14 A100 stack: Dt 0.366 (claimed 0.3605); S12 0.360 / 0.502 / 0.514, S14 0.358 / 0.374 (claimed 0.365 / 0.510 / 0.514 and 0.355 / 0.366).
- So the S14 match is the weakest part of the event: 0.61-0.63 with the S14 + S16 stacks on the frozen grid, 0.50 with my other-phase rebuild, 0.37 with the S12 + S14 stack. The gated value (pre-registered stack and grid) is above 0.5 in both implementations; the claim discloses the S12 + S14 number.
- S14 energy above noise (my C3 formula on S14): R_MH1 1.50, R_MH2 1.87 (claimed 1.59 / 1.86, descriptive).

## Mismatches (both values), cause, gate impact

1. Per-channel NCC and Dt differ in the 3rd decimal (e.g. S14 MH2 0.6211 vs 0.6298; Dt 0.29806 vs 0.29844). Cause: implementation choices the prereg text leaves open (claimant despikes before demeaning and replaces gaps by the median first, dilates gaps by 20 s, whitening width floor(0.1/df) and |X| floor 1.0, no pre-midnight pad, MAD by a median filter of |x - med|; mine an exact running MAD and +/- 30 min pads). No gate changes.
2. Null maxima: C0 0.15744 vs 0.13183, best shift 0.19062 vs 0.17136. Same cause, mostly the gap handling. Real beats every control in both; no gate changes.
3. Template halves S14 0.597 / 0.584 vs 0.571 / 0.554. Positive in both; no gate change.
4. R8 reference values and median: claimant 6 references, median 0.82 s; mine 5 references (08-09 below my null), median 0.618 s (0.161 s with 08-09). 07-13 and 08-09 differ through the station lags: at 07-13 the claimant's S14 MH2 is invalid (None in results/n0_stdout.txt; most likely its 20 s gap dilation) while mine is valid at 0.18, and at 08-09 my nominal S16 - S14 lag difference is -1.81 s against the claimant's -0.60 s. Candidate within 2 s under every variant, including the literal "ATT value of the nearest sample" reading (1.216 s). No gate change.
5. C3 values: r2 0.056 vs 0.042; A8 reference -0.103 vs -0.051. Same decision.
6. Reverse search: 07-13 0.231 vs 0.323, 08-09 0.165 vs 0.231, random 99th percentile 0.119 vs 0.127; A35 best 0.1235 vs 0.118; A7 0.101 vs "scores 0". The descriptive "A100 median rank 2 of 98 nests" is 17 of 98 in my variant b (3 in variant a): the median of 14 A100 scores falls between the 7th and 8th values, and the 8th (02-27) is just above the 0.10 peak threshold in the claimant's scan (0.1008) and below it in mine. Not a gate (SUPPORTED by top-10 count holds in both: 6 A100 events).
7. Glitch rule, ambiguity G-1: run1_PREREG.md says "exceeds 8 times the window's median absolute deviation"; on S14 the MAD is 0 DU, so the literal rule flags 974 (MH1) and 1231 (MH2) samples. The G2 text of PREREG.md calls the frozen rule "|x - median| > 8 x max(MAD, 0.5)", under which nothing is flagged. Under the literal reading the rule's exception still applies per channel: Dt with S14 MH1 removed or with S14 MH2 removed stays 0.298 (claimant's Dt_without 0.29805), above the null. No gate change unless one reads "without that channel" as removing both S14 channels at once, which the text does not say.
8. CLAIM.md says the rerun scan is "byte-identical" to the lens scan. The files are not byte-identical (78416461 vs 78410618 bytes; sha256 f6a5b5e7... vs dd6b8fb4...): the rerun adds a "seconds" timing field to each day. The science fields (fwd_peaks, rev_max, scanned, shift_max) are identical on all 365 days for all 12 nests (my own comparison), which is what results/n0_stdout.txt states. Wording only.
9. CLAIM.md: "A35 (5 N, 36.1 E) lies inside that ellipse" of A100 (-2 +/- 4.2 N, 32.2 +/- 17.1 E). With those errors as semi-axes A35's normalised distance squared is 2.83: outside the 1-sigma ellipse, inside a 2-sigma one. Descriptive; strengthens rather than weakens the stated caveat that A35 cannot be excluded.

## Determinism

- Claimant's frozen scan rerun by me: copy of claim/code/ in panel_work/reproduce/ccopy/, waveforms read from claim/waveforms (APOLLO_WF), `run_capped.py scripts/lagtol_scan_1416.py frozen/nets25_1973.npz 1973 1 365 out/scan12_1973.jsonl 400`, V3_WORKERS=1, one process (about 340 MB), 17:38-18:12Z. All 365 days, all 12 nests: fwd_peaks, rev_max, scanned and shift_max identical to claim/results/scan12_1973.jsonl (and therefore to data/lens_scan_1973.jsonl, see mismatch 8); only the run-time field "seconds" differs.
- The claimant's code/c1030/n0_analyse.py on my rerun output reproduces results/n0_stdout.txt, results/n0.json and results/n0_A100_control_maxima.csv byte for byte.
- My own pipeline has no random element except the seeded random-window baseline; the candidate numbers from cand.py, cand_detail.py and the full scan agree with each other (Dt 0.29844, same per-channel values).

## What I did not check

- Knapmeyer-Endrun and Hammer 2015 Tables S1-S3 (no .xls reader available without installs). Bulow et al. 2005 Table 2: text extracted with pypdf; the 1973 entries nearest the candidate are day 309 05:03 (1973-11-05, +146.6 h) and day 202 18:34, as claimed; multi-column extraction could miss rows.
- The live PDS re-fetch and the 24-month literature search (NOVELTY's).
- M3 counts (55, 26), G3 base rate, the coda profile, A4 phase listing and A3b beyond the values above.
- I did not rerun the claimant's per-candidate scripts (cand12, r8, glitch, G1/G2, A1/A2, A3, A5, D1, S12); I recomputed those quantities with my own code instead (above).

## Summary of coverage

- Recomputed independently with my own code: waveform and catalogue hashes; the candidate's Dt, per-channel NCC, station lags and station means; the bank null over all 365 days of 1973 with all 401 controls (C0 + 400 shifts) and the candidate's rank; R6 (all timed PDS tables as saved, levent spans, Onodera); R7; R8 (ATT, two conversions, reference events from my scan); R9 (95 % arc from the 62 catalogued A100 events, mean anomaly); gap; thermal; frozen glitch rule (both MAD readings) and template halves; G1/G2 against data/lit_acc; C1 (12 stacks); C2; C3; C6/C6b and the random-window baseline (my reverse scan, both variants); A6; moveout table; D1 and stack provenance (my own stack rebuild, both phases); S12 third station; S14/S16 energy ratios; M1/M2 arithmetic and the rank/count of the claimant's A100 peaks (my code applied to the claimant's scan file); the field-by-field comparison of the two saved scans.
- Rerun with the claimant's code: the full 12-nest frozen scan of 1973 and n0_analyse.py (identical outputs, above).
- Not checked: listed in the previous section.

## Verdict

All bank clauses that can be checked from the saved package reproduce with independently written code under the pre-registered readings: the candidate's Dt (0.2984 vs 0.2981) exceeds the full-span maximum of every one of 401 controls over all 365 days of 1973 in my implementation (best 0.1714) as in the claimant's (best 0.1906); R7 (S14 MH2 0.630, S16 MH1 0.620), R8 (0.715 s, within 2 s of the nest median under every reference set and ATT reading), R9 (161.49 deg in [46.71, 318.34]), gap, thermal, glitch rule, G1/G2 and R6 on the saved tables pass; none of the attribution attacks C1, C2, C3, C6, C6b holds; the multiplicity numbers recompute exactly from the claimant's scan; the claimant's scan is deterministic. Every numerical difference traces to implementation choices the prereg text leaves open and none changes a gate. Caveats for the other panelists and the reader: the null maxima depend on gap handling at the 0.02 level; the S14 match depends on the stack (0.63 frozen, 0.50 with my other-phase rebuild, 0.37 with the S12 + S14 stack); the per-channel R7 reading carries the claim at S16 (station mean 0.298 because MH2 is unresponsive), which is the CRITERION skeptic's question, not a reproduction failure; CLAIM.md overstates "byte-identical" and "inside that ellipse" (mismatches 8, 9) and its "A100 median rank 2 of 98" is fragile (mismatch 6).

pass: true
