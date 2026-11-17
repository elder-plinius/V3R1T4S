# How the object was built

The object is a hand-written Lean proof, developed on 2026-10-14 by compiling Lean files against a local Physlib build
at be0f21e5002d6d73b87f2055530c1e8bf7151546 (Lean v4.34.1), and re-checked on 2026-10-15 against
76245c854e4827a1dd7f20d1c053b61219cc8fbb. In the run, every Lean command went through a small wrapper that limits
concurrent Lean processes to two (memory); it does not change any check.

Files here:
- `PREREG.md`: the run's pre-registration (statement, checker and criterion frozen before any attempt).
- `code/numeric_check.py` and `out/numeric_check.txt`: the numerical check run before any Lean.
- `lean/Exp2_controls.lean` and `out/exp2_controls.txt`: the controls (kernel ≠ ℤ₆, kernel ≠ ⊥), axioms
  [propext, Classical.choice, Quot.sound]; machine paths in the output are shown as [workdir] and [scratch].

Commands used in the run, with `$WORKDIR` the workspace and `$PHYSLIB` the Physlib checkout (from the run folder,
whose `checker/` holds the same two files as `verify-it-yourself/`):

```sh
python3 attempts/kernel-first/code/numeric_check.py
python3 -I checker/lean_claim_check.py --physlib "$PHYSLIB" \
  --spec checker/spec_patisalam_inclSM_ker.lean --candidate attempts/kernel-first/result/Claim.lean
cd "$PHYSLIB" && lake env lean "$WORKDIR/runs/2026-10-14-0701/attempts/kernel-first/lean/Exp2_controls.lean"
```
