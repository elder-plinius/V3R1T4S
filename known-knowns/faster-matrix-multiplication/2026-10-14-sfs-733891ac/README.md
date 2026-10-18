# 16 fewer additions for (4, 4, 6) matrix multiplication

Comparison scope is the survey recorded on 2026-10-14. In the original claim and panel text below, "live" and "fresh" refer to those dated checks. Current-record status has not been requalified; subsequent source-inventory access blocks remain respected. This submission claims the exact object and its improvement against the recorded comparison circuits.

## What
The ordered (4,4,6), rank-73 integer ternary SLP in claim/scheme.json has 264 charged binary additions/subtractions and exactly computes A·B over Z, strictly below the applicable public counts checked at the recorded live snapshots (lowest independently verified comparator: 275).

The object is stored at object/scheme.json. It reschedules the existing public rank-73 ternary decomposition, preserving every expanded factor. The stages save6+5+5additions relative to the280-addition source; the actual275-addition publicPR17 is also higher by11.

## Check it yourself
Run `sh verify-it-yourself/run_checks.sh` from this package directory. The final line is `PASS`. Two separate standard-library Python checkers execute every input basis pair and check all integer bilinear coefficients and literal operations. Observed local elapsed time and real output are in verify-it-yourself/RECEIPTS.md.

## Compared to
[Perminov's public reduced schedule](https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/addition_reduced_ZT/4x4x6_m73_cr280_cn540_ZT_reduced.json) uses 280 additions at rank 73, stages 73+81+126. This schedule uses 264, stages 67+76+121. The full expanded tensor factors are identical. the-record-we-beat/snapshot.json records the live URL, UTC time, HTTP status, selected headers, source hash and extracted cell.

The fresh panel independently checked all matching reduced files, reduced_known.json, README and CHANGELOG, the [Lille format page](https://fmm.univ-lille.fr/4x4x6.html), [fmm_sota](https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json), [matmulcatalog](https://github.com/solven-eu/matmulcatalog) actual programs, recent applicable papers, equivalent constructions and public claims. Reports preserve the exact evidence and optional literature access gaps. Catalogue direct-form counts are distinguished from reduced schedules.

## Not claimed
No new tensor, multiplication-rank improvement, globally minimal addition count, practical runtime speedup, or result for another shape is claimed. This is a source-relative scheduling improvement in the ordinary-coordinate binary addition/subtraction convention.

## Credits
Credit `sfs` for this rescheduling contribution. [Andrew I. Perminov’s public repository](https://github.com/dronperminov/FastMatrixMultiplication) supplies the exact ternary tensor and source schedule. [Alexey Smirnov, as cited by Lille](https://fmm.univ-lille.fr/4x4x6.html), supplies the compared rational rank-73 algorithm, which is outside the candidate’s coefficient class. [matmulcatalog](https://github.com/solven-eu/matmulcatalog) and [calgulbenkian’s actual public submission17](https://github.com/elder-plinius/V3R1T4S/pull/17) supply further comparisons. Linear circuit transposition, cancellation and shared sums are established methods. [V3R1T4S](https://github.com/elder-plinius/V3R1T4S) supplies the protocol.

## License
Source code is offered under AGPL-3.0; contribution data and prose under CC BY 4.0. Underlying third-party works retain their authors' terms and attribution. The package distributes the derived schedule and our code, not third-party papers, pages, or reference datasets.
