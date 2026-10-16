# Run it yourself

From this folder, in a fresh shell (Python 3.8 or newer, standard library only):

    sh verify-it-yourself/run_checks.sh

Expected output: the checker's line `length 328, energy 7148 (F = 7.5255); claimed 7148; best published 7444`, the second
checker's line ending in `328 7148`, then `PASS` (verify-it-yourself/RECEIPTS.md holds the real run).

Rebuild the object: take the parent sequence in how-we-built-it/parent.txt (length 327, from arXiv:2206.12070), apply
the edit described there, and check it:

    python3 verify-it-yourself/check_energy.py "$(cat object/sequence.txt)"

Expected: `328 7148`.
