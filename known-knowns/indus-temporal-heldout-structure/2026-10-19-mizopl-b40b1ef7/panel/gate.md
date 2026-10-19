# Skeptic Panel Gate (`indus-temporal-heldout-structure`)

status: CONFIRMED_SOLUTION
target: indus-temporal-heldout-structure
reproduce_pass: true
novelty_pass: true
criterion_pass: true
confirmed_scope: Structural finding on indus-temporal-heldout-structure: a strictly pre-1977 frozen M77 Closed-Form Slot-Syntax model (claim/m77_frozen_structural_model.json, sha256 b40b1ef7b100e944aa1d86efa3b8f7dbdfbcd15885ab785e25e7e7454b1451a3, trained solely on 2,165 deduplicated M77 sequences from claim/im77_corpus_lines.csv and claim/bridge_extended.json) evaluated without refitting on 999 deduplicated post-1977 held-out inscriptions (3,731 tokens in claim/post1977_heldout_predictions.csv, sha256 7e7bfba35edfd160ddaa54bacec5babebfe2d182e1c4cb60a1272a801d8cf448, with zero M77 object, loop24, seal-identity, or sequence overlap) achieves masked-sign top-1 restoration accuracy of 20.05% (748/3,731) Mode 1 and 22.67% (846/3,731) Mode 2 vs M77 Kneser-Ney 3-gram 14.71% (p = 0.0001 < 0.001), bidirectional KN3 18.90% (p = 0.0001 < 0.001), SIGIL matched-null 9.38% (p = 0.0001 < 0.001), and 400 independent SIGIL controls (best_control = 0.096221), holding separately on post-1977 Mohenjo-daro (20.94% vs 15.47%, p = 0.0001), Harappa (21.28% vs 15.51%, p = 0.0001), Dholavira (16.18% vs 11.59%, p = 0.0001), and strict CISI Vol. 3.1/3.2 catalog ranges (19.20% vs 14.33%, p = 0.0001, p1), together with 30 shared post-1977 parallel frames across 25 frozen M77 telescoping composite/bigram pairs vs random frequency-matched permutation mean 7.64 (max 23, p = 0.0001 < 0.001, p3).
