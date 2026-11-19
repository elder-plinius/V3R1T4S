# Run it yourself

Three levels of verification, from 2 seconds (Python 3 standard library only) to full 200-stream and 400-control null suite re-execution (~11 minutes on 8 CPUs).

## 1. Verify the claim from this package (2 seconds, no network, Python 3 stdlib only)

From the package root:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:

```text
102 checks passed, 0 failed
PASS
```

What it does:
1. Verifies the `SHA-256` digest of every file in `object/` against `verify-it-yourself/MANIFEST.sha256`.
2. Imports `object/vbclc.py` and verifies that `LETTER_MAP_16` (16), `ONSET_TABLE_20` (20), `CORE_TABLE_96` (96), and `CODA_TABLE_20` (20) sum to **152 table entries ($\le 200$)**, that `sigma_f` is restricted to 1 bit (`{0, 1}`), that `object/HAND_PROCEDURE.md` documents all 4 tables, and that `encrypt_vbclc_lines` is deterministic.
3. Audits `object/vbclc_200streams_evaluation.json` across all 6 dialect $\times$ transliteration cells (`A/ZL3b`, `B/ZL3b`, `A/IT2a`, `B/IT2a`, `A/RF1b-e`, `B/RF1b-e`), confirming `200/200 (100.0%)` joint passage on every cell (`100/100` Latin, `100/100` Italian).
4. Audits `object/reference_calibration.json` to confirm that the published slot generator (`signatures_v27.py`), Cardan-grille generator (`grille.py`), and unmodified Naibbe cipher (`naibbe.py`) fail joint passage.
5. Audits `object/null_suite_400_results.json` across all 4 cells (`A/ZL3b`, `B/ZL3b`, `A/IT2a`, `B/IT2a`), confirming that both the Voynich manuscript and `VBCLC-152` beat all 400/400 controls on `delta_mi_10chunk`, `es_x_delta_mi`, and `excess_edge_mi`.
6. Re-implements the 58-grapheme greedy EVA tokenizer and all 4 Currier signatures (`E->S`, `Bilat_full`, 10-chunk `MI`, and `Zipfian Shape`) from first principles using only the Python 3 standard library and verifies freshly generated Currier A ($\sigma_f=1$) and Currier B ($\sigma_f=0$) streams from `object/vbclc.py`.

## 2. Run the standalone cipher module directly (1 second, stdlib only)

```sh
python3 object/vbclc.py
```

Expected output:

```text
VBCLC-152 self-check passed: 152 table entries (<= 200), 1 per-folio state bit.
Sample Currier A line (sigma_f=1): ['daiin', 'qokeey', 'olaiin', 'chody', 'otaiin', 'shody', 'qokaiin', 'chedy']
Sample Currier B line (sigma_f=0): ['qokedy', 'chedy', 'qokaiin', 'daiin', 'otedy', 'shedy', 'qokeey', 'okaiin']
```

## 3. Rebuild the full 200-stream evaluation and 400-control null suite from scratch (~11 minutes on 8 CPUs)

Fetch the public Voynich transliterations (`ZL3b-n.txt`, `IT2a-n.txt`, `RF1b-e.txt`) from <https://www.voynich.nu/transcr.html> and the official `arXiv:2604.19762` verifier repository from <https://github.com/labyrinthinesecurity/currier-signatures> into a `data/` directory alongside 10 Latin (`Latin-00..09.txt`) and 10 Italian (`Italian-00..09.txt`) period plaintexts, copy `object/vbclc.py` and `how-we-built-it/*.py` into `code/`, and run with `numpy` installed:

```sh
python3 code/calibrate_and_audit.py
python3 code/evaluate_vbclc_200streams.py
python3 code/run_null_suite.py
```

- `calibrate_and_audit.py` writes `reference_calibration.json` (matching `object/reference_calibration.json`).
- `evaluate_vbclc_200streams.py` writes `vbclc_200streams_evaluation.json` (matching `object/vbclc_200streams_evaluation.json`, `200/200` pass across all 6 cells).
- `run_null_suite.py` writes `null_suite_400_results.json` (matching `object/null_suite_400_results.json`, `400/400` controls beaten across all 4 cells).
