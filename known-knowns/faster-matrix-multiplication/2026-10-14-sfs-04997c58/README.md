# 7 fewer additions for (3, 5, 5) matrix multiplication

Comparison scope is the survey recorded on 2026-10-14. In the original claim and panel text below, "live" and "fresh" refer to those dated checks. Current-record status has not been requalified; subsequent source-inventory access blocks remain respected. This submission claims the exact object and its improvement against the recorded comparison circuits.

## What
The exact integer ternary circuit in claim/scheme.json (SHA256 04997c5844e0968c43b347b7e911059ac1464c5da653b29bd3838a489723df7c) computes ordered 3×5×5 matrix multiplication with 58 active products and 214 charged binary additions/subtractions, strictly below the applicable freshly checked Perminov, Lille and matmulcatalog references and the lowest checked public same-cell circuit at 218.

The object is stored at object/scheme.json. It reschedules the existing public ternary rank-58 decomposition. The stages save 3+2+2 additions relative to the 221-addition source; the actual public PR23 schedule uses 218, so this circuit also saves four additions against the lowest checked public circuit. All 58 products and expanded factors are preserved.

## Check it yourself
Run `sh verify-it-yourself/run_checks.sh` from this package directory. The final line is `PASS`. Two separate standard-library Python checkers execute every input basis pair and check all integer bilinear coefficients and literal operations. Observed local elapsed time and real output are in verify-it-yourself/RECEIPTS.md.

## Compared to
[Perminov's public reduced schedule](https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/addition_reduced_ZT/3x5x5_m58_cr221_cn357_ZT_reduced.json) uses 221 additions at rank 58, stages 53+72+96. This schedule uses 214, stages 50+70+94. The full expanded tensor factors are identical. the-record-we-beat/snapshot.json records the live URL, UTC time, HTTP status, selected headers, source hash and extracted cell.

The fresh panel independently checked all matching reduced files, reduced_known.json, README and CHANGELOG, the [Lille format page](https://fmm.univ-lille.fr/3x5x5.html), [fmm_sota](https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json), [matmulcatalog](https://github.com/solven-eu/matmulcatalog) actual programs, recent applicable papers, equivalent constructions and public claims. Reports preserve the exact evidence and optional literature access gaps. Catalogue direct-form counts are distinguished from reduced schedules.

## Not claimed
No new tensor, multiplication-rank improvement, globally minimal addition count, practical runtime speedup, or result for another shape is claimed. This is a source-relative scheduling improvement in the ordinary-coordinate binary addition/subtraction convention.

## Credits
Credit `sfs` for this rescheduling contribution. [Andrew I. Perminov](https://github.com/dronperminov/FastMatrixMultiplication) supplied the exact ternary tensor and source schedule. [Alexandre Sedoglavic and Alexey Smirnov, as cited by Lille](https://fmm.univ-lille.fr/3x5x5.html), supplied the original rank-58 decomposition; the independently checked Lille program uses the same normalized factors. [matmulcatalog](https://github.com/solven-eu/matmulcatalog) and [calgulbenkian’s actual public submission23](https://github.com/elder-plinius/V3R1T4S/pull/23) supplied comparison programs. Linear circuit transposition and cancellation are established methods. [V3R1T4S](https://github.com/elder-plinius/V3R1T4S) supplies the research protocol.

## License
Source code is offered under AGPL-3.0; contribution data and prose under CC BY 4.0. Underlying third-party works retain their authors' terms and attribution. The package distributes the derived schedule and our code, not third-party papers, pages, or reference datasets.
