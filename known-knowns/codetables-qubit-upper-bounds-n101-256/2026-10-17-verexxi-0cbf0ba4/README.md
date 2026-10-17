# [[155,3]] qubit codes: upper bound on the distance lowered from 53 to 50

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[155,3]] (155 physical qubits encoding 3 logical qubits) had an
upper bound of 53 on the distance. This package proves that no such code has distance 51 or more, so the
upper bound is at most 50. The proof is 2 exact certificates (at d = 51 and 53) for the standard weight-enumerator linear program with Rains'
shadow constraints, checked by two separately written checkers. The certificate at d = 53 is the one at d = 51 with the rows for 51 <= j < 53 relabelled from inequalities to equalities (same multipliers, identical coefficients); both checkers verify it on its own. The new bound does not follow from the table's
other entries.

The exact scope, as signed off by the three reviewers:

> No qubit stabilizer code [[155,3,d]] with d >= 51 exists, shown by an exact integer-checked Farkas certificate (quantum weight-enumerator LP with Rains shadow constraints) in object/cert_155_3_51_sh.json, so the [[155,3]] upper bound drops from the saved claim-time table value of 53 to at most 50, below the propagation closure of 52 from the other saved table cells.
>
> (File paths as in this package. The reviewers' original sentence, which names the claim-folder paths, is under Review record.)

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` after a few seconds. Sample output is in verify-it-yourself/RECEIPTS.md.

## Compared to
M. Grassl, codetables.de, qubit table, cell [[155,3]]: Bounds on [[155,3]] lower bound: 30 upper bound: 53, https://codetables.de/QECC.php?q=4&n=155&k=3, fetched 2026-10-17T05:33:30Z (claim time), HTTP 200,
page sha256 ad092d4b904c89212e0de366657e1b97a07d53fd7f0aa4ed045a48ca892fcfba; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

## Not claimed
- No new code: the lower bound stays 30.
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

## Review record
The reviewers' scope sentence exactly as signed off in panel/gate.md:

> No qubit stabilizer code [[155,3,d]] with d >= 51 exists, shown by an exact integer-checked Farkas certificate (quantum weight-enumerator LP with Rains shadow constraints) in result/cert_155_3_51_sh.json, so the [[155,3]] upper bound drops from the saved claim-time table value of 53 to at most 50, below the propagation closure of 52 from the other saved table cells.
