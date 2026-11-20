# Baseline reproduction record (step 3c) — 2026-11-16

## What was reproduced
Command (captured output: baseline/naibbe_driver.log, 43 s wall; JSON: baseline/
naibbe_driver.json; Caesar ciphertext dump: baseline/naibbe_caesar_ciphertext.txt):
  <workdir>/.venv/bin/python data/voynich-units/analysis/reproduce_naibbe_control.py \
    data/voynich-units/voynich_decipherment_repro_bundle --skip-attack --skip-crossing \
    --shuffles 100 --json-output baseline/naibbe_driver.json \
    --dump-ciphertext baseline/naibbe_caesar_ciphertext.txt
Object: the checksum-pinned driver lrozanova/voynich-units @ 956a7c4 (analysis/
reproduce_naibbe_control.py sha256 df9f01ed8f5eefa03830e4e31904d7163e902119988e9138074ac5cb1e9ecd8e,
tables JSON 46c1235a..., Pliny ciphertext 9cdf2de1... — all re-verified locally against
the PR16 pinned hashes, all match), re-implementing Greshko's Naibbe procedure from the
published tables, default parameters (52-card deck alpha20/beta8x3/gamma4x2, 17/36
respacing, v1 ambiguity rule), encrypting the package's Caesar (De Bello Gallico I-IV)
plus the author's shipped Pliny ciphertext.

## Expected (published: 2608.17096 Table 7 + PR16 JSON + 2604.19762 Table 1) vs reproduced
| statistic | published (expected) | reproduced (driver/JSON) | gate (PREREG s3) |
|---|---|---|---|
| Voynich H1/H2 (collapsed) | 3.976 / 2.690 (paper 2.69) | 3.976 / 2.690 | PASS |
| Voynich BPE k64 gap / min | 1.045 / 64 (paper D64 1.05) | 1.0448 / 64 | PASS |
| Voynich order share cap2000 | 0.79% (paper 0.79%) | 0.794% | PASS |
| Voynich hapax | 69.7% (paper ~70%) | 69.68% | PASS |
| Naibbe/Caesar H1/H2 | 3.979 / 2.707 | 3.979 / 2.707 | PASS |
| Naibbe/Caesar BPE k64 | 1.028 / min 64 | 1.0276 / 64 | PASS |
| Naibbe/Caesar order | 1.25% | 1.247% | PASS |
| Naibbe/Caesar hapax | 40.5% | 40.52% | PASS |
| Naibbe/Pliny (shipped) hapax / order / H2 | 41.7% / 1.06% / 2.712 | 41.68% / 1.062% / 2.712 | PASS |
| Shipped-sample table check | 34,764 tokens, 0 unreproducible | 34,764 tokens, 16,887 unigram + 17,877 bigram reproduced, 0 unreproducible | PASS |

Edge-glyph coupling (S1) and the 4 signatures (S5-S8) and the switch (S9) are NOT in this
driver's output; they are reproduced from the fetched corpora by this run's own
statistic library (expected-vs-reproduced recorded there, against 0.197/5.7% [Voynich],
0.006/0.2-0.3% [Naibbe], Table-1 references [S5-S8], and p1=0.682/p0=0.160 [S9]).
PR16 JSON edge crossfit (alpha=1): Voynich +0.1871 (16/16 blocks) vs Naibbe/Caesar
-0.0016 (5/16) / Pliny -0.0020 (5/16); paired p=1.53e-05 (copied verbatim from the PR16
summary JSON, data/pr16/...).

## What could NOT be reproduced within budget
- The driver's calibrated substitution-attack differential (run with --skip-attack; the
  attack is not part of this run's scoring statistics).
- The erased-space BPE crossing (run with --skip-crossing; the graded-space regime is
  explicitly out of scope for the hand-executable generator, which does not emit an
  uncertain-space channel, so the criterion's space-regime clause does not bind).
- The driver used the bundle's ZL3b.txt (identical content to the fetched ZL3b-n.txt;
  both are "Version 3b of 13/05/2025" per the file headers) — envelopes for THIS run are
  recomputed from the fetched ZL3b-n.txt / IT2a-n.txt by the statistic library, not from
  the bundle.
