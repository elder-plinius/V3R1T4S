# 27 fewer additions for (4, 5, 8) matrix multiplication

Comparison scope is the survey recorded on 2026-10-14. In the original claim and panel text below, "live" and "fresh" refer to those dated checks. Current-record status has not been requalified; subsequent source-inventory access blocks remain respected. This submission claims the exact object and its improvement against the recorded comparison circuits.

## What
scheme.json (sha256 61917376617f1db0a75f5e9f5efd8bbd748713896418760b469126ea042ae5ee) is an exact integer ternary straight-line program for the ordered format (4, 5, 8) at the live listed rank 118, using 486 binary additions/subtractions, strictly below the applicable published counts examined in this audit, including Perminov's 513 and the immutable public PR 15 object's 507.

The object is stored at object/scheme.json. It reschedules the existing public rank-118 ternary decomposition, preserving every expanded factor. The stages save 10 + 7 + 10 additions relative to the 513-addition source. The actual 507-addition public PR 15 and verified compatible public mixtures are also higher by 21. Lille links a separate 419-addition raw program at rank 122; the comparison here fixes rank 118.

## Check it yourself
Run `sh verify-it-yourself/run_checks.sh` from this package directory. The final line is `PASS`. Two separate standard-library Python checkers execute every input basis pair and check all integer bilinear coefficients and literal operations. Observed local elapsed time and real output are in verify-it-yourself/RECEIPTS.md.

## Compared to
[Perminov's public reduced schedule](https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/addition_reduced_ZT/4x5x8_m118_cr513_fv249_cn1521_ZT_reduced.json) uses 513 additions at rank 118, stages 111+166+236. This schedule uses 486, stages 101+159+226. The full expanded tensor factors are identical. the-record-we-beat/snapshot.json records the live URL, UTC time, HTTP status, selected headers, source hash and extracted cell.

The fresh panel independently checked all matching reduced files, reduced_known.json, README and CHANGELOG, the [Lille format page](https://fmm.univ-lille.fr/4x5x8.html), [fmm_sota](https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json), [matmulcatalog](https://github.com/solven-eu/matmulcatalog) actual programs, recent applicable papers, equivalent constructions and public claims. Reports preserve the exact evidence and optional literature access gaps. Catalogue direct-form counts are distinguished from reduced schedules.

## Not claimed
No new tensor, multiplication-rank improvement, globally minimal addition count, practical runtime speedup, or result for another shape is claimed. This is a source-relative scheduling improvement in the ordinary-coordinate binary addition/subtraction convention.

## Credits
Credit `sfs` for this rescheduling contribution. [Andrew I. Perminov’s public repository](https://github.com/dronperminov/FastMatrixMultiplication) supplies the exact ternary tensor and source schedule. [Alexandre Sedoglavic’s Lille catalogue](https://fmm.univ-lille.fr/4x5x8.html), [Manuel Kauers, Jakob Moosbauer and Isaac Wood](https://arxiv.org/abs/2602.11041), [matmulcatalog](https://github.com/solven-eu/matmulcatalog), and [calgulbenkian’s public PR 15](https://github.com/elder-plinius/V3R1T4S/pull/15) supply compared algorithms and schedules. Linear circuit transposition, cancellation and shared sums are established methods. [V3R1T4S](https://github.com/elder-plinius/V3R1T4S) supplies the protocol.

## License
Source code is offered under AGPL-3.0; contribution data and prose under CC BY 4.0. Underlying third-party works retain their authors' terms and attribution. The package distributes the derived schedule and our code, not third-party papers, pages, or reference datasets.
