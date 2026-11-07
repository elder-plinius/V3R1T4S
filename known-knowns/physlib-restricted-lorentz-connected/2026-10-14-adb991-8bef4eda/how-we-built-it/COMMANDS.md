# How the object was built

The object is a hand-written Lean proof, developed by compiling Lean files against a local Physlib build at
be0f21e5002d6d73b87f2055530c1e8bf7151546 (Lean v4.34.1). In the run, every Lean command went through a small
wrapper that limits concurrent Lean processes to two (memory); it does not change any check.

Files here:
- `PREREG.md`: the run's pre-registration (statement, checker and criterion frozen before any attempt).
- `lean/ExplicitPath.lean`: the development file. It is the object without the final `V3R1T4S.claim` line, with
  `#print axioms` lines instead; `out/explicitpath_run2.txt` is its output.
- `checker_output_C.txt`: the run's checker on the object (06:55 UTC), last line PASS.
- `upstream/RestrictedConnected.lean`: a module-style draft for Physlib (not reviewed by the panel);
  `out/upstream_audit.txt` is its axiom audit.

Commands used in the run, with `$WORKDIR` the workspace and `$PHYSLIB` the Physlib checkout:

```sh
cd "$PHYSLIB" && lake env lean "$WORKDIR/runs/2026-10-14-0608/attempts/construct-space/lean/ExplicitPath.lean"
python3 -I checker/lean_claim_check.py --physlib "$PHYSLIB" \
  --spec checker/spec_restricted_isConnected.lean --candidate attempts/construct-space/result/alt/CandidateC_explicitPath.lean
```

(the second from the run folder; `checker/` there holds the same two files as `verify-it-yourself/`).
