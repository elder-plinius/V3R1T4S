# Notes (disclosed)

- The code here is the run code with machine-specific paths rewritten to package-relative ones (no behaviour change).
- The prereg named score_scan.py for the null; the null was computed with tools/fast_null.py, an exact re-implementation
  (overlap-save, precomputed control spectra); with the A39 stack its output equals score_scan.py on 1971-248 for all
  401 controls to the 1e-5 rounding of the stored values (fastnull_equality_A39_248.txt).
- Selection: 14 uncatalogued seeds with a single-channel CC >= 0.6 in 25 scanned nests; nulls were run for A38 (claimed
  in a separate package), A39 and A201 (a separate candidate). Three A39 seeds beat the A39 null; 1971-05-19 (D 0.736)
  is not claimed (solar elevation -12.24 deg, inside the ephemeris-formula error of the 12 deg cut; phase 14 deg from
  any catalogued member) and 1971-12-11 fails the thermal check. One object per claim.
- PREREG.md (frozen 2026-11-13T05:53:23Z) named the Liu, Xiao and Li (2025) S14 acceleration-glitch catalogue and fixed
  gates G1 (no catalogued spike in the window) and G2 (muted test), the descriptive G3 and the decimation-phase
  check D1 before they were computed; results in glitch_gates_A39.json and phase1_check.json. Several numbers were
  already known before that prereg and are listed in it.
- Decimation phase: templates and data rebuilt on the other grid give 0.600 / 0.690 (D1). With the phase-0 templates
  held fixed and only the data moved to the other grid the values are 0.613 / 0.349 (decimation_phase_A39_A38.txt): the
  narrow-band NCC oscillates with lag at about 1.2 s, so a half-sample template/data misalignment reads it off its
  peak (explained by the CRITERION panelist; the phase-randomised controls keep the same spectrum). The onset carries a
  one-cycle (about 1.2 s) ambiguity; the CC bar is met under the best-channel reading (MH1 alone 0.595).
- This is a third p1 object from the same 1971 S14 multi-nest scan as the A38 package; one object per claim.
