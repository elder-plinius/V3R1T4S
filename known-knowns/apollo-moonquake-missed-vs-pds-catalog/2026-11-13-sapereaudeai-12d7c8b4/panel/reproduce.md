# REPRODUCE skeptic: p1 claim, nest A39 member on S14 at 1971-09-05 01:26:14 UTC

context: subagent (fresh context, Claude Code Agent tool, subagent_type reproduce)

Evidence used: claim/ only. All reruns used the saved files in claim/ (no network). Resource caps: at most two
single-thread processes at a time.

## Definitions checked against (quoted from claim/prereg/)

- prereg/run1_PREREG.md: "Statistic D(t) = mean over available components of the single-channel normalised
  cross-correlation at common lag t. D is defined only where >= 2 of 3 components have >= 90% valid samples in the
  window." prereg/run1_PREREG.v12.md: "D14 = mean single-channel NCC over MH1/MH2 (both valid)."
- prereg/run1_PREREG.v2.md: "FROZEN: band 0.25-1.0 Hz (4-pole zero-phase Butterworth), whitening 0.1 Hz, decimation 2
  (3.3125 Hz), L = 450 s (1491 samples)"; "Despike (added): Hampel filter, window 7 samples, a sample is replaced by
  the running median when it deviates by more than max(3 DU, 5 x 1.4826 x running MAD)"; "each day span is divided
  in the frequency domain by the running mean of its amplitude spectrum over 0.1 Hz before band-passing".
  prereg/run1_PREREG.md: "Daily arrays at 6.625 Hz on a uniform grid from record start times; -1 samples and missing
  records are gaps."
- Null (run1_PREREG.md): "C0 (bank-literal for one station): the frozen templates correlated with the time-reversed
  data of every scanned 1971 day"; "C1..C400: 400 phase-randomised templates (for each control, one set of uniformly
  random Fourier phases, seed 20261112 + k, applied to all three components' template spectra ...; amplitude spectra
  unchanged)"; "real candidate D must exceed the full-span maximum of D in every control C0..C400 (401 controls)".
  Span (PREREG.v12): "1971 days 36-365".
- R6: "a candidate is not new if any row of any table of the PDS catalogue data directory has a time within +/- 5 min
  of the candidate onset, or if the onset lies between a levent row's signal start and its stop time".
- Checks (run1_PREREG.md, PREREG.v9): gap ">= 99% valid samples on every used component in [onset - 10 min, onset +
  window + 10 min]; no record timing discontinuity"; glitch "no sample in the demeaned raw window exceeds 8 times the
  window's median absolute deviation ... unless D stays above [the null maximum] with that component excluded; CC
  computed separately on the first and second halves of the template must both be positive"; thermal "|solar
  elevation at S14| > 12 deg" (subsolar longitude 180 deg minus the Meeus mean elongation).
- prereg/PREREG.md G1: "no catalogued ACC-Spike interval [start, end] on S14 MH1 or MH2 overlaps the 450 s template
  window". G2: mute "every raw sample flagged by the frozen glitch rule ... each from 5 s before to 5 s after.
  Statistic: NCC over the unmuted samples (template and data muted at the same samples), best lag within +/- 10 s.
  Pass: best single-channel CC >= 0.6 and the two-channel mean above the null maximum 0.318."

## Independent code (written from the definitions above before reading the claim's code)

My own MiniSEED Steim2 decoder, day grid from 00:00 at 6.625 Hz placed by record start times, mean removal, Hampel
despike (7 samples, max(3, 5 x 1.4826 x MAD)), whitening by a 0.1 Hz running mean of |X|, order-4 Butterworth
band-pass 0.25-1.0 Hz with sosfiltfilt, decimation [::2], Pearson NCC; own catalogue parser for every table of
data/catalog; own G1/G2, gap, glitch, halves and thermal code. It differs from the claim's code in small details
(mean instead of median, no 20 s dilation of invalid samples, own whitening kernel, no head of the next day).

## Results (mine next to the claim)

| item | claimed | claim's code rerun | my own code |
|---|---|---|---|
| waveform hashes (waveforms/SHA256SUMS_waveforms.txt) | all OK | 667 of 667 OK, exit 0 | - |
| glitch catalogue copies, sha256 | 78e91b83... / 1219c0fa... (prereg/PREREG.md) | same | - |
| levent.1008weber.csv sha256 | f95743b2...b0b9b93c | same | - |
| NCC MH1 at window 01:25:44.150 (index 17040 on the 3.3125 Hz grid) | 0.5952 | 0.59520 | 0.5952 |
| NCC MH2 at window | 0.6925 | 0.69252 | 0.6926 |
| D14 (two-channel mean) | 0.6439 | 0.64386 (largest D on 1971-248 and within +/- 5 min) | 0.6439 |
| A39 stack rebuilt (code/scripts/s14_multinest_build.py 39) | 16 members of 19 events | 19 events, 16 members, onset 35.3 s; bit-identical to frozen/s14_A39_1971_templates.npz and to the A39 entry of frozen/s14_multinest_1971_templates.npz | - |
| C0 time-reversed, full-span max | 0.2205 | 0.22055 (day 192) | day 192: 0.2205 |
| best of 400 phase-randomised, full-span max | 0.3180 | 0.31803 (C367, day 290); 2nd best 0.31116; median of the 400 maxima 0.2344 | day 290: 0.3182 |
| catalogue rows within +/- 5 min, or levent span containing onset | none | - | none (all 11 tables) |
| gap: valid fraction MH1 / MH2, discontinuities | 0.9999 / 0.9998, none | - | 0.99991 / 0.99982, none |
| glitch flag | MH1 flagged (MAD 0, thr 4 DU); D without MH1 0.6925 | - | MH1 median 500, MAD 0, two samples of 505 at +228.53 s and +228.68 s; MH2 MAD 1, none; D without MH1 0.6926 > 0.318 |
| halves (two-channel mean) | 0.602 / 0.678 | - | 0.600 / 0.678 (not demeaned per half); both positive |
| thermal: solar elevation at S14 | +71.4 deg | - | +71.37 deg |
| G1 overlap; nearest spike start from onset | none; +1487 s (MH1), about -12799 s (MH2) | identical JSON to results/glitch_gates_A39.json | none; +1487.1 s MH1, -12799.2 s MH2 (52458 MH1 and 50810 MH2 rows parsed) |
| G2 lag 0 | 0.588 / 0.694 (D 0.641) | identical | 0.5883 / 0.6936 (D 0.6409), 35 samples muted (claim 34) |
| G2 best within +/- 10 s | 0.557 / 0.725 (D 0.641) at +1.21 s | identical | 0.5570 / 0.7257 (D 0.6413) at +1.21 s; pass |
| D1 decimation phase (code/scripts/phase1_check.py) | 0.600 / 0.690 (D 0.645) | output byte-identical to results/phase1_check.json | - |

Null over the full span, with the claim's code: code/tools/fast_null.py with frozen/s14_A39_1971_templates.npz,
1971 days 36-365, 400 controls, seed base 20261112 (run as two single-thread processes over days 36-200 and 201-365;
days are independent). Every one of the 330 day records is bit-identical to results/null_A39_1971.jsonl (0 days
differ, largest absolute difference 0.0). The pre-registered code/scripts/score_scan.py on day 290 (the day of the
best control) gives the same C0 (0.197816) and all 400 control maxima identical to fast_null.py (best 0.31803).
Result: D14 0.6439 beats all 401 controls, the best by 0.326. No non-determinism found.

Independent null spot check (my own decoder, preprocessing and NCC; 4 days: 248, 290, 192, 100). C0 day maxima
0.2072 / 0.1949 / 0.2205 / 0.1717 against the claim's 0.2071 / 0.1978 / 0.2205 / 0.1718. Seeded phase-randomised
controls (same seeds, my own correlation): day maxima 0.2608 / 0.3182 / 0.3026 / 0.2057 against 0.2606 / 0.3180 /
0.3025 / 0.2137; per-control median absolute difference about 1e-4. 400 controls from a different random generator:
day maxima 0.262 / 0.300 / 0.287 / 0.209, so the 0.318 level does not depend on the particular seeds. This is a spot
check only; the full-span result rests on the full claim-code rerun above.

Catalogue absence (own parser): rows with event times parsed in levent.1008weber.csv (13057), gagnepian_2006 (58),
lognonne_2003 (59), nakamura_1979_sm_locations (28), nakamura_1983_ai_locations (8), nakamura_1983_m_arrivals and
nakamura_1983_sm_arrivals (dated rows); none within +/- 5 min of 01:26:14.150, and no levent start-stop span contains
it. There is no levent row at all between 1971-09-04 12:00 and 1971-09-05 12:00. The other four tables
(nakamura_1983_ai_arrivals, nakamura_2005_dm_arrivals, nakamura_2005_dm_locations, weber_2011_dmq_s_picks) carry no
event times. I did not re-fetch anything (no network in this panel); the live re-fetch rests on data/scout_record.md.

## Sensitivities found

1. The claim rests on MH2: MH1 alone is 0.5952 (< 0.6). The p1 bar is met only under the pre-registered best-channel
   reading (stated in the claim).
2. Narrow, oscillating correlation peak. D on the grid around the window: -0.549 at -0.604 s, +0.644 at 0, -0.681 at
   +0.604 s (period about 1.2 s; 96-97% of template and window energy is in 0.25-1.0 Hz). At full rate (my code,
   template Fourier-resampled): D 0.481 at -0.151 s and 0.413 at +0.151 s; MH1 peaks near -0.15 s (0.613) and MH2
   near 0 (0.693). With the frozen phase-0 templates on the other decimation grid the values are MH1 0.613, MH2
   0.349, D 0.481 (my code; the same as the claim's own results/decimation_phase_A39_A38.txt, a file CLAIM.md does
   not quote). The pre-registered D1 (templates rebuilt on that grid) gives 0.600 / 0.690 and reproduces exactly.
   In every variant the best channel stays >= 0.6 (0.613 or higher) and D stays above 0.318. A second peak one
   carrier period later (+1.21 s) is almost as high (G2 best lag), so the onset is uncertain by about one period,
   which does not matter for the +/- 5 min test.
3. Filter reading: "4-pole" read as order 2 instead of order 4 gives MH1 0.578, MH2 0.675, D 0.626 (still best CC >=
   0.6; the null was not recomputed for this variant).
4. Between-channel circular-shift control (the bank's wording, not the pre-registered single-station null; my own
   code, MH2 shifted by 1-23 h within each day against MH1, A39 templates, all 330 days): full-span maximum 0.516
   (day 289, 12 h); day 248: 0.400. This control is much harder than the phase-randomised one (a strong real event on
   one channel paired with noise gives about 0.5), and D14 0.644 still exceeds it by 0.128. It agrees with the 0.529
   that prereg/PREREG.md reports from an earlier panelist.
5. Amplitude context: the raw window is at the digitiser's lowest levels (MH1 median 500 DU, MAD 0, largest deviation
   5 DU; MH2 MAD 1, largest deviation 4 DU). The null is computed on the same data, so this does not change the test,
   but the detection is a few-DU signal.

## Verdict

Every claimed number reproduces: the waveform hashes, the NCC values at the claimed window (claim code exact,
independent code to 1e-4), the A39 stack (bit-identical rebuild), the full-span null (bit-identical over all 330 days,
C0 0.2205, best control 0.3180), catalogue absence in every table, the gap, glitch, halves and thermal checks, G1 and
G2 (rerun identical; independent values match), and D1. No mismatch, missing object or non-determinism. The
sensitivities above leave the p1 bars met (best CC >= 0.6 and D above every control) under every variant I tried.
Two caveats are disclosed or nearly so: the result relies on the best-channel reading (MH1 0.595), and the grid
sensitivity (MH2 0.349 with fixed templates on the other grid) appears in results/ but not in CLAIM.md.

pass: true
