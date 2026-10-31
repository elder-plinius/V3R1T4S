# Skeptic Panel Gate (`indus-temporal-heldout-structure`)

claim_type: partial_win
partial_win: p3
target: indus-temporal-heldout-structure
reproduce_pass: true
novelty_pass: true
criterion_pass: true
confirmed_scope: Partial win p3 (structural finding) on indus-temporal-heldout-structure: on 999 deduplicated post-1977 held-out Indus inscriptions (3,731 tokens in object/post1977_heldout_predictions.csv, sha256 7e7bfba35edfd160ddaa54bacec5babebfe2d182e1c4cb60a1272a801d8cf448, with zero M77 object, loop24, seal-identity, or sequence overlap), the 25 pre-1977 frozen M77 telescoping composite/bigram pairs in object/m77_frozen_structural_model.json (sha256 b40b1ef7b100e944aa1d86efa3b8f7dbdfbcd15885ab785e25e7e7454b1451a3, trained solely on 2,165 deduplicated M77 sequences from data/im77/im77_corpus_lines.csv and data/derived/bridge_extended.json in paragorth/Indus- commit d62ec82d58642038640da25a97177d7a1fddc9d9) share 30 exact parallel flanking frames vs a 10,000-permutation frequency-matched null mean of 7.6427 (max 23, 0/10,000 controls >= 30, p = 0.0001 < 0.001, p3); masked-sign top-1 restoration with M77-CLSS achieves 20.05% (748/3,731) Mode 1 and 22.67% (846/3,731) Mode 2, beating KN3-Left (14.71%, p = 0.0001) and SIGIL (9.38%, p = 0.0001; 400 controls best_control = 0.096221) across pooled, Mohenjo-daro, and Harappa, while paired-bootstrap p-values against KN3-Bidir (p = 0.0001 pooled, 0.0019 Mohenjo-daro, 0.0147 Harappa in Mode 1) and KN3-BlanketF (p = 0.0048 pooled, 0.2988 Mohenjo-daro, 0.0188 Harappa in Mode 1) exceed the 3-variant KN3 p < 0.001 bar in how-we-built-it/PREREG.md.
