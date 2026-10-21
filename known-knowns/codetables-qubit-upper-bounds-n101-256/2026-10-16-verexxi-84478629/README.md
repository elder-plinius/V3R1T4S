# [[200,2]] qubit codes: upper bound on the distance lowered from 67 to 65

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[200,2]] (200 physical qubits encoding 2 logical qubits) had an
upper bound of 67 on the distance. This package proves that no such code has distance 66 or more, so the
upper bound is at most 65. The proof is 2 exact certificates (at d = 66 and 67) for the standard weight-enumerator linear program with Rains'
shadow constraints, checked by two separately written checkers. The new bound does not follow from the table's
other entries.

The exact scope, as signed off by the three reviewers:

> The exact-integer Farkas certificate object/cert_200_2_66_sh.json (verified by verify-it-yourself/check_cert.py) proves that no qubit stabilizer code [[200,2,d]] with d >= 66 exists, so the [[200,2]] upper bound (67 in data/QECC_q4_n200_k2_claimtime.html) is lowered to at most 65, and the closure of the rules R1-R3 over data/qubit_table_full_n1-256.html at (200,2) is 67, so this is not implied by neighbouring cells.
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
M. Grassl, codetables.de, qubit table, cell [[200,2]]: Bounds on [[200,2]] lower bound: 39 upper bound: 67, https://codetables.de/QECC.php?q=4&n=200&k=2, fetched 2026-10-16T21:01:52Z (claim time), HTTP 200,
page sha256 83407f406126a7bb6b725add67b0ec7128d170f6fd189103a79b419875fd60b8; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

## Not claimed
- No new code: the lower bound stays 39.
- Not the exact optimum: 65 is the bound this linear program proves, not a proof that a distance-65 code exists.
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

> The exact-integer Farkas certificate result/cert_200_2_66_sh.json (verified by check/check_cert.py) proves that no qubit stabilizer code [[200,2,d]] with d >= 66 exists, so the [[200,2]] upper bound (67 in data/QECC_q4_n200_k2_claimtime.html) is lowered to at most 65, and the closure of the rules R1-R3 over data/qubit_table_full_n1-256.html at (200,2) is 67, so this is not implied by neighbouring cells.
