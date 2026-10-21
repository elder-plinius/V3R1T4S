# [[195,2]] qubit codes: upper bound on the distance lowered from 65 to 64

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[195,2]] (195 physical qubits encoding 2 logical qubits) had an
upper bound of 65 on the distance. This package proves that no such code has distance 65 or more, so the
upper bound is at most 64. The proof is one exact certificate for the standard weight-enumerator linear program with Rains'
shadow constraints, checked by two separately written checkers. The new bound does not follow from the table's
other entries.

The exact scope, as signed off by the three reviewers:

> Relative to the saved claim-time codetables.de snapshot (upper bound 65 for [[195,2]]), the integer Farkas certificate object/cert_195_2_65_sh.json (quantum weight-enumerator LP with the MacWilliams link, A_j = B_j for j from 1 to 64, A_j at most B_j, A at least 0, and Rains shadow nonnegativity) is valid under two separately written checkers, so no qubit stabilizer code [[195,2,d]] with d at least 65 exists and the upper bound for this single cell is at most 64, a value that the R1-R3 closure of the saved complete table (also with the extra rule d(n,k) at most d(n-1,k)+1) does not imply (the closure stays 65); I did not re-fetch the live table and did not search the literature outside the table.
>
> (File paths as in this package. The reviewers' original sentence, which names the claim-folder paths, is under Review record.)

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` after a few seconds. Sample output is in verify-it-yourself/RECEIPTS.md.

## Compared to
M. Grassl, codetables.de, qubit table, cell [[195,2]]: Bounds on [[195,2]] lower bound: 38 upper bound: 65, https://codetables.de/QECC.php?q=4&n=195&k=2, fetched 2026-10-17T00:30:13Z (claim time), HTTP 200,
page sha256 db84e866276bb307905e0c3a6637edeaa1c3c9e50ed10d0c87721a5a46ac1030; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

## Not claimed
- No new code: the lower bound stays 38.
- Not the exact optimum: 64 is the bound this linear program proves, not a proof that a distance-64 code exists.
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

> Relative to the saved claim-time codetables.de snapshot (upper bound 65 for [[195,2]]), the integer Farkas certificate claim/result/cert_195_2_65_sh.json (quantum weight-enumerator LP with the MacWilliams link, A_j = B_j for j from 1 to 64, A_j at most B_j, A at least 0, and Rains shadow nonnegativity) is valid under two independent exact-integer checks, so no qubit stabilizer code [[195,2,d]] with d at least 65 exists and the upper bound for this single cell is at most 64, a value that the R1-R3 closure of the saved complete table (also with the extra rule d(n,k) at most d(n-1,k)+1) does not imply (the closure stays 65); I did not re-fetch the live table and did not search the literature outside the table.
