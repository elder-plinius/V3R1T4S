# How We Found It (`contributor text, unverified`)

*Note: contributor text, unverified.*

## 1. The Brief

Target `indus-temporal-heldout-structure` asks whether a structural sign-syntax model (functional sign-equivalence classes, slot grammar, and positional dependency rules) trained strictly on Iravatham Mahadevan's 1977 concordance (`M77`, inscriptions known up to 1977 in `data/im77/im77_corpus_lines.csv` from `https://github.com/paragorth/Indus-`) generalizes without refitting to a clean held-out set of Indus inscriptions excavated or published strictly after 1977 (such as Dholavira, post-1977 Harappa HARP excavations, and CISI Vols. 2–3.2), and whether composite signs listed in `M77` / Wells behave distributionally as their constituent two-sign bigrams in parallel contexts on the post-1977 held-out set (`p3`, permutation $p \le 0.001$).

## 2. What Failed or Needed Care

1. **Unidirectional left-context Kneser-Ney (`KN3-Left`) vs Bidirectional / Full-Blanket Kneser-Ney (`KN3-Bidir`, `KN3-BlanketF`)**: The reference `ngram.py` implementation conditions only on the two preceding tokens $(l_2, l_1)$. On short inscriptions (median length 4–5 signs), masking an interior or initial sign leaves half of the local Markov blanket unused (`29.15%` in `M77` 5-fold CV and `14.71%` on the post-1977 held-out set). When we also constructed bidirectional (`KN3-Bidir`, `18.90%`) and full forward Markov-blanket (`KN3-BlanketF`, `19.46%`) 3-gram baselines and required in `how-we-built-it/PREREG.md` that `M77-CLSS` beat all three KN3 variants at $p < 0.001$ across pooled, Mohenjo-daro, and Harappa, `M77-CLSS` (`20.05%`) beat `KN3-Left` and `SIGIL` at $p = 0.0001$ everywhere and `KN3-Bidir` on pooled ($p = 0.0001$), but its gains over `KN3-BlanketF` ($p = 0.0048$ pooled, $p = 0.2988$ Mohenjo-daro, $p = 0.0188$ Harappa) and over `KN3-Bidir` on individual sites ($p = 0.0019$ Mohenjo-daro, $p = 0.0147$ Harappa) did not pass our own $p < 0.001$ bar.
2. **Sign-code bridge alignment**: `im77_corpus_lines.csv` uses Mahadevan (`M`) sign numbers (`1..417`), whereas `merged-corpus-canonical.v2.json` uses Wells/ICIT (`W`) sign numbers. Furthermore, `merged-corpus-canonical.v2.json` stores sequences in canonical right-to-left reading order (`index 0` = right-hand initial sign, `index -1` = left-hand terminal sign, verified by the terminal jar sign `W740` appearing at `index -1` in `223 / 231 = 96.54%` of boundary occurrences). We evaluated both the exact `test_prereg.py` `m2g` mapping (Mode 1) and the connected-component equivalence bridge from `bridge_extended.json` (Mode 2).
3. **Whitespace hygiene in `loop24_pairs.json`**: When checking object-ID disjointness between `merged-corpus-canonical.v2.json` and `loop24_pairs.json`, our standalone checker caught a single entry (`'cisi': 'L-78 '`) in `loop24_pairs.json` with a trailing space; stripping whitespace on `loop24_pairs.json` CISI strings eliminated `L-78` cleanly (`999` strictly disjoint held-out inscriptions, `3,731` tokens).

## 3. What Worked (`p3` Telescoping Composite/Bigram Substitutions & `M77-CLSS`)

Using 5-fold cross-validation strictly on the `2,165` unique `M77` sequences (`9,652` tokens), we combined the full forward 3-gram Markov blanket (`KN3-BlanketF`) with:
- A 5-zone positional slot-grammar log-likelihood ratio (`Initial`, `Post-Initial`, `Medial`, `Pre-Terminal`, `Terminal`),
- `32` Ward hierarchical distributional sign-equivalence class transitions (`C0..C31`, `n_distributional_clusters = 32` in `object/m77_frozen_structural_model.json`; an earlier `K = 48` SVD prototype was superseded before freezing),
- Slot-conditioned boundary bigrams,
- Center-bypass skip-bigram $(l_1, r_1) \to w$ residuals, and
- An `M77`-derived anti-gemination constraint for non-numeral signs.

Frozen in `object/m77_frozen_structural_model.json` before touching the post-1977 evaluation script, the `25` frozen `M77` telescoping composite/bigram pairs (`frozen_m77_top25_telescoping_ligatures_p3`) shared **`30` exact parallel flanking frames** in the post-1977 held-out corpus vs a `10,000`-permutation frequency-matched random mean of **`7.6427`** (`max = 23`, `0 / 10,000` controls $\ge 30$, **$p = 0.000100 < 0.001$**), cleanly passing our preregistered bar for **Partial Win `p3`**.
