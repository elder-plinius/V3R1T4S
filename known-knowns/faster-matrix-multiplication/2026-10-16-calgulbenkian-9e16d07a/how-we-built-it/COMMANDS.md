# Exact commands (opus-add)

All paths are relative to agents/addcomp/. Binaries: `cc -O2 -o src/{name} src/{source}` (table in src/README.md;
bpopt is built from src/bpopt_v1.c). The searches are time-capped random searches: re-running a command gives a valid
program but not necessarily the same one. The graph files listed are the actual outputs used; scheme.json is checkable
on its own with check_slp.py and sym_check.py.

## 0. Base scheme
Perminov file `data/schemes/5x5x5_m93_cr383_fv160_cn843_ZT_reduced.json` (sha256 808285b8fb393d2e...). Every product of scheme.json is a product of this file.

## 1. Driver runs that produced the map programs
tools/opt_scheme.py writes the map matrices (U: r x nm, V: r x mp, W^T: r x np for w_t jobs) and starts
one search process per job; job k gets seed = (sweep seed)*7 + k.

```
JOBSET=u:p:bp5a,u:p:bp5b,v:p:bp5a,v:p:bp5b,w:t:bp6s,w:t:bp6t python tools/opt_scheme.py data/schemes/5x5x5_m93_cr383_fv160_cn843_ZT_reduced.json 150 5 work/top150/5x5x5_m93
```

## 2. Per-map programs used

| map | command | output graph sha256 | final line of its log |
|---|---|---|---|
| U | `nice -n 19 src/bpopt5 work/top150/5x5x5_m93/u_p_bp5b.mat work/top150/5x5x5_m93/u_p_bp5b.graph 36 150` | 6818e71ecf6e1f4c | `best 87 iters 67039 K 93 N 25 D 74` |
| V | `nice -n 19 src/bpopt5 work/top150/5x5x5_m93/v_p_bp5a.mat work/top150/5x5x5_m93/v_p_bp5a.graph 37 150` | 8e085620ca211151 | `best 88 iters 58661 K 93 N 25 D 76` |
| W | `nice -n 19 src/bpopt6 work/top150/5x5x5_m93/w_t_bp6s.mat work/top150/5x5x5_m93/w_t_bp6s.graph 39 150 30 0.8 1 1` | 1bc485195aec97b4 | `best 89 iters 50964 K 93 N 25 D 76` |

Log lines give the search's own count before pruning unused nodes; for W it is the cost of the W^T program,
cost(W) = cost(W^T) + r - n*p after transposition (tools/graphs.py transpose).

## 3. Assembly into scheme.json
```
python3 tools/combine.py 5x5x5 93
python tools/package.py work/final/5x5x5_m93/strict.json work/final/5x5x5_m93/strict_summary.json
```
combine.py takes, per map, the cheapest verified program over all run directories of this tensor whose every intermediate
value is a ternary combination (strict), falling back to Perminov's own program when ours is not strictly better.

