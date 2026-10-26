# How the design was built
Python 3.13 with the pinned requirements.txt (numpy, ortools with SCIP).

## A. Clean rebuild (rebuild/rebuild.py; standalone)
rebuild/gsets.py builds the small groups and their transitive coset actions (rebuild/mr.py and rebuild/orbit_cover.py
are helpers it imports); rebuild/kmcover.py labels orbits of k- and t-subsets (numpy colex ranks) and solves the
minimum orbit set cover as a MIP with SCIP via OR-tools. rebuild/rebuild.py takes PSL(2,7) (order 168) on the disjoint
union of its coset space of degree 24 (stabiliser Z7) and one of degree 14 (stabiliser A4, either class), 38 points,
and solves the 6-subset orbit cover of all 3-subsets (120 s cap, 1 thread).
```sh
mkdir work && cp rebuild/*.py work/ && cd work
python3 rebuild.py
# prints, for each of the two 24+14 G-sets: "OPTIMAL blocks 469 bound 469 valid True"; writes rebuilt_469.txt
python3 ../../verify-it-yourself/verify.py 38 6 3 rebuilt_469.txt 469
```
On 2026-10-20 (16:44:07Z-16:44:25Z) this printed, for both G-sets, `G-set [(24, 7), (14, 12)] OPTIMAL blocks 469 bound
469 valid True`, and verify.py printed `VERIFIED C(38,6,3) <= 469` for rebuilt_469.txt. That rebuilt file is a
different set of 469 blocks from object/C38_6_3_469blocks.txt (the MIP has several optimal orbit choices); it has the
same size. 469 is optimal only within these G-sets, not globally.

## B. The run's original search (code/sweep.py)
`sweep.py cap threads worker_id nworkers outdir` builds the job list deterministically (groups above, 1-3 coset
actions, v = 29..40, k = 5..7, t = 3) and splits it round-robin. The run used 4 workers, then 2 (30 s cap, 1 thread,
nice 10, hard time cap). The object came from the row
`{"group": "PSL27", "orbits": [[24, 7], [14, 12]], "v": 38, "k": 6, "t": 3, "status": "OPTIMAL", "korb": 16578,
"torb": 59, "best": 469, "bound": 469, "snap": 510, "low_bd": 425, "sec": 8.6}` and its output file
C38_6_3_PSL27_24-14_469.txt is byte-identical to the object. The only edit to sweep.py is its run-folder path, which
now comes from the V3R1T4S_RUN environment variable. It reads the LJCR coverdata.json (used only to pick cells and
screen results; third-party data, not included):
```sh
mkdir -p data && curl -sS -o data/coverdata.json https://raw.githubusercontent.com/dmgordo/LJCR/main/coverings/coverdata.json
```
It imports gsets.py and kmcover.py from rebuild/ (copy them next to it).

PREREG.md is the preregistration of the run that found and panelled the design.
null_test: not needed (explicit object, deterministic exhaustive checker).
