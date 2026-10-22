# Receipts (real output)

Full run_checks.sh, loaded machine (an earlier run alone on the machine took about 5 minutes for the all-sector step).

```
RESULT trace dims=2,2,2 l=4 vertices=32 perfect_matchings=546803712 tr(T^l)=546803712 all_matchings=1880275257729 tr(TMD^l)=1880275257729 EQUAL
PASS trace identity (2,2,2), l=4 
RESULT propc dims=2,2,2 |G|=192 HOLDS (dimer and monomer-dimer)
PASS property C (2,2,2) 
RESULT propc dims=3,2,2 |G|=24 HOLDS (dimer and monomer-dimer)
PASS property C (3,2,2) 
RESULT cert dims=3,3,2 sector=9 orbits=1404 listed_mismatches=0 u=1382 ratio=4527733104115888037323625277988191910329450496/3349983888759867418883092542107779072 bound=0.5840147693 ceil6=0.584015
PASS sector 9 exact ratio equals the shipped one; l4 <= 0.5840147693, rounded up 0.584015 87s
layer [3, 3, 2] |G|=36 N=18
  sector 0: 1 orbits (2.8s)
  sector 1: 1 orbits (5.8s)
  sector 2: 7 orbits (17.7s)
  sector 3: 29 orbits (61.8s)
  sector 4: 99 orbits (165.0s)
  sector 5: 256 orbits (315.5s)
  sector 6: 558 orbits (396.2s)
  sector 7: 922 orbits (453.1s)
  sector 8: 1275 orbits (495.3s)
  sector 9: 1404 orbits (512.8s)
RESULT dims=3,3,2 p=0 bound=0.5928456205 ceil6=0.592846 sector=9 ratio=1857397848/1
RESULT dims=3,3,2 p=1 bound=0.5842605035 ceil6=0.584261 sector=9 ratio=1833311847985449088/1344486016
RESULT dims=3,3,2 p=2 bound=0.5840228596 ceil6=0.584023 sector=9 ratio=2478568546142049439853627392/1833311847985449088
RESULT dims=3,3,2 p=3 bound=0.5840150050 ceil6=0.584016 sector=9 ratio=3349983888759867418883092542107779072/2478568546142049439853627392
RESULT dims=3,3,2 p=4 bound=0.5840147693 ceil6=0.584015 sector=9 ratio=4527733104115888037323625277988191910329450496/3349983888759867418883092542107779072
PASS all sectors at p=4: maximum 0.5840147693 in sector 9; equals the shipped ratio 
ALL CHECKS PASS

real	11m4.555s
user	5m42.615s
sys	0m1.051s

```

## Re-run after the rounding correction (orchestrator, 2026-10-19)

The checker now prints the ten-place bound rounded UP (0.5840147694); the earlier output above printed 0.5840147693, which was rounded to nearest and is not an upper bound. Real output of sh verify-it-yourself/run_checks.sh:

```
RESULT trace dims=2,2,2 l=4 vertices=32 perfect_matchings=546803712 tr(T^l)=546803712 all_matchings=1880275257729 tr(TMD^l)=1880275257729 EQUAL
PASS trace identity (2,2,2), l=4 
RESULT propc dims=2,2,2 |G|=192 HOLDS (dimer and monomer-dimer)
PASS property C (2,2,2) 
RESULT propc dims=3,2,2 |G|=24 HOLDS (dimer and monomer-dimer)
PASS property C (3,2,2) 
RESULT cert dims=3,3,2 sector=9 orbits=1404 listed_mismatches=0 u=1382 ratio=4527733104115888037323625277988191910329450496/3349983888759867418883092542107779072 bound=0.5840147693 ceil6=0.584015
PASS sector 9 exact ratio equals the shipped one; l4 <= 0.5840147694 (ten places, rounded up), rounded up to six places 0.584015 21s
layer [3, 3, 2] |G|=36 N=18
  sector 0: 1 orbits (0.6s)
  sector 1: 1 orbits (1.1s)
  sector 2: 7 orbits (4.8s)
  sector 3: 29 orbits (18.1s)
  sector 4: 99 orbits (51.2s)
  sector 5: 256 orbits (109.4s)
  sector 6: 558 orbits (181.2s)
  sector 7: 922 orbits (242.8s)
  sector 8: 1275 orbits (289.3s)
  sector 9: 1404 orbits (309.3s)
RESULT dims=3,3,2 p=0 bound=0.5928456205 ceil6=0.592846 sector=9 ratio=1857397848/1
RESULT dims=3,3,2 p=1 bound=0.5842605035 ceil6=0.584261 sector=9 ratio=1833311847985449088/1344486016
RESULT dims=3,3,2 p=2 bound=0.5840228596 ceil6=0.584023 sector=9 ratio=2478568546142049439853627392/1833311847985449088
RESULT dims=3,3,2 p=3 bound=0.5840150050 ceil6=0.584016 sector=9 ratio=3349983888759867418883092542107779072/2478568546142049439853627392
RESULT dims=3,3,2 p=4 bound=0.5840147693 ceil6=0.584015 sector=9 ratio=4527733104115888037323625277988191910329450496/3349983888759867418883092542107779072
PASS all sectors at p=4: maximum 0.5840147693 in sector 9; equals the shipped ratio 
ALL CHECKS PASS
sh claim/verify-it-yourself/run_checks.sh  339.12s user 4.86s system 96% cpu 5:55.74 total
```
