# Run it yourself

Four levels, cheapest first. Level 1 needs nothing but Python 3. The rest need the source data, numpy and scipy.

## 1. Check the shipped object (a few seconds, standard library only)

```sh
sh verify-it-yourself/run_checks.sh
```

This is the check described in `README.md`. It hashes `object/`, rebuilds the scored set from the fold table and
the vocabulary, recomputes both pooled cross-entropies from the per-position losses, checks p3's 0.05-bit
threshold, runs its own 10,000-resample paired bootstrap over the 96 rewritten-Date groups under seed `31415926`,
and checks both null tests against all 800 shipped control gains. Last line `PASS` or `FAIL`.
`verify-it-yourself/RECEIPTS.md` lists every check and the expected output.

## 2. Refit the model from the source data (about 2 minutes, needs numpy and scipy)

Fetch the pinned CSV into a `data/csv/` folder beside this one:

```sh
mkdir -p data/csv
curl -L -o data/csv/DominicaCodas.csv \
  https://raw.githubusercontent.com/pratyushasharma/sw-combinatoriality/7228c8ee/data/csv/DominicaCodas.csv
```

Expected sha256 `53dd44fb...6b45`, 747,518 bytes. **Do not load the repository's `.p` files**: unpickling runs
code, and the bank says so. The CSV holds everything needed.

Then:

```sh
python3 -I how-we-built-it/code/score_p3.py data/csv/DominicaCodas.csv out
```

The first argument is the CSV, the second an output directory.

### What the refit should reproduce

Per fold, the held-out cross-entropy of each of the five fitted families:

| fold | n | bigram | one | rep | local | full |
|---|---|---|---|---|---|---|
| 0 | 1327 | 1.507673 | 1.495092 | 1.475949 | 1.383141 | 1.364413 |
| 1 | 1914 | 1.705945 | 1.687393 | 1.686021 | 1.614154 | 1.593230 |
| 2 | 2003 | 1.870903 | 1.872645 | 1.864615 | 1.753759 | 1.721340 |
| 3 | 1568 | 1.848438 | 1.848885 | 1.829031 | 1.737927 | 1.697788 |
| 4 | 1689 | 1.594055 | 1.592983 | 1.579180 | 1.519230 | 1.505194 |

Pooled: bigram 1.7179142139602834, one 1.712053332868193, rep 1.7004598342704087, local 1.6149567452692102,
full 1.589491467897628. The claimed gain is `bigram - full` = 0.1284227460626554 with interval
[0.08793142691897537, 0.16299376323756598]. The additive smoothing of the bigram comes out at alpha = 0.3 on every
fold.

`out/p3_summary.json` should match `object/p3_summary.json`. The per-position probability files it writes,
`p3_probs_bigram.csv` and `p3_probs_full.csv`, are 6.5 MB each and are **not shipped**, because this repository
caps a package file at 1 MB. `object/p3_per_position.csv` is derived from them: for each scored position it holds
the log-loss of the bigram and of the full model, which is what every number in the claim is computed from. To
confirm the derivation, take `-log2` of the probability each file assigns to that row's `y_token`; the two agree
to 9e-15.

`object/run_output.txt` is the frozen run's own console output, including the per-fold leakage results: every
field of the predicted coda and of every later coda was rewritten and re-scored, 0 of 42,505 checks moved a
prediction, and a deliberately leaky control feature was flagged at every one of the 8,501 positions.

## 3. The stream-local reference, and the ordered component

`local` in the table above is the stream-local reference: the same model family reading an order-free bag of the
stream's earlier codas. `full - local` is the ordered component, 0.025465 bits, which is the figure the
composition-preserving control tests. It is **not** recomputable from `object/`, because `local`'s per-position
probabilities are not shipped; the refit in section 2 produces it.

## 4. Rebuild the composition-preserving control (about 2 h 10 m on nine workers)

```sh
python3 -I how-we-built-it/composition-null/nulls_n5.py N6 data/csv/DominicaCodas.csv 0 400 nulls5/N6_a.csv
```

Each control permutes the coda records within each stream - the whole record moving as a unit, so the stream's
multiset of records is preserved exactly and only the order is destroyed - then reruns the frozen pipeline end to
end. All 400 control gains as this run computed them are in `how-we-built-it/composition-null/n6_controls.csv`,
with the design, the correction to its statistic, and the result in the same folder. See the note there about the
`sys.path` entries needing adjustment inside a package layout.

## 5. Rebuild the N3 null test (about 400 x 2 minutes, or split across workers)

```sh
python3 -I how-we-built-it/null/nulls.py N3 data/csv/DominicaCodas.csv 0 400 nulls/N3_a.csv
```

All 400 gains as computed here are in `how-we-built-it/null/N3_controls.csv`. The runner checkpoints each control
and skips indices already present, so it can be stopped, restarted and split by giving each worker a different
index range.

## Reading the claim itself

`how-we-built-it/CLAIM.md` is the claim as written during the run, `how-we-built-it/PREREG.md` the
pre-registration frozen at 2026-11-19T09:55:11Z before any held-out score existed, and
`how-we-built-it/PREREG.v2.md` the escape-hatch record - worth reading, because it is where the `IDN` string
quirk described in `README.md` was found and deliberately left unfixed. `panel/` holds the three independent
skeptic verdicts, the honesty gate and the freeze audit. `prompt/` holds the run prompt and charter, with the
workspace path replaced by a placeholder.
