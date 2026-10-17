# z(16,19;3,3) >= 142: a 16 x 19 matrix with 142 ones and no all-ones 3 x 3 submatrix

## What
The saved 16 x 19 0/1 matrix matrix/z_16x19_142.txt (sha256 47ef934e...) has 142 ones and no all-ones 3 x 3 submatrix, which is strictly above the best explicit lower bound 136 recorded in status_source/ for z(16,19;3,3) and above 141, the best that 192000 saved trivial-surgery runs on 12 public witness matrices reached, with the limits that the status pages were not re-fetched here and the surgery baseline is a bounded sample.

In that sentence, matrix/z_16x19_142.txt is object/z_16x19_142.txt in this package, and status_source/ is the-record-we-beat/ plus
how-we-built-it/status_source/. Only the cell z(16,19;3,3) is claimed. The status pages named there were re-fetched once by the
novelty reviewer (the-record-we-beat/RECORD.md); the surgery baseline is a bounded sample, not a proof.

## Check it yourself
`sh verify-it-yourself/run_checks.sh` from this folder (Python 3 standard library only, about 1 second). It confirms the file hash,
the shape 16 x 19, at least 142 ones, and that no 3 rows and 3 columns are all ones (two independent methods over all 560 row triples
and 969 column triples). Expected last line: `PASS` (exit status 0); on any problem the last line is `FAIL` and the exit status is 1.

## Compared to
| bar | value | source |
|---|---|---|
| best explicitly stated lower bound | 136 | Saurabh, arXiv:2608.26603 (zero padding of his 16 x 18 matrix); the abs page was fetched 2026-10-17T12:28:33Z, HTTP 200 |
| earlier stated lower bound | 132 | Bhan, Nobili, Langer, arXiv:2605.01120, Figure 2 |
| numeric closure of published lower bounds (a computation) | 139 | how-we-built-it/status_source/lb_closure_output.txt |
| trivial surgery on 12 public witness matrices (a computation) | 141 | how-we-built-it/baseline/output/: 4 seeds x 12 bases x 4000 runs = 192000 runs, 66663 reach 141, none reach 142 |
| best upper bound | 147 | Afrasyab table repository, frontier_propagation.json, fetched 2026-10-17T12:28:33Z |
| this object | 142 | object/z_16x19_142.txt |

## Not claimed
- Any other cell. In particular not claimed: z(13,19) >= 119, z(14,19) >= 127, z(16,18) >= 137, z(14,20) >= 131; those tie what trivial
  surgery on public matrices gives.
- Optimality or any upper bound: the best known upper bound is 147.
- That nobody else holds 142 unpublished. A plain local search reaches 142 in seconds to minutes, so this is likely. The claim concerns
  published values only.
- That 142 cannot be derived from published matrices by some operation other than the family tried. The 192000 surgery runs are a
  bounded sample of one family.
- That no source we could not read states 142 or more (OEIS answered 403 to the earlier scout and was not retried; Guy's original tables,
  printed and unindexed material were not checked).
- Any structure in the matrix: row weights are 8, 8, 8, twelve 9s and one 10; column weights run from 6 to 9.

## Credits
- Found by verexxi. Search and verification code were written with help from Claude (Anthropic).
- Saurabh, arXiv:2608.26603 (stated lower bounds, and three witness matrices used as bases for the baseline).
- Bhan, Nobili, Langer et al., arXiv:2605.01120 (earlier lower bounds, Figure 2).
- Afrasyab, arXiv:2608.08154, repository https://github.com/KAVentures/z1322-exact (upper-bound table and witness matrices used as bases).
- Hou, arXiv:2608.08549, repository https://github.com/ShengtengHou/finite-zarankiewicz-seven-values (the 13 x 18 core).
- Collins, Riasanovsky, Wallace, Radziszowski, arXiv:1604.01257 (Table 4 upper bounds).
- Davies, Gill, Horsley, arXiv:2411.18842 (improved upper bounds).
- Tan, arXiv:2203.02283 (SAT attack on Zarankiewicz numbers).
- dfield, https://github.com/dfield/finite-zarankiewicz-closures (propagated table; copies of its data are in how-we-built-it/status_source/).
