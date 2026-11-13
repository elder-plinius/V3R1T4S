# Run it yourself (from this package folder, fresh shell)

1. Verify the claim (stdlib only, ~15-30 min):
       sh verify-it-yourself/run_checks.sh
   Expected last line: PASS. (Receipts from our run:
   verify-it-yourself/RECEIPTS.md.)

2. Rebuild the object from the two independent residue records:
       python3 how-we-built-it/final_gate.py
   (expects the workspace layout of the producing run; in this package the
   same CRT logic runs inside verify_row29.py steps 2/3 — the standalone
   form is the authoritative in-package path.)

3. Growth check (needs numpy):
       python3 how-we-built-it/growth_row29.py object-as-json
   The frozen test: fit ln T/(mn) = lnW - c/(mn) on published rows 26-27;
   every claimed root within max(1e-5, 3*max residual) of the fit and below
   Finch's W = 1.9402139258. Our run: W = 1.9318762, worst claimed-cell
   deviation 1.19e-3, PASS.

4. How the numbers were produced: how-we-built-it/COMMANDS.md (two runs:
   left-to-right row sweeps over 22 set-A29 primes; right-to-left sweeps
   over 22 disjoint set-B29 primes; sliced fast DP for k=27/28).
