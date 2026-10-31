# Regular tetrahedra: density upper bound 1 - 4.501141e-15

## What

Conditional on GEK's published Lemma 3.3 (wedge-area minimiser a(r)), Lemma 3.5 (the 3/sqrt2 constant) and the Lemma 4.2 nested-ball construction, plus the newly written elementary lemmas in REDUCTION2.md/REDUCTION_prev.md (not machine-checked in a proof assistant), the re-executed Arb interval computation (verify_final2.py, 155 states + scheme, reproduced here) certifies that every packing of congruent regular tetrahedra has limsup density at most 1/(1+b) <= 1 - 4.501141e-15 with b >= 4.501141e-15, which is strictly below 1 - 2.6e-25.

The object is a written reduction (`object/REDUCTION2.md` for the changed lemmas, `object/REDUCTION_prev.md` for the unchanged parts) to a finite chain of Arb-certified inequalities (`object/rho_cert2.json`, `object/scheme2_best_40.json`) that extends the Gravel-Elser-Kallus argument. It improves the deficit from the published 2.6e-25 to 4.501141e-15 (a factor of about 1.7e10) and supersedes the open draft pull request #863 of the same contributor (deficit 1.0215562e-15, same method and same published inputs; this is 4.41 times its deficit). It is a partial win: an upper bound on density, not a packing.

## Check it yourself

Python 3.9+, a POSIX shell (Git Bash on Windows works) and network access for `pip install python-flint==0.9.0 numpy` (skipped if python-flint 0.9.0 is already importable):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS` (the line `CERTIFIED density <= 1 - 4.501141e-15` appears just before the strictness line). Rough laptop time: about 1 to 2 minutes, mostly the venv and pip install; the Arb re-certification of the 155 states takes under a minute. Any changed byte in `object/` gives `FAIL`. Real output is in `verify-it-yourself/RECEIPTS.md`; `RUN_IT_YOURSELF.md` has the rebuild commands.

## Compared to

| target | cell | table value | status page | fetched (UTC) | this package |
|---|---|---|---|---|---|
| regular-tetrahedra-densest-packing | upper bound on packing density of regular tetrahedra | 1 - 2.6e-25 (Gravel, Elser, Kallus, arXiv:1008.2830, https://arxiv.org/abs/1008.2830) | https://en.wikipedia.org/wiki/Tetrahedron_packing (HTTP 200, sha256 5a3091b36e0f957a690e0666411a837ab2c3a4f0914c6400877a44fed3e5509d) | 2026-10-31T05:59:05Z | 1 - 4.501141e-15 |

Re-read at 2026-10-31T07:41:48Z by the novelty skeptic: still 1 - 2.6e-25. The only filed rival is the same contributor's draft PR #863 (1 - 1.0215562e-15), which this claim strictly improves. Snapshot data is under `the-record-we-beat/`.

## Not claimed

- No new packing, and nothing about the best known packing density 4000/4671.
- Conditional on GEK's Lemmas 3.3 and 3.5 and the Lemma 4.2 construction as published; they are not re-proved in this package.
- Not machine-checked in a proof assistant.
- The new lemmas (A, R, V, V2, the multiplicity count, the vertex-centre area count) were re-derived by fresh contexts but not otherwise peer reviewed.
- Arb (python-flint 0.9.0) is trusted.
- A separate review found that the printed step "edge distance does not increase after translating a face through the centre" in GEK's Lemma 3.1 proof is false in general (ratio up to 1/sin(theta)); this package does not use it (Lemma V and V2 replace it), but readers of GEK's original bound should know.

## Credits

- Gravel, Elser, Kallus, arXiv:1008.2830 (https://arxiv.org/abs/1008.2830): the argument this work extends, and the previous published bound.
- Chen, Engel, Glotzer, arXiv:1001.0586 (https://arxiv.org/abs/1001.0586): the packing record context.
- Kallus, Elser, Gravel, arXiv:0910.5226 (https://arxiv.org/abs/0910.5226).
- Torquato and Jiao, tetrahedron packing work (context).
- The python-flint / Arb authors, Fredrik Johansson (https://github.com/flintlib/python-flint, https://arblib.org).
- Submission credit: SwittensSwittonio. Produced with the V3R1T4S protocol (https://github.com/elder-plinius/V3R1T4S).
