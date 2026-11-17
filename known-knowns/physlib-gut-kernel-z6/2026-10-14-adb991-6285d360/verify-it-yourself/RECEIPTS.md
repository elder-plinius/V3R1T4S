# Receipts: real output of verify-it-yourself/run_checks.sh

Recorded 2026-10-15T08:03:02Z on the contributor's machine (Linux, 4 cores, 15 GB), PHYSLIB = a Physlib checkout at 76245c854e4827a1dd7f20d1c053b61219cc8fbb built with Lean 4 v4.34.1. Machine paths of the checker's scratch folder are shown as [scratch].

## 1. The package as shipped (exit 0, 24 s)

```
physlib commit: 76245c854e4827a1dd7f20d1c053b61219cc8fbb
object sha256: 6285d360e0d0a5a396fb3a5461d732888f314b08dcef13c1eda2bcd63aa3a5bd
spec compile: exit 0
candidate compile: exit 0
check file: exit 0
'V3R1T4S_check' depends on axioms: [propext, Classical.choice, Quot.sound]
axioms: ['Classical.choice', 'Quot.sound', 'propext']
PASS
```

## 2. Control: one digit of the object changed (exit 1, 15 s)

The middle ASCII digit of object/PatiSalamInclSMKer.lean (line 144) was changed from 4 to 1 in a copy, the same corruption repo/kit/check_run.py applies to text objects (it does not scan .lean files itself).

```
physlib commit: 76245c854e4827a1dd7f20d1c053b61219cc8fbb
object sha256: 6ca4d496bf796785bcc680ae09b7a7ec6daf19f4d7d4c161cbfb77697c67545d
spec compile: exit 0
candidate compile: exit 1
[scratch]/V3R1T4SClaim.lean:144:4: error: Function expected at
  psMatrix1
but this term has type
  ?m.1

Note: Expected a function because this term is being applied to the argument
  x

Hint: The identifier `psMatrix1` is unknown, and Lean's `autoImplicit` option causes an unknown identifier to be treated as an implicitly bound variable with an unknown type. However, the unknown type cannot be a function, and a function is what Lean expects here. This is often the result of a typo or a missing `import` or `open` statement.
[scratch]/V3R1T4SClaim.lean:157:8: error: Failed to rewrite using equation theorems for `psMatrix4`
[scratch]/V3R1T4SClaim.lean:172:6: warning: declaration uses `sorry`
[scratch]/V3R1T4SClaim.lean:185:2: warning: Unused tactic linter: `constructor` does nothing

Note: This linter can be disabled with `set_option linter.unusedTactic false`
[scratch]/V3R1T4SClaim.lean:186:2: warning: Unused tactic linter: `·
  rintro ⟨⟨hA, _⟩, h2, h3⟩
  exact ⟨h3, hA, h2⟩` does nothing

Note: This linter can be disabled with `set_option linter.unusedTactic false`
[scratch]/V3R1T4SClaim.lean:188:2: warning: Unused tactic linter: `·
  rintro ⟨h3, hA, h2⟩
  refine ⟨⟨hA, ?_⟩, h2, h3⟩
  rw [inv_pow, h3, inv_one]` does nothing

Note: This linter can be disabled with `set_option linter.unusedTactic false`
[scratch]/V3R1T4SClaim.lean:185:2: warning: this tactic is never executed

Note: This linter can be disabled with `set_option linter.unreachableTactic false`
[scratch]/V3R1T4SClaim.lean:186:2: warning: this tactic is never executed

Note: This linter can be disabled with `set_option linter.unreachableTactic false`
[scratch]/V3R1T4SClaim.lean:188:2: warning: this tactic is never executed

Note: This linter can be disabled with `set_option linter.unreachableTactic false`

problem: candidate does not compile cleanly
FAIL
```
