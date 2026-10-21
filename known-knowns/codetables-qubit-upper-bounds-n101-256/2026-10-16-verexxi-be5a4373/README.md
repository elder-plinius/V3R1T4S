# [[159,2]] qubit codes: upper bound on the distance lowered from 53 to 51

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[159,2]] (159 physical qubits encoding 2 logical qubits) had an
upper bound of 53 on the distance. This package proves that no such code has distance 52 or more, so the
upper bound is at most 51. The proof is 2 exact certificates (at d = 52 and 53) for the standard weight-enumerator linear program with Rains'
shadow constraints, checked by two separately written checkers. The new bound does not follow from the table's
other entries.

The exact scope, as signed off by the three reviewers:

> Within the standard stabilizer-code LP with Rains shadow constraints, object/cert_159_2_53_sh.json and object/cert_159_2_52_sh.json are exact integer Farkas certificates (verified by verify-it-yourself/check_cert.py) that no qubit stabilizer code [[159,2,53]] or [[159,2,52]] exists, lowering the saved-record codetables.de upper bound for cell (159,2) from 53 to at most 51, and that value is not implied by the propagation rules R1-R3 applied to the saved full table (closure at (159,2) is 53).
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
M. Grassl, codetables.de, qubit table, cell [[159,2]]: Bounds on [[159,2]] lower bound: 31 upper bound: 53, https://codetables.de/QECC.php?q=4&n=159&k=2, fetched 2026-10-16T21:00:59Z (claim time), HTTP 200,
page sha256 bf8570d740bdf2ba0d51826bb553e6604fc381be9067b1b7032690bd16267652; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

## Not claimed
- No new code: the lower bound stays 31.
- Not the exact optimum: 51 is the bound this linear program proves, not a proof that a distance-51 code exists.
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

> Within the standard stabilizer-code LP with Rains shadow constraints, result/cert_159_2_53_sh.json and result/cert_159_2_52_sh.json are exact integer Farkas certificates (verified by check/check_cert.py) that no qubit stabilizer code [[159,2,53]] or [[159,2,52]] exists, lowering the saved-record codetables.de upper bound for cell (159,2) from 53 to at most 51, and that value is not implied by the propagation rules R1-R3 applied to the saved full table (closure at (159,2) is 53).
