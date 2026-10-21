# [[230,3]] qubit codes: upper bound on the distance lowered from 77 to 74

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[230,3]] (230 physical qubits encoding 3 logical qubits) had an
upper bound of 77 on the distance. This package proves that no such code has distance 75 or more, so the
upper bound is at most 74. The proof is 2 exact certificates (at d = 75 and 77) for the standard weight-enumerator linear program with Rains'
shadow constraints, checked by two separately written checkers. The new bound does not follow from the table's
other entries.

The exact scope, as signed off by the three reviewers:

> Given the saved table record (data/QECC_q4_n230_k3_claimtime.html: [[230,3]] upper bound 77, lower 44, unchanged by the R1/R2/R3 closure over the saved full table), object/cert_230_3_77_sh.json and object/cert_230_3_75_sh.json are exact integer Farkas certificates of the qubit weight-enumerator LP with Rains shadow constraints that pass verify-it-yourself/check_cert.py, so no [[230,3,d]] stabilizer code exists for d >= 75 and the upper bound on [[230,3]] is at most 74; this is not a proof about anything beyond that cell, and "live at claim time" rests on the saved record only.
>
> (File paths as in this package. The reviewers' original sentence, which names the claim-folder paths, is under Review record.)

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` after a few seconds. Sample output is in verify-it-yourself/RECEIPTS.md.

## Compared to
M. Grassl, codetables.de, qubit table, cell [[230,3]]: Bounds on [[230,3]] lower bound: 44 upper bound: 77, https://codetables.de/QECC.php?q=4&n=230&k=3, fetched 2026-10-16T20:59:54Z (claim time), HTTP 200,
page sha256 ac4e69556df8a90aafeb48b2131844e601841034c3127372a23300b7238480c3; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

## Not claimed
- No new code: the lower bound stays 44.
- Not the exact optimum: 74 is the bound this linear program proves, not a proof that a distance-74 code exists.
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

> Given the saved table record (data/QECC_q4_n230_k3_claimtime.html: [[230,3]] upper bound 77, lower 44, unchanged by the R1/R2/R3 closure over the saved full table), result/cert_230_3_77_sh.json and result/cert_230_3_75_sh.json are exact integer Farkas certificates of the qubit weight-enumerator LP with Rains shadow constraints that pass check/check_cert.py, so no [[230,3,d]] stabilizer code exists for d >= 75 and the upper bound on [[230,3]] is at most 74; this is not a proof about anything beyond that cell, and "live at claim time" rests on the saved record only.
