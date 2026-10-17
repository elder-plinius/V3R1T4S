# [[120,2]] qubit codes: upper bound on the distance lowered from 40 to 39

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[120,2]] (120 physical qubits encoding 2 logical qubits) had an
upper bound of 40 on the distance. This package proves that no such code has distance 40 or more, so the
upper bound is at most 39. The proof is one exact certificate for the standard weight-enumerator linear program with Rains'
shadow constraints, checked by two separately written checkers. The new bound does not follow from the table's
other entries.

The exact scope, as signed off by the three reviewers:

> The exact Farkas certificate object/cert_120_2_40_sh.json passes the integer checker verify-it-yourself/check_cert.py (quantum weight-enumerator LP with A_j=B_j for 1<=j<=39, A_j<=B_j for j>=40 and Rains shadow nonnegativity), proving no [[120,2,40]] qubit stabilizer code exists, which lowers the upper bound of the saved claim-time codetables.de cell (120,2) from 40 to at most 39 without that value being implied by the propagation rules applied to the saved full qubit table.
>
> (File paths as in this package. The reviewers' original sentence, which names the claim-folder paths, is under Review record.)

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` after a few seconds. Sample output is in verify-it-yourself/RECEIPTS.md.

## Compared to
M. Grassl, codetables.de, qubit table, cell [[120,2]]: Bounds on [[120,2]] lower bound: 25 upper bound: 40, https://codetables.de/QECC.php?q=4&n=120&k=2, fetched 2026-10-17T00:28:52Z (claim time), HTTP 200,
page sha256 992696ad605b36e1e26626457066c36aa9661a55be10541d8001ad85bd5c04a9; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

## Not claimed
- No new code: the lower bound stays 25.
- Not the exact optimum: 39 is the bound this linear program proves, not a proof that a distance-39 code exists.
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

> The exact Farkas certificate result/cert_120_2_40_sh.json passes the integer checker check/check_cert.py (quantum weight-enumerator LP with A_j=B_j for 1<=j<=39, A_j<=B_j for j>=40 and Rains shadow nonnegativity), proving no [[120,2,40]] qubit stabilizer code exists, which lowers the upper bound of the saved claim-time codetables.de cell (120,2) from 40 to at most 39 without that value being implied by the propagation rules applied to the saved full qubit table.
