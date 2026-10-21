# [[110,5]] qubit codes: upper bound on the distance lowered from 37 to 35

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[110,5]] (110 physical qubits encoding 5 logical qubits) had an
upper bound of 37 on the distance. This package proves that no such code has distance 36 or more, so the
upper bound is at most 35. The proof is 2 exact certificates (at d = 36 and 37) for the standard weight-enumerator linear program with Rains'
shadow constraints, checked by two separately written checkers. The certificate at d = 37 is the one at d = 36 with the rows for 36 <= j < 37 relabelled from inequalities to equalities (same multipliers, identical coefficients); both checkers verify it on its own. The new bound does not follow from the table's
other entries.

The exact scope, as signed off by the three reviewers:

> Both certificates verify in exact integer arithmetic, so no [[110,5,36]] (and no [[110,5,37]]) qubit stabilizer code exists, giving upper bound d(110,5) <= 35 versus the claim-time live table value of 37 and the live-table propagation closure of 36.

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` after a few seconds. Sample output is in verify-it-yourself/RECEIPTS.md.

## Compared to
M. Grassl, codetables.de, qubit table, cell [[110,5]]: Bounds on [[110,5]] lower bound: 23 upper bound: 37, https://codetables.de/QECC.php?q=4&n=110&k=5, fetched 2026-10-17T05:34:49Z (claim time), HTTP 200,
page sha256 22454f4e6b49c2cdb38e5734342607b33a49b92c6c638dd802e6b45fc071767c; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

## Not claimed
- No new code: the lower bound stays 23.
- Not the exact optimum: 35 is the bound this linear program proves, not a proof that a distance-35 code exists.
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
