# [[154,1]] qubit codes: upper bound on the distance lowered from 52 to 50

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[154,1]] (154 physical qubits encoding 1 logical qubit)
had an upper bound of 52 on the distance. This package proves that no such code has distance 51 or 52, so
the upper bound is at most 50. The proof is two exact certificates for the standard weight-enumerator linear
program with Rains' shadow constraints, checked by two separately written checkers. The new bound does not
follow from the table's other entries.

The exact scope, as signed off by the three reviewers:

> In the saved codetables.de record (cell [[154,1]], lower 33, upper 52, plus the saved full qubit table whose propagation closure at (154,1) is 52), two integer Farkas certificates (d=52 and d=51, with Rains shadow constraints) pass both the claimant's exact checker and my independent integer re-implementation, so no [[154,1,d]] stabilizer code with d >= 51 exists under the quantum weight-enumerator LP, lowering the table upper bound from 52 to 50 and not implied by the stated propagation rules, with live freshness resting on the recorded fetch timestamps.

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` after a few seconds. Sample output is in verify-it-yourself/RECEIPTS.md.

## Compared to
M. Grassl, codetables.de, qubit table, cell [[154,1]]: Bounds on [[154,1]] lower bound: 33 upper bound: 52, https://codetables.de/QECC.php?q=4&n=154&k=1, fetched 2026-10-16T19:44:15Z (claim time), HTTP 200,
page sha256 beef68a113abb7963fdb5df6a47650868541d2a4d57c41b02dc8d8f46ed7d4a5; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

## Not claimed
- No new code: the lower bound stays 33.
- Not the exact optimum: 50 is the bound this linear program proves, not a proof that a distance-50 code exists.
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
