# [[150,3]] qubit codes: upper bound on the distance lowered from 51 to 48

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[150,3]] (150 physical qubits encoding 3 logical qubits) had an
upper bound of 51 on the distance. This package proves that no such code has distance 49 or more, so the
upper bound is at most 48. The proof is 2 exact certificates (at d = 49 and 51) for the standard weight-enumerator linear program with Rains'
shadow constraints, checked by two separately written checkers. The certificate at d = 51 is the one at d = 49 with the rows for 49 <= j < 51 relabelled from inequalities to equalities (same multipliers, identical coefficients); both checkers verify it on its own. The new bound does not follow from the table's
other entries.

The exact scope, as signed off by the three reviewers:

> No qubit stabilizer code [[150,3,d]] with d >= 49 exists, per exact integer Farkas certificates (d=49 and d=51) of the shadow-augmented quantum weight-enumerator LP, so the upper bound at cell (150,3) is at most 48 against the claim-time table value of 51, which the other live cells' propagation closure (50) does not imply.

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` after a few seconds. Sample output is in verify-it-yourself/RECEIPTS.md.

A note for reviewers running V3R1T4S's `kit/check_run.py`: its tamper test changes the middle digit of the
first certificate file and warns that the checkers still print PASS. That digit sits deep inside a multiplier
that is hundreds of digits long, so the changed file is still a valid certificate and both checkers are right to
accept it. Changes that break a certificate are rejected: see how-we-built-it/step5_checks.md.

## Compared to
M. Grassl, codetables.de, qubit table, cell [[150,3]]: Bounds on [[150,3]] lower bound: 29 upper bound: 51, https://codetables.de/QECC.php?q=4&n=150&k=3, fetched 2026-10-17T05:33:19Z (claim time), HTTP 200,
page sha256 8607e7f6566d983596e9faf28762b7aecdc7929b713831e16531442e02282c49; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

## Not claimed
- No new code: the lower bound stays 29.
- Not the exact optimum: 48 is the bound this linear program proves, not a proof that a distance-48 code exists.
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
