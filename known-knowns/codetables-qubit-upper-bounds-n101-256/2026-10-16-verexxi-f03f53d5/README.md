# [[158,1]] qubit codes: upper bound on the distance lowered from 53 to 51

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[158,1]] (158 physical qubits encoding 1 logical qubit)
had an upper bound of 53 on the distance. This package proves that no such code has distance 52 or 53, so
the upper bound is at most 51. The proof is two exact certificates for the standard weight-enumerator linear
program with Rains' shadow constraints, checked by two separately written checkers. The new bound does not
follow from the table's other entries.

The exact scope, as signed off by the three reviewers:

> For the single qubit cell (n,k)=(158,1), the exact integer Farkas certificates in object/cert_158_1_53_sh.json (the table's listed upper bound 53) and object/cert_158_1_52_sh.json both pass the standalone integer checker and my own re-derived checker, so no [[158,1,52]] or [[158,1,53]] stabilizer code exists (upper bound 51, versus 53 in the saved codetables.de snapshot), and the propagation closure over all other cells of that snapshot still gives 53; the snapshot's liveness at claim time (2026-10-16T19:44Z) was taken from recorded timestamps and hashes, not re-fetched by me.
>
> (File paths as in this package. The reviewers' original sentence, which names the claim-folder paths, is under Review record.)

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` after a few seconds. Sample output is in verify-it-yourself/RECEIPTS.md.

## Compared to
M. Grassl, codetables.de, qubit table, cell [[158,1]]: Bounds on [[158,1]] lower bound: 33 upper bound: 53, https://codetables.de/QECC.php?q=4&n=158&k=1, fetched 2026-10-16T19:44:24Z (claim time), HTTP 200,
page sha256 d31b4dac0672c8edbfbd0ad60974cf6129f0b89a016a234ed4e0fc1fe4db9540; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

## Not claimed
- No new code: the lower bound stays 33.
- Not the exact optimum: 51 is the bound this linear program proves, not a proof that a distance-51 code exists.
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

> For the single qubit cell (n,k)=(158,1), the exact integer Farkas certificates in result/cert_158_1_53_sh.json (the table's listed upper bound 53) and result/cert_158_1_52_sh.json both pass the standalone integer checker and my own re-derived checker, so no [[158,1,52]] or [[158,1,53]] stabilizer code exists (upper bound 51, versus 53 in the saved codetables.de snapshot), and the propagation closure over all other cells of that snapshot still gives 53; the snapshot's liveness at claim time (2026-10-16T19:44Z) was taken from recorded timestamps and hashes, not re-fetched by me.
