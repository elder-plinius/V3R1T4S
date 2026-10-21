# [[128,5]] qubit codes: upper bound on the distance lowered from 43 to 41

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[128,5]] (128 physical qubits encoding 5 logical qubits) had an
upper bound of 43 on the distance. This package proves that no such code has distance 42 or more, so the
upper bound is at most 41. The proof is 2 exact certificates (at d = 42 and 43) for the standard weight-enumerator linear program with Rains'
shadow constraints, checked by two separately written checkers. The certificate at d = 43 is the one at d = 42 with the rows for 42 <= j < 43 relabelled from inequalities to equalities (same multipliers, identical coefficients); both checkers verify it on its own. The new bound does not follow from the table's
other entries.

The exact scope, as signed off by the three reviewers:

> The exact Farkas certificate in object/cert_128_5_42_sh.json, verified in integer arithmetic by verify-it-yourself/check_cert.py, proves that no [[128,5,42]] qubit stabilizer code (hence no [[128,5,43]]) exists, so the upper bound for [[128,5]] drops from the claim-time table value 43 to at most 41, below the propagation closure value of 42 from other claim-time cells.
>
> (File paths as in this package. The reviewers' original sentence, which names the claim-folder paths, is under Review record.)

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` after a few seconds. Sample output is in verify-it-yourself/RECEIPTS.md.

## Compared to
M. Grassl, codetables.de, qubit table, cell [[128,5]]: Bounds on [[128,5]] lower bound: 24 upper bound: 43, https://codetables.de/QECC.php?q=4&n=128&k=5, fetched 2026-10-17T05:35:11Z (claim time), HTTP 200,
page sha256 8c721d4d79ff6172421d20ce629c1eee19f20b1f4093e65bd21d06c4d0ad24e7; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

## Not claimed
- No new code: the lower bound stays 24.
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

> The exact Farkas certificate in result/cert_128_5_42_sh.json, verified in integer arithmetic by check/check_cert.py, proves that no [[128,5,42]] qubit stabilizer code (hence no [[128,5,43]]) exists, so the upper bound for [[128,5]] drops from the claim-time table value 43 to at most 41, below the propagation closure value of 42 from other claim-time cells.
