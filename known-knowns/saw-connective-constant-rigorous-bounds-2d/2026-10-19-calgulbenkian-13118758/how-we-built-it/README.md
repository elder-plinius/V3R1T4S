# How we built it

Contributor material, unverified. Source copied from Argon's generator snapshot of 2026-10-19 (read-only; the snapshot taken at 05:47 UTC), file saw_bounds_2d.c (sha256 e49aab1197d5f061dbfff1c190b0b2a4bf1733f240c74c548627c8dc67cbf7fd before the edit below; byte-identical to the file in the earlier snapshot of 02:53 UTC), with one sanitising edit: the usage message printed by the program had angle-bracket placeholders, which were replaced by braces. Nothing else in the source was changed. The generator's sibling programs for other targets are not included.

This is the original generator. It has an indexing slip in its second pass (candidate lists are indexed by all free neighbours, not only kept ones). The orchestrator's builder compiled a copy with that slip fixed and with the vector solver replaced by a rounded-vector solver (16-bit mantissa); that copy gave the same 16,873,086 states and, for the same vector, the same exact fraction as the checker. That modified copy is not shipped.

## Provenance of the certificate

The author's run for loop length 34 with pocket pruning wrote a certificate file named cert_482_k34.txt (3,250,641,775 bytes, sha256 7079b8598c07cfe5724b5a126210c224082600b4c96c6015626f92949f19a204, as the orchestrator regenerated it). Our triage regenerated it by compiling and running saw_bounds_2d.c; the regenerated file is byte-identical to the one on the author's laptop, as reported to us (the builder did not see the author's copy). The object in object/ is not that certificate but a rounded (16-bit mantissa) copy of its vector, in state order, produced by the modified generator copy described above. The checker uses neither the author's code nor the author's transitions or vector.

## Commands

The snapshot documents the program's interface and the run it reports, but not the compile line or the shell history. As far as it is documented:

- Interface (from the program): saw_bounds_2d takes a lattice name (482, kagome, triangular or square), the maximum loop length k, an optional certificate file name, and an optional use_bridges mode (default 1; mode 2 adds finite-pocket pruning).
- The run for this claim, in shell form: saw_bounds_2d 482 34 cert_482_k34.txt 2 (the author reported 16,873,086 states in 101.78 s).
- The compile command is not recorded. The source includes only stdio, stdlib, stdint, string, math and time, and uses 128-bit integer arithmetic for the exact comparison, so a plain C compiler with optimisation and the math library should build it.
- The author's snapshot holds no PREREG.md for this target (the run was a direct construction, not a measurement against a null), so none is shipped. A null test is not required for this category.

## Reported results (excerpt of the author's results notes of the 02:53 UTC snapshot, local paths removed)

The best published rigorous upper bound the author compared with was 1.82926 (Jensen 2004 Table 3).

| Max loop k | Mode | States | Exact fraction max (MV)_i / V_i | Bound |
|---:|---|---:|---|---:|
| 22 | use_bridges=1 | 39,367 | 693444578290/377832855505 | 1.835321010829 |
| 28 | use_bridges=1 | 940,974 | 15540968660/8494170644 | 1.829604008601 |
| 30 | use_bridges=1 | 2,750,336 | 6792410744/3715467520 | 1.828144293400 |
| 30 | use_bridges=2 | 1,990,016 | 20081808562/10987138918 | 1.827755952835 |
| 32 | use_bridges=1 | 8,135,148 | 18108999119/9912056861 | 1.826966831703 |
| 32 | use_bridges=2 | 5,787,106 | 14988071382/8205358318 | 1.826619972113 |
| 34 | use_bridges=2 | 16,873,086 | 19360805483/10605620094 | 1.825523195381 |

The claim in this package is the loop length 34, use_bridges=2 automaton with the rounded shipped vector: 169287/92732 = 1.825551050339. The table's 34 row (1.825523195381) is the author's own full-precision figure, which is not claimed. The other rows are not claimed here (the k = 30 and k = 32 use_bridges=1 rows were the earlier states of pull request #534).
