# Receipts: real output of `sh verify-it-yourself/run_checks.sh` on the packaging machine (2026-10-15 20:22 UTC, under heavy machine load)

```
values.json: 15 reduced fractions, decimals consistent
n=2 m=2 states=21 actions=27 value=17/6 = 2.833333333333
PASS
n=3 m=2 states=118 actions=194 value=271/90 = 3.011111111111
PASS
n=4 m=2 states=496 actions=968 value=1279/420 = 3.045238095238
PASS
n=5 m=2 states=1727 actions=3890 value=57583/18900 = 3.046719576720
PASS
n=6 m=2 states=5311 actions=13510 value=1136743/374220 = 3.037632943188
PASS
n=7 m=2 states=14903 actions=42108 value=206528731/68108040 = 3.032369320861
PASS
n=8 m=2 states=38967 actions=120575 value=61829276953/20432412000 = 3.026039067390
PASS
n=9 m=2 states=96163 actions=322242 value=6298009733989/2084106024000 = 3.021923866379
PASS
n=11 m=2 states=509906 actions=1952906 value=137912544707079557/45735706696680000 = 3.015423936088
PASS
PASS
```

Also run on the packaging machine, `FULL=1 sh verify-it-yourself/run_checks.sh` (the shipped n = 10, 12, 13 parts reassembled and verified as well), real output:

```
values.json: 15 reduced fractions, decimals consistent
n=2 m=2 states=21 actions=27 value=17/6 = 2.833333333333
PASS
n=3 m=2 states=118 actions=194 value=271/90 = 3.011111111111
PASS
n=4 m=2 states=496 actions=968 value=1279/420 = 3.045238095238
PASS
n=5 m=2 states=1727 actions=3890 value=57583/18900 = 3.046719576720
PASS
n=6 m=2 states=5311 actions=13510 value=1136743/374220 = 3.037632943188
PASS
n=7 m=2 states=14903 actions=42108 value=206528731/68108040 = 3.032369320861
PASS
n=8 m=2 states=38967 actions=120575 value=61829276953/20432412000 = 3.026039067390
PASS
n=9 m=2 states=96163 actions=322242 value=6298009733989/2084106024000 = 3.021923866379
PASS
n=10 m=2 states=226091 actions=812989 value=170757866939041/56568592080000 = 3.018598495390
PASS
n=11 m=2 states=509906 actions=1952906 value=137912544707079557/45735706696680000 = 3.015423936088
PASS
n=12 m=2 states=1109092 actions=4496408 value=228254911260131056513/75738330289702080000 = 3.013730437244
PASS
n=13 m=2 states=2336473 actions=9975628 value=3901622163101296907981/1295524070744904000000 = 3.011616882470
PASS
PASS
```

The C++ checker (verify-it-yourself/cg_verify.cpp) was also run on every certificate n = 2..17 during the run; all PASS.
