# How the design was built
Python 3.13 with the pinned requirements.txt (ortools CP-SAT; networkx only for iso_check.py).

## A. Clean rebuild (rebuild/rebuild_a5.py; standalone, written separately from the run's code)
Build PSL(2,19) acting on PG(1,19) (points 0..18 and infinity = 19). Pick a random (order 2, order 3) pair whose product
has order 5 and take the order-60 closure (A5; element orders 1:1, 2:15, 3:20, 5:24). It is transitive on the 20
points. Split the 6-subsets into A5 orbits (681 orbits) and the triples into A5 orbits (21 orbits). Then solve the
min-weight orbit set cover exactly with CP-SAT.
```sh
mkdir work && cd work
python3 ../rebuild/rebuild_a5.py 1      # seed; prints "CP-SAT status OPTIMAL objective 70.0 bound 70.0", writes rebuilt_C20_6_3.txt
python3 ../../verify-it-yourself/verify.py 20 6 3 rebuilt_C20_6_3.txt 70
python3 ../rebuild/iso_check.py rebuilt_C20_6_3.txt ../../object/C20_6_3_70blocks.txt   # VF2 isomorphism of incidence graphs
```
The chosen orbits have sizes 20 + 20 + 30. Seeds 1-5 all gave 70, and every result was isomorphic to object/C20_6_3_70blocks.txt.
CP-SAT can pick among equal optima, so the labelling of the file can differ from run to run.

## B. The run's original search (code/)
code/subgroup_cover.py (usage: `subgroup_cover.py q extra maxck cap seed outdir`) searches A4/S4/A5 subgroups of PGL(2,q)
on PG(1,q) and imports code/orbit_cover.py. The object came from `python subgroup_cover.py 19 0 1000000 15 7 OUTDIR`,
row q=19, order 60, (20,6,3): OPTIMAL 70 (file C20_6_3_q19e0o60_70.txt, byte-identical to the object). code/coset_cover2.py
(`coset_cover2.py A5:Z3:0::6,3 1000000 60 OUTDIR 4`) finds the same value through A5 acting on cosets of Z3.
These scripts read `snap.json`, a {"C(v,k,t)": {"size", "low_bd"}} extract of the LJCR coverdata.json, used only to
pick cells and screen results. It is not included (third-party data). Rebuild it with:
```sh
curl -sS -o coverdata.json https://raw.githubusercontent.com/dmgordo/LJCR/main/coverings/coverdata.json
python3 -c "import json;d=json.load(open('coverdata.json'));json.dump({c:{'size':e['size'],'low_bd':e['low_bd']} for c,e in d.items()},open('snap.json','w'))"
```

PREREG.md is the run's preregistration (written 2026-10-17T13:05:18Z, before any attack output). null_test: not needed (explicit object, deterministic exhaustive checker).
