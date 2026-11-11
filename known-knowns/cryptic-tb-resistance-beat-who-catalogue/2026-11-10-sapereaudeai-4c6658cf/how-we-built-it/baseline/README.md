# Baseline record (step 3c), run 2026-11-10-1136

## Engine check (published released predictions reproduced)
- Published: CRyPTIC PREDICTIONS.csv.gz (release_june2022 data_tables; sha256 de940f0f296ec7669157f4adbfc4645b5f138c123c3861c4a551e4c4defa9425), catalogue version v1.2 (piezo pipeline).
- Mine: attempts/evaluator-first/code/who_lookup2.py run with NC_000962.3_CRyPTIC_v1.2_GARC1_RUS.csv (sha256 c91c2d42...f7aa) on MUTATIONS_GPI.csv.gz rows (sha256 736c809f70d945a75c72cff9d703139f8ac4f11e7aba76e1f48b4be32d30b178) of the 12,287 reuse isolates; null calls dropped, filter-fail (O) calls kept.
- Command: python -I attempts/evaluator-first/code/score2.py . PREDICTIONS.csv.gz (output attempts/evaluator-first/score2_output.txt; table engine_check_v2.csv).
- Expected: >= 99.0% isolate-level agreement per drug (PREREG.md). Reproduced (agree / n): AMI 12279/12279 1.0000, BDQ 12256/12256 1.0000, CFZ 12259/12259 1.0000, DLM 10024/10024 1.0000, EMB 12241/12242 0.9999, ETH 8148/8148 1.0000, INH 10104/10153 0.9952, KAN 12279/12279 1.0000, LEV 12279/12279 1.0000, LZD 5660/5660 1.0000, MXF 12279/12279 1.0000, RIF 11843/11846 0.9997, RFB 11846/11846 1.0000. All 13 PASS.

## WHO-UCN-TB-2023.5 (GARC1 v2.1) on split-v2 TEST, HIGH filter, R/S only (TP/FN/FP/TN, sens, spec)
AMI 111/31/14/2069 0.7817/0.9933; BDQ 3/15/28/2047 0.1667/0.9865; CFZ 1/23/26/1865 0.0417/0.9863; DLM 4/21/3/1987 0.1600/0.9985;
EMB 296/40/58/1206 0.8810/0.9541; ETH 212/54/68/1762 0.7970/0.9628; INH 987/70/20/1283 0.9338/0.9847; KAN 147/36/35/2094 0.8033/0.9836;
LEV 245/46/32/1604 0.8419/0.9804; LZD 6/14/0/1762 0.3000/1.0000; MXF 201/26/73/1387 0.8855/0.9500; RIF 840/20/53/1312 0.9767/0.9612;
RFB 0/807/0/1735 0.0000/1.0000 (WHO has no RFB rows). TRAIN rows, HIGH+MEDIUM and the 2021.7 edition: baseline_scores_v2.csv.

## Published baseline for the p2 leakage test
None exists for this split and model; the p2 comparison is internal (same model, same drug, cluster-aware vs random
splits), so no external baseline applies. Nothing here is clinical advice.
