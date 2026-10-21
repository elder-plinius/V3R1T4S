# [[230,5]] qubit codes: upper bound on the distance lowered from 77 to 73

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[230,5]] (230 physical qubits encoding 5 logical qubits) had an
upper bound of 77 on the distance. This package proves that no such code has distance 74 or more, so the
upper bound is at most 73. The proof is 2 exact certificates (at d = 74 and 77) for the standard weight-enumerator linear program with Rains'
shadow constraints, checked by two separately written checkers. The new bound does not follow from the table's
other entries.

The exact scope, as signed off by the three reviewers:

> Within the standard quantum weight-enumerator LP with Rains shadow constraints, no qubit stabilizer code [[230,5,d]] exists for any d >= 74 (in particular d = 77, the live table upper bound of 77 recorded in data/QECC_q4_n230_k5_claimtime.html), so the upper bound for [[230,5]] drops from 77 to at most 73, and 73 is not implied by propagation of other cells of the complete table in data/qubit_table_full_n1-256.html.

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` after a few seconds. Sample output is in verify-it-yourself/RECEIPTS.md.

A note for reviewers running V3R1T4S's `kit/check_run.py`: its tamper test changes the middle digit of the
first certificate file and warns that the checkers still print PASS. That digit sits deep inside a multiplier
that is hundreds of digits long, so the changed file is still a valid certificate and both checkers are right to
accept it. Changes that break a certificate are rejected: see how-we-built-it/step5_checks.md.

## Compared to
M. Grassl, codetables.de, qubit table, cell [[230,5]]: Bounds on [[230,5]] lower bound: 44 upper bound: 77, https://codetables.de/QECC.php?q=4&n=230&k=5, fetched 2026-10-16T20:56:42Z (claim time), HTTP 200,
page sha256 aabd159795d970a2eaee7503c56c62ebbc5aa4ea761e8de015a1eaa529f3dbdb; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

## Not claimed
- No new code: the lower bound stays 44.
- Not the exact optimum: 73 is the bound this linear program proves, not a proof that a distance-73 code exists.
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
