# Receipts (real output, 2026-11-03T13:42:02Z)

## sh verify-it-yourself/run_checks.sh
```
== 1. object/VALUE.txt: hash vs INDEX.csv and every pinned file
object/VALUE.txt sha256 matches INDEX.csv
value line: ['value: 624'] INDEX value: 624 ok
78 pinned files checked; recorded but not shipped: tools/geng
ok
== 2. saved outputs: graph counts (A001349), published a(1..8), A and B agree class by class on a(10) = 624
n=1 A graphs=1 max=1  B graphs=1 max=1  A001349=1 OEIS=1 ok
n=2 A graphs=1 max=2  B graphs=1 max=2  A001349=1 OEIS=2 ok
n=3 A graphs=2 max=2  B graphs=2 max=2  A001349=2 OEIS=2 ok
n=4 A graphs=6 max=6  B graphs=6 max=6  A001349=6 OEIS=6 ok
n=5 A graphs=21 max=7  B graphs=21 max=7  A001349=21 OEIS=7 ok
n=6 A graphs=112 max=18  B graphs=112 max=18  A001349=112 OEIS=18 ok
n=7 A graphs=853 max=38  B graphs=853 max=38  A001349=853 OEIS=38 ok
n=8 A graphs=11117 max=96  B graphs=11117 max=96  A001349=11117 OEIS=96 ok
n=9 A graphs=261080 max=180  B graphs=261080 max=180 (earlier separate cell, not claimed here) ok
class  0/32: graphs 384170 max 364 high 3289 fnv 05c060c4c76bbe79 | A = B ok
class  1/32: graphs 307745 max 369 high 2268 fnv cee511ade241edac | A = B ok
class  2/32: graphs 367657 max 391 high 2827 fnv 5e83162661647a92 | A = B ok
class  3/32: graphs 380998 max 376 high 3094 fnv 97b053072fa4903b | A = B ok
class  4/32: graphs 126778 max 326 high 1037 fnv f094283f4ea76b2a | A = B ok
class  5/32: graphs 231383 max 330 high 1943 fnv a8af17a102ed31eb | A = B ok
class  6/32: graphs 426875 max 366 high 4489 fnv b7d4afebfe51cfdd | A = B ok
class  7/32: graphs 358450 max 624 high 2750 fnv efd1f66841587a6f | A = B ok
class  8/32: graphs 384111 max 353 high 3469 fnv 39d2415ea36694e0 | A = B ok
class  9/32: graphs 449036 max 347 high 3962 fnv a7d58c8868f46a12 | A = B ok
class 10/32: graphs 555336 max 413 high 6593 fnv e03c0ebbcc8db27a | A = B ok
class 11/32: graphs 571153 max 388 high 5498 fnv a43557a25d010f54 | A = B ok
class 12/32: graphs 566448 max 360 high 4495 fnv 6cf0ad6604f32fed | A = B ok
class 13/32: graphs 592499 max 352 high 5945 fnv 63a3517599976d7f | A = B ok
class 14/32: graphs 377593 max 346 high 3095 fnv 6ccd71d131575a21 | A = B ok
class 15/32: graphs 351589 max 364 high 2823 fnv f7a8c4c196a151f7 | A = B ok
class 16/32: graphs 217902 max 324 high 1758 fnv db0d94d212fa2074 | A = B ok
class 17/32: graphs 200525 max 363 high 1814 fnv bbca823d75576b0f | A = B ok
class 18/32: graphs 194840 max 410 high 1716 fnv 168f4222a0c1f4b7 | A = B ok
class 19/32: graphs 226711 max 356 high 1973 fnv d74fd434a4d16df9 | A = B ok
class 20/32: graphs 193188 max 367 high 1443 fnv 7c012a8cc6a87ccb | A = B ok
class 21/32: graphs 355500 max 353 high 3285 fnv 2d6b0f6898209898 | A = B ok
class 22/32: graphs 452760 max 368 high 4463 fnv 7d1a741eceb43f65 | A = B ok
class 23/32: graphs 239295 max 370 high 2113 fnv e63b82633856c9d5 | A = B ok
class 24/32: graphs 290566 max 350 high 2454 fnv c55c00556f704977 | A = B ok
class 25/32: graphs 374506 max 357 high 3624 fnv b52548a1cf62f250 | A = B ok
class 26/32: graphs 255178 max 325 high 1779 fnv 4035a57aa98e9ed4 | A = B ok
class 27/32: graphs 507572 max 367 high 5187 fnv 5625689f644239ba | A = B ok
class 28/32: graphs 768561 max 429 high 8098 fnv 30bf4a84eaa120d9 | A = B ok
class 29/32: graphs 196949 max 333 high 1624 fnv 675f154a820aff44 | A = B ok
class 30/32: graphs 386985 max 349 high 3492 fnv 1823c4c4144c4a55 | A = B ok
class 31/32: graphs 423712 max 470 high 4181 fnv c235976774ac4028 | A = B ok
n=10 total graphs A=11716571 B=11716571 (A001349(10)=11716571); max A=624 B=624; graphs reaching 624: 1; graphs with max >= 150: 106581 ok
top per-graph maxima (value:count): 429:1 464:1 470:1 624:1
witness from saved outputs: class 7 A I?AAD@oIg rule_mask=5 state=2; B I?AAD@oIg rule_mask=5 state=2
saved compare_AB.txt: VERDICT AGREE M = 624 ok
ok
== 3. witness simulation from the definition (pure Python, neighbours only, node itself not counted)
witness I?AAD@oIg n=10 edges=11 connected=True rule={0,2} start=2 preperiod=0 cycle_length=624 expected=624
ok
graph I?AAD@oIg: max over 1024 rules (all subsets of {0..n-1}) and 1024 starts = 624 (first at rule {0,2}) expected=624
ok
graph ICQfRh|z_: max over 1024 rules (all subsets of {0..n-1}) and 1024 starts = 470 (first at rule {0,2,4}) expected=470
ok
witness FJe~O n=7 edges=13 connected=True rule={0,2} start=1 preperiod=0 cycle_length=38 expected=38
ok
== 4. definition-level exhaustive check, n = 1..6, from all labelled graphs (no nauty)
n=1 labelled_graphs=1 iso_classes=1 connected=1 (A001349=1) max_period=1 oeis=1 ok
n=2 labelled_graphs=2 iso_classes=2 connected=1 (A001349=1) max_period=2 oeis=2 ok
n=3 labelled_graphs=8 iso_classes=4 connected=2 (A001349=2) max_period=2 oeis=2 ok
n=4 labelled_graphs=64 iso_classes=11 connected=6 (A001349=6) max_period=6 oeis=6 ok
n=5 labelled_graphs=1024 iso_classes=34 connected=21 (A001349=21) max_period=7 oeis=7 ok
n=6 labelled_graphs=32768 iso_classes=156 connected=112 (A001349=112) max_period=18 oeis=18 ok
ok
== 5. saved optimal graphs n = 1..9, the OEIS n = 7 example, the n = 10 witness and runner-up: pure Python, C and Go
@ python=1 totF=1 totBgo=1 expected=1 ok
A_ python=2 totF=2 totBgo=2 expected=2 ok
BW python=2 totF=2 totBgo=2 expected=2 ok
CU python=6 totF=6 totBgo=6 expected=6 ok
D]w python=7 totF=7 totBgo=7 expected=7 ok
ECrw python=18 totF=18 totBgo=18 expected=18 ok
FQzuo python=38 totF=38 totBgo=38 expected=38 ok
FJe~O python=38 totF=38 totBgo=38 expected=38 ok
GCz^nw python=96 totF=96 totBgo=96 expected=96 ok
H?`DBbS python=180 totF=180 totBgo=180 expected=180 ok
I?AAD@oIg python=624 totF=624 totBgo=624 expected=624 ok
ICQfRh|z_ python=470 totF=470 totBgo=470 expected=470 ok
summary: A357953(10) = 624 (witness I?AAD@oIg, rule {0,2}, start 2, neighbours-only totalistic)
PASS
```

## FULL=1 path (exercised 2026-11-03T13:34Z-13:41Z)
With nauty 2.8.8's geng, `FULL=1` recomputed a(1..9) with fresh builds of both programs: "n = 1..9: fresh A and B
outputs identical to saved". The class 7/32 part of that exercise was run against a stand-in generator that emits
only the witness graph (to test the script path, not the result), so its "differs from saved" line is expected and
is not a result. The full n = 10 recompute was done independently by the reproduce skeptic (all 32 classes, own
checker, plus a fresh Program B rerun of class 7 byte-identical to the saved output; panel/reproduce.md).
