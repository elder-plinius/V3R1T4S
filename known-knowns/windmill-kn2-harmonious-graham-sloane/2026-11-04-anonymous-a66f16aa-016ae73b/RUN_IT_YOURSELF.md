# Reproduction

From the package root, run `python verify-it-yourself/check.py`, or `sh verify-it-yourself/run_checks.sh`. Python and PowerShell must already be on PATH. No additional libraries are used. The exact scientific check is complete clique enumeration at n=10, not reading saved numbers alone. Expected deterministic counts: nodes 91726677, leaves 1702800, masks 1571472, complement_pairs 0; status COMPLETE and found false. The last line is PASS. A cap, exception, incomplete search, or mismatch is FAIL.

## Rebuild the two original computations

Use a fresh PowerShell process for each command. Create a new writable output directory outside the package. From the package root, for example:

```powershell
New-Item -ItemType Directory -Path ../n10-reproduction-output -ErrorAction Stop
pwsh -NoProfile -File how-we-built-it/method1/run-optimized.ps1 -N 10 -CapSeconds 600 -MemoryCapMiB 2048 -OutputPrefix ../n10-reproduction-output/complement
New-Item -ItemType Directory -Path how-we-built-it/output -ErrorAction Stop
pwsh -NoProfile -File how-we-built-it/method2/run.ps1 -N 10 -CapSeconds 600 -Tag reproduced-n10
```

The direct wrapper uses `how-we-built-it/output/`; run these reconstruction commands in a writable copy. Do not treat these generated files as part of the frozen package. The complemented method must finish all roots 1..81 with exhaustive_no_pair, 1702800 leaves, and 1571472 distinct masks. The direct result must say found:false, range_complete:true, full_domain:true, timed_out:false. Any partial output is inconclusive. Sources are byte-for-byte copies of the independently reviewed programs; commands only select n=10 and sufficient limits.

`object/receipts/` holds the original scientific outputs with only local process identifiers omitted. Counts, completion flags, timings and UTC research timestamps are retained. The original independent checker source is unchanged. The original preregistration is included. No calibration case needs rerunning to validate this package.
