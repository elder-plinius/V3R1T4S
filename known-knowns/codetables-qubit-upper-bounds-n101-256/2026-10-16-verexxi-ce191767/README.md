# [[140,2]] qubit codes: upper bound on the distance lowered from 47 to 45

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[140,2]] (140 physical qubits encoding 2 logical qubits) had an
upper bound of 47 on the distance. This package proves that no such code has distance 46 or more, so the
upper bound is at most 45. The proof is 2 exact certificates (at d = 46 and 47) for the standard weight-enumerator linear program with Rains'
shadow constraints, checked by two separately written checkers. The new bound does not follow from the table's
other entries.

The exact scope, as signed off by the three reviewers:

> The supplied certificates (object/cert_140_2_46_sh.json and object/cert_140_2_47_sh.json) are exact integer Farkas certificates, passing verify-it-yourself/check_cert.py, that the quantum weight-enumerator LP with Rains shadow constraints is infeasible for [[140,2,46]] and [[140,2,47]], so no qubit stabilizer code [[140,2,46]] exists, lowering the upper bound recorded in the claim-time table (47) to at most 45, and 45 is not implied by the propagation rules applied to the saved complete table.
>
> (File paths as in this package. The reviewers' original sentence, which names the claim-folder paths, is under Review record.)

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` after a few seconds. Sample output is in verify-it-yourself/RECEIPTS.md.

A note for reviewers running V3R1T4S's `kit/check_run.py`: its tamper test changes the middle digit of the
first certificate file and warns that the checkers still print PASS. That digit sits deep inside a multiplier
that is hundreds of digits long, so the changed file is still a valid certificate and both checkers are right to
accept it. Changes that break a certificate are rejected: see how-we-built-it/step5_checks.md.

## Compared to
M. Grassl, codetables.de, qubit table, cell [[140,2]]: Bounds on [[140,2]] lower bound: 30 upper bound: 47, https://codetables.de/QECC.php?q=4&n=140&k=2, fetched 2026-10-16T21:00:17Z (claim time), HTTP 200,
page sha256 ec703213402ff0ed34e51e496842aa195c266cea09e7aeb7bc6a21734cbff7c6; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

## Not claimed
- No new code: the lower bound stays 30.
- Not the exact optimum: 45 is the bound this linear program proves, not a proof that a distance-45 code exists.
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

> The supplied certificates (result/cert_140_2_46_sh.json and result/cert_140_2_47_sh.json) are exact integer Farkas certificates, passing check/check_cert.py, that the quantum weight-enumerator LP with Rains shadow constraints is infeasible for [[140,2,46]] and [[140,2,47]], so no qubit stabilizer code [[140,2,46]] exists, lowering the upper bound recorded in the claim-time table (47) to at most 45, and 45 is not implied by the propagation rules applied to the saved complete table.
