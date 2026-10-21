# [[132,1]] qubit codes: upper bound on the distance lowered from 45 to 43

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[132,1]] (132 physical qubits encoding 1 logical qubit)
had an upper bound of 45 on the distance. This package proves that no such code has distance 44 or 45, so
the upper bound is at most 43. The proof is two exact certificates for the standard weight-enumerator linear
program with Rains' shadow constraints, checked by two separately written checkers. The new bound does not
follow from the table's other entries.

The exact scope, as signed off by the three reviewers:

> For qubit stabilizer codes, the exact integer Farkas certificates object/cert_132_1_44_sh.json and object/cert_132_1_45_sh.json (quantum weight-enumerator LP with Rains shadow constraints, verified by verify-it-yourself/check_cert.py and by my independent re-implementation) show that no [[132,1,d]] code exists for any d >= 44, lowering the recorded table upper bound of 45 (from the saved fetches, not re-fetched by me) to at most 43, and that value is not implied by R1/R2/R3 propagation from the other cells of the saved table (closure at (132,1) = 45).
>
> (File paths as in this package. The reviewers' original sentence, which names the claim-folder paths, is under Review record.)

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` after a few seconds. Sample output is in verify-it-yourself/RECEIPTS.md.

## Compared to
M. Grassl, codetables.de, qubit table, cell [[132,1]]: Bounds on [[132,1]] lower bound: 27 upper bound: 45, https://codetables.de/QECC.php?q=4&n=132&k=1, fetched 2026-10-16T19:43:40Z (claim time), HTTP 200,
page sha256 61399b24e3e415e90dd5ea5a3eeb0897c628605dbaef73de052b897140b2bd11; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

## Not claimed
- No new code: the lower bound stays 27.
- Not the exact optimum: 43 is the bound this linear program proves, not a proof that a distance-43 code exists.
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

> For qubit stabilizer codes, the exact integer Farkas certificates result/cert_132_1_44_sh.json and result/cert_132_1_45_sh.json (quantum weight-enumerator LP with Rains shadow constraints, verified by check/check_cert.py and by my independent re-implementation) show that no [[132,1,d]] code exists for any d >= 44, lowering the recorded table upper bound of 45 (from the saved fetches, not re-fetched by me) to at most 43, and that value is not implied by R1/R2/R3 propagation from the other cells of the saved table (closure at (132,1) = 45).
