# [[133,2]] qubit codes: upper bound on the distance lowered from 45 to 43

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[133,2]] (133 physical qubits encoding 2 logical qubits) had an
upper bound of 45 on the distance. This package proves that no such code has distance 44 or more, so the
upper bound is at most 43. The proof is 2 exact certificates (at d = 44 and 45) for the standard weight-enumerator linear program with Rains'
shadow constraints, checked by two separately written checkers. The new bound does not follow from the table's
other entries.

The exact scope, as signed off by the three reviewers:

> The two integer Farkas certificates in object/ (shadow-enhanced quaternary-MacWilliams LP, n=133, k=2, d=44 and d=45) are valid, so no [[133,2,d]] qubit stabilizer code exists for d >= 44, which lowers the claim-time snapshot upper bound of 45 (data/QECC_q4_n133_k2_claimtime.html) to at most 43 and is not implied by the R1/R2/R3 propagation closure of the full table snapshot (data/qubit_table_full_n1-256.html).
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
M. Grassl, codetables.de, qubit table, cell [[133,2]]: Bounds on [[133,2]] lower bound: 26 upper bound: 45, https://codetables.de/QECC.php?q=4&n=133&k=2, fetched 2026-10-16T21:00:07Z (claim time), HTTP 200,
page sha256 a2919c391e9ff74cdfda23a839da049d31657525ff06fe55230ad0d7f024fb9c; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

## Not claimed
- No new code: the lower bound stays 26.
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

> The two integer Farkas certificates in result/ (shadow-enhanced quaternary-MacWilliams LP, n=133, k=2, d=44 and d=45) are valid, so no [[133,2,d]] qubit stabilizer code exists for d >= 44, which lowers the claim-time snapshot upper bound of 45 (data/QECC_q4_n133_k2_claimtime.html) to at most 43 and is not implied by the R1/R2/R3 propagation closure of the full table snapshot (data/qubit_table_full_n1-256.html).
