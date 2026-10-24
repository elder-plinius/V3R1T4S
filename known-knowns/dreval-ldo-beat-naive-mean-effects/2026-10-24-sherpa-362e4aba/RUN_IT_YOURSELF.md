# Run it yourself

Three levels, cheapest first. Level 1 needs no network and no large download and settles whether the
claimed number is what the shipped predictions actually contain. Levels 2 and 3 rebuild the result.

All commands run **from this package folder**.

## Level 1 — verify the claim from the shipped files (about 10 seconds)

```sh
sh verify-it-yourself/run_checks.sh
```

Last line: `PASS`. **Python 3 standard library only** — no numpy, no pandas, no drevalpy, no network, no
1.5 GB dataset, no environment variables. A couple of minutes.
It recomputes the benchmark's own statistic from `object/`, which holds, for each of the 10 CV splits of
each of the two split generations, every test pair with its ground truth, this model's prediction and the
NaiveMeanEffectsPredictor's prediction. Specifically it checks:

1. **The leave-drug-out property**: in every split, no test drug appears in that split's training or
   validation set, and no predicted drug lies outside the test fold. Read from `object/*_split_drug_roles.csv.gz`.
2. **The statistic**: normalized R² per split — R² of `(truth − baseline)` against `(prediction − baseline)` —
   then averaged. This is drevalpy's `_normalize_metrics_by_mean_effects` reduced to the quantity it produces.
3. **The ruler**: the baseline's own normalized R² must reproduce its published behaviour (published −0.0169).
4. **The margin**: above the published maximum by at least 0.02 absolute *and* at least 2 × the across-split SE.
5. **That the gain is not the combination leak**: single agents alone must still clear the bar.

Real output from this machine is in `verify-it-yourself/RECEIPTS.md`.

## Level 2 — re-score with drevalpy's own evaluation code (minutes)

This proves the number is the package's, not the checker's. Needs drevalpy 1.3.5 and the pinned data.

```sh
python -m venv env && . env/bin/activate     # Python 3.11-3.13
pip install "drevalpy==1.3.5"
```

Fetch the pinned data (Zenodo record 17343165; md5s in `the-record-we-beat/README.md`), unpack `CTRPv2.zip`
and `meta.zip` into one directory `$DATA`, then — because drevalpy 1.3.5 looks for `<dataset>/gene_lists/`
while the record ships `meta/gene_lists/` — link them:

```sh
ln -s ../meta/gene_lists "$DATA/CTRPv2/gene_lists"
```

Install the method's two lookup files. `teacher_pred.csv` is shipped here (it is this work's own output:
the external potency prior evaluated on each CTRPv2 drug's fingerprint). `drug_pathways.csv.gz` is **not**
shipped, because it is third-party data that already comes with the dataset — copy it from the `meta`
bundle you just unpacked:

```sh
mkdir -p "$DATA/CTRPv2/potency_transfer"
cp how-we-built-it/teacher_pred.csv "$DATA/CTRPv2/potency_transfer/"
cp "$DATA/meta/gcmf_drug_relations/drug_pathways.csv.gz" "$DATA/CTRPv2/potency_transfer/"
```

`drug_pathways.csv.gz` is drevalpy's own `(pubchem_id, drug_name, pathway)` table, where each pathway is a
KEGG or Reactome term a drug's **targets** belong to — target annotation, which the criterion permits, not
experimental activity data. sha256 `514c247dc6838217abceb90fd3515e89a4c48642ebed6e4b3f86a50fa9b87307`.

Then run the frozen model through drevalpy's own CLI and score it with drevalpy's own report code:

```sh
python how-we-built-it/run_confirmatory.py repro_seed42
python how-we-built-it/evaluate_with_drevalpy.py repro_seed42 pt PotencyTransfer
```

Expect `PotencyTransfer  normR2 +0.2249` and `NaiveMeanEffectsPredictor  normR2 -0.0247` over 10 splits.
The small difference from Level 1 (+0.2244) is explained in `verify-it-yourself/RECEIPTS.md`: drevalpy's
normalization left-merges on (drug, cell line, split), and CTRPv2 has 4,118 duplicated keys, so its
evaluation scores 245,122 rows from 235,974 predictions. Both numbers are reported; neither is hidden.

## Level 3 — rebuild the external potency prior from scratch (about an hour, GPU helps)

The prior is the method's decisive component, so this is the level that matters most to a skeptic.

```sh
# NCI DTP public NCI-60 (sha256s in the-record-we-beat/README.md)
curl -L -o GI50.zip      'https://wiki.nci.nih.gov/download/attachments/147193864/GI50.zip?api=v2'
curl -L -o nsc_smiles.csv 'https://wiki.nci.nih.gov/download/attachments/155844992/nsc_smiles.csv?api=v2'
curl -L -o nsc_sid_cid.csv 'https://wiki.nci.nih.gov/download/attachments/155844992/nsc_sid_cid.csv?api=v2'

pip install rdkit torch
python how-we-built-it/h10_build_teacher.py        # applies the CID and Tanimoto 0.85 exclusions
python how-we-built-it/h10_leak_audit.py           # salt-stripped audit; must report 3 skeleton matches
python how-we-built-it/h10_teacher_threshold.py 0.60   # the frozen prior: 53,486 compounds
```

The audit is the step worth repeating independently: it is what found 3 CTRPv2 compounds inside the prior's
training data under different identifiers, and it is why the frozen exclusion threshold is 0.60 rather than
the 0.85 originally pre-committed.

Sensitivity, all reported in `../attempts/potency-transfer/output/dev_teacher_thresholds.log` (development
data) and `../attempts/confirmation/output/teacher050_seed42.txt` (confirmatory): the stricter the
exclusion, the smaller the gain — 0.85 → +0.227, 0.70 → +0.172, **0.60 → +0.163**, 0.50 → +0.123 on
development data; **+0.1736** on the official splits at the strictest 0.50 setting. Part of the prior's
power is analogue knowledge, and the monotonicity is the honest measure of how much.

## Level 4 — the null test (about 10 minutes on 16 cores)

```sh
python how-we-built-it/null_test.py 400 16
```

Expect the real value to exceed all 400 permutation controls; the summary is reproduced in
`how-we-built-it/null_test.md`. Each control gives every drug another drug's fingerprint, pathway set and
prior value, consistently in training and test, leaving responses, splits and tuning untouched.

## If a number differs

The live table governs the bar. Re-fetch it and re-decode it with
`../attempts/literature/code/live_table_check.py YOUR_NORMR2 YOUR_SE`; it prints the live maximum over
all models and both margin conditions. If the published maximum has risen above this claim's margin, the
claim no longer holds and should be marked as such.
