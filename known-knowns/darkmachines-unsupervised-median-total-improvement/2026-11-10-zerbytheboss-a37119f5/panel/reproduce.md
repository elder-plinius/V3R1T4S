# Skeptic Panel — REPRODUCE

- context: fresh research subagent invoked with zero solver history (role: REPRODUCE)
- target_id: `darkmachines-unsupervised-median-total-improvement`
- audited_utc: `2026-11-10T20:40:01Z`

## 1. Quoted Target Criterion (`KNOWN`)

From the target specification (`darkmachines-unsupervised-median-total-improvement`):

> "An anomaly detector trained only on SM background events from the hackathon files: per channel, background events whose event ID is odd are used for training and selection, and the remaining background events plus all signal events of that channel are used for evaluation. No signal labels or signal events may be used for training or selection. Report, for all 19 signals in their channels, eps_S at eps_B = 1e-2, 1e-3 and 1e-4 in the repository's CSV format (Signal, Model, Chan, AUC, 1e-2, 1e-3, 1e-4). At each working point the score threshold must leave at most that fraction of the evaluation background events at or above it, with tied scores counted as passing. Each eps_S is rounded to two decimals, as in the record holder's CSV, before SI is computed."
>
> "**p1:** Under the full-win protocol, TI strictly above 1.1 for chaneut_cha300_neut100 or strictly above 1.0 for chaneut_cha400_neut200 (the best of the 1040 challenge detectors)."

## 2. Zero-Leakage & Protocol Code Audit (`PROVED-HERE`)

Line-by-line inspection of `how-we-built-it/dm_featurize.c`, `how-we-built-it/dm_bsp_eval.c`, `how-we-built-it/run_darkmachines_bspot.py`, and `how-we-built-it/export_bspot_objects.py` confirms every protocol requirement:

1. **Unweighted & Label-Free Featurization (`PROVED-HERE`)**:
   - In `how-we-built-it/dm_featurize.c` (`extract_line`, lines 85–95), column `0` (`event_ID`) is parsed as `int64_t`, while column `1` (`process_id`) and column `2` (`weight`) are stepped over via `strtok_r(NULL, ";\r\n", &saveptr)` at lines 89–90 without conversion, storage, or branching.
   - All `52` kinematic invariants (`feats[0..51]`, lines 320–371) are deterministic functions of single-event 4-momenta and missing transverse energy, and every event is counted with unit weight (`1`) during training, threshold calibration, and signal efficiency evaluation.
2. **Strict Odd-`event_ID` SM Background Training & Zero Signal Leakage (`PROVED-HERE`)**:
   - In `how-we-built-it/dm_bsp_eval.c` (`run_channel`, lines 581–685), Pass 1 over the channel background `.bin` file (`lines 584–596`) inspects event features (`augment_event`, `stratum_id`) strictly when `(buf[i].eid & 1) != 0`; for even events (`(buf[i].eid & 1) == 0`), only `n_even++` is executed.
   - `stratum_nlp` (`lines 606–608`), `X_glob`, `X_strat`, and `X_coarse` (`Pass 2`, line 629: `if ((buf[i].eid & 1) == 0) continue;`), `train_stratum_model` (`lines 662, 668, 678`), and `train_floor_guard` (`line 684`) are fitted exclusively on odd-`event_ID` SM background events.
   - All training buffers are freed by line 685, even-`event_ID` SM background events are scored in Pass 3 (`line 697`: `if ((buf[i].eid & 1) != 0) continue;`), `fbg` is closed at line 705, and thresholds `taus` are locked at line 712 before any BSM signal `.bin` file is opened (`fopen` at line 734). Signal files are never read during training, feature weighting, calibration, or threshold selection.
3. **Strict Even-`event_ID` Calibration & Tie-Aware Threshold Soundness (`PROVED-HERE`)**:
   - `radix_sort_floats_asc` (`dm_bsp_eval.c`, lines 97–127) applies the exact IEEE-754 sign-bit bijection (`0xFFFFFFFFu` for negative floats, `0x80000000u` for non-negative floats) across four 8-bit LSD passes, sorting all `n_even` even-background scores in exact ascending order.
   - In `compute_thresholds_from_asc` (`lines 507–525`), let `mp = floor(eps_B * n_b)` and `pos = n_b - mp`:
     - When `mp <= 0` (Channel `2a` at `eps_B = 1e-4`, where `floor(1e-4 * 8377) = 0`), `taus[e] = bg_asc[n_b - 1] + 1e-5f`. For Channel `2a` scores (`max_bg` in `[12.1524, 17.7905]`, IEEE-754 `float32` ULP `1.91e-6 < 1e-5`), `taus[2] > bg_asc[n_b - 1]` strictly in `float32`, leaving `0 <= 0` evaluation background events at or above `taus[2]`.
     - When `mp >= 1` and (`pos == 0` or `bg_asc[pos - 1] < bg_asc[pos]`), `taus[e] = ct = bg_asc[pos]` leaves `n_b - pos = mp <= floor(eps_B * n_b)` passing background events.
     - When `pos > 0` and `bg_asc[pos - 1] == ct` (a score tie crossing the `mp` boundary), the loop `int64_t idx = pos + 1; while (idx < n_b && bg_asc[idx] == ct) idx++;` advances past all copies of `ct`. If `idx < n_b`, `bg_asc[idx - 1] = ct < bg_asc[idx] = taus[e]`, so `count(bg_asc >= taus[e]) = n_b - idx <= mp - 1 < floor(eps_B * n_b)`; if `idx == n_b`, `taus[e] = ct + 1e-5f` leaves `0 <= mp` passing events.
   - `how-we-built-it/run_darkmachines_bspot.py` (`lines 318–334`) implements the identical tie-advancement rule via `higher = asc[pos + 1:]; gt = higher[higher > ct]`.
4. **Channel-Uniform Code, Hyperparameters & End-to-End Rebuild Pipeline (`PROVED-HERE`)**:
   - In `dm_bsp_eval.c` (`lines 796–799`), `run_channel` runs with identical constants (`N_STRATA = 60`, `MIN_STRATUM_N = 250`, `MAX_TRAIN_GLOBAL = 250000`, `MAX_TRAIN_STRATUM = 60000`, `SEC_COLS`, `CORE27_COLS`, and model combination weights) across `chan1`, `chan2a`, `chan2b`, and `chan3`, with zero channel-specific or signal-specific branches.
   - `RUN_IT_YOURSELF.md` Section 2 iterates `./dm_featurize` per CSV across `chan1`, `chan2a`, `chan2b`, and `chan3`, executes `./dm_bsp_eval`, and invokes `how-we-built-it/export_bspot_objects.py` to sort rows deterministically by `(Chan, Signal, Model)` and compute IEEE-754 2-decimal `eps_S` rounding (`round(p / float(n_sig), 2)`), `SI`, and `TI` per `notebooks/04-SignificanceImprovement.ipynb`.

## 3. Independent Verification Run (`NUMERICAL`)

1. **Package Checker Reproduction (`NUMERICAL`)**:
   Executing `sh verify-it-yourself/run_checks.sh` from the package root exited with status `0` and reproduced `verify-it-yourself/RECEIPTS.md` verbatim:
   - Negative control rejected perturbed CSV cell.
   - All `136` signal-channel rows and live Channel `2a` retraining verified (`max float32 diff = 0.0000`).
   - Final output line: `PASS`.
2. **Independent Provenance, Odd/Even Split, Full 4-Channel Live Execution & Byte-Exact Object Export (`NUMERICAL`)**:
   An independent in-memory Python audit script (writing zero files to disk) verified:
   - Running `dm_featurize` directly on all `8` raw Zenodo `3961917` Channel `2a` CSV files (`1` background + `7` signal CSVs, `0` empty fields in header columns `0..4`) reproduced the pre-featurized Channel `2a` binary cache (`background_chan2a_309.6.bin`, `20,005` events, `4,321,080` bytes, plus all `7` signal `.bin` files) byte for byte.
   - Partitioning `background_chan2a_309.6.bin` strictly by `(eid % 2) == 1` vs `(eid % 2) == 0` produced `11,628` odd-`event_ID` training events (`137` distinct odd IDs) and `8,377` even-`event_ID` evaluation events (`114` distinct even IDs) with `0` shared `event_ID`s, matching `verify-it-yourself/data/chan2a_odd_part{1,2}.npz` and `verify-it-yourself/data/chan2a_even_part{1,2}.npz` byte for byte (`np.array_equal == True`), and all `7` Channel `2a` signal `.npz` archives matched their `.bin` counterparts byte for byte.
   - Exact SM background splits verified across all `4` binary-cache channels: Channel `1` (`108,473` odd / `105,712` even), Channel `2a` (`11,628` odd / `8,377` even), Channel `2b` (`177,640` odd / `162,628` even), and Channel `3` (`4,282,867` odd / `4,261,244` even), with all `34` signal-channel `n_sig` counts matching `verify-it-yourself/data/bspot_eval_ref.json.gz`.
   - Live Channel `2a` Python retraining yielded `float32` evaluation-background pass counts at `(1e-2, 1e-3, 1e-4)` of `[83, 7, 0]` for `BSPOT_MaxSec` (`max_bg = 14.584374`, `taus = {1e-2: 6.911915, 1e-3: 13.670317, 1e-4: 14.584384}`) and `BSPOT_Bayes_Full` (`max_bg = 17.790474`, `taus = {1e-2: 8.062573, 1e-3: 16.802683, 1e-4: 17.790484}`), and `[83, 8, 0]` for `BSPOT_FloorGuard` (`max_bg = 12.152401`, `taus = {1e-2: 5.600038, 1e-3: 9.026459, 1e-4: 12.152411}`) and `BSPOT_Union_OR` (`max_bg = 15.892866`, `taus = {1e-2: 7.117236, 1e-3: 12.055179, 1e-4: 15.892876}`), strictly satisfying `<= [83, 8, 0]`. Maximum signal pass-count difference between Python and C across all `28 x 3` Channel `2a` working-point cells is `1` event (`0.0000` rounded efficiency difference).
   - Full 4-channel live execution of the compiled C99 evaluator (`dm_bsp_eval.c`) across all `4,580,608` odd training events and `4,537,961` even evaluation events (`17.47 s`) reproduced all `136 / 136` rows (`n_sig`, `pass_1e-2`, `pass_1e-3`, `pass_1e-4`, and `AUC`) with `0` integer pass-count discrepancies across all `544` count cells.
   - Running `how-we-built-it/export_bspot_objects.py` in memory on the raw `dm_bsp_eval` output reproduced `object/darkmachines_bspot_results.csv` (`sha256 = a37119f59f0abe26391bac2270beb5d42fd4f727dc7a3222dbfd4c11adbc1609`) and `object/darkmachines_19signals_bspot_summary.tsv` (`sha256 = 68fbd1e05071188d5e979c163c5d970ee38e9dc1d168f5962d4b43874a285ba7`) byte for byte.
3. **Independent `SI`, `TI` & Benchmark Baseline Recomputation (`NUMERICAL`)**:
   - All baseline figures in `how-we-built-it/baseline/baseline_record.md`, `the-record-we-beat/darkmachines_bspot_snapshot.md`, and `README.md` match direct recomputation from `data/Flow.csv` (`4,838` bytes, `sha256 = e2e17152c3222f6ea089706836a6b0f274a041c717a1138c93669629536098e0`), `data/Combined.csv` (`19,439` bytes, `sha256 = 7754b06b4a820769ac38986e94b299a54c2e1e845ae30e013e99a4bbc3c5f3b6`), and all `13` challenge detector CSVs: `Flow-Efficient_Likelihood` (`Median_TI = 15.0000`, `7.9057` from `1e-2` and `1e-3` alone, `Min_TI = 0.9000`, `cha300 TI = 1.1000` at `eps_S = 0.11, 0.0, 0.0`, `cha400 TI = 0.9000`) and `Combined-AVG-DeepSVDD-Flow` (`Median_TI = 10.0000`, `Min_TI = 0.8000`, `cha300 TI = 0.8000`, `cha400 TI = 1.0000` tied alongside `Combined-OR-DeepSVDD-Flow` and `Flow-Efficient-No-E_Likelihood`).
   - Recomputing `SI = round(eps_S, 2) / sqrt(eps_B)` and `TI(signal) = max_{chan, eps_B} SI` independently across all `136` rows of `object/darkmachines_bspot_results.csv` and `19` signals confirmed every cell of both object files:

   | Detector | `Median_TI` (`19` signals) | `Min_TI` (Signal) | `Max_TI` (Signal) | `chaneut_cha300_neut100` `TI` | `chaneut_cha400_neut200` `TI` |
   | :--- | :---: | :---: | :---: | :---: | :---: |
   | `BSPOT_MaxSec` | `5.3759` | `0.2000` (`pp23mt_50`) | `46.0000` (`stlp_st1000`) | `6.0000` | `7.0000` |
   | `BSPOT_Bayes_Full` | `4.9000` | `0.3000` (`pp23mt_50`) | `44.0000` (`stlp_st1000`) | `4.0000` | `5.0000` |
   | `BSPOT_Union_OR` | `5.0000` | `0.8000` (`pp23mt_50`) | `50.0000` (`stlp_st1000`) | `3.0000` | `5.0000` |
   | `BSPOT_FloorGuard` | `3.1000` | `0.9000` (`chaneut_cha250_neut150`, `pp23mt_50`) | `47.0000` (`stlp_st1000`) | `1.8000` | `2.2136` |

pass: true
