# [[110,2]] qubit codes: upper bound on the distance lowered from 37 to 36

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[110,2]] (110 physical qubits encoding 2 logical qubits) had an
upper bound of 37 on the distance. This package proves that no such code has distance 37 or more, so the
upper bound is at most 36. The proof is one exact certificate for the standard weight-enumerator linear program with Rains'
shadow constraints, checked by two separately written checkers. The new bound does not follow from the table's
other entries.

The exact scope, as signed off by the three reviewers:

> Within the weight-enumerator LP with Rains shadow constraints, the integer Farkas certificate object/cert_110_2_37_sh.json is exactly verified to rule out any [[110,2,d]] qubit stabilizer code with d >= 37, so the codetables.de upper bound 37 (as saved at claim time; see the-record-we-beat/record.md) can be lowered to 36, and 36 is not implied by the propagation rules R1-R3 applied to the saved full table.
>
> (File paths as in this package. The reviewers' original sentence, which names the claim-folder paths, is under Review record.)

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` after a few seconds. Sample output is in verify-it-yourself/RECEIPTS.md.

## Compared to
M. Grassl, codetables.de, qubit table, cell [[110,2]]: Bounds on [[110,2]] lower bound: 24 upper bound: 37, https://codetables.de/QECC.php?q=4&n=110&k=2, fetched 2026-10-17T00:28:34Z (claim time), HTTP 200,
page sha256 9366ddf82bcfd8cba8025060d03f553dd6a312f0bd3dd6a767cf6349119c2034; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

## Not claimed
- No new code: the lower bound stays 24.
- Not the exact optimum: 36 is the bound this linear program proves, not a proof that a distance-36 code exists.
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

> Within the weight-enumerator LP with Rains shadow constraints, the integer Farkas certificate result/cert_110_2_37_sh.json is exactly verified to rule out any [[110,2,d]] qubit stabilizer code with d >= 37, so the codetables.de upper bound 37 (as saved at claim time in data/QECC_q4_n110_k2_claimtime.html) can be lowered to 36, and 36 is not implied by the propagation rules R1-R3 applied to the saved full table.
