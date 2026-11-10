# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from the package folder when the package was built:

```
== sha256 of the object
51269122c46632ad2ad2343dd0b36aadf8fab59aba39bb911537695723cd818b
== checker on the object (must be VALID)
size                         ok  16
distinct                     ok  
length and alphabet          ok  n=20
GC count = floor(n/2)        ok  GC counts [10]
pairwise Hamming >= d        ok  min 15 over 120 pairs
Hamming(x, rc(y)) >= d       ok  min 15 over 256 ordered pairs incl. self
self-pairs Hamming(x, rc(x)) ok  min 16
VALID
== checker on a corrupted copy (first letter of word 1 changed; must be INVALID)
size                         ok  16
distinct                     ok  
length and alphabet          ok  n=20
GC count = floor(n/2)        FAIL  GC counts [9, 10]
pairwise Hamming >= d        FAIL  min 14 over 120 pairs
Hamming(x, rc(y)) >= d       FAIL  min 14 over 256 ordered pairs incl. self
self-pairs Hamming(x, rc(x)) ok  min 16
INVALID
corrupted copy rejected
== size must be 16, strictly above the table entry 15
size 16
PASS
```
