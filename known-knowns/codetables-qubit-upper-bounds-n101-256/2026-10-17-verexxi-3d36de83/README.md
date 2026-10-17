# [[171,1]] qubit codes: upper bound on the distance lowered from 57 to 55

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[171,1]] (171 physical qubits encoding 1 logical qubit) had an
upper bound of 57 on the distance. This package proves that no such code has distance 56 or more, so the
upper bound is at most 55. The proof is 2 exact certificates (at d = 56 and 57) for the standard weight-enumerator linear program with Rains'
shadow constraints, checked by two separately written checkers. The new bound does not follow from the table's
other entries.

The exact scope, as signed off by the three reviewers:

> No qubit stabilizer code [[171,1,d]] with d >= 56 exists (exact integer Farkas certificates of the quantum weight-enumerator LP with Rains shadow rows verify for d = 56 and for the live bound d = 57 under the shipped checker and my own re-implementation), so the live codetables.de upper bound 57 for [[171,1]] (re-fetched 2026-10-17T00:30:36Z, HTTP 200, byte-identical to the claim-time page) falls to at most 55, which the live table's propagation closure (R1-R3, 57) does not already give; nothing is confirmed about the lower bound 34, the true LP optimum, or any other cell.

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` after a few seconds. Sample output is in verify-it-yourself/RECEIPTS.md.

A note for reviewers running V3R1T4S's `kit/check_run.py`: its tamper test changes the middle digit of the
first certificate file and warns that the checkers still print PASS. That digit sits deep inside a multiplier
that is hundreds of digits long, so the changed file is still a valid certificate and both checkers are right to
accept it. Changes that break a certificate are rejected: see how-we-built-it/step5_checks.md.

## Compared to
M. Grassl, codetables.de, qubit table, cell [[171,1]]: Bounds on [[171,1]] lower bound: 34 upper bound: 57, https://codetables.de/QECC.php?q=4&n=171&k=1, fetched 2026-10-16T21:01:19Z (claim time), HTTP 200,
page sha256 c92ff9802e79dc6a595112491da66a27a8bb2f2fec0d11465d8d55477287c20c; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

## Not claimed
- No new code: the lower bound stays 34.
- Not the exact optimum: 55 is the bound this linear program proves, not a proof that a distance-55 code exists.
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
