## What

The unmodified Naibbe cipher (published Greshko 2025 tables, 414 cells / 356 strings, 52-card deck, 17/36 respacing, v1 ambiguity; procedure via the checksum-pinned driver that reproduces all published Naibbe values) run on 20 plaintexts (10 Latin + 10 Italian) x 10 seeds in both A- and B-mode (200 pooled runs) yields a pooled edit-1 adjacency-similarity ratio H1 of 0.7981 (A) and 0.7917 (B), which falls below the 99.9% Voynich quire-bootstrap envelope lower bound in all four dialect x transliteration cells (A/ZL3b 1.0690, A/IT2a 1.0271, B/ZL3b 0.9053, B/IT2a 0.9012) and below the minimum of all 16,000 Voynich bootstrap controls (0.8990), on a pre-registered statistic not among edge-glyph coupling, singleton/hapax rate, the 2604.19762 four signatures, or Greshko-2025's stated limitations — a genuine, non-subsumed outcome-(B) falsification.

Target: voynich-generator-heldout-fingerprints. Outcome (B) of the success criterion (quoted
verbatim in the-record-we-beat/criterion_verbatim.txt): a pre-registered falsification of Naibbe
on a statistic outside the excluded set, unmodified Naibbe (20 plaintexts x 10 seeds) outside the
99.9% Voynich envelope on A and B and both transliterations. This is a falsification, not a
decipherment, and not the (generator) outcome (A) / p1 / p2 / p3 (those were probed and came back
negative; they are not the confirmed object).

## Check it yourself

    sh verify-it-yourself/run_checks.sh

Expected last line: PASS (recomputes the pooled Naibbe H1 from objects/pooled_{A,B}.wrapped.txt
and checks the four 99.9% envelope cells, the 16,000-control minima, and the 20/20 per-plaintext
secondary). Rough laptop time: ~30 s.

## Compared to

- Published Naibbe H1 (arXiv 2608.17096, Rozanova & Temerev 2026, Table 4): Naibbe (Caesar) 0.82
  vs Voynich 1.12 (A 1.20, B 1.07) — a single-corpus, ZL-only point estimate (pre-cutoff).
- This object: the pooled, both-dialect (A and B), both-transliteration (ZL3b and IT2a)
  99.9%-Voynich-quire-bootstrap-envelope falsification (4 cells) with a 16,000-control null, on the
  pre-registered statistic. The run's reproduced Naibbe H1 is 0.825 (vs published 0.82); the
  recomputed observed Voynich H1 is 1.197/1.238 (A) and 1.067/1.066 (B) vs published 1.20/1.07.
- Status source: https://www.voynich.nu/transcr.html (HTTP 200, 2026-11-16T11:42:08Z, sha256
  57f8aaf6b1cdd6a292361b3a94e723f8fb14f0960b2cb349acee142fbadb19a5) — see the-record-we-beat/.

## Not claimed

- Not a decipherment of the Voynich manuscript (the criterion states neither outcome is a
  decipherment).
- Not outcome (A) (a matching generator) and not any of the p1/p2/p3 partial wins (the generator
  lens was negative; its measured ceilings are in the run's attempts/generator/).
- The pooled streams are the template-wrapped Naibbe output; the 8 (A) / 16 (B) token gap vs the
  stored n_tokens is a wrap trailing-line-pop artifact (~0.0003%) that does not change any H1
  value (recorded in panel/gate.md).

## Credits

- Greshko 2025, greshko/naibbe-cipher (the cipher under test; published tables + 52-card deck).
- Rozanova & Temerev, arXiv 2608.17096 (the Naibbe failure statistics incl. Table-4 H1, and the
  single-corpus 0.82-vs-1.12 record this falsification builds on).
- arXiv 2604.19762 (4-signature test) and arXiv 2604.25979 (Parisel switch) — the held-out
  statistics and the criterion's neighbouring cells.
- SoylentAquamarine/voynich-collective PR16 (the pre-cutoff Naibbe audit).
- The V3R1T4S target bank (voynich-generator-heldout-fingerprints, pinned commit 25c99686).
## Large object files (kept out of git, listed here)

Two object files exceed the 1 MB per-file package limit, so they are kept outside this package
(and outside git); their sizes and sha256 are recorded here and a public archive URL is created by
the human before opening the PR. The machine-readable object that IS in the package is
object/ (naibbe_batch.json with the 200 per-run + pooled stats + per-plaintext H1 means + per-run
shas; the four env_H1 99.9%-envelope files; null_H1_bootstraps.json with the 16,000-control
minima; observed_*.json; naibbe_tables.json). The checker verifies the falsification from those
JSON objects (stored pooled H1 0.7981 A / 0.7917 B, the four 99.9% envelope cells, the 16,000-
control minima, the 20/20 per-plaintext secondary). When the two large streams are present next to
them (in the run's claim/objects/ or object/), the checker additionally re-derives the pooled H1
from them bit-exactly. The large streams:
- object/pooled_A.wrapped.txt (template-wrapped pooled A-mode Naibbe output, 3,049,184 tokens;
  ~19 MB)
- object/pooled_B.wrapped.txt (template-wrapped pooled B-mode Naibbe output, 3,057,184 tokens;
  ~19 MB)
The 8 (A) / 16 (B) token gap vs the stored n_tokens in naibbe_batch.json is a template-wrap
trailing-line-pop artifact (~0.0003%) that does not change any H1 value (recorded in
panel/gate.md).

## Recreation of the large streams (verified bit-exact)

Both streams are fully deterministic and were re-generated on 2026-11-16 with a
byte-identical result (sha256 match against the stored copies):

    # pinned inputs (public repos at fixed commits):
    #   lrozanova/voynich-units  @ 956a7c4fc39981f4d116fa3f4edfccce6d065571 (checksum-pinned driver + caesar_words output)
    #   greshko/naibbe-cipher    @ 5145f526b52741a6dca14201147f687e62c7162e (published table source; examples/divina_commedia.txt)
    #   object/naibbe_tables.json (in this package; identical to the driver's control table)
    python3 how-we-built-it/code/plaintexts.py    # -> output/plaintexts.json (template sha256 b9cb5b81c4966ca4)
    python3 how-we-built-it/code/dump_pooled.py   # -> output/pooled_{A,B}.wrapped.txt

Every RNG draw in the generator is seeded from the frozen seed grid (SEEDS = 2026111601..2026111610,
per PREREG §5); no unseeded global state. Verified sha256:
- pooled_A.wrapped.txt  e45c01a40a0902c6ac88bbd537dd8352d90e14bee7c425dbe3b7eb8926aa066b
- pooled_B.wrapped.txt  d24eb35509d01470e1f69bae0e913cffc6eb3677dbd1a0d82141ebbd1d7c56e8
