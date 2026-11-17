# Run it yourself (fresh shell, from this folder)

    sh verify-it-yourself/run_checks.sh

Expected last line: PASS. It re-derives, with stdlib python3 only, from this folder:
- the per-site 4-class object-type accuracies of the claim model, the tuned KN3
  baseline and the SIGIL-style synthetic control (object/output_sweep_main.json
  pool_detail, 1,613 held-out objects);
- the 2-class Seal-vs-Tablet sub-property;
- the frozen model's class priors (recomputed from how-we-built-it/data/ m77
  + im77 with the exact TemplateModel prior formula (n_c+1)/(T+4));
- the frozen model record (seed 20261117, ctx-counts sha256);
- the 3x10,000 paired-bootstrap null test (object/output_nulltest.json: real beats
  all controls, p=0.0) and the p < 0.001 threshold at pooled / Mohenjo-daro / Harappa;
- integrity: sha256 of every object/ file against the pins in the checker.

Rough laptop time: <1 minute. No network, no third-party packages.

To rebuild the object from scratch (not needed to check it; this is how it was made):
    cd <run>/attempts/structure
    python3 code/pipeline.py            # sanity: M77 training stats
    python3 code/direction_check.py     # orientation check (as_stored_matches: true both corpora)
    python3 code/sweep_main.py         # refit frozen model + baselines, score pool, 3x10,000 bootstrap
    python3 code/nulltest.py           # the null_test.md numbers
    python3 code/probes.py            # H5/H7/H8 robustness
Inputs: the run's pinned data (how-we-built-it/data/ here; the 1.4 MB
merged-corpus-reading-order.json is listed in README.md "Large object files").
Deterministic: seed 20261117; ~5-15 min on a laptop (KN fitting + 30,000 resamples).
