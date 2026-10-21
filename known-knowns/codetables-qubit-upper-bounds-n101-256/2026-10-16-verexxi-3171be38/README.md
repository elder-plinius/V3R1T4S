# [[152,1]] qubit codes: upper bound on the distance lowered from 51 to 49

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[152,1]] (152 physical qubits encoding 1 logical qubit)
had an upper bound of 51 on the distance. This package proves that no such code has distance 50 or 51, so
the upper bound is at most 49. The proof is two exact certificates for the standard weight-enumerator linear
program with Rains' shadow constraints, checked by two separately written checkers. The new bound does not
follow from the table's other entries.

The exact scope, as signed off by the three reviewers:

> For the qubit cell (152,1), the supplied integer Farkas certificates (d=50 and d=51) of the stated weight-enumerator LP with Rains shadow constraints verify in exact integer arithmetic (supplied checker and my own re-implementation), so no [[152,1,50]] (hence no [[152,1,51]]) stabilizer code exists, lowering the recorded live upper bound 51 to at most 49, which the propagation closure of the recorded full-table snapshot (51) does not imply; the live status was taken from the recorded fetch files and not re-fetched by me.

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` after a few seconds. Sample output is in verify-it-yourself/RECEIPTS.md.

## Compared to
M. Grassl, codetables.de, qubit table, cell [[152,1]]: Bounds on [[152,1]] lower bound: 33 upper bound: 51, https://codetables.de/QECC.php?q=4&n=152&k=1, fetched 2026-10-16T19:44:06Z (claim time), HTTP 200,
page sha256 d03ffa956a2bf8c67ef4d4cd7ff402c86bc7ffff5d0f2189578489dd0167b0d1; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

## Not claimed
- No new code: the lower bound stays 33.
- Not the exact optimum: 49 is the bound this linear program proves, not a proof that a distance-49 code exists.
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
