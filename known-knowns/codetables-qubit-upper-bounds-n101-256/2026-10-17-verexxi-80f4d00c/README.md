# [[200,10]] qubit codes: upper bound on the distance lowered from 67 to 62

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[200,10]] (200 physical qubits encoding 10 logical qubits) had an
upper bound of 67 on the distance. This package proves that no such code has distance 63 or more, so the
upper bound is at most 62. The proof is 2 exact certificates (at d = 63 and 67) for the standard weight-enumerator linear program with Rains'
shadow constraints, checked by two separately written checkers. The certificate at d = 67 is the one at d = 63 with the rows for 63 <= j < 67 relabelled from inequalities to equalities (same multipliers, identical coefficients); both checkers verify it on its own. The new bound does not follow from the table's
other entries.

The exact scope, as signed off by the three reviewers:

> The exact integer Farkas certificate object/cert_200_10_63_sh.json, checked by verify-it-yourself/check_cert.py, proves that no [[200,10,d]] qubit stabilizer code exists for any d >= 63, which lowers the claim-time table upper bound of 67 to at most 62 and is below the value of 63 obtained by propagating the other claim-time table cells.
>
> (File paths as in this package. The reviewers' original sentence, which names the claim-folder paths, is under Review record.)

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` after a few seconds. Sample output is in verify-it-yourself/RECEIPTS.md.

## Compared to
M. Grassl, codetables.de, qubit table, cell [[200,10]]: Bounds on [[200,10]] lower bound: 37 upper bound: 67, https://codetables.de/QECC.php?q=4&n=200&k=10, fetched 2026-10-17T05:32:41Z (claim time), HTTP 200,
page sha256 4e64d7790b52b60bebfc7662ee57891a4e46cfe968b6696bd1feaf3a7cf5de56; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

## Not claimed
- No new code: the lower bound stays 37.
- Not the exact optimum: 62 is the bound this linear program proves, not a proof that a distance-62 code exists.
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

> The exact integer Farkas certificate result/cert_200_10_63_sh.json, checked by check/check_cert.py, proves that no [[200,10,d]] qubit stabilizer code exists for any d >= 63, which lowers the claim-time table upper bound of 67 to at most 62 and is below the value of 63 obtained by propagating the other claim-time table cells.
