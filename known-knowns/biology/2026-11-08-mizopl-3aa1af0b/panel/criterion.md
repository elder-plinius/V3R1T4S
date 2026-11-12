# Skeptic 3 — Criterion & Traps Audit (`eterna100-v2-vienna2-algorithmic-solve`)

context: fresh review session

## 1. Target Specification & Pitfall Checklist

- **Target ID:** `eterna100-v2-vienna2-algorithmic-solve`
- **Submission ID:** `2026-11-08-mizopl-3aa1af0b`

1. **Trap 1 — Stock ViennaRNA 2 Energy Model (`Turner 2004`, `T = 37.0 C`, No Extra Flags):**
   - Verified that `how-we-built-it/cegis_rna_solver.py` (`sha256: 52f5b2e60fe717e9c18768bd31776d33eafa1ee62da6b830cd622eb95249cb75`), `how-we-built-it/verify_p3_undesignability_certificates.py` (`sha256: c4670dfee1223a03880ae97a7494f9a003b4ac5e5cccfa177ca4b6f5636fc1e5`), and `verify-it-yourself/verify.py` call stock `RNA.fold(seq)` and `RNA.eval_structure_simple(seq, target)` under default `ViennaRNA 2.6.4` (`T = 37.0 C`, `dangles = 2`, Turner 2004 parameters, zero Turner 1999 parameter overrides).
2. **Trap 2 — `Secondary Structure V2` Column Only (Not V1):**
   - Verified that `how-we-built-it/eterna100_v2_targets_only.tsv` (`sha256: c3e79eef8eef7db8a40d5c3e92c71114703e36a847593997dbe3edc025c7978a`) extracts strictly `(puzzle_id, puzzle_name, target_structure)` from the `Secondary Structure V2` column of `data/eterna100_puzzles.tsv` (`sha256: 71147b94c1762a3c8fe93f59e87b53b6292b1c3b9367ce22d5a9c7c6b4736ef6`).
3. **Trap 3 — Zero Seeding or Copying from `Sample Solution` or Player Solutions:**
   - Verified by static AST/source inspection that `how-we-built-it/cegis_rna_solver.py` has zero references to `Sample Solution`, `eterna100_puzzles.tsv`, or `results.tsv`, zero hardcoded puzzle IDs, and zero hardcoded literal RNA sequence strings or motif palettes. Every sequence is generated de novo from the input dot-bracket string and seed.
   - Cross-checked all 100 sequences in `object/ckpt_best.json` (`sha256: 03594be6116df6a7e796fc45191e8aade08b12a215c15c394deb2d636af39b2f`) against the 95 `Sample Solution` strings in `eterna100_puzzles.tsv`: all 94 structured puzzles have completely distinct sequences (the only identical string is the trivial all-`A` open chain `AAA...AAA` on `#52 The String`).
4. **Trap 4 — Exact `RNAfold` Traceback String vs. Energy Tie (`d_bp = 0` vs `de_mfe = 0.00`):**
   - Strictly distinguished throughout the package: `95 / 100` puzzles (including `#79 Shapes and Energy` and `#71 Variation of a crop circle`) achieve `d_bp = 0` where stock `RNA.fold(seq)[0] == target_structure` character-for-character, while `#68 Taraxacum officinale` (`Sample Solution = None`) is reported honestly as an exact MFE ground-state energy tie (`de_mfe = 0.00 kcal/mol`, `E_target == E_MFE = -100.60 kcal/mol`, `d_bp = 13`) paired with `Theorem #68-Pigeonhole-Degeneracy-and-RY-Orthogonality`.
5. **Scope Honesty on `p3`:**
   - Explicitly documented in `README.md` (`## Not Claimed`) that `object/p3_undesignability_certificates.json` (`sha256: e08fb41d6b11a3d01841866bba9cd33ca25d43924039267e3673e8001207f240`) is produced by our standalone exhaustive Turner 2004 motif & Pigeonhole barrier verifier (`how-we-built-it/verify_p3_undesignability_certificates.py`) under stock `ViennaRNA 2.6.4` rather than invoking the external `shanry/RNA-Undesign` binary.

pass: true
