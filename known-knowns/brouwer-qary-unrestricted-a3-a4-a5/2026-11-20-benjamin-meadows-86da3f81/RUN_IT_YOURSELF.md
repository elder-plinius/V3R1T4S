# Run it yourself

From this folder, in a fresh shell (Python 3, standard library only):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:

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

The three steps can also be run one at a time:

```sh
python3 verify-it-yourself/check_code.py object/A3-15-10-31words.txt 3 15 10 31 27 39 86da3f818e06cbe15a35aabf63c8849ee96e1ccf3dd36c9964113732876d9555
python3 verify-it-yourself/rebuild.py object/A3-15-10-31words.txt
python3 verify-it-yourself/planted_bugs.py object/A3-15-10-31words.txt 3 15 10 31 27 39
```

check_code.py arguments: code file, q, n, d, claimed size, table lower bound, table upper bound, expected sha256.

## Rebuild

verify-it-yourself/rebuild.py holds the generators and the orbit representatives as plain lists and rebuilds the code from them; it is the description of the object, run as a program. Maximality (no word can be added) is checked by a separate C program: `cc -O2 -o maximal how-we-built-it/maximal.c && ./maximal object/A3-15-10-31words.txt 3 15 10` (about a second; expected last line ends `addable words=0`; output in how-we-built-it/MAXIMALITY.txt).

## Where it came from

how-we-built-it/COMMANDS.md gives the search commands; the logs of the search are in how-we-built-it/logs/.
