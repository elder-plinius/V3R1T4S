(Saved by the main session from the subagent's returned text at 2026-10-18T22:54:04Z; the LA REPRODUCE skeptic subagent (Opus 5.5, model opus, agent a85539a159e18f4d0) could not write a file named like a report. Text verbatim below.)

# REPRODUCE skeptic: cell LA (aggregate mean BLEU over P = 0.10-0.50), session 2026-10-18-1758

context: subagent (Claude Code Agent tool, fresh context, model opus = Opus 5.5)
role: REPRODUCE skeptic of the three-skeptic panel, cell LA
start: 2026-10-18T22:10:21Z
end: 2026-10-18T22:43:51Z
material: only the claim package claim/ (paths below are relative to claim/), the kit rules, interpreters SYS (q15ml venv) and SCO (calibrator venv, used only as an interpreter), and /opt/homebrew python3.13 for my own scripts. All scratch work stayed in my own folders outside claim/. I made no web requests, so I added nothing to the stop list. The stop lists were present and I did not need to consult them for any URL.
injection_suspected: none (I read no web pages).

## 0. Definition used (quoted)
- Criterion (definition/Q15.json "success_criterion"): "A system trained ONLY on training-*.tsv and the masked test-*.tsv (never reading solutions-*.tsv), whose mean score over the 10 surprise families at a declared proportion (or aggregated over all 5 proportions, stated in PREREG.md) strictly beats Mockingbird-I1's score from the official results-surprise-*.json on the SAME metric: ... or a higher mean BLEU. ... The repo scorer `st2022` at a pinned commit computes the score."
- Aggregate (rules/PREREG.md rule 2): "A_m = (S_m(0.10) + S_m(0.20) + S_m(0.30) + S_m(0.40) + S_m(0.50)) / 5, summed left to right in that order, where S_m(P) is the family mean of metric m at P (the official "total")." Bar for LA: "Mockingbird-I1 0.6015772270938825".
- Statistic: official/src/sigtypst2022.py. Per family, compare_words(solutions-P, result-P, report=False)[-1][1:] gives [ED, NED, BCFS, BLEU]. S(P) is statistics.mean over the 10 families, as compare_systems computes "total".

## 1. My own checker (written before I opened any entry code)
mine/myscore.py, run with SCO -I. It loads official/src/sigtypst2022.py by path (sha256 9cde59bb9d042aeb06016806c749cd9147230caa9899e1f43c62d88fc0f5b23a, identical to the module installed in SCO). It computes per-family and mean ED/NED/BCFS/BLEU at each P and then A. It has two modes:
- "ltr": `sum` is shadowed by a plain left-to-right loop in the sigtypst2022 and lingrex.util namespaces.
- "builtin": Python 3.13's builtin sum.

In both modes the outer aggregate is computed both left to right and with the builtin sum.

### 1a. Calibration on Mockingbird-I1
Input: official/systems/mockingbird-i1/surprise per-item files, compared with official/results/results-surprise-P.json. Real output, ltr mode:
```
MB 0.10 fam_bit_identical 10/10 total_bit_identical True BLEU 0.6633184488563897
MB 0.20 fam_bit_identical 10/10 total_bit_identical True BLEU 0.632633947442519
MB 0.30 fam_bit_identical 10/10 total_bit_identical True BLEU 0.6058548112827981
MB 0.40 fam_bit_identical 10/10 total_bit_identical True BLEU 0.5723601982335171
MB 0.50 fam_bit_identical 10/10 total_bit_identical True BLEU 0.5337187296541888
BAR A (official totals) [ED,NED,BCFS,BLEU] ltr ['1.1654140850286332', '0.2931673956342817', '0.6797616040522236', '0.6015772270938825']
BAR A (official totals) builtin-sum ['1.1654140850286332', '0.29316739563428174', '0.6797616040522234', '0.6015772270938825']
MB A from my per-item scoring ltr ['1.1654140850286332', '0.2931673956342817', '0.6797616040522236', '0.6015772270938825']
```
The family values and totals are bit-identical at all five P (all 4 metrics are compared together as one list). The bar is A_BLEU(Mockingbird-I1) = 0.6015772270938825 with either outer summation, and it equals the PREREG value.

Builtin mode is not bit-identical to the 2022 JSON, as expected: 0/10, 2/10, 1/10, 0/10 and 1/10 families are identical at P = 0.10 to 0.50. Even so, its Mockingbird-I1 A_BLEU from per-item scoring is also 0.6015772270938825.

### 1b. Claimed object
Input: attempts/classifier/frozen/PRIMARY/test/P/FAM/result-P.tsv for all five P. Real output, ltr mode, [ED, NED, BCFS, BLEU]:
```
CAND 0.10 ['0.7741426354973481', '0.20017478183757248', '0.8091752827860231', '0.7183395130131847']
CAND 0.20 ['0.8518682371657778', '0.21213687542061813', '0.7629197798251665', '0.6960719420978517']
CAND 0.30 ['0.9552549562700591', '0.23201071558421696', '0.7347693490340722', '0.6721728449836378']
CAND 0.40 ['1.0267686117591617', '0.2455448938803044', '0.7136377968288752', '0.6533966833715619']
CAND 0.50 ['1.1367942567904354', '0.26834206801685595', '0.690510517808069', '0.624905217712099']
CAND A ltr ['0.9489657394965564', '0.23164186694791358', '0.7422025452564412', '0.6729772402356671']
CAND A_BLEU - BAR (ltr): 0.07140001314178457
```
Builtin mode gives these mean BLEU values: 0.10 0.7183395130131847, 0.20 0.6960719420978518, 0.30 0.6721728449836379, 0.40 0.6533966833715619, 0.50 0.624905217712099. Its A_BLEU is 0.6729772402356671 (outer ltr and outer builtin agree), and its margin over the bar is 0.07140001314178457.

Every value in the CLAIM.md table (all four metrics at each P and A, both rows) equals my output exactly. A_BLEU beats the bar by more than 1e-9 in both summation modes. The scorer printed no "Missing entry" line (0 in both logs).

Per-family BLEU (ltr) at 0.40, for example: bantubvd 0.5832800617998198, beidazihui 0.8353130901381886, birchallchapacuran 0.5614710409078928, bodtkhobwa 0.822466684196625, bremerberta 0.6260984947459621, deepadungpalaung 0.715949620314872, hillburmish 0.6005714430070029, kesslersignificance 0.22073285723213143, luangthongkumkaren 0.8622149525906906, wangbai 0.7058685887824336.

## 2. Integrity of the saved files
- MANIFEST.sha256: `shasum -a 256 -c` gives 470 of 470 OK. The package holds 471 files (470 plus MANIFEST itself): none is unlisted and no listed file is missing. I re-ran the check at the end and got 470 of 470 OK again, so my runs added nothing to claim/.
- FROZEN.md (ROLE=PRIMARY block):
  - code files: config.json OK and system.py OK.
  - result files (test/0.40 x10, val/0.50 x10): 20 OK.
  - code_tree_sha256 recomputed as sha256 of `shasum -a 256 config.json system.py` = 4880a9cd6f2bd892ecdc2008277bb78f7fe5435c1cd2415183b12f2ebb993051 (equal).
  - results_tree_sha256 recomputed the same way over the 20 result files = 242596c2972e589cb236e3a6095fe406fb0723358b9130c094f1896ad8ed11c0 (equal).
- checker/frozen_result_sha256.txt: 50 files, ok=50 bad=0.
- object/predictions-P.tsv against the result files and against test-P (mine/objcheck.py):
```
0.10 result rows 4029 masked cells in test-P 4029 row/mask mismatches 0 object rows 4029 object==results (same order) True (as multiset) True
0.20 result rows 7887 masked cells in test-P 7887 row/mask mismatches 0 object rows 7887 object==results (same order) True (as multiset) True
0.30 result rows 11586 masked cells in test-P 11586 row/mask mismatches 0 object rows 11586 object==results (same order) True (as multiset) True
0.40 result rows 14992 masked cells in test-P 14992 row/mask mismatches 0 object rows 14992 object==results (same order) True (as multiset) True
0.50 result rows 18101 masked cells in test-P 18101 row/mask mismatches 0 object rows 18101 object==results (same order) True (as multiset) True
OBJECT_CHECK PASS
```
  Each result row fills exactly the one "?" cell of its test row and nothing else.
- data/view/surprise: 100 files (training-P and test-P for 10 families x 5 P), 0 differ from official/data-surprise. data/view holds no solutions, cognates or wordlist file (find count 0).
- Run records attempts/classifier/frozen/PRIMARY/run_test_P.txt (0.10, 0.20, 0.30, 0.50): each has 10 families "ok". Training times: 0.10 rc=0 230s, 0.20 rc=0 203s, 0.30 rc=0 277s, 0.50 rc=0 146s.
- Audit records audit_test_P.txt: every P shows identical=40 (30 single-row files and 10 whole partitions), differ=0, and "AUDIT PASS".
- Sealed-check logs rules/sealed_cand_P.log: every P shows train ok 1, 10 families "bytes IDENTICAL", and last line "SEALED_CHECK P PASS". The item counts sum to 4029, 7887, 11586, 14992 and 18101, which equals the object rows.
- The package's standalone checker (python3 -I checker/check_q15.py . object) ends: "4. object A_BLEU 0.6729772402356671 (claimed 0.6729772402356671): EQUAL / margin vs Mockingbird-I1 0.071400013142 / 5. rebuilt official-format files equal to the frozen ones: 50 of 50 / PASS".

## 3. PREREG rule 12 (iv): retrain and re-predict at every P
For each P I created a fresh scratch folder of my own with its own HOME and ran:
```
OMP_NUM_THREADS=2 MKL_NUM_THREADS=2 HOME=fresh SYS -I tools/q15h.py run --code attempts/classifier/frozen/PRIMARY/code --mode test --out fresh/out --props P --workers 1 --python SYS
```
I ran 0.10, 0.20 and 0.30 in parallel, then 0.40 and 0.50.

Note on compute: the entry's train step always uses a 2-process spawn pool (system.py train_all(..., 2)). So the three parallel proportions ran 6 busy worker processes, not 3.

The harness wrote a manifest at each P. At every P it had mode test, the right proportion, 10 surprise_train entries each equal to data/view/surprise/FAM/training-P.tsv of its own family, and dev_dir data/view/dev. Nothing else was listed.

Training times under machine load were 726s (0.10), 647s (0.20), 536s (0.30), 443s (0.40) and 396s (0.50), all rc=0. I compared all 50 files with `cmp`:

| P | files byte-identical to claimed result-P.tsv | mean BLEU recomputed (ltr) | mean BLEU (builtin) |
|---|---|---|---|
| 0.10 | 10/10 | 0.7183395130131847 | 0.7183395130131847 |
| 0.20 | 10/10 | 0.6960719420978517 | 0.6960719420978518 |
| 0.30 | 10/10 | 0.6721728449836378 | 0.6721728449836379 |
| 0.40 | 10/10 | 0.6533966833715619 | 0.6533966833715619 |
| 0.50 | 10/10 | 0.624905217712099 | 0.624905217712099 |
| A | 50/50 | 0.6729772402356671 | 0.6729772402356671 |

The bar is 0.6015772270938825, so the margin is 0.07140001314178457 in both modes. The retrained predictions are byte-identical to the claimed ones at all five P. The case that holds is bit-deterministic reproduction, so I did not need the fallback of a recomputed value beating the bar.

## 4. What the entry reads, and row isolation
- Code audit (attempts/classifier/frozen/PRIMARY/code/system.py, after my checker was written):
  - `train` reads only the manifest, the manifest's surprise_train files (training-P), and config.json.
  - Through config.json "devx" it also reads dev_dir/mannburmish/training-0.10.tsv (Achang, Bela, Lashi, Maru, Zaiwa renamed to AchangLongchuan, Bola, Lashi, Maru, Atsi, for hillburmish). It reads dev_dir/listsamplesize/training-0.10.tsv (english, german, french renamed to English, German, French, for kesslersignificance).
  - These two development-family files are training-0.10 at EVERY P. That is the only "other proportion" file it touches, and it belongs to a development family, which PREREG rule 4 allows ("the development families (data/view/dev/)") and CLAIM.md discloses.
  - `predict` reads only model_dir (opts.json, model-FAM.pkl), the jobs file and the partition files it lists, and predicts each row with predict_row(m, row, langs).
  - The code never refers to solutions, cognates, wordlist, test-P, or any surprise file of another proportion.
- My own dynamic check: I re-ran the train step at 0.50 and at 0.40 under macOS sandbox-exec. The profile denied file reads on the whole workspace root, re-allowed only the SYS venv and a staging folder, and allowed writes only to the staging folder. The staging folder held a copy of code/, the 10 training-P files and data/view/dev, plus a harness-form manifest.
  - Negative controls inside the sandbox: reading data/view/surprise/bremerberta/test-0.50.tsv and official/data-surprise/bremerberta/solutions-0.50.tsv both gave "Operation not permitted". Positive control: reading the staged training-0.50 file worked.
  - Result: train rc=0 at both P with 0 denials in the logs. The model files (10 pickles plus opts.json) were 11/11 byte-identical to the models of my unsandboxed harness runs at 0.50 and at 0.40.
- Row isolation, my own test (mine/rowiso.py): each selected test row was written alone (header plus that row) and predicted in its own fresh process from my retrained model, then compared with the claimed result row:
```
ROWISO 0.10 bremerberta rows 80 of 80 identical 80 differ 0
ROWISO 0.10 kesslersignificance rows 99 of 99 identical 99 differ 0
ROWISO 0.20 hillburmish rows 40 of 778 identical 40 differ 0
ROWISO 0.30 beidazihui rows 30 of 2945 identical 30 differ 0
```
  The harness partitions I inspected (bremerberta 0.10) each hold one masked language and no duplicate cognate set. The audits and sealed logs above cover every P.

## 5. Observations (none changes the result)
- CLAIM.md gives the margin as 0.071400013142 (rounded). My A difference is 0.07140001314178457. The null-test real d in CLAIM.md, 0.07140001314178449, differs only in the last digits, probably because it uses a different order of operations. The claim does not depend on it.
- The entry's REPRODUCE.md cites determinism.txt, which is not in the package. My 50/50 byte-identical retrains replace that evidence.
- The system.py docstring says the rr reranker is "not used in the frozen entries", but config.json enables it for every family except bantubvd, beidazihui and kesslersignificance. This is a stale docstring. The per-family gate is disclosed in the selection note, and the frozen config is what I reproduced.

## Verdict
Every check passed:
- The official scorer reproduces Mockingbird-I1 bit for bit at all five P. The bar is A_BLEU 0.6015772270938825.
- The claimed A_BLEU 0.6729772402356671 reproduces exactly in both summation modes and beats the bar by 0.07140001314178457.
- All hashes and records match.
- Retraining from the frozen code with training-P-only manifests reproduced all 50 test-P files byte for byte (bit-deterministic case).
- The code reads only training-P plus two disclosed development-family files (training-0.10, permitted by PREREG rule 4). This is confirmed statically, by my sandboxed retrains at 0.50 and 0.40, and by the sealed logs.
- Each row is predicted from its own row only.

pass: true