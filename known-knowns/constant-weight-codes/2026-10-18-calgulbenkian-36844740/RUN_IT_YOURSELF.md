# Run it yourself

From this folder, in a fresh shell (python3 3.8 or later, standard library only; numpy is optional):

```sh
sh verify-it-yourself/run_checks.sh
```

The last line should be `ALL CHECKS PASS`. The checker alone:

```sh
python3 -I verify-it-yourself/check_cw_std.py object/A51_6_6_11187.txt 51 6 6 11187
```

Expected output: `A51_6_6_11187.txt: M=11187 n=51 w=6 distinct, weight w, no two words share 4 ones, so min distance >= 6 PASS`.

What it asserts: every line is a 0/1 string of length 51; there are exactly 11187 lines; they are all distinct; each has exactly 6 ones; and no two words share 4 ones (two distinct weight-6 words that share at most 3 ones differ in at least 6 positions, and conversely), so every pairwise distance is at least 6. For the direct check of every pair, add `--pairwise` (pure Python; slow for large codes: minutes for the biggest). The run script also checks the sha256 of the object against INDEX.csv, runs the panel's numpy checker `check_cw.py` when numpy is installed, and runs three negative controls (a duplicated word, a claim of one more word, and a word forced to share 4 ones with another), all of which must be rejected.

Compare with the live table: save the page with `curl -A 'V3R1T4S-research (honest client; curl)' -o Andw.html https://aeb.win.tue.nl/codes/Andw.html` and run `python3 -I the-record-we-beat/tools/andw_cells.py Andw.html 51,6,6`; the cell was `11184Pl-16660` when fetched.

How to rebuild the object: the search is randomised and its exact commands are not recorded (see `how-we-built-it/README.md`), so the object cannot be regenerated bit for bit. The object file itself is the certificate; the check above needs nothing else.
