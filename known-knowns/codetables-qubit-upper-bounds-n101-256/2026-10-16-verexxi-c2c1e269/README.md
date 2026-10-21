# [[164,1]] qubit codes: upper bound on the distance lowered from 55 to 53

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[164,1]] (164 physical qubits encoding 1 logical qubit)
had an upper bound of 55 on the distance. This package proves that no such code has distance 54 or 55, so
the upper bound is at most 53. The proof is two exact certificates for the standard weight-enumerator linear
program with Rains' shadow constraints, checked by two separately written checkers. The new bound does not
follow from the table's other entries.

The exact scope, as signed off by the three reviewers:

> Within the stored 2026-10-16 codetables.de snapshot (upper bound 55 for qubit cell (164,1), closure of the propagation rules R1-R3 over that snapshot also 55), integer-multiplier Farkas certificates for d = 54 and d = 55 were verified exactly by two independent scripts, so the quantum weight-enumerator LP with MacWilliams, A_j = B_j for 0 < j < d, A_j <= B_j and shadow nonnegativity is infeasible and no [[164,1,54]] or [[164,1,55]] stabilizer code exists, which lowers that cell's upper bound from 55 to 53 and is not implied by other cells of that snapshot.

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` after a few seconds. Sample output is in verify-it-yourself/RECEIPTS.md.

## Compared to
M. Grassl, codetables.de, qubit table, cell [[164,1]]: Bounds on [[164,1]] lower bound: 33 upper bound: 55, https://codetables.de/QECC.php?q=4&n=164&k=1, fetched 2026-10-16T19:44:32Z (claim time), HTTP 200,
page sha256 05af667ae6d87dc678a5e544b752ab7fa3c57ed28cbeca31608a71766b2ab1d8; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

## Not claimed
- No new code: the lower bound stays 33.
- Not the exact optimum: 53 is the bound this linear program proves, not a proof that a distance-53 code exists.
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
