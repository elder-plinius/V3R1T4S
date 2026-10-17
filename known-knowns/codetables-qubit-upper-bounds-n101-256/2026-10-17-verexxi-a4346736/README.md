# [[190,2]] qubit codes: upper bound on the distance lowered from 64 to 62

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[190,2]] (190 physical qubits encoding 2 logical qubits) had an
upper bound of 64 on the distance. This package proves that no such code has distance 63 or more, so the
upper bound is at most 62. The proof is 2 exact certificates (at d = 63 and 64) for the standard weight-enumerator linear program with Rains'
shadow constraints, checked by two separately written checkers. The certificate at d = 64 is the one at d = 63 with the rows for 63 <= j < 64 relabelled from inequalities to equalities (same multipliers, identical coefficients); both checkers verify it on its own. The new bound does not follow from the table's
other entries.

The exact scope, as signed off by the three reviewers:

> No qubit stabilizer code [[190,2,63]] (hence none with d >= 63, including d = 64) exists, as shown by an exact integer Farkas certificate of the shadow-augmented quantum weight-enumerator LP verified by verify-it-yourself/check_cert.py, which lowers the claim-time table upper bound for [[190,2]] from 64 to at most 62 (below the propagation closure of 63 computed from the saved complete table).
>
> (File paths as in this package. The reviewers' original sentence, which names the claim-folder paths, is under Review record.)

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` after a few seconds. Sample output is in verify-it-yourself/RECEIPTS.md.

## Compared to
M. Grassl, codetables.de, qubit table, cell [[190,2]]: Bounds on [[190,2]] lower bound: 37 upper bound: 64, https://codetables.de/QECC.php?q=4&n=190&k=2, fetched 2026-10-17T05:35:32Z (claim time), HTTP 200,
page sha256 36d83bf11f5ab16750c67c59692941cb2c0f80013f3e25951e59c63821687798; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

## Not claimed
- No new code: the lower bound stays 37.
- Not the exact optimum: 62 is the bound this linear program proves, not a proof that a distance-62 code exists.
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

> No qubit stabilizer code [[190,2,63]] (hence none with d >= 63, including d = 64) exists, as shown by an exact integer Farkas certificate of the shadow-augmented quantum weight-enumerator LP verified by check/check_cert.py, which lowers the claim-time table upper bound for [[190,2]] from 64 to at most 62 (below the propagation closure of 63 computed from the saved complete table).
