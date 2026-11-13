# Reproducing the German Hospitalization Nowcast Hub's main published WIS tables: 31 of 31 per-model cells, with the reconciling rules (bank target german-hospitalization-nowcast-hub-beat-ensemble-wis, partial win p3)

## What
A released, independently written Python script (claim/code/p3_reproduce.py, with the provenance, exclusion-re-derivation and FrozenBaseline checks in claim/code/) recomputes the 31 per-model mean WIS cells of the published evaluation's three main tables (data/scores/wis_national.csv, wis_states.csv, wis_age.csv; the overall means of Wolffram et al. 2023 Fig 7) for forecast dates 2021-11-22..2022-04-29 from the hub's data-processed, data-processed_retrospective and data-processed_updated_models nowcasts (read via the evaluation's assembly, verified row for row against those hub files) and the hub's truth at the 2022-08-08 commit 11c74532, matching 28 cells to |relative difference| below 1e-9 and the 3 Epiforecasts cells to within 1.04e-4, and documents the exclusion and repair rules of the released evaluation code needed for that agreement, without reproducing the evaluation's other WIS tables (_100k, _40d, _7d, _updated) or verifying the paper's S1 Appendix description of those rules.

(The panel judged the claim folder; in this package its claim/code/ scripts are in how-we-built-it/code/.)

This is a retrospective benchmark of forecasting methods on an archived series. It is not public-health guidance.

## Check it yourself
    sh verify-it-yourself/run_checks.sh
Expected last line: `PASS`. It takes under a second and needs only the Python 3 standard library (set PYTHON if
python3 is not on PATH). It checks:
- the object's sha256;
- the 31 published values;
- the per-stage agreement: S2 within 1% everywhere and 28 cells exact; S0 and S1 each leave 6 cells outside 1% or
  undefined;
- the WIS identity.
RUN_IT_YOURSELF.md rebuilds every number from the public hub and evaluation files. That takes about 15 minutes of
polite downloads plus 3 minutes of compute, with numpy and pandas.

## Compared to
| what | value | source | fetched (UTC) |
|---|---|---|---|
| published per-model mean WIS (31 cells; Fig 7 of Wolffram et al. 2023) | MeanEnsemble national 259.5945, states 22.1865, age 41.4840; all cells in the-record-we-beat/record.md | https://github.com/dwolffram/hospitalization-nowcast-hub-evaluation (data/scores/wis_{national,states,age}.csv) | 2026-11-13T04:23:56Z |
| status source | hub repository (no leaderboard; study closed) | https://github.com/KITmetricslab/hospitalization-nowcast-hub | 2026-11-13T04:20:41Z |
| nearest published work (as read by the NOVELTY skeptic, panel/novelty.md) | the authors' own R pipeline (the original evaluation); Amaral et al. 2025 (40-day truth, shorter period); Johnson et al. 2025 (baselinenowcast vs KIT); no independent recomputation found | panel/novelty.md | 2026-11-13 |

## Rules needed to reconcile (each re-implemented from the released R code; effect in object/p3_reproduction_table.csv)
1. Exclusion of 547 targets (4,376 rows) missing for Epiforecasts, MeanEnsemble, MedianEnsemble or SZ, applied to
   all models. These lists can be re-derived exactly from the nowcast files.
2. RKI: 42 values above 1e6 and 6 NA values, all on 0-day targets, replaced by the min of the 0- and -1-day values.
3. Epiforecasts: the missing 0.1 quantile on 29,348 targets is interpolated from a normal fitted to the 0.025 and
   0.25 quantiles.
4. ILM (1,008 rows) and LMU (60,291 rows): missing rows filled from the hub's data-processed_updated_models.
5. Retrospective files replace prospective ones (RKI 159 dates, ILM 19, SU 3, Epiforecasts 2, RIVM 2).
Without rules 1-4, 6 of 31 cells miss by more than 1% (up to +11.1%) or are undefined.

## Not claimed
- No new nowcast and no better score: this reproduces published numbers.
- The cause of the Epiforecasts residuals (+1.03e-4 / +1.28e-5 / +6.7e-7) is a hypothesis: the closed-form normal
  fit versus rriskDistributions::get.norm.par. R was not run.
- Only the three main tables (wis_national, wis_states, wis_age) are reproduced; the evaluation's _100k, _40d, _7d and
  _updated WIS tables are not.
- The paper's main text says 0.3% of all targets were omitted; the released lists that reproduce the published tables
  omit 547 of 106,053 targets (0.52%). The published tables follow the released code; the cause of the difference is
  not established.
- The paper's S1 Appendix was not opened by the claimant. Its RKI threshold ("1 billion") and its excluded-target
  count (394) are quoted as read by a reviewer. Both differ from the released code (1e6 or NA; 547 targets), and the
  published tables follow the code.
- The run's p1 nowcaster is not part of this package. It is not new: published retrospective reruns beat it on the
  same rows.

## Credits
- Daniel Wolffram, Johannes Bracher and co-authors: the paper (PLoS Comput Biol 19:e1011394,
  https://doi.org/10.1371/journal.pcbi.1011394) and the evaluation code and data
  (https://github.com/dwolffram/hospitalization-nowcast-hub-evaluation).
- The Hospitalization Nowcast Hub team at Karlsruhe Institute of Technology and the Heidelberg Institute for
  Theoretical Studies: https://github.com/KITmetricslab/hospitalization-nowcast-hub.
- The contributing teams: Epiforecasts (LSHTM), ILM, KIT, LMU StaBLab, RIVM, RKI, SU and SZ (see the paper, Table 1).
- Robert Koch Institute: the hospitalization data.
- Bracher, Ray, Gneiting and Reich (2021, PLoS Comput Biol 17:e1008618): the WIS.
