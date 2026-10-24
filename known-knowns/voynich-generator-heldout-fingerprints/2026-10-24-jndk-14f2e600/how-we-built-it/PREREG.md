# Pre-Registration (`PREREG.md`) — `voynich-generator-heldout-fingerprints`

- timestamp_utc: `2026-10-23T18:26:52Z`
- session_id: `gemini-6fa1ad`
- target: `voynich-generator-heldout-fingerprints`
- null_test: required (statistical / cipher-generator target; 400-control null suite pre-registered below)

---

## 1. Verbatim Bank Criterion & Partial Wins

### Success Criterion
Either (A) exhibit a hand-executable text generator (table size at most 200 entries plus a written procedure, state at most 1 per-folio bit) whose output, when driven by period Latin and Italian plaintexts across at least 10 random seeds and at least 8 plaintexts from at least 2 languages, simultaneously lies within the empirical Voynich 95% bootstrap envelope on BOTH the Zandbergen-Landini (ZL3b-n) and Takahashi (IT2a-n) EVA transliterations and on Currier A and Currier B separately for ALL of: (i) cross-boundary last-glyph to next-first-glyph mutual information and its share of marginal entropy (arXiv 2608.17096), (ii) corpus singleton-type (hapax) rate (arXiv 2608.17096), (iii) the four Currier line/boundary signatures of arXiv 2604.19762 (E->S rate, bilateral extremity, cross-boundary MI, word-initial frequency distribution shape), (iv) the per-folio ch/sh-vowel switch bimodality and state separation of arXiv 2604.25979, and (v) within-word conditional character entropy h2 and word-length distribution; OR (B) exhibit a NEW corpus-level statistic (not already published in arXiv 2608.17096, 2604.19762, or 2604.25979 — in particular not cross-boundary edge MI, singleton/hapax rate, the four Currier boundary signatures, or the per-folio ch/sh-vowel switch) on which every one of 200 ciphertext streams produced by the unmodified published Naibbe reference implementation (github.com/mjgreshko/naibbe-cipher, default parameters, across 20 period Latin and Italian plaintexts x 10 seeds) falls outside the 99.9% Voynich bootstrap envelope on both ZL3b-n and IT2a-n and both Currier dialects, AND survives 400 glyph-shuffled and word-order-shuffled null controls.

### Partial Wins
- **`p1`**: A hand-executable generator (at most 200 table entries plus a written procedure, at most 1 per-folio state bit) that brings edge-glyph coupling mutual information and entropy share AND singleton-type rate into the Voynich envelope on both transliterations and both Currier dialects, across at least 80% of 10 seeds x 8 plaintexts from >=2 period languages, while preserving within-word h2 and word-length distribution within the Voynich envelope.
- **`p2`**: A hand-executable generator (at most 200 table entries plus a written procedure, at most 1 per-folio state bit) that passes all four signatures of arXiv 2604.19762 jointly, per Currier dialect and on both transliterations, which the published slot and Cardan-grille generators fail.
- **`p3`**: A 1-bit per-folio state modification to the published Naibbe table procedure (at most 200 total entries) that reproduces the per-folio ch/sh-vowel switch bimodality and state separation of arXiv 2604.25979 on both transliterations without degrading the statistics Naibbe already matches.

---

## 2. Pre-Registered Primary Attack: Partial Win `p2` (and Coupled `p1` Evaluation)

### 2.1 Scorer for `p2` (`arXiv:2604.19762` Four Signatures)
We use the official `arXiv:2604.19762` implementation (`data/currier-signatures/signatures_v27.py` and `data/currier-signatures/verifier.py` by Parisel 2026) with zero modifications to its metric computation (`compute_metrics` and `evaluate_signatures`):
1. **Tokenization**: Greedy longest-match over the 57-grapheme inventory (`ALL_GRAPHEMES = PREFIX_GRAPHEMES | SUFFIX_GRAPHEMES | {'o', 'a'}`).
2. **Signature 1 (`E->S` rate)**: Percentage of consecutive within-line word pairs $(w_i, w_{i+1})$ where $\text{cls}(\text{last}(w_i)) = \text{"end"}$ ($e(g) > 2s(g)$) and $\text{cls}(\text{first}(w_{i+1})) = \text{"start"}$ ($s(g) > 2e(g)$).
   - **Adaptive threshold (`signatures_v27.py`)**: $\text{E}\to\text{S} \in [\max(\text{ref\_es}-15, 50), \min(\text{ref\_es}+15, 98)]\%$.
   - **Fixed verifier threshold (`verifier.py`)**: $\text{E}\to\text{S} \in [60.0, 85.0]\%$.
3. **Signature 2 (`Bilateral extremity`)**: $n_{se} = |\{g : (s(g)+1)/(e(g)+1) > 100\}| > 0$ AND $n_{ee} = |\{g : (e(g)+1)/(s(g)+1) > 100\}| > 0$ on the full dialect corpus, plus chunk bilateral fraction $\ge 0.5$ (`signatures_v27.py`).
4. **Signature 3 (`MI` — Cross-Boundary Mutual Information)**: Mean across 10 equal chunks of the plug-in mutual information $I(\text{last}(w_i); \text{first}(w_{i+1}))$ in bits.
   - **Adaptive threshold (`signatures_v27.py`)**: $\text{MI} \in [\max(0.10, 0.5 \times \text{ref\_mi}), 2.0 \times \text{ref\_mi}]$ bits.
   - **Fixed verifier threshold (`verifier.py`)**: $\text{MI} \in [0.20, 0.65]$ bits.
5. **Signature 4 (`Shape` — Word-Initial Frequency Distribution)**: Log-log OLS $R^2$ and coefficient of variation $\text{CV} = \sigma/\mu$ of word-initial grapheme frequencies.
   - **Strict threshold (`verifier.py` & `signatures_v27.py` `pass_zipf`)**: `Shape == "Zipfian"` ($R^2 > 0.85$ and $\text{CV} > 0.8$). (Note: `pass_4` in `signatures_v27.py` only requires `Shape != "Plateau"`, i.e. $\text{CV} \ge 0.5$; we require the stricter `Shape == "Zipfian"` so both `pass_4` and `pass_zipf` and `verifier.py` pass simultaneously.)

### 2.2 Pre-Registered Acceptance Rule for `p2`
A candidate generator qualifies for `p2` if and only if:
1. **Hand-Executability & Table Budget**: Its lookup tables contain at most **200 total entries** across all tables combined, accompanied by an explicit written step-by-step procedure executable by hand and using at most **1 per-folio state bit**.
2. **Dialect & Transliteration Coverage**: Evaluated on Currier A and Currier B separately across BOTH `ZL3b-n.txt` and `IT2a-n.txt` (4 cells: `A/ZL3b`, `B/ZL3b`, `A/IT2a`, `B/IT2a`, plus `A/RF1b-e` and `B/RF1b-e` for completeness), across the 20 period plaintexts (10 Latin `Latin-00..09`, 10 Italian `Italian-00..09`) $\times$ 10 seeds (`seeds 0..9` = 200 plaintext-driven streams per cell), wrapped to the dialect's line/folio structure (and also checked at the 37,000-word synthetic length of `signatures_v27.py`), the generator passes **all 4 signatures jointly** (`4/4` on BOTH the adaptive `evaluate_signatures` criteria AND the strict `verifier.py` Zipfian criteria) on $\ge 80\%$ of streams (and we aim for $100\%$ of streams) in every one of the 4 cells (`A/ZL3b`, `B/ZL3b`, `A/IT2a`, `B/IT2a`).
3. **Failure of Published Slot, Cardan-Grille, and Naibbe Generators**: We verify on the exact same scorer that the published slot generator (`signatures_v27.py` baseline `S1`), the published Cardan-grille generator (`grille.py`), and unmodified Naibbe (`naibbe.py`) all fail to pass all 4 signatures jointly across the 4 cells.

### 2.3 Pre-Registered Evaluation for `p1` (`arXiv:2608.17096` Statistics)
We also score our hand-executable generator on the five `p1` metrics across the 4 cells (`A/ZL3b`, `B/ZL3b`, `A/IT2a`, `B/IT2a`) over the 20 plaintexts $\times$ 10 seeds:
1. Shuffle-corrected cross-boundary excess edge MI: $I_{\text{excess}}(L_i; F_{i+1}) = I_{\text{obs}}(L_i; F_{i+1}) - \mathbb{E}_{\pi}[I(L_{\pi(i)}; F_{\pi(i)+1})]$ (in bits),
2. Edge-coupling share of marginal entropy: $I_{\text{excess}}(L_i; F_{i+1}) / H(F_{i+1})$,
3. Corpus singleton-type (hapax) rate: $V_1 / V$,
4. Within-word conditional character entropy $h_2 = H(c_k | c_{k-1})$,
5. Word-length distribution (mean word length $\bar{\ell}$ and standard deviation $\sigma_\ell$ in EVA characters / graphemes),
against the 95% page-bootstrap envelope of the corresponding Voynich dialect and transliteration cell (2,000 page-level bootstrap resamples).

---

## 3. Pre-Registered 400-Control Null Test (`null_test.md`)

To ensure our results are not artifacts of marginal token frequencies, corpus length, or line-wrapping geometry, we pre-register a **400-control null suite** for each dialect $\times$ transliteration cell (`A/ZL3b`, `B/ZL3b`, `A/IT2a`, `B/IT2a`):
- **Control Family 1 (200 Word-Order Permutations, seeds `1000..1199`)**: Randomly permute the order of word tokens across the corpus while keeping line lengths (tokens per line) and the exact word multiset fixed. This preserves single-word statistics (singleton rate $V_1/V$, within-word $h_2$, word-length distribution, Signature 2 bilateral extremity, Signature 4 word-initial Zipfian shape) while destroying sequential word-to-word coupling.
- **Control Family 2 (200 Position-Preserving Glyph Shuffles, seeds `2000..2199`)**: Randomly permute the grapheme/glyph sequence across word tokens of identical length while preserving line lengths and overall character frequencies.
- **Null Test Pass Criterion**:
  1. The real Voynich manuscript corpus in each cell (`A/ZL3b`, `B/ZL3b`, `A/IT2a`, `B/IT2a`) must beat **all 200 word-order-shuffled controls** and **all 200 glyph-shuffled controls** (400/400 controls) on cross-boundary coupling (`arXiv:2604.19762` Signature 3 MI and `arXiv:2608.17096` excess edge MI).
  2. Our hand-executable boundary-coupled generator must likewise beat **all 400 null controls** constructed from its own output streams on cross-boundary coupling, AND all 400 null controls must fail the joint 4-signature criterion of `arXiv:2604.19762` (`0/400` controls passing all 4 signatures jointly).
