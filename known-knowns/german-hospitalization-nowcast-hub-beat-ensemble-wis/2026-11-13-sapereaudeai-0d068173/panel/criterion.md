# CRITERION skeptic: german-hospitalization-nowcast-hub-beat-ensemble-wis, partial win p3

context: subagent (fresh context, Claude Code Agent tool)

Read: claim/CLAIM.md, claim/ADDENDUM.md, claim/REPRODUCE.md, claim/scout_record.md, claim/baseline/, claim/reference_outputs/, claim/code/. Inputs in claim/data/ were read in chunks. Nothing else in the run folder was opened.

Network: 9 requests, one each, User-Agent naming V3R1T4S, all HTTP 200, no retries:
- Europe PMC full text PMC10446237
- GitHub API commit 11c745322c055cfbd4f0c8f72241642a50aea399 of KITmetricslab/hospitalization-nowcast-hub
- 3 hub nowcast files (raw.githubusercontent, branch main)
- GitHub API listing of the evaluation repository's data/scores
- the 3 published tables wis_{national,states,age}_7d.csv

Scratch files are under panel/work_criterion/: dl/ holds the downloads, scripts/ my own code.

The criterion text and p3 are as quoted in claim/CLAIM.md: "A reproduction of the hub's published evaluation: recompute per-model WIS for the published period from data-processed and the truth data with a released script, documenting every discrepancy and the exclusion rules needed to reconcile it."

## Word by word

**"the hub's published evaluation"**
- The paper is Wolffram et al. 2023 (PLoS Comput Biol, PMC10446237). Its data-availability statement says the nowcasts and truth data are in the hub repository and that "Code to reproduce results and figures are provided at" the evaluation repository (github.com/dwolffram/hospitalization-nowcast-hub-evaluation). That is the published evaluation, and Fig 7 (mean WIS per model at three levels) is its headline result.
- The claim reproduces the three main tables, data/scores/wis_national.csv (11 models), wis_states.csv (10) and wis_age.csv (10): 31 cells.
- Their sha256 (78aeb28a..., 2cde62e4..., 88936f4c...) match the values recorded in claim/baseline/README.md.
- Hidden quantifier found: the claim's sentence says "all 31 per-model mean WIS cells of the ... published evaluation". My listing of the evaluation repository's data/scores (GitHub API) shows 15 per-model WIS tables, not 3:
  - wis_*.csv (the 3 reproduced)
  - wis_*_100k.csv (per 100,000 population, Fig A12)
  - wis_*_40d.csv (rolling target, Section 3.7)
  - wis_*_7d.csv (horizons 0..-7, Fig 9)
  - wis_*_updated.csv (the four revised models)
- The other 12 are not reproduced. The p3 operational clause ("per-model WIS for the published period from data-processed and the truth data") fairly reads as the main per-model WIS. The 100k variant also needs population data, the updated variant uses data-processed_updated_models, and the 40d variant uses a different target definition. So I do not fail p3 on this.
- The claim's wording "all 31 ... cells of the published evaluation" is wider than the evidence and must be narrowed to "the 31 cells of the three main tables".
- Partial check of the obvious extension: with the claim's exclusion rule and the hub truth, my own code (panel/work_criterion/scripts/cell7d.py) reproduces the published _7d tables exactly for MeanEnsemble and SZ at all three levels (6 cells, |rel diff| <= 2.2e-16). The claim does not assert this.

**"recompute per-model WIS"**
- claim/code/p3_reproduce.py is an independent Python re-implementation (numpy and pandas only). It scores the mean over quantile rows of 2(1{y<q}-tau)(q-y).
- The paper's eq. 2, (1/(2N+1))(|y-m| + sum alpha_k IS_alpha_k) with N = 3, is identical to that mean over the 7 quantiles. The paper itself notes the pinball-loss equivalence. claim/reference_outputs/wis_selftest.txt checks the identity.
- Result (claim/reference_outputs/p3_log.txt, claim/baseline/p3_S2_vs_published.csv, identical to the S2 rows of claim/reference_outputs/p3_ladder.csv, which I checked):
  - 31 of 31 cells within 1%.
  - 28 cells at |rel diff| <= 2.3e-16.
  - Epiforecasts at +1.031e-4 (national), +1.28e-5 (states) and +6.7e-7 (age).
- The components (spread, over- and underprediction) also agree. All non-zero component differences are in the Epiforecasts cells.
- Independent check: my own code (panel/work_criterion/scripts/cell.py) reads the assembly, the 4 exclusion lists and the hub preprocessed truth at commit 11c74532. It reproduces MeanEnsemble (259.59445032205866 / 22.18647102805194 / 41.48400441858294) and SZ (national, states, age) to |rel diff| <= 2.3e-16, with the same row counts (32,137 / 513,583 / 192,822).
- I did not run p3_reproduce.py itself: its stated peak memory is about 1 GB, above my limit. Re-running it is the REPRODUCE skeptic's task.

**"for the published period"**
- The paper says "from Monday 22 November 2021 to Friday 29 April 2022", with the final truth defined as "the time series available on 8 August 2022".
- My chunked read of claim/data/eval_data/submissions.csv.gz gives 7,577,313 rows, forecast_date range 2021-11-22..2022-04-29 (159 dates), and 10 models.
- The GitHub API gives the truth commit 11c74532 as 2022-08-08T05:10:27Z, "Daily RKI update". It touches data-truth/COVID-19/COVID-19_hospitalizations_preprocessed.csv.
- The local truth files hash to the sha256 in the fetch log (bdd34ddb..., 2c18ca95...).
- The period matches.

**"from data-processed and the truth data"**
- Truth: p3_reproduce.py rebuilds the 7-day sums from the hub's preprocessed file at that commit. They equal the evaluation's truth_2022-08-08.csv on all 57,596 rows, max |diff| 0 (p3_log.txt). My own truth build gives the same scores.
- Nowcasts: the script reads the evaluation's assembly, not the hub folders directly. The link to the hub is claim/code/p3_provenance.py, and its output claim/reference_outputs/p3_provenance_full.txt reads: files_checked=1593, hub_rows=7,592,953, key_mismatches=0, value_mismatches=0.
- The 3 MeanEnsemble files checked twice (sample dates 2021-11-22, 2022-01-15, 2022-03-31) hold 4,968 + 5,336 + 5,336 = 15,640 rows, and 7,592,953 - 15,640 = 7,577,313 = the assembly's row count. So every assembly row is matched to a hub row.
- My own spot check fetched 3 hub files:
  - data-processed_retrospective/RKI-weekly_report 2022-02-10
  - data-processed/LMU_StaBLab-GAM_nowcast 2022-03-15
  - data-processed/NowcastHub-MeanEnsemble 2022-01-10
  Their sha256 equal the logged ones (2149471c..., 0272b41b..., 4d112913...). Their rows equal the assembly rows exactly (3,944 / 4,930 / 5,336; no key or value difference).
- Literal caveat: the sources are three hub folders, not one.
  - data-processed: 1,408 files
  - data-processed_retrospective: 185 files, including all 159 RKI files. The paper says RKI's quantiles "were only provided in retrospect".
  - data-processed_updated_models: the ILM/LMU fill rows (claim/data/hub/updated_models/)

  The published evaluation's own loader does this, and claim/CLAIM.md rules 4-5 document it. I read "data-processed" as the hub's processed-submission folders, not one folder name; a one-folder reading would make the published evaluation itself unreproducible.
- FrozenBaseline: claim/code/frozen_baseline_check.py truncates the hub's raw triangle at the 2022-08-08 commit to cells d+k <= t, a genuine derivation that I read and that is not circular. The result equals the evaluation's baseline file on 106,053 of 106,053 targets.
- Exclusion lists: claim/code/rederive_exclusions.py builds them as the hub template minus the keys each model submitted, and they equal the released lists as sets (claim/reference_outputs/rederive_exclusions.txt). The lists are therefore derivable from data-processed, not opaque inputs.

**"with a released script"**
- claim/code/p3_reproduce.py does the S0/S1/S2 ladder.
- The rest of the chain is also in claim/code/: fetch_hub.py, p3_provenance.py, rederive_exclusions.py, frozen_baseline_check.py and wis_selftest.py.
- claim/REPRODUCE.md gives commands and expected lines.

**"documenting every discrepancy and the exclusion rules needed to reconcile it"**
- The ladder documents every deviation in the published tables.
  - S0 (no rules): 25/31 within 1%, 0 exact. The 6 failures are Epiforecasts x3 (+2.0..2.8%), LMU states (+11.1%) and RKI national/states (undefined; NA values).
  - S1 (exclusion of the 547 listed targets for all models): 23 exact.
  - S2 (fix_RKI, fix_epiforecasts, fix_ILM, fix_LMU, then exclusion, in the released code's order): 28 exact.
- Each repair touches one model's rows and the cells are per model, so every S1-to-S2 change is attributable to exactly one named rule.
- The 3 residual Epiforecasts cells: the cause is stated only implicitly, in CLAIM.md rule 3 (closed-form two-point normal fit vs rriskDistributions::get.norm.par). It is not proven by running R. It is supported by a fingerprint I checked in p3_ladder.csv:
  - The residuals sit only in spread and overprediction.
  - The underprediction differences are 0, 3.3e-9 and 7e-15.
  - For a lower quantile below the median with y above the median, the underprediction term equals 0.2(y-m), independent of the imputed 0.1-quantile value. This is exactly the pattern a slightly different imputed 0.1 quantile produces.
- Paper text vs released code: ADDENDUM.md item 2 reports two differences, flagged as second-hand and unverified (the S1 Appendix was not opened).
  - The RKI repair threshold: 1e6 in the code vs a reported "1 billion" reading of Table A4.
  - The number of excluded targets: 547 in the released lists vs a reported 394 in Table A3.

  I add that the main text says "0.3% of all targets" were omitted. 547/106,053 = 0.52%; 394/106,053 = 0.37%. So the main text agrees with the reported Table A3 count, not with the released lists that reproduce the published tables. This is the same discrepancy ADDENDUM item 2 already names, now confirmed from the main text. Its cause is not established.
- Because the published WIS values are reproduced with the released code's rules, the discrepancies that p3 asks to reconcile (recomputed vs published WIS) are all documented.
- Wording errors to fix (no number changes):
  - ADDENDUM.md "31/31 within 1e-4" is false: the national Epiforecasts cell is at 1.031e-4. It should read "within 1.04e-4" (or "within 1%").
  - The claim should state the cause of the 3 Epiforecasts residuals explicitly as inferred, not verified.

## Baseline record

claim/baseline/README.md and claim/baseline/p3_S2_vs_published.csv match the claim:
- Same data: assembly sha256 04608675..., truth commit 11c74532.
- Same period: 2021-11-22..2022-04-29.
- Same metric: mean of 2x pinball per model and level.
- Same level definitions: national DE 00+; states 16 states with ILM absent; age DE six groups with RKI absent.
- Same tolerance: 1%.

The CSV equals the S2 rows of the ladder exactly, and its pub_wis column equals the three published tables exactly. The README's command path points into the run's attempts folder, which I did not open; the same script ships as claim/code/p3_reproduce.py.

## Null models / subsumption

- The S0 rung is the null: the naive recomputation without the evaluation's rules. It visibly fails on 6 of 31 cells, so the rules are doing real work and the agreement is not automatic.
- The 28 exact cells could not arise by chance: there are 28 independent values to 15 or more significant digits.
- p3 is not subsumed. No main-criterion claim exists. An independent re-implementation plus a provenance chain to the hub's files is more than re-running the authors' R code. Prior-art novelty is the NOVELTY skeptic's question.

## Verdict

p3 is met for the evaluation's main per-model WIS tables, under the reading "data-processed" = the hub's processed-submission folders that the published loader reads.

Corrections required before posting:
1. Narrow "all 31 per-model mean WIS cells of the published evaluation" to "the 31 cells of the three main tables (Fig 7)", and say that the _100k, _40d, _7d and _updated tables are not reproduced.
2. Fix "31/31 within 1e-4" in ADDENDUM.md.
3. State the Epiforecasts residual cause as inferred.
4. Say plainly that the paper's main text (0.3% of targets omitted) and the reported S1 Appendix description differ from the released code, which is what the published tables follow.

confirmed_scope: A released, independently written Python script (claim/code/p3_reproduce.py, with the provenance, exclusion-re-derivation and FrozenBaseline checks in claim/code/) recomputes the 31 per-model mean WIS cells of the published evaluation's three main tables (data/scores/wis_national.csv, wis_states.csv, wis_age.csv; the overall means of Wolffram et al. 2023 Fig 7) for forecast dates 2021-11-22..2022-04-29 from the hub's data-processed, data-processed_retrospective and data-processed_updated_models nowcasts (read via the evaluation's assembly, verified row for row against those hub files) and the hub's truth at the 2022-08-08 commit 11c74532, matching 28 cells to |relative difference| below 1e-9 and the 3 Epiforecasts cells to within 1.04e-4, and documents the exclusion and repair rules of the released evaluation code needed for that agreement, without reproducing the evaluation's other WIS tables (_100k, _40d, _7d, _updated) or verifying the paper's S1 Appendix description of those rules.
pass: true
