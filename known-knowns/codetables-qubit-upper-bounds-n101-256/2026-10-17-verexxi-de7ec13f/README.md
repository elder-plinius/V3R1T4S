# [[192,2]] qubit codes: upper bound on the distance lowered from 65 to 63

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[192,2]] (192 physical qubits encoding 2 logical qubits) had an
upper bound of 65 on the distance. This package proves that no such code has distance 64 or more, so the
upper bound is at most 63. The proof is 2 exact certificates (at d = 64 and 65) for the standard weight-enumerator linear program with Rains'
shadow constraints, checked by two separately written checkers. The certificate at d = 65 is the one at d = 64 with the rows for 64 <= j < 65 relabelled from inequalities to equalities (same multipliers, identical coefficients); both checkers verify it on its own. The new bound does not follow from the table's
other entries.

The exact scope, as signed off by the three reviewers:

> No [[192,2,d]] qubit stabilizer code exists for d = 64 or d = 65 (hence d <= 63), proved by an integer-arithmetic Farkas certificate of the shadow-enhanced quantum weight-enumerator LP that is verified by verify-it-yourself/check_cert.py and is not implied by the R1/R2/R3 propagation closure (64) of the claim-time table, whose upper bound for that cell was 65.
>
> (File paths as in this package. The reviewers' original sentence, which names the claim-folder paths, is under Review record.)

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` after a few seconds. Sample output is in verify-it-yourself/RECEIPTS.md.

## Compared to
M. Grassl, codetables.de, qubit table, cell [[192,2]]: Bounds on [[192,2]] lower bound: 37 upper bound: 65, https://codetables.de/QECC.php?q=4&n=192&k=2, fetched 2026-10-17T05:35:44Z (claim time), HTTP 200,
page sha256 20940479cbdff12078de1b0cba4cc0b756a9af457a6aaa441cd741e58415ff76; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

## Not claimed
- No new code: the lower bound stays 37.
- Not the exact optimum: 63 is the bound this linear program proves, not a proof that a distance-63 code exists.
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

> No [[192,2,d]] qubit stabilizer code exists for d = 64 or d = 65 (hence d <= 63), proved by an integer-arithmetic Farkas certificate of the shadow-enhanced quantum weight-enumerator LP that is verified by check/check_cert.py and is not implied by the R1/R2/R3 propagation closure (64) of the claim-time table, whose upper bound for that cell was 65.
