# [[185,3]] qubit codes: upper bound on the distance lowered from 63 to 60

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[185,3]] (185 physical qubits encoding 3 logical qubits) had an
upper bound of 63 on the distance. This package proves that no such code has distance 61 or more, so the
upper bound is at most 60. The proof is 2 exact certificates (at d = 61 and 63) for the standard weight-enumerator linear program with Rains'
shadow constraints, checked by two separately written checkers. The certificate at d = 63 is the one at d = 61 with the rows for 61 <= j < 63 relabelled from inequalities to equalities (same multipliers, identical coefficients); both checkers verify it on its own. The new bound does not follow from the table's
other entries.

The exact scope, as signed off by the three reviewers:

> For the qubit cell [[185,3]], the checked exact integer Farkas certificates (with Rains shadow constraints) show no stabilizer code [[185,3,d]] exists for d = 61 and for d = 63 (the live upper bound of 63 at claim time), giving an upper bound of at most 60, which is not implied by propagation rules applied to the live table (closure value 61).

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` after a few seconds. Sample output is in verify-it-yourself/RECEIPTS.md.

## Compared to
M. Grassl, codetables.de, qubit table, cell [[185,3]]: Bounds on [[185,3]] lower bound: 36 upper bound: 63, https://codetables.de/QECC.php?q=4&n=185&k=3, fetched 2026-10-17T05:34:38Z (claim time), HTTP 200,
page sha256 b63791604a45d3cf7bd4ada4ab322fdf8888038bb1b4eaaabaa258bf551694e2; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

## Not claimed
- No new code: the lower bound stays 36.
- Not the exact optimum: 60 is the bound this linear program proves, not a proof that a distance-60 code exists.
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
