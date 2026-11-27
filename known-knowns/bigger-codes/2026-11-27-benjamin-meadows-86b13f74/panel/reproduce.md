# REPRODUCE verdict: constant-weight-codes, cell A(25,10,12)
context: fresh reviewer (new subagent context started for the REPRODUCE role only; saw only the claim package and public pages; no access to other reviewers' files)
verdict_utc: 2026-11-27T18:55:45Z

## 1. Own checker on the object

I wrote my own checker (mycheck.py in my scratch folder, Python standard library, run with `python3 -I`) from the definition, before reading verify-it-yourself/. It skips the first line (a `#` comment), requires every other line to be 25 characters over {0,1} with exactly 12 ones, stores each word as a Python int, checks they are all distinct, and computes the popcount of x ^ y for all pairs (no sampling).

Output:

```
sha256 86b13f74de60c58c60f8255a4ced73ad9a126038dc79c543021b55b5159bc658
M 142 distinct 142
pairs 10011 min distance 10 histogram {10: 3930, 12: 1972, 14: 2596, 16: 1119, 18: 367, 20: 26, 22: 1}
OK
```

`shasum -a 256` gives the same hash. The file has 143 lines: 1 comment line and 142 words. All of this matches README.md (142 words, length 25, weight 12, minimum distance 10, 10011 pairs, the same sha256).

## 2. Brouwer table

I fetched https://aeb.win.tue.nl/codes/Andw.html once with curl at 2026-11-27T18:53:51Z (UTC, from `date -u`):

- HTTP status 200
- Date: Fri, 27 Nov 2026 18:53:52 GMT
- Last-Modified: Fri, 27 Nov 2026 00:32:42 GMT
- Content-Length: 130587 (the saved body is 130587 bytes)
- body sha256 ad1196547427dbaa0ee7eb1970c445d4d7f4890c39860ebd8433bc9df6ceefad. This is the same hash and the same Last-Modified that the-record-we-beat/RECORD.md records.

In the section "Bounds on A(n,10,w)" the column headers run w = 6..16. Row n = 25 has 7 cells for w = 6..12. The w = 12 cell is:

```
<td><a href="cwc/d10/a25.10.12.141H">141</a><sup>E</sup>-433<sup>KT</sup></td>
```

So the lower bound is 141 and the upper bound is 433. The mirror cell A(25,10,13) is not printed, because row 25 stops at w = 12 = floor(n/2). This gives 141 < 142 <= 433, so the claim holds against the table.

## 3. Rebuild

I copied the package into my scratch folder and ran `nice -n 15 sh how-we-built-it/rebuild.sh` once from the copy, with `python3` resolving to Homebrew Python 3.15.2. The compiler is **Apple clang** version 21.0.0 (clang-2100.3.34.2), target arm64-apple-darwin, so the script adds no `-mpopcnt`. Output:

```
seed sha256 71f7603eac9ee759f07696eb2741dcb9b159503eee639f13a28bfd66493a4a97
seed words: 141
step 1: size 142, random seed 1017: RESULT FOUND pen 0 steps 22733579 restarts 20 cpu 45.9
search output equals the object (without its first line), byte for byte
PASS
```

It ran from 18:54:26Z to 18:55:20Z (real 53.83 s, user 46.23 s) and exited 0. The step count (22733579) matches chain.tsv, logs/original-runs.tsv and logs/rebuild-run.log, where it was recorded on Linux x86-64 with g++. So the result is the same across compilers and architectures.

I read how-we-built-it/rebuild.sh, cwbst.cpp, seed_to_rows.py and chain.tsv:

- **Inputs.** The replay uses only three things:
  - the downloaded seed file, which must have the pinned sha256 or the script fails
  - its hex-to-0/1 conversion, which keeps the file's order
  - the single recorded row of chain.tsv (size 142, seed 1017, tabu settings 5 15 1000000)

  No other file is read. cwbst.cpp uses only the standard library.
- **No platform-dependent randomness.** The program uses std::mt19937, whose output the standard defines exactly, and only takes `rng() % k` of it. It uses no std:: distributions, which could differ between library implementations.
- **Padding is enumerated, not sampled.** The extra word is chosen from a full Gosper enumeration of all C(25,12) = 5,200,300 weight-12 words, because that is under the program's 5e7 limit.
- **The CPU limit cannot change the output.** The limit (3600 s in the replay) only decides whether the run stops early. A run that stops early would print NOT_FOUND and the script would FAIL.
- **The comparison is honest.** `grep -v '^#' object/A-25-10-12-142words.txt | cmp -s - "$prev"` compares the program's freshly written output file with the object minus its comment lines. The object has exactly one such line, its first. The script also requires the exact recorded step count before it compares.

## 4. Seed code

I fetched https://aeb.win.tue.nl/codes/cwc/d10/a25.10.12.141H once with curl:

- HTTP status 200
- Date: Fri, 27 Nov 2026 18:55:30 GMT
- Last-Modified: Sun, 02 Aug 2026 11:05:43 GMT
- Content-Length: 1137
- sha256 71f7603eac9ee759f07696eb2741dcb9b159503eee639f13a28bfd66493a4a97, which equals SEED_SHA in how-we-built-it/rebuild.sh

The file is `$BASE=16` followed by 141 hex words. I converted them with my own script (overlap.py in my scratch folder) and found:

- 141 distinct words, minimum distance 10
- **117 of the 142 object words are also in the seed code**
- the other 25 words are 24 seed words that the search changed plus one added word

The object's first 141 rows are not the seed rows in order, which is expected because the search changes seed words in place.

(The rebuild script made its own separate download of the same seed URL, as the brief requires the rebuild to do.)

## Claimant checker (after my own checks)

After my own checks I ran verify-it-yourself/run_checks.sh in my scratch copy. It ends in PASS, and it rejects all three planted-bug copies (distance 8 pair, wrong weight, duplicate). It reports the same bound comparison (141, 433, margin 1).

## Problems found

None in this role's checks.

Not covered by this role: the success criterion also needs M to beat any value for this cell in arXiv:2608.13906, arXiv:2607.19550 or newer arXiv papers. README.md states Echols lists 141 and Lysenstoen lists no value, but I did not re-check the arXiv papers. My brief assigns the four checks above to this role, and all four hold.

## Reasoning

- The object is exactly what README.md says (hash, size, length, weight, distinctness, minimum distance 10 over every pair).
- It strictly beats the live table's lower bound of 141 and stays under the upper bound of 433.
- It rebuilds byte for byte from the published seed code with the recorded seed and settings, on a different compiler and architecture from the original run, through a replay whose only inputs are the pinned seed file, the published source and chain.tsv.

pass: true
