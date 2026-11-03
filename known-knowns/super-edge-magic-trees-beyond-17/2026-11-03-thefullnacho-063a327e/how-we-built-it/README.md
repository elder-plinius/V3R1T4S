# How the certificates were built

Everything here ran on one 8-core Linux machine (gcc 14.2.0, Python 3.13.5) inside a single scheduled V3R1T4S run
(run folder 2026-11-03-0818) and its same-day resumption. `PREREG.md` is the run's pre-registration, copied as
written (2026-11-03T08:20:26Z, before any attack output).

## Null test: waived, and why

`PREREG.md` says `null_test: not needed because each claim is an explicit object (a labeling per tree) checked by a
deterministic checker against the definition, with coverage checked against A000055.` kit/RUN.md step 3b allows
exactly this waiver ("an explicit object checked by a deterministic checker against a table value"). The claim is
not a search score or a "beats chance" statistic: each labeling either satisfies the definition or it does not, and
coverage is a count compared with OEIS A000055. A shuffled-input control has nothing to beat. In place of a null
test the checkers were calibrated on known positives and injected negatives (`code/run-checker/test_checker.py`,
output in `code/run-checker/test_output.txt`, including the exhaustive check that C4 has no SEM labeling), and the
package checkers were run on 18 corrupted copies and one unmodified control of the n=18 certificate (`../verify-it-yourself/RECEIPTS.md`).

## Requirements

- C compiler (the run used gcc 14.2.0): `cc -O2 -o sem_direct sem_direct.c` and `cc -O2 -o alpha_sem alpha_sem.c`.
- Python 3 standard library for every script except `code/trees/dump_trees.py`, which needs networkx (the run used
  networkx 3.7: `pip install networkx==3.7`).

## Steps

1. Trees: `python3 code/trees/dump_trees.py N > trees_nN.txt` for n = 18, 19, 20 (networkx `nonisomorphic_trees`;
   one line `n;edges` per tree). The checkers in `verify-it-yourself/` do not trust this list: they regenerate all
   trees independently and compare counts with A000055.
2. n = 18 and 19: `code/small-data-direct/run_order.sh N 5` (sem_direct with node cap 300, random restarts,
   5 shards, `timeout 2400`). n = 18 finished with 0 unlabeled; n = 19 left 2 trees, labelled by a longer
   sem_direct retry (larger cap) and merged with `code/small-data-direct/merge_retry.py`.
3. n = 20, in four stages (the run notes record the stages and parameters below; the exact shell lines of stages 2-4
   were not logged, so treat them as a description, not a transcript):
   1. sem_direct cap 300 on 5 shards, `timeout 2400`: 585641 labelled, 237424 left.
   2. `alpha_sem` (alpha-labeling search, then the map lower l -> k+1-l, upper u -> u+1) on the residue:
      77666 more, 159758 left.
   3. sem_direct on that residue, 8 shards: all but 3 labelled.
   4. `code/small-data-direct/caterpillar_sem.py` (the Enomoto-Llado-Nakamigawa-Ringel caterpillar construction)
      on the last 3 trees; all three are caterpillars.
   `code/small-data-direct/assemble_checked.py trees_n20.txt <stage outputs...>` keeps, for each tree, the first
   labeling that passes `check_sem`, and marks anything else RESIDUE; the final file has no RESIDUE line.
4. Separately, `code/structured-family/run_order.sh 18 5` built a second, independent certificate for n = 18 by the
   alpha route (`assemble.py`); it also passes the coverage check. It is not part of this package's object.

The search programs are randomised; rerunning them gives different (equally valid) labelings, not byte-identical
files. Rebuilding is not needed to check the claim: the certificates are checked directly.

`code/run-checker/` holds the checkers exactly as the run used them, kept for provenance. Their docstrings still
carry stale text from the previous run's odd-graceful checker, and an out-of-range vertex id makes them crash
(IndexError, never PASS). The fixed versions in `verify-it-yourself/` are the ones to use.
