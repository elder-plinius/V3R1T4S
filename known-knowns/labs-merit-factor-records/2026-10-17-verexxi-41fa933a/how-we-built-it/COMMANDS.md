# How the object was made (Python 3, numpy for the scans)

1. `baseline.py` extracts every published LABS row (length, printed energy or merit factor, printed sequence) from the
   fetched sources and decodes the sequences; `repair_dimitrov.py` repairs rows of arXiv:2206.12070 whose printed hex
   does not reproduce the printed merit factor.
2. `seeds.py` takes, for each length, the minimum over every printed value and every decoded sequence (the baseline),
   and the published sequences of nearby lengths as seeds.
3. `multi_edit_scan.py` scans small end edits of those seeds (append, prepend or trim one to three elements), with
   exact energies (`labs_energy.py`).
4. `make_claim.py` builds the claim folder for one length.

For this length: one-element edit (remove 0 element(s) at the start and 1 at the end) of the published L=339 sequence from 2206.12070 (parent: L = 339, energy 7393, from arXiv:2206.12070; see parent.txt). Rebuild it by applying that edit to the
parent sequence in parent.txt and checking the energy with verify-it-yourself/check_energy.py.
