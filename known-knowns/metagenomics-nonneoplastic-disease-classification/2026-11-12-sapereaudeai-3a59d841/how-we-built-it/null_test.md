# Null test N1 (PREREG.md, primary)

Setting P2 (MetAML T2D + WT2D cases and controls plus the healthy stool controls of the cirrhosis, colorectal, HMP and
IBD datasets; 882 samples, 223 cases). Statistic: study-of-origin-only logistic regression, mean per-fold AUC on the
repeat-0 grouped folds (folds/folds_P2.csv). Controls: the identical pipeline with the study column permuted across
samples (numpy default_rng seeds 0..399). Values copied from attempts/pooled-audit/out/null_n1.json.

controls: 400
best_control: 0.5751598302882888
real: 0.8305438467987875
real_beats_all_controls: yes
control_mean: 0.4994964107861835
command: python -I code/null_n1.py . CACHE_DIR (a scratch folder) attempts/pooled-audit/out   (run from the run folder after code/prep.py . CACHE_DIR (a scratch folder))
