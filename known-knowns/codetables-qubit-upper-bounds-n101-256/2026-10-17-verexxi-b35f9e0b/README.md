# [[135,8]] qubit codes: upper bound on the distance lowered from 43 to 42

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[135,8]] (135 physical qubits encoding 8 logical qubits) had an
upper bound of 43 on the distance. This package proves that no such code has distance 43 or more, so the
upper bound is at most 42. The proof is one exact certificate for the standard weight-enumerator linear program with Rains'
shadow constraints, checked by two separately written checkers. The new bound does not follow from the table's
other entries.

The exact scope, as signed off by the three reviewers:

> Both the shipped verify-it-yourself/check_cert.py and my own independent re-implementation accept object/cert_135_8_43_sh.json in exact integer arithmetic, which proves that the qubit stabilizer weight-enumerator LP (quaternary MacWilliams link, A_i = B_i for i from 1 to 42, A_i at most B_i, nonnegativity, Rains shadow nonnegativity) is infeasible for n = 135, k = 8, so no [[135,8,d]] qubit stabilizer code with d at least 43 exists, which lowers the upper bound recorded for cell (135,8) in the claimant's saved codetables.de snapshots (recorded in the-record-we-beat/record.md, fetched 2026-10-17T00:27:18Z and 2026-10-17T00:29:55Z) from 43 to 42, and that 42 is not implied by the propagation rules R1, R2, R3 (nor by puncturing or the quantum Singleton bound) applied to any other cell of the saved complete table, whose closure at (135,8) is 43; I did not re-fetch the live table or search the literature.
>
> (File paths as in this package. The reviewers' original sentence, which names the claim-folder paths, is under Review record.)

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` after a few seconds. Sample output is in verify-it-yourself/RECEIPTS.md.

## Compared to
M. Grassl, codetables.de, qubit table, cell [[135,8]]: Bounds on [[135,8]] lower bound: 25 upper bound: 43, https://codetables.de/QECC.php?q=4&n=135&k=8, fetched 2026-10-17T00:29:55Z (claim time), HTTP 200,
page sha256 98f7ab4b286f9e163f24a0a4518963451cedc989b13ed0f3d52ad4556ef51f91; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

## Not claimed
- No new code: the lower bound stays 25.
- Not the exact optimum: 42 is the bound this linear program proves, not a proof that a distance-42 code exists.
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

> Both the shipped check/check_cert.py and my own independent re-implementation accept result/cert_135_8_43_sh.json in exact integer arithmetic, which proves that the qubit stabilizer weight-enumerator LP (quaternary MacWilliams link, A_i = B_i for i from 1 to 42, A_i at most B_i, nonnegativity, Rains shadow nonnegativity) is infeasible for n = 135, k = 8, so no [[135,8,d]] qubit stabilizer code with d at least 43 exists, which lowers the upper bound recorded for cell (135,8) in the claimant's saved codetables.de snapshots (hash-matched to CLAIM.md, fetches recorded there as 2026-10-17T00:27:18Z and 2026-10-17T00:29:55Z) from 43 to 42, and that 42 is not implied by the propagation rules R1, R2, R3 (nor by puncturing or the quantum Singleton bound) applied to any other cell of the saved complete table, whose closure at (135,8) is 43; I did not re-fetch the live table or search the literature.
