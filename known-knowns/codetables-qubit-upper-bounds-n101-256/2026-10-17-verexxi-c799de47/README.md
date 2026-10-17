# [[127,2]] qubit codes: upper bound on the distance lowered from 42 to 41

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[127,2]] (127 physical qubits encoding 2 logical qubits) had an
upper bound of 42 on the distance. This package proves that no such code has distance 42 or more, so the
upper bound is at most 41. The proof is one exact certificate for the standard weight-enumerator linear program with Rains'
shadow constraints, checked by two separately written checkers. The new bound does not follow from the table's
other entries.

The exact scope, as signed off by the three reviewers:

> The exact integer Farkas certificate object/cert_127_2_42_sh.json (quantum weight-enumerator LP with A_i<=B_i, A_i=B_i for 0<i<42, and Rains shadow nonnegativity) proves no [[127,2,42]] qubit stabilizer code exists, which lowers the claim-time table upper bound for cell (127,2) from 42 to at most 41, and that bound is not implied by the propagation rules applied to the saved claim-time table.
>
> (File paths as in this package. The reviewers' original sentence, which names the claim-folder paths, is under Review record.)

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` after a few seconds. Sample output is in verify-it-yourself/RECEIPTS.md.

## Compared to
M. Grassl, codetables.de, qubit table, cell [[127,2]]: Bounds on [[127,2]] lower bound: 25 upper bound: 42, https://codetables.de/QECC.php?q=4&n=127&k=2, fetched 2026-10-17T00:29:28Z (claim time), HTTP 200,
page sha256 cae0ee29dc7683f64c5a3c79c55a0bca14dac338465c9840b4105c053ca2b3b1; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

## Not claimed
- No new code: the lower bound stays 25.
- Not the exact optimum: 41 is the bound this linear program proves, not a proof that a distance-41 code exists.
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

## Review record
The reviewers' scope sentence exactly as signed off in panel/gate.md:

> The exact integer Farkas certificate result/cert_127_2_42_sh.json (quantum weight-enumerator LP with A_i<=B_i, A_i=B_i for 0<i<42, and Rains shadow nonnegativity) proves no [[127,2,42]] qubit stabilizer code exists, which lowers the claim-time table upper bound for cell (127,2) from 42 to at most 41, and that bound is not implied by the propagation rules applied to the saved claim-time table.
