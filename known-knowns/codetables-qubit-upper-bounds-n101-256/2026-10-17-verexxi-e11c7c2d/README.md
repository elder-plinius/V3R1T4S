# [[175,3]] qubit codes: upper bound on the distance lowered from 59 to 56

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[175,3]] (175 physical qubits encoding 3 logical qubits) had an
upper bound of 59 on the distance. This package proves that no such code has distance 57 or more, so the
upper bound is at most 56. The proof is 2 exact certificates (at d = 57 and 59) for the standard weight-enumerator linear program with Rains'
shadow constraints, checked by two separately written checkers. The certificate at d = 59 is the one at d = 57 with the rows for 57 <= j < 59 relabelled from inequalities to equalities (same multipliers, identical coefficients); both checkers verify it on its own. The new bound does not follow from the table's
other entries.

The exact scope, as signed off by the three reviewers:

> Within the saved claim-time codetables.de snapshot (upper bound 59 for qubit [[175,3]]), the integer-checked Farkas certificates with shadow constraints prove that no [[175,3,d]] stabilizer code exists for d = 57 through 59, so the upper bound is at most 56, and propagation from the other live cells gives only 58.

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` after a few seconds. Sample output is in verify-it-yourself/RECEIPTS.md.

A note for reviewers running V3R1T4S's `kit/check_run.py`: its tamper test changes the middle digit of the
first certificate file and warns that the checkers still print PASS. That digit sits deep inside a multiplier
that is hundreds of digits long, so the changed file is still a valid certificate and both checkers are right to
accept it. Changes that break a certificate are rejected: see how-we-built-it/step5_checks.md.

## Compared to
M. Grassl, codetables.de, qubit table, cell [[175,3]]: Bounds on [[175,3]] lower bound: 34 upper bound: 59, https://codetables.de/QECC.php?q=4&n=175&k=3, fetched 2026-10-17T05:34:15Z (claim time), HTTP 200,
page sha256 100faa6c5f8e72cfbb25bd0c033727fbd08ed9af57991177286c3106a26ef37e; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

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
