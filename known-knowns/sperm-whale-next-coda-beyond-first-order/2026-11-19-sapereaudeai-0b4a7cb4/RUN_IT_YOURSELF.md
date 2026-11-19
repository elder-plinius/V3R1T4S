# Run it yourself

Two levels. The first checks the claim's arithmetic from the shipped object and needs nothing but Python 3. The
second refits the model from the source data and reproduces the probability files byte for byte.

## 1. Check the shipped object (about 10 seconds, standard library only)

From this package folder, in a fresh shell:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line:

```
PASS
```

The full expected output is in `verify-it-yourself/RECEIPTS.md`. If your `python3` is not on the path under that
name, set `PYTHON`, for example `PYTHON=python sh verify-it-yourself/run_checks.sh`.

## 2. Refit from the source data (about 12 minutes, needs numpy and scipy)

The data file is not copied into this package. Fetch it by URL and check its checksum first:

```sh
mkdir -p data/csv
curl -sSL -o data/csv/sperm-whale-dialogues.csv \
  https://raw.githubusercontent.com/pratyushasharma/sw-combinatoriality/7228c8eed2cc27ddd23b74c51aeccec9d762389e/data/sperm-whale-dialogues.csv
python3 -c "import hashlib;print(hashlib.sha256(open('data/csv/sperm-whale-dialogues.csv','rb').read()).hexdigest())"
```

Expected: `1856c8bf915cc5ae6f928aaa2036cbbc6ad8840bb6e4f6a96aaeb96953215da2` (500,380 bytes). The URL pins the
repository commit, so the bytes do not move under you.

**Do not load that repository's `.p` files.** Unpickling runs code, and the bank's own entry warns about it. The
two CSV files hold everything this claim uses.

Then put the frozen code where it expects to be and run the scorer:

```sh
mkdir -p attempts/evaluator/code attempts/sequence-model/code
cp how-we-built-it/code/swlib.py how-we-built-it/code/leak.py attempts/evaluator/code/
cp how-we-built-it/code/seqlib.py how-we-built-it/code/seqpipe.py how-we-built-it/code/score_content.py attempts/sequence-model/code/
python3 -I attempts/sequence-model/code/score_content.py data/csv/sperm-whale-dialogues.csv out/
```

Requirements: numpy and scipy (the run used numpy 2.4.6 and scipy 1.17.1 on CPython 3.11). The run's own printed
output is shipped as `object/run_output.txt` for comparison; expect identical numbers and different elapsed
seconds.

### What the refit should reproduce

| file | bytes | sha256 |
|---|---|---|
| probs_R1.csv | 3,632,192 | 7dbfd5df7090838e3f0d625c91c49220b0a39c6a5519e3f3fa9d7202bc5cdcd7 |
| probs_twin.csv | 3,763,606 | d708d63a1a827a1d8a3f60dba5962e87772748e84cd03f801da1eda202e6bc02 |
| probs_full.csv | 3,788,211 | d456be16fa2a8c6ea0fd1ef601c34ab75266435b13a00dba0ce886f440e9e7fe |
| probs_rep_diagnostic.csv | 3,761,738 | 804ae22608eefa040adf26c86c20a244c15604dd1e9325f9b2630f1babbe9313 |
| probs_local_diagnostic.csv | 3,782,864 | b2a257ee09115102ab6efca646aff42110a4fa16b88c97452e8619bde21125e1 |
| folds.csv | 3,755 | 675bd6cbd2250d2eaf24fe560ee22e4889a683876fe4d070ad97d117a8519e82 |
| bin_edges.csv | 327 | c05e94716fa83081c247b1200aa259a68d91c75bd4d89b6c64046c7182903967 |
| content_summary.json | 12,407 | 9d2c0aecae9623a83a51db0f3d69e8157100f2c128910027af3599c0e3a09a5f |

The five probability files are 3.6 to 3.8 MB each, over this repository's 1 MB per-file limit, so they are listed
here rather than shipped. They are regenerable by the command above, and this package's `object/` carries what
every claimed number is computed from: the per-position log-loss of each model at each of the 3,418 scored
positions. No public archive copy of the probability files has been created.

The run's REPRODUCE panellist did this refit independently, with its own feature code and its own optimiser,
before reading the author's code, and reported pooled twin 2.654906 against the shipped 2.654909 and pooled full
2.123844 against 2.123847, tracing the 3e-6 bit difference to optimiser tolerance and to rounding in four tail
features. It also reran the frozen pipeline and got the same sha256 values as the table above.

## 3. Rebuild the null test (about 14 hours of CPU, or 2 hours on 6 workers)

```sh
python3 -I how-we-built-it/code/nulls.py N2 data/csv/sperm-whale-dialogues.csv 0 400 nulls/N2_a.csv
```

`how-we-built-it/code/nulls.py` is that script, with `fastfeats.py` (its vectorised feature path) and
`make_null_test.py` (the aggregator that writes `null_test.md` from the per-control files).
`how-we-built-it/null_test.md` records the design, the exact command, all 400 control gains in summary and the
speed shims that were checked bit-identical against the frozen code before use. Each control reruns the
whole frozen pipeline, all five folds and all inner cross-validation, on data resimulated from a first-order
Markov chain over coda records. Workers checkpoint each control and skip indices already present, so the job can
be stopped and restarted.

## 4. Rebuild the composition-preserving controls (about 2.6 hours on 9 workers)

```sh
python3 -I how-we-built-it/composition-null/nulls_n5.py N5 data/csv/sperm-whale-dialogues.csv 0 400 nulls5/N5_a.csv
python3 -I how-we-built-it/composition-null/nulls_n5.py N6 data/csv/DominicaCodas.csv 0 400 nulls5/N6_a.csv
```

These are the post-hoc diagnostic described in `how-we-built-it/composition-null/README.md`, not part of the
claim's gate. Each control permutes the coda records within each stream, keeping the stream's exact multiset of
records and destroying only their order, then reruns the frozen pipeline end to end. All 800 control gains are
shipped in `n5_controls.csv` and `n6_controls.csv`, the designs in `PREREG.N5.md` and `PREREG.N5.v2.md`, and the
result with its integrity checks in `RESULT.md`.

One honest obstacle: `nulls_n5.py` imports the frozen pipeline modules through a `sys.path` entry of the form
`code/../../evaluator/code`, which exists in the run folder but not in this package layout, so the import paths
need adjusting before it will run from here. The frozen files were not edited to fix that. The same defect is
noted against `how-we-built-it/code/`.
