# NOVELTY verdict — dreval-lco-ctrpv2-normalized-r2 (partial win p2)

context: subagent (fresh session)
Role: NOVELTY skeptic. I read claim/CLAIM.md first; I did not modify anything in claim/. I did
not re-run the attacker's model (that is the verifier's job); novelty is judged on the claim's
reported numbers (Pearson 0.4600 / Spearman 0.4432 under the report's v1.3.1 ruler; R^2 0.2087)
against everything published or otherwise known for the cell CTRPv2, LCO, normalized metrics.

## 1. Primary status fetches (once, honest, no retries — none blocked)

1. Report heatmap, https://dilis-lab.github.io/drevalpy-report/heatmaps/heatmap_algorithms_LCO_normalized.html
   - curl -A "V3R1T4S-agent/1.0", HTTP 200, 4,666,613 bytes, fetched 2026-11-21T11:42:12Z.
   - Own decoder (scripts/dump_traces.py, numpy base64 float64 "bdata", shape "15, 1" / "15, 3") decoded
     BOTH Plotly traces. The page is not R^2-only: trace 0 is "R^2: normalized" (15 models), trace 1 is
     "Kendall/Pearson/Spearman: normalized" (15 models). The claim's statement that the report's tables
     publish normalized R^2 but not Pearson/Spearman is wrong in detail (the normalized Pearson/Spearman
     ARE in the heatmap figure) — but this favours the claim: the heatmap itself publishes the comparator.
   - Live maxima (all RandomForest): R^2: normalized **0.1851801**; Pearson: normalized **0.43469311**;
     Spearman: normalized **0.42829111**; Kendall: normalized 0.30605953. Runners-up: MultiOmicsRandomForest
     (R^2 0.16327124, Pearson 0.40756464), ProteomicsRandomForest (0.16116436 / 0.40396921), DIPK
     (0.10842067 / 0.38162282). 15 models total.
2. Leaderboard image, https://raw.githubusercontent.com/daisybio/drevalpy/main/docs/_static/img/leaderboard_light.png
   - curl -A "V3R1T4S-agent/1.0", HTTP 200, 1,280,519 bytes, fetched 2026-11-21T11:42:17Z.
   - Best normalized Pearson = **EnsembleMF 0.376** (34 models; #2 SingleDrugMorgoth 0.361, #3
     SingleDrugRandomForest 0.359). Confirms the claim's 0.376/EnsembleMF.
3. Claim-time copies match fresh fetches byte-for-byte (sha256):
   - claim/heatmap_algorithms_LCO_normalized.claimtime.html = 31a313febc02831bc4930304b76263ec66b28297619768382d9d9badf600ed68 = fresh fetch.
   - claim/leaderboard_light.claimtime.png = 1b2313ee5de8e1fffb7e34ff0bc4724f49fca66c97c9b0cb71bb383c1684d563 = fresh fetch.
   So the live tables are unchanged between the claim's fetch (10:56Z/01:44Z) and mine.

## 2. Comparator verification (Zenodo)

- Record 17343165 metadata fetched 2026-11-21T11:45:10Z (HTTP 200). "Dataset for drevalpy", all_results.zip 2,690,160,813 bytes.
- I did NOT download the 2.69 GB zip: scripts/extract_eval_csv.py reads the zip central directory and the single
  entry over HTTP Range requests (Zenodo returned HTTP 206 on ranges). Extracted all_results/evaluation_results.csv
  (596,447 rows-line file, 15 columns) at ~11:46Z.
- Recomputed means over the report's own per-split rows (rand_setting=predictions, test_mode=LCO, n=10 splits):
  RandomForest: Pearson: normalized **0.434693**, Spearman: normalized **0.428291**, R^2: normalized **0.185180** —
  identical to the live heatmap to 6 decimals, and RandomForest tops all 15 models on every normalized metric.
  The claim's comparator values (0.4347 / 0.4283 / 0.1852, RandomForest, CTRPv2 LCO) are VERIFIED.
- Maintained leaderboard data: record 12633909 redirects (302) to current version 23916090 ("Dataset for drevalpy",
  2026-11-03). Extracted leaderboard_Nov26/evaluation_results.csv from leaderboard_Nov26.zip (Range requests).
  34 models, CTRPv2 LCO. Best normalized Pearson **0.376099 (EnsembleMF)** (matches the image's 0.376), best
  normalized Spearman **0.366892 (RandomForestAEMolGNet)**, best normalized R^2 **0.126944 (EnsembleMF)**.
  Note: leaderboard RandomForest Pearson_norm = 0.327838 — corroborates the claim's ruler account (the
  leaderboard runs the current-package normalization; the report runs the v1.3.1-era one; claim's RF re-run under
  v1.6.0 = 0.3277 per CLAIM.md, matching the leaderboard's 0.3278 to 4 decimals).

## 3. Novelty comparison (object and result)

Published bests for the cell (CTRPv2 LCO normalized metrics), all verified live today:

| source (ruler) | best Pearson_norm | best Spearman_norm | best R^2_norm | holder |
|---|---|---|---|---|
| report heatmap + Zenodo 17343165 CSV (v1.3.1-era) | 0.434693 | 0.428291 | 0.185180 | RandomForest (15 models) |
| leaderboard image + leaderboard_Nov26.zip (v1.6.0) | 0.376099 | 0.366892 | 0.126944 | EnsembleMF / RF-AEMolGNet / EnsembleMF (34 models) |

Claimed result: 0.4600 / 0.4432 / 0.2087 (report ruler). Margins vs the strictest published numbers:
+0.0253 Pearson, +0.0149 Spearman, +0.0235 R^2 — all strictly positive, none near a tie; all above the bank
p2 bars (+0.01 Pearson/Spearman; R^2 floor 0.1752, cleared by 0.0335). Also strictly above every leaderboard
number (0.4600 > 0.3761, 0.4432 > 0.3669, 0.2087 > 0.1269).

Literature and code sweep (last 24 months):
- The benchmark paper itself (Bernett et al., Nature Communications 2026, "Critical evaluation of drug response
  prediction models with DrEval") publishes the same numbers as the report/heatmap; its LCO tables are the
  heatmap's (the "0.44" in its normalized-Pearson table is RF 0.4347 rounded).
- All literature models are already inside the two tables above: PharmaFormer (0.286), Precily (0.262),
  SparseGO (0.297), SRMF (0.030), MOLIR (0.075), SuperFELTR (0.066), PaccMann (0.135), DrugGNN (0.192),
  DIPK (0.311 leaderboard / 0.382 report ruler), MultiView* (0.011-0.325), EnsembleMF (0.376), SingleDrug*
  (0.340-0.361), RandomForestAEMolGNet (0.357). None exceeds its table row.
- Non-drevalpy papers found (arXiv 2605.20885 "Training distribution determines the ceiling...", Pillbox
  bioRxiv 2026, Asiaee et al. leakage paper, Partin et al. 2026, Iversen et al.) use per-drug Pearson, raw
  Pearson or MSE under different protocols — different ruler, different cell; none reports a CTRPv2 LCO
  drevalpy-normalized Pearson/Spearman/R^2 above the table bests.
- drevalpy repo: models tree (DIPK, DrugGNN, EnsembleMF, MOLIR, Morgoth, PaccMann, PharmaFormer, Precily,
  SRMF, SimpleNeuralNetwork, SparseGO, SuperFELTR + baselines incl. multi_view_*, singledrug_*, sklearn_models,
  ae_molgnet_random_forest, naive_pred) contains no residual-ridge ensemble; releases v1.2.0-v1.7.0 carry no
  assets; all 414 PRs scanned — model-adding PRs are #514/#513 (literature models), #458 (EnsembleMF),
  #442 (GCMF), #439 (SparseGO), #430 (MultiViewLightGBM), #496/#497/#495 (SingleDrugMorgoth/KNN, RF-AEMolGNet),
  #465 (drug_mean / drug_tissue_mean conditional-mean residualization — the nearest published relative of the
  claim's "base + ridge on residuals" pattern; its leaderboard descendants, the SingleDrug* family, top out at
  Pearson_norm 0.3611). Nothing named or resembling EnsembleResidualOmics; a web search for the name returns
  nothing outside this claim.

Object construction test (per my instructions):
- The object is SEEDED from published objects: drevalpy's own NaiveMeanEffectsPredictor (member A base,
  literally instantiated in code/ensemble_model.py), the tissue-x-drug mean base (member B; = the published
  NaiveTissueDrugMeanPredictor semantics), and ridge on gene-expression residuals (the ElasticNet family).
- It NAMES its seeds (CLAIM.md and the code docstrings name all three) and beats what those seeds/edits alone
  give: naive bases 0.0000 (report ruler) / 0.2510 NaiveTissueDrugMeanPredictor (leaderboard); plain ridge
  (ElasticNet) 0.0705 report / 0.0225 leaderboard; SingleDrug residual family 0.3576-0.3611 leaderboard;
  and the best published object on the comparison ruler, RandomForest 0.4347 report-ruler, by +0.0253.
- It is not a trivial edit (no deletion/restriction/relabelling/symmetry/numerical polish of a single published
  object yields a two-member residual-ridge ensemble); the composition is not published anywhere I searched.

## 4. Repo history (TROPHY_CASE, known-knowns, PRs)

- v3r1t4s/V3R1T4S/TROPHY_CASE.md: six families + 2 cipher commitments; NO dreval rows.
- known-knowns/: no dreval-* directories (dreval PRs are unmerged submissions, so not integrated).
- V3R1T4S PRs, 800 scanned (8 pages, open+closed): dreval claims are #836, #837, #835, #834, #984, #712.
- **Prior claim on THIS target id: PR #836 (2026-10-29, mizopl, SchurBilinearExVivoDRP, CONFIRMED_PARTIAL,
  partial_win: p1, p3).** Its p1 is the LTO setting (R^2_norm 0.13506 LTO vs 0.07279 published) and p3 is the
  reproducibility audit. It did NOT claim p2 (the LCO Pearson/Spearman beat). Its extra "Live 2026 Leaderboard
  #1 Beat in LCO" reports Pearson_norm 0.41460, Spearman_norm 0.39156, R^2_norm 0.17153 under drevalpy 1.6.0
  on the leaderboard's precomputed splits (companion repo mizopl/dreval-drug-response-transfer confirms ruler
  and numbers). Every one of those LCO numbers is BELOW this claim's reported numbers (0.4600 > 0.4146,
  0.4432 > 0.3916, 0.2087 > 0.17153), and the p2 scope (strictly beating the report's 0.4347/0.4283 with a
  same-splits RF gate) was left open by #836. No prior claim anywhere reports higher LCO numbers than this
  claim's. No tie.

## 5. Honest caveats (do not change the novelty verdict)

1. Ruler split: under the current-package (v1.6.0) ruler the claim's model co-reports Pearson_norm 0.3652 /
   Spearman 0.3452 / R^2 0.1314 — BELOW EnsembleMF's published 0.3761 Pearson and BELOW the prior claim's
   0.4146/0.3916/0.17153. On the only ruler on which both this claim's object and the prior claim's object
   have been measured, the prior claim's object is stronger. This claim therefore does not demonstrate
   superiority over PR #836's object; it claims exactly the bank's p2 under the report's ruler (the ruler that
   reproduces the published report table, which I verified by recomputation), discloses the v1.6.0 numbers,
   and satisfies the bank criterion's leaderboard clause as written (reported normalized Pearson 0.4600 is not
   lower than the live leaderboard maximum 0.376). The bank's pitfall 6 ("beating the older [frozen report]
   scoreboard alone is not a record") is answered by the criterion's own leaderboard constraint, and the claim
   does not assert the headline R^2 win.
2. The claim says the report heatmap "publishes normalized R^2 but its tables are broken" — in fact the live
   heatmap's second trace publishes normalized Pearson/Spearman (I decoded them), which is what let me verify
   the comparators directly; the claim's comparator values match.
3. The leaderboard now lists 34 models (bank text said 25 as of 2026-10-15; EnsembleMF remains #1 at 0.376).
4. The claimed per-run numbers (0.4600/0.4432/0.2087 and the v1.6.0 co-values) are taken from CLAIM.md and its
   artifacts; re-running them is the verifier's task, not novelty's.

## 6. Conclusion

Everything published for CTRPv2 LCO normalized metrics — report heatmap (15 models, RF 0.4347/0.4283/0.1852,
verified live and recomputed from Zenodo 17343165) and the maintained leaderboard (34 models, EnsembleMF
0.3761 / RF-AEMolGNet 0.3669 / EnsembleMF 0.1269, verified live and from leaderboard_Nov26.zip) — is strictly
below the claimed 0.4600/0.4432/0.2087, as are the repo's prior claims (PR #836 LCO: 0.4146/0.3916/0.17153,
which claimed p1/p3, not this p2). No literature or code object reaches these values; the object is new, names
its published seeds, and beats what those seeds alone give. No ties anywhere. Novelty: the p2 partial win is
not pre-empted; the claimed result strictly beats everything published for this cell under the ruler that
reproduces the published table.

pass: true
