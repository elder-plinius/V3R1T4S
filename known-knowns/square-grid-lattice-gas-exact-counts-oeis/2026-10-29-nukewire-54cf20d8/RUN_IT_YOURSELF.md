# RUN_IT_YOURSELF — from this package folder in a fresh shell

1. Standalone check (Python 3.8+, standard library only, ~4 min):

   sh verify-it-yourself/run_checks.sh

   Expected: reproduces published terms exactly; last line PASS
   (receipts in verify-it-yourself/RECEIPTS.md from the packaging run).

2. The object: object/a28_value.txt — the 222-digit integer a(28).

3. Rebuild the object from scratch (needs numpy + sympy; ~4-6 h of compute):
   - how-we-built-it/mdp_dp_rowmajor.py — Run A's row-major DP (n=28 mod p per prime)
   - how-we-built-it/mdp_dp_col.py + run_n28B.py — Run B's column sweep
   - CRT each run's 21 residues (prime lists in the run folders referenced by
     object/runA_crt.json / runB_crt.json); the two CRT results must be identical.
   - how-we-built-it/exact_gate.py — the exact n=21..27 reproduction gate.
   The full residue records, logs, and PREREGs are preserved in the source run folders:
   runs/2026-10-27-0735 (Run A), runs/2026-10-28-0734 (Run B), runs/2026-10-29-0733
   (panel + gate), runs/2026-10-29-1031 (n=27 gate completion) under the submitting
   workspace.
