# [[207,2]] qubit codes: upper bound on the distance lowered from 69 to 68

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[207,2]] (207 physical qubits encoding 2 logical qubits) had an
upper bound of 69 on the distance. This package proves that no such code has distance 69 or more, so the
upper bound is at most 68. The proof is one exact certificate for the standard weight-enumerator linear program with Rains'
shadow constraints, checked by two separately written checkers. The new bound does not follow from the table's
other entries.

The exact scope, as signed off by the three reviewers:

> Within the saved claim-time codetables.de qubit table (cell [[207,2]], lower bound 40, upper bound 69), an exact integer Farkas certificate of the quantum weight-enumerator LP with Rains shadow constraints shows no [[207,2,69]] stabilizer code exists, and propagation over the saved full table (rules d(n,k)<=d(n,k-1), d(n,k)<=d(n+1,k), d(n,k)<=d(n-1,k+1)+1) gives 69 at (207,2), so the 68 bound is not implied by other saved cells.

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` after a few seconds. Sample output is in verify-it-yourself/RECEIPTS.md.

## Compared to
M. Grassl, codetables.de, qubit table, cell [[207,2]]: Bounds on [[207,2]] lower bound: 40 upper bound: 69, https://codetables.de/QECC.php?q=4&n=207&k=2, fetched 2026-10-17T00:30:22Z (claim time), HTTP 200,
page sha256 2031783a4262d0c0dbdb194134442768e220fa63562ed315766175aa1b40f150; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

## Not claimed
- No new code: the lower bound stays 40.
- Not the exact optimum: 68 is the bound this linear program proves, not a proof that a distance-68 code exists.
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
