# Current wrapper receipt (2026-10-17)

Real end-to-end run on macOS arm64 (Darwin 27.0.0), Apple clang 21.0.0, Python 3.11.17, NumPy 2.4.6.
`THREADS=4`; exit code **0**; 5.19 s wall clock (started 2026-10-17T23:54:04Z).
The graph files, `ddcheck.c`, `ddcheck.py` and the (13,4) near-miss parent are byte-identical to upstream commit
`04fdfba48c6e277fe083b6811f1a5deb3c52b74e`. These are actual scientific checker outputs, not synthetic fixture output.

All five small graphs ran with both checkers, and all six negative controls ran (each graph at D-1, and the (13,4)
near-miss parent with exactly 4 far ordered pairs); `known-knowns/check_harness_contract.py` accepted each control
(`HARNESS CONTROL PASS`). The two D=6 graphs (`BIG=1`) were not rerun: that part of the wrapper did not change, and
its 2026-10-10 output is kept in the historical receipts below.

Command (from this family directory):

```sh
THREADS=4 sh verify-it-yourself/run_checks.sh
```

Exact source and output SHA-256:

- `run_checks.sh`: `3aa04765c5c600dbeb9d1c74735a5db51304ec2142d0bf057e30213ac40e0a25`
- `ddcheck.c`: `bb01dacafd49c6a037610adf9d93e300c014dded298b85da5f3caf1d25527477`
- `ddcheck.py`: `ca62ae8e08617bb63543ce878a3804b9f6459c0f34e570f53aa0a720e4b56e28`
- `known-knowns/check_harness_contract.py`: `f0f43ba4ab6970001f228affb5a95f9ec5d37b115f8487c7ce4cc11ce9e5a070`
- Combined stdout/stderr below: `dbae79411307aa8342b013b38ef043463956da0404d8f9cd9887a14d12ba618d`

Paths in the output are relative to `known-knowns/biggest-graphs/`: the absolute checkout prefix was removed, and
nothing else was changed.

## Complete current output

```text
== compile
== G_9_4_n1700.edges (Delta=9, D=4)
sha256 ok
file=graphs/G_9_4_n1700.edges
N=1700 edges=7650 loops=0 duplicates=0 unused_labels=0 mindeg=9 maxdeg=9 (DELTA=9, D=4)
degree_histogram: 9:1700
ordered_pairs_within_distance: r=0:1700 r=1:17000 r=2:132400 r=3:939800 r=4:2890000
ordered_pairs_at_distance_gt_4=0 (of 2890000)
VALID
{"file": "graphs/G_9_4_n1700.edges", "N": 1700, "edges": 7650, "loops": 0, "duplicates": 0, "unparsable_lines": 0, "unused_labels": 0, "mindeg": 9, "maxdeg": 9, "DELTA": 9, "D": 4, "degree_histogram": {"9": 1700}, "ordered_pairs_within_distance": {"0": 1700, "1": 17000, "2": 132400, "3": 939800, "4": 2890000}, "far_pairs": 0, "valid": true}
-- control at D-1 (must be INVALID):
ordered_pairs_at_distance_gt_3=1950200 (of 2890000)
INVALID
HARNESS CONTROL PASS graph: expected semantic rejection
== G_15_3_n1620.edges.txt (Delta=15, D=3)
sha256 ok
file=graphs/G_15_3_n1620.edges.txt
N=1620 edges=12150 loops=0 duplicates=0 unused_labels=0 mindeg=15 maxdeg=15 (DELTA=15, D=3)
degree_histogram: 15:1620
ordered_pairs_within_distance: r=0:1620 r=1:25920 r=2:330480 r=3:2624400
ordered_pairs_at_distance_gt_3=0 (of 2624400)
VALID
{"file": "graphs/G_15_3_n1620.edges.txt", "N": 1620, "edges": 12150, "loops": 0, "duplicates": 0, "unparsable_lines": 0, "unused_labels": 0, "mindeg": 15, "maxdeg": 15, "DELTA": 15, "D": 3, "degree_histogram": {"15": 1620}, "ordered_pairs_within_distance": {"0": 1620, "1": 25920, "2": 330480, "3": 2624400}, "far_pairs": 0, "valid": true}
-- control at D-1 (must be INVALID):
ordered_pairs_at_distance_gt_2=2293920 (of 2624400)
INVALID
HARNESS CONTROL PASS graph: expected semantic rejection
== G_14_4_n8424.edges.txt (Delta=14, D=4)
sha256 ok
file=graphs/G_14_4_n8424.edges.txt
N=8424 edges=58968 loops=0 duplicates=0 unused_labels=0 mindeg=14 maxdeg=14 (DELTA=14, D=4)
degree_histogram: 14:8424
ordered_pairs_within_distance: r=0:8424 r=1:126360 r=2:1507896 r=3:15875352 r=4:70963776
ordered_pairs_at_distance_gt_4=0 (of 70963776)
VALID
{"file": "graphs/G_14_4_n8424.edges.txt", "N": 8424, "edges": 58968, "loops": 0, "duplicates": 0, "unparsable_lines": 0, "unused_labels": 0, "mindeg": 14, "maxdeg": 14, "DELTA": 14, "D": 4, "degree_histogram": {"14": 8424}, "ordered_pairs_within_distance": {"0": 8424, "1": 126360, "2": 1507896, "3": 15875352, "4": 70963776}, "far_pairs": 0, "valid": true}
-- control at D-1 (must be INVALID):
ordered_pairs_at_distance_gt_3=55088424 (of 70963776)
INVALID
HARNESS CONTROL PASS graph: expected semantic rejection
== G_15_4_n13365.edges (Delta=15, D=4)
sha256 ok
file=graphs/G_15_4_n13365.edges
N=13365 edges=100035 loops=0 duplicates=0 unused_labels=0 mindeg=14 maxdeg=15 (DELTA=15, D=4)
degree_histogram: 14:405 15:12960
ordered_pairs_within_distance: r=0:13365 r=1:213435 r=2:2735775 r=3:31533705 r=4:178623225
ordered_pairs_at_distance_gt_4=0 (of 178623225)
VALID
{"file": "graphs/G_15_4_n13365.edges", "N": 13365, "edges": 100035, "loops": 0, "duplicates": 0, "unparsable_lines": 0, "unused_labels": 0, "mindeg": 14, "maxdeg": 15, "DELTA": 15, "D": 4, "degree_histogram": {"14": 405, "15": 12960}, "ordered_pairs_within_distance": {"0": 13365, "1": 213435, "2": 2735775, "3": 31533705, "4": 178623225}, "far_pairs": 0, "valid": true}
-- control at D-1 (must be INVALID):
ordered_pairs_at_distance_gt_3=147089520 (of 178623225)
INVALID
HARNESS CONTROL PASS graph: expected semantic rejection
== G_13_4_n6630.edges (Delta=13, D=4)
sha256 ok
file=graphs/G_13_4_n6630.edges
N=6630 edges=43086 loops=0 duplicates=0 unused_labels=0 mindeg=11 maxdeg=13 (DELTA=13, D=4)
degree_histogram: 11:4 12:10 13:6616
ordered_pairs_within_distance: r=0:6630 r=1:92802 r=2:1118358 r=3:11694838 r=4:43956900
ordered_pairs_at_distance_gt_4=0 (of 43956900)
VALID
{"file": "graphs/G_13_4_n6630.edges", "N": 6630, "edges": 43086, "loops": 0, "duplicates": 0, "unparsable_lines": 0, "unused_labels": 0, "mindeg": 11, "maxdeg": 13, "DELTA": 13, "D": 4, "degree_histogram": {"11": 4, "12": 10, "13": 6616}, "ordered_pairs_within_distance": {"0": 6630, "1": 92802, "2": 1118358, "3": 11694838, "4": 43956900}, "far_pairs": 0, "valid": true}
-- control at D-1 (must be INVALID):
ordered_pairs_at_distance_gt_3=32262062 (of 43956900)
INVALID
HARNESS CONTROL PASS graph: expected semantic rejection
-- control: the (13,4) near-miss parent (how-we-built-it/13_4) must be INVALID with exactly 4 far ordered pairs:
ordered_pairs_at_distance_gt_4=4 (of 43956900)
INVALID
HARNESS CONTROL PASS graph: expected semantic rejection
== large graphs skipped (set BIG=1)
ALL CHECKS PASSED
```

---

## Historical receipts

The records below are preserved from earlier runs of the former wrapper. Their
wrapper messages do not describe the current run; use the complete current
output above for the current wrapper contract. Historical comparison dates and
optional-runtime coverage remain those stated in the original records.

# Check results (degree-diameter graphs)

All seven graphs were checked with the release checkers on the shipped files on 2026-10-10 on the build machine
(macOS, 10 cores, load average about 80–110 from other jobs). Paths in the raw output are relative to
`known-knowns/biggest-graphs/`.

| graph | sha256 (= INDEX.csv) | N | edges | loops / dup / unused | degree histogram | ordered pairs at distance > D | C checker | numpy checker | control at D−1 |
|---|---|---|---|---|---|---|---|---|---|
| (9,4) `G_9_4_n1700.edges` | d271a1e8…7ebd | 1 700 | 7 650 | 0 / 0 / 0 | 9: 1700 | 0 of 2 890 000 | VALID | valid | 1 950 200 far, INVALID |
| (15,3) `G_15_3_n1620.edges.txt` | da9faa8c…92ce | 1 620 | 12 150 | 0 / 0 / 0 | 15: 1620 | 0 of 2 624 400 | VALID | valid | 2 293 920 far, INVALID |
| (14,4) `G_14_4_n8424.edges.txt` | 71ef820b…f281 | 8 424 | 58 968 | 0 / 0 / 0 | 14: 8424 | 0 of 70 963 776 | VALID | valid | 55 088 424 far, INVALID |
| (15,4) `G_15_4_n13365.edges` | 2d368140…e52f | 13 365 | 100 035 | 0 / 0 / 0 | 14: 405, 15: 12960 | 0 of 178 623 225 | VALID | valid | 147 089 520 far, INVALID |
| (13,4) `G_13_4_n6630.edges` (new) | 7c44e128…10a4 | 6 630 | 43 086 | 0 / 0 / 0 | 11: 4, 12: 10, 13: 6616 | 0 of 43 956 900 | VALID | valid | 32 262 062 far, INVALID |
| (13,6) `G_13_6_n535495.edges.gz` | 4ed4fc62…0e94 | 535 495 | 3 475 214 | 0 / 0 / 0 | 11: 3656, 12: 3695, 13: 528144 | 0 of 286 754 895 025 | VALID (340.22 s, 6 threads) | — | — |
| (15,6) `G_15_6_n1424896.edges.gz` | 554149b5…7a75 | 1 424 896 | 10 671 340 | 0 / 0 / 0 | 13: 7681, 14: 15398, 15: 1401817 | 0 of 2 030 328 610 816 | VALID (2618.62 s, 6 threads) | — | — |

Additional control: the (13,4) near-miss parent `how-we-built-it/13_4/near_miss_N6630_cost2.edges` is INVALID with
exactly 4 ordered pairs at distance 5 (the 2 unordered far pairs that the 5-edge switch removes), and
`how-we-built-it/13_4/apply_diff.py` rebuilds the edge set of the shipped (13,4) graph from it (EDGE SETS IDENTICAL).
The release checker ran to completion on both D=6 graphs. Toy controls of the checker (earlier run, same code): Petersen
graph VALID at D=2 and INVALID at D=1; 7-cycle VALID at D=3, INVALID at D=2; a duplicated edge, a loop and a label
gap each INVALID.

## Raw output: `THREADS=4 sh verify-it-yourself/run_checks.sh` (five small graphs, both checkers, controls)

```
2026-10-10T19:34:16Z
== compile
== G_9_4_n1700.edges (Delta=9, D=4)
sha256 ok
file=graphs/G_9_4_n1700.edges
N=1700 edges=7650 loops=0 duplicates=0 unused_labels=0 mindeg=9 maxdeg=9 (DELTA=9, D=4)
degree_histogram: 9:1700
ordered_pairs_within_distance: r=0:1700 r=1:17000 r=2:132400 r=3:939800 r=4:2890000
ordered_pairs_at_distance_gt_4=0 (of 2890000)
VALID
{"file": "graphs/G_9_4_n1700.edges", "N": 1700, "edges": 7650, "loops": 0, "duplicates": 0, "unparsable_lines": 0, "unused_labels": 0, "mindeg": 9, "maxdeg": 9, "DELTA": 9, "D": 4, "degree_histogram": {"9": 1700}, "ordered_pairs_within_distance": {"0": 1700, "1": 17000, "2": 132400, "3": 939800, "4": 2890000}, "far_pairs": 0, "valid": true}
-- control at D-1 (must be INVALID):
ordered_pairs_at_distance_gt_3=1950200 (of 2890000)
INVALID
== G_15_3_n1620.edges.txt (Delta=15, D=3)
sha256 ok
file=graphs/G_15_3_n1620.edges.txt
N=1620 edges=12150 loops=0 duplicates=0 unused_labels=0 mindeg=15 maxdeg=15 (DELTA=15, D=3)
degree_histogram: 15:1620
ordered_pairs_within_distance: r=0:1620 r=1:25920 r=2:330480 r=3:2624400
ordered_pairs_at_distance_gt_3=0 (of 2624400)
VALID
{"file": "graphs/G_15_3_n1620.edges.txt", "N": 1620, "edges": 12150, "loops": 0, "duplicates": 0, "unparsable_lines": 0, "unused_labels": 0, "mindeg": 15, "maxdeg": 15, "DELTA": 15, "D": 3, "degree_histogram": {"15": 1620}, "ordered_pairs_within_distance": {"0": 1620, "1": 25920, "2": 330480, "3": 2624400}, "far_pairs": 0, "valid": true}
-- control at D-1 (must be INVALID):
ordered_pairs_at_distance_gt_2=2293920 (of 2624400)
INVALID
== G_14_4_n8424.edges.txt (Delta=14, D=4)
sha256 ok
file=graphs/G_14_4_n8424.edges.txt
N=8424 edges=58968 loops=0 duplicates=0 unused_labels=0 mindeg=14 maxdeg=14 (DELTA=14, D=4)
degree_histogram: 14:8424
ordered_pairs_within_distance: r=0:8424 r=1:126360 r=2:1507896 r=3:15875352 r=4:70963776
ordered_pairs_at_distance_gt_4=0 (of 70963776)
VALID
{"file": "graphs/G_14_4_n8424.edges.txt", "N": 8424, "edges": 58968, "loops": 0, "duplicates": 0, "unparsable_lines": 0, "unused_labels": 0, "mindeg": 14, "maxdeg": 14, "DELTA": 14, "D": 4, "degree_histogram": {"14": 8424}, "ordered_pairs_within_distance": {"0": 8424, "1": 126360, "2": 1507896, "3": 15875352, "4": 70963776}, "far_pairs": 0, "valid": true}
-- control at D-1 (must be INVALID):
ordered_pairs_at_distance_gt_3=55088424 (of 70963776)
INVALID
== G_15_4_n13365.edges (Delta=15, D=4)
sha256 ok
file=graphs/G_15_4_n13365.edges
N=13365 edges=100035 loops=0 duplicates=0 unused_labels=0 mindeg=14 maxdeg=15 (DELTA=15, D=4)
degree_histogram: 14:405 15:12960
ordered_pairs_within_distance: r=0:13365 r=1:213435 r=2:2735775 r=3:31533705 r=4:178623225
ordered_pairs_at_distance_gt_4=0 (of 178623225)
VALID
{"file": "graphs/G_15_4_n13365.edges", "N": 13365, "edges": 100035, "loops": 0, "duplicates": 0, "unparsable_lines": 0, "unused_labels": 0, "mindeg": 14, "maxdeg": 15, "DELTA": 15, "D": 4, "degree_histogram": {"14": 405, "15": 12960}, "ordered_pairs_within_distance": {"0": 13365, "1": 213435, "2": 2735775, "3": 31533705, "4": 178623225}, "far_pairs": 0, "valid": true}
-- control at D-1 (must be INVALID):
ordered_pairs_at_distance_gt_3=147089520 (of 178623225)
INVALID
== G_13_4_n6630.edges (Delta=13, D=4)
sha256 ok
file=graphs/G_13_4_n6630.edges
N=6630 edges=43086 loops=0 duplicates=0 unused_labels=0 mindeg=11 maxdeg=13 (DELTA=13, D=4)
degree_histogram: 11:4 12:10 13:6616
ordered_pairs_within_distance: r=0:6630 r=1:92802 r=2:1118358 r=3:11694838 r=4:43956900
ordered_pairs_at_distance_gt_4=0 (of 43956900)
VALID
{"file": "graphs/G_13_4_n6630.edges", "N": 6630, "edges": 43086, "loops": 0, "duplicates": 0, "unparsable_lines": 0, "unused_labels": 0, "mindeg": 11, "maxdeg": 13, "DELTA": 13, "D": 4, "degree_histogram": {"11": 4, "12": 10, "13": 6616}, "ordered_pairs_within_distance": {"0": 6630, "1": 92802, "2": 1118358, "3": 11694838, "4": 43956900}, "far_pairs": 0, "valid": true}
-- control at D-1 (must be INVALID):
ordered_pairs_at_distance_gt_3=32262062 (of 43956900)
INVALID
-- control: the (13,4) near-miss parent (how-we-built-it/13_4) must be INVALID with exactly 4 far ordered pairs:
ordered_pairs_at_distance_gt_4=4 (of 43956900)
INVALID
== large graphs skipped (set BIG=1)
ALL CHECKS PASSED
THREADS=4 sh verify-it-yourself/run_checks.sh  4.84s user 0.92s system 26% cpu 21.391 total
2026-10-10T19:34:37Z
```

## Raw output: C checker on the two decompressed D=6 graphs (`ddcheck FILE Δ 6 6`)

```
2026-10-10T19:23:45Z
4ed4fc62000b3cbc6c23b08d9db4af383aa28b01e69fc802b5b1bbdbab170e94  G_13_6_n535495.edges (decompressed)
file=G_13_6_n535495.edges (decompressed)
N=535495 edges=3475214 loops=0 duplicates=0 unused_labels=0 mindeg=11 maxdeg=13 (DELTA=13, D=6)
degree_histogram: 11:3656 12:3695 13:528144
ordered_pairs_within_distance: r=0:535495 r=1:7485923 r=2:89790287 r=3:942049209 r=4:9768012797 r=5:93215795805 r=6:286754895025
ordered_pairs_at_distance_gt_6=0 (of 286754895025)
VALID
real 340.22
user 495.60
sys 5.63
2026-10-10T19:29:26Z
554149b59ffe151197dff3ae48ae315596d9c618924d25db4775b1315ab47a75  G_15_6_n1424896.edges (decompressed)
file=G_15_6_n1424896.edges (decompressed)
N=1424896 edges=10671340 loops=0 duplicates=0 unused_labels=0 mindeg=13 maxdeg=15 (DELTA=15, D=6)
degree_histogram: 13:7681 14:15398 15:1401817
ordered_pairs_within_distance: r=0:1424896 r=1:22767576 r=2:318479572 r=3:3965655428 r=4:49012939716 r=5:571361673870 r=6:2030328610816
ordered_pairs_at_distance_gt_6=0 (of 2030328610816)
VALID
real 2618.62
user 4446.85
sys 28.72
2026-10-10T20:13:08Z
```

## Rebuilds from construction parameters (2026-10-09; not rerun for this release)

- (15,4): `gen_G_15_4_direct.py state_Z11x2Z30.json` → byte-identical to `G_15_4_n13365.edges` (11 s).
- (15,3): `rebuild_route_chart.py` → byte-identical to `G_15_3_n1620.edges.txt`; `check_route_certificate.py`:
  "(R) ok: all 3300 non-adjacent ordered pairs have a rank-3 walk of length 3; (P) ok: all 300 adjacent ordered pairs
  have a complete pencil of 4 planes; CERTIFICATE VALID: the lift (order 1620, 15-regular) has diameter <= 3".
- (14,4): `rebuild_lift.py` → byte-identical to `G_14_4_n8424.edges.txt`.
- (9,4): `rebuild_1700.py` → "geometry OK; N = 1700 edges = 7650; sha256 d271a1e8…7ebd", byte-identical.
- (13,6): `rebuild13.py` with Rajiv's published `graph_d13_k6_n534234.edges.xz` (sha256 of the compressed file
  c86346b121a6f24591ae12dbf0a9f8dfb4a82f3c8cea25339c11139140b95bae) and his witness file, the two relaxed cut sets and
  the certificate file → "self-test: rebuilt C' with Rajiv's cut sets == his published C'" then
  "REBUILT N 535495 M 3475214 sha256 4ed4fc62…0e94", i.e. byte-identical (96 s).
- (15,6): not rerun for this release (the author's run of the same `rebuild.py` on 2026-10-06 reported
  "rebuilt N=1424896 m=10671340 maxdeg=15 sha256 554149b5…7a75"; the command is in `RUN_IT_YOURSELF.md`).


## Earlier independent checks of the large graphs

Before this release, (13,6) had passed four separately written exhaustive checkers and (15,6) three, all on files
with the same sha256 and all reporting 0 far pairs; none of those checkers is shipped.
