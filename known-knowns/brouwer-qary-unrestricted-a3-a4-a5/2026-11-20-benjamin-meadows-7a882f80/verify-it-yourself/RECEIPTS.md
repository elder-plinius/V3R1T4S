# Receipts

Output of `sh verify-it-yourself/run_checks.sh`, run from the package folder on 2026-11-20 (Python 3 standard library):

```
== exact check of the code against the table cell
file sha256 7a882f805e40e7ef6a9565684cc1c36d616b91f2d3081be69aef2d00dfe69d82
q = 4, n = 12, words read: 320
pairs checked: 51040 (all of them)
distance distribution: 7:10176 8:6816 9:17536 10:5376 11:10176 12:960
minimum distance: 7
table lower bound 256, upper bound 1167, size 320: margin over the lower bound 64
PASS
== rebuild from the written description
object file: 320 lines of words, 320 distinct
rebuilt from 11 representatives and 2 generators: 320 words
rebuilt set equals the object's set: True
(other reading of the generators gives 396 words; equal to the object's set: False)
PASS
== planted bugs (each must be rejected)
planted bug: one changed symbol (word 1, position 1, 0 -> 1) -> checker exit 1, last line FAIL (rejected, as required)
planted bug: duplicated word (word 1 written twice) -> checker exit 1, last line FAIL (rejected, as required)
planted bug: symbol 4 outside the alphabet (last word, position 0) -> checker exit 1, last line FAIL (rejected, as required)
PASS
PASS
```
