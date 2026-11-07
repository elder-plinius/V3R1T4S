# How the object was built

The object is a hand-written Lean proof, developed by compiling Lean files against a local Physlib build at
be0f21e5002d6d73b87f2055530c1e8bf7151546 (Lean v4.34.1). In the run, every Lean command went through a small
wrapper that limits concurrent Lean processes to two (memory); it does not change any check.

Files here:
- `PREREG.md`: the run's pre-registration (statement, checker and criterion frozen before any attempt).
- `code/numcheck.py` and `out/numcheck.txt`: the numerical sanity check run before any Lean (standard library).
- `lean/Fidelity.lean`: the frozen `inclSMMatrix` written out entry by entry, and `gaugeGroupℤ₆OfRoot (-1) ≠ 1`
  (compiled with no output).
- `lean/EmbedZ6.lean` and `out/EmbedZ6.txt`: bonus, the induced injective hom `StandardModel.GaugeGroupℤ₆ →* SU(5)`
  (Physlib's informal `embedSMℤ₆`). It imports the compiled object as module `V3R1T4SClaim`; not reviewed by the
  panel.
- `checker_output.txt`: the run's checker on the object (06:29–06:30 UTC), last line PASS.

Commands used in the run, with `$WORKDIR` the workspace and `$PHYSLIB` the Physlib checkout (the second from the
run folder, whose `checker/` holds the same two files as `verify-it-yourself/`):

```sh
python3 attempts/kernel-first/code/numcheck.py
python3 -I checker/lean_claim_check.py --physlib "$PHYSLIB" \
  --spec checker/spec_inclSM_ker.lean --candidate attempts/kernel-first/result/claim.lean
cd "$PHYSLIB" && lake env lean "$WORKDIR/runs/2026-10-14-0616/attempts/kernel-first/lean/Fidelity.lean"
```
