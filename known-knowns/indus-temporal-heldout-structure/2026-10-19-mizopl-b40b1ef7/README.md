# `indus-temporal-heldout-structure` — Pre-1977 (`M77`) Closed-Form Slot-Syntax (`M77-CLSS`) Masked-Sign Restoration & Telescoping Composite Substitution on Post-1977 Held-Out Indus Inscriptions (`2026-10-19-mizopl-b40b1ef7`)

## What

Structural finding on indus-temporal-heldout-structure: a strictly pre-1977 frozen M77 Closed-Form Slot-Syntax model (claim/m77_frozen_structural_model.json, sha256 b40b1ef7b100e944aa1d86efa3b8f7dbdfbcd15885ab785e25e7e7454b1451a3, trained solely on 2,165 deduplicated M77 sequences from claim/im77_corpus_lines.csv and claim/bridge_extended.json) evaluated without refitting on 999 deduplicated post-1977 held-out inscriptions (3,731 tokens in claim/post1977_heldout_predictions.csv, sha256 7e7bfba35edfd160ddaa54bacec5babebfe2d182e1c4cb60a1272a801d8cf448, with zero M77 object, loop24, seal-identity, or sequence overlap) achieves masked-sign top-1 restoration accuracy of 20.05% (748/3,731) Mode 1 and 22.67% (846/3,731) Mode 2 vs M77 Kneser-Ney 3-gram 14.71% (p = 0.0001 < 0.001), bidirectional KN3 18.90% (p = 0.0001 < 0.001), SIGIL matched-null 9.38% (p = 0.0001 < 0.001), and 400 independent SIGIL controls (best_control = 0.096221), holding separately on post-1977 Mohenjo-daro (20.94% vs 15.47%, p = 0.0001), Harappa (21.28% vs 15.51%, p = 0.0001), Dholavira (16.18% vs 11.59%, p = 0.0001), and strict CISI Vol. 3.1/3.2 catalog ranges (19.20% vs 14.33%, p = 0.0001, p1), together with 30 shared post-1977 parallel frames across 25 frozen M77 telescoping composite/bigram pairs vs random frequency-matched permutation mean 7.64 (max 23, p = 0.0001 < 0.001, p3).

## Check It Yourself

From this package directory, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Expected last line**: `PASS`
- **Rough laptop time**: `~3` seconds on CPU (`python3` + `numpy`).

## Compared To

- **Target ID**: `indus-temporal-heldout-structure` (`category: undeciphered-scripts`)
- **Primary Baseline Repositories**:
  - `https://github.com/joyboseroy/indus_decipher` (`analysis/ngram.py` Kneser-Ney 3-gram and `analysis/adversarial_null_model.py` `SIGIL` matched-null generator; latest commit `1f925b85ca8fa138b874252546f435a333b14df6` fetched `2026-10-19T20:27:50Z`, `sha256: 8dddd5d5682f942f45fc1ebd17f4b98bc19fb2fb1cec68be70abc62ee0b329d9`)
  - `https://github.com/amlansahoo07/Indus-` (`data/im77/im77_corpus_lines.csv`, `data/derived/bridge_extended.json`, `data/derived/merged-corpus-canonical.v2.json`, `data/derived/dark/loop24_pairs.json`, `data/derived/identity-directory.json`, and frozen preregistrations `P1-P9`, `Q1-Q14`, `R1-R13`)
- **Quantitative Comparison (`10,000` paired bootstrap resamples, `seed = 0`)**:

| Stratum / Test | `M77-CLSS` (Ours) | `KN3-Left` (`ngram.py`) | `KN3-Bidir` | `SIGIL` Matched Null | $p$ vs `KN3-Left` / `SIGIL` |
|---|---:|---:|---:|---:|---:|
| **Pooled Post-1977 Mode 1 (`n = 3,731`)** | **`20.05%` (`748`)** | `14.71%` (`549`) | `18.90%` (`705`) | `9.38%` (`350`) | **`0.000100` / `0.000100`** |
| **Mohenjo-daro Post-1977 (`n = 1,041`)** | **`20.94%` (`218`)** | `15.47%` (`161`) | `19.50%` (`203`) | `9.89%` (`103`) | **`0.000100` / `0.000100`** |
| **Harappa Post-1977 (`n = 1,593`)** | **`21.28%` (`339`)** | `15.51%` (`247`) | `20.21%` (`322`) | `10.11%` (`161`) | **`0.000100` / `0.000100`** |
| **Dholavira Post-1990 (`n = 414`)** | **`16.18%` (`67`)** | `11.59%` (`48`) | `15.46%` (`64`) | `7.25%` (`30`) | **`0.000100` / `0.000100`** |
| **Other Post-1977 Sites (`n = 1,097`)** | **`17.41%` (`191`)** | `12.85%` (`141`) | `16.41%` (`180`) | `7.84%` (`86`) | **`0.000100` / `0.000100`** |
| **Cohort B Strict CISI 3.1/3.2 (`n = 2,031`, `p1`)** | **`19.20%` (`390`)** | `14.33%` (`291`) | `18.22%` (`370`) | `9.26%` (`188`) | **`0.000100` / `0.000100`** |
| **Pooled Post-1977 Mode 2 CC (`n = 3,731`)** | **`22.67%` (`846`)** | `16.05%` (`599`) | `21.60%` (`806`) | `9.06%` (`338`) | **`0.000100` / `0.000100`** |
| **Top-25 Frozen `M77` Telescoping Pairs (`p3`)** | **`30` shared frames** | — | — | `7.64` null mean (`max = 23`) | **`0.000100`** (`0/10,000`) |
| **400 `SIGIL` Controls (`null_test.md`)** | **`0.200482`** | — | — | `best_control = 0.096221` | **`real_beats_all_controls: yes`** |

## Not Claimed

- **Strictly a structural finding**: We make zero phonetic, lexical, semantic, or linguistic-family claims about the Indus Valley script.
- We do not claim partial win `p2` (visual-allograph equivalence from glyph images).

## Credits

- **Datasets & Concordances**: Iravatham Mahadevan (*The Indus Script: Texts, Concordance and Tables*, MASI 77, 1977); Asko Parpola, B. M. Pande, Petteri Koskikallio, Richard H. Meadow, and S. G. M. Shah (*Corpus of Indus Seals and Inscriptions*, Vols. 1–3.2, 1987–2019); Bryan K. Wells (ICIT corpus); `Indus-` (`https://github.com/amlansahoo07/Indus-`).
- **Baseline Code**: `indus_decipher` (`https://github.com/joyboseroy/indus_decipher`, Kneser-Ney 3-gram `analysis/ngram.py` and `SIGIL` matched-null corpus generator `analysis/adversarial_null_model.py`).
- **Contributor**: `mizopl`.
