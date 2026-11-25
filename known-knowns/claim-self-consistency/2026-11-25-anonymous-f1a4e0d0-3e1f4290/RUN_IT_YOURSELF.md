# Run it yourself (fresh shell, from this package folder)
sh verify-it-yourself/run_checks.sh
Expected output: see verify-it-yourself/RECEIPTS.md; last line PASS.
Rebuild the numbers: cd how-we-built-it && python3 check_bound.py && python3 eval3d.py (needs mpmath, numpy, scipy;
versions in how-we-built-it/COMMANDS.md); compare with check_bound_output.txt and eval3d_output.txt.
The proof is object/PROOF.md (every step labelled).
