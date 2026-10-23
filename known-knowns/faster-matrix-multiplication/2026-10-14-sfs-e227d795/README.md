# 5 fewer additions for (3, 4, 5) matrix multiplication

Comparison scope is the survey recorded on 2026-10-14. In the original claim and panel text below, "live" and "fresh" refer to those dated checks. Current-record status has not been requalified; subsequent source-inventory access blocks remain respected. This submission claims the exact object and its improvement against the recorded comparison circuits.

## What
scheme.json exactly computes ordered (3,4,5) matrix multiplication over Z with 47 ternary bilinear products and 156 binary additions/subtractions, strictly below the applicable live Perminov, Lille, matmulcatalog and public same-cell comparisons fetched during this audit.

The object is stored at object/scheme.json. It reschedules Perminov's public ternary rank47 tensor, saving one addition in A preprocessing and four in B preprocessing relative to the161-addition source. The checked159-addition public submission is also higher than156. The47 products and expanded factors are preserved. All comparisons apply to the ordered3x4x5 product.

## Check it yourself
Run `sh verify-it-yourself/run_checks.sh` from this package directory. The final line is `PASS`. Two separate standard-library Python checkers execute every input basis pair and check all integer bilinear coefficients and literal operations. Observed local elapsed time and real output are in verify-it-yourself/RECEIPTS.md.

## Compared to
[Perminov's public reduced schedule](https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/addition_reduced_ZT/3x4x5_m47_cr161_cn277_ZT_reduced.json) uses 161 additions at rank 47, stages 39+48+74. This schedule uses 156, stages 38+44+74. The full expanded tensor factors are identical. the-record-we-beat/snapshot.json records the live URL, UTC time, HTTP status, selected headers, source hash and extracted cell.

The fresh panel independently checked all matching reduced files, reduced_known.json, README and CHANGELOG, the [Lille format page](https://fmm.univ-lille.fr/3x4x5.html), [fmm_sota](https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json), [matmulcatalog](https://github.com/solven-eu/matmulcatalog) actual programs, recent applicable papers, equivalent constructions and public claims. Reports preserve the exact evidence and optional literature access gaps. Catalogue direct-form counts are distinguished from reduced schedules.

## Not claimed
No new tensor, multiplication-rank improvement, globally minimal addition count, practical runtime speedup, or result for another shape is claimed. This is a source-relative scheduling improvement in the ordinary-coordinate binary addition/subtraction convention.

## Credits
Credit `sfs` for this rescheduling contribution. The exact ternary tensor and161-addition reference schedule are credited to [Andrew I. Perminov's public FMM repository](https://github.com/dronperminov/FastMatrixMultiplication). [Alexandre Sedoglavic's Lille catalogue](https://fmm.univ-lille.fr/3x4x5.html) supplies a comparison to the [AlphaTensor work by Alhussein Fawzi and coauthors](https://doi.org/10.1038/s41586-022-05172-4); that compared tensor is distinct from the candidate's source. [matmulcatalog](https://github.com/solven-eu/matmulcatalog) and [calgulbenkian's public V3R1T4S submission24](https://github.com/elder-plinius/V3R1T4S/pull/24) supply further actual-program comparisons. Circuit transposition and cancellation are established methods. [V3R1T4S](https://github.com/elder-plinius/V3R1T4S) supplies the research protocol.

## License
Source code is offered under AGPL-3.0; contribution data and prose under CC BY 4.0. Underlying third-party works retain their authors' terms and attribution. The package distributes the derived schedule and our code, not third-party papers, pages, or reference datasets.
