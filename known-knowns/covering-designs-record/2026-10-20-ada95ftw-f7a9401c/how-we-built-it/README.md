# How the design was built
Python 3.13 with the pinned requirements.txt (numpy, ortools with its bundled SCIP solver).

## A. Clean rebuild (rebuild/; standalone)
rebuild/gsets.py builds PSL(2,7) (order 168), finds its subgroup classes by random 2-generation (seed 1, deterministic)
and lists its transitive coset actions of degree <= 40. rebuild/rebuild.py takes the actions with indices 3, 4 and 5
(degrees 14, 14 and 8; stabilisers of order 12, 12 and 21), places them side by side (points 1..14, 15..28, 29..36),
splits the 5-subsets and 3-subsets of the 36 points into PSL(2,7)-orbits (2364 block orbits), and solves the min-size
orbit set cover exactly (rebuild/kmcover.py, SCIP MIP via OR-tools, one thread, 120 s cap).
```sh
mkdir work && cd work && cp ../rebuild/*.py .
python3 rebuild.py
# prints: G-set [(14, 12), (14, 12), (8, 21)] OPTIMAL blocks 812 bound 812 valid True   (about 13 s)
python3 ../../verify-it-yourself/verify.py 36 5 3 rebuilt_812.txt 812
sort rebuilt_812.txt | cmp - <(sort ../../object/C36_5_3_812.txt) && echo same block set   # bash
```
On 2026-10-20 this rebuild printed OPTIMAL blocks 812 bound 812 in about 13 s, and rebuilt_812.txt was byte-identical
to object/C36_5_3_812.txt. OPTIMAL means 812 is the minimum within this one G-set only; it says nothing about
C(36,5,3) in general.

## B. The run's original search (code/)
code/sweep.py is the job-list builder from the earlier sweep (`jobs()` lists disjoint unions of 1-3 coset actions of
A5, S5, PSL(2,7), PGL(2,7), PSL(2,8), PGammaL(2,8), PSL(2,11) and A6 with 29 <= v <= 40 for C(v,k,3), k = 5, 6, 7;
`perms_for()` glues the actions). code/live_mip.py (usage: `live_mip.py cap worker nworkers outdir`) ran SCIP (60 s
cap, 1 thread) on the jobs an earlier run's LP screen marked LIVE, smallest orbit count first. Both import gsets and
kmcover from their own folder (copy rebuild/*.py next to them). Their only edits from the run: absolute workspace paths
became environment variables (V3R1T4S_RUN: a folder with data/coverdata.json, data/zenodo_coverdata.json,
data/coveringrepo_archive_vkt.txt and attempts/structured/output/ for the cached actions.pkl; V3R1T4S_LP_DIR: the LP
screen's live_jobs.json and lp_w*.jsonl, not included), and live_mip.py imports `sweep` instead of `sweep_1253`. The
third-party data files are not included; get the GitHub one with:
```sh
curl -sS -o data/coverdata.json https://raw.githubusercontent.com/dmgordo/LJCR/main/coverings/coverdata.json
```
The object is job 680, `(36, 5, 'PSL27', (3, 4, 5))`. Its row was `{"job": 680, "group": "PSL27", "combo": [3, 4, 5],
"orbits": [[14, 12], [14, 12], [8, 21]], "v": 36, "k": 5, "t": 3, "status": "OPTIMAL", "korb": 2364, "best": 812,
"bound": 812, "lp": 768.069, "table": 821, "sec": 10.2, "selfcheck": true}` and its output file is byte-identical to
the object. Use part A to rebuild.

PREREG.md is the run's preregistration (frozen 2026-10-20T22:57:10Z, before any attack output).
null_test: not needed (explicit object, deterministic exhaustive checker).
