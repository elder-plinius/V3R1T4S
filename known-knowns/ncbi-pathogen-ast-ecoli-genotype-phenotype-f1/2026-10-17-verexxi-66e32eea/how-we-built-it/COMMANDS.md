# How the object was built (exact commands, from this folder)
```bash
uv venv venv --python 3.12 && uv pip install --python venv/bin/python pandas==3.0.6 numpy==2.5.4 scikit-learn==1.9.1 lightgbm==4.7.0
mkdir -p data && (cd data && curl -sSO https://ftp.ncbi.nlm.nih.gov/pathogen/Results/Escherichia_coli_Shigella/PDG000000004.6366/Metadata/PDG000000004.6366.metadata.tsv \
  && curl -sSO https://ftp.ncbi.nlm.nih.gov/pathogen/Results/Escherichia_coli_Shigella/PDG000000004.6366/Clusters/PDG000000004.6366.reference_target.cluster_list.tsv)
venv/bin/python -P -s code/ecoli_prep.py data/PDG000000004.6366.metadata.tsv data/PDG000000004.6366.reference_target.cluster_list.tsv prep
cmp prep/split.csv split.csv
venv/bin/python -P -s code/ecoli_model.py prep rebuild cluster     # writes rebuild/test_predictions.csv (all eight antibiotics) and rebuild/results.json
```
The object is the rows of rebuild/test_predictions.csv for this antibiotic (rebuild/ is the folder the last command creates). code/ecoli_rule_check.py checks the rule against the paper's own
supplementary tables (0 mismatches on 56,141 comparisons).
