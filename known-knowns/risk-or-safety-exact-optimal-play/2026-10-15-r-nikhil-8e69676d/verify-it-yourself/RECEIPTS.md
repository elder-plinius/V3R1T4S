# RECEIPTS: real output of `sh verify-it-yourself/run_checks.sh` from a clean copy of this package

Run started: Thu Oct 15 09:17:45 UTC 2026

```
ALL_PASS
compare_values: ALL_EQUAL
ALL_PASS
my_verify summary: 30 passed, 0 failed, of 30 certificates
15 certificates n=16..30 verified; 15 calibration certificates n=1..15 equal the published terms; second verifier agrees
PASS
exit code: 0
```

Per-certificate lines of the claim check (verify-it-yourself/_work/check_claim.txt):

```
n16.json: n=16 positions_checked=2176 P000=1599710761252635467097849938052769718961535662524/309000789280333251817791401
n17.json: n=17 positions_checked=2601 P000=1271934201995087824531562911568806911954931581879270794/245906690590528991447
n18.json: n=18 positions_checked=3078 P000=28247088896509526684833556406803399555218653423253279570310576/54670177377720
n19.json: n=19 positions_checked=3610 P000=669663748187798960299370649019840271261510564439147472414465579166/1297062327
n20.json: n=20 positions_checked=4200 P000=66496512444936569744985774803016169284564753386698071451174729031677100468/12
n21.json: n=21 positions_checked=4851 P000=11150601768836677744829480404878084867989163374264820071729947255819083074293
n22.json: n=22 positions_checked=5566 P000=98464438447917488363682498105279276252661329626200725077373960946137587277745
n23.json: n=23 positions_checked=6348 P000=16804971339804096758701401983396389612430253637235128756923316729869921672392
n24.json: n=24 positions_checked=7200 P000=61641522672390175245757644635648262298380422505942592588283292482777067721800
n25.json: n=25 positions_checked=8125 P000=13779974025358789491275007933419335247190288864906627265049450465509300008691
n26.json: n=26 positions_checked=9126 P000=18091489088333485944291793854081074404882875893911097845282752929815563286940
n27.json: n=27 positions_checked=10206 P000=2697882861914361798650696218179127537614187784879347640450491182142288979215
n28.json: n=28 positions_checked=11368 P000=3121605769229646583449076664182122463683169731883919682633436508056286165869
n29.json: n=29 positions_checked=12615 P000=3370525791808447178501937541371450362121602961346576385203636717446848055483
n30.json: n=30 positions_checked=13950 P000=9702985056846137933218838885572616340384403016127146978457034221965057701745
ALL_PASS
```

Calibration lines (n = 1..15, oeis_match):

```
n1.json: n=1 positions_checked=1 P000=... oeis_match=yes PASS
n2.json: n=2 positions_checked=6 P000=... oeis_match=yes PASS
n3.json: n=3 positions_checked=18 P000=... oeis_match=yes PASS
n4.json: n=4 positions_checked=40 P000=... oeis_match=yes PASS
n5.json: n=5 positions_checked=75 P000=... oeis_match=yes PASS
n6.json: n=6 positions_checked=126 P000=... oeis_match=yes PASS
n7.json: n=7 positions_checked=196 P000=... oeis_match=yes PASS
n8.json: n=8 positions_checked=288 P000=... oeis_match=yes PASS
n9.json: n=9 positions_checked=405 P000=... oeis_match=yes PASS
n10.json: n=10 positions_checked=550 P000=... oeis_match=yes PASS
n11.json: n=11 positions_checked=726 P000=... oeis_match=yes PASS
n12.json: n=12 positions_checked=936 P000=... oeis_match=yes PASS
n13.json: n=13 positions_checked=1183 P000=... oeis_match=yes PASS
n14.json: n=14 positions_checked=1470 P000=... oeis_match=yes PASS
n15.json: n=15 positions_checked=1800 P000=... oeis_match=yes PASS
ALL_PASS
```

Run finished: Thu Oct 15 09:17:55 UTC 2026
