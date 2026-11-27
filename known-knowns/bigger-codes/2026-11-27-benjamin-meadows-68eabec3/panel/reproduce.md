# REPRODUCE verdict: constant-weight-codes, cell A(27,8,8)
context: fresh reviewer (new subagent context started for the REPRODUCE role only; saw only the claim package and public pages; no access to other reviewers' files)
verdict_utc: 2026-11-27T18:55:32Z

## 1. Independent check of the object

I wrote my own checker (mycheck.py in my scratch folder, Python standard library, run with `/opt/homebrew/bin/python3 -I`) from the definition before opening verify-it-yourself/. It reads object/A-27-8-8-778words.txt, skips the one `#` line, requires every other line to be 27 characters from {0,1}, converts each to a Python int, asserts popcount 8 for every word and that all words are distinct, then computes the popcount of x XOR y for every one of the M(M-1)/2 pairs (no sampling).

Output:

```
sha256 68eabec3d2808175e4f0f8db629c0b6137d8ab94b19e8e24e23186b03f6bc26f
header_lines 1 word_lines 778
M 778 pairs 302253 expected 302253
min_distance 8
hist {8: 90546, 10: 19328, 12: 161656, 14: 18110, 16: 12613}
ALL_OK
```

This matches README.md: sha256 68eabec3..., 778 words, length 27, weight 8, minimum distance 8, 302253 pairs. After my own check I ran the claimant's verify-it-yourself/run_checks.sh on my copy. It ended in `PASS`, and each of its three planted-bug copies was rejected.

## 2. Table cell

One curl request to https://aeb.win.tue.nl/codes/Andw.html (headers and body saved in my scratch folder):

- HTTP status 200
- Date: Fri, 27 Nov 2026 18:53:52 GMT
- Last-Modified: Fri, 27 Nov 2026 00:32:42 GMT
- Content-Length: 130587 (130587 bytes received)
- sha256 of body: ad1196547427dbaa0ee7eb1970c445d4d7f4890c39860ebd8433bc9df6ceefad (identical to the hash in the-record-we-beat/RECORD.md)

In the section "Bounds on A(n,8,w)", the header columns are w = 5, 6, ..., 14. Row 27, fourth data cell (w = 8):

```
<td><a href="cwc/d8/a27.8.8.777H">777</a><sup>Di</sup>-1252</td>
```

Lower bound 777, upper bound 1252. The mirror cell A(27,8,19) is not printed because the table's columns stop at w = 14. The subsection "Lower bounds for A(n,8,8) and kissing numbers" has no entry for n = 27. Check: 777 < 778 <= 1252 holds, with a margin of 1.

I did not check the arXiv comparison values (Echols, Lysenstoen) because they are outside the REPRODUCE role.

## 3. Rebuild

I copied the package into my scratch folder and ran `nice -n 15 sh how-we-built-it/rebuild.sh` once. Compiler: Apple clang version 21.0.0 (clang-2100.3.34.2), target arm64-apple-darwin27.2.0, so no -mpopcnt. Output:

```
seed sha256 b342cddfbbf96828dff9f5763b2d63138af014c7d0f94e8a41197dd88cd01868
seed words: 777
step 1: size 778, random seed 1005: RESULT FOUND pen 0 steps 7029649 restarts 7 cpu 34.7
search output equals the object (without its first line), byte for byte
PASS
```

Exit status 0, wall time 42.55 s. The step count 7029649 matches chain.tsv and logs/original-runs.tsv (original: Linux x86-64, g++, 55.1 CPU s). A recursive diff afterwards showed my copy was unchanged against the package.

What I read in how-we-built-it/:

- rebuild.sh downloads only the seed URL and refuses to continue if the sha256 differs. It converts the seed with seed_to_rows.py, which keeps the file's order and expands hex to binary with left padding to 27 digits. It compiles cwbst.cpp and runs it with the size, seed and tabu settings from chain.tsv. It requires each step's RESULT line to show penalty 0 at the recorded step count. At the end it runs `grep -v '^#' object/... | cmp -s - output`, a byte-for-byte comparison of the object without its comment line against the program's output. The object is never fed into the search, so the comparison is honest.
- cwbst.cpp uses only the C++ standard library. Its randomness comes from std::mt19937 seeded from the command line, and mt19937 output is fixed by the standard. Padding words come from a full Gosper enumeration of the weight-8 words, which is deterministic because C(27,8)·777 is below its 4e9 limit. The unordered_set is used only for membership tests, never iterated, so it cannot change the order. The CPU-time limit (3600 s in the rebuild, 120 s in the original) only decides when a run stops, and the step counts match, so it did not affect this run. Before writing its output the program recomputes the full penalty and requires it to be 0. Bit i of the internal word is character i of the row on both read and write, so the orientation stays consistent.
- The replay therefore depends only on the published seed file, the recorded random seed 1005, the tabu settings 5 15 1000000 and the program source. It produced the same result on a different OS, compiler and architecture (Apple clang on arm64) than the original (g++ on x86-64).
- rebuild.sh calls `python3` from PATH for the seed conversion and hashing, not a pinned interpreter. This has no effect on the result.

## 4. Seed code

One curl request to https://aeb.win.tue.nl/codes/cwc/d8/a27.8.8.777H returned HTTP 200 (Date: Fri, 27 Nov 2026 18:55:14 GMT; Last-Modified: Thu, 26 Nov 2026 20:15:24 GMT; Content-Length: 6225). Its sha256 is b342cddfbbf96828dff9f5763b2d63138af014c7d0f94e8a41197dd88cd01868, which matches SEED_SHA in how-we-built-it/rebuild.sh. The file is `$BASE=16` followed by 777 distinct hex words, all of weight 8.

Overlap (overlap.py in my scratch folder): 651 of the 778 object words also appear in the seed code and 127 do not. With the bit order reversed the overlap is 0, which confirms that both files are compared in the same orientation. This fits README.md's description: the search adds one word to the 777 seed words and then moves bits in some words to clear the conflicts.

## Problems found

none

## Reasoning

The object is exactly what README.md describes: 778 distinct words of length 27 and weight 8, minimum distance 8, and sha256 68eabec3.... It lies strictly above the table's lower bound of 777 and below its upper bound of 1252, read today from a page whose bytes are identical to the claimant's snapshot. The search can be rebuilt: one run of the published program, using only the published seed code and the recorded seed and settings, reproduced the object byte for byte on Apple clang/arm64 with the recorded step count. All four checks in the REPRODUCE role hold.

pass: true
