# Run it yourself

From this folder, in a fresh shell (python3 3.8 or later, standard library only; numpy is optional):

```sh
sh verify-it-yourself/run_checks.sh
```

The last line should be `ALL CHECKS PASS`. The checker alone:

```sh
python3 -I verify-it-yourself/check_cw_std.py object/A27_8_11_2422.txt 27 8 11 2422
```

Expected output: `A27_8_11_2422.txt: M=2422 n=27 w=11 distinct, weight w, no two words share 8 ones, so min distance >= 8 PASS`.

What it asserts: every line is a 0/1 string of length 27; there are exactly 2422 lines; they are all distinct; each has exactly 11 ones; and no two words share 8 ones (two distinct weight-11 words that share at most 7 ones differ in at least 8 positions, and conversely), so every pairwise distance is at least 8. For the direct check of every pair, add `--pairwise` (pure Python; slow for large codes: minutes for the biggest). The run script also checks the sha256 of the object against INDEX.csv, runs the panel's numpy checker `check_cw.py` when numpy is installed, and runs three negative controls (a duplicated word, a claim of one more word, and a word forced to share 8 ones with another), all of which must be rejected.

Compare with the live table: save the page with `curl -A 'V3R1T4S-research (honest client; curl)' -o Andw.html https://aeb.win.tue.nl/codes/Andw.html` and run `python3 -I the-record-we-beat/tools/andw_cells.py Andw.html 27,8,11`; the cell was `2421Pl-7754` when fetched.

How to rebuild the object: the search is randomised and its exact commands are not recorded (see `how-we-built-it/README.md`), so the object cannot be regenerated bit for bit. The object file itself is the certificate; the check above needs nothing else.
