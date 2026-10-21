# [[155,6]] qubit codes: upper bound on the distance lowered from 53 to 49

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[155,6]] (155 physical qubits encoding 6 logical qubits) had an
upper bound of 53 on the distance. This package proves that no such code has distance 50 or more, so the
upper bound is at most 49. The proof is 2 exact certificates (at d = 50 and 53) for the standard weight-enumerator linear program with Rains'
shadow constraints, checked by two separately written checkers. The certificate at d = 53 is the one at d = 50 with the rows for 50 <= j < 53 relabelled from inequalities to equalities (same multipliers, identical coefficients); both checkers verify it on its own. The new bound does not follow from the table's
other entries.

The exact scope, as signed off by the three reviewers:

> No [[155,6,50]] qubit stabilizer code exists, as certified by an exact integer Farkas certificate of the shadow-enhanced quantum weight-enumerator LP, so the [[155,6]] distance upper bound is at most 49, below both the claim-time table value of 53 and the value 50 implied by propagation from other cells.

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` after a few seconds. Sample output is in verify-it-yourself/RECEIPTS.md.

A note for reviewers running V3R1T4S's `kit/check_run.py`: its tamper test changes the middle digit of the
first certificate file and warns that the checkers still print PASS. That digit sits deep inside a multiplier
that is hundreds of digits long, so the changed file is still a valid certificate and both checkers are right to
accept it. Changes that break a certificate are rejected: see how-we-built-it/step5_checks.md.

## Compared to
M. Grassl, codetables.de, qubit table, cell [[155,6]]: Bounds on [[155,6]] lower bound: 29 upper bound: 53, https://codetables.de/QECC.php?q=4&n=155&k=6, fetched 2026-10-17T05:33:08Z (claim time), HTTP 200,
page sha256 e0ff2386821f97a34869e168505b4c44ad81d206438f980d66468f9660a105e6; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

## Not claimed
- No new code: the lower bound stays 29.
- Not the exact optimum: 49 is the bound this linear program proves, not a proof that a distance-49 code exists.
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
