# Receipts

Output of `sh verify-it-yourself/run_checks.sh`, run from the package folder on 2026-11-20 (Python 3 standard library):

```
== exact check of the code against the table cell
file sha256 86da3f818e06cbe15a35aabf63c8849ee96e1ccf3dd36c9964113732876d9555
q = 3, n = 15, words read: 31
pairs checked: 465 (all of them)
distance distribution: 10:360 11:75 12:30
minimum distance: 10
table lower bound 27, upper bound 39, size 31: margin over the lower bound 4
PASS
== rebuild from the written description
object file: 31 lines of words, 31 distinct
rebuilt from 2 representatives and 2 generators: 31 words
rebuilt set equals the object's set: True
(other reading of the generators gives 31 words; equal to the object's set: True)
PASS
== planted bugs (each must be rejected)
planted bug: one changed symbol (word 2, position 1, 0 -> 1) -> checker exit 1, last line FAIL (rejected, as required)
planted bug: duplicated word (word 1 written twice) -> checker exit 1, last line FAIL (rejected, as required)
planted bug: symbol 3 outside the alphabet (last word, position 0) -> checker exit 1, last line FAIL (rejected, as required)
PASS
PASS
```
