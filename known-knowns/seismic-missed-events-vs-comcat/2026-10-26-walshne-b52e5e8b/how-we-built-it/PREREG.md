# PREREG (run 2026-10-26-1727): written 2026-10-26T17:31:13Z (date -u), before any of this run's values are computed

## Criterion
Verbatim in target.md. Claim path: p1 for run 12's event (2024-12-09T23:20:13.27 UTC, Parker Butte NV); the object is
not re-selected and the main win is not claimed.

null_test: required

## L1 detector-f64 (clean-room: fix the evaluator, rerun everything that depends on it)
1. **Change:** in claim/code/null_full.py the per-station correlation numerator becomes float64 end to end (float64
   chunk array, rfft of float64 data and template, float64 output before division). Nothing else in the pipeline
   changes: same prep (stored float32 20 Hz traces), same 16,384-sample chunks, same normalisation, 9 x MAD threshold,
   2 s peak spacing, +/-2 s declustering, the same 385 templates and the same 600 control jobs.
2. **Added output:** for every job, the raw maximum NCC over all samples and all templates (no threshold, no
   declustering), with its template and time, written to a per-control table (data/null_per_control_max.csv).
3. **Checker (written first, from the definition):** direct time-domain Pearson CC of the 120-sample template window
   against the 120-sample data window, per station, at chosen lags. Tests:
   - known negative (artefact): YER, template nn00888600, unshifted 2024-12-09 at 23:09:29 (REPRODUCE's point). The
     float32 code gives about 0.705; the float64 code must match the direct CC (REPRODUCE: about 0.194) within 1e-5;
   - known positive: the event's template nn00890362 at its exact aligned lag; station CCs must match the direct CC
     within 1e-5 (REPRODUCE: BFC 0.6557, KVN 0.5044, PNT 0.8373, YER 0.6857 on its own prep);
   - 200 random (template, station, day, lag) points, including 50 inside the mainshock chunk: max |diff| <= 1e-5.
   If any test fails, the float64 code is not used and the run reports it.
4. **Expected (not a gate):** event NCC about 0.6705; 12-10..12 best raw maximum 0.6121; 12-09 best raw maximum about
   0.5352 (REPRODUCE's exact values). Differences are reported; the package carries this code's numbers.
5. **Null decision rule (the claim's null, unchanged design):** count of declustered control detections with
   NCC >= the event's NCC over the 600 controls; EFC = count x 3.0 / 600. Pass if EFC < 0.05. null_test.md reports
   controls 600, best_control (the best raw per-control maximum), real (the event NCC) and real_beats_all_controls.
6. **Regenerated from the float64 real detections:** the daytime-cluster blast table (code/blast_table.py, unchanged
   rule) and the list of detections within +/-30 s of the event (doublet check).

## L2 early-hours null (statistician: a stated sensitivity, CRITERION's design made reproducible)
1. **Window:** 2024-12-09T23:13:31 to 2024-12-10T01:13:31 UTC (the first 2 h of the searched span, 5 min after the
   mainshock), 144,000 samples at 20 Hz.
2. **Data:** the same 8 raw HHZ day files; 12-09 and 12-10 merged per station, cut to 22:00-02:30, prep as in
   null_full.py (gap mask, demean, 5 % cosine taper of the 4.5-h segment, 2-8 Hz 4-pole zero-phase Butterworth,
   decimate to 20 Hz), then cut to the window.
3. **Statistic:** per template and station, circular normalised CC over the window (float64 FFT), circularly aligned
   by the template moveout; NCC = mean over the template's stations with data (>= 3 required); a control's statistic
   is the maximum NCC over all samples and all 385 templates. The event's value E2 is the maximum NCC of the
   unshifted data within +/-0.5 s of 23:20:12.75, computed by the same code.
4. **Controls:** 3,000, seed 20261026. YER is not shifted; the other 7 stations get integer sample shifts drawn
   uniformly from [12000, 132000], rejected until all 8 stations are pairwise >= 12,000 samples (10 min) apart in
   circular distance.
5. **Result:** count of controls >= E2; EFC_early = count / 3000 x (72 h / 2 h) = count x 0.012 (a worst case that
   treats the whole span as being as active as its first 2 h).
6. **Decision:** if EFC_early >= 0.05 (count >= 5), the claim is not panelled this run and the report says why.
   Otherwise the result is shipped in claim/ as a stated sensitivity, not as the criterion's null.

## Package (built only if L1's checker passes and L1's rule passes)
- Keep: claim.md, event.json, picks.csv, REPRODUCE.md; event windows and responses; mag_check.py with its windows;
  the locator; Mc and absence data; the enhanced-catalogue check; blast_table.py; null_full.py (float64) with the
  template and job files; the L2 script; fetch logs.
- Drop: discovery-stage files (mf.py, stage2.py, candidate, group and day-detection tables from run 12), the
  product-bound approximation and its output, the 9-pick statement, the STA/LTA statement.
- Fix: "385 of the 415 ComCat events within 20 km in the span (30 dropped for fewer than 3 stations with SNR >= 3)";
  Bogolub and Trugman's SRL paper as 2026 (Zenodo catalogue 2025).
- Before the panel: re-fetch ComCat and ISC absence queries once each.
