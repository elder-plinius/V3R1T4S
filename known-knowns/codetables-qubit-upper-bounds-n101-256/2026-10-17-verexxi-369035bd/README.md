# [[167,2]] qubit codes: upper bound on the distance lowered from 57 to 54

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[167,2]] (167 physical qubits encoding 2 logical qubits) had an
upper bound of 57 on the distance. This package proves that no such code has distance 55 or more, so the
upper bound is at most 54. The proof is 2 exact certificates (at d = 55 and 57) for the standard weight-enumerator linear program with Rains'
shadow constraints, checked by two separately written checkers. The certificate at d = 57 is the one at d = 55 with the rows for 55 <= j < 57 relabelled from inequalities to equalities (same multipliers, identical coefficients); both checkers verify it on its own. The new bound does not follow from the table's
other entries.

The exact scope, as signed off by the three reviewers:

> Using exact integer Farkas certificates that check_cert.py verifies, no qubit stabilizer code [[167,2,d]] exists for d >= 55 (including the live table upper bound d = 57 recorded at claim time), so the upper bound for [[167,2]] is at most 54, below the propagation closure of 56 from the saved full table.

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` after a few seconds. Sample output is in verify-it-yourself/RECEIPTS.md.

## Compared to
M. Grassl, codetables.de, qubit table, cell [[167,2]]: Bounds on [[167,2]] lower bound: 33 upper bound: 57, https://codetables.de/QECC.php?q=4&n=167&k=2, fetched 2026-10-17T05:33:52Z (claim time), HTTP 200,
page sha256 d26f775ad3a031e70da81ef53f066165b4dc4efd993892c19d6241caad4b3869; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

## Not claimed
- No new code: the lower bound stays 33.
- Not the exact optimum: 54 is the bound this linear program proves, not a proof that a distance-54 code exists.
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
