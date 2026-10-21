# [[219,2]] qubit codes: upper bound on the distance lowered from 73 to 72

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[219,2]] (219 physical qubits encoding 2 logical qubits) had an
upper bound of 73 on the distance. This package proves that no such code has distance 73 or more, so the
upper bound is at most 72. The proof is one exact certificate for the standard weight-enumerator linear program with Rains'
shadow constraints, checked by two separately written checkers. The new bound does not follow from the table's
other entries.

The exact scope, as signed off by the three reviewers:

> For the single qubit cell [[219,2]], the saved claim-time codetables.de record (upper bound 73) is lowered to 72 because object/cert_219_2_73_sh.json is an exact integer Farkas certificate, checked by verify-it-yourself/check_cert.py, that no [[219,2,d]] stabilizer code with d >= 73 satisfies the quantum weight-enumerator LP with Rains shadow constraints, and the propagation closure of the saved complete table at (219,2) is 73, so 72 is not implied by other cells.
>
> (File paths as in this package. The reviewers' original sentence, which names the claim-folder paths, is under Review record.)

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` after a few seconds. Sample output is in verify-it-yourself/RECEIPTS.md.

## Compared to
M. Grassl, codetables.de, qubit table, cell [[219,2]]: Bounds on [[219,2]] lower bound: 42 upper bound: 73, https://codetables.de/QECC.php?q=4&n=219&k=2, fetched 2026-10-17T00:30:39Z (claim time), HTTP 200,
page sha256 6af37db32446cc5a70ab0ca1d21d9bc154d598ba1e6af22b4e3cf828b22857b3; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

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

> For the single qubit cell [[219,2]], the saved claim-time codetables.de record (upper bound 73) is lowered to 72 because result/cert_219_2_73_sh.json is an exact integer Farkas certificate, checked by check/check_cert.py, that no [[219,2,d]] stabilizer code with d >= 73 satisfies the quantum weight-enumerator LP with Rains shadow constraints, and the propagation closure of the saved complete table at (219,2) is 73, so 72 is not implied by other cells.
