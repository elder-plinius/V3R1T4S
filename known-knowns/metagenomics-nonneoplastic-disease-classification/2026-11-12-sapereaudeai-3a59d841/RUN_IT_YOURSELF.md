# Run it yourself (from this folder, fresh shell)

## 1. Check the claimed numbers (under a second, Python 3 standard library)
    sh verify-it-yourself/run_checks.sh
Expected output: the lines in verify-it-yourself/RECEIPTS.md, ending with `PASS`. It recomputes the single-covariate
AUCs (W1 age, W1/W2/P1 depth, W1/W2 BMI, P1 age) exactly from the shipped covariate table and fold files, the pooled
study-only AUC (to 0.005), the permutation summaries, the null and the headline fractions, and checks the object hash.

## 2. Rebuild everything from public data (about 1.5 hours of CPU at 2-4 threads)
Inputs (not included; public): MetAML data/abundance.txt.bz2
(https://raw.githubusercontent.com/SegataLab/metaml/master/data/abundance.txt.bz2, 2,028,873 bytes, sha256
64b505c930c8801debef1e95202699c13acf8a44f99ebb0700a4622f60ddcc16; repo head commit 52fbd54a) and curatedMetagenomicData
data/sampleMetadata.rda (https://raw.githubusercontent.com/waldronlab/curatedMetagenomicData/devel/data/sampleMetadata.rda,
624,293 bytes, sha256 168c8650d2893dcb49930b9b85a4187637775c9aae0a8023efb4cca52dc73444).
Software: how-we-built-it/requirements.txt. Memory: read_rda.py converts the whole sampleMetadata.rda with rdata and
needs about 1.1 GB; prep.py's depth match expects the six-study subset that read_rda.py writes. In an empty folder RUN with data/abundance.txt.bz2 in it, and a scratch
folder CACHE:

    python -I how-we-built-it/code/read_rda.py sampleMetadata.rda CACHE/cmd_sampleMetadata_subset.tsv
    python -I how-we-built-it/code/prep.py RUN CACHE              # cohorts, depth match, folds (compare with folds sha256)
    python -I how-we-built-it/code/audit_main.py RUN CACHE W1 OUT  # and W2, P1, P2
    python -I how-we-built-it/code/audit_perm.py RUN CACHE P2 0 400 OUT/perm_P2.tsv   # and W1, W2, P1
    python -I how-we-built-it/code/null_n1.py RUN CACHE OUT
    python -I how-we-built-it/code/summarize_audit.py RUN audit_results.csv audit_summary.md

(audit_main.py and friends import audit_lib.py from their own folder; prep.py writes RUN/folds/; the shipped fold
files are in verify-it-yourself/data/ and how-we-built-it/folds/, hashes in how-we-built-it/folds/FOLDS.sha256.)
Expected outputs: how-we-built-it/results/. Sensitivity analyses: how-we-built-it/code/sensitivity.py (parts s1-s7),
outputs in how-we-built-it/results/sensitivity/.
