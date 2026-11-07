# Receipts: real output of verify-it-yourself/run_checks.sh

Recorded 2026-10-14T07:38:59Z on the contributor's machine (Linux, 4 cores, 15 GB), PHYSLIB = a Physlib checkout at be0f21e5002d6d73b87f2055530c1e8bf7151546 built with Lean 4 v4.34.1. Machine paths of the checker's scratch folder are shown as [scratch].

## 1. The package as shipped (exit 0, 62 s)

```
physlib commit: be0f21e5002d6d73b87f2055530c1e8bf7151546
object sha256: 13837a7e226a97b9fef5bd04d6f362c0db869627cfa3a7239d4f54343cde5c8b
spec compile: exit 0
candidate compile: exit 0
check file: exit 0
'V3R1T4S_check' depends on axioms: [propext, Classical.choice, Quot.sound]
axioms: ['Classical.choice', 'Quot.sound', 'propext']
PASS
```

## 2. Control: one digit of the object changed (exit 1, 50 s)

The middle ASCII digit of object/OfCliffordAlgebraInjective.lean (line 75) was changed from 4 to 1 in a copy, the same corruption repo/kit/check_run.py applies to text objects (it does not scan .lean files itself).

```
physlib commit: be0f21e5002d6d73b87f2055530c1e8bf7151546
object sha256: 288308d57f9950694da036d69be4756e290c866d7d4fd7f5ac18da3d0aba5b9f
spec compile: exit 0
candidate compile: exit 1
[scratch]/V3R1T4SClaim.lean:34:2: warning: Try this: 
  haveI̵

The goal is a proposition, so `have` is preferred over `haveI`.
The difference between `have` and `haveI` is that `haveI` inlines the value.
But this is not relevant for proofs because of proof irrelevance.

Note: This linter can be disabled with `set_option linter.style.haveILetI false`
[scratch]/V3R1T4SClaim.lean:75:8: error: Tactic `rewrite` failed: Did not find an occurrence of the pattern
  ⟨3, ?m.554⟩
in the target expression
  (LinearMap.toMatrix chiralBasis chiralBasis) (gamma (finSumFinEquiv.symm ((fun i => i) ⟨3, ⋯⟩))) =
    C ((fun i => i) ⟨3, ⋯⟩)

case «3»
⊢ (LinearMap.toMatrix chiralBasis chiralBasis) (gamma (finSumFinEquiv.symm ((fun i => i) ⟨3, ⋯⟩))) =
    C ((fun i => i) ⟨3, ⋯⟩)
[scratch]/V3R1T4SClaim.lean:75:22: error: Tactic `decide` proved that the proposition
  3 < 1
is false
[scratch]/V3R1T4SClaim.lean:109:33: warning: This simp argument is unused:
  Matrix.mul_apply

Hint: Omit it from the simp argument list.
  [apply] simp [W, C, Fin.sum_univ_succ, Fin.sum_univ_four, Matrix.sum_apply, Complex.ext_iff, Matrix.cons_val_two,
    Matrix.cons_val_three] at h00 h11 h01 h10 h02 h20 h03 h12

Note: This linter can be disabled with `set_option linter.unusedSimpArgs false`
[scratch]/V3R1T4SClaim.lean:109:51: warning: This simp argument is unused:
  Fin.sum_univ_four

Hint: Omit it from the simp argument list.
  [apply] simp [W, C, Fin.sum_univ_succ, Matrix.mul_apply, Matrix.sum_apply, Complex.ext_iff, Matrix.cons_val_two,
    Matrix.cons_val_three] at h00 h11 h01 h10 h02 h20 h03 h12

Note: This linter can be disabled with `set_option linter.unusedSimpArgs false`

problem: candidate does not compile cleanly
FAIL
```
