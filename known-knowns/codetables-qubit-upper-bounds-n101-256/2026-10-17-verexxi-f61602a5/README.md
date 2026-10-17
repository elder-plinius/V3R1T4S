# [[215,6]] qubit codes: upper bound on the distance lowered from 73 to 71

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[215,6]] (215 physical qubits encoding 6 logical qubits) had an
upper bound of 73 on the distance. This package proves that no such code has distance 72 or more, so the
upper bound is at most 71. The proof is 2 exact certificates (at d = 72 and 73) for the standard weight-enumerator linear program with Rains'
shadow constraints, checked by two separately written checkers. The certificate at d = 73 is the one at d = 72 with the rows for 72 <= j < 73 relabelled from inequalities to equalities (same multipliers, identical coefficients); both checkers verify it on its own. The new bound does not follow from the table's
other entries.

The exact scope, as signed off by the three reviewers:

> The exact integer-checked Farkas certificate (shadow-enhanced quantum weight-enumerator LP) in object/cert_215_6_72_sh.json shows no qubit stabilizer code [[215,6,72]] exists, so the [[215,6]] distance upper bound is at most 71, which is below both the saved claim-time table value 73 and the propagation closure 72 of the saved full table (no claim about lower bounds or any other cell).
>
> (File paths as in this package. The reviewers' original sentence, which names the claim-folder paths, is under Review record.)

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` after a few seconds. Sample output is in verify-it-yourself/RECEIPTS.md.

## Compared to
M. Grassl, codetables.de, qubit table, cell [[215,6]]: Bounds on [[215,6]] lower bound: 41 upper bound: 73, https://codetables.de/QECC.php?q=4&n=215&k=6, fetched 2026-10-17T05:36:07Z (claim time), HTTP 200,
page sha256 d22488ba2d9fc1c2befbcefe60a1b986675815d90d36976d49947ce8efa231c1; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

## Not claimed
- No new code: the lower bound stays 41.
- Not the exact optimum: 71 is the bound this linear program proves, not a proof that a distance-71 code exists.
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

> The exact integer-checked Farkas certificate (shadow-enhanced quantum weight-enumerator LP) in result/cert_215_6_72_sh.json shows no qubit stabilizer code [[215,6,72]] exists, so the [[215,6]] distance upper bound is at most 71, which is below both the saved claim-time table value 73 and the propagation closure 72 of the saved full table (no claim about lower bounds or any other cell).
