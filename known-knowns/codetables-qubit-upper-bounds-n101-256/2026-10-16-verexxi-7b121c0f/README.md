# [[200,5]] qubit codes: upper bound on the distance lowered from 67 to 64

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[200,5]] (200 physical qubits encoding 5 logical qubits) had an
upper bound of 67 on the distance. This package proves that no such code has distance 65 or more, so the
upper bound is at most 64. The proof is 2 exact certificates (at d = 65 and 67) for the standard weight-enumerator linear program with Rains'
shadow constraints, checked by two separately written checkers. The new bound does not follow from the table's
other entries.

The exact scope, as signed off by the three reviewers:

> Per the claim-time table record (upper bound 67 for [[200,5]]), the exact integer Farkas certificates object/cert_200_5_67_sh.json and object/cert_200_5_65_sh.json (quantum weight-enumerator LP with MacWilliams and Rains shadow rows) show no qubit stabilizer code [[200,5,d]] exists for d >= 65 (so the upper bound is at most 64), and that bound is not implied by the propagation closure (67) of the saved complete table.
>
> (File paths as in this package. The reviewers' original sentence, which names the claim-folder paths, is under Review record.)

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` after a few seconds. Sample output is in verify-it-yourself/RECEIPTS.md.

## Compared to
M. Grassl, codetables.de, qubit table, cell [[200,5]]: Bounds on [[200,5]] lower bound: 38 upper bound: 67, https://codetables.de/QECC.php?q=4&n=200&k=5, fetched 2026-10-16T20:59:43Z (claim time), HTTP 200,
page sha256 c008b56351f8c2ba53448ceb2f0e6e6e18aaf80a7496764410ed4aab889c0aab; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

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

> Per the claim-time table record (upper bound 67 for [[200,5]]), the exact integer Farkas certificates result/cert_200_5_67_sh.json and result/cert_200_5_65_sh.json (quantum weight-enumerator LP with MacWilliams and Rains shadow rows) show no qubit stabilizer code [[200,5,d]] exists for d >= 65 (so the upper bound is at most 64), and that bound is not implied by the propagation closure (67) of the saved complete table.
