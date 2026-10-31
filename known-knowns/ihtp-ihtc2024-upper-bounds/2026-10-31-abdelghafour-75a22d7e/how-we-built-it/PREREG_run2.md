# Pre-registration (run 2), frozen 2026-10-31 before lens output

Criterion: verbatim in target.md (official IHTP_Validator, 0 violations, strictly below the live table and below any
value the NOVELTY check finds, including open V3R1T4S PRs).
Statistic: official validator "Total violations" (must be 0) and "Total cost" per instance.
Threshold: strictly lower than max-known(table, any PR or paper value for that instance); ties fail.
Method (fixed settings): runs/2026-10-30-2321/attempts/optimizer/code/anneal.cc, 300 s, seed 2, warm start = our run-1
best for that instance; instances: i08 i16 i18 i20 m06 m07 m08 m14 m19 m09 m21 m24 m26 m30.
One table cell per claim; each surviving cell gets its own claim/ and its own three-skeptic panel.

null_test: not needed because each claim is an explicit solution object checked by a deterministic validator against a table value.

Baseline (step 3c): not an empirical benchmark; the published solutions reproduce the table (run 1 contrarian audit, 60/60).
