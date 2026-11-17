# REPRODUCE skeptic verdict (panel 2)

context: subagent (fresh, saw only claim/)

Scope: only the files under claim/ were read (CLAIM.md, status.md, REPRODUCE.md, object/counts.txt; after my own
checker and counter were written and run, also checker/checklist.c, source/conventions.py, source/fix.py). The
other source files were compiled and run as REPRODUCE.md says, not read. All work was done in a scratch copy of
claim/; my own code lives there in a subfolder own/ (mycount.c, mycheck.c, brute.c, conv.py, run scripts) and is
not part of claim/.

## Definition used (quoted from CLAIM.md)

> Charges F_X, X in {Q_i, u_i, d_i, L_i, e_i} (SM) or also nu_i (SMnuR), i = 1, 2, 3, all-left-handed basis ...; sums over i:
>   SU(3)^2 U(1)_F:  sum (2 F_Q + F_u + F_d) = 0
>   SU(2)^2 U(1)_F:  sum (3 F_Q + F_L) = 0
>   U(1)_Y^2 U(1)_F: sum (F_Q/6 + 4 F_u/3 + F_d/3 + F_L/2 + F_e) = 0
>   grav^2 U(1)_F:   sum (6 F_Q + 3 F_u + 3 F_d + 2 F_L + F_e + F_nu) = 0
>   U(1)_Y U(1)_F^2: sum (F_Q^2 - 2 F_u^2 + F_d^2 - F_L^2 + F_e^2) = 0
>   U(1)_F^3:        sum (6 F_Q^3 + 3 F_u^3 + 3 F_d^3 + 2 F_L^3 + F_e^3 + F_nu^3) = 0
> (SM: drop nu.)
>
> Convention ("inequivalent"): count = 1 + the number of nonzero integer solutions with |F| <= Q_max and gcd 1,
> modulo independent permutations of the three families within each species and the overall sign F -> -F (the "1"
> is the all-zero assignment).
>
> Canonical line: species order Q u d L e [nu]; each species sorted ascending; of F and -F the lexicographically
> larger; gcd 1; nonzero; lines strictly increasing (lexicographic, as integer tuples); integers separated by single
> spaces, "\n" line ends.

(I checked the multiplicities/hypercharges of these six equations against the stated representations; they are the
standard anomaly coefficients. The hypercharge-squared equation is used x6 in integer form.)

## (1) Own exhaustive counter (own algorithm, written before reading source/)

Re-derived steps:
- Linear ACCs in terms of species sums S_X: with S_Q, S_u free, S_d = -2S_Q - S_u, S_L = -3S_Q, S_e = 2S_Q - S_u,
  S_nu = 4S_Q + S_u (SM: S_nu = 0, so S_u = -4S_Q). Asserted numerically in the code.
- Family permutations within a species: each species is a sorted triple (multiset); count species-sorted solutions
  Nraw(Q) exactly by meet-in-the-middle over (S_Q, S_u): A = (Q,u,d), B = (L,e,nu), joined on the exact pair
  (quadratic partial sum, cubic partial sum) with a hash table (injective 64-bit key). Exhaustive, no sampling.
- Sign F -> -F on multiset classes: Burnside, classes = (N + Fix)/2, where Fix = sign-fixed solutions = every species
  of form {-a,0,a} (then linear and cubic vanish; quadratic gives aQ^2 - 2au^2 + ad^2 - aL^2 + ae^2 = 0, nu free).
  Note: such nonzero fixed points exist (e.g. Q = L = {-1,0,1}, rest 0), so the sign quotient is not N/2.
- gcd 1: ACCs are homogeneous, so solutions with gcd k and bound Q <-> primitive solutions with bound floor(Q/k);
  Moebius: P(Q) = sum_k mu(k) (Nraw(floor(Q/k)) - 1), same for Fix; count = 1 + (P + PF)/2.
- Counter validated against an independent brute force (all species-sorted tuples, all six ACCs checked literally):
  SM Q=1,2,3 and SMnuR Q=1,2 give identical (Nraw, Nfix): (8,8) (37,21) (146,46); (60,16) (727,63).

Calibration (own counter vs. published values listed in status.md):
```
calib SM 1 published 8 mine 8 OK
calib SM 3 published 82 mine 82 OK
calib SM 5 published 626 mine 626 OK
calib SM 7 published 3902 mine 3902 OK
calib SM 10 published 23800 mine 23800 OK
calib SMnuR 6 published 435305 mine 435305 OK
calib SMnuR 7 published 1358388 mine 1358388 OK
calib SMnuR 8 published 3612734 mine 3612734 OK
calib SMnuR 9 published 9587085 mine 9587085 OK
calib SMnuR 10 published 21546920 mine 21546920 OK
```

Own counter vs. object/counts.txt, every row:
```
row SMnuR 12 claimed 95067546 mine 95067546 MATCH
row SMnuR 13 claimed 180207252 mine 180207252 MATCH
row SMnuR 14 claimed 324627816 mine 324627816 MATCH
row SMnuR 15 claimed 595857832 mine 595857832 MATCH
row SMnuR 16 claimed 1002483711 mine 1002483711 MATCH
row SM 12 claimed 67968 mine 67968 MATCH
row SM 13 claimed 100388 mine 100388 MATCH
row SM 14 claimed 144102 mine 144102 MATCH
row SM 15 claimed 223605 mine 223605 MATCH
row SM 16 claimed 310691 mine 310691 MATCH
row SM 17 claimed 418636 mine 418636 MATCH
row SM 18 claimed 628488 mine 628488 MATCH
row SM 19 claimed 824232 mine 824232 MATCH
row SM 20 claimed 1071441 mine 1071441 MATCH
row SM 21 claimed 1477213 mine 1477213 MATCH
row SM 22 claimed 1871968 mine 1871968 MATCH
row SM 23 claimed 2338832 mine 2338832 MATCH
row SM 24 claimed 3188475 mine 3188475 MATCH
row SM 25 claimed 3920608 mine 3920608 MATCH
row SM 26 claimed 4789179 mine 4789179 MATCH
row SM 27 claimed 6167709 mine 6167709 MATCH
row SM 28 claimed 7467095 mine 7467095 MATCH
row SM 29 claimed 8910591 mine 8910591 MATCH
row SM 30 claimed 11359021 mine 11359021 MATCH
row SM 31 claimed 13425699 mine 13425699 MATCH
```

Raw own-counter output (Q NU Nraw Nfix), SMnuR 9..16:
```
9 1 Nraw 19226326 Nfix 6260
10 1 Nraw 43317513 Nfix 8657
11 1 Nraw 90976848 Nfix 12312
12 1 Nraw 191048355 Nfix 16549
13 1 Nraw 361321962 Nfix 22428
14 1 Nraw 652002953 Nfix 29445
15 1 Nraw 1194635588 Nfix 37632
16 1 Nraw 2012427605 Nfix 47651
```
Own-counter run times (2 threads), SMnuR: 14: 34 s, 15: 55 s, 16: 108 s.

Also: in object/counts.txt every row has lines = count - 1 and independent_count = count (awk check, 25/25 rows).

## (2) Lists regenerated and streamed through my own checker

Own checker (mycheck.c, written from the canonical-line definition above): exact format (single spaces, "\n", no
leading zeros, no "-0", exactly 15/18 integers), |F| <= Q_max, all six ACCs, nonzero, each species sorted
ascending, F >= canon(-F) lexicographically, gcd 1, strict lexicographic increase, and line count == the claimed
list_lines (and > 0); it prints MYCHECK PASS only if all hold. Mutation tests on the SM 12 stream all gave
MYCHECK FAIL: dropped line, duplicated line, swapped lines, sign-flipped line, line doubled (gcd 2), one entry
altered, empty stream.

Pipeline per row (no file stored): `LISTER ... | tee >(sha256sum) | mycheck QMAX NU LINES` (SM rows additionally
`>(checker/checklist.c QMAX NU)` on the same bytes). Listers as in REPRODUCE.md: source/acclist.c `QMAX NU`;
source/csenum.c `QMAX NU NPASS NTHR` with NPASS 2/4/10/16/26 for SMnuR 12..16, NTHR 2; for SM rows csenum
`QMAX 0 1 1`. pipestatus 0 0 0 = lister, tee and mycheck exit codes. Lister tags: c_ = csenum, a_/a2_ = acclist,
c_nu12b = second csenum run of SMnuR 12 (determinism).

### SMnuR Q_max 12: claimed count 95067546, lines 95067545, sha256 c92c6342e2f70126cb61a620f36e589f9b430e3002e1a180af77a088fcd7df84
- own counter: 95067546 -> MATCH
- c_nu12 (source/csenum.c): OK | 09:55:59 secs=65 pipestatus=0 0 0 sha=c92c6342e2f70126cb61a620f36e589f9b430e3002e1a180af77a088fcd7df84 mycheck Q=12 NU=1 lines=95067545 expected=95067545 bad=0 MYCHECK PASS  gen_tail: QMAX 12 NU 1: blocks 913, build 102953946, probes 118189179, matches 96261476, lines 95067545, count(+1) 95067546, 62.8s
- c_nu12b (source/csenum.c): OK | 09:56:59 secs=60 pipestatus=0 0 0 sha=c92c6342e2f70126cb61a620f36e589f9b430e3002e1a180af77a088fcd7df84 mycheck Q=12 NU=1 lines=95067545 expected=95067545 bad=0 MYCHECK PASS  gen_tail: QMAX 12 NU 1: blocks 913, build 102953946, probes 118189179, matches 96261476, lines 95067545, count(+1) 95067546, 58.4s
- a2_nu12 (source/acclist.c): OK | 10:16:34 secs=99 pipestatus=0 0 0 sha=c92c6342e2f70126cb61a620f36e589f9b430e3002e1a180af77a088fcd7df84 mycheck Q=12 NU=1 lines=95067545 expected=95067545 bad=0 MYCHECK PASS  gen_tail: DONE Q=12 NU=1 MODE=0 count=95067545 rawA=117883215 Bentries=102339673 Bbytes=2456152152 elapsed=97s
- row result: CONFIRMED

### SMnuR Q_max 13: claimed count 180207252, lines 180207251, sha256 73dcad862a93788c9665f4b89365ede1d121fb3d5dbf46373c3898acad3a5763
- own counter: 180207252 -> MATCH
- c_nu13 (source/csenum.c): OK | 09:59:41 secs=162 pipestatus=0 0 0 sha=73dcad862a93788c9665f4b89365ede1d121fb3d5dbf46373c3898acad3a5763 mycheck Q=13 NU=1 lines=180207251 expected=180207251 bad=0 MYCHECK PASS  gen_tail: QMAX 13 NU 1: blocks 1067, build 372018300, probes 214573892, matches 181848896, lines 180207251, count(+1) 180207252, 159.6s
- a2_nu13 (source/acclist.c): OK | 10:19:39 secs=185 pipestatus=0 0 0 sha=73dcad862a93788c9665f4b89365ede1d121fb3d5dbf46373c3898acad3a5763 mycheck Q=13 NU=1 lines=180207251 expected=180207251 bad=0 MYCHECK PASS  gen_tail: DONE Q=13 NU=1 MODE=0 count=180207251 rawA=214104668 Bentries=185067810 Bbytes=4441627440 elapsed=183s
- row result: CONFIRMED

### SMnuR Q_max 14: claimed count 324627816, lines 324627815, sha256 1978ce33f39aa91acb895cfde36fe57f83b703ec7d140ec12c45bf0a9fd3e8cf
- own counter: 324627816 -> MATCH
- c_nu14 (source/csenum.c): OK | 10:05:57 secs=376 pipestatus=0 0 0 sha=1978ce33f39aa91acb895cfde36fe57f83b703ec7d140ec12c45bf0a9fd3e8cf mycheck Q=14 NU=1 lines=324627815 expected=324627815 bad=0 MYCHECK PASS  gen_tail: QMAX 14 NU 1: blocks 1233, build 1614171600, probes 373782748, matches 327831241, lines 324627815, count(+1) 324627816, 374.2s
- row result: CONFIRMED

### SMnuR Q_max 15: claimed count 595857832, lines 595857831, sha256 0e35db7f73a1485f0af2759684efff52f1771894be7e160466f45b73953d26b3
- own counter: 595857832 -> MATCH
- c_nu15 (source/csenum.c): OK | 10:14:49 secs=532 pipestatus=0 0 0 sha=0e35db7f73a1485f0af2759684efff52f1771894be7e160466f45b73953d26b3 mycheck Q=15 NU=1 lines=595857831 expected=595857831 bad=0 MYCHECK PASS  gen_tail: QMAX 15 NU 1: blocks 1411, build 3656494629, probes 628048778, matches 600364951, lines 595857831, count(+1) 595857832, 529.7s
- row result: CONFIRMED

### SMnuR Q_max 16: claimed count 1002483711, lines 1002483710, sha256 15bc1ed7dada71acf9bba04cc85734710259f75d9e4f1b9a94c6745f74d632d2
- own counter: 1002483711 -> MATCH
- c_nu16 (source/csenum.c): OK | 10:27:48 secs=779 pipestatus=0 0 0 sha=15bc1ed7dada71acf9bba04cc85734710259f75d9e4f1b9a94c6745f74d632d2 mycheck Q=16 NU=1 lines=1002483710 expected=1002483710 bad=0 MYCHECK PASS  gen_tail: QMAX 16 NU 1: blocks 1601, build 6835644642, probes 1022469050, matches 1010749737, lines 1002483710, count(+1) 1002483711, 777.3s
- row result: CONFIRMED

### SM Q_max 12: claimed count 67968, lines 67967, sha256 23d1469a30ccf713b5129f14e47eb62e19512ee89bd06c2f7422bb35ae5c612f
- own counter: 67968 -> MATCH
- a_sm12 (source/acclist.c): OK | secs=2 pipestatus=0 0 0 sha=23d1469a30ccf713b5129f14e47eb62e19512ee89bd06c2f7422bb35ae5c612f mycheck Q=12 NU=0 lines=67967 expected=67967 bad=0 MYCHECK PASS  checklist: valid solutions: 67967 PASS
- c_sm12 (source/csenum.c): OK | secs=1 pipestatus=0 0 0 sha=23d1469a30ccf713b5129f14e47eb62e19512ee89bd06c2f7422bb35ae5c612f mycheck Q=12 NU=0 lines=67967 expected=67967 bad=0 MYCHECK PASS  checklist: valid solutions: 67967 PASS
- row result: CONFIRMED

### SM Q_max 13: claimed count 100388, lines 100387, sha256 262ca74409938625365a4c2da50b95a941bce1c1e3aaf43fae2006afbe92ab9e
- own counter: 100388 -> MATCH
- a_sm13 (source/acclist.c): OK | secs=2 pipestatus=0 0 0 sha=262ca74409938625365a4c2da50b95a941bce1c1e3aaf43fae2006afbe92ab9e mycheck Q=13 NU=0 lines=100387 expected=100387 bad=0 MYCHECK PASS  checklist: valid solutions: 100387 PASS
- c_sm13 (source/csenum.c): OK | secs=1 pipestatus=0 0 0 sha=262ca74409938625365a4c2da50b95a941bce1c1e3aaf43fae2006afbe92ab9e mycheck Q=13 NU=0 lines=100387 expected=100387 bad=0 MYCHECK PASS  checklist: valid solutions: 100387 PASS
- row result: CONFIRMED

### SM Q_max 14: claimed count 144102, lines 144101, sha256 8ce628b32bd21123799290615d6942c68395587b59ac2a3d6648a335bc230f3f
- own counter: 144102 -> MATCH
- a_sm14 (source/acclist.c): OK | secs=3 pipestatus=0 0 0 sha=8ce628b32bd21123799290615d6942c68395587b59ac2a3d6648a335bc230f3f mycheck Q=14 NU=0 lines=144101 expected=144101 bad=0 MYCHECK PASS  checklist: valid solutions: 144101 PASS
- c_sm14 (source/csenum.c): OK | secs=1 pipestatus=0 0 0 sha=8ce628b32bd21123799290615d6942c68395587b59ac2a3d6648a335bc230f3f mycheck Q=14 NU=0 lines=144101 expected=144101 bad=0 MYCHECK PASS  checklist: valid solutions: 144101 PASS
- row result: CONFIRMED

### SM Q_max 15: claimed count 223605, lines 223604, sha256 c51e3b8715f092275326c8ddfaabc806d63616bf71797c92c2a940e7764d4114
- own counter: 223605 -> MATCH
- a_sm15 (source/acclist.c): OK | secs=3 pipestatus=0 0 0 sha=c51e3b8715f092275326c8ddfaabc806d63616bf71797c92c2a940e7764d4114 mycheck Q=15 NU=0 lines=223604 expected=223604 bad=0 MYCHECK PASS  checklist: valid solutions: 223604 PASS
- c_sm15 (source/csenum.c): OK | secs=2 pipestatus=0 0 0 sha=c51e3b8715f092275326c8ddfaabc806d63616bf71797c92c2a940e7764d4114 mycheck Q=15 NU=0 lines=223604 expected=223604 bad=0 MYCHECK PASS  checklist: valid solutions: 223604 PASS
- row result: CONFIRMED

### SM Q_max 16: claimed count 310691, lines 310690, sha256 a9c31c0b3c035429776c5e5556fca88c4bbd8e55800734ab16b6c3ab4ad9f61b
- own counter: 310691 -> MATCH
- a_sm16 (source/acclist.c): OK | secs=3 pipestatus=0 0 0 sha=a9c31c0b3c035429776c5e5556fca88c4bbd8e55800734ab16b6c3ab4ad9f61b mycheck Q=16 NU=0 lines=310690 expected=310690 bad=0 MYCHECK PASS  checklist: valid solutions: 310690 PASS
- c_sm16 (source/csenum.c): OK | secs=2 pipestatus=0 0 0 sha=a9c31c0b3c035429776c5e5556fca88c4bbd8e55800734ab16b6c3ab4ad9f61b mycheck Q=16 NU=0 lines=310690 expected=310690 bad=0 MYCHECK PASS  checklist: valid solutions: 310690 PASS
- row result: CONFIRMED

### SM Q_max 17: claimed count 418636, lines 418635, sha256 cba838bfc0797d0c33915e45d9ec51f24c1a24b6e9c25d80cd627a7bc46928f8
- own counter: 418636 -> MATCH
- a_sm17 (source/acclist.c): OK | secs=7 pipestatus=0 0 0 sha=cba838bfc0797d0c33915e45d9ec51f24c1a24b6e9c25d80cd627a7bc46928f8 mycheck Q=17 NU=0 lines=418635 expected=418635 bad=0 MYCHECK PASS  checklist: valid solutions: 418635 PASS
- c_sm17 (source/csenum.c): OK | secs=2 pipestatus=0 0 0 sha=cba838bfc0797d0c33915e45d9ec51f24c1a24b6e9c25d80cd627a7bc46928f8 mycheck Q=17 NU=0 lines=418635 expected=418635 bad=0 MYCHECK PASS  checklist: valid solutions: 418635 PASS
- row result: CONFIRMED

### SM Q_max 18: claimed count 628488, lines 628487, sha256 7018dde47623603fdb8b9600bdbf0d854cf6002325314864825bc027cc3b62cb
- own counter: 628488 -> MATCH
- a_sm18 (source/acclist.c): OK | secs=7 pipestatus=0 0 0 sha=7018dde47623603fdb8b9600bdbf0d854cf6002325314864825bc027cc3b62cb mycheck Q=18 NU=0 lines=628487 expected=628487 bad=0 MYCHECK PASS  checklist: valid solutions: 628487 PASS
- c_sm18 (source/csenum.c): OK | secs=3 pipestatus=0 0 0 sha=7018dde47623603fdb8b9600bdbf0d854cf6002325314864825bc027cc3b62cb mycheck Q=18 NU=0 lines=628487 expected=628487 bad=0 MYCHECK PASS  checklist: valid solutions: 628487 PASS
- row result: CONFIRMED

### SM Q_max 19: claimed count 824232, lines 824231, sha256 e4b32bc0dd2c2d6c7bdc0948371c35e2721f273b6d31154243825c64a1e35734
- own counter: 824232 -> MATCH
- a_sm19 (source/acclist.c): OK | secs=10 pipestatus=0 0 0 sha=e4b32bc0dd2c2d6c7bdc0948371c35e2721f273b6d31154243825c64a1e35734 mycheck Q=19 NU=0 lines=824231 expected=824231 bad=0 MYCHECK PASS  checklist: valid solutions: 824231 PASS
- c_sm19 (source/csenum.c): OK | secs=3 pipestatus=0 0 0 sha=e4b32bc0dd2c2d6c7bdc0948371c35e2721f273b6d31154243825c64a1e35734 mycheck Q=19 NU=0 lines=824231 expected=824231 bad=0 MYCHECK PASS  checklist: valid solutions: 824231 PASS
- row result: CONFIRMED

### SM Q_max 20: claimed count 1071441, lines 1071440, sha256 f8e2ce35236a5792c3795608aaafcd3f2d4a68f7dfd3bdb0c65bc6efad23e770
- own counter: 1071441 -> MATCH
- a_sm20 (source/acclist.c): OK | secs=17 pipestatus=0 0 0 sha=f8e2ce35236a5792c3795608aaafcd3f2d4a68f7dfd3bdb0c65bc6efad23e770 mycheck Q=20 NU=0 lines=1071440 expected=1071440 bad=0 MYCHECK PASS  checklist: valid solutions: 1071440 PASS
- c_sm20 (source/csenum.c): OK | secs=4 pipestatus=0 0 0 sha=f8e2ce35236a5792c3795608aaafcd3f2d4a68f7dfd3bdb0c65bc6efad23e770 mycheck Q=20 NU=0 lines=1071440 expected=1071440 bad=0 MYCHECK PASS  checklist: valid solutions: 1071440 PASS
- row result: CONFIRMED

### SM Q_max 21: claimed count 1477213, lines 1477212, sha256 77b6c66a63581e9a1c3b9a88aa88422e6dc8003e0dc7d210c81c49de5d2c35b4
- own counter: 1477213 -> MATCH
- a_sm21 (source/acclist.c): OK | secs=26 pipestatus=0 0 0 sha=77b6c66a63581e9a1c3b9a88aa88422e6dc8003e0dc7d210c81c49de5d2c35b4 mycheck Q=21 NU=0 lines=1477212 expected=1477212 bad=0 MYCHECK PASS  checklist: valid solutions: 1477212 PASS
- row result: CONFIRMED

### SM Q_max 22: claimed count 1871968, lines 1871967, sha256 41e378880fca97cc2b107415db388ffbe14fe1998859e42fea22964b79a52a52
- own counter: 1871968 -> MATCH
- a_sm22 (source/acclist.c): OK | secs=26 pipestatus=0 0 0 sha=41e378880fca97cc2b107415db388ffbe14fe1998859e42fea22964b79a52a52 mycheck Q=22 NU=0 lines=1871967 expected=1871967 bad=0 MYCHECK PASS  checklist: valid solutions: 1871967 PASS
- row result: CONFIRMED

### SM Q_max 23: claimed count 2338832, lines 2338831, sha256 169575ee30b864988623a740d298886722ebe3b7e9145ee996212957b8a627f6
- own counter: 2338832 -> MATCH
- a_sm23 (source/acclist.c): OK | secs=38 pipestatus=0 0 0 sha=169575ee30b864988623a740d298886722ebe3b7e9145ee996212957b8a627f6 mycheck Q=23 NU=0 lines=2338831 expected=2338831 bad=0 MYCHECK PASS  checklist: valid solutions: 2338831 PASS
- row result: CONFIRMED

### SM Q_max 24: claimed count 3188475, lines 3188474, sha256 deef8f54329bf7ac2c32ae849123b6ea6bd69f3f792db0488f177e9ea14ca4e4
- own counter: 3188475 -> MATCH
- a_sm24 (source/acclist.c): OK | secs=59 pipestatus=0 0 0 sha=deef8f54329bf7ac2c32ae849123b6ea6bd69f3f792db0488f177e9ea14ca4e4 mycheck Q=24 NU=0 lines=3188474 expected=3188474 bad=0 MYCHECK PASS  checklist: valid solutions: 3188474 PASS
- row result: CONFIRMED

### SM Q_max 25: claimed count 3920608, lines 3920607, sha256 2dfdc23a383d705cb5bb84be45cfa070eded7749540b147f97b403d4b05a3ec4
- own counter: 3920608 -> MATCH
- a_sm25 (source/acclist.c): OK | secs=66 pipestatus=0 0 0 sha=2dfdc23a383d705cb5bb84be45cfa070eded7749540b147f97b403d4b05a3ec4 mycheck Q=25 NU=0 lines=3920607 expected=3920607 bad=0 MYCHECK PASS  checklist: valid solutions: 3920607 PASS
- row result: CONFIRMED

### SM Q_max 26: claimed count 4789179, lines 4789178, sha256 58cf1b34b76c227cd526075b434da8e796c65f7515e1789d0dea838295ec883a
- own counter: 4789179 -> MATCH
- a_sm26 (source/acclist.c): OK | secs=78 pipestatus=0 0 0 sha=58cf1b34b76c227cd526075b434da8e796c65f7515e1789d0dea838295ec883a mycheck Q=26 NU=0 lines=4789178 expected=4789178 bad=0 MYCHECK PASS  checklist: valid solutions: 4789178 PASS
- row result: CONFIRMED

### SM Q_max 27: claimed count 6167709, lines 6167708, sha256 b6bcea045c7da4273857f0bf00a050b2646d1d18216728e9efcaff4bf0cbaed5
- own counter: 6167709 -> MATCH
- a_sm27 (source/acclist.c): OK | secs=102 pipestatus=0 0 0 sha=b6bcea045c7da4273857f0bf00a050b2646d1d18216728e9efcaff4bf0cbaed5 mycheck Q=27 NU=0 lines=6167708 expected=6167708 bad=0 MYCHECK PASS  checklist: valid solutions: 6167708 PASS
- row result: CONFIRMED

### SM Q_max 28: claimed count 7467095, lines 7467094, sha256 16d4ba74be1cbbd1828bbe1cb1801f865164bf1e93afe363763c76b5f38722b6
- own counter: 7467095 -> MATCH
- a_sm28 (source/acclist.c): OK | secs=97 pipestatus=0 0 0 sha=16d4ba74be1cbbd1828bbe1cb1801f865164bf1e93afe363763c76b5f38722b6 mycheck Q=28 NU=0 lines=7467094 expected=7467094 bad=0 MYCHECK PASS  checklist: valid solutions: 7467094 PASS
- row result: CONFIRMED

### SM Q_max 29: claimed count 8910591, lines 8910590, sha256 ea3ba6dc4ddc40a7a4e7c010304f0c4eacba15286509b224b516b29236161c9f
- own counter: 8910591 -> MATCH
- a_sm29 (source/acclist.c): OK | secs=111 pipestatus=0 0 0 sha=ea3ba6dc4ddc40a7a4e7c010304f0c4eacba15286509b224b516b29236161c9f mycheck Q=29 NU=0 lines=8910590 expected=8910590 bad=0 MYCHECK PASS  checklist: valid solutions: 8910590 PASS
- row result: CONFIRMED

### SM Q_max 30: claimed count 11359021, lines 11359020, sha256 f8c6543ee3e30630bfda3dc016f96e22d83e5978f41285ad7e82e29b7a8b5dd0
- own counter: 11359021 -> MATCH
- a_sm30 (source/acclist.c): OK | secs=141 pipestatus=0 0 0 sha=f8c6543ee3e30630bfda3dc016f96e22d83e5978f41285ad7e82e29b7a8b5dd0 mycheck Q=30 NU=0 lines=11359020 expected=11359020 bad=0 MYCHECK PASS  checklist: valid solutions: 11359020 PASS
- row result: CONFIRMED

### SM Q_max 31: claimed count 13425699, lines 13425698, sha256 ace3ca282d91c147d56d61370c945daee94d7c5982222052606578aa69bf134e
- own counter: 13425699 -> MATCH
- a_sm31 (source/acclist.c): OK | secs=182 pipestatus=0 0 0 sha=ace3ca282d91c147d56d61370c945daee94d7c5982222052606578aa69bf134e mycheck Q=31 NU=0 lines=13425698 expected=13425698 bad=0 MYCHECK PASS  checklist: valid solutions: 13425698 PASS
- row result: CONFIRMED

## Coverage of the requested checks

- Own counts: all 25 rows (SMnuR 12..16, SM 12..31) recomputed exhaustively: 25/25 MATCH; calibration 10/10 OK.
- Lists: all 25 rows regenerated in full and streamed; sha256 and line count equal to counts.txt and own checker
  PASS on every row (SM rows also checker/checklist.c PASS).
- Both listers: SMnuR 12 and 13 (acclist and csenum, identical sha256), SM 12..20 (both), as counts.txt marks.
  SMnuR 14..16 and SM 21..31 regenerated with the single lister counts.txt marks as 'same'.
- Determinism: SMnuR 12 regenerated twice with csenum (identical sha256 and line count), and a third time with
  acclist (identical).
- Since every listed line is a valid, canonical, primitive, nonzero solution, lines are strictly increasing (so
  distinct classes), and the line count equals my independently computed number of nonzero primitive classes, each
  list is complete.
- No mismatch, missing object or non-determinism found.

## Caveats (do not affect this verdict)

- The calibration values come from status.md, which says they were obtained from a web-search tool, not a byte-exact
  page (paper/Zenodo fetch refused); the convention therefore rests on agreement with those 10 reported values.
- checker/checklist.c does not compare the line count with an expected value and would print PASS on an empty
  stream; my checker enforces the count.

pass: true
