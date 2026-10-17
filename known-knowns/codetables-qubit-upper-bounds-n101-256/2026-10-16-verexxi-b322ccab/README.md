# [[165,2]] qubit codes: upper bound on the distance lowered from 55 to 53

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[165,2]] (165 physical qubits encoding 2 logical qubits) had an
upper bound of 55 on the distance. This package proves that no such code has distance 54 or more, so the
upper bound is at most 53. The proof is 2 exact certificates (at d = 54 and 55) for the standard weight-enumerator linear program with Rains'
shadow constraints, checked by two separately written checkers. The new bound does not follow from the table's
other entries.

The exact scope, as signed off by the three reviewers:

> For the qubit cell [[165,2]] (table record fetched 2026-10-16T21:01:09Z showing upper bound 55), the exact integer Farkas certificates in object/cert_165_2_55_sh.json and object/cert_165_2_54_sh.json (LP with MacWilliams link, A_j=B_j for 1<=j<d, A_j<=B_j, nonnegativity, shadow nonnegativity) verify and exclude every qubit stabilizer code [[165,2,d]] with d>=54, lowering the table upper bound from 55 to at most 53, and this value is not implied by the propagation rules applied to the saved table (closure at (165,2) is 55).
>
> (File paths as in this package. The reviewers' original sentence, which names the claim-folder paths, is under Review record.)

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` after a few seconds. Sample output is in verify-it-yourself/RECEIPTS.md.

## Compared to
M. Grassl, codetables.de, qubit table, cell [[165,2]]: Bounds on [[165,2]] lower bound: 32 upper bound: 55, https://codetables.de/QECC.php?q=4&n=165&k=2, fetched 2026-10-16T21:01:09Z (claim time), HTTP 200,
page sha256 c38c91cf8ef8660e6746443d1db91f1310d04704347531a08f5a121f6afa5e1b; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

## Not claimed
- No new code: the lower bound stays 32.
- Not the exact optimum: 53 is the bound this linear program proves, not a proof that a distance-53 code exists.
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

> For the qubit cell [[165,2]] (table record fetched 2026-10-16T21:01:09Z showing upper bound 55), the exact integer Farkas certificates in result/cert_165_2_55_sh.json and result/cert_165_2_54_sh.json (LP with MacWilliams link, A_j=B_j for 1<=j<d, A_j<=B_j, nonnegativity, shadow nonnegativity) verify and exclude every qubit stabilizer code [[165,2,d]] with d>=54, lowering the table upper bound from 55 to at most 53, and this value is not implied by the propagation rules applied to the saved table (closure at (165,2) is 55).
