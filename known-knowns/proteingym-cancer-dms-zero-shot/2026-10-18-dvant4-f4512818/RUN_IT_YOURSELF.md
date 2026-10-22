# Run it yourself

From this folder, in a fresh shell with Python 3:

```
sh verify-it-yourself/run_checks.sh
```

It prints one line per assay (sha, Spearman, table max, margin), then the list of assays clearing +0.015, then PASS. The real
output is in verify-it-yourself/RECEIPTS.md.

Against a fresh copy of the live table:
```
curl -s -o table.csv https://raw.githubusercontent.com/OATML-Markslab/ProteinGym/main/benchmarks/DMS_zero_shot/substitutions/Spearman/DMS_substitutions_Spearman_DMS_level.csv
TABLE_CSV=table.csv sh verify-it-yourself/run_checks.sh
```

To rebuild the 13 objects from ProteinGym's published score files (about 2 GB download), follow how-we-built-it/README.md.
