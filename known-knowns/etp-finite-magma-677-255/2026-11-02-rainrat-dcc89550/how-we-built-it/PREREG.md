# Pre-Registration — `etp-finite-magma-677-255`

- Frozen at (UTC): `2026-11-01T16:44:38Z`
- Target ID: `etp-finite-magma-677-255`
- null_test: not needed because any claim on this target is either an explicit finite magma operation table checked deterministically against the equational laws (`check_etp.py` and Lean `decide`), an exhaustive SAT/DRAT UNSAT certificate checked deterministically, or a machine-checked Lean 4 formal theorem compiled by the Lean kernel at the pinned ETP toolchain (`leanprover/lean4:v4.29.1`) with `#print axioms` showing only standard axioms (`propext`, `Classical.choice`, `Quot.sound`) and zero `sorry`.

## Binding Success Criterion (verbatim from `repo/bank/targets.json`)

Success means, for one of the implications listed with 'no proof' on https://teorth.github.io/equational_theories/dashboard/ (finite graph, re-fetched live immediately before claiming, and still 'unknown' in raw_data/finite_outcomes.json.gz): EITHER an explicit finite magma (operation table) that satisfies the hypothesis law and violates the conclusion, verified by an independent exhaustive Python check AND a Lean `decide` proof compiled in the ETP repository at its pinned toolchain; OR a Lean proof of the finite implication, sorry-free, no new axioms, `#print axioms` only propext/Classical.choice/Quot.sound.

## Enumerated Partial Wins (verbatim from `repo/bank/targets.json`)

- `p1`: Exhaustive exclusion of counterexamples up to a new size bound beyond any bound documented in the ETP paper, blueprint or issues for that implication (for 677 => 255 this means excluding order 11 or more, since issue #1464 claims order 10), with a reproducible SAT/DRAT certificate per size and the symmetry-breaking argument written out.
- `p2`: A Lean proof of the implication under an additional natural hypothesis (e.g. the magma is a quasigroup, or left-cancellative) that is neither implied by nor equivalent to a hypothesis already proved in the ETP issues (e.g. the translation-conjugacy closure of issue #1517), stated as a separate theorem.

## Verification & Thresholds Frozen Before Measurement

1. **For a full proof or `p2` conditional Lean proof**:
   - Must compile cleanly under ETP's pinned toolchain `leanprover/lean4:v4.29.1` importing `equational_theories.Equations.All` (and `equational_theories.ManuallyProved.Equation677`).
   - Zero `sorry`, zero `admit`, no `native_decide`, and `#print axioms` on every claimed theorem must contain only a subset of `{propext, Classical.choice, Quot.sound}`.
   - For `p2`, we additionally require a rigorous proof (and/or explicit finite magma models verified by `check_etp.py` and Lean `decide`) demonstrating that the additional natural hypothesis is **neither implied by nor equivalent to** any hypothesis already proved in the ETP repository (`Equation677.lean` fixer-existence equivalents) or ETP issues (`#1464` right-orbit idempotence lemma; `#1517`/`#1518` left-translation conjugacy closure).
2. **For a finite counterexample**:
   - Must pass `python3 check_etp.py <table.json>` (`COUNTEREXAMPLE_CHECK: PASS`) AND compile a `decide` refutation theorem in Lean 4.29.1 without `native_decide`.
3. **For `p1` (exhaustive finite exclusion beyond documented bounds)**:
   - Must exclude all counterexamples up to a new size bound (`n >= 11` for `677 => 255`), with a complete written symmetry-breaking proof and a verified DRAT/LRAT UNSAT certificate for every case.
