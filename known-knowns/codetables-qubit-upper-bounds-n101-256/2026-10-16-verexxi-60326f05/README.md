# [[105,4]] qubit codes: upper bound on the distance lowered from 35 to 34

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[105,4]] (105 physical qubits encoding 4 logical qubits) had an
upper bound of 35 on the distance. This package proves that no such code has distance 35 or more, so the
upper bound is at most 34. The proof is one exact certificate for the standard weight-enumerator linear program with Rains'
shadow constraints, checked by two separately written checkers. The new bound does not follow from the table's
other entries.

The exact scope, as signed off by the three reviewers:

> For the qubit cell (105,4), the saved table record (fetched 2026-10-16T21:02:04Z, upper bound 35) is lowered to 34 by an exact Farkas certificate (object/cert_105_4_35_sh.json; weight-enumerator LP with A_j=B_j for 1<=j<=34, A_j<=B_j for j>=35, and shadow nonnegativity) that verify-it-yourself/check_cert.py verifies in integer arithmetic, and the closure of the saved full table under R1, R2, R3 at (105,4) is 35, so the bound is not implied by propagation from other saved cells.
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
M. Grassl, codetables.de, qubit table, cell [[105,4]]: Bounds on [[105,4]] lower bound: 21 upper bound: 35, https://codetables.de/QECC.php?q=4&n=105&k=4, fetched 2026-10-16T21:02:04Z (claim time), HTTP 200,
page sha256 93d5fd17b2cb6c3e8fd97bf84154faa5b88c0922c31d7ea4a21ddf75e4e079b0; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

## Not claimed
- No new code: the lower bound stays 21.
- Not the exact optimum: 34 is the bound this linear program proves, not a proof that a distance-34 code exists.
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

> For the qubit cell (105,4), the saved table record (fetched 2026-10-16T21:02:04Z, upper bound 35) is lowered to 34 by an exact Farkas certificate (result/cert_105_4_35_sh.json; weight-enumerator LP with A_j=B_j for 1<=j<=34, A_j<=B_j for j>=35, and shadow nonnegativity) that check/check_cert.py verifies in integer arithmetic, and the closure of the saved full table under R1, R2, R3 at (105,4) is 35, so the bound is not implied by propagation from other saved cells.
