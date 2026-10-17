# Reproduce: degree-diameter graphs

All commands are relative to the `known-knowns/biggest-graphs/` directory; rebuilt files go to `rebuilt/` (create it first with `mkdir -p rebuilt`; it is not part of the release). Requirements: a C compiler with pthreads, `python3` with `numpy`
(the rebuild scripts for the D=6 graphs also need `pandas`). Nothing here accesses the network except where a
download is spelled out.

## 1. Integrity

```sh
cd graphs
sha256sum G_15_4_n13365.edges G_15_3_n1620.edges.txt G_14_4_n8424.edges.txt G_9_4_n1700.edges G_13_4_n6630.edges   # macOS: shasum -a 256
gzip -dc G_13_6_n535495.edges.gz | sha256sum      # 4ed4fc62...0e94
gzip -dc G_15_6_n1424896.edges.gz | sha256sum     # 554149b5...7a75
```
Expected values are in `README.md` and `INDEX.csv`.

## 2. Exhaustive all-pairs check (the proof)

```sh
cc -O3 -o verify-it-yourself/ddcheck verify-it-yourself/ddcheck.c -lpthread
verify-it-yourself/ddcheck graphs/G_9_4_n1700.edges       9 4 4
verify-it-yourself/ddcheck graphs/G_15_3_n1620.edges.txt 15 3 4
verify-it-yourself/ddcheck graphs/G_14_4_n8424.edges.txt 14 4 4
verify-it-yourself/ddcheck graphs/G_15_4_n13365.edges    15 4 4
verify-it-yourself/ddcheck graphs/G_13_4_n6630.edges     13 4 4
gzip -dk graphs/G_13_6_n535495.edges.gz   && verify-it-yourself/ddcheck graphs/G_13_6_n535495.edges   13 6 8   # minutes
gzip -dk graphs/G_15_6_n1424896.edges.gz  && verify-it-yourself/ddcheck graphs/G_15_6_n1424896.edges  15 6 8   # tens of minutes
```
Expected last lines, each: `ordered_pairs_at_distance_gt_D=0 (of N*N)` and `VALID`. Expected headers:

| graph | N | edges | degree histogram | ordered pairs within distance r = 0..D |
|---|---|---|---|---|
| (9,4) | 1 700 | 7 650 | 9: 1700 | 1700, 17000, 132400, 939800, 2890000 |
| (15,3) | 1 620 | 12 150 | 15: 1620 | 1620, 25920, 330480, 2624400 |
| (14,4) | 8 424 | 58 968 | 14: 8424 | 8424, 126360, 1507896, 15875352, 70963776 |
| (15,4) | 13 365 | 100 035 | 14: 405, 15: 12960 | 13365, 213435, 2735775, 31533705, 178623225 |
| (13,4) | 6 630 | 43 086 | 11: 4, 12: 10, 13: 6616 | 6630, 92802, 1118358, 11694838, 43956900 |
| (13,6) | 535 495 | 3 475 214 | 11: 3656, 12: 3695, 13: 528144 | 535495, 7485923, 89790287, 942049209, 9768012797, 93215795805, 286754895025 |
| (15,6) | 1 424 896 | 10 671 340 | 13: 7681, 14: 15398, 15: 1401817 | 1424896, 22767576, 318479572, 3965655428, 49012939716, 571361673870, 2030328610816 |

Memory: the C checker uses 2·N·W·8 bytes per thread (W = 16 words = 1024 sources per batch): about 140 MB per thread
for (13,6) and 365 MB per thread for (15,6). Time scales with N²·D/1024; on a 10-core laptop the (13,6) run took
about 1–2 minutes with 10 threads at low load, and the (15,6) run is roughly seven times longer.

The numpy checker gives the same numbers for the five small graphs: `python3 verify-it-yourself/ddcheck.py graphs/G_9_4_n1700.edges 9 4`
etc. (seconds). Controls: pass `D-1` to either checker; every graph then reports far pairs > 0 and INVALID
(e.g. (9,4) at D=3: 1 950 200 far ordered pairs).

`sh verify-it-yourself/run_checks.sh` does all of the above (set `THREADS=8` and `BIG=1` to include the two large graphs).

## 3. Rebuild the graphs from their construction parameters (byte-identical)

```sh
# (15,4): numpy only
python3 how-we-built-it/15_4/gen_G_15_4_direct.py how-we-built-it/15_4/state_Z11x2Z30.json rebuilt/G154.edges
cmp rebuilt/G154.edges graphs/G_15_4_n13365.edges && echo IDENTICAL

# (15,3): pure python; also the algebraic diameter certificate
cd how-we-built-it/15_3
python3 rebuild_route_chart.py G_15_3_n1620.params.json ../../rebuilt/G153.edges controller_own_k5_n60.adj
cmp ../../rebuilt/G153.edges ../../graphs/G_15_3_n1620.edges.txt && echo IDENTICAL
python3 check_route_certificate.py G_15_3_n1620.params.json controller_own_k5_n60.adj   # CERTIFICATE VALID
cd ../..

# (14,4): numpy only (the params file embeds Bhakar's 104-vertex controller)
python3 how-we-built-it/14_4/rebuild_lift.py how-we-built-it/14_4/G_14_4_n8424.params.json rebuilt/G144.edges
cmp rebuilt/G144.edges graphs/G_14_4_n8424.edges.txt && echo IDENTICAL

# (9,4): pure python; re-verifies the W(7) geometry, the spread and the voltage, writes G_9_4_n1700.rebuilt.edges next to itself
python3 how-we-built-it/9_4/rebuild_1700.py          # prints the sha256, must be d271a1e8...7ebd
```

The two D=6 graphs are modifications of Rishabh Rajiv's published compound graphs, which are not redistributed here.
Download his dataset (Zenodo record 23052995, file `data-and-verification.zip`; the Zenodo API lists its md5) and
unzip it to `$Z`; it contains `graph_d13_k6_n534234.edges.xz`, `graph_d15_k6_n1424472.edges.xz` and the witness
files `witnesses/cs_d13_k6_n534234.json`, `witnesses/cs_d15_k6_n1424472.json`. Then (python3 with numpy and pandas):

```sh
# (13,6): bare compound from block 0 of Rajiv's graph, cut at the relaxed cut sets, plus the 46 740 certificate edges
cd how-we-built-it/13_6
python3 rebuild13.py $Z/graph_d13_k6_n534234.edges.xz $Z/witnesses/cs_d13_k6_n534234.json \
        SP_relaxed_t4055.json SL_relaxed_t4055.json G_13_6_n535495.extra_vs_compound.txt ../../rebuilt/G136.edges
# prints the self-test "rebuilt C' with Rajiv's cut sets == his published C'" and REBUILT ... sha256 4ed4fc62...0e94
cd ../..

# (15,6): compound at the larger cut sets, 7648 new vertices with seed 1, plus 9 shortcuts
cd how-we-built-it/15_6
python3 rebuild.py --rajiv $Z/graph_d15_k6_n1424472.edges.xz --witness $Z/witnesses/cs_d15_k6_n1424472.json \
        --sp H11_points_s5.json --sl H11_lines_s1.json --t 7648 --seed 1 \
        --shortcuts G_15_6_n1424896.shortcuts.npy --out ../../rebuilt/G156.edges
# prints "rebuilt N=1424896 m=10671340 maxdeg=15 sha256 554149b5...7a75"
cd ../..
```
`compound.py` checks on every run that, with Rajiv's own cut sets, it reproduces his published edge set exactly
(self-test), so the rebuild is anchored to his file. The (15,6) rebuild depends on numpy's `default_rng(1)` stream
(numpy >= 1.17); if a future numpy changes the generator the random part would differ, but the shipped edge list and
its all-pairs check do not depend on this.

The (13,4) graph comes from a local search (see `how-we-built-it/13_4/README.md`), so only its edge set is rebuilt, from
the near-miss parent and the 5-edge switch:

```sh
# (13,4): local search, so only the edge set is rebuilt, from the near-miss parent and the 5-edge switch
python3 how-we-built-it/13_4/apply_diff.py how-we-built-it/13_4/near_miss_N6630_cost2.edges \
        how-we-built-it/13_4/G_13_4_n6630.diff_vs_near_miss.txt graphs/G_13_4_n6630.edges      # EDGE SETS IDENTICAL
```

## Regenerate (the searches that produced the parameters and the (13,4) graph)

Section 3 rebuilds the graphs from their parameters. The code that *found* those parameters, and the local-search
chain behind the (13,4) graph, is in `how-we-built-it/<cell>/search/`; `how-we-built-it/README.md` lists, per cell,
the command, seed, runtime and what could not be recovered (python3 with numpy and numba; some cells also need
python-sat, galois or networkx, see each `requirements.txt`). The main (13,4) step, deterministic, about 3 minutes:

```sh
cd how-we-built-it/13_4 && mkdir -p rebuilt
cp near_miss_N6630_cost2.edges rebuilt/near_c134_N6630_s13064_c2.edges
python3 search/sa2_resume.py rebuilt/near_c134_N6630_s13064_c2.edges 13 4 rebuilt/sa2c2 --iters 250000 --T0 0.12 --T1 0.02 --seeds 101
cmp rebuilt/sa2c2_s101_c0.edges ../../graphs/G_13_4_n6630.edges && echo IDENTICAL
cd ../..
```

## 4. Compare with today's table

```sh
curl -sS -D headers.txt -o table.html https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html
sha256sum table.html            # 5482007a...bea3 was the version recorded on 2026-10-10
python3 the-record-we-beat/parse_comellas_table.py table.html cells.json
python3 -c "import json; c=json.load(open('cells.json')); [print(k, c[k]['raw'], 'bold' if c[k]['bold'] else '') for k in ['(15,4)','(15,3)','(14,4)','(9,4)','(13,4)','(13,6)','(15,6)']]"
```
One plain GET is enough; the page is small and changes often. If a cell now shows a value >= ours, that cell is no
longer exceeded by this release (see Corrections in `READ_BEFORE_CITING.md` at the repository root).

## Wrapper contract dependency

`verify-it-yourself/run_checks.sh` requires the standard-library helper
`../check_harness_contract.py`, relative to this family directory. Keep the normal
repository layout, or copy `known-knowns/check_harness_contract.py` beside any
standalone family copy. A missing helper fails explicitly with exit 2. The helper
validates completed negative-control evidence and/or indexed inventory; it does
not replace the scientific checker or independently prove its result.

For lightweight orchestration regressions from the repository root (Python 3.9+,
no scientific dependencies, downloads, or compiler):

```sh
python3 known-knowns/tests/harness_contracts/run_regressions.py --output /tmp/veritas-harness-results
```

These tests mock scientific commands and execute only the standard-library
contract helper. Root `SHA256SUMS` edits remain a maintainer-only step. Before merging, maintainers
must refresh entries for the changed wrappers/documents and add the helper and
regression files. The pinned 91419e28 manifest already has stale kit entries;
regenerate and verify the manifest against the final complete tree, rather than
assuming unchanged entries are current.
