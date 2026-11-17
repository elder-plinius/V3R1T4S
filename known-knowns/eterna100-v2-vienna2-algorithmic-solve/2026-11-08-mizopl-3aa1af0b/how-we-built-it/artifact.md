# Technical Artifact Overview — `eterna100-v2-vienna2-algorithmic-solve` (`2026-11-08-mizopl-3aa1af0b`)

## 1. Released Code & Data Artifacts in `how-we-built-it/`

1. `how-we-built-it/cegis_rna_solver.py` (`sha256: 52f5b2e60fe717e9c18768bd31776d33eafa1ee62da6b830cd622eb95249cb75`):
   - Standalone deterministic de novo RNA inverse-folding solver implementing:
     - **Passive-Unpaired Poly-A Lock (`CLSS-4`):** Locks unpaired bases at distance `>= 2` from all target base pairs (outside hairpins `<= 6` nt) to `'A'`, eliminating zero-gradient unpaired degrees of freedom that cause parasitic duplexes.
     - **Inside-Out Compositional Beam Search for Concentric 2-bp Internal-Loop Cascades (`Op-M3` + `CLSS-3`):** Solves concentric `2-bp` stem cascades (`#64, #71`) from the innermost hairpin outward by maximizing the `2`-mismatch internal-loop bonus (`UU + GA = -1.60 kcal/mol`).
     - **Coupled Inner/Outer Stem-Boundary Seam Enumeration & Anti-Collision Flip (`Op-M1` + `Law M37`):** Breaks `de_mfe = 0.00 kcal/mol` MFE ties (`#79 Shapes and Energy`) by coupling short-stem closure with inner-helix single-pair anti-collision flips.
     - **Runtime Turner Pyrimidine-Stratum Discovery & `RYRY` vs `RRRY/YYYY` Chain Synthesis (`Op-M1` + `CLSS-1`):** Discovers optimal tetraloop pyrimidine strata and synthesizes orthogonal 5' heteropolymer (`RYRY`) vs 3' homopolymer (`RRRY/YYYY`) repeat chains (`#68 Taraxacum officinale`, reaching exact MFE ground state `de_mfe = 0.00 kcal/mol`, `E = -100.60 kcal/mol`).
2. `how-we-built-it/verify_p3_undesignability_certificates.py` (`sha256: c4670dfee1223a03880ae97a7494f9a003b4ac5e5cccfa177ca4b6f5636fc1e5`):
   - Standalone exhaustive Turner 2004 motif & Pigeonhole barrier verifier certifying `object/p3_undesignability_certificates.json` (`sha256: e08fb41d6b11a3d01841866bba9cd33ca25d43924039267e3673e8001207f240`) in `~7.7s` under stock `ViennaRNA 2.6.4`.
3. `how-we-built-it/eterna100_v2_targets_only.tsv` (`sha256: c3e79eef8eef7db8a40d5c3e92c71114703e36a847593997dbe3edc025c7978a`):
   - Pure 3-column target table `(puzzle_id, puzzle_name, target_structure)` extracted from the `Secondary Structure V2` column of `data/eterna100_puzzles.tsv` with all `Sample Solution` columns removed.
