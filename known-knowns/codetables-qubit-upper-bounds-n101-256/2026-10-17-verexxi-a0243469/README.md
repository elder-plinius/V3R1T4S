# [[173,2]] qubit codes: upper bound on the distance lowered from 59 to 56

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[173,2]] (173 physical qubits encoding 2 logical qubits) had an
upper bound of 59 on the distance. This package proves that no such code has distance 57 or more, so the
upper bound is at most 56. The proof is 2 exact certificates (at d = 57 and 59) for the standard weight-enumerator linear program with Rains'
shadow constraints, checked by two separately written checkers. The certificate at d = 59 is the one at d = 57 with the rows for 57 <= j < 59 relabelled from inequalities to equalities (same multipliers, identical coefficients); both checkers verify it on its own. The new bound does not follow from the table's
other entries.

The exact scope, as signed off by the three reviewers:

> For the qubit cell [[173,2]], the saved claim-time codetables.de upper bound 59 is lowered to at most 56, because the exact integer Farkas certificates object/cert_173_2_57_sh.json (and object/cert_173_2_59_sh.json for the literal d=59) of the quantum weight-enumerator LP with Rains shadow constraints verify under verify-it-yourself/check_cert.py, and the propagation closure of the saved full table at (173,2) is 58, so the bound is not implied by other cells.
>
> (File paths as in this package. The reviewers' original sentence, which names the claim-folder paths, is under Review record.)

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` after a few seconds. Sample output is in verify-it-yourself/RECEIPTS.md.

## Compared to
M. Grassl, codetables.de, qubit table, cell [[173,2]]: Bounds on [[173,2]] lower bound: 34 upper bound: 59, https://codetables.de/QECC.php?q=4&n=173&k=2, fetched 2026-10-17T05:34:04Z (claim time), HTTP 200,
page sha256 19e8a7b675dd86211a013ee68b646d28f4710b3c694d39490baa9bc02069a02f; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

## Not claimed
- No new code: the lower bound stays 34.
- Not the exact optimum: 56 is the bound this linear program proves, not a proof that a distance-56 code exists.
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

> For the qubit cell [[173,2]], the saved claim-time codetables.de upper bound 59 is lowered to at most 56, because the exact integer Farkas certificates result/cert_173_2_57_sh.json (and result/cert_173_2_59_sh.json for the literal d=59) of the quantum weight-enumerator LP with Rains shadow constraints verify under check/check_cert.py, and the propagation closure of the saved full table at (173,2) is 58, so the bound is not implied by other cells.
