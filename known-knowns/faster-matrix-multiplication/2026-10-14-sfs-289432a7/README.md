# 6 fewer additions for (2, 4, 8) matrix multiplication

Comparison scope is the survey recorded on 2026-10-14. In the original claim and panel text below, "live" and "fresh" refer to those dated checks. Current-record status has not been requalified; subsequent source-inventory access blocks remain respected. This submission claims the exact object and its improvement against the recorded comparison circuits.

## What
scheme.json gives a standard-coordinate exact integer ternary SLP for (2,4,8) at the live-listed rank 51 using 182 additions/subtractions, below the applicable counts in the freshly checked criterion sources and public rank-equal programs.

The object is stored at object/scheme.json. It reschedules the public AlphaEvolve decomposition, saving one addition in A preprocessing, four in B preprocessing and one in output reconstruction relative to the 188-addition source. The checked 187-addition public submission is also higher than 182. The 51 products and fully expanded factors are preserved.

## Check it yourself
Run `sh verify-it-yourself/run_checks.sh` from this package directory. The final line is `PASS`. Two separate standard-library Python checkers execute every input basis pair and check all integer bilinear coefficients and literal operations. Observed local elapsed time and real output are in verify-it-yourself/RECEIPTS.md.

## Compared to
[Perminov's public reduced schedule](https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/addition_reduced_ZT/2x4x8_m51_cr188_cn354_ZT_reduced.json) uses 188 additions at rank 51, stages 38+72+78. This schedule uses 182, stages 37+68+77. The full expanded tensor factors are identical. the-record-we-beat/snapshot.json records the live URL, UTC time, HTTP status, selected headers, source hash and extracted cell.

The fresh panel independently checked all matching reduced files, reduced_known.json, README and CHANGELOG, the [Lille format page](https://fmm.univ-lille.fr/2x4x8.html), [fmm_sota](https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json), [matmulcatalog](https://github.com/solven-eu/matmulcatalog) actual programs, recent applicable papers, equivalent constructions and public claims. Reports preserve the exact evidence and optional literature access gaps. Catalogue direct-form counts are distinguished from reduced schedules.

## Not claimed
No new tensor, multiplication-rank improvement, globally minimal addition count, practical runtime speedup, or result for another shape is claimed. This is a source-relative scheduling improvement in the ordinary-coordinate binary addition/subtraction convention.

## Credits
Credit `sfs` for this rescheduling contribution. The188-addition reference is [Andrew I. Perminov's public FMM schedule](https://github.com/dronperminov/FastMatrixMultiplication). The rank 51 factorization is credited to [Alexander Novikov and the AlphaEvolve authors at Google DeepMind](https://arxiv.org/abs/2506.13131), catalogued by [Alexandre Sedoglavic](https://fmm.univ-lille.fr/2x4x8.html). [matmulcatalog](https://github.com/solven-eu/matmulcatalog) supplies additional actual SLPs. [calgulbenkian's V3R1T4S submission26](https://github.com/elder-plinius/V3R1T4S/pull/26) supplies the checked 187-addition comparison; its exact object was independently checked. Circuit transposition, cancellation and integer scheduling are established methods; no method invention is claimed. [V3R1T4S](https://github.com/elder-plinius/V3R1T4S) supplies the three-skeptic research protocol.

## License
Source code is offered under AGPL-3.0; contribution data and prose under CC BY 4.0. Underlying third-party works retain their authors' terms and attribution. The package distributes the derived schedule and our code, not third-party papers, pages, or reference datasets.
