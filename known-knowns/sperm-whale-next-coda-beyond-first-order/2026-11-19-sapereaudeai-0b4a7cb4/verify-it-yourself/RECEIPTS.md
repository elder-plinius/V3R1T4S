# Receipts

The real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder on
2026-11-19T12:55:55Z, CPython 3.11, standard library only, no network. Elapsed: about 10 seconds.

```
ok   object/ holds exactly the expected files (bin_edges.csv, content_summary.json, folds.csv, per_position_bits.csv, run_output.txt)
ok   object/bin_edges.csv sha256 matches (c05e94716fa83081)
ok   object/content_summary.json sha256 matches (9d2c0aecae9623a8)
ok   object/folds.csv sha256 matches (675bd6cbd2250d2e)
ok   object/per_position_bits.csv sha256 matches (0b4a7cb45ddd85aa)
ok   object/run_output.txt sha256 matches (b40802b0eb0a38d9)
ok   3418 scored positions (bank: 3418)
ok   every scored position has at least 2 earlier codas in its stream
ok   5 folds in folds.csv, each held out once
ok   every position is scored in the fold its REC belongs to
ok   per-fold counts match content_summary.json (514, 1305, 508, 692, 399)
ok   R1    per-position losses are all finite and strictly positive
ok   twin  per-position losses are all finite and strictly positive
ok   rep   per-position losses are all finite and strictly positive
ok   local per-position losses are all finite and strictly positive
ok   full  per-position losses are all finite and strictly positive
ok   R1    pooled 2.780154 bits, matches content_summary.json (2.780154)
ok   twin  pooled 2.654909 bits, matches content_summary.json (2.654909)
ok   rep   pooled 2.565329 bits, matches content_summary.json (2.565329)
ok   local pooled 2.335085 bits, matches content_summary.json (2.335085)
ok   full  pooled 2.123847 bits, matches content_summary.json (2.123847)
ok   condition (1): R1 - full = 0.656306 bits, at least 0.10
ok   condition (2a): twin - full = 0.531062 bits, at least 0.05
ok   188 REC groups own a scored position
ok   condition (2b): own-seed 95% paired REC bootstrap [0.4588, 0.6322] excludes 0
ok   null test ran 400 controls (at least 400)
ok   null test: the real gain beat every control
ok   null test real gain 0.5310621359536837 equals the twin gain recomputed here (0.531062136)
ok   real 0.531062 is above the best control 0.010643

Both conditions of the bank criterion hold on the shipped object:
  full          2.123847 bits per coda over 3418 scored codas
  R1            2.780154   gain 0.656306  (threshold 0.10)
  cut twin      2.654909   gain 0.531062  (threshold 0.05, 95% [0.4588, 0.6322])
PASS
```

Exit status 0.

Note on the bootstrap line: the checker runs its own 10,000-resample paired bootstrap over REC groups with
its own seed (8675309), deliberately not the claim's seed (20261119). It gets [0.4588, 0.6322] where the
claim reports [0.4571, 0.6325]. Both exclude 0 by a wide margin, which is what condition (2) requires.

## Corrupted-copy behaviour

Checked by hand as well as by the kit: flipping one digit in the first file of `object/` (bin_edges.csv) makes
the checker exit 1 with `FAIL` as its last line, naming the file whose sha256 no longer matches. The checker
stops before reporting any cross-entropy in that case, because a changed object means the shipped numbers can no
longer be attributed to it.
