# Receipts (real output)

Default run_checks.sh (Python sector 12; C for all 13 sectors) on a 28-core Apple M3 Ultra, run at the same time as two other long jobs (heavily loaded). Python sector 12 alone took 158 s on 24 processes in an earlier, less loaded run. Python sectors 11, 10, 9 with CW_SMALL=1 (16 processes, loaded): 293 s, 687 s, 214 s, same ratios as C (sector 11: 282404744906972997897/49494065286; sector 10: 301133314805378772813/69324082204; sector 9: 363203564097052574687/126318622370).

```
PASS object parts and whole sha256 8d6198121bb490e8f44f352114144556fd75cc33aa98b4f698335ca274342661
RESULT trace dims=2,2 l=4 vertices=16 perfect_matchings=4752 tr(T^l)=4752 all_matchings=306305 tr(TMD^l)=306305 EQUAL
RESULT trace dims=3,2 l=4 vertices=24 perfect_matchings=194244 tr(T^l)=194244 all_matchings=162589284 tr(TMD^l)=162589284 EQUAL
RESULT trace dims=2,2 l=6 vertices=24 perfect_matchings=190992 tr(T^l)=190992 all_matchings=162465104 tr(TMD^l)=162465104 EQUAL
PASS trace identity tr(T^l) = matchings of the quotient graph 
RESULT propc dims=3,3 |G|=54 HOLDS (dimer and monomer-dimer)
PASS property C on the full (3,3) matrices 
orbit tables built, 35070 orbits in sector 12 (32s)
second layer done (370s)
RESULT certfull dims=5,5 sector=12 orbits=35070 listed_mismatches=0 u=53 ratio=68004910275217693829986/10405826313374 bound=0.4520095976 ceil6=0.45201 (476s)
PASS sector 12 exact ratio equals 68004910275217693829986/10405826313374 477s
NOTE default run: sectors 0..11 NOT checked in Python (set CW_SMALL=1, or use the C program, see REPRODUCE.md); sector 12 alone gives 0.4520095976
ALL CHECKS PASS
m=5 n=5 |G|=150 sector=12 orbits=35070/35070 threads=28
LISTED_VALUE_MISMATCHES 0 of 35070
CHECK sector=12 p=0 u=53 ratio=68004910275217693829986/10405826313374 approx=6535272474.019190788 l3bound=0.4520095976
m=5 n=5 |G|=150 sector=0 orbits=1/1 threads=28
m=5 n=5 |G|=150 sector=1 orbits=1/1 threads=28
m=5 n=5 |G|=150 sector=2 orbits=4/4 threads=28
m=5 n=5 |G|=150 sector=3 orbits=24/24 threads=28
m=5 n=5 |G|=150 sector=4 orbits=102/102 threads=28
m=5 n=5 |G|=150 sector=5 orbits=388/388 threads=28
m=5 n=5 |G|=150 sector=6 orbits=1252/1252 threads=28
m=5 n=5 |G|=150 sector=7 orbits=3320/3320 threads=28
m=5 n=5 |G|=150 sector=8 orbits=7374/7374 threads=28
m=5 n=5 |G|=150 sector=9 orbits=13868/13868 threads=28
m=5 n=5 |G|=150 sector=10 orbits=22108/22108 threads=28
m=5 n=5 |G|=150 sector=11 orbits=30064/30064 threads=28
PASS C implementation, all 13 sectors: maximum 0.4520095976 in sector 12, rounded up 0.45201 (claimed 0.452010)
ALL CHECKS PASS

real	8m22.687s
user	50m38.178s
sys	0m12.147s

```
