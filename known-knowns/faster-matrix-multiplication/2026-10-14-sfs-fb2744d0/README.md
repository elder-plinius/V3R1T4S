# Five fewer additions for (2,5,5) matrix multiplication

Comparison scope is the survey recorded on 2026-10-14. In the original claim and panel text below, "live" and "fresh" refer to those dated checks. Current-record status has not been requalified; subsequent source-inventory access blocks remain respected. This submission claims the exact object and its improvement against the recorded comparison circuits.

## What
At the recorded live survey, claim/scheme.json is an exact integer ternary SLP for (2,5,5) with 40 active products and 148 binary additions/subtractions, matching Sedoglavic's listed rank 40 and strictly beating Perminov's minimum reduced count 153 and matmulcatalog's listed unshared count 256, while Lille cites no reduced-complexity variant for this format.

The object is stored at object/scheme.json. It reschedules an existing public decomposition, saving three additions in A preprocessing and two in output reconstruction. The B stage and number of products stay at their source values.

## Check it yourself
Run `sh verify-it-yourself/run_checks.sh` from this package directory. The final line is `PASS`. Two separate standard-library Python checkers verify every integer bilinear coefficient and count the operations. The observed local elapsed time is recorded in verify-it-yourself/RECEIPTS.md.

## Compared to
[Perminov's public reduced schedule](https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/addition_reduced_ZT/2x5x5_m40_cr153_cn283_ZT_reduced.json) uses 153 additions at rank 40, stages 34+55+64. This schedule uses 148, stages 31+55+62, for the identical expanded tensor factors. the-record-we-beat/snapshot.json records the live URL, fetch time, selected headers, source hash and extracted cell.

The fresh panel independently checked all matching reduced files, reduced_known.json, README and CHANGELOG, the [Lille format page](https://fmm.univ-lille.fr/2x5x5.html), [fmm_sota](https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json), [matmulcatalog](https://github.com/solven-eu/matmulcatalog), recent applicable papers and public claims. Panel reports preserve the exact scope and an optional literature PDF access gap. Catalog's 256 and Lille's 208 values are unshared counts, not reduced records.

## Not claimed
No new tensor, multiplication-rank improvement, globally minimal addition count, practical runtime speedup, or result for another shape is claimed. This is a source-relative scheduling improvement in the ordinary-coordinate binary addition/subtraction convention.

## Credits
Credit `sfs` for this rescheduling contribution. The factorization and 153-addition reference come from [Andrew I. Perminov's public FMM repository](https://github.com/dronperminov/FastMatrixMultiplication). [Alexandre Sedoglavic's Lille catalogue](https://fmm.univ-lille.fr/2x5x5.html) credits John Edward Hopcroft and Leslie R. Kerr's 1971 rank construction. [matmulcatalog](https://github.com/solven-eu/matmulcatalog) supplies further comparison data. Circuit transposition and common-subexpression elimination are established methods; no invention of those techniques is claimed. [V3R1T4S](https://github.com/elder-plinius/V3R1T4S) supplies the research and three-skeptic protocol.

## License
Source code is offered under AGPL-3.0; contribution data and prose under CC BY 4.0. Underlying third-party works retain their authors' terms and attribution. The package distributes the derived schedule and our code, not third-party papers, pages, or reference datasets.
