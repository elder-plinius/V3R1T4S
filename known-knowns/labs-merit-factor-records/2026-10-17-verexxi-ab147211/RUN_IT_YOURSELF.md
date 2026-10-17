# Run it yourself

From this folder, in a fresh shell (Python 3.8 or newer, standard library only):

    sh verify-it-yourself/run_checks.sh

Expected output: the checker's line `length 380, energy 10058 (F = 7.1784); claimed 10058; best published 10286`, the second
checker's line ending in `380 10058`, then `PASS` (verify-it-yourself/RECEIPTS.md holds the real run).

Rebuild the object: take the parent sequence in how-we-built-it/parent.txt (length 383, from arXiv:2206.12070), apply
the edit described there, and check it:

    python3 verify-it-yourself/check_energy.py "$(cat object/sequence.txt)"

Expected: `380 10058`.
