# How the design was built
Python 3.13 with the pinned requirements.txt (ortools CP-SAT).

## A. Clean rebuild (rebuild/rebuild_psl27.py; standalone)
Build PSL(2,7) (order 168) on PG(1,7) from x->x+1, x->2x, x->-1/x. Find its subgroups of order 12 (A4) by random
2-generation (seed 1) and split them into conjugacy classes (there are two). Each class gives a transitive action on
14 cosets. The G-set is the disjoint union of one 14-point action from each class plus one fixed point (v = 29).
Split the 5-subsets (792 orbits) and the 3-subsets (37 orbits) into orbits, then solve the min-size orbit set cover
with CP-SAT (single worker).
```sh
mkdir work && cd work
python3 ../rebuild/rebuild_psl27.py 20 rebuilt_C29_5_3.txt
# prints one line per A4-class pair; the pair (0, 1) gives "CP-SAT FEASIBLE blocks 399 bound 0"; about 1 minute
python3 ../../verify-it-yourself/verify.py 29 5 3 rebuilt_C29_5_3.txt 399
sort rebuilt_C29_5_3.txt | cmp - <(sort ../../object/C29_5_3_399blocks.txt) && echo same block set   # bash
python3 ../rebuild/rebuild_psl27.py --orbits ../../object/C29_5_3_399blocks.txt
# the object is a union of orbits for the pair (0, 1) only
```
On 2026-10-19 the rebuild with a 20 s cap per pair gave the pairs (0,0): 469, (0,1): 399, (1,1): 462 blocks, and the
399-block result was the same set of blocks as object/C29_5_3_399blocks.txt (different line order). The solve is
time-capped (FEASIBLE, not OPTIMAL), so a different machine or cap can give a different value; 399 is not claimed
optimal in this family.

## B. The run's original search (code/)
code/msum_cover.py (usage: `msum_cover.py cap maxck outdir worker nworkers`) sweeps disjoint unions of 1-3 coset actions
of A5, S5 and PSL(2,7) for v = 10..32 against every open table cell with 3 <= t <= 5, and imports code/orbit_cover.py.
The object came from code/msum_resume.py, the same sweep resumed after an earlier run's jobs:
`python3 msum_resume.py 20 700000 out 3 4` (worker 3 of 4, 20 s cap per job). Its row was
`{"group": "PSL27", "orbits": [[14, 12], [14, 12], [1, 168]], "v": 29, "k": 5, "t": 3, "korb": 792, "torb": 37,
"status": "FEASIBLE", "snap": 413, "low_bd": 366, "best": 399}` and its output file C29_5_3_PSL27_14-14-1_399.txt is
byte-identical to the object. The scripts read the LJCR coverdata.json (used only to pick cells and screen results;
not included, third-party data) and msum_resume.py also reads the earlier run's result files to skip finished jobs,
so they are included as a record of the method; use part A to rebuild. Get the data with:
```sh
curl -sS -o coverdata.json https://raw.githubusercontent.com/dmgordo/LJCR/main/coverings/coverdata.json
```

PREREG.md is the preregistration of the run that verified, tried to improve and panelled the design (written
2026-10-19T23:03Z). PREREG_run_2026-10-19-1303.md is the preregistration of the run that found it (written
2026-10-19T13:07:34Z, before any attack output). null_test: not needed (explicit object, deterministic exhaustive checker).
