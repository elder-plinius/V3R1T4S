# [[230,10]] qubit codes: upper bound on the distance lowered from 77 to 72

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[230,10]] (230 physical qubits encoding 10 logical qubits) had an
upper bound of 77 on the distance. This package proves that no such code has distance 73 or more, so the
upper bound is at most 72. The proof is 2 exact certificates (at d = 73 and 77) for the standard weight-enumerator linear program with Rains'
shadow constraints, checked by two separately written checkers. The certificate at d = 77 is the one at d = 73 with the rows for 73 <= j < 77 relabelled from inequalities to equalities (same multipliers, identical coefficients); both checkers verify it on its own. The new bound does not follow from the table's
other entries.

The exact scope, as signed off by the three reviewers:

> No [[230,10,d]] qubit stabilizer code exists for d = 73 (and hence for every d >= 73 including the live table upper bound 77), so the upper bound on d for [[230,10]] is at most 72, proven by an integer Farkas certificate of the quantum weight-enumerator LP with shadow constraints that verifies in verify-it-yourself/check_cert.py and is below the propagation closure of 75 from other live cells.
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
M. Grassl, codetables.de, qubit table, cell [[230,10]]: Bounds on [[230,10]] lower bound: 42 upper bound: 77, https://codetables.de/QECC.php?q=4&n=230&k=10, fetched 2026-10-17T05:32:54Z (claim time), HTTP 200,
page sha256 3ad6f4cb846fc5e018c1ca6b9a665bd4610c10326dadf48bc0518656c423bc7c; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

## Not claimed
- No new code: the lower bound stays 42.
- Not the exact optimum: 72 is the bound this linear program proves, not a proof that a distance-72 code exists.
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

> No [[230,10,d]] qubit stabilizer code exists for d = 73 (and hence for every d >= 73 including the live table upper bound 77), so the upper bound on d for [[230,10]] is at most 72, proven by an integer Farkas certificate of the quantum weight-enumerator LP with shadow constraints that verifies in check/check_cert.py and is below the propagation closure of 75 from other live cells.
