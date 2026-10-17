# Exact commands (opus-add)

All paths are relative to agents/addcomp/. Binaries: `cc -O2 -o src/{name} src/{source}` (table in src/README.md;
bpopt is built from src/bpopt_v1.c). The searches are time-capped random searches: re-running a command gives a valid
program but not necessarily the same one. The graph files listed are the actual outputs used; scheme.json is checkable
on its own with check_slp.py and sym_check.py.

## 0. Base scheme
Perminov file `data/schemes/2x4x7_m45_cr174_cn308_ZT_reduced.json` (sha256 b839eb6e30cfd9e0...). Every product of scheme.json is a product of this file.

## 1. Driver runs that produced the map programs
tools/opt_scheme.py writes the map matrices (U: r x nm, V: r x mp, W^T: r x np for w_t jobs) and starts
one search process per job; job k gets seed = (sweep seed)*7 + k.

```
python tools/opt_scheme.py data/schemes/2x4x7_m45_cr174_cn308_ZT_reduced.json 60 1 work/bp60/2x4x7_m45
```

## 2. Per-map programs used

| map | command | output graph sha256 | final line of its log |
|---|---|---|---|
| U | none: Perminov's own program from the base file, copied unchanged (`u_fresh`, `u`) | - | - |
| V | `nice -n 19 src/bpopt work/bp60/2x4x7_m45/v_p.mat work/bp60/2x4x7_m45/v_p_bp.graph 8 60` | dd4f9ec2df4d5c3d | `best 67 iters 47126 K 45 N 28 D 41` |
| W | `nice -n 19 src/bpopt work/bp60/2x4x7_m45/w_t.mat work/bp60/2x4x7_m45/w_t_bp.graph 9 60` | 8198ef6ca67b8a2b | `best 36 iters 1162875 K 45 N 14 D 36` |

Log lines give the search's own count before pruning unused nodes; for W it is the cost of the W^T program,
cost(W) = cost(W^T) + r - n*p after transposition (tools/graphs.py transpose).

## 3. Assembly into scheme.json
```
python3 tools/combine.py 2x4x7 45
python tools/package.py work/final/2x4x7_m45/strict.json work/final/2x4x7_m45/strict_summary.json
```
combine.py takes, per map, the cheapest verified program over all run directories of this tensor whose every intermediate
value is a ternary combination (strict), falling back to Perminov's own program when ours is not strictly better.

