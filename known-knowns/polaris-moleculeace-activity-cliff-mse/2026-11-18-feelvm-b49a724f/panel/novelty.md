context: subagent

# NOVELTY skeptic — polaris-moleculeace-activity-cliff-mse (p2, CHEMBL244_Ki)

## Fetches (each one honest GET, UA `V3R1T4S-novelty-skeptic/1.0`, no retries; all fetches succeeded, none blocked)

- **Status page** `https://polarishub.io/benchmarks/molecularml/moleculeace-chembl244-ki` — HTTP 200 at **2026-11-18T03:42:19Z**. Embedded leaderboard data: exactly **1 entry**, `autosota-moleculeace-chembl244-ki`, `"scores":{"mean_squared_error":0.4749981512616306}`, `testSet: "test"`, `isCertified: false`. Matches the claim's scout record.
- **GraphCliff paper** `https://arxiv.org/pdf/2511.03170v2` — HTTP 200 at **2026-11-18T03:42:19Z**, 1,995,694 bytes; text extracted locally (pypdf). Table 1 (p. 6) and appendix Tables 5–7 (pp. 18–20), CHEMBL244 (Ki) column, format RMSE / RMSEcliff: **GraphCliff GRAPH 0.668 / 0.752** (best), SVM ECFP 0.715 / 0.797, Chemprop 0.726 / 0.797, MLP 0.796 / 0.850, all others worse. Confirms the claim's context quote.
- **TROPHY_CASE.md** `https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md` — HTTP 200 at **2026-11-18T03:42:19Z**; 100 lines, 53 rows; **no** polaris / moleculeace / chembl / cliff row.
- **known-knowns/ on main** `https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns` — HTTP 200 at **2026-11-18T03:42:19Z**; 38 family dirs, none moleculeace/polaris.
- **Pulls** `https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100` (HTTP 200, 2026-11-18T03:42:19Z; 100 most recent, 1 closed) and repo-wide issue search `https://api.github.com/search/issues?q=repo:elder-plinius/V3R1T4S+chembl244+OR+moleculeace+OR+activity-cliff-mse` — HTTP 200 at **2026-11-18T03:42:47Z**, `total_count = 1`: **open PR #568**, created 2026-10-19, "submission(polaris-moleculeace-activity-cliff-mse): CHEMBL287_Ki MSE 0.4080 (-18.91%) + 29/30 sweep + cliff RMSE 0.7211".
- **PR #568 detail** `https://api.github.com/repos/elder-plinius/V3R1T4S/pulls/568` (HTTP 200, 2026-11-18T03:42:58Z), files list (HTTP 200, 2026-11-18T03:43:26Z, 53 files, includes `object/predictions/CHEMBL244_Ki_test_predictions.csv`), and its sweep manifest from the PR head (`.../object/moleculeace_30_sweep_manifest.json`) — HTTP 200 at **2026-11-18T03:43:34Z**. Its CHEMBL244_Ki row (same csv sha256 `b296c595…4ef2`, same official split n_test 621 / n_cliff 296): **clss_cliff_mse 0.5542191211577052, clss_noncliff_mse 0.3243087465052875, clss_mse 0.43389565616247866** (RMSE 0.7444589 / 0.5694811 / 0.6587076), vs its reproduced SVM/ECFP baseline 0.6345887511374076 — i.e. it already satisfies the p2 criterion on CHEMBL244.
- **SupCon/contrastive biorxiv** `https://biorxiv.org/content/10.64898/2026.09.08.750257v1.full.pdf` — HTTP 200 at **2026-11-18T03:44:44Z**, 19 pp; zero mentions of "244": aggregate results over 30 datasets only, **no per-target CHEMBL244 values** — poses no cell comparison.
- **MAPCliff-WMGR** (JCIM doi 10.1021/acs.jcim.5c01915, Chen et al. 2025, 65(23) 12978): existence confirmed via web search; per-target source data behind the ACS bot check — the claim itself records honest-GET 403, and per my instructions I did **not** retry or bypass. **Unverifiable.**

## What I compared (claimed object = `result/M1_predictions.json`, per `output/M1_read_result.json`: cliff MSE 0.5501943375378687 → RMSE 0.741751; non-cliff 0.33343039149183445 → 0.577435; overall 0.43675104854437247 → 0.660872; 296 cliff / 325 non-cliff)

| Known object, same cell (CHEMBL244_Ki official split) | Overall | Cliff subset | Non-cliff |
|---|---|---|---|
| Paper's 24 rows (`data/MoleculeACE_results_CHEMBL244_rows.csv`, best = SVM/ECFP) | RMSE 0.715157 | RMSE 0.796601 | not reported (repro B: MSE 0.399311) |
| GraphCliff (arXiv 2511.03170v2, best on 244) | RMSE 0.668 | RMSE 0.752 | not reported |
| Polaris leaderboard sole entry (uncertified) | MSE 0.474998 | — | — |
| **V3R1T4S open PR #568 CLSS sweep, CHEMBL244_Ki** | **MSE 0.433896** | **MSE 0.554219** | **MSE 0.324309** |
| **Claimed M1** | MSE 0.436751 | MSE 0.550194 | MSE 0.333430 |

- M1 beats every paper row, GraphCliff, and the Polaris leaderboard entry (overall and cliff). ✔
- M1 does **not** beat PR #568's CLSS object: it wins cliff MSE by only **0.004025 (0.73% relative; 0.36% in RMSE: 0.741751 vs 0.744459)** while being **worse on non-cliff (+2.8%: 0.333430 vs 0.324309) and worse overall (+0.66%: 0.436751 vs 0.433896)**. No significance test, no seed-variation evidence, and — decisive for the mandate — the claim names this prior object **nowhere**; its novelty survey (paper rows, leaderboard, GraphCliff, MAPCliff) omits the repo's own prior submission on the same bank target id.

## Judgment

**Not a strict beat of everything known → fail.** The nearest known object for this exact cell is the CLSS sweep entry in open PR #568 (same bank target id `polaris-moleculeace-activity-cliff-mse`, 2026-10-19, identical CSV sha256 and identical 621/296 official split). That object already demonstrated the p2 result on CHEMBL244 (cliff MSE 0.554219 vs the same reproduced baseline 0.634574, non-cliff 0.324309 < 0.399311, n_cliff 296 ≥ 40), already beat the Polaris leaderboard entry, and still holds the better non-cliff and overall numbers. The claimed M1 shaves only the cliff metric by 0.73% — a bare-minimum margin of exactly the kind "a tie is not a record" forbids, with regressions on both companion metrics and no head-to-head statistics against the prior object. A single-metric 0.7% edge over an un-named known object, obtained by a 6-member SVR ensemble whose first member is the published baseline itself (the remaining members are standard SVR/Morgan-variant siblings), does not clear the bar; trivial-extension constructions must at least name the prior object and beat what such edits alone give, and this claim does neither. Unverifiable sources: MAPCliff-WMGR per-target data (ACS bot check, 403 on honest GET, not retried) — weighted as unverifiable, i.e. it cannot support a "strictly beats" confirmation, though here the verdict already rests on a fully verified source. For completeness: a search-result attribute on the Polaris artifact page ("Original-split primary metric macro_cliff_rmse=0.745310113401") is above M1's cliff RMSE 0.741751 either way and changes nothing.

pass: false
