# [[180,2]] qubit codes: upper bound on the distance lowered from 61 to 58

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[180,2]] (180 physical qubits encoding 2 logical qubits) had an
upper bound of 61 on the distance. This package proves that no such code has distance 59 or more, so the
upper bound is at most 58. The proof is 2 exact certificates (at d = 59 and 61) for the standard weight-enumerator linear program with Rains'
shadow constraints, checked by two separately written checkers. The certificate at d = 61 is the one at d = 59 with the rows for 59 <= j < 61 relabelled from inequalities to equalities (same multipliers, identical coefficients); both checkers verify it on its own. The new bound does not follow from the table's
other entries.

The exact scope, as signed off by the three reviewers:

> For the qubit cell (n,k)=(180,2), the saved codetables.de record (upper bound 61, lower bound 35) is lowered, with exact integer-checked Farkas certificates of the weight-enumerator LP with Rains shadow constraints, to the statement that no [[180,2,d]] stabilizer code exists for d=59 (hence an upper bound of at most 58, and in particular none for the live bound d=61), and this bound is not implied by the standard propagation closure of the other saved table cells, which gives 60.

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` after a few seconds. Sample output is in verify-it-yourself/RECEIPTS.md.

A note for reviewers running V3R1T4S's `kit/check_run.py`: its tamper test changes the middle digit of the
first certificate file and warns that the checkers still print PASS. That digit sits deep inside a multiplier
that is hundreds of digits long, so the changed file is still a valid certificate and both checkers are right to
accept it. Changes that break a certificate are rejected: see how-we-built-it/step5_checks.md.

## Compared to
M. Grassl, codetables.de, qubit table, cell [[180,2]]: Bounds on [[180,2]] lower bound: 35 upper bound: 61, https://codetables.de/QECC.php?q=4&n=180&k=2, fetched 2026-10-17T05:34:27Z (claim time), HTTP 200,
page sha256 dbf9ce06dfaacb2c3998b0301e0d23f529bc9ab66be3859a613708df7d15f7df; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

## Not claimed
- No new code: the lower bound stays 35.
- Not the exact optimum: 58 is the bound this linear program proves, not a proof that a distance-58 code exists.
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
