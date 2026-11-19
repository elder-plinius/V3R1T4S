# Null Test Report (`voynich-generator-heldout-fingerprints`)

- `target_id`: `voynich-generator-heldout-fingerprints`
- `category`: `undeciphered-scripts`
- `controls`: 400
- `protocol`: 200 word-order permutations (seeds `1000..1199`) + 200 position-preserving glyph-shuffled controls (seeds `2000..2199`) = 400 controls per cell, evaluated through the identical scoring pipeline across all 4 dialect x transliteration cells (`A/ZL3b`, `B/ZL3b`, `A/IT2a`, `B/IT2a`) for both the real Voynich manuscript and our 152-entry Hand-Executable Boundary-Coupled Lexicon Cipher (`VBCLC-152`, 3,200 controls total).
- `statistic`: Shuffle-corrected 10-chunk boundary grapheme mutual information `delta_mi_10chunk = mi_orig - mi_shuf` (`arXiv:2604.19762`), joint positional-sequential coupling `es_x_delta_mi = (es_pct/100) * delta_mi_10chunk`, and shuffle-corrected collapsed-EVA edge-glyph mutual information `excess_edge_mi` (`arXiv:2608.17096`).
- `real`: `VBCLC-152` `delta_mi_10chunk = 0.2812` bits (`B/ZL3b`), `0.2779` bits (`B/IT2a`), `0.1501` bits (`A/ZL3b`), `0.1218` bits (`A/IT2a`); `excess_edge_mi = 0.2448` bits (`B/ZL3b`), `0.2391` bits (`B/IT2a`), `0.1366` bits (`A/ZL3b`), `0.1052` bits (`A/IT2a`).
- `best_control`: `VBCLC-152` `delta_mi_10chunk best_control_400 = 0.0126` bits (`B/ZL3b`), `0.0138` bits (`B/IT2a`), `0.0306` bits (`A/ZL3b`), `0.0304` bits (`A/IT2a`); `excess_edge_mi best_control_400 = 0.0045` bits (`B/ZL3b`), `0.0035` bits (`B/IT2a`), `0.0059` bits (`A/ZL3b`), `0.0062` bits (`A/IT2a`).
- `mean_control`: `VBCLC-152` `delta_mi_10chunk mean_control_400 = -0.0002` bits (`B/ZL3b`), `0.0000` bits (`B/IT2a`), `-0.0004` bits (`A/ZL3b`), `-0.0008` bits (`A/IT2a`); `excess_edge_mi mean_control_400 = 0.0000` bits (`B/ZL3b`), `0.0000` bits (`B/IT2a`), `-0.0001` bits (`A/ZL3b`), `-0.0002` bits (`A/IT2a`).
- `sd_control`: `VBCLC-152` `delta_mi_10chunk sd_control_400 = 0.0047` bits (`B/ZL3b`), `0.0049` bits (`B/IT2a`), `0.0095` bits (`A/ZL3b`), `0.0091` bits (`A/IT2a`); `excess_edge_mi sd_control_400 = 0.0011` bits (`B/ZL3b`), `0.0010` bits (`B/IT2a`), `0.0021` bits (`A/ZL3b`), `0.0021` bits (`A/IT2a`).
- `command`: `python3 attempts/statistician/code/run_null_suite.py`
- `real_beats_all_controls`: yes

## Complete 400-Control Summary Across All 8 Corpora (`attempts/statistician/output/job-2807/out/null_suite_400_results.json`)

| Corpus & Cell | Controls | `delta_mi_10chunk` Real | `delta_mi_10chunk` Best Control (Mean $\pm$ SD) | $z$-Score | `excess_edge_mi` Real | `excess_edge_mi` Best Control (Mean $\pm$ SD) | $z$-Score | Beats All 400 Controls? |
|---|---:|---:|---|---:|---:|---|---:|---|
| **`VBCLC-152 A/ZL3b`** | 400 | **`0.1501`** | `0.0306` (`-0.0004 ± 0.0095`) | `+15.81` | **`0.1366`** | `0.0059` (`-0.0001 ± 0.0021`) | `+64.91` | **YES (`400/400`)** |
| **`VBCLC-152 B/ZL3b`** | 400 | **`0.2812`** | `0.0126` (`-0.0002 ± 0.0047`) | `+60.37` | **`0.2448`** | `0.0045` (`0.0000 ± 0.0011`) | `+229.08` | **YES (`400/400`)** |
| **`VBCLC-152 A/IT2a`** | 400 | **`0.1218`** | `0.0304` (`-0.0008 ± 0.0091`) | `+13.41` | **`0.1052`** | `0.0062` (`-0.0002 ± 0.0021`) | `+49.93` | **YES (`400/400`)** |
| **`VBCLC-152 B/IT2a`** | 400 | **`0.2779`** | `0.0138` (`0.0000 ± 0.0049`) | `+56.22` | **`0.2391`** | `0.0035` (`0.0000 ± 0.0010`) | `+239.41` | **YES (`400/400`)** |
| **Manuscript `A/ZL3b`** | 400 | **`0.0760`** | `0.0358` (`0.0003 ± 0.0100`) | `+7.60` | **`0.0842`** | `0.0088` (`0.0000 ± 0.0024`) | `+35.56` | **YES (`400/400`)** |
| **Manuscript `B/ZL3b`** | 400 | **`0.2073`** | `0.0149` (`-0.0002 ± 0.0056`) | `+37.03` | **`0.2089`** | `0.0034` (`0.0000 ± 0.0012`) | `+180.46` | **YES (`400/400`)** |
| **Manuscript `A/IT2a`** | 400 | **`0.0717`** | `0.0340` (`0.0002 ± 0.0098`) | `+7.28` | **`0.0852`** | `0.0069` (`0.0001 ± 0.0024`) | `+36.05` | **YES (`400/400`)** |
| **Manuscript `B/IT2a`** | 400 | **`0.2182`** | `0.0158` (`-0.0002 ± 0.0054`) | `+40.33` | **`0.2202`** | `0.0035` (`0.0000 ± 0.0011`) | `+198.22` | **YES (`400/400`)** |
