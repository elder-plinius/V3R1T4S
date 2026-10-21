# [[135,6]] qubit codes: upper bound on the distance lowered from 45 to 43

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[135,6]] (135 physical qubits encoding 6 logical qubits) had an
upper bound of 45 on the distance. This package proves that no such code has distance 44 or more, so the
upper bound is at most 43. The proof is 2 exact certificates (at d = 44 and 45) for the standard weight-enumerator linear program with Rains'
shadow constraints, checked by two separately written checkers. The certificate at d = 45 is the one at d = 44 with the rows for 44 <= j < 45 relabelled from inequalities to equalities (same multipliers, identical coefficients); both checkers verify it on its own. The new bound does not follow from the table's
other entries.

The exact scope, as signed off by the three reviewers:

> No [[135,6,44]] (hence no [[135,6,45]]) qubit stabilizer code exists, by an exact integer Farkas certificate of the shadow-augmented quantum weight-enumerator LP verified by verify-it-yourself/check_cert.py, so the upper bound on d for [[135,6]] is at most 43, which is below both the claim-time table value 45 and the propagation closure 44 from other cells.
>
> (File paths as in this package. The reviewers' original sentence, which names the claim-folder paths, is under Review record.)

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` after a few seconds. Sample output is in verify-it-yourself/RECEIPTS.md.

## Compared to
M. Grassl, codetables.de, qubit table, cell [[135,6]]: Bounds on [[135,6]] lower bound: 25 upper bound: 45, https://codetables.de/QECC.php?q=4&n=135&k=6, fetched 2026-10-17T05:35:22Z (claim time), HTTP 200,
page sha256 867633fbf0f579b8e5adbf7c26d365ca7b3548951fe1df798c835d7b0b62c6b5; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

## Not claimed
- No new code: the lower bound stays 25.
- Not the exact optimum: 43 is the bound this linear program proves, not a proof that a distance-43 code exists.
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

> No [[135,6,44]] (hence no [[135,6,45]]) qubit stabilizer code exists, by an exact integer Farkas certificate of the shadow-augmented quantum weight-enumerator LP verified by check/check_cert.py, so the upper bound on d for [[135,6]] is at most 43, which is below both the claim-time table value 45 and the propagation closure 44 from other cells.
