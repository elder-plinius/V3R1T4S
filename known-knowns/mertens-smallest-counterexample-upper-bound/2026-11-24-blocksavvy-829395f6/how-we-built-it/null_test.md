# null_test.md (frozen design in PREREG.md, section "Null test")

controls: 400
pipeline: lib/pipeline.py score(): polish y in [-1e-3, 1e-3] (step 2e-6, top 20000 terms, golden refine), round to
  12 decimals, certified arb h_StR over all 98,625 zeros gamma < 74000 at 256 bits.
control_inputs: y uniform in [1e18, 1.957e19], random.Random(20261124), 6 decimals (attempts/lattice/code/null_test.py)
command: nice -n 10 python attempts/lattice/code/null_test.py   (output attempts/lattice/null_controls.jsonl)
best_control: |h_StR| = 0.493998 at y = 8599547031670932506.625698136670 (certified ball [0.493997991573509 +/- 1.24e-16])
control_hits: 0 of 400 reach 1 + 6e-8
real: KN record point y_KN = 19571878850562201959.215107, certified h_StR = -1.0074515722180327214 +- 2.4e-22
  (no lattice hit of our own below y_KN was found; see attempts/lattice/report.md)
real_beats_all_controls: yes
note: median control |h| = 0.1501; the polish step alone cannot manufacture values
  near 1 from random y, so any |h| > 1 must come from the lattice alignment, not from the pipeline.
