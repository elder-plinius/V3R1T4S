# Regular tetrahedra: density upper bound 1 - 4.501166e-15 with every lemma proved in the package

## What

Every packing of congruent regular tetrahedra in R^3 has limsup density at most 1 - 4.501166e-15 (strictly below 1 - 2.6e-25), by a Gravel-Elser-Kallus-style argument with all lemmas given written proofs in REDUCTION_FULL.md plus an Arb interval-arithmetic chain and an exact-integer K4' branch-and-bound (with eps=1/1000 slack) that I re-ran and that reproduced the stored outputs, resting on residual trust in the software and in human-checked, unrefereed paper proofs and standard-geometry facts (not machine-checked in a proof assistant).

The object is a written reduction (`object/REDUCTION_FULL.md`) to a finite chain of Arb-certified inequalities (`object/code/rho_cert.json`, `object/code/scheme_best_40.json`) and an exact-integer branch-and-bound (`object/code/k4_bb.py`) that extends the Gravel-Elser-Kallus argument. It improves the deficit from the published 2.6e-25 to 4.501166e-15 (a factor of about 1.7e10). It is a partial win: an upper bound on density, not a packing.

Relation to the same contributor's open draft pull requests #863 (deficit 1.0215562e-15) and #864 (deficit 4.501141e-15): both depend on three published lemmas of Gravel, Elser and Kallus (Lemma 3.3, Lemma 3.5, Lemma 4.2) that are not re-proved there. This package gives the same value as #864 up to the 5th digit (the margin 2.5e-20 is not a record margin) and re-proves those three lemmas (K1, K4 with a 1/1000 slack, K3) inside the package; that removal of the conditions is what is new. #864 and #863 are superseded by this one.

## Check it yourself

Python 3.9+, a POSIX shell (Git Bash on Windows works) and network access for `pip install python-flint==0.9.0 numpy` (skipped if python-flint 0.9.0 is already importable):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS` (the lines `RESULT: PROVED (all boxes certified)` and `CERTIFIED (Arb, modulo the Residual trust list) density <= 1 - 4.501166e-15` appear before it). Rough laptop time: 2 to 3 minutes, mostly the venv and pip install and the Arb re-certification (about 1 minute). Any changed byte in `object/` gives `FAIL`. Real output is in `verify-it-yourself/RECEIPTS.md`; `RUN_IT_YOURSELF.md` has the rebuild commands.

## Compared to

| target | cell | table value | status page | fetched (UTC) | this package |
|---|---|---|---|---|---|
| regular-tetrahedra-densest-packing | upper bound on packing density of regular tetrahedra | 1 - 2.6e-25 (Gravel, Elser, Kallus, arXiv:1008.2830, https://arxiv.org/abs/1008.2830) | https://en.wikipedia.org/wiki/Tetrahedron_packing (HTTP 200, sha256 5a3091b36e0f957a690e0666411a837ab2c3a4f0914c6400877a44fed3e5509d) | 2026-10-31T05:59:05Z | 1 - 4.501166e-15 |

Re-read at 2026-10-31T09:48:55Z by the novelty skeptic: still 1 - 2.6e-25. Snapshot data is under `the-record-we-beat/`.

## Not claimed

- No new packing, and nothing about the best known packing density 4000/4671.
- Not machine-checked in a proof assistant and not refereed: the lemmas have written human-checked proofs (K1, K3, V2, Lemma A, Lemma R, the counting claims, boundary argument) plus Arb/exact-integer computations; Arb (python-flint 0.9.0), CPython and the two programs are trusted; standard geometry facts are used without proof (`object/REDUCTION_FULL.md`, section 10).
- K4 (GEK Lemma 3.5) is proved only with the constant (3/sqrt2)(1+1/1000).
- A review found that GEK's Lemma 3.1 proof step "the edge distance does not increase after translating a face through the centre" is false as printed (ratio up to 1/sin(theta); `how-we-built-it/edge_dist_counter.out`); this package does not use it. Readers of the original bound should know. (Retraction duty: GEK's published value 1 - 2.6e-25 is not shown wrong here, only that step of its proof.)
- The same value is not a new record against #864; only the removal of unproved inputs is new.

## Credits

- Gravel, Elser, Kallus, arXiv:1008.2830 (https://arxiv.org/abs/1008.2830): the argument this work extends, and the previous published bound.
- Chen, Engel, Glotzer, arXiv:1001.0586 (https://arxiv.org/abs/1001.0586): the packing record context.
- Kallus, Elser, Gravel, arXiv:0910.5226 (https://arxiv.org/abs/0910.5226).
- The python-flint / Arb authors, Fredrik Johansson (https://github.com/flintlib/python-flint, https://arblib.org).
- Submission credit: SwittensSwittonio. Produced with the V3R1T4S protocol (https://github.com/elder-plinius/V3R1T4S).
