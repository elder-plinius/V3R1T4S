# Honesty gate — voynich-generator-heldout-fingerprints (run 2026-11-16-1141)

status: CONFIRMED_SOLUTION
confirmed_scope: The unmodified Naibbe cipher (published Greshko 2025 tables, 414 cells / 356 strings, 52-card deck, 17/36 respacing, v1 ambiguity; procedure via the checksum-pinned driver that reproduces all published Naibbe values) run on 20 plaintexts (10 Latin + 10 Italian) x 10 seeds in both A- and B-mode (200 pooled runs) yields a pooled edit-1 adjacency-similarity ratio H1 of 0.7981 (A) and 0.7917 (B), which falls below the 99.9% Voynich quire-bootstrap envelope lower bound in all four dialect x transliteration cells (A/ZL3b 1.0690, A/IT2a 1.0271, B/ZL3b 0.9053, B/IT2a 0.9012) and below the minimum of all 16,000 Voynich bootstrap controls (0.8990), on a pre-registered statistic not among edge-glyph coupling, singleton/hapax rate, the 2604.19762 four signatures, or Greshko-2025's stated limitations — a genuine, non-subsumed outcome-(B) falsification.

Rationale (main session, steps 5-7):
- Three fresh-context skeptics (panel/reproduce.md, panel/novelty.md, panel/criterion.md) all
  end `pass: true`; each names a fresh context (fresh isolated OpenClaw subagent, given only
  claim/) and none is a same-session/role-play/single-context/main-session file.
- REPRODUCE: an independent stdlib checker (lru_cache lev1, cross-validated against naive
  Levenshtein on 200k random pairs) re-derived the pooled Naibbe H1 from the saved
  template-wrapped token streams = 0.7981215023387158 (A) / 0.791668403014533 (B), bit-identical
  to the stored values (no non-determinism across two runs). It confirmed the four 99.9%
  envelope cells, the 16,000-control minima, and the 20/20 per-plaintext secondary. One
  non-blocking packaging artifact was found and is recorded here: the saved pooled files carry
  8 (A) / 16 (B) fewer tokens than the stored n_tokens (3,049,184 vs 3,049,192; 3,057,184 vs
  3,057,200) — a template-wrap trailing-line-pop artifact (~0.0003%) that does not change any H1
  value. It does not affect the falsification.
- NOVELTY: one honest fetch of the status source (https://www.voynich.nu/transcr.html, HTTP 200,
  2026-11-16 13:59 UTC) and a bounded 24-month search found no post-2026-10-03 publication that
  already achieves the exact pooled, both-dialect, both-transliteration, 99.9%-Voynich-
  quire-bootstrap-envelope H1 falsification (the 2608.17096 Table-4 single-corpus 0.82-vs-1.12/
  1.20/1.07 is pre-cutoff and is a point estimate, not the 4-cell 99.9%-envelope + 16,000-control
  object).
- CRITERION: judged the criterion literally — the statistic is not in the excluded set; the
  object is unmodified Naibbe at default parameters (published 414-cell/356-string tables, 52-card
  deck, 17/36 respacing, v1 ambiguity); 20 plaintexts x 10 seeds (200 runs, both modes); the
  pooled H1 is outside the 99.9% envelope in EACH of the four (dialect x transliteration) cells;
  the null is the 16,000-control Voynich quire-bootstrap distribution (the real value is below
  its minimum); the baseline/ record is the same data / unmodified procedure / same metric; and
  the reproduction gate holds (recomputed Voynich H1 1.197/1.238/1.067/1.066 within +/-0.05 of
  the published 1.20/1.07). A genuine, non-subsumed outcome-(B) win.
- Downgrade checks (never upgrade): no hedging panelist (all three pass:true), no reproduction
  mismatch (bit-identical), the value is strictly better (below the 99.9% bound AND below all
  16,000 controls), no stretched criterion (outcome (B) read literally; the generator/partial
  A/p1/p2/p3 outcomes are the falsifier-lens complements and were NOT the confirmed object — they
  came back negative and are not widened into the scope), scope not wider than reproduced, the
  search was complete (the 200-run grid is exhaustive as stated), and the baseline was resolved
  (not left unresolved). The 8/16-token wrap artifact is a packaging detail, recorded, and does
  not touch the statistic, the null, or the envelope.
- The null_test.md (controls: 16000; real beats all controls: yes) is present and passes
  check_null; PREREG.md predates the null test (frozen before measuring).
