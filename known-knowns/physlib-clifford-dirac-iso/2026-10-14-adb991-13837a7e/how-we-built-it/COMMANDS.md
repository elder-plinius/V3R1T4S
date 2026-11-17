# How the object was built

The object is a hand-written Lean proof, developed by compiling Lean files against a local Physlib build at
be0f21e5002d6d73b87f2055530c1e8bf7151546 (Lean v4.34.1). In the run, every Lean command went through a small
wrapper that limits concurrent Lean processes to two (memory); it does not change any check.

Files here:
- `PREREG.md`: the run's pre-registration (statement, checker and criterion frozen before any attempt).
- `code/numcheck.py` and `out/numcheck.txt`: the exact-arithmetic check run before any Lean (standard library).
- `lean/LemmaFinrankClifford.lean`: dim_ℝ Cl(diracForm) = 16 and the dimension-count glue.
- `lean/LemmaFinrankDirac.lean`: the 16 gamma products are ℝ-independent; 16 ≤ dim_ℝ diracAlgebra.
- `lean/FullIsoStandalone.lean`: injectivity plus the isomorphism `KF.cliffordEquivDirac` (not reviewed by the
  panel).
- `checker_output.txt`: the run's checker on the object (06:40 UTC), last line PASS.

Commands used in the run, with `$WORKDIR` the workspace and `$PHYSLIB` the Physlib checkout (the second from the
run folder, whose `checker/` holds the same two files as `verify-it-yourself/`):

```sh
python3 -I attempts/kernel-first/code/numcheck.py
python3 -I checker/lean_claim_check.py --physlib "$PHYSLIB" \
  --spec checker/spec_ofCliffordAlgebra_injective.lean --candidate attempts/kernel-first/result/Candidate.lean
cd "$PHYSLIB" && lake env lean "$WORKDIR/runs/2026-10-14-0615/attempts/kernel-first/code/lean/FullIsoStandalone.lean"
```
