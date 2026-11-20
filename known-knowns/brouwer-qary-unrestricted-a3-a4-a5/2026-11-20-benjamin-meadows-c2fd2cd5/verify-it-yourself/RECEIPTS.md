# Receipts

Output of `sh verify-it-yourself/run_checks.sh`, run from the package folder on 2026-11-20 (Python 3 standard library):

```
== exact check of the code against the table cell
file sha256 c2fd2cd5a942d6381693303c92e3f4ad107ad0a2f5565239dc443a55a6e24d6b
q = 4, n = 12, words read: 145
pairs checked: 10440 (all of them)
distance distribution: 8:5940 10:3456 12:1044
minimum distance: 8
table lower bound 128, upper bound 240, size 145: margin over the lower bound 17
PASS
== rebuild from the written description
object file: 145 lines of words, 145 distinct
rebuilt from 5 representatives and 2 generators: 145 words
rebuilt set equals the object's set: True
(other reading of the generators gives 145 words; equal to the object's set: True)
PASS
== planted bugs (each must be rejected)
planted bug: one changed symbol (word 1, position 3, 0 -> 1) -> checker exit 1, last line FAIL (rejected, as required)
planted bug: duplicated word (word 1 written twice) -> checker exit 1, last line FAIL (rejected, as required)
planted bug: symbol 4 outside the alphabet (last word, position 0) -> checker exit 1, last line FAIL (rejected, as required)
PASS
PASS
```
