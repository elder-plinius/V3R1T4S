# REPRODUCE: classifier lens, PRIMARY (session 2026-10-18-1758)

Method (one line): run 2026-10-18-0839's classifier PRIMARY (multiple alignment, per-target mixture of absolute-label
LR, copy-label LR and a log-linear copy-feature model, family-pooled back-off, beam + MBR; development-family rows for
hillburmish from mannburmish and for kesslersignificance from listsamplesize) plus a new n-best reranker: the top 16
beam strings are scored by a linear softmax over 11 features (forward log posterior, MBR risk, forward and reverse
segment-correspondence channel scores averaged over the visible sources and similarity-weighted (chm, chw, crm, crw),
reliability of the sources the candidate copies (idw), the log-linear and pooled members' mean log-probabilities of the
candidate's best beam path (m_ll, m_pool), number of sources equal to the candidate (eqsrc), mean NED to the visible
reflexes (mned)); argmax. The channel tables are per ordered language pair segment-correspondence counts from the
global alignments of co-attested training reflexes, built at train time from the manifest's training file only (plus
the devx rows where the pooled model uses them). Reranker weights are constants in config.json ("rr"), fit on my
inner folds f1-f4 (bands 2-5 of training-0.50, cut with the organisers' rule) and never on shared val. The reranker is
not applied ("skip") in bantubvd, beidazihui and kesslersignificance, where my folds show no mean gain.

Code: `code/system.py` + `code/config.json`. Python: WORKDIR/venvs/q15ml/bin/python (numpy, scipy,
scikit-learn; standard library otherwise). It reads only the harness manifest files, the manifest's dev_dir files
dev_dir/mannburmish/training-0.10.tsv and dev_dir/listsamplesize/training-0.10.tsv, and the partition files.
Nothing depends on the proportion: run it unchanged at any P.

## Fresh shell: retrain and re-predict at proportion P (val needs P = 0.50; test any of 0.10 ... 0.50)

```
cd WORKDIR/runs/2026-10-18-1758
export OMP_NUM_THREADS=2 MKL_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
F=attempts/classifier/frozen/PRIMARY
OUT=SCRATCH_DIR/cls_primary_repro_1758          # any empty folder
python3 -I tools/q15h.py run --code $F/code --mode val  --out $OUT --props 0.50 --workers 2
python3 -I tools/q15h.py score-val --pred $OUT --props 0.50        # expect the frozen val numbers (score_val050.txt)
P=0.40
python3 -I tools/q15h.py run --code $F/code --mode test --out $OUT --props $P --workers 2
for m in val test; do pp=0.50; [ $m = test ] && pp=$P
  for fam in bantubvd beidazihui birchallchapacuran bodtkhobwa bremerberta deepadungpalaung hillburmish \
             kesslersignificance luangthongkumkaren wangbai; do
    cmp $F/$m/$pp/$fam/result-$pp.tsv $OUT/$m/$pp/$fam/result-$pp.tsv || echo "DIFF $m $fam"
  done; done
python3 -I tools/q15h.py audit --code $F/code --mode test --out $OUT --props $P
```
(The frozen folder holds val/0.50 and test/0.40; at other P there is nothing to compare against, the run itself is the
reproduction.)

The exact script used for the frozen runs: final_runs.sh here (val 0.50 + score-val, test 0.40, audit in test mode at
0.40, independent retrain of val 0.50 into attempts/classifier/work/det_PRIMARY + byte comparison). Log: final_runs.log.

## Determinism
No randomness: liblinear/lbfgs and scipy L-BFGS-B fits on fixed inputs, sorted iteration everywhere, fixed tie-breaks
(beam ties by label tuple, reranker ties to the higher-ranked candidate). See determinism.txt for the retrain test.

## Results of the frozen runs (2026-10-18, final_runs.log)
- val 0.50 (score_val050.txt): mean NED 0.2663, ED 1.1140, BCFS 0.8356, BLEU 0.6195; harness train 238 s; the 10
  val result files equal the development run attempts/classifier/work/p1_val (same scores).
- test 0.40: all 10 families "ok"; harness train 296 s (limit 12 min), prediction 2-34 s per family (only the stdout
  was looked at).
- audit in test mode at 0.40 (audit_test_0.40.txt): 40 identical, 0 FAIL, AUDIT PASS.
- determinism (determinism.txt, 2026-10-18T19:13:51Z): "determinism val 0.50: 10 families compared, 0 differ"
  (independent retrain in fresh processes): training and prediction are bit-deterministic.
- frozen 2026-10-18T19:14:05Z: code_tree_sha256 4880a9cd6f2bd892ecdc2008277bb78f7fe5435c1cd2415183b12f2ebb993051,
  results_tree_sha256 242596c2972e589cb236e3a6095fe406fb0723358b9130c094f1896ad8ed11c0 (attempts/classifier/FROZEN.md).
- Uses development-family rows for surprise languages: yes (hillburmish: mannburmish rows for the sparse targets Atsi
  and Lashi; kesslersignificance: listsamplesize English/German/French rows with notation maps), as run 0839's entry.

## How the reranker weights were obtained (development only; not run by the frozen system)
attempts/classifier/code/dev/: q_base.sh (base models on shared val train and folds f1-f4), dump2.py (n-best + features
through system.predict_row), fit2.py (listwise softmax on expected 1-NED, row weights as the official scorer, LOFO over
f1-f4), work/fit_lofo4/B1.json = the weights in config.json. Gate: per-family official LOFO deltas (out/lofo4_fam/).
