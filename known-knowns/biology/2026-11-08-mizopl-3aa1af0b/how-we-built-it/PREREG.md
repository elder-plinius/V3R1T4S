# Prospective Pre-Registration — `eterna100-v2-vienna2-algorithmic-solve`

- `target_id`: `eterna100-v2-vienna2-algorithmic-solve`
- `freeze_utc`: `2026-11-08T15:35:00Z`
- `primary_metric`: Exact character-for-character dot-bracket match (`d_bp == 0`, `RNA.fold(seq)[0] == target_structure`) under stock `ViennaRNA 2.6.4` (`RNAfold -T 37.0` with no extra flags, Turner 2004 energy parameters) on the `Secondary Structure V2` column of `data/eterna100_puzzles.tsv` (`sha256: 71147b94c1762a3c8fe93f59e87b53b6292b1c3b9367ce22d5a9c7c6b4736ef6`).
- `scoreboard_bar`:
  - `Full Win / p1`: Solve de novo (`d_bp == 0`) at least one of the `7` Eterna100-V2 puzzles that have zero `Success=1` rows under `folder == 'vienna2'` in `data/results.tsv` (`sha256: 2861ceb5a0280e5565c40016f169697fb324db7f7c56505c1489a8b78afcea6c`): `#68, #71, #79, #86, #90, #99, #100`.
  - `p2`: Solve more than `DesiRNA`'s `92 / 100` Eterna100-V2 targets using a single frozen de novo algorithm.
  - `p3`: Provide machine-checkable Turner 2004 thermodynamic barrier / undesignability certificates for the remaining `Sample Solution = None` targets (`#68, #86, #90, #99, #100`).

## 1. Frozen Zero-Leakage Protocol

1. **Strict Input Isolation (`how-we-built-it/eterna100_v2_targets_only.tsv`):** Strip all `Sample Solution` columns before algorithm development so the solver (`how-we-built-it/cegis_rna_solver.py`) reads only `(puzzle_id, puzzle_name, target_structure)` and a deterministic seed (`20261101 + puzzle_id`).
2. **Zero Hardcoded Sequences or Puzzle IDs:** No sequence string, motif palette, or puzzle-ID branch may be hardcoded inside `cegis_rna_solver.py`; every motif and sequence is synthesized algorithmically at runtime from the input dot-bracket structure under stock `ViennaRNA 2.6.4`.
