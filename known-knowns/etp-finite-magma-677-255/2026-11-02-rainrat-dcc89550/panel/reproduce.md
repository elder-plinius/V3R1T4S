# Panel Skeptic 1 — REPRODUCE Report (`etp-finite-magma-677-255`)

context: subagent (fresh REPRODUCE skeptic)

## 1. Scope & Artifact Integrity Receipts

This reproduction audit examined only the files inside `claim/`:
- `claim/claim.md`
- `claim/target.md`
- `claim/REPRODUCE.md`
- `claim/Equation677.lean` (SHA-256: `dcc89550b0e5ce6d4e15f6e283a0401ccdaf9831289189929e67fa48cfebbe7f`, 399 lines)
- `claim/separation_models.json` (SHA-256: `f92fb469669e9911e75fb8db65e566eea9db82d7491a581965db76b82a90f4bb`)
- `claim/check_p2.py` (SHA-256: `3bc4c61269baed20814fd352d8f0b0fbed1cbebccb57a0c7d5d73b667ea89ec3`, 310 lines)
- `claim/status_snapshot.md`
- `claim/lean_build.log`

## 2. Independent Python Verifier Execution (`claim/check_p2.py`)

Command executed:
```bash
python3 claim/check_p2.py claim/separation_models.json claim/Equation677.lean
```

Exact stdout:
```text
CALIBRATION_OK: self-test passed
MODELS_OK: Fin7 (n=7), Fin25 (n=25), Fin55 (n=55) and opposite duals verified
LEAN_OK: Lean imports, full witness definitions, and theorem signatures verified
PASS
```
Exit code: `0`.

## 3. Negative / Corrupted-Input Calibration Tests

1. **Corrupted `separation_models.json` test**: Modifying a single Cayley table entry (`Fin7[0][0] = 1`) in a temporary copy caused `claim/check_p2.py` to exit with code `1` and print:
   ```text
   CALIBRATION_OK: self-test passed
   MODELS_FAIL: Fin7 table does not match Sep7 formula (4x + y) mod 7
   FAIL
   ```
2. **Corrupted `Equation677.lean` test**: Modifying a witness constant (`d == 9` -> `d == 8` in `isQR11`) in a temporary copy of `claim/Equation677.lean` caused `claim/check_p2.py` to exit with code `1` and print:
   ```text
   CALIBRATION_OK: self-test passed
   MODELS_OK: Fin7 (n=7), Fin25 (n=25), Fin55 (n=55) and opposite duals verified
   LEAN_FAIL: missing or modified Lean declaration:
   def isQR11 (d : Nat) : Bool :=
     d == 1 || d == 3 || d == 4 || d == 5 || d == 9
   FAIL
   ```

## 4. Independent Lean 4 Kernel Compilation (`claim/Equation677.lean`)

From the upstream Equational Theories Project repository (`references/equational_theories`, toolchain `leanprover/lean4:v4.29.1`), `claim/Equation677.lean` (which directly imports `equational_theories.Equations.All` and `equational_theories.ManuallyProved.Equation677`) was independently compiled via:
```bash
lake env lean ../../runs/2026-11-01-1637/claim/Equation677.lean
```

Exact compiler output (exit code `0`, zero warnings, zero errors, zero `sorryAx`):
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

All 12 `#print axioms` declarations depend exclusively on `[propext, Classical.choice, Quot.sound]`, matching `claim/REPRODUCE.md` and `claim/lean_build.log` verbatim.

pass: true
