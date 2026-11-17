# Run it yourself

From this folder, in a fresh shell (python3 3.8 or later, standard library only; numpy is optional):

```sh
sh verify-it-yourself/run_checks.sh
```

The last line should be `ALL CHECKS PASS`. The checker alone:

```sh
python3 -I verify-it-yourself/check_cw_std.py object/A45_8_7_1913.txt 45 8 7 1913
```

Expected output: `A45_8_7_1913.txt: M=1913 n=45 w=7 distinct, weight w, no two words share 4 ones, so min distance >= 8 PASS`.

What it asserts: every line is a 0/1 string of length 45; there are exactly 1913 lines; they are all distinct; each has exactly 7 ones; and no two words share 4 ones (two distinct weight-7 words that share at most 3 ones differ in at least 8 positions, and conversely), so every pairwise distance is at least 8. For the direct check of every pair, add `--pairwise` (pure Python; slow for large codes: minutes for the biggest). The run script also checks the sha256 of the object against INDEX.csv, runs the panel's numpy checker `check_cw.py` when numpy is installed, and runs three negative controls (a duplicated word, a claim of one more word, and a word forced to share 4 ones with another), all of which must be rejected.

Compare with the live table: save the page with `curl -A 'V3R1T4S-research (honest client; curl)' -o Andw.html https://aeb.win.tue.nl/codes/Andw.html` and run `python3 -I the-record-we-beat/tools/andw_cells.py Andw.html 45,8,7`; the cell was `1907Pl-4050` when fetched.

How to rebuild the object: the search is randomised and its exact commands are not recorded (see `how-we-built-it/README.md`), so the object cannot be regenerated bit for bit. The object file itself is the certificate; the check above needs nothing else.
