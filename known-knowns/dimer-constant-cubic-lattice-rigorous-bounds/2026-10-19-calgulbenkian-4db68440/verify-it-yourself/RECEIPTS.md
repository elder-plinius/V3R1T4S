# Receipts (real output)

Full run_checks.sh.

```
== sanity: (3,3) ==
RESULT trace dims=2,2 l=4 vertices=16 perfect_matchings=4752 tr(T^l)=4752 all_matchings=306305 tr(TMD^l)=306305 EQUAL
RESULT trace dims=3,2 l=4 vertices=24 perfect_matchings=194244 tr(T^l)=194244 all_matchings=162589284 tr(TMD^l)=162589284 EQUAL
RESULT trace dims=2,2 l=6 vertices=24 perfect_matchings=190992 tr(T^l)=190992 all_matchings=162465104 tr(TMD^l)=162465104 EQUAL
PASS trace identity: tr(TMD^l) = number of ALL matchings of the quotient graph, (2,2,4) (3,2,4) (2,2,6) 
PASS certificate lines are exactly the orbits of the 18-element group (canonical = minimum mask), cover all 512 states, all values positive; 44 orbits 
peak state bits 13
PASS 40 sampled rows (including the all-ones state) agree with a separate pure-Python expansion of the permanent definition 
RESULT mdcert dims=3,3 states=512 orbits=44 argmax_state=255 ratio=731051554747087/618837374495
ratio decimal (15 places) = 1181.330644975441207
log(ratio)/9 = 0.786044083039586946   (12 places, rounded up: 0.78604408304; 7 places, rounded up: 0.7860441)
PASS exact ratio 731051554747087/618837374495 
PASS claimed 7-place bound 0.7860441 
PASS h3 <= 0.7860441 is below FKLM 0.7862023450 by 0.0001582450 (needed: at least 1e-6) 
elapsed seconds: total 0.8, of which C matrix-vector step 0.2
ALL CHECKS PASS
== claim: (5,4) ==
PASS part cert_md_h3_54.txt.part00 900000 bytes
PASS part cert_md_h3_54.txt.part01 414630 bytes
PASS whole certificate 1314630 bytes sha256 4db684405f609065a95ffe192fcdf672742b3910e7dfff37ed80b02ec0f74c0c
RESULT trace dims=2,2 l=4 vertices=16 perfect_matchings=4752 tr(T^l)=4752 all_matchings=306305 tr(TMD^l)=306305 EQUAL
RESULT trace dims=3,2 l=4 vertices=24 perfect_matchings=194244 tr(T^l)=194244 all_matchings=162589284 tr(TMD^l)=162589284 EQUAL
RESULT trace dims=2,2 l=6 vertices=24 perfect_matchings=190992 tr(T^l)=190992 all_matchings=162465104 tr(TMD^l)=162465104 EQUAL
PASS trace identity: tr(TMD^l) = number of ALL matchings of the quotient graph, (2,2,4) (3,2,4) (2,2,6) 
PASS certificate lines are exactly the orbits of the 20-element group (canonical = minimum mask), cover all 1048576 states, all values positive; 52488 orbits 
peak state bits 25
PASS 40 sampled rows (including the all-ones state) agree with a separate pure-Python expansion of the permanent definition 
RESULT mdcert dims=5,4 states=1048576 orbits=52488 argmax_state=524031 ratio=1891821269973664/281869529
ratio decimal (15 places) = 6711691.315784843135705
log(ratio)/20 = 0.785968076808533207   (12 places, rounded up: 0.785968076809; 7 places, rounded up: 0.7859681)
PASS exact ratio 1891821269973664/281869529 
PASS claimed 7-place bound 0.7859681 
PASS h3 <= 0.7859681 is below FKLM 0.7862023450 by 0.0002342450 (needed: at least 1e-6) 
elapsed seconds: total 17.3, of which C matrix-vector step 14.4
ALL CHECKS PASS
sh verify-it-yourself/run_checks.sh  15.63s user 1.14s system 90% cpu 18.476 total
```
