# REPRODUCE skeptic: p1 claim, new A38 member on S14 at 1971-05-13 18:40:04 UTC

context: subagent (fresh context, Claude Code Agent tool, subagent_type reproduce)
date: 2026-11-13 (UTC), work 00:40-01:38Z
scope: everything below was recomputed from the package (CLAIM.md, REPRODUCE.md, prereg/, data/, waveforms/, frozen/, results/, code/). My own scripts and outputs are in the panel's scratch folder p1_reproduce, outside the package (msr.py, prep.py, build_a38.py, build_a38_v.py, my_null.py, cand_checks.py, cat_check*.py, loo_and_pairs.py, compare_nulls.py). The claim folder was checksummed before and after: unchanged (731 files). The claim's code was run with python -I -B, 1 FFT thread (V3_WORKERS=1, OMP_NUM_THREADS=1), with outputs written to the scratch folder.

## Order of work (kit rule: own checker first)

Before reading any of the claim's code I wrote my own tools from the definitions in prereg/:

- MiniSEED v2 / Steim2 reader (msr.py), written from the SEED manual. Every record of the 664 S14 files and the S12 files decoded with the reverse-integration-constant check passing. Day 133 has 87 records per channel, 572,436 samples at 6.625 Hz, no inter-record gaps above one sample.
- Preprocessing (prep.py) from prereg/run1_PREREG.v2.md, quoted: "Despike: Hampel filter, window 7 samples, a sample is replaced by the running median when it deviates by more than max(3 DU, 5 x 1.4826 x running MAD)"; "each day span is divided in the frequency domain by the running mean of its amplitude spectrum over 0.1 Hz before band-passing"; "band 0.25-1.0 Hz (4-pole zero-phase Butterworth), whitening 0.1 Hz, decimation 2 (3.3125 Hz), L = 450 s (1491 samples)". My reading where the text is open: NaN-aware Hampel, butter(4) run forward and backward (sosfiltfilt), every second sample, no dilation of gaps.
- Statistic, from prereg/PREREG.md: "D14 = mean single-channel NCC over MH1/MH2 (both valid)", where a channel is valid with ">= 90% valid samples" in the window. Pearson NCC per window.
- Stack builder (build_a38.py), from run1_PREREG.md and v2 items 3-5: iterative alignment within +/- 240 s of the catalogued start, members with D >= 0.3, 4 iterations, onset picked on the stack envelope, window starting 30 s before the onset, and the v11 screen (max|x|/rms > 8 left out).
- Null (my_null.py), from run1_PREREG.md "Null design": C0 is the templates on time-reversed data. C1..C400 apply one set of uniform random Fourier phases (seed 20261112 + k) to both channels' template spectra, run on forward data, maximum over the full span.
- Candidate checks (cand_checks.py), from the "Candidate checks" rules: gap, glitch, template halves and thermal. For the thermal check I used my own ephemeris: synodic age counted from the new moon of 2000-01-06 18:14 UTC.

Then I read code/ and ran the claim's own pipeline (REPRODUCE.md steps 1-6, all of them) for an exact comparison.

## Numbers recomputed (mine vs claimed)

| quantity | claimed | claim's code rerun by me | my independent code |
|---|---|---|---|
| waveform sha256 (667 files) | waveforms/SHA256SUMS_waveforms.txt | 667/667 OK | - |
| A38 template (frozen/s14_A38_1971_templates.npz) | 6 members, onset 101.4 s | rebuilt bit-identical; all 25 nest templates bit-identical to frozen/s14_multinest_1971_templates.npz; build stdout identical to results/build_stdout.txt | see "Stack from catalogue times" below |
| candidate window start | 1971-05-13 18:39:33.735 | 18:39:33.735 | D peak at 18:39:33.736 (frozen template) |
| CC S14 MH1 | 0.7268 | 0.7268 | 0.7225 |
| CC S14 MH2 | 0.7567 | 0.7567 | 0.7545 |
| D14 (2-channel mean) | 0.7417 | 0.7417 (day-133 scan line identical; score_scan fwd_max 0.74174) | 0.7385 |
| C0 time-reversed, full-span max (days 36-365) | 0.2124 | 0.2124 (day 50) | 0.2136 (day 50) |
| best of C1..C400, full-span max | 0.2868 | 0.2868 (control 367, day 351) | 0.2956 (same control 367, same day 351) |
| null file results/null_A38_1971.jsonl | 330 days | 330/330 day records identical, only the wall-clock "seconds" field differs; day 133 also identical with code/scripts/score_scan.py | per-control full-span maxima vs shipped: corr 0.963, mean abs diff 0.003 |
| real beats all 401 controls | yes | yes (0.7417 > 0.2868) | yes (0.7385 > 0.2956) |
| seeds (results/seeds_summary.json) | A38 one seed | regenerated identical | - |
| checks (results/seed_checks_final.json) | all pass | regenerated identical | see below |
| gap [onset-10 min, onset+L+10 min] | valid 1.0, disc 0 | identical | 10,931/10,931 samples valid on both channels, no -1, no record discontinuity |
| glitch, 8 x MAD in raw window | none; MAD 4.0 / 6.0 DU | identical | max deviation 6.50 x MAD (MH1, MAD 4.0 DU) and 6.33 x MAD (MH2, MAD 6.0 DU): no spike |
| template halves | 0.743 / 0.742 | identical | 0.739 / 0.739 |
| solar elevation at S14 | 61.3 deg | identical | 63.2 deg with my own ephemeris (55-71 deg if the elongation is off by +/- 8 deg); far from the 12 deg limit |

Both nulls were run over the full stated span, all 330 days (1971 days 36-365), with nothing sampled. My own null covered the frozen template with 400 controls (about 9 s per day, 53 min). The claim's code/tools/fast_null.py, rerun at one thread, took about 6 s per day (34 min).

## PDS tables (R6) and live state

- data/catalog/levent.1008weber.csv sha256 f95743b2...b0b9b93c matches CLAIM.md. All 11 local tables match the sizes in data/catalog_data_index.html.
- Live check at 2026-11-13T00:06-00:07Z, one HEAD per table 4-5 s apart, plus one GET of levent. All 11 tables returned 200 with the same Content-Length as the shipped copies; Last-Modified dates are 2018-2019. The live levent.1008weber.csv is byte-identical to the shipped file.
- My own parse of levent: no row on 1971-133 within +/- 90 min of 18:40:04. The nearest rows are 16:03-16:40 (type C, 157 min before) and 1971-134 00:30 (350 min after). No start-stop span (9999 resolved to the next row) covers the onset.
- The other tables (gagnepian_2006, lognonne_2003, nakamura_1979_sm, nakamura_1983 ai/m/sm) have no row on 1971-05-13. The 2005 DM and 2011 S-pick tables have no times.
- The claim's code/tools/catalog_check.py gives the same answer (catalogued: []).

## Is it really A38? (independent checks)

- All 25 frozen nest templates were run with my pipeline at the candidate time. A38 gives 0.7385; the other 24 nests give at most 0.175 within +/- 10 min, which is the day-133 background. The same run recovers the catalogued A7 (0.83) and A22 (0.73) events that day, so the pipeline is sane.
- The candidate window correlated with each 1971 catalogued A38 event separately (my code): 1971-187 0.697, 1971-106 0.622, 1971-324 0.501, 1971-351 0.507. The claim's results/member_similarity.txt gives 0.704 and 0.625. Since none of these is near 1.0, the candidate is not a duplicated copy of a catalogued event.
- Timing fits the monthly recurrence: A38 catalogued 1971 days 81, 106, 186/187; the candidate is day 133 (106 + 27). There is also an A38-like peak at day 160 17:05 (D 0.649), which levent lists as type C. The claim gives the anomalistic phase as 279 deg, 0.2 deg from the nearest catalogued member.
- In my full-span forward scan with the frozen template, the candidate is the fifth-highest daily maximum of 1971 (0.739). The four above it are in-sample stack members (days 187, 106, 351, 297), and the next is the type-C row on day 160.

## Stack from catalogue times: sensitivity (caveat, not a mismatch)

- My builder, written from the prose, applied the >8 max|x|/rms screen on a long window [S-120 s, S+720 s]. That excluded 1971-106 and 1971-242 14:41, so my stack has 5 members per channel (187, 270, 297 11:08, 324, 351) and a different onset pick.
- With that stack the candidate's best single-channel CC is 0.593 at my own onset-defined window (D 0.592). It is 0.60-0.64 for window starts from S_ref+20 s to S_ref+220 s (0.626 at the claim's window position) and 0.56-0.60 for earlier windows.
- In my full-span null for this stack the candidate still beats every control by a wide margin: C0 max 0.2108; best of 100 phase-randomised controls 0.2592.
- The difference comes from stack membership, not from a computation error. With the claim's six members (106, 187, 242 14:41, 297 11:08, 324, 351), my own alignment and stacking code gives D 0.733-0.745 and MH2 0.75-0.76 around the claim's window position, which reproduces the claimed value independently.
- The prereg names the builder explicitly ("tools/nesttemplates2.py; reference = largest positive A1 + A2 among events whose reference-window channels pass the screen", prereg/PREREG.md). In this package that is code/tools/nesttemplates2.py, called by code/scripts/s14_multinest_build.py. It uses only catalogued 1971 events, never the candidate, and rebuilds bit-identically. The claimed object is therefore the stack the prereg fixed.
- Leave-one-out context (my code): each of the six members against the stack of the other five reaches a best single-channel CC of 0.31-0.68. The candidate's 0.757 against the six-member stack is at or above what catalogued members reach, so the CC >= 0.6 bar holds firmly for the stated stack. It is construction-dependent near 0.6 for other reasonable stacks. The CRITERION skeptic may want to weigh this.

## Determinism

The template build, seeds, checks, day-133 scan, day-133 score_scan and the 330-day null all reproduced bit-exactly, apart from timing fields. No non-determinism was found.

## Not covered by this check

- I did not rerun the 330-day forward multinest scan (REPRODUCE.md step 3), only its day-133 line. It is identical, and the seeds were regenerated from the shipped scan and are identical. The p1 claim needs only that the candidate exists and passes the bars, which was verified directly.
- The bank's "shifted between stations" null cannot be applied to a single station. The time-reversed control C0, which is literal to the bank, is beaten (0.742 vs 0.212), and so is the phase-randomised replacement. Whether that replacement is acceptable is a criterion question, not a reproduction question.

## Verdict

Every claimed number reproduces exactly with the package's own code. My independently written reader, preprocessing, NCC and full-span null (330 days, 401 controls) agree within 0.004 on the candidate (D 0.7385 vs 0.7417; MH2 0.7545 vs 0.7567) and within 0.009 on the null maximum (0.2956 vs 0.2868). The candidate beats every control by a factor of about 2.5. The gap, glitch, halves and thermal checks pass with my own code, and no PDS catalogue row, re-checked live, lies within 90 min. The only reservation is the stack-construction sensitivity above, and the stated, preregistered six-member stack meets CC >= 0.6 robustly. I found no mismatch, missing object or non-determinism.

pass: true
