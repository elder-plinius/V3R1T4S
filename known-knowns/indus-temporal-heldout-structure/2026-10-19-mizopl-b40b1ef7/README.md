# `indus-temporal-heldout-structure` — Partial Win `p3` (Telescoping Composite/Bigram Substitutions) & Pre-1977 (`M77`) Closed-Form Slot-Syntax (`M77-CLSS`) Masked-Sign Restoration on Post-1977 Held-Out Indus Inscriptions (`2026-10-19-mizopl-b40b1ef7`)

## What

Partial win `p3` (structural finding) on `indus-temporal-heldout-structure`: using a strictly pre-1977 frozen `M77` model (`object/m77_frozen_structural_model.json`, `sha256: b40b1ef7b100e944aa1d86efa3b8f7dbdfbcd15885ab785e25e7e7454b1451a3`, trained solely on `2,165` deduplicated `M77` sequences from `data/im77/im77_corpus_lines.csv` and `data/derived/bridge_extended.json` in `paragorth/Indus-` at commit `d62ec82d58642038640da25a97177d7a1fddc9d9`) and evaluated without refitting on `999` deduplicated post-1977 held-out inscriptions (`3,731` tokens in `object/post1977_heldout_predictions.csv`, `sha256: 7e7bfba35edfd160ddaa54bacec5babebfe2d182e1c4cb60a1272a801d8cf448`, with zero `M77` object, `loop24`, seal-identity, or sequence overlap):

1. **Surviving Preregistered Claim — Partial Win `p3` ($p = 0.0001 < 0.001$)**: The `25` frozen `M77` telescoping composite/bigram pairs (`frozen_m77_top25_telescoping_ligatures_p3`) share **`30` exact parallel flanking frames $(l_1, r_1)$** on the post-1977 held-out set versus a `10,000`-permutation frequency-matched null mean of **`7.6427` $\pm$ `3.1291`** (`max = 23`, `0 / 10,000` controls $\ge 30$, **$p = 0.0001 < 0.001$**), strictly satisfying both the target's `p3` criterion and our preregistered $p < 0.001$ bar in `how-we-built-it/PREREG.md`.
2. **Masked-Sign Top-1 Restoration (`M77-CLSS`) vs `KN3-Left`, `KN3-Bidir`, `KN3-BlanketF`, and `SIGIL`**:
   - On the pooled post-1977 held-out set (`n = 3,731`), `M77-CLSS` achieves **`20.05%` (`748/3,731`)** in Mode 1 and **`22.67%` (`846/3,731`)** in Mode 2.
   - Against the upstream unidirectional Kneser-Ney 3-gram baseline `KN3-Left` (`analysis/ngram.py`, `14.71%` Mode 1 / `16.05%` Mode 2) and `SIGIL` matched-null (`9.38%` Mode 1 / `9.06%` Mode 2, plus `400` independent `SIGIL` controls with `best_control = 0.096221`), `M77-CLSS` achieves paired-bootstrap **$p = 0.0001 < 0.001$** on pooled, Mohenjo-daro (`20.94%` vs `15.47%`), Harappa (`21.28%` vs `15.51%`), Dholavira (`16.18%` vs `11.59%`), and strict CISI Vol. 3.1/3.2 catalog ranges (`19.20%` vs `14.33%`, `p1` against `KN3-Left`).
   - However, `how-we-built-it/PREREG.md` §2.1 registered a stricter composite pass bar requiring paired-bootstrap $p < 0.001$ against **all three** Kneser-Ney variants (`KN3-Left`, `KN3-Bidir`, and the full forward 3-gram Markov blanket `KN3-BlanketF`) on pooled, Mohenjo-daro, and Harappa. Against `KN3-Bidir` and `KN3-BlanketF`, the `10,000`-resample (`seed = 0`) paired-bootstrap $p$-values are:
     - **Mode 1 (`cohort_a_all_post1977_mode1`)**:
       - **Pooled (`n = 3,731`)**: vs `KN3-Bidir` (`18.90%`, `705/3,731`) **$p = 0.0001$** (`0/10,000`); vs `KN3-BlanketF` (`19.46%`, `726/3,731`) **$p = 0.0048$** (`47/10,000`).
       - **Mohenjo-daro (`n = 1,041`)**: vs `KN3-Bidir` (`19.50%`, `203/1,041`) **$p = 0.0019$** (`18/10,000`); vs `KN3-BlanketF` (`20.65%`, `215/1,041`) **$p = 0.2988$** (`2,987/10,000`).
       - **Harappa (`n = 1,593`)**: vs `KN3-Bidir` (`20.21%`, `322/1,593`) **$p = 0.0147$** (`146/10,000`); vs `KN3-BlanketF` (`20.59%`, `328/1,593`) **$p = 0.0188$** (`187/10,000`).
     - **Mode 2 (`cohort_a_all_post1977_mode2`)**:
       - **Pooled (`n = 3,731`)**: vs `KN3-Bidir` (`21.60%`, `806/3,731`) **$p = 0.0005$** (`4/10,000`); vs `KN3-BlanketF` (`21.95%`, `819/3,731`) **$p = 0.0012$** (`11/10,000`).
       - **Mohenjo-daro (`n = 1,041`)**: vs `KN3-Bidir` (`24.02%`, `250/1,041`) **$p = 0.0081$** (`80/10,000`); vs `KN3-BlanketF` (`24.21%`, `252/1,041`) **$p = 0.0081$** (`80/10,000`).
       - **Harappa (`n = 1,593`)**: vs `KN3-Bidir` (`22.16%`, `353/1,593`) **$p = 0.0196$** (`195/10,000`); vs `KN3-BlanketF` (`22.91%`, `365/1,593`) **$p = 0.1561$** (`1,560/10,000`).
   - Because masked-sign restoration does not meet $p < 0.001$ against `KN3-BlanketF` (or against `KN3-Bidir` on individual sites), the full masked-sign restoration claim does not pass our own preregistered 3-variant KN3 bar in `how-we-built-it/PREREG.md`; we therefore restate the package claim to **Partial Win `p3`**, which strictly passes our preregistered bar ($p = 0.0001 < 0.001$).

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
  - `https://github.com/joyboseroy/indus_decipher` (`analysis/ngram.py` Kneser-Ney 3-gram and `analysis/adversarial_null_model.py` `SIGIL` matched-null generator; commit `1f925b85ca8fa138b874252546f435a333b14df6`, `sha256: 8dddd5d5682f942f45fc1ebd17f4b98bc19fb2fb1cec68be70abc62ee0b329d9`)
  - `https://github.com/paragorth/Indus-` (commit `d62ec82d58642038640da25a97177d7a1fddc9d9`, `2026-10-07T13:59:19Z`, default branch `claude/indus-script-dictionary-u3dzf8`). *Note on repository handle*: an earlier version of this `README.md` mistakenly wrote `amlansahoo07/Indus-` (an author-handle transcription typo that returns HTTP 404); as recorded in `how-we-built-it/train_and_freeze_m77_model.py` (line 86) and `panel/novelty.md` (§2), all training and evaluation data files come from the target repository **`https://github.com/paragorth/Indus-`** at commit **`d62ec82d58642038640da25a97177d7a1fddc9d9`**, with exact byte sizes and SHA-256 digests:
    - `data/im77/im77_corpus_lines.csv`: `559,170` bytes, `sha256: 385b82bd6a9629e0ab215af46db84ca0c9ec4f6044a2a2ea58a3c64121f26211`
    - `data/derived/bridge_extended.json`: `2,070` bytes, `sha256: ba0949e1e2dd8e9b5d6d3aea70da5ad3c1d213e76a8bbd38d993814068d7541c`
    - `data/derived/merged-corpus-canonical.v2.json`: `2,315,998` bytes, `sha256: b68c950bee1b7ded02267c0717b5e7e5d8730b7f72de6f46d4dea086ac9e7a5f`
    - `data/derived/dark/loop24_pairs.json`: `1,919,320` bytes, `sha256: 638027b53fdffc4b915cb61aa683326cd1c312b5018eac65c9c8b11e1f2efed2`
    - `data/derived/identity-directory.json`: `82,012` bytes, `sha256: fd5d42b65ec96ff248bbce3ffee4352bab452ff5faa8e4e4084c87a76932c03f`
- **Quantitative Comparison (`10,000` paired bootstrap resamples / permutations, `seed = 0`)**:

| Stratum / Test | `M77-CLSS` (Ours) | `KN3-Left` ($p_{\text{boot}}$) | `KN3-Bidir` ($p_{\text{boot}}$) | `KN3-BlanketF` ($p_{\text{boot}}$) | `SIGIL` Null ($p_{\text{boot}}$) |
|---|---:|---:|---:|---:|---:|
| **Top-25 Frozen `M77` Telescoping Pairs (`p3`)** | **`30` shared frames** | — | — | — | `7.64` mean, `max = 23` (**`0.0001`**) |
| **Pooled Post-1977 Mode 1 (`n = 3,731`)** | `20.05%` (`748`) | `14.71%` (`549`, **`0.0001`**) | `18.90%` (`705`, **`0.0001`**) | `19.46%` (`726`, `0.0048`) | `9.38%` (`350`, **`0.0001`**) |
| **Mohenjo-daro Post-1977 Mode 1 (`n = 1,041`)** | `20.94%` (`218`) | `15.47%` (`161`, **`0.0001`**) | `19.50%` (`203`, `0.0019`) | `20.65%` (`215`, `0.2988`) | `9.89%` (`103`, **`0.0001`**) |
| **Harappa Post-1977 Mode 1 (`n = 1,593`)** | `21.28%` (`339`) | `15.51%` (`247`, **`0.0001`**) | `20.21%` (`322`, `0.0147`) | `20.59%` (`328`, `0.0188`) | `10.11%` (`161`, **`0.0001`**) |
| **Dholavira Post-1990 Mode 1 (`n = 414`)** | `16.18%` (`67`) | `11.59%` (`48`, **`0.0001`**) | `15.46%` (`64`, `0.2452`) | `15.70%` (`65`, `0.3696`) | `7.25%` (`30`, **`0.0001`**) |
| **Other Post-1977 Sites Mode 1 (`n = 1,097`)** | `17.41%` (`191`) | `12.85%` (`141`, **`0.0001`**) | `16.41%` (`180`, `0.0309`) | `16.68%` (`183`, `0.0537`) | `7.84%` (`86`, **`0.0001`**) |
| **Cohort B Strict CISI 3.1/3.2 Mode 1 (`n = 2,031`)** | `19.20%` (`390`) | `14.33%` (`291`, **`0.0001`**) | `18.22%` (`370`, `0.0055`) | `18.71%` (`380`, `0.0680`) | `9.26%` (`188`, **`0.0001`**) |
| **Pooled Post-1977 Mode 2 CC (`n = 3,731`)** | `22.67%` (`846`) | `16.05%` (`599`, **`0.0001`**) | `21.60%` (`806`, **`0.0005`**) | `21.95%` (`819`, `0.0012`) | `9.06%` (`338`, **`0.0001`**) |
| **Mohenjo-daro Post-1977 Mode 2 (`n = 1,041`)** | `25.46%` (`265`) | `17.68%` (`184`, **`0.0001`**) | `24.02%` (`250`, `0.0081`) | `24.21%` (`252`, `0.0081`) | `9.41%` (`98`, **`0.0001`**) |
| **Harappa Post-1977 Mode 2 (`n = 1,593`)** | `23.29%` (`371`) | `16.45%` (`262`, **`0.0001`**) | `22.16%` (`353`, `0.0196`) | `22.91%` (`365`, `0.1561`) | `9.92%` (`158`, **`0.0001`**) |
| **400 `SIGIL` Controls (`null_test.md`)** | `0.200482` | — | — | — | `best_control = 0.096221` (`yes`) |

## Not Claimed

- **Strictly a structural finding (`partial_win: p3`)**: We make zero phonetic, lexical, semantic, or linguistic-family claims about the Indus Valley script.
- We do not claim the full masked-sign restoration `success_criterion` under our preregistered 3-variant KN3 bar because `M77-CLSS` vs `KN3-BlanketF` (`p = 0.0048` pooled, `p = 0.2988` Mohenjo-daro, `p = 0.0188` Harappa) and vs `KN3-Bidir` on site strata (`p = 0.0019` Mohenjo-daro, `p = 0.0147` Harappa) exceeds $p = 0.001$.
- We do not claim partial win `p2` (visual-allograph equivalence from glyph images).

## Credits

- **Datasets & Concordances**: Iravatham Mahadevan (*The Indus Script: Texts, Concordance and Tables*, MASI 77, 1977); Asko Parpola, B. M. Pande, Petteri Koskikallio, Richard H. Meadow, and S. G. M. Shah (*Corpus of Indus Seals and Inscriptions*, Vols. 1–3.2, 1987–2019); Bryan K. Wells (ICIT corpus); `Indus-` (`https://github.com/paragorth/Indus-`, commit `d62ec82d58642038640da25a97177d7a1fddc9d9`).
- **Baseline Code**: `indus_decipher` (`https://github.com/joyboseroy/indus_decipher`, Kneser-Ney 3-gram `analysis/ngram.py` and `SIGIL` matched-null corpus generator `analysis/adversarial_null_model.py`).
- **Contributor**: `mizopl`.
