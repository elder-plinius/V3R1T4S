# How We Found It (`contributor text, unverified`)

*Note: contributor text, unverified.*

## 1. The Brief

Target `indus-temporal-heldout-structure` asks whether a structural sign-syntax model (functional sign-equivalence classes, slot grammar, and positional dependency rules) trained strictly on Iravatham Mahadevan's 1977 concordance (`M77`, inscriptions known up to 1977 in `im77_corpus_lines.csv`) generalizes without refitting to a clean held-out set of Indus inscriptions excavated or published strictly after 1977 (such as Dholavira, post-1977 Harappa HARP excavations, and CISI Vols. 2–3.2), beating both an `M77`-trained Kneser-Ney 3-gram baseline (`ngram.py`) and the `SIGIL` matched-null baseline (`adversarial_null_model.py`) at $p < 0.001$ (`10,000` paired bootstrap resamples, `seed = 0`) on the pooled set and separately on Mohenjo-daro and Harappa post-1977 finds.

## 2. What Failed or Needed Care

1. **Unidirectional left-context Kneser-Ney (`KN3-Left`)**: The reference `ngram.py` implementation conditions only on the two preceding tokens $(l_2, l_1)$. On short inscriptions (median length 4–5 signs), masking an interior or initial sign leaves half of the local Markov blanket unused (`29.15%` in `M77` 5-fold CV and `14.71%` on the post-1977 held-out set).
2. **Sign-code bridge alignment**: `im77_corpus_lines.csv` uses Mahadevan (`M`) sign numbers (`1..417`), whereas `merged-corpus-canonical.v2.json` uses Wells/ICIT (`W`) sign numbers. Furthermore, `merged-corpus-canonical.v2.json` stores sequences in canonical right-to-left reading order (`index 0` = right-hand initial sign, `index -1` = left-hand terminal sign, verified by the terminal jar sign `W740` appearing at `index -1` in `223 / 231 = 96.54%` of boundary occurrences). We evaluated both the exact `test_prereg.py` `m2g` mapping (Mode 1) and the connected-component equivalence bridge from `bridge_extended.json` (Mode 2).
3. **Whitespace hygiene in `loop24_pairs.json`**: When checking object-ID disjointness between `merged-corpus-canonical.v2.json` and `loop24_pairs.json`, our standalone checker caught a single entry (`'cisi': 'L-78 '`) in `loop24_pairs.json` with a trailing space; stripping whitespace on `loop24_pairs.json` CISI strings eliminated `L-78` cleanly (`999` strictly disjoint held-out inscriptions, `3,731` tokens).

## 3. What Worked (`M77-CLSS`)

Using 5-fold cross-validation strictly on the `2,165` unique `M77` sequences (`9,652` tokens), we combined the full forward 3-gram Markov blanket (`KN3-BlanketF`) with:
- A 5-zone positional slot-grammar log-likelihood ratio (`Initial`, `Post-Initial`, `Medial`, `Pre-Terminal`, `Terminal`),
- `K = 48` SVD distributional sign-equivalence class transitions,
- Slot-conditioned boundary bigrams,
- Center-bypass skip-bigram $(l_1, r_1) \to w$ residuals, and
- An `M77`-derived anti-gemination constraint for non-numeral signs.

Frozen in `m77_frozen_structural_model.json` before touching the post-1977 evaluation script, `M77-CLSS` improved masked-sign top-1 restoration on the `3,731` post-1977 tokens from `14.71%` (`KN3-Left`) and `9.38%` (`SIGIL`) to **`20.05%` Mode 1 / `22.67%` Mode 2** ($p = 0.000100 < 0.001$ pooled, on Mohenjo-daro, on Harappa, and on Dholavira), while the `25` frozen `M77` telescoping composite/bigram pairs shared **`30` exact parallel frames** in the post-1977 corpus vs a frequency-matched random permutation mean of **`7.64`** (`max = 23`, $p = 0.000100 < 0.001$, `p3`).
