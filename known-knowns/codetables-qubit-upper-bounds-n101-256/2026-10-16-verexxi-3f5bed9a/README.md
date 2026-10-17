# [[139,1]] qubit codes: upper bound on the distance lowered from 47 to 45

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[139,1]] (139 physical qubits encoding 1 logical qubit)
had an upper bound of 47 on the distance. This package proves that no such code has distance 46 or 47, so
the upper bound is at most 45. The proof is two exact certificates for the standard weight-enumerator linear
program with Rains' shadow constraints, checked by two separately written checkers. The new bound does not
follow from the table's other entries.

The exact scope, as signed off by the three reviewers:

> The exact-integer Farkas certificates for the quantum weight-enumerator LP (with Rains shadow nonnegativity, and with only the criterion's listed constraints) verify for [[139,1,46]] and for [[139,1,47]], so there is no additive qubit [[139,1,d]] code for d >= 46 and the codetables.de upper bound for [[139,1]], which was 47 at the recorded fetch of 2026-10-16T19:43Z, can be lowered to at most 45, and the closure of the other live cells under the stated propagation rules at (139,1) is 47, so this is not implied by them.

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` after a few seconds. Sample output is in verify-it-yourself/RECEIPTS.md.

## Compared to
M. Grassl, codetables.de, qubit table, cell [[139,1]]: Bounds on [[139,1]] lower bound: 29 upper bound: 47, https://codetables.de/QECC.php?q=4&n=139&k=1, fetched 2026-10-16T19:43:49Z (claim time), HTTP 200,
page sha256 22fe191aa3c3310d48d62cbf7e88640b2110cce4e0842998fb73e796bf75ba2e; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

## Not claimed
- No new code: the lower bound stays 29.
- Not the exact optimum: 45 is the bound this linear program proves, not a proof that a distance-45 code exists.
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
