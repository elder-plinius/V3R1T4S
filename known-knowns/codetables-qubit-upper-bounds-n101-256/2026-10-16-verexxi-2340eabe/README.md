# [[146,2]] qubit codes: upper bound on the distance lowered from 49 to 47

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[146,2]] (146 physical qubits encoding 2 logical qubits) had an
upper bound of 49 on the distance. This package proves that no such code has distance 48 or more, so the
upper bound is at most 47. The proof is 2 exact certificates (at d = 48 and 49) for the standard weight-enumerator linear program with Rains'
shadow constraints, checked by two separately written checkers. The new bound does not follow from the table's
other entries.

The exact scope, as signed off by the three reviewers:

> Two independently re-run exact-integer Farkas certificates (object/cert_146_2_49_sh.json and object/cert_146_2_48_sh.json) show that the quantum weight-enumerator LP with Rains shadow constraints is infeasible for [[146,2,49]] and for [[146,2,48]], so no qubit stabilizer code [[146,2,d]] with d >= 48 exists, which lowers the table upper bound for cell (146,2) from 49 to at most 47 and is not implied by the propagation closure of the saved live table (49).
>
> (File paths as in this package. The reviewers' original sentence, which names the claim-folder paths, is under Review record.)

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` after a few seconds. Sample output is in verify-it-yourself/RECEIPTS.md.

## Compared to
M. Grassl, codetables.de, qubit table, cell [[146,2]]: Bounds on [[146,2]] lower bound: 30 upper bound: 49, https://codetables.de/QECC.php?q=4&n=146&k=2, fetched 2026-10-16T21:00:38Z (claim time), HTTP 200,
page sha256 e767c28e676aecd16c0ce703b8a38796dd935f742602a9912db4846cad96e627; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

## Not claimed
- No new code: the lower bound stays 30.
- Not the exact optimum: 47 is the bound this linear program proves, not a proof that a distance-47 code exists.
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

> Two independently re-run exact-integer Farkas certificates (result/cert_146_2_49_sh.json and result/cert_146_2_48_sh.json) show that the quantum weight-enumerator LP with Rains shadow constraints is infeasible for [[146,2,49]] and for [[146,2,48]], so no qubit stabilizer code [[146,2,d]] with d >= 48 exists, which lowers the table upper bound for cell (146,2) from 49 to at most 47 and is not implied by the propagation closure of the saved live table (49).
