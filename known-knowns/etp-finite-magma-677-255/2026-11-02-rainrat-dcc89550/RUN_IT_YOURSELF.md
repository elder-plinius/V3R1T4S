# Run It Yourself (`2026-11-02-rainrat-dcc89550`)

## 1. Standalone Verification from This Folder (Python 3 Standard Library Only)

From a fresh shell inside this package directory, run:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:

```text
CALIBRATION_OK: self-test passed
MODELS_OK: Fin7 (n=7), Fin25 (n=25), Fin55 (n=55) and opposite duals verified
LEAN_OK: Lean imports, full witness definitions, and theorem signatures verified
PASS
```

## 2. Rebuild `object/separation_models.json` from Scratch

```sh
python3 how-we-built-it/build_separation_models.py object/separation_models.json
```

## 3. Full Lean 4.29.1 Kernel Verification Against Upstream `equational_theories`

With `elan` (`leanprover/lean4:v4.29.1`) and a checkout of `https://github.com/teorth/equational_theories` (commit `2f49bdaf3d38ffb722e54ac1288c8269dac61846`, with Mathlib cache fetched via `lake exe cache get` and `lake build equational_theories.ManuallyProved.Equation677`):

```sh
cd /path/to/equational_theories
lake env lean /path/to/2026-11-02-rainrat-dcc89550/object/Equation677.lean
```

Expected compiler output (zero warnings, zero errors, zero `sorryAx`):

```text
'Eq677.eq677_leftMul_fixed_disjoint' depends on axioms: [propext, Classical.choice, Quot.sound]
'Eq677.eq255_of_eq677_leftMul_has_fixed_point' depends on axioms: [propext, Classical.choice, Quot.sound]
'Eq677.eq255_of_eq677_right_cancel' depends on axioms: [propext, Classical.choice, Quot.sound]
'Eq677.eq255_of_eq677_quasigroup' depends on axioms: [propext, Classical.choice, Quot.sound]
'Eq677.eq677_leftMul_faithful' depends on axioms: [propext, Classical.choice, Quot.sound]
'Eq677.eq255_of_eq677_uniform_leftMul' depends on axioms: [propext, Classical.choice, Quot.sound]
'Eq2910.eq47_of_eq2910_rightMul_has_fixed_point' depends on axioms: [propext, Classical.choice, Quot.sound]
'Eq2910.eq47_of_eq2910_left_cancel' depends on axioms: [propext, Classical.choice, Quot.sound]
'Eq2910.eq47_of_eq2910_quasigroup' depends on axioms: [propext, Classical.choice, Quot.sound]
'Eq677.Separation.not_leftMulHasFixedPoint_of_conjClosed' depends on axioms: [propext, Classical.choice, Quot.sound]
'Eq677.Separation.not_conjClosed_of_rightCancel_and_leftMulHasFixedPoint' depends on axioms: [propext,
 Classical.choice,
 Quot.sound]
'Eq677.Separation.not_rightCancel_and_not_conjClosed_of_leftMulHasFixedPoint' depends on axioms: [propext,
 Classical.choice,
 Quot.sound]
```
