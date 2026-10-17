# Run it yourself

From this folder, in a fresh shell (Python 3.8 or newer, standard library only):

    sh verify-it-yourself/run_checks.sh

Expected output: the checker's line `length 252, energy 3534 (F = 8.9847); claimed 3534; best published 3738`, the second
checker's line ending in `252 3534`, then `PASS` (verify-it-yourself/RECEIPTS.md holds the real run).

Rebuild the object: take the parent sequence in how-we-built-it/parent.txt (length 253, from arXiv:2011.00068), apply
the edit described there, and check it:

    python3 verify-it-yourself/check_energy.py "$(cat object/sequence.txt)"

Expected: `252 3534`.
