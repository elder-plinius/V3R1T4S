# [[165,6]] qubit codes: upper bound on the distance lowered from 53 to 52

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[165,6]] (165 physical qubits encoding 6 logical qubits) had an
upper bound of 53 on the distance. This package proves that no such code has distance 53 or more, so the
upper bound is at most 52. The proof is one exact certificate for the standard weight-enumerator linear program with Rains'
shadow constraints, checked by two separately written checkers. The new bound does not follow from the table's
other entries.

The exact scope, as signed off by the three reviewers:

> Working only from the saved claim-time records (the [[165,6]] cell page showing lower bound 31 and upper bound 53, and the complete qubit-table snapshot) and without any live re-fetch by me, the supplied integer Farkas certificate for the shadow-augmented quantum weight-enumerator LP at n=165, k=6, d=53 verifies in exact integer arithmetic under both the shipped checker and my own independent re-implementation, which proves that no [[165,6,d]] qubit stabilizer code with d at least 53 exists (upper bound at most 52, one below the recorded 53), and the bound 52 cannot be derived from any other cell of that snapshot by the three listed propagation rules (the closure of the other live cells at (165,6) is 53).

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` after a few seconds. Sample output is in verify-it-yourself/RECEIPTS.md.

A note for reviewers running V3R1T4S's `kit/check_run.py`: its tamper test changes the middle digit of the
first certificate file and warns that the checkers still print PASS. That digit sits deep inside a multiplier
that is hundreds of digits long, so the changed file is still a valid certificate and both checkers are right to
accept it. Changes that break a certificate are rejected: see how-we-built-it/step5_checks.md.

## Compared to
M. Grassl, codetables.de, qubit table, cell [[165,6]]: Bounds on [[165,6]] lower bound: 31 upper bound: 53, https://codetables.de/QECC.php?q=4&n=165&k=6, fetched 2026-10-17T00:30:04Z (claim time), HTTP 200,
page sha256 2ab973981689cd1731fa749a17b6cc4d48c6eb1e956fbc0658ef732dcdc33bb2; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

## Not claimed
- No new code: the lower bound stays 31.
- Not the exact optimum: 52 is the bound this linear program proves, not a proof that a distance-52 code exists.
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
