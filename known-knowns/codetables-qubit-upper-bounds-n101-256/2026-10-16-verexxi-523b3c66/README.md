# [[142,2]] qubit codes: upper bound on the distance lowered from 48 to 46

## What
In M. Grassl's table of qubit stabilizer codes, the cell [[142,2]] (142 physical qubits encoding 2 logical qubits) had an
upper bound of 48 on the distance. This package proves that no such code has distance 47 or more, so the
upper bound is at most 46. The proof is 2 exact certificates (at d = 47 and 48) for the standard weight-enumerator linear program with Rains'
shadow constraints, checked by two separately written checkers. The new bound does not follow from the table's
other entries.

The exact scope, as signed off by the three reviewers:

> Two exact-integer Farkas certificates for the quantum weight-enumerator LP with Rains shadow constraints (cert_142_2_48_sh.json for d=48, cert_142_2_47_sh.json for d=47) verify in verify-it-yourself/check_cert.py, so no qubit stabilizer code [[142,2,47]] (hence none with d>=47, including the snapshot upper bound 48) exists, lowering the upper bound of cell (142,2) from the table value 48 (record in data/QECC_q4_n142_k2_claimtime.html) to at most 46, and propagation over the saved full table gives closure 48 at (142,2), so the bound is not implied by other cells in that saved snapshot; I did not re-fetch the live table.
>
> (File paths as in this package. The reviewers' original sentence, which names the claim-folder paths, is under Review record.)

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` after a few seconds. Sample output is in verify-it-yourself/RECEIPTS.md.

A note for reviewers running V3R1T4S's `kit/check_run.py`: its tamper test changes the middle digit of the
first certificate file and warns that the checkers still print PASS. That digit sits deep inside a multiplier
that is hundreds of digits long, so the changed file is still a valid certificate and both checkers are right to
accept it. Changes that break a certificate are rejected: see how-we-built-it/step5_checks.md.

## Compared to
M. Grassl, codetables.de, qubit table, cell [[142,2]]: Bounds on [[142,2]] lower bound: 30 upper bound: 48, https://codetables.de/QECC.php?q=4&n=142&k=2, fetched 2026-10-16T21:00:27Z (claim time), HTTP 200,
page sha256 66fef426d41383cc48140ebb8e49076880723af92cfff17e91bbc09f682bde8d; re-fetched by the NOVELTY panelist (panel/novelty.md). Details in the-record-we-beat/.

## Not claimed
- No new code: the lower bound stays 30.
- Not the exact optimum: 46 is the bound this linear program proves, not a proof that a distance-46 code exists.
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

> Two exact-integer Farkas certificates for the quantum weight-enumerator LP with Rains shadow constraints (cert_142_2_48_sh.json for d=48, cert_142_2_47_sh.json for d=47) verify in check/check_cert.py, so no qubit stabilizer code [[142,2,47]] (hence none with d>=47, including the snapshot upper bound 48) exists, lowering the upper bound of cell (142,2) from the table value 48 (record in data/QECC_q4_n142_k2_claimtime.html) to at most 46, and propagation over the saved full table gives closure 48 at (142,2), so the bound is not implied by other cells in that saved snapshot; I did not re-fetch the live table.
