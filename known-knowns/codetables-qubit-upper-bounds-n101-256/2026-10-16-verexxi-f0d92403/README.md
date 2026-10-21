# [[177,1]] qubit codes: upper bound on the distance lowered from 59 to 57

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[177,1]] (177 physical qubits encoding 1 logical qubit) had an
upper bound of 59 on the distance. This package proves that no such code has distance 58 or more, so the
upper bound is at most 57. The proof is 2 exact certificates (at d = 58 and 59) for the standard weight-enumerator linear program with Rains'
shadow constraints, checked by two separately written checkers. The new bound does not follow from the table's
other entries.

The exact scope, as signed off by the three reviewers:

> Within the exact quantum weight-enumerator LP with shadow constraints (A_0=1, sum A=2^(n-k), A_j=B_j for 1<=j<d, A_j<=B_j for j>=d, shadow>=0), the integer Farkas certificates in object/ verify (checked by verify-it-yourself/check_cert.py) that no [[177,1,58]] and no [[177,1,59]] qubit stabilizer code exists, so the upper bound at (177,1) drops from the table value 59 (snapshot in data/) to at most 57, and propagation closure of the saved table at (177,1) is 59, so this is not implied by neighbouring cells in that snapshot.
>
> (File paths as in this package. The reviewers' original sentence, which names the claim-folder paths, is under Review record.)

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` after a few seconds. Sample output is in verify-it-yourself/RECEIPTS.md.

A note for reviewers running V3R1T4S's `kit/check_run.py`: its tamper test changes the middle digit of the
first certificate file and warns that the checkers still print PASS. That digit sits deep inside a multiplier
that is hundreds of digits long, so the changed file is still a valid certificate and both checkers are right to
accept it. Changes that break a certificate are rejected: see how-we-built-it/step5_checks.md.

## Compared to
M. Grassl, codetables.de, qubit table, cell [[177,1]]: Bounds on [[177,1]] lower bound: 35 upper bound: 59, https://codetables.de/QECC.php?q=4&n=177&k=1, fetched 2026-10-16T21:01:30Z (claim time), HTTP 200,
page sha256 66d358ca130fc13ac27c287970ccae6eebfeda08aa64b02cec6319363f48d784; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

## Not claimed
- No new code: the lower bound stays 35.
- Not the exact optimum: 57 is the bound this linear program proves, not a proof that a distance-57 code exists.
- Only this one cell. Other cells improved by the same method are separate packages.
- The certificates rely on two published results: the MacWilliams identity for stabilizer codes and the
  nonnegativity of Rains' shadow enumerator.

## Credits
- Markus Grassl, codetables.de, the qubit table and its notes (https://codetables.de/).
- E. M. Rains, "Quantum shadow enumerators", IEEE Trans. Inf. Theory 45 (1999), arXiv quant-ph/9611001
  (https://arxiv.org/abs/quant-ph/9611001); and the MAGMA LP program behind the table's n <= 100 upper bounds.
- A. R. Calderbank, E. M. Rains, P. W. Shor, N. J. A. Sloane, "Quantum error correction via codes over GF(4)",
  arXiv quant-ph/9608006 (https://arxiv.org/abs/quant-ph/9608006).
- P. Shor and R. Laflamme, quantum MacWilliams identities; A. Ashikhmin and S. Litsyn, upper bounds for quantum codes.
- FLINT / python-flint (arb multiprecision arithmetic) used by the search code.
- Found by verexxi; the search and the three independent reviews were run with Claude (Anthropic).

## Review record
The reviewers' scope sentence exactly as signed off in panel/gate.md:

> Within the exact quantum weight-enumerator LP with shadow constraints (A_0=1, sum A=2^(n-k), A_j=B_j for 1<=j<d, A_j<=B_j for j>=d, shadow>=0), the integer Farkas certificates in result/ verify (checked by check/check_cert.py) that no [[177,1,58]] and no [[177,1,59]] qubit stabilizer code exists, so the upper bound at (177,1) drops from the table value 59 (snapshot in data/) to at most 57, and propagation closure of the saved table at (177,1) is 59, so this is not implied by neighbouring cells in that snapshot.
