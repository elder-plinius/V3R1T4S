# Verification Receipts (`2026-11-02-rainrat-dcc89550`)

## 1. Output of `sh verify-it-yourself/run_checks.sh`

```text
CALIBRATION_OK: self-test passed
MODELS_OK: Fin7 (n=7), Fin25 (n=25), Fin55 (n=55) and opposite duals verified
LEAN_OK: Lean imports, full witness definitions, and theorem signatures verified
PASS
```

## 2. Output of Lean 4.29.1 Kernel Compilation (`lake env lean object/Equation677.lean`)

Compiled against `https://github.com/teorth/equational_theories` commit `2f49bdaf3d38ffb722e54ac1288c8269dac61846` (`leanprover/lean4:v4.29.1`):

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

## 3. Object File SHA-256 Receipts

- `object/Equation677.lean`: `dcc89550b0e5ce6d4e15f6e283a0401ccdaf9831289189929e67fa48cfebbe7f`
- `object/separation_models.json`: `f92fb469669e9911e75fb8db65e566eea9db82d7491a581965db76b82a90f4bb`
