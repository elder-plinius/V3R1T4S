# [[125,4]] qubit codes: upper bound on the distance lowered from 41 to 40

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[125,4]] (125 physical qubits encoding 4 logical qubits) had an
upper bound of 41 on the distance. This package proves that no such code has distance 41 or more, so the
upper bound is at most 40. The proof is one exact certificate for the standard weight-enumerator linear program with Rains'
shadow constraints, checked by two separately written checkers. The new bound does not follow from the table's
other entries.

The exact scope, as signed off by the three reviewers:

> There is no qubit stabilizer code [[125,4,41]] (certificate: quantum weight-enumerator LP with Rains shadow constraints, verified in exact integer arithmetic), so the [[125,4]] upper bound drops from 41 to at most 40, and 41 is not implied by rules R1, R2, R3 applied to the saved complete table of 2026-10-17.

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` after a few seconds. Sample output is in verify-it-yourself/RECEIPTS.md.

## Compared to
M. Grassl, codetables.de, qubit table, cell [[125,4]]: Bounds on [[125,4]] lower bound: 24 upper bound: 41, https://codetables.de/QECC.php?q=4&n=125&k=4, fetched 2026-10-17T00:29:19Z (claim time), HTTP 200,
page sha256 7907ff3b963f3557d2fa6f91d771451aad2666cbfe77e64b50136c843412b3ea; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

## Not claimed
- No new code: the lower bound stays 24.
- Not the exact optimum: 40 is the bound this linear program proves, not a proof that a distance-40 code exists.
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
