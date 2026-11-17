# Notes (disclosed)

- The code here is the run code with machine-specific paths rewritten to package-relative ones (no behaviour change).
- The prereg named score_scan.py for the null; the null was computed with tools/fast_null.py, an exact re-implementation
  (overlap-save, precomputed control spectra) whose output equals score_scan.py on 1971-133 for all 401 controls
  (checked by the claimant and independently by the CRITERION panelist).
- The candidate was the largest-statistic seed among 14 seeds in 11 of 25 nests; the panel reran a cross-nest null
  (75 controls over all 25 nests, maximum 0.306) and a channel-shift stress test (maximum 0.486), both below 0.742.

## Rebuild with the glitch catalogue named (2026-11-13)

- This package replaces the unsubmitted package 2026-11-13-[credit]-dd93c774 (same object and numbers; glitch-catalogue
  gates added). It was rebuilt because that package did not cite the published S14 acceleration-glitch catalogue of
  Liu, Xiao and Li (2025), https://doi.org/10.1029/2025JE009277, catalogue https://doi.org/10.5281/zenodo.15715187.
- The glitch-catalogue gates G1 and G2 were not part of this claim's original pre-registration: they were pre-registered at the lens level at 2026-11-13T05:59:12Z, after the claim's own three-skeptic panel (run 2026-11-12-2317), with G1 already seen (a post-panel check, run 2026-11-13-0514) and G2 not yet computed at the time of the freeze. G2's outcome was already implied before its freeze, by G1 and by the claim's original glitch check (no raw sample above 8 x MAD in the window), so there was nothing to mute and G2 adds no independent evidence.
- Unchanged, byte for byte: object/window_and_template.csv, object/null_full_span_maxima.csv and
  object/null_daily_maxima.csv. They were rebuilt from the PDS waveforms with the original builder code and are
  identical; the full 330-day null was rerun and gives the same 401 full-span maxima. Also unchanged: every original
  field of object/candidate.json, and every how-we-built-it/ file of the earlier package except COMMANDS.md (steps
  7-9 added), this file (this section added) and the header of PREREG.md (one paragraph added above the verbatim
  copy; the frozen text itself is unchanged).
- Added to object/candidate.json: the key glitch_catalogue_gates, which records the catalogue, the source sha256 values,
  the extracts, the timing, the G1 and G2 results, G3 for scale and the descriptive coverage note.
- Added to object/: the catalogue extracts (glitch_catalogue_s14_acc_spike_mh1_onset_pm24h.csv and _mh2_; every
  catalogued spike interval overlapping the onset +/- 24 h, 48 and 65 rows) and the G2 inputs (g2_raw_window.csv,
  g2_prepped_window_pm10s.csv). verify-it-yourself/check_p1.py now recomputes G1 and G2.
- Added to how-we-built-it/:
  - PREREG_glitch_gates.md (the gate texts verbatim, with their timing);
  - glitch_gates_A38.json (the gate run's output; its rerun in the rebuild run was byte-identical);
  - the catalogue survey files (descriptive);
  - our own per-day counts of catalogued S14 MH1/MH2 intervals over 1971 days 36-365 and a gap-length summary
    (glitch_catalogue_daily_counts_1971d036-365.csv, glitch_catalogue_gap_summary.txt; derived statistics, added
    after the panel at the operator's request, to let a reader judge whether the silent stretch around the onset is
    unusual);
  - code/scripts/glitch_gates_a38.py, extract_spike_subset.py, rebuild_object_extracts.py, survey_nine_files.py,
    day133_hourly.py, coverage_boundaries.py, daily_counts.py and g3_base_rates.py (the G3 section of the gate code,
    unchanged, runnable without the waveforms; it reproduces the G3 counts exactly);
  - original_panel/, the four panel files of the claim's original panel exactly as written.
- glitch_gates_a38.py is the gate code exactly as run. Its usage line names the template file FROZEN_A39.npz, a leftover
  of the A39 version it was copied from; for this object it is given the A38 file.
- The descriptive survey and coverage files were computed in the rebuild run, after the gates were frozen and after G1
  and G2 were known. They decide nothing.
- After the panel, the wording of README.md, HOW_WE_FOUND_IT.md, INDEX.csv, the header of PREREG.md and the header of
  PREREG_glitch_gates.md was tightened along the CRITERION panelist's notes (panel/criterion.md, section 4). The
  changes add the remark that G2 adds no independent evidence, give the catalogue's silent stretch its correct
  position and bound, add a qualifier in INDEX.csv and a cross-reference note. README.md's "## What" is the
  CRITERION panelist's confirmed_scope, word for word.
- Also after the panel, the shipped catalogue extract was narrowed. The panel checked a draft that carried every
  catalogued S14 MH1/MH2 spike starting in 1971 days 36-365 (9361 + 11394 rows). This package ships only the intervals
  overlapping the onset +/- 24 h (48 + 65 rows, a subset of those rows), because the package must not carry a copy of
  a third-party dataset (kit SUBMIT.md). As a result:
  - extract_spike_subset.py gained a mode argument (window, shipped; year, the earlier full extract, still
    byte-identical);
  - check_p1.py reads the window files;
  - object/candidate.json's extract records changed, so its sha256 and the package id differ from the draft the
    panel saw.
  No number, gate result or claim sentence changed: the G1/G2 values the checker recomputes from the window are the
  values it recomputed from the full extract.
- At the honesty gate, README.md gained one bullet under "## Not claimed". It says that the "stack of six" counts
  members, and that the pre-registered glitch screen leaves one member out on both channels, so each channel's stack
  averages five events. The REPRODUCE panelist raised this wording point (panel/reproduce.md, section 7; panel/gate.md).
  No number changed.
