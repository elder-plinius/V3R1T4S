# Y reproduce (scu N=507)

## Findings
- `verify-it-yourself/run_checks.sh` (run from a /tmp copy, cores 4-7): PASS. The sha256 of `object/scu507_refined.txt` and `the-record-we-beat/scu507-posted.txt` both match `verify-it-yourself/CLAIM.json`.
- Independent recompute (my own mpmath at 50 digits; numpy prefilters the near-minimal pairs, then those pairs are recomputed exactly; wall term over all 507 centres):
  - posted `the-record-we-beat/scu507-posted.txt`: 507 centres, r* = 0.06592835801358237207291462, r* - cell = -3.7611868e-6. This matches the claim's -3.761186769e-6 in `RUN_IT_YOURSELF.md`.
  - `object/scu507_refined.txt`: 507 centres, r* = 0.06592848603610355706993808, which matches the CLAIM prefix 0.06592848603610355706. r* - cell = -3.633e-6, so the object also falls short of the cell.
- Cell value 0.065932119200351706079281328718 is taken from `the-record-we-beat/SNAPSHOT.md` and `CLAIM.json`. I did not re-fetch it live, so it was not checked independently.
- `how-we-built-it/` (mp_recheck.py, hunt3.py), which `RUN_IT_YOURSELF.md` refers to, is not in the package, so steps 1 and 2 there cannot be run.
- Conclusion: the stated numbers reproduce. The posted coordinates reach r* about 3.76e-6 below the table cell, well beyond the 1e-9 margin.

context: executor subagent, fresh context
pass: true
