# [[122,1]] qubit codes: upper bound on the distance lowered from 41 to 40

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[122,1]] (122 physical qubits encoding 1 logical qubit) had an
upper bound of 41 on the distance. This package proves that no such code has distance 41 or more, so the
upper bound is at most 40. The proof is one exact certificate for the standard weight-enumerator linear program with Rains'
shadow constraints, checked by two separately written checkers. The new bound does not follow from the table's
other entries.

The exact scope, as signed off by the three reviewers:

> The exact integer Farkas certificate object/cert_122_1_41_sh.json, verified by verify-it-yourself/check_cert.py, shows the quantum weight-enumerator LP (A_0=1, sum A_i=2^121, A_j=B_j for 1<=j<=40, A_j<=B_j for j>=41, shadow enumerator nonnegativity) is infeasible for [[122,1,41]], so no qubit stabilizer code [[122,1,41]] exists and the [[122,1]] upper bound is at most 40 against the claim-time table value of 41, and this value is not implied by the propagation rules R1, R2, R3 applied to the claim-time table.
>
> (File paths as in this package. The reviewers' original sentence, which names the claim-folder paths, is under Review record.)

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` after a few seconds. Sample output is in verify-it-yourself/RECEIPTS.md.

## Compared to
M. Grassl, codetables.de, qubit table, cell [[122,1]]: Bounds on [[122,1]] lower bound: 25 upper bound: 41, https://codetables.de/QECC.php?q=4&n=122&k=1, fetched 2026-10-17T00:29:01Z (claim time), HTTP 200,
page sha256 d1b0f2dfad44f149c46c0e3bfd7b947ad837ce5397fbdd71d9cf61d7fb6c599f; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

## Not claimed
- No new code: the lower bound stays 25.
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

## Review record
The reviewers' scope sentence exactly as signed off in panel/gate.md:

> The exact integer Farkas certificate result/cert_122_1_41_sh.json, verified by check/check_cert.py, shows the quantum weight-enumerator LP (A_0=1, sum A_i=2^121, A_j=B_j for 1<=j<=40, A_j<=B_j for j>=41, shadow enumerator nonnegativity) is infeasible for [[122,1,41]], so no qubit stabilizer code [[122,1,41]] exists and the [[122,1]] upper bound is at most 40 against the claim-time table value of 41, and this value is not implied by the propagation rules R1, R2, R3 applied to the claim-time table.
