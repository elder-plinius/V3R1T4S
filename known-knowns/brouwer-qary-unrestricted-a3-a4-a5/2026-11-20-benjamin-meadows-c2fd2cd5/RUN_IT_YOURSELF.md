# Run it yourself

From this folder, in a fresh shell (Python 3, standard library only):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:

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

The three steps can also be run one at a time:

```sh
python3 verify-it-yourself/check_code.py object/A4-12-8-145words.txt 4 12 8 145 128 240 c2fd2cd5a942d6381693303c92e3f4ad107ad0a2f5565239dc443a55a6e24d6b
python3 verify-it-yourself/rebuild.py object/A4-12-8-145words.txt
python3 verify-it-yourself/planted_bugs.py object/A4-12-8-145words.txt 4 12 8 145 128 240
```

check_code.py arguments: code file, q, n, d, claimed size, table lower bound, table upper bound, expected sha256.

## Rebuild

verify-it-yourself/rebuild.py holds the generators and the orbit representatives as plain lists and rebuilds the code from them; it is the description of the object, run as a program. Maximality (no word can be added) is checked by a separate C program: `cc -O2 -o maximal how-we-built-it/maximal.c && ./maximal object/A4-12-8-145words.txt 4 12 8` (about a second; expected last line ends `addable words=0`; output in how-we-built-it/MAXIMALITY.txt).

## Where it came from

how-we-built-it/COMMANDS.md gives the search commands; the logs of the search are in how-we-built-it/logs/.
