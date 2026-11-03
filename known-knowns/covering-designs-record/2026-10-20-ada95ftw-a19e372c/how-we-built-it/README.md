# How the design was built
Python 3.13 with the pinned requirements.txt (numpy, ortools with its bundled SCIP solver).

## A. Clean rebuild (rebuild/; standalone)
rebuild/gsets.py builds S5 (order 120), finds its subgroup classes by random 2-generation (seed 1, deterministic)
and lists its transitive coset actions of degree <= 40. rebuild/rebuild.py takes the actions with indices 7, 10 and
13 (degrees 20, 10 and 5; stabilisers of order 6, 12 and 24), places them side by side (points 1..20, 21..30,
31..35), splits the 5-subsets (2966 orbits) and the 3-subsets (87 orbits) of the 35 points into S5-orbits, and solves
the min-size orbit set cover exactly (rebuild/kmcover.py, SCIP MIP via OR-tools, one thread, 120 s cap).
```sh
mkdir work && cd work && cp ../rebuild/*.py .
python3 rebuild.py
# prints: G-set [(20, 6), (10, 12), (5, 24)] OPTIMAL blocks 713 bound 713 valid True   (about 15 s)
python3 ../../verify-it-yourself/verify.py 35 5 3 rebuilt_713.txt 713
sort rebuilt_713.txt | cmp - <(sort ../../object/C35_5_3_713blocks.txt) && echo same block set   # bash
```
On 2026-10-20 this rebuild printed OPTIMAL blocks 713 bound 713 in 14 s, and rebuilt_713.txt was the same set of
blocks as object/C35_5_3_713blocks.txt (different line order). OPTIMAL means 713 is the minimum within this one
G-set only; it says nothing about C(35,5,3) in general. The other 20+10+5 G-sets of S5 reached only 768-780 blocks
within 120 s.

## B. The run's original search (code/sweep.py)
code/sweep.py (usage: `sweep.py cap threads worker nworkers outdir`) builds a deterministic job list of disjoint
unions of 1-3 coset actions of A5, S5, PSL(2,7), PGL(2,7), PSL(2,8), PGammaL(2,8), PSL(2,11) and A6 with 29 <= v <= 40,
for every C(v,k,3), k = 5, 6, 7, whose LJCR value is at least 5% above the Schonheim bound, and solves each with
kmcover.solve_mip. It imports gsets and kmcover from its own folder (copy rebuild/*.py next to it) and reads the
run folder (environment variable V3R1T4S_RUN) for data/coverdata.json (the dmgordo/LJCR GitHub file, used only to
pick cells and screen results; not included, third-party data) and a cached actions.pkl. Its only edit from the run
is that the run folder path is no longer an absolute path. Get the data with:
```sh
curl -sS -o data/coverdata.json https://raw.githubusercontent.com/dmgordo/LJCR/main/coverings/coverdata.json
```
The object came from phase 2 of the sweep (`sweep.py 30 1 0 2 output`, which skips the jobs phase 1 had finished).
Its row was `{"group": "S5", "orbits": [[20, 6], [10, 12], [5, 24]], "v": 35, "k": 5, "t": 3, "status": "OPTIMAL",
"korb": 2966, "torb": 87, "best": 713, "bound": 713, "snap": 733, "low_bd": 658, "sec": 13.7, "selfcheck": true}` and
its output file C35_5_3_S5_20-10-5_713.txt is byte-identical to the object. Use part A to rebuild.

PREREG.md is the run's preregistration (written 2026-10-20T12:57:48Z, before any attack output).
null_test: not needed (explicit object, deterministic exhaustive checker).
