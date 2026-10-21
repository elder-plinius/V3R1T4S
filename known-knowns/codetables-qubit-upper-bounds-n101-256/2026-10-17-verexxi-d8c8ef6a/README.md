# [[161,2]] qubit codes: upper bound on the distance lowered from 55 to 52

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[161,2]] (161 physical qubits encoding 2 logical qubits) had an
upper bound of 55 on the distance. This package proves that no such code has distance 53 or more, so the
upper bound is at most 52. The proof is 2 exact certificates (at d = 53 and 55) for the standard weight-enumerator linear program with Rains'
shadow constraints, checked by two separately written checkers. The certificate at d = 55 is the one at d = 53 with the rows for 53 <= j < 55 relabelled from inequalities to equalities (same multipliers, identical coefficients); both checkers verify it on its own. The new bound does not follow from the table's
other entries.

The exact scope, as signed off by the three reviewers:

> For qubit stabilizer codes [[161,2]], an exact integer-arithmetic Farkas certificate of the weight-enumerator LP with Rains shadow constraints, verified by verify-it-yourself/check_cert.py, shows no [[161,2,d]] code exists with d>=53 (including d=55, the claim-time table upper bound), so the upper bound is at most 52, and this is not implied by propagation from the claim-time table (closure 54).
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
M. Grassl, codetables.de, qubit table, cell [[161,2]]: Bounds on [[161,2]] lower bound: 31 upper bound: 55, https://codetables.de/QECC.php?q=4&n=161&k=2, fetched 2026-10-17T05:33:41Z (claim time), HTTP 200,
page sha256 f7271221c6cf52a5b73dd7c073f40879dee98b24c77e9bb794745673746039ef; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

## Not claimed
- No new code: the lower bound stays 31.
- Not the exact optimum: 52 is the bound this linear program proves, not a proof that a distance-52 code exists.
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

> For qubit stabilizer codes [[161,2]], an exact integer-arithmetic Farkas certificate of the weight-enumerator LP with Rains shadow constraints, verified by check/check_cert.py, shows no [[161,2,d]] code exists with d>=53 (including d=55, the claim-time table upper bound), so the upper bound is at most 52, and this is not implied by propagation from the claim-time table (closure 54).
