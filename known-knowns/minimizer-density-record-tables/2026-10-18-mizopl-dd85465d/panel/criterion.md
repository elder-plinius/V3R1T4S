# CRITERION Panel Report — `(w = 12, k = 3)` Binary-Projected DNA Minimizer Order

context: Antigravity fresh subagent (invoke_subagent, role CRITERION)
confirmed_scope: An explicit binary-projected DNA minimizer rank order claim/w12_k3_improved.gm (72 bytes, sha256 dd85465d87f23d688778ff35175ed19e4c9f00e71cad28b535d7a9d73294f302, rank vector [4, 7, 1, 0, 6, 5, 2, 3]) for (w, k) = (12, 3) with exact expected DNA density 146,639,789 / 2^30 = 0.1365689458, strictly lowering the smallest listed expected DNA density 0.138389448 (angle-based) by 1.315492% relative and the published GreedyMini density 149,082,035 / 2^30 = 0.1388434647 by 1.638189% relative across OrensteinLab/10-minimizers and OrensteinLab/GreedyMini at identical 72-byte storage cost.

## 1. Clause-by-Clause Audit of the Verbatim Success Criterion

1. **Clause (1) — Explicit minimizer order for a stated `(w, k)` pair, given as a complete rank file:**
   - Target parameters: `(w, k) = (12, 3)`.
   - Binary `.gm` witness file `claim/w12_k3_improved.gm` is present on disk (`72` bytes, `sha256: dd85465d87f23d688778ff35175ed19e4c9f00e71cad28b535d7a9d73294f302`), encoding length header `size = 8` followed by the `8` little-endian `uint64_t` ranks `[4, 7, 1, 0, 6, 5, 2, 3]`, which is a strict permutation of `0..7` over binary 3-mers `000..111`.
   - Human-readable witness file `claim/w12_k3_improved.csv` (`59` bytes, `sha256: 24790fb381b985fe053ea4d82ae225412815e1a2df754a55fe5a53448ab7b55a`) encodes the identical mapping `000:4, 001:7, 010:1, 011:0, 100:6, 101:5, 110:2, 111:3`.
   - **Verdict:** Satisfied without qualification.

2. **Clause (2) — DNA density computed by the skeptic with the repositories' own density measurement code:**
   - Compiling and running `claim/verify_greedymini_dna.cpp` (containing verbatim `prob_gc_dna` and `density_expected_dna` from `OrensteinLab/GreedyMini/code/density_and_gc.cpp`) and cross-checking with independent exact 4-ary de Bruijn transfer-matrix dynamic programming in `panel/w12_k3/criterion_work/verify_criterion.py` over all `4^(12+3) = 4^15 = 2^30 = 1,073,741,824` DNA windows of length `15` yields:
     - `claim/w12_k3_improved.gm`: `prob_gc_dna = 146,639,789 / 2^30 = 0.1365689458` (density factor `(w+1)*d = 1.7753962958`). Both `prob_gc_dna` and the 4-ary transfer-matrix DP agree to the exact integer numerator `146,639,789`.
     - `claim/published_w12_k3.gm` (`72` bytes, `sha256: c592519b57ad8104860b7e1559b28c2d37ef329db82298b151a65e056ce27f1d`, rank vector `[8, 2, 8, 8, 0, 4, 1, 3]`): `prob_gc_dna = 149,082,035 / 2^30 = 0.1388434647` (density factor `(w+1)*d = 1.8049650406`). Both `prob_gc_dna` and the 4-ary transfer-matrix DP agree to the exact integer numerator `149,082,035`.
   - Empirical check using the `10-minimizers` sampling routine (`random_density_function_dna_includes_tiebreaking`, `N = 1,000,000`, `seed = 0`) in `claim/author_checker_minimizer_check.py` gives `0.136709` for `claim/w12_k3_improved.gm` vs `0.138838` for `claim/published_w12_k3.gm` (`-1.5334%` relative), consistent with the exact expectation.
   - **Verdict:** Satisfied without qualification.

3. **Clause (3) — Strictly lower than the smallest value listed for `(w = 12, k = 3)` across `OrensteinLab/10-minimizers` and `OrensteinLab/GreedyMini` by at least `0.5%` relative:**
   - In `claim/k_extension_k16_w12.csv` (`1,644` bytes, `sha256: 88c4f8fcd0ea6d4308f4e1fc716bb901ea78d3c6112b7e70d4af42bb631bf2fa`), column `3` (`k = 3`, `w = 12`) lists five non-empty methods (`miniception` and `open-close-syncmer` are blank/NaN at `k = 3`):
     - `angle-based`: `0.138389448` — our order (`0.1365689458`) reduces expected DNA density by `-0.0018205022` absolute, or **`-1.315492%` relative** (`2.63x` the required `0.5%` threshold).
     - `GreedyMini` (CSV rounded entry): `0.138843` — reduced by `-0.0022740542` absolute, or **`-1.637860%` relative**.
     - `claim/published_w12_k3.gm` (exact precomputed `.gm` binary): `149,082,035 / 2^30 = 0.1388434647` — reduced by `2,442,246` gamechanger windows (`-0.0022745188` absolute), or **`-1.638189%` relative** (`3.28x` the required `0.5%` threshold).
     - `decycling`: `0.150863` — reduced by **`-9.474857%` relative**.
     - `double decycling`: `0.150863` — reduced by **`-9.474857%` relative**.
     - `mod-minimizer`: `0.222468` — reduced by **`-38.611870%` relative**.
   - **Verdict:** Satisfied without qualification.

4. **Clause (4) — Same density definition and stated storage cost:**
   - The `k_extension_k16_w12.csv` table at `k = 3` reports expected DNA density over `4^(w+k) = 4^15` random DNA windows (`prob_gc_dna` / `density_expected_dna` produces `0.1388434647`, matching the table's `0.138843` to 6 decimal places). Our comparison uses the exact same expected DNA density definition.
   - Storage cost is explicitly stated and verified: `72` bytes on disk in `.gm` binary format (`8`-byte `size_t` length prefix `8` plus `8` `uint64_t` rank entries, matching `claim/published_w12_k3.gm` byte-for-byte in size and schema), or `24` bits (`8 x 3` bits) of raw rank table information.
   - **Verdict:** Satisfied without qualification.

## 2. Null-Model Control, Single-Swap Neighborhood, and Exhaustive `8! = 40,320` Audit

- **400-Random-Permutation Null Model (`seed = 20261018`, `panel/w12_k3/criterion_work/verify_criterion.py`):**
  - Sample size: `400` uniform random permutations of `0..7`.
  - Sample mean density: `0.1533737694` (mean gamechangers: `164,683,830.89 / 2^30`).
  - Sample standard deviation: `0.0142896630`; median: `0.1492427755`; range: `[0.1365689458, 0.1936503230]`.
  - `claim/w12_k3_improved.gm` (`0.1365689458`) sits `1.1760` standard deviations below the random null mean and at the absolute floor of the distribution.
- **Exhaustive Population Audit Over All `8! = 40,320` Permutations (`panel/w12_k3/criterion_work/exhaustive_8fact.cpp`):**
  - Across all `40,320` strict permutations of `0..7`, the exact global minimum expected DNA numerator is `146,639,789 / 2^30 = 0.1365689458` (`0` permutations out of `40,320` achieve a strictly smaller numerator).
  - Population mean density: `0.1533575830` (`164,666,450.90 / 2^30`); population standard deviation: `0.0143474339` (`15,405,439.84 / 2^30`); global maximum: `208,267,453 / 2^30 = 0.1939641805`.
  - The second-lowest distinct numerator in the entire `40,320`-permutation space is `146,651,507 / 2^30 = 0.1365798591` (`+11,718` gamechanger windows higher than `claim/w12_k3_improved.gm`).
  - Why `80` permutations tie at the global minimum `146,639,789`: assigning ranks `{0, 1, 2}` to `(011, 010, 110)` (or its bitwise complement `(100, 101, 001)`) leaves only `000000000000000`, `100000000000000`, and `111111111111111` (and their complements) free of the top-3 3-mers across a window of `w = 12` k-mers; consequently `001` and `101` never become window minimizers, producing an equivalence class of `40` permutations (plus `40` bitwise-complement permutations) that all induce the exact same gamechanger set of `146,639,789` DNA windows.
- **Single-Swap Neighborhood (`28` transpositions of `claim/w12_k3_improved.gm`):**
  - `0 / 28` single-swap neighbors have strictly lower density; `6 / 28` are tied at `146,639,789 / 2^30` (transpositions among the inactive high-rank 3-mers preserving `rank(000)` lower than `rank(100)`), and `22 / 28` are strictly worse (up to `187,850,547 / 2^30 = 0.1749494551` for `swap(0, 3)`).

## 3. Hidden Quantifiers & Scope Check

- No hidden quantifiers or stretched definitions exist: `(w, k) = (12, 3)` is an explicit cell in `claim/k_extension_k16_w12.csv`, the binary `.gm` format is identical to `claim/published_w12_k3.gm`, and the relative reduction (`-1.315492%` vs `angle-based`, `-1.638189%` vs `GreedyMini`) is more than double the `0.5%` relative threshold.
- Note on scope precision: `claim/w12_k3_improved.gm` (`[4, 7, 1, 0, 6, 5, 2, 3]`) achieves the exact global minimum expected DNA density `146,639,789 / 2^30 = 0.1365689458` across all `8! = 40,320` binary 3-mer permutations (shared by an equivalence class of `80` permutations that assign identical active ranks `{0, 1, 2}` to `{011, 010, 110}` or its complement). `confirmed_scope` states the exact verified claim without overclaiming uniqueness of the permutation representation.

pass: true
