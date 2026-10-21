# [[135,1]] qubit codes: upper bound on the distance lowered from 45 to 44

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[135,1]] (135 physical qubits encoding 1 logical qubit) had an
upper bound of 45 on the distance. This package proves that no such code has distance 45 or more, so the
upper bound is at most 44. The proof is one exact certificate for the standard weight-enumerator linear program with Rains'
shadow constraints, checked by two separately written checkers. The new bound does not follow from the table's
other entries.

The exact scope, as signed off by the three reviewers:

> Within the weight-enumerator LP with Rains shadow constraints (A_0=1, sum A_i=2^(n-k), A_j=B_j for 1<=j<=44, A_j<=B_j for j>=45, shadow>=0, A>=0), the exact integer Farkas certificate object/cert_135_1_45_sh.json passes verify-it-yourself/check_cert.py, so no [[135,1,45]] qubit stabilizer code exists and the upper bound for the [[135,1]] cell (45 in the claim-time page recorded in the-record-we-beat/record.md) drops to at most 44, not implied by propagation from the other live cells in the saved table.
>
> (File paths as in this package. The reviewers' original sentence, which names the claim-folder paths, is under Review record.)

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` after a few seconds. Sample output is in verify-it-yourself/RECEIPTS.md.

## Compared to
M. Grassl, codetables.de, qubit table, cell [[135,1]]: Bounds on [[135,1]] lower bound: 27 upper bound: 45, https://codetables.de/QECC.php?q=4&n=135&k=1, fetched 2026-10-17T00:29:46Z (claim time), HTTP 200,
page sha256 2a04a91c8a2b060c19f079102e24e85b231f1a8587404c1248cb81a3dff26d77; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

## Not claimed
- No new code: the lower bound stays 27.
- Not the exact optimum: 44 is the bound this linear program proves, not a proof that a distance-44 code exists.
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

> Within the weight-enumerator LP with Rains shadow constraints (A_0=1, sum A_i=2^(n-k), A_j=B_j for 1<=j<=44, A_j<=B_j for j>=45, shadow>=0, A>=0), the exact integer Farkas certificate result/cert_135_1_45_sh.json passes check/check_cert.py, so no [[135,1,45]] qubit stabilizer code exists and the upper bound for the [[135,1]] cell (45 in the claim-time page data/QECC_q4_n135_k1_claimtime.html) drops to at most 44, not implied by propagation from the other live cells in the saved table.
