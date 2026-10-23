# 2 fewer additions for (2, 5, 6) matrix multiplication

Comparison scope is the survey recorded on 2026-10-14. In the original claim and panel text below, "live" and "fresh" refer to those dated checks. Current-record status has not been requalified; subsequent source-inventory access blocks remain respected. This submission claims the exact object and its improvement against the recorded comparison circuits.

## What
scheme.json exactly computes the full ⟨2,5,6⟩ product over Z with 47 bilinear products and 179 additions/subtractions under Perminov's reduced convention, two fewer than the live applicable 181-addition Perminov record and below the applicable Lille and matmulcatalog counts checked on 2026-10-14.

The object is stored at object/scheme.json. It reschedules an existing public decomposition, saving two additions in A preprocessing. The B stage, output reconstruction, and 47 products have the source values.

## Check it yourself
Run `sh verify-it-yourself/run_checks.sh` from this package directory. The final line is `PASS`. Two separate standard-library Python checkers execute every input basis pair and check all integer bilinear coefficients and literal operations. Observed local elapsed time and real output are in verify-it-yourself/RECEIPTS.md.

## Compared to
[Perminov's public reduced schedule](https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/addition_reduced_ZT/2x5x6_m47_cr181_fv63_cn332_ZT_reduced.json) uses 181 additions at rank 47, stages 40+65+76. This schedule uses 179, stages 38+65+76. The full expanded tensor factors are identical. the-record-we-beat/snapshot.json records the live URL, UTC time, HTTP status, selected headers, source hash and extracted cell.

The fresh panel independently checked all matching reduced files, reduced_known.json, README and CHANGELOG, the [Lille format page](https://fmm.univ-lille.fr/2x5x6.html), [fmm_sota](https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json), [matmulcatalog](https://github.com/solven-eu/matmulcatalog) actual programs, recent applicable papers, equivalent constructions and public claims. Reports preserve the exact evidence and optional literature access gaps. Catalogue direct-form counts are distinguished from reduced schedules.

## Not claimed
No new tensor, multiplication-rank improvement, globally minimal addition count, practical runtime speedup, or result for another shape is claimed. This is a source-relative scheduling improvement in the ordinary-coordinate binary addition/subtraction convention.

## Credits
Credit `sfs` for this rescheduling contribution. The reference 181-addition schedule comes from [Andrew I. Perminov](https://github.com/dronperminov/FastMatrixMultiplication). The factorization is the [AlphaEvolve rank 47 construction by Alexander Novikov and coauthors at Google DeepMind](https://arxiv.org/abs/2506.13131), as credited in [Alexandre Sedoglavic's Lille catalogue](https://fmm.univ-lille.fr/2x5x6.html). [matmulcatalog](https://github.com/solven-eu/matmulcatalog) supplies further programs and comparison data. Circuit transposition and common-subexpression elimination are established methods; no invention of these techniques is claimed. [V3R1T4S](https://github.com/elder-plinius/V3R1T4S) supplies the research and three-skeptic protocol.

## License
Source code is offered under AGPL-3.0; contribution data and prose under CC BY 4.0. Underlying third-party works retain their authors' terms and attribution. The package distributes the derived schedule and our code, not third-party papers, pages, or reference datasets.
