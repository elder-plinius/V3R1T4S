# Run it yourself (from this folder, fresh shell)

1. Verify the claim (standard library only):
   sh verify-it-yourself/run_checks.sh
   Expected: lines starting with ok, then PASS as the last line.
2. Re-run the saved models (optional; needs a Python 3.12 environment with `numpy ase torch mace-torch jarvis-tools`; CPU is enough):
   MLFF_PYTHON=/path/to/that/python sh verify-it-yourself/run_checks.sh
   Expected: `max |re-run - predictions file| = ... eV/A` at most 1e-6, then PASS.
3. Rebuild the object: see `how-we-built-it/COMMANDS.md` (about 150 epochs per seed at 2 CPU threads; the weights are not bit-for-bit reproducible across machines, so the saved models in `object/` are the object of record).
