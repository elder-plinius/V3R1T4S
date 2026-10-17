# [[145,1]] qubit codes: upper bound on the distance lowered from 49 to 47

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[145,1]] (145 physical qubits encoding 1 logical qubit)
had an upper bound of 49 on the distance. This package proves that no such code has distance 48 or 49, so
the upper bound is at most 47. The proof is two exact certificates for the standard weight-enumerator linear
program with Rains' shadow constraints, checked by two separately written checkers. The new bound does not
follow from the table's other entries.

The exact scope, as signed off by the three reviewers:

> For qubit stabilizer codes of length 145 and dimension 1, exact integer Farkas certificates of the quantum weight-enumerator LP with MacWilliams link, A_j = B_j below d, A_j <= B_j from d, and shadow nonnegativity, which I re-verified with the claimant's checker and my own re-implementation, show that no [[145,1,d]] code exists for any d >= 48, so the upper bound of the table cell (145,1) (recorded as 49) lowers to at most 47, and the propagation closure of the recorded live table at that cell is 49, so this is not implied by other recorded cells.

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` after a few seconds. Sample output is in verify-it-yourself/RECEIPTS.md.

## Compared to
M. Grassl, codetables.de, qubit table, cell [[145,1]]: Bounds on [[145,1]] lower bound: 33 upper bound: 49, https://codetables.de/QECC.php?q=4&n=145&k=1, fetched 2026-10-16T19:43:57Z (claim time), HTTP 200,
page sha256 50d08374d09ec79d0a120e630b25db0ffb33ea0151e4594074ba26392a64bf77; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

## Not claimed
- No new code: the lower bound stays 33.
- Not the exact optimum: 47 is the bound this linear program proves, not a proof that a distance-47 code exists.
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
