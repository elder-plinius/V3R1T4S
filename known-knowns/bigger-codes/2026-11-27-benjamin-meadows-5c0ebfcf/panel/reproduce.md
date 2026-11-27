# REPRODUCE verdict: constant-weight-codes, cell A(29,10,8)
context: fresh reviewer (new subagent context started for the REPRODUCE role only; saw only the claim package and public pages; no access to other reviewers' files)
verdict_utc: 2026-11-27T18:56:39Z

## 1. Independent check of the object

I wrote my own checker (mycheck.py in my scratch folder, Python standard library, run with `/opt/homebrew/bin/python3 -I`) from the definition before opening anything in verify-it-yourself/. It reads each non-`#` line, requires exactly 29 characters from {0,1}, stores the word as a Python int, checks popcount == 8, distinctness, and computes popcount(x ^ y) for every one of the M(M-1)/2 pairs (no sampling).

`shasum -a 256 object/A-29-10-8-98words.txt`:
```
5c0ebfcf58bd20ac9e89c62b10560e485e9a416bf027df1dd4c680feaf3354ee
```
Checker output:
```
comment lines: 1
words: 98
format problems: none
distinct: 98
pairs: 4753 expected 4753
histogram: 10:2327 12:1315 14:714 16:397
min distance: 10
OK
```
This matches README.md and RUN_IT_YOURSELF.md exactly (sha256 5c0ebfcf..., 98 words, 4753 pairs, distribution 10:2327 12:1315 14:714 16:397, minimum distance 10). Only after this did I run the claimant's `sh verify-it-yourself/run_checks.sh` on my copy; it printed the same numbers, rejected all three planted bugs and ended in PASS.

## 2. Table cell

One curl request to https://aeb.win.tue.nl/codes/Andw.html (headers and body saved in my scratch folder):
- HTTP status: 200
- Date: Fri, 27 Nov 2026 18:53:56 GMT
- Last-Modified: Fri, 27 Nov 2026 00:32:42 GMT
- Content-Length: 130587 (body is 130587 bytes)
- sha256 of body: ad1196547427dbaa0ee7eb1970c445d4d7f4890c39860ebd8433bc9df6ceefad

Section "Bounds on A(n,10,w)", header columns w = 6..16; row n = 29, third data cell (w = 8):
```
<td><a href="cwc/d10/a29.10.8.96">96</a><sup>E</sup>-203</td>
```
Lower bound 96, upper bound 203. The mirror cell A(29,10,21) is not printed: the table's columns stop at w = 16 and only w <= n/2 is filled, so A(29,10,21) = A(29,10,8) is this same cell. 96 < 98 <= 203 holds. The page is byte-identical to the one in the-record-we-beat/RECORD.md (same Last-Modified, Content-Length and sha256), so the table has not changed since the claimant's fetch.

## 3. Rebuild

On a copy of the package in my scratch folder, `nice -n 15 sh how-we-built-it/rebuild.sh`, run once. Compiler: Apple clang version 21.0.0 (clang-2100.3.34.2), target arm64-apple-darwin27.2.0 (the original runs used g++ 13.3 on Linux x86-64, per how-we-built-it/COMMANDS.md). Output:
```
seed sha256 71b98dcc2ed90dabffe98c800d42162e852cc0babe8511ae3b60897a16f7e26b
seed words: 96
step 1: size 97, random seed 1011: RESULT FOUND pen 0 steps 27332716 restarts 26 cpu 35.5
step 2: size 98, random seed 1001: RESULT FOUND pen 0 steps 36240211 restarts 34 cpu 40.7
search output equals the object (without its first line), byte for byte
PASS
```
Exit status 0; wall time 86.49 s. Step counts and restart counts equal the recorded ones in how-we-built-it/chain.tsv and logs/original-runs.tsv; only CPU seconds differ (machine speed), which is expected because the CPU limit is only a cutoff (3600 s in the replay).

What I read in how-we-built-it/:
- cwbst.cpp contains no code words or tables of words. Its only inputs are n, w, d, target size, the RNG seed, the CPU limit, the output file, the start file and the three tabu settings. Randomness comes only from std::mt19937 seeded from the command line (its output sequence is fixed by the C++ standard); the padding library for the added word is built by an exhaustive Gosper enumeration of all C(29,8) weight-8 words in increasing order (deterministic); the unordered_set is used only for membership tests, so its iteration order cannot affect results. The time check reads CPU time only every 1024 steps and only decides whether to stop, so it cannot change the path of a run that succeeds. The search verifies penalty 0 from scratch before writing.
- seed_to_rows.py only reformats the downloaded seed file into 0/1 rows in file order (the seed file is already plain 0/1 rows).
- chain.tsv holds the two recorded steps (sizes 97, 98; seeds 1011, 1001; tabu 5 15 1000000; recorded step counts).
- rebuild.sh downloads the seed file, refuses to continue if its sha256 differs from 71b98dcc..., chains step 1's output into step 2, requires each run to end in `RESULT FOUND pen 0 steps` with the recorded count, and finally compares `grep -v '^#' object/A-29-10-8-98words.txt` with the step 2 output using `cmp -s`. The object's only `#` line is its first line, so this is a byte-for-byte comparison against the object file without its first line. The replay therefore depends only on the published seed code, the recorded seeds and settings, and the program source; the comparison is honest.

## 4. Seed code

One curl request to https://aeb.win.tue.nl/codes/cwc/d10/a29.10.8.96 (the URL named in README.md): HTTP 200, Date Fri, 27 Nov 2026 18:55:57 GMT, Last-Modified Sun, 02 Aug 2026 11:05:44 GMT, Content-Length 2880. `shasum -a 256`: 71b98dcc2ed90dabffe98c800d42162e852cc0babe8511ae3b60897a16f7e26b, which equals SEED_SHA in how-we-built-it/rebuild.sh. It has 96 distinct words of length 29 and weight 8 with minimum distance 10 (overlap.py in my scratch folder). 54 of the object's 98 words occur in the seed code (0 under bit reversal), so the search changed 42 seed-derived positions and added 2 words; the object is not the seed with two words appended.

## Problems found

none. (Minor, not affecting the claim: the CPU times in the rebuild differ from the recorded ones, as expected on different hardware.)

## Reasoning

Every check in this role holds: the object is 98 distinct length-29 weight-8 binary words with minimum distance 10, verified over all 4753 pairs by my own checker; its sha256 and distance histogram match README.md; the live table cell A(29,10,8) reads 96-203 (mirror cell is the same cell), so 96 < 98 <= 203; the claimant's rebuild, run once on a different compiler and architecture (Apple clang, arm64), reproduces the object byte for byte from the hash-checked public seed code and the recorded seeds, with identical step and restart counts. Checking the arXiv papers named in the success criterion (Echols, Lysenstoen, newer) is outside the REPRODUCE role and was not done here.

pass: true
