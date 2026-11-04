# f(3,6) = 13: no three tournaments on 12 vertices have every 6-subset dominated

## What

There is no set of three tournaments on 12 vertices with property S_6 (Jeffries, arXiv:2604.08790, Definition 2.1), shown by a three-level cube-and-conquer certificate of 2,871 LRAT proofs, each accepted by the verified checker cake_lpr and all regenerated and re-checked in a second full run with matching hashes, relative to the written normal-form arguments and the Python cover-lemma construction; with the 13-vertex S_6 object in this package and monotonicity in the number of vertices, this gives f(3,6) = 13 (partial win p1).

In plain words: Jeffries (arXiv:2604.08790, Figure 7) showed that 13 vertices suffice for three tournaments with property
S_6 and left open whether fewer would do. This package shows 12 do not, so the smallest number is exactly 13. This is
partial win p1 of the bank entry `schutte-multiple-tournament-dice-bounds` (an exact value by a verified UNSAT
certificate), not its main criterion (no smaller construction exists, by this result).

How the certificate is built: the question "do three tournaments on 12 vertices have S_6?" is written as a SAT formula
(encoder in how-we-built-it/certify/encoder/) with a normal form that fixes a vertex's out-degree and some neighbourhood
counts. The space is split into 2,809 cubes (126 at level 1, 114 at level 2, 2,569 at level 3), and 62 cover lemmas
(1 + 21 + 40, built by how-we-built-it/certify/certlib.py) prove that the cubes of each split cover their parent. Every one
of these 2,871 formulas was solved by CaDiCaL 1.9.5 with a DRAT proof, converted to LRAT by drat-trim, and accepted by
cake_lpr, the CakeML-verified LRAT checker (`s VERIFIED UNSAT`). object/certificate_m3k6n12.tsv lists every job with its
formula's sha256 and size and its proof's sha256 and size. The proofs (up to 2 GB each) are regenerated, not stored:
CaDiCaL is deterministic here, and a second full run on 2026-10-30 reproduced every formula hash, proof hash and LRAT size.

What stays trusted (not machine-checked): that the encoder and its normal form match Definition 2.2 (argued in
how-we-built-it/proofs-of-lemmas/, checked line by line by a reviewer and re-encoded independently by the REPRODUCE
panelist, who got identical base clauses), that the cover lemmas' formulas say what certlib.py intends, and the C wrapper,
compiler and OS under cake_lpr.

Second encoder (2026-11-03): a fresh agent that never saw our code wrote a second encoder from the paper's definitions alone
(how-we-built-it/second-encoder/enc2/). On 13 small cells it gives the same answer as ours on all 379 level-1 cubes, and
f(2,4) = 10 with no normal form at all; on 12,813 full arc assignments both formulas and a direct check of Definition 2.1
always agree; on seeded samples of the real cells (30 cubes of (2,5,13), 20 level-1 leaves of (3,6,12)) both say UNSAT; and
both accept the (2,5,14) and (3,6,13) witnesses and agree on every single-arc flip of them. No disagreement anywhere
(how-we-built-it/second-encoder/RESULT.md). It does not re-run the whole certificate with the second encoder.

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. About 5 minutes on an Apple M-series laptop. It checks the 13-vertex object from Definition 2.1,
that the job list is exactly the cover tree, 40 rebuilt formulas, and re-proves 6 of the 2,871 jobs (the root cover lemma
and 5 seeded small ones) through CaDiCaL, drat-trim and cake_lpr. `FULL=1 sh verify-it-yourself/run_checks.sh` re-proves
all 2,871 (about 27 CPU-hours, 4.5 GB peak per job). Needs python3 3.10-3.12, git, a C compiler, network access to pypi.org
and github.com, about 5 GB of memory. Details: RUN_IT_YOURSELF.md; real output: verify-it-yourself/RECEIPTS.md.

## Compared to

| what | value | source | fetched (UTC) |
|---|---|---|---|
| arXiv:2604.08790 v1, Figure 7, cell (m,k) = (3,6) | 13, unstarred (an upper bound; starred cells are exact). Section 4: no non-trivial lower bound for f(m,k) | https://arxiv.org/abs/2604.08790 | 2026-11-02T06:27:43Z |
| this package | **f(3,6) = 13** (lower bound 13 by the certificate; upper bound 13 by the paper's Proposition 2.3 and by object/witness_m3k6n13.json) | object/certificate_m3k6n12.tsv | - |

Snapshot with hashes: the-record-we-beat/RECORD.md.

## Not claimed

- Not the bank's main criterion: no construction below 13 is given, because none exists.
- Nothing about f(2,5). Draft PR #816 (DmitrL-dev, 2026-10-29) claims f(2,5) = 14 with its own certificate.
- Not one formula with one proof: the certificate is 2,871 checked proofs joined by the cover lemmas, and the claim rests
  on the cover tree being complete (checked by verify-it-yourself/check_cert.py and by the REPRODUCE panelist).
- Not a statement about physical dice: only tournament matrices.
- Prior public mention: draft PR #816 reports that CaDiCaL found its own (3,6,12) formula UNSAT, without a checked
  certificate (cake_lpr ran out of memory there), and explicitly makes no claim about f(3,6). That is the same outcome,
  unverified; this package supplies the verified certificate.

## Credits

- Joel Jeffries, "Schütte's property for sets of tournaments and an application to dice games", arXiv:2604.08790
  (https://arxiv.org/abs/2604.08790): definitions, Proposition 2.3, Figure 7.
- CaDiCaL (Armin Biere et al.) through python-sat 1.9.dev17 (Alexey Ignatiev et al., https://github.com/pysathq/pysat).
- drat-trim (Marijn Heule et al., https://github.com/marijnheule/drat-trim).
- cake_lpr (Yong Kiam Tan, Marijn Heule, Magnus Myreen, https://github.com/tanyongkiam/cake_lpr), built on CakeML.
- DmitrL-dev, draft PR #816 in this repository, for the independent f(2,5) certificate and the public (3,6,12) report.
- Contributor: sartoshi-foot-dao. Work done by Claude (Anthropic) research sessions in the contributor's workspace; panel by three
  fresh-context Claude Opus 5.5 sessions.
