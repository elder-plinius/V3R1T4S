# [[213,2]] qubit codes: upper bound on the distance lowered from 71 to 70

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[213,2]] (213 physical qubits encoding 2 logical qubits) had an
upper bound of 71 on the distance. This package proves that no such code has distance 71 or more, so the
upper bound is at most 70. The proof is one exact certificate for the standard weight-enumerator linear program with Rains'
shadow constraints, checked by two separately written checkers. The new bound does not follow from the table's
other entries.

The exact scope, as signed off by the three reviewers:

> No qubit stabilizer code [[213,2,71]] exists (certified by an exact integer Farkas certificate of the weight-enumerator LP with Rains shadow constraints), so the upper bound for the qubit cell [[213,2]] is at most 70 against a claim-time table upper bound of 71, and this value is not implied by the table's other cells under the rules R1, R2 and R3.

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` after a few seconds. Sample output is in verify-it-yourself/RECEIPTS.md.

## Compared to
M. Grassl, codetables.de, qubit table, cell [[213,2]]: Bounds on [[213,2]] lower bound: 41 upper bound: 71, https://codetables.de/QECC.php?q=4&n=213&k=2, fetched 2026-10-17T00:30:30Z (claim time), HTTP 200,
page sha256 c8103c8f467704c8f0910e189f0f57a234c1aea949b5179099202c52e2a83236; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

## Not claimed
- No new code: the lower bound stays 41.
- Not the exact optimum: 70 is the bound this linear program proves, not a proof that a distance-70 code exists.
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
