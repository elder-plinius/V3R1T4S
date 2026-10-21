# [[115,4]] qubit codes: upper bound on the distance lowered from 39 to 37

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[115,4]] (115 physical qubits encoding 4 logical qubits) had an
upper bound of 39 on the distance. This package proves that no such code has distance 38 or more, so the
upper bound is at most 37. The proof is 2 exact certificates (at d = 38 and 39) for the standard weight-enumerator linear program with Rains'
shadow constraints, checked by two separately written checkers. The certificate at d = 39 is the one at d = 38 with the rows for 38 <= j < 39 relabelled from inequalities to equalities (same multipliers, identical coefficients); both checkers verify it on its own. The new bound does not follow from the table's
other entries.

The exact scope, as signed off by the three reviewers:

> Within the saved claim-time codetables.de table (upper bound 39 for [[115,4]]), exact-integer Farkas certificates of the weight-enumerator LP with shadow constraints rule out qubit stabilizer codes [[115,4,38]] and [[115,4,39]], giving an upper bound of at most 37 that is not implied by propagation from the other saved cells (their closure is 38).

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` after a few seconds. Sample output is in verify-it-yourself/RECEIPTS.md.

A note for reviewers running V3R1T4S's `kit/check_run.py`: its tamper test changes the middle digit of the
first certificate file and warns that the checkers still print PASS. That digit sits deep inside a multiplier
that is hundreds of digits long, so the changed file is still a valid certificate and both checkers are right to
accept it. Changes that break a certificate are rejected: see how-we-built-it/step5_checks.md.

## Compared to
M. Grassl, codetables.de, qubit table, cell [[115,4]]: Bounds on [[115,4]] lower bound: 24 upper bound: 39, https://codetables.de/QECC.php?q=4&n=115&k=4, fetched 2026-10-17T05:35:00Z (claim time), HTTP 200,
page sha256 b40fb6f88b7879f4f6d454220f5c8c5b5ec97ee57e9679a9c492d512ad378f97; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

## Not claimed
- No new code: the lower bound stays 24.
- Not the exact optimum: 37 is the bound this linear program proves, not a proof that a distance-37 code exists.
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
