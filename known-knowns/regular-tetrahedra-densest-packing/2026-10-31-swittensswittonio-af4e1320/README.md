# Regular tetrahedra: density upper bound 1 - 1.0215562e-15

## What

Conditional on GEK's published Lemma 3.3 (the wedge-area minimiser W*), Lemma 3.5 and the Lemma 4.2 nested-ball construction, and on Arb (python-flint 0.9.0) being correct, every packing of congruent regular tetrahedra has limsup density at most 1 - 1.0215562e-15, with the argument re-executed and reconciled with the written reduction but not machine-checked in a proof assistant.

The object is a written reduction (`object/REDUCTION.md`) to a finite chain of Arb-certified inequalities (`object/rho_cert.json`, `object/scheme_best.json`) that extends the Gravel-Elser-Kallus argument. The bound is as rigorous as GEK's own published lemmas, plus Arb. It improves the deficit from 2.6e-25 to 1.0215562e-15 (a factor of about 3.9e9). It is a partial win: an upper bound on density, not a packing.

## Check it yourself

Python 3.9+, a POSIX shell (Git Bash on Windows works) and network access for `pip install python-flint==0.9.0 numpy` (skipped if python-flint 0.9.0 is already importable):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS` (the line `CERTIFIED density <= 1 - 1.021556e-15` appears just before it). Rough laptop time: about 1 minute, mostly the venv and pip install; the Arb re-certification itself takes a few seconds. Any changed byte in `object/` gives `FAIL`. Real output is in `verify-it-yourself/RECEIPTS.md`; `RUN_IT_YOURSELF.md` has the rebuild commands.

## Compared to

| target | cell | table value | status page | fetched (UTC) | this package |
|---|---|---|---|---|---|
| regular-tetrahedra-densest-packing | upper bound on packing density of regular tetrahedra | 1 - 2.6e-25 (Gravel, Elser, Kallus, arXiv:1008.2830, https://arxiv.org/abs/1008.2830) | https://en.wikipedia.org/wiki/Tetrahedron_packing (HTTP 200, sha256 5a3091b36e0f957a690e0666411a837ab2c3a4f0914c6400877a44fed3e5509d) | 2026-10-31T00:46:24Z | 1 - 1.0215562e-15 |

Re-read at about 2026-10-31T05:17Z by the novelty skeptic: still 1 - 2.6e-25. Snapshot data is under `the-record-we-beat/`.

## Not claimed

- No new packing, and nothing about the best known packing density 4000/4671.
- Conditional on GEK's Lemmas 3.3 and 3.5 and the Lemma 4.2 construction as published; they are not re-proved here.
- Not machine-checked in a proof assistant.
- The new Lemmas A, R and V were re-derived by three fresh contexts but not otherwise peer reviewed.
- Arb (python-flint 0.9.0) is trusted.
- An earlier certificate of 1 - 1.0748e-23 from an earlier lens is withdrawn: its exact wedge volume bound was found unsound. It is not part of this package.
- Brooks is not used in this claim version.

## Credits

- Gravel, Elser, Kallus, arXiv:1008.2830 (https://arxiv.org/abs/1008.2830): the argument this work extends, and the previous bound.
- Chen, Engel, Glotzer, arXiv:1001.0586 (https://arxiv.org/abs/1001.0586): the packing record context.
- Kallus, Elser, Gravel, arXiv:0910.5226 (https://arxiv.org/abs/0910.5226).
- Torquato and Jiao, tetrahedron packing work (context).
- The python-flint / Arb authors, Fredrik Johansson (https://github.com/flintlib/python-flint, https://arblib.org).
- Submission credit: SwittensSwittonio. Produced with the V3R1T4S protocol (https://github.com/elder-plinius/V3R1T4S).
