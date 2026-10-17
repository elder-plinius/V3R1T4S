# [[129,2]] qubit codes: upper bound on the distance lowered from 43 to 42

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[129,2]] (129 physical qubits encoding 2 logical qubits) had an
upper bound of 43 on the distance. This package proves that no such code has distance 43 or more, so the
upper bound is at most 42. The proof is one exact certificate for the standard weight-enumerator linear program with Rains'
shadow constraints, checked by two separately written checkers. The new bound does not follow from the table's
other entries.

The exact scope, as signed off by the three reviewers:

> The exact integer Farkas certificate object/cert_129_2_43_sh.json (quantum weight-enumerator LP with Rains shadow rows) proves no [[129,2,43]] qubit stabilizer (additive) code exists, which lowers the claim-time codetables.de upper bound for [[129,2]] from 43 to at most 42, and 43 is not implied by the standard propagation rules applied to the other live cells of the saved claim-time table.
>
> (File paths as in this package. The reviewers' original sentence, which names the claim-folder paths, is under Review record.)

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` after a few seconds. Sample output is in verify-it-yourself/RECEIPTS.md.

## Compared to
M. Grassl, codetables.de, qubit table, cell [[129,2]]: Bounds on [[129,2]] lower bound: 25 upper bound: 43, https://codetables.de/QECC.php?q=4&n=129&k=2, fetched 2026-10-17T00:29:37Z (claim time), HTTP 200,
page sha256 19c28eb589e7dc3562d188b951a584ff23a27b333e04fe8b07ae03a9f901e551; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

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

> The exact integer Farkas certificate result/cert_129_2_43_sh.json (quantum weight-enumerator LP with Rains shadow rows) proves no [[129,2,43]] qubit stabilizer (additive) code exists, which lowers the claim-time codetables.de upper bound for [[129,2]] from 43 to at most 42, and 43 is not implied by the standard propagation rules applied to the other live cells of the saved claim-time table.
