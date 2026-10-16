# [[150,1]] qubit codes: upper bound on the distance lowered from 51 to 49

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[150,1]] (150 physical qubits encoding 1 logical qubit)
had an upper bound of 51 on the distance. This package proves that no such code has distance 50 or 51, so
the upper bound is at most 49. The proof is two exact certificates for the standard weight-enumerator linear
program with Rains' shadow constraints, checked by two independently written programs. The new bound does not
follow from the table's other entries.

The exact scope, as signed off by the three reviewers:

> For the qubit cell (n,k)=(150,1) with 101<=n<=256, the exact integer Farkas certificates result/cert_150_1_50_sh.json and result/cert_150_1_51_sh.json of the stated weight-enumerator LP (A_0=1, sum A=2^149, A_j=B_j for j<d, A_j<=B_j for j>=d, A>=0, shadow Sh_j>=0) verify under check/check_cert.py and an independent re-implementation, proving no [[150,1,d]] stabilizer code exists for d=50 or d=51 (so the upper bound is at most 49, lowering the recorded live bound of 51 by at least 2), and this is not implied by R1-R3 propagation of other cells of the recorded table snapshot (closure at (150,1) is 51); the live-fetch timing itself was not independently verifiable.

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` after a few seconds. Sample output is in verify-it-yourself/RECEIPTS.md.

## Compared to
M. Grassl, codetables.de, qubit table, cell [[150,1]]: lower bound 33, upper bound 51,
https://codetables.de/QECC.php?q=4&n=150&k=1, fetched 2026-10-16T18:15:30Z (claim time) and 2026-10-16T18:28:09Z
(panel), HTTP 200 both times, page sha256 47511f9f95f6a377da769c0fb1bd811497a555cbc1b10b11c76385bb3c9dfa6c.
Details in the-record-we-beat/.

## Not claimed
- No new code: the lower bound stays 33.
- Not the exact optimum: 49 is the bound this linear program proves, not a proof that a distance-49 code exists.
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
