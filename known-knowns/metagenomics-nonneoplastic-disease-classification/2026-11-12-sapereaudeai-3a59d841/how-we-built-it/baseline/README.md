# Baseline record (kit/RUN.md step 3c): MetAML random forest on species abundance, T2D settings

Source of the expected values: Pasolli et al. 2016, PLoS Comput Biol 12(7): e1004977 (status source
https://www.ebi.ac.uk/europepmc/webservices/rest/PMC4939962/fullTextXML, fetched 2026-11-12T18:27:02Z, sha256
1edb0d04...661c), text quotes in scout.md; RF row of Fig 3 for W1/W2.

Code revision: MetAML's own Python 2-era scripts are not run; the RF is reimplemented in scikit-learn 1.9.1 (numpy
2.4.6, Python 3.11.15) with the paper's stated settings: 500 trees, max_features = sqrt(number of features),
gini. Features: the 1,291 species rows of abundance.txt.bz2 (sha256 64b505c9...dcc16), values as given.
Split: committed folds (folds/FOLDS.sha256, copied here), StratifiedGroupKFold(10, shuffle, random_state 0..19),
grouped by subject. Metric: per-fold ROC AUC averaged over 10 folds x 20 repeats; 95% margin
t(0.975, 9) x mean per-repeat standard error (the paper's margin-of-error convention).

Commands (from the run folder; CACHE = any scratch folder holding the prep.py outputs):
    python -I code/prep.py . CACHE
    python -I code/audit_main.py . CACHE W1 attempts/within-cohort-audit/out     (and W2; P1, P2 -> attempts/pooled-audit/out)

| setting | expected (published) | tolerance (PREREG) | reproduced [95% margin] | repeat-mean range | verdict | output |
|---|---|---|---|---|---|---|
| W1 T2D (Qin 2012) | 0.744 | inside 0.688-0.800 | 0.7442 [0.6862-0.8023] | 0.7213-0.7560 | reproduced | attempts/within-cohort-audit/out/W1_audit.json |
| W2 WT2D (Karlsson 2013) | 0.762 | inside 0.651-0.873 | 0.7684 [0.6449-0.8919] | 0.7247-0.8159 | reproduced | attempts/within-cohort-audit/out/W2_audit.json |
| P1 T2D + WT2D merged | 0.743 | +/- 0.03 | 0.7426 [0.6906-0.7945] | 0.7268-0.7551 | reproduced | attempts/pooled-audit/out/P1_audit.json |
| P2 merged + external healthy controls | 0.837 | +/- 0.03 | 0.8560 [0.8251-0.8868] | 0.8507-0.8620 | reproduced (+0.019, inside +/- 0.03; the published value lies inside our 95% margin) | attempts/pooled-audit/out/P2_audit.json |

Captured outputs: the *_audit.log files next to each JSON (the first line of each is the species RF result).
