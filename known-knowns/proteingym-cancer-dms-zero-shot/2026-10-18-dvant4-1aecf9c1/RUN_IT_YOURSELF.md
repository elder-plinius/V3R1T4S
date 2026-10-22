# Run it yourself

From this folder, in a fresh shell with Python 3:

```
sh verify-it-yourself/run_checks.sh
```

Expected output (see verify-it-yourself/RECEIPTS.md for the real run):
```
object sha256 1aecf9c14a0746b6b434b38acebfdfe8ddeefec98bedb322d6ea53b1ee7760db matches INDEX.csv
reference zip sha256 ok
reference file sha256 ok
mutants 5083 identical sets
spearman 0.565763  table max 0.516  margin +0.049763  (needs > 0 and >= 0.015)
PASS
```

To compare against a fresh copy of the live table:
```
curl -s -o table.csv https://raw.githubusercontent.com/OATML-Markslab/ProteinGym/main/benchmarks/DMS_zero_shot/substitutions/Spearman/DMS_substitutions_Spearman_DMS_level.csv
TABLE_CSV=table.csv sh verify-it-yourself/run_checks.sh
```

To rebuild the object from ProteinGym's published score files (about 2 GB download, pandas/numpy/scipy), follow
how-we-built-it/README.md. The rebuilt file has sha256 1aecf9c14a0746b6b434b38acebfdfe8ddeefec98bedb322d6ea53b1ee7760db.
