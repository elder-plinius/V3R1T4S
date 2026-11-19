# Independent REPRODUCE Skeptic Verification Report

context: subagent
target_id: voynich-generator-heldout-fingerprints
skeptic_role: reproduce

## 1. Quoted Target Criterion & Partial Win `p2` Definition

From `claim/CLAIM.md` (verbatim from target specification):

> - **Success criterion (hand-executability & corpus scope)**:
>   "It must be hand-executable: at most 200 table entries plus a written procedure, and at most 1 per-folio state bit beyond the tables. Run it on at least 20 plaintexts from at least 2 period languages x 10 seeds."
> - **Enumerated partial win `p2`**:
>   "`p2`: A hand-executable generator (same limits) that passes all four signatures of arXiv 2604.19762 jointly, per Currier dialect and on both transliterations, which the published slot and Cardan-grille generators fail."

Before reading `claim/verify_p2_claim.py`, an independent checker script was written directly from the mathematical definitions of the four structural signatures in `claim/data/verifier.py` and `claim/data/signatures_v27.py` (`arXiv:2604.19762`) and executed on the `veritas` cluster (`job 2903`, `sci-torch`, exit code `0`, runtime `60s`).

---

## 2. Audit of Hand-Executability Constraints (`claim/vbclc.py` & `claim/HAND_PROCEDURE.md`)

1. **Table Entry Count ($\le 200$)**:
   - `LETTER_MAP_16` (Table 0 in `claim/vbclc.py`): **16** base-16 plaintext letter-group entries (or **26** raw ASCII letter keys if counted ungrouped).
   - `ONSET_TABLE_20` (Table I in `claim/vbclc.py`): **20** prefix entries ($4 \text{ macro-classes} \times 5 \text{ sub-ranks}$).
   - `CORE_TABLE_96` (Table II in `claim/vbclc.py`): **96** medial slot-rigid core entries ($4 \text{ harmonic groups} \times 24 \text{ entries}$).
   - `CODA_TABLE_20` (Table III in `claim/vbclc.py`): **20** suffix entries ($4 \text{ outgoing macro-classes} \times 5 \text{ sub-ranks}$).
   - **Total Table Entries**: $16 + 20 + 96 + 20 = \mathbf{152 \le 200}$ (even if counting all 26 raw alphabet keys in `LETTER_MAP_16` individually, $26 + 20 + 96 + 20 = 162 \le 200$).
2. **Per-Folio State Bit ($\le 1\text{ bit}$)**:
   - `encrypt_vbclc_lines(plaintext, template_lines, sigma_f, seed)` in `claim/vbclc.py` enforces `assert sigma_f in (0, 1)` (`sigma_f = 1` for Currier A, `sigma_f = 0` for Currier B). Passing `sigma_f` outside `{0, 1}` (`-1, 2, 3`) raises `AssertionError`.
3. **Written Hand Procedure**:
   - `claim/HAND_PROCEDURE.md` (`7,307` bytes) provides the complete 152-entry lookup sheet (Tables 0, I, II, III) and step-by-step human scribe instructions (Folio Setup, Read Plaintext Tetrad, Step A Onset Selection, Step B Core Selection, Step C Coda Selection, Step D Non-Merging Boundary Join & Advance).
4. **Determinism**:
   - Encrypting `claim/data/plaintexts/Latin-00.txt` twice with `seed=42` for both `sigma_f=0` and `sigma_f=1` produced bit-for-bit, word-for-word identical line arrays; changing to `seed=43` produced distinct output.

---

## 3. Verification of Saved 200-Stream Evaluation (`claim/vbclc_200streams_evaluation.json`)

All six dialect/transliteration cells (`A/ZL3b`, `B/ZL3b`, `A/IT2a`, `B/IT2a`, `A/RF1b-e`, `B/RF1b-e`) were checked across 200 streams per cell (10 period Latin plaintexts `claim/data/plaintexts/Latin-00..09.txt` + 10 period Italian plaintexts `claim/data/plaintexts/Italian-00..09.txt` $\times 10$ seeds = 200 streams/cell, 1,200 streams total):

| Cell | Streams | Latin Pass | Italian Pass | Joint Pass (All Criteria) | `E->S` Mean $\pm$ SD (Min–Max) | 10-Chunk `MI` Mean $\pm$ SD (Min–Max) | `Zipf R²` Mean (Min) | `CV` Mean (Min) | `Bilat_full` | `Shape` |
|---|---:|---:|---:|---:|---|---|---|---|---:|---|
| `A/ZL3b` | 200 | 100/100 | 100/100 | **200/200 (100%)** | $68.04\% \pm 1.25\%$ ($65.95\text{–}73.66\%$) | $0.4631 \pm 0.0099$ ($0.4267\text{–}0.4912$) | $0.922$ ($0.884$) | $1.25$ ($1.21$) | 100% | `Zipfian` (200/200) |
| `B/ZL3b` | 200 | 100/100 | 100/100 | **200/200 (100%)** | $67.30\% \pm 1.05\%$ ($65.86\text{–}71.72\%$) | $0.4312 \pm 0.0070$ ($0.4170\text{–}0.4543$) | $0.937$ ($0.920$) | $1.24$ ($1.21$) | 100% | `Zipfian` (200/200) |
| `A/IT2a` | 200 | 100/100 | 100/100 | **200/200 (100%)** | $68.09\% \pm 1.44\%$ ($65.54\text{–}72.94\%$) | $0.4635 \pm 0.0092$ ($0.4369\text{–}0.4909$) | $0.923$ ($0.896$) | $1.25$ ($1.21$) | 100% | `Zipfian` (200/200) |
| `B/IT2a` | 200 | 100/100 | 100/100 | **200/200 (100%)** | $67.27\% \pm 1.10\%$ ($65.66\text{–}72.01\%$) | $0.4307 \pm 0.0071$ ($0.4145\text{–}0.4491$) | $0.937$ ($0.923$) | $1.24$ ($1.22$) | 100% | `Zipfian` (200/200) |
| `A/RF1b-e` | 200 | 100/100 | 100/100 | **200/200 (100%)** | $68.19\% \pm 1.38\%$ ($65.81\text{–}72.78\%$) | $0.4684 \pm 0.0097$ ($0.4380\text{–}0.4899$) | $0.921$ ($0.891$) | $1.25$ ($1.22$) | 100% | `Zipfian` (200/200) |
| `B/RF1b-e` | 200 | 100/100 | 100/100 | **200/200 (100%)** | $67.43\% \pm 1.19\%$ ($65.66\text{–}72.14\%$) | $0.4304 \pm 0.0066$ ($0.4129\text{–}0.4471$) | $0.938$ ($0.917$) | $1.24$ ($1.22$) | 100% | `Zipfian` (200/200) |

Every single stream passes under adaptive clean-IVTFF calibration, adaptive raw-Parisel calibration, fixed thresholds, and strict-Zipfian thresholds (`R² > 0.85` and `CV > 0.80`).

---

## 4. Verification of Saved 400-Control Null Suite (`claim/null_suite_400_results.json`)

For both the Voynich manuscript and `VBCLC-152`, 400 controls per cell (200 word-order permutations + 200 glyph-shuffled controls) were audited across `A/ZL3b`, `B/ZL3b`, `A/IT2a`, and `B/IT2a`:

- **Manuscript (`manuscript_400_nulls`)**:
  - `A/ZL3b`: $\Delta\text{MI} = 0.0760 > \max_{400} = 0.0358$ ($z = 7.6$); $\text{ES}\times\Delta\text{MI} = 0.0532 > 0.0186$ ($z = 11.3$); $\text{excess\_edge\_MI} = 0.0842 > 0.0088$ ($z = 35.6$).
  - `B/ZL3b`: $\Delta\text{MI} = 0.2073 > \max_{400} = 0.0149$ ($z = 37.0$); $\text{ES}\times\Delta\text{MI} = 0.1337 > 0.0096$ ($z = 53.2$); $\text{excess\_edge\_MI} = 0.2089 > 0.0034$ ($z = 180.5$).
  - `A/IT2a`: $\Delta\text{MI} = 0.0717 > \max_{400} = 0.0340$ ($z = 7.3$); $\text{ES}\times\Delta\text{MI} = 0.0504 > 0.0168$ ($z = 11.7$); $\text{excess\_edge\_MI} = 0.0852 > 0.0069$ ($z = 36.1$).
  - `B/IT2a`: $\Delta\text{MI} = 0.2182 > \max_{400} = 0.0158$ ($z = 40.3$); $\text{ES}\times\Delta\text{MI} = 0.1390 > 0.0078$ ($z = 56.8$); $\text{excess\_edge\_MI} = 0.2202 > 0.0035$ ($z = 198.2$).
- **VBCLC-152 (`vbclc152_400_nulls`)**:
  - `A/ZL3b`: $\Delta\text{MI} = 0.1501 > \max_{400} = 0.0306$ ($z = 15.8$); $\text{ES}\times\Delta\text{MI} = 0.1041 > 0.0176$ ($z = 24.5$); $\text{excess\_edge\_MI} = 0.1366 > 0.0059$ ($z = 64.9$).
  - `B/ZL3b`: $\Delta\text{MI} = 0.2812 > \max_{400} = 0.0126$ ($z = 60.4$); $\text{ES}\times\Delta\text{MI} = 0.1870 > 0.0085$ ($z = 98.3$); $\text{excess\_edge\_MI} = 0.2448 > 0.0045$ ($z = 229.1$).
  - `A/IT2a`: $\Delta\text{MI} = 0.1218 > \max_{400} = 0.0304$ ($z = 13.4$); $\text{ES}\times\Delta\text{MI} = 0.0815 > 0.0153$ ($z = 19.6$); $\text{excess\_edge\_MI} = 0.1052 > 0.0062$ ($z = 49.9$).
  - `B/IT2a`: $\Delta\text{MI} = 0.2779 > \max_{400} = 0.0138$ ($z = 56.2$); $\text{ES}\times\Delta\text{MI} = 0.1848 > 0.0074$ ($z = 91.8$); $\text{excess\_edge\_MI} = 0.2391 > 0.0035$ ($z = 239.4$).

In every cell, the real statistic strictly beats all 400 controls (`beats_all_400 == true`).

---

## 5. Independent Re-Derivation from Scratch on `veritas`

1. **Manuscript Calibrations Re-Derived**:
   Using an independently written greedy longest-first 58-grapheme EVA tokenizer and independent implementations of `E->S`, `Bilat_full`, 10-chunk `MI`, and `Zipfian Shape`, all six manuscript cells in `claim/reference_calibration.json` (`A/ZL3b`, `B/ZL3b`, `A/IT2a`, `B/IT2a`, `A/RF1b-e`, `B/RF1b-e`) were reproduced to $< 10^{-6}$ numerical precision.
2. **Published Baselines Verified (`claim/reference_calibration.json`)**:
   - Slot-based generator (`claim/data/signatures_v27.py`): `0%` joint pass on Currier B (`MI = 0.1396`), `10%` on Currier A (`MI = 0.1771`).
   - Cardan grille (`claim/data/grille.py`): `0%` joint pass across all modes (`E->S = 0.3%–17.8%`).
   - Unmodified Naibbe (`0%` strict-Zipf joint pass, `E->S = 52.9%–53.2%`, `Shape = Intermediate`).
3. **Live Re-Derivation of Generated `VBCLC-152` Streams**:
   - Across all 20 period Latin and Italian plaintexts $\times 2$ seeds per cell (`40` streams/cell = `160` streams across `A/ZL3b`, `B/ZL3b`, `A/IT2a`, `B/IT2a`) plus `16` additional streams generated with unseen seeds (`seed = 90000+`), **100% (`40/40` and `4/4` per cell)** jointly passed all four `arXiv:2604.19762` signatures under every calibration regime.
   - Executing `claim/verify_p2_claim.py` on `veritas` also succeeded and printed `PASS`.
4. **Workspace Hygiene**:
   - Temporary checker files and job output directories inside `claim/` were removed after verification.

pass: true
