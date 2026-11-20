# Receipts

Output of `sh verify-it-yourself/run_checks.sh`, run from the package folder on 2026-11-20 (Python 3 standard library):

```
== exact check of the code against the table cell
file sha256 96ddddaebbcc6cf5d43f8869ebf951cf4520634e12d32df060e8b4acc5b6f9f0
q = 4, n = 11, words read: 145
pairs checked: 10440 (all of them)
distance distribution: 7:3960 8:1980 9:2880 10:576 11:1044
minimum distance: 7
table lower bound 128, upper bound 320, size 145: margin over the lower bound 17
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
