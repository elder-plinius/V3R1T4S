# [[148,2]] qubit codes: upper bound on the distance lowered from 50 to 48

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[148,2]] (148 physical qubits encoding 2 logical qubits) had an
upper bound of 50 on the distance. This package proves that no such code has distance 49 or more, so the
upper bound is at most 48. The proof is 2 exact certificates (at d = 49 and 50) for the standard weight-enumerator linear program with Rains'
shadow constraints, checked by two separately written checkers. The new bound does not follow from the table's
other entries.

The exact scope, as signed off by the three reviewers:

> For the qubit cell (148,2), the exact integer Farkas certificates object/cert_148_2_50_sh.json (d = 50, the live upper bound recorded 2026-10-16) and object/cert_148_2_49_sh.json (d = 49) both verify under verify-it-yourself/check_cert.py for the shadow-augmented quantum weight-enumerator LP (stabilizer codes only), so no [[148,2,50]] (hence, by the d = 49 certificate, no [[148,2,49]]) stabilizer code exists, and the propagation closure of the saved complete table at (148,2) is 50, so the new bound of 48 is not implied by other saved cells.
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
M. Grassl, codetables.de, qubit table, cell [[148,2]]: Bounds on [[148,2]] lower bound: 30 upper bound: 50, https://codetables.de/QECC.php?q=4&n=148&k=2, fetched 2026-10-16T21:00:48Z (claim time), HTTP 200,
page sha256 d59b202d91deade3d265d1144a3eda548db859b69f7d8ea0dc7a98136aeb98c0; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

## Not claimed
- No new code: the lower bound stays 30.
- Not the exact optimum: 48 is the bound this linear program proves, not a proof that a distance-48 code exists.
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

> For the qubit cell (148,2), the exact integer Farkas certificates result/cert_148_2_50_sh.json (d = 50, the live upper bound recorded 2026-10-16) and result/cert_148_2_49_sh.json (d = 49) both verify under check/check_cert.py for the shadow-augmented quantum weight-enumerator LP (stabilizer codes only), so no [[148,2,50]] (hence, by the d = 49 certificate, no [[148,2,49]]) stabilizer code exists, and the propagation closure of the saved complete table at (148,2) is 50, so the new bound of 48 is not implied by other saved cells.
