# Pre-Registration & Protocol Lock

- **Target ID**: `nceas-disdat-presence-only-sdm-auc` (`ecology`)
- **Strict Presence-Only Training Protocol**: Model training and suitability score prediction on all 6 regions (`AWT`, `CAN`, `NSW`, `NZ`, `SA`, `SWI`) use only `{R}train_po.rds`, `{R}train_bg.rds`, and `{R}test_env*.rds`.
- **Zero PA-Leakage Invariant**: `{R}test_pa*.rds` binary presence-absence labels are never accessed during feature standardization, target-group background construction, DeepMaxent MLP training, Newton-IRLS Maxent fitting, Empirical-Bayes guild shrinkage, or suitability score prediction.
- **Point-Covariate Only Constraint (`p3`)**: Uses only the tabular environmental covariates bundled in `rspatial/disdat` (`inst/extdata/*.rds`), with zero external environmental raster grids.
- **Species Set**: All 225 valid species (`nsw30` excluded per `RYCKEWAERT/deepmaxent` and `hideyuki-doi/tabfm-distribution` because it has only 2 presence records), with the 217-species median computed over the exact 217 species having `< 1,000` presence-only records.
