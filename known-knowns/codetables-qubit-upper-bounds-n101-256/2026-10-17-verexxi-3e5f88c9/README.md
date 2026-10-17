# [[225,2]] qubit codes: upper bound on the distance lowered from 75 to 74

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[225,2]] (225 physical qubits encoding 2 logical qubits) had an
upper bound of 75 on the distance. This package proves that no such code has distance 75 or more, so the
upper bound is at most 74. The proof is one exact certificate for the standard weight-enumerator linear program with Rains'
shadow constraints, checked by two separately written checkers. The new bound does not follow from the table's
other entries.

The exact scope, as signed off by the three reviewers:

> The exact integer Farkas certificate object/cert_225_2_75_sh.json (quantum weight-enumerator LP with MacWilliams links, A_j = B_j for 1<=j<=74, A_j <= B_j for j>=75, and Rains shadow nonnegativity) verifies in the standard-library checker, proving no qubit stabilizer code [[225,2,75]] exists, so the [[225,2]] upper bound is at most 74 versus the 75 recorded on the claim-time page, and that bound is not obtained by propagation from the other cells of the saved full table.
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
M. Grassl, codetables.de, qubit table, cell [[225,2]]: Bounds on [[225,2]] lower bound: 44 upper bound: 75, https://codetables.de/QECC.php?q=4&n=225&k=2, fetched 2026-10-17T00:30:48Z (claim time), HTTP 200,
page sha256 e7790e91af4cc9b264e7d2211744d741aaff4435417e790eb03bd09aede35759; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

## Not claimed
- No new code: the lower bound stays 44.
- Not the exact optimum: 74 is the bound this linear program proves, not a proof that a distance-74 code exists.
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

> The exact integer Farkas certificate result/cert_225_2_75_sh.json (quantum weight-enumerator LP with MacWilliams links, A_j = B_j for 1<=j<=74, A_j <= B_j for j>=75, and Rains shadow nonnegativity) verifies in the standard-library checker, proving no qubit stabilizer code [[225,2,75]] exists, so the [[225,2]] upper bound is at most 74 versus the 75 recorded on the claim-time page, and that bound is not obtained by propagation from the other cells of the saved full table.
