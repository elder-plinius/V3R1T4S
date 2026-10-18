# 29 fewer additions for (5, 5, 5) matrix multiplication

Comparison scope is the survey recorded on 2026-10-14. In the original claim and panel text below, "live" and "fresh" refer to those dated checks. Current-record status has not been requalified; subsequent source-inventory access blocks remain respected. This submission claims the exact object and its improvement against the recorded comparison circuits.

## What
The immutable ternary straight-line program in claim/scheme.json (SHA256 c0c7abe9136e5f773d01c5c276cb1f6c3f565afab183499fdda63ac67947e02e) computes ordinary ordered (5,5,5) matrix multiplication exactly over Z with the live listed rank of 93 active products and 354 binary additions/subtractions, strictly below the applicable live 383-addition Perminov reference, the 846-addition matmulcatalog coverage value, and the independently verified 378-addition matching public PR circuit.

The object is stored at object/scheme.json. It reschedules the existing public rank-93 ternary decomposition, preserving every expanded factor. The stages save 10+9+10 additions relative to the 383-addition source. The lowest checked public same-cell circuit, PR21, uses378, so this schedule also saves24 additions against that actual program.

## Check it yourself
Run `sh verify-it-yourself/run_checks.sh` from this package directory. The final line is `PASS`. Two separate standard-library Python checkers execute every input basis pair and check all integer bilinear coefficients and literal operations. Observed local elapsed time and real output are in verify-it-yourself/RECEIPTS.md.

## Compared to
[Perminov's public reduced schedule](https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/addition_reduced_ZT/5x5x5_m93_cr383_fv160_cn843_ZT_reduced.json) uses 383 additions at rank 93, stages 103+105+175. This schedule uses 354, stages 93+96+165. The full expanded tensor factors are identical. the-record-we-beat/snapshot.json records the live URL, UTC time, HTTP status, selected headers, source hash and extracted cell.

The fresh panel independently checked all matching reduced files, reduced_known.json, README and CHANGELOG, the [Lille format page](https://fmm.univ-lille.fr/5x5x5.html), [fmm_sota](https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json), [matmulcatalog](https://github.com/solven-eu/matmulcatalog) actual programs, recent applicable papers, equivalent constructions and public claims. Reports preserve the exact evidence and optional literature access gaps. Catalogue direct-form counts are distinguished from reduced schedules.

## Not claimed
No new tensor, multiplication-rank improvement, globally minimal addition count, practical runtime speedup, or result for another shape is claimed. This is a source-relative scheduling improvement in the ordinary-coordinate binary addition/subtraction convention.

## Credits
Credit `sfs` for this rescheduling contribution. [Andrew I. Perminov’s public repository](https://github.com/dronperminov/FastMatrixMultiplication) supplies the exact ternary tensor and source schedule. [Moosbauer and Poole](https://arxiv.org/html/2502.04514), as cited by [Lille](https://fmm.univ-lille.fr/5x5x5.html), supply the compared nonternary rank-93 algorithm; it is distinct from the candidate’s coefficient class. [Kauers and Wood](https://arxiv.org/html/2505.05896), the AlphaEvolve objects in [matmulcatalog](https://github.com/solven-eu/matmulcatalog), and [calgulbenkian’s actual public submission21](https://github.com/elder-plinius/V3R1T4S/pull/21) provide further comparisons. Circuit transposition, cancellation and shared sums are established methods. [V3R1T4S](https://github.com/elder-plinius/V3R1T4S) supplies the research protocol.

## License
Source code is offered under AGPL-3.0; contribution data and prose under CC BY 4.0. Underlying third-party works retain their authors' terms and attribution. The package distributes the derived schedule and our code, not third-party papers, pages, or reference datasets.
