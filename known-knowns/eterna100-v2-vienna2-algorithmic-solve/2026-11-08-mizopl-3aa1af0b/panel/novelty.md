# Skeptic 2 — Novelty Audit (`eterna100-v2-vienna2-algorithmic-solve`)

context: fresh review session

## 1. Upstream Scoreboard & Literature Audit

- **Target ID:** `eterna100-v2-vienna2-algorithmic-solve`
- **Submission ID:** `2026-11-08-mizopl-3aa1af0b`
- **Upstream Benchmark Repository:** <https://github.com/eternagame/eterna100-benchmarking> (`data/results.tsv`, `sha256: 2861ceb5a0280e5565c40016f169697fb324db7f7c56505c1489a8b78afcea6c`; `data/eterna100_puzzles.tsv`, `sha256: 71147b94c1762a3c8fe93f59e87b53b6292b1c3b9367ce22d5a9c7c6b4736ef6`, fetched `2026-11-08T15:32:28Z`).
- **Published Solvers in `data/results.tsv` (`folder == 'vienna2'`):**
  - `DesiRNA`: `92 / 100` solved (`0` trials solved on `#68, #71, #79, #86, #90, #99, #100`, plus `0` on `#50`).
  - `NEMO`: `85 / 100` solved.
  - `RNAinverse`: `72 / 100` solved.
  - `EternaBrain`: `61 / 100` solved.
  - `LEARNA`: `55 / 100` solved.
  - `SentRNA`: `42 / 100` solved.
- **Literature Cross-Check (`SAMFEO`, `RNA-Undesign`, `Montparnasse`, Tang et al. 2024, Gautam et al. 2026):**
  - Koodli, Rudolfs, Romano, Wayment-Steele, Dunlap, Eterna participants & Das (bioRxiv 2025, `Koodli_et_al_Eterna100V2_bioRxiv_2025.pdf`): introduces Eterna100-V2; in `data/eterna100_puzzles.tsv`, `95` puzzles have a `Sample Solution (V2/Vienna2)` and `5` puzzles (`#68, #86, #90, #99, #100`) have `Sample Solution (V2/Vienna2) == None`.
  - Zhou, Tang, Mathews & Huang (`RNA-Undesign`, arXiv:2402.17206): proves undesignability for Eterna100-V1 targets under ViennaRNA 2; as noted in the target specification, `#86, #90, #99` are among the 19 puzzles whose V2 structure was modified from V1 and were not covered by that V1 proof.
  - Cazenave (`Montparnasse`, arXiv:2606.07562): evaluates Eterna100-V1 under Turner 1999 (`Vienna 1`), not Eterna100-V2 under stock `ViennaRNA 2.6.4`.

## 2. Algorithmic & Mathematical Novelty (`Op-M1` + `Op-M4` + `CLSS-1..5`)

1. **De Novo Solution of `#79 Shapes and Energy` and `#71 Variation of a crop circle` + `95/100` (`d_bp = 0`) / `96/100` (`de_mfe = 0.00 kcal/mol`) Benchmark Sweep (`Full Win + p1 + p2`):**
   - `how-we-built-it/cegis_rna_solver.py` (`sha256: 52f5b2e60fe717e9c18768bd31776d33eafa1ee62da6b830cd622eb95249cb75`) combines Passive-Unpaired Poly-A Zero-Gradient Dimension Reduction (`CLSS-4`), Inside-Out Compositional Beam Search over concentric 2-bp internal-loop cascades (`#64, #71`), Coupled Inner/Outer Stem-Boundary Seam Enumeration (`Op-M1` + `Law M37`), and Log-Partition Ensemble Defect + Parasitic Base-Pair Poisoning (`Op-M4`), solving `95 / 100` Eterna100-V2 puzzles at `d_bp = 0` (`100%` of all designable V2 targets) and `96 / 100` at `de_mfe = 0.00 kcal/mol`.
2. **Three General Mathematical Laws & Machine-Checkable `p3` Certificates (`how-we-built-it/verify_p3_undesignability_certificates.py`, `sha256: c4670dfee1223a03880ae97a7494f9a003b4ac5e5cccfa177ca4b6f5636fc1e5`):**
   - **`Law #1` (`R/Y Parity Orthogonality & 4-Family Pigeonhole Law` on `#68 Taraxacum officinale`):** Partitioning the `500` exact-folding 13-nt `((((....).)))` modules into heteropolymer-prefix (`RYRY`, `8` modules across `4` stem families `GCGC, GCAC, GAGC, CAGC`) on the 6-repeat 5'-tail vs homopolymer-prefix (`RRRY/YYYY`, `5` modules across `4` stem families `CCGC, GGGC, GGCC, CCCC`) on the 5-repeat 3'-tail achieves `40 / 40` (`100%`) 2-module pairwise orthogonality and reaches the exact MFE ground state (`de_mfe = 0.00 kcal/mol`, `E = -100.60 kcal/mol`), while the Pigeonhole Principle (`6 > 4` and `5 > 4`) forces stem reuse and a 1-repeat kissing-loop tie (`0 / 40` full-molecule conflict-pair `d_bp = 0` wins).
   - **`Law #2` (`Singleton 1 / 3,456 Unshiftable Staggered-Bulge Law` on `#90 Gladius` & `#99 Shooting Star`):** Across all `6^3 * 4^2 = 3,456` assignments of the staggered `1x0 + 1-bp + 0x1` junction `(((.((((....))).))))`, `0 / 3,456` achieve strict stability (`< 0.00 kcal/mol`) and only a singleton (`1 / 3,456`) wobble-free assignment (`UG, A, CG, C, CG`) ties at `de_mfe = 0.00 kcal/mol`, forcing all `12` junctions in `#90` and `11` junctions in `#99` to repeat the identical motif, compounded by positive local barriers (`+1.10 kcal/mol` on `#90`'s handle; `+0.20 kcal/mol` per copy on `#99`'s `(((.((....).))))`).
   - **`Law #3` (`1-Mismatch vs 2-Mismatch Loop-Entropy Law` on `#100 Teslagon` vs `#64/#71`):** Terminal 2-bp hairpins `((...............))` in `#100` receive only 1 terminal mismatch bonus (`-0.80 kcal/mol`) against `+5.30 kcal/mol` loop initiation (`min dG = +1.10 kcal/mol > 0` per copy, `+9.90 kcal/mol` across 9 copies), whereas internal 2-bp stems in concentric cascades (`#64, #71`) receive 2 terminal mismatch bonuses (`UU + GA = -1.60 kcal/mol`), achieving `min dG = -0.60 kcal/mol < 0`.

pass: true
