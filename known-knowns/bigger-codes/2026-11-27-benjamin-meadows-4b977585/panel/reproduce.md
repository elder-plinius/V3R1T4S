# REPRODUCE verdict: constant-weight-codes, cell A(27,8,12)
context: fresh reviewer (new subagent context started for the REPRODUCE role only; saw only the claim package and public pages; no access to other reviewers' files)
verdict_utc: 2026-11-27T18:56:43Z

## 1. Independent check of the object

I wrote my own checker (my scratch folder, mycheck.py, Python standard library, run with `/opt/homebrew/bin/python3 -I`) from the definition before opening verify-it-yourself/. It reads object/A-27-8-12-3387words.txt, requires exactly one leading `#` line, then for every other line checks length 27, alphabet {0,1}, weight 12 (word stored as a Python int, popcount), distinctness, and the Hamming distance of every pair (full double loop, no sampling).

Output:

```
sha256 4b977585972408991e43784ce2f81591c529d9f3a9d770ee9fc4262eb056e3ba
header lines 1
M 3387 pairs 5734191 expected 5734191
min distance 8
histogram {8: 654035, 10: 288850, 12: 2442986, 14: 949326, 16: 1118579, 18: 228926, 20: 49452, 22: 749, 24: 1288}
OK
```

This matches README.md: sha256 4b977585..., 3387 words, length 27, weight 12, minimum distance 8, 5734191 pairs. Complementing every word gives a (27,8,15) code of the same size, so A(27,8,15) >= 3387 follows.

After my own check I ran the claimant's verify-it-yourself/run_checks.sh on my scratch copy: it reported the same sha256, the same pair count, the identical distance distribution, minimum distance 8, rejected all three planted-bug copies, and ended in `PASS`. The claimant's checker makes no network request (it takes the bounds 3374 and 10460 as arguments).

## 2. The table cell

One request: `curl -sS -D andw.headers -o andw.html -w 'http=%{http_code} size=%{size_download}' https://aeb.win.tue.nl/codes/Andw.html` at 2026-11-27T18:53:53Z.

- HTTP status: 200
- Date: Fri, 27 Nov 2026 18:53:54 GMT
- Last-Modified: Fri, 27 Nov 2026 00:32:42 GMT
- Content-Length: 130587 (130587 bytes saved)
- sha256 of body: ad1196547427dbaa0ee7eb1970c445d4d7f4890c39860ebd8433bc9df6ceefad (identical to the hash in the-record-we-beat/RECORD.md)

Section "Bounds on A(n,8,w)" (anchor d8): header columns w = 5..14; row 27 has nine cells for w = 5..13. The eighth cell (w = 12) reads in the source:

```
<td><a href="cwc/d8/a27.8.12.3374H">3374</a><sup>Di</sup>-10460<sup>KT</sup></td>
```

Footnote: `Di: Kerem Dilker, email 2026-11-26 with 31 new bounds.` The mirror cell A(27,8,15) is not printed: row 27 stops at w = 13, so the table lists only w up to about n/2 and the w = 12 cell is the only entry for the pair. Check: 3374 < 3387 <= 10460 holds (margin 13).

## 3. Rebuild

I copied the whole package into my scratch folder (the copy's object file has the same sha256) and ran `nice -n 15 sh how-we-built-it/rebuild.sh` once from it. Compiler: Apple clang version 21.0.0 (clang-2100.3.34.2), target arm64-apple-darwin27.2.0, so no -mpopcnt flag was used and the build differs from the claimant's Linux x86-64 g++ 13.3 build. Exit status 0, real 105.17 s, user 93.01 s. Output:

```
seed sha256 91aff7ff2e09ed7449bd464412f5ceba1e37e02d5d2f08fc46ee89d835baf7a6
seed words: 3374
step 1: size 3375, random seed 1002: RESULT FOUND pen 0 steps 102469 restarts 0 cpu 2.8
step 2: size 3376, random seed 1001: RESULT FOUND pen 0 steps 30924 restarts 0 cpu 1.7
step 3: size 3377, random seed 1003: RESULT FOUND pen 0 steps 32966 restarts 0 cpu 1.9
step 4: size 3378, random seed 1001: RESULT FOUND pen 0 steps 40104 restarts 0 cpu 2.0
step 5: size 3379, random seed 1001: RESULT FOUND pen 0 steps 32818 restarts 0 cpu 1.9
step 6: size 3380, random seed 1001: RESULT FOUND pen 0 steps 58467 restarts 0 cpu 2.3
step 7: size 3381, random seed 1001: RESULT FOUND pen 0 steps 56931 restarts 0 cpu 2.3
step 8: size 3382, random seed 1001: RESULT FOUND pen 0 steps 27316 restarts 0 cpu 1.7
step 9: size 3383, random seed 1002: RESULT FOUND pen 0 steps 37095 restarts 0 cpu 1.8
step 10: size 3384, random seed 1001: RESULT FOUND pen 0 steps 1789499 restarts 1 cpu 30.0
step 11: size 3385, random seed 1009: RESULT FOUND pen 0 steps 33756 restarts 0 cpu 1.6
step 12: size 3386, random seed 1001: RESULT FOUND pen 0 steps 630983 restarts 0 cpu 10.4
step 13: size 3387, random seed 1001: RESULT FOUND pen 0 steps 2157585 restarts 2 cpu 32.7
search output equals the object (without its first line), byte for byte
PASS
```

Every step count equals the steps_original column of how-we-built-it/chain.tsv, and the run ends in PASS.

What I read in how-we-built-it/ and what it shows:

- rebuild.sh downloads exactly one file (the seed code URL), refuses to continue unless its sha256 is 91aff7ff..., converts it with seed_to_rows.py, compiles cwbst.cpp, and runs the 13 rows of chain.tsv in order. Each run's start file is the previous run's output; the first start file is the converted seed code. No other input file, cached code or intermediate result from the claimant is used. Each run's command line comes only from chain.tsv (size, random seed, tabu min/max, restart limit) plus fixed n = 27, w = 12, d = 8 and a 3600 s CPU limit.
- seed_to_rows.py decodes the `$BASE=16` format (one hex number per word, left-padded to 27 binary digits) and keeps the file's order; it does not add, drop or reorder words.
- cwbst.cpp uses only std::mt19937 seeded from the command line (its output sequence is fixed by the C++ standard) and `rng() % k` choices. The pad-word sample uses its own mt19937 seeded from the main stream. The unordered_set is used only for membership tests, never iterated, so hash order cannot affect the result. CPU time is read only to decide whether to stop (checked every 1024 steps); it never influences a choice. A run is therefore a function of the start file, the seed and the settings, which is consistent with an Apple clang arm64 build reproducing the Linux g++ step counts exactly. The program re-checks the full penalty before writing an output, so a reported FOUND means the written code has no pair below distance 8.
- The final comparison is `grep -v '^#' object/A-27-8-12-3387words.txt | cmp -s - "$prev"`: the object file without its `#` description line is compared byte for byte with the last run's output file. The comparison is honest: it reads the object file in the package (not a copy produced by the search), and cmp fails on any byte difference, including line order and trailing newline.

## 4. Seed code

One request: `curl -sS -D seed.headers -o a27.8.12.3374H https://aeb.win.tue.nl/codes/cwc/d8/a27.8.12.3374H` at 2026-11-27T18:56:22Z: HTTP 200, Date Fri, 27 Nov 2026 18:56:22 GMT, Last-Modified Thu, 26 Nov 2026 20:15:24 GMT, Content-Length 27001. sha256 91aff7ff2e09ed7449bd464412f5ceba1e37e02d5d2f08fc46ee89d835baf7a6, equal to SEED_SHA in how-we-built-it/rebuild.sh and to RECORD.md. (rebuild.sh also downloaded this URL once during step 3, as designed.)

My own script (my scratch folder, overlap.py) decoded the file: 3374 words, all weight 12, minimum distance 8 (the hosted code is itself a valid (27,8,12) code of size 3374, matching the table's lower bound). 2699 of the object's 3387 words are words of the seed code; the other 688 are words changed or added by the search.

## Problems found

None within this role. Note on scope: the success criterion also requires M to exceed any value for this cell in arXiv:2608.13906, arXiv:2607.19550 and newer arXiv papers. That comparison is not one of the REPRODUCE checks in my brief and I did not fetch those papers; README.md states 3337 (Echols) and no value (Lysenstoen) for this cell.

## Reasoning

The object is exactly what README.md says: 3387 distinct weight-12 words of length 27 with minimum distance 8, sha256 4b977585... It beats the live table's lower bound 3374 (page Last-Modified Fri, 27 Nov 2026 00:32:42 GMT, same page hash as the claimant's record) and stays below the upper bound 10460. The rebuild, on a different compiler and architecture, regenerated the object byte for byte from the published seed code and the 13 recorded seeds and settings, with every step count matching the record.

pass: true
