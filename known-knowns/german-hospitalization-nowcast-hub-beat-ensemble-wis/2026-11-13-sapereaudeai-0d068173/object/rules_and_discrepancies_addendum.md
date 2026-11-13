# Addendum to the claim (added 2026-11-13 ~05:10 UTC, after the NOVELTY skeptic's report and before the CRITERION skeptic started;
# documentation only, no number of the claim changes)

1. **The exclusion lists are re-derivable from the nowcast files.** `code/rederive_exclusions.py` builds the full hub
   target template (848,424 keys: DE x 7 age groups + 16 states x 00+, horizons 0..-28, mean + 7 quantiles,
   159 dates) and subtracts the keys each model submitted (Epiforecasts after its 0.1-quantile repair). The result
   equals the released lists exactly: Epiforecasts 696/696, MeanEnsemble 368/368, MedianEnsemble 368/368, SZ
   3,312/3,312 (`reference_outputs/rederive_exclusions.txt`). Together they are 4,376 keys = 547 targets on 6 forecast
   dates: Epiforecasts 87 targets on 2022-01-31, 02-01, 02-08; Mean/MedianEnsemble 46 on 2021-11-22; SZ 414 on
   2021-11-22..24.
2. **Discrepancies between the paper's text and the released code/data.** The published tables follow the released
   code. Our S2 matches those tables 28/31 to < 1e-9 relative and 31/31 within 1.04e-4 (wording corrected after the panel; it
   read "within 1e-4", which the national Epiforecasts cell at 1.031e-4 contradicts). The paper's main text says 0.3% of
   targets were omitted; the released lists omit 547 of 106,053 (0.52%).
   - RKI repair. The released code replaces RKI values > 1e6 or NA by the minimum of the 0- and -1-day values. The
     assembly has 42 such values > 1e6 (8 above 1e9, 34 between 1e6 and 1e9) and 6 NA, all on "0 day ahead"
     targets. A reviewer read the paper's S1 Appendix Table A4 as saying "values above 1 billion, replaced by the
     -1-day nowcast"; the author of this claim has not opened the S1 Appendix. Under the 1e9 reading, 34 implausible
     values (1.1e7..6.6e8) and the 6 NA would stay, and the RKI cells would not match the published tables.
   - Excluded targets. The released lists give 547 targets (above). The same reviewer read Table A3 as giving 394
     targets and not listing 2022-02-08 (not verified by the author). The published tables are reproduced only
     with the released 547-target lists.
3. **Full provenance.** `reference_outputs/p3_provenance_full.txt` compares the assembly with every hub file the
   released loader reads for the period: all 1,431 other-model files plus the 159 MeanEnsemble files. Its summary
   line is copied below when the check finishes.

   Summary line of `reference_outputs/p3_provenance_full.txt` (finished 2026-11-13T05:22Z):
   `files_checked=1593 hub_rows=7592953 key_mismatches=0 value_mismatches=0 files_with_any_difference=0`
   The 1,593 files cover all 1,590 (model, forecast_date) pairs of the assembly (10 models x 159 dates; 3 MeanEnsemble
   files are checked twice), each from the folder the released loader reads (data-processed, or
   data-processed_retrospective where a retrospective file exists). Every assembly row equals a hub row and vice versa.
   All 1,404 files of the second fetch returned HTTP 200 (`reference_outputs/hub_fetch_log_full.tsv`).

4. **Epiforecasts residuals.** Their cause (closed-form two-point normal fit versus rriskDistributions::get.norm.par for
   the interpolated 0.1 quantile) is inferred, not verified: R was not run. Only the spread and overprediction components
   move; underprediction agrees to 3.3e-9.
