# [[183,1]] qubit codes: upper bound on the distance lowered from 61 to 59

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[183,1]] (183 physical qubits encoding 1 logical qubit) had an
upper bound of 61 on the distance. This package proves that no such code has distance 60 or more, so the
upper bound is at most 59. The proof is 2 exact certificates (at d = 60 and 61) for the standard weight-enumerator linear program with Rains'
shadow constraints, checked by two separately written checkers. The new bound does not follow from the table's
other entries.

The exact scope, as signed off by the three reviewers:

> For the single qubit cell (n,k)=(183,1), the saved table record (live upper bound 61, fetched 2026-10-16) is lowered by at least 1 (to at most 59 via d=60, and d=61 itself is also excluded) by exact integer Farkas certificates of the quantum weight-enumerator LP with Rains shadow constraints, and the saved complete table gives a propagation closure of 61 at that cell so the bound is not implied by other cells; this says nothing about any other cell and rests on the saved table, not a fresh live re-fetch by me.

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` after a few seconds. Sample output is in verify-it-yourself/RECEIPTS.md.

A note for reviewers running V3R1T4S's `kit/check_run.py`: its tamper test changes the middle digit of the
first certificate file and warns that the checkers still print PASS. That digit sits deep inside a multiplier
that is hundreds of digits long, so the changed file is still a valid certificate and both checkers are right to
accept it. Changes that break a certificate are rejected: see how-we-built-it/step5_checks.md.

## Compared to
M. Grassl, codetables.de, qubit table, cell [[183,1]]: Bounds on [[183,1]] lower bound: 36 upper bound: 61, https://codetables.de/QECC.php?q=4&n=183&k=1, fetched 2026-10-16T21:01:41Z (claim time), HTTP 200,
page sha256 5dc930c084ce6566ab47d2af41b6f0275a0854c06a1118cc6cde873efc10d2c0; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

## Not claimed
- No new code: the lower bound stays 36.
- Not the exact optimum: 59 is the bound this linear program proves, not a proof that a distance-59 code exists.
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
