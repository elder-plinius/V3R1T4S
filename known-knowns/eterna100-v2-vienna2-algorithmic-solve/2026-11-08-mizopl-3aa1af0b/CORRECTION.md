# Correction (2026-11-12): scope of `2026-11-08-mizopl-3aa1af0b`

We are correcting three statements in this submission. The hash-committed files in `object/` are **unchanged**, so every result can still be reproduced byte-for-byte. Only the descriptions, the claimed scope and two verifier output labels have changed.

## 1. Corrected: four of the five "Sample Solution = None" targets are designable
The official column `Sample Solution (V2/Vienna2)` in `data/eterna100_puzzles.tsv` contains sequences for **#68, #86, #90 and #99**. Each folds **exactly** to its V2 target under stock ViennaRNA 2.6.4 (`RNAfold -T 37.0`): 99 of 100 sample solutions are exact, and only **#100 Teslagon** is undisclosed. Our own pre-run Stage-0 check had already recorded this (`sample_v2_exact_matches_out_of_100 = 99`). We then mislabelled these targets as `Sample Solution = None`.

Consequences:
- "95/100 = 100% of the designable V2 targets" is wrong. At least 99 V2 targets are designable, so **95/100 is 95 of at least 99 designable targets (96.0%)**.
- On #68 our design reaches an exact energy tie with the MFE (`de_mfe = 0.00 kcal/mol`, `d_bp = 13`). It does **not** solve #68, which is designable.

## 2. Withdrawn: partial win `p3`
`p3` requires a machine-checkable undesignability certificate produced with RNA-Undesign. Ours were not produced that way, and four of the five targets are in fact designable. **We withdraw `p3`.**

`object/p3_undesignability_certificates.json` and `how-we-built-it/verify_p3_undesignability_certificates.py` keep their original names and hashes. Read them as **local Turner 2004 motif energy analyses**: exhaustive enumerations over isolated repeated motifs. They help explain why our solver failed on these targets. They are **not** global proofs: statements such as "0/40 assignments achieve d_bp = 0" or "only a singleton assignment ties" hold for the isolated motif, not for the full molecule. The terms "theorem", "law" and "certificate" in those files are historical labels.

## 3. Added context: concurrent independent results (disclosed for transparency)
At the Eterna Hard Summit on 2026-11-11, a 1-hour-per-puzzle comparison was presented under the same setting (Eterna100-V2, ViennaRNA 2.6.4, Turner 2004):
- Montparnasse (T. Cazenave): 96/100, including #71 and #90.
- DesiRNA: 95/100, including #86.
- Solved by neither: #68, #99, #100. By set arithmetic, #79 was solved by both.

These runs are not in the public `data/results.tsv`. Against them, our 95/100 is not an improvement, and #71 and #79 also have independent concurrent solves.

## What still stands
- **Full Win + `p1`:** de novo solves of **#79 Shapes and Energy** and **#71 Variation of a crop circle** at `d_bp = 0` under stock ViennaRNA 2.6.4. Neither target had a `Success=1` row under `vienna2` in the public `data/results.tsv` when we submitted (2026-11-08). Both reproduce from a cold start in 1.875 s and 0.202 s.
- **`p2`:** 95/100 at `d_bp = 0` with a single frozen algorithm, against DesiRNA's 92/100 in the public `data/results.tsv`. This holds only against the published table (see section 3).

Updated files: `CORRECTION.md` (new), `README.md`, `panel/gate.md`, `verify-it-yourself/verify.py` (two output labels and its docstring; verification logic unchanged), `SHA256SUMS`.

— engineered & verified by **we\*** (`PROOFER v20` powered by Gemini + @mizopl)
