# REPRODUCE verdict: constant-weight-codes, cell A(26,10,12)
context: fresh reviewer (new subagent context started for the REPRODUCE role only; saw only the claim package and public pages; no access to other reviewers' files)
verdict_utc: 2026-11-27T18:56:04Z

## 1. Independent check of the object

I wrote my own checker (mycheck.py in my scratch folder, Python standard library, run with `/opt/homebrew/bin/python3 -I`) from the definition before I opened anything in verify-it-yourself/. It reads each non-comment line as a 26-character 0/1 string, rejects any other length or symbol, stores each word as a Python int, and checks the weight of every word, distinctness, and the Hamming distance of every pair (all pairs, no sampling).

Output on object/A-26-10-12-214words.txt:

```
sha256 c78abc24b831d29945e88f58953941927761132fa60f8a2cd2696a5dcec81715
comment lines 1 words 214
wrong-weight words 0
distinct 214
pairs 22791 expected 22791
histogram 10:5210 12:8756 14:2712 16:4676 18:1425 20:12
min distance 10
OK
```

`shasum -a 256` gives the same hash. The sha256, word count (214), pair count (22791), minimum distance (10) and distance histogram all match README.md and RUN_IT_YOURSELF.md exactly. I then read the claimant's verify-it-yourself/check_cw.py and ran verify-it-yourself/run_checks.sh on a copy of the package. It ends in `PASS`, and all three planted-bug copies were rejected.

## 2. Table cell (one curl request)

`curl -sS -D andw.headers -o andw.html -w '%{http_code}' https://aeb.win.tue.nl/codes/Andw.html`, run at 2026-11-27T18:53:58Z:

- HTTP status 200
- Date: Fri, 27 Nov 2026 18:53:58 GMT
- Last-Modified: Fri, 27 Nov 2026 00:32:42 GMT
- Content-Length: 130587 (file size 130587 bytes)
- ETag: "1fe1b-6613732bff19f"
- sha256 of body: ad1196547427dbaa0ee7eb1970c445d4d7f4890c39860ebd8433bc9df6ceefad. This is identical to the sha256 in the-record-we-beat/RECORD.md, so the page has not changed since the claimant's fetch.

In section "Bounds on A(n,10,w)" (column headers w = 6 to 16), the row `<th>26</th>` reads 13, 30-36, 68-104, 91-213, 130-397, 168-565, then for w = 12:

```
<td><a href="cwc/d10/a26.10.12.213H">213</a><sup>Bol</sup>-691<sup>KT</sup></td>
```

So the lower bound is 213 and the upper bound is 691. The mirror cell A(26,10,14) is not printed, because the row stops at w = 13 = n/2. Since the object's complement gives the mirror cell, the same bounds apply to it. The check 213 < 214 <= 691 holds.

## 3. Rebuild

My machine's compiler is Apple clang (`Apple clang version 21.0.0 (clang-2100.3.34.2)`, arm64). The original runs used g++ 13.3 on Linux x86-64.

I copied the whole package into my scratch folder and ran `nice -n 15 sh how-we-built-it/rebuild.sh` from the copy, once. Exit status 0, wall time 34.57 s, user time 28.22 s. Output:

```
seed sha256 662ef208b5b79c7dd842e717caf9fa298cb1f217b9bdcbad433a0cfc363199d4
seed words: 213
step 1: size 214, random seed 1005: RESULT FOUND pen 0 steps 10436323 restarts 10 cpu 27.5
search output equals the object (without its first line), byte for byte
PASS
```

The step count 10436323 matches chain.tsv, logs/original-runs.tsv and COMMANDS.md, which means the search followed the same trajectory on a different compiler and architecture.

What I found reading how-we-built-it/:

- rebuild.sh downloads only the seed URL and checks its sha256 before use. It converts the seed with seed_to_rows.py and compiles cwbst.cpp with `-O2 -std=c++17` (no `-mpopcnt` on arm64). It runs the one row of chain.tsv with size 214, seed 1005, tabu 5 15, restart 1000000 and a 3600 s CPU cap. It accepts only `RESULT FOUND pen 0 steps 10436323`. Finally it compares `grep -v '^#' object/...` against the search output with `cmp -s`. That is an honest byte-for-byte comparison against the object minus its single comment line, and no other data enters.
- cwbst.cpp takes all randomness from one `std::mt19937` seeded from the command line. mt19937 output is fixed by the C++ standard, and the program uses no other generator. The padding word is chosen from an exhaustive Gosper enumeration of all C(26,12) weight-12 words, because C(26,12)·213 is within the program's 4e9 limit. The unordered_set is used only for membership tests, so its iteration order does not matter. Elapsed CPU time is read only to decide whether to stop. The program re-verifies penalty 0 from scratch before it writes the output. The replay therefore depends only on the published seed code, the recorded random seed and the recorded settings.
- The program reported `padlib size 2 minpen 2 base 213`. So no weight-12 word can be added to the 213-word seed without a conflict, and the 214th word comes from the search moves, not from a trivial extension.

I also ran an independent replay. I converted the seed with my own script (seedrows.py, not seed_to_rows.py), compiled cwbst.cpp myself, and ran `cwbst 26 12 10 214 1005 3600 ... 5 15 1000000`. Result: `RESULT FOUND pen 0 steps 10436323 restarts 10 cpu 24.4`. The output and the object without its first line have the same sha256, 77dd61ee3b01e2f8f5d10faf5861ae0f014adf39153612e5a9c85b9bb9074074, and `cmp` reports them identical.

## 4. Seed code

I fetched https://aeb.win.tue.nl/codes/cwc/d10/a26.10.12.213H once with curl (rebuild.sh made its own separate fetch). HTTP 200, Date Fri, 27 Nov 2026 18:55:13 GMT, Last-Modified Mon, 09 Nov 2026 17:25:20 GMT, Content-Length 1713. Its sha256 is 662ef208b5b79c7dd842e717caf9fa298cb1f217b9bdcbad433a0cfc363199d4, which equals SEED_SHA in how-we-built-it/rebuild.sh.

The file is in `$BASE=16` format with 213 words. My checker says the seed itself is a valid A(26,10,12) code: 213 distinct words, all of weight 12, minimum distance 10. Of the object's 214 words, 178 also appear in the seed code, so 36 words are new or moved.

## Problems found

None that affect this role. One informational point: HOW_WE_FOUND_IT.md (marked unverified contributor text) says the first pass used seeds 1001 to 1020, but it accounts for only 9 runs at 214 words (1 success and 8 others). This does not affect the object or the rebuild.

Out of scope for this role: comparison with arXiv:2608.13906, arXiv:2607.19550 and newer arXiv papers belongs to the other reviewers.

## Reasoning

The object is exactly what README.md says. It is 214 distinct weight-12 words of length 26 with minimum distance 10, sha256 c78abc24... I checked this exhaustively with my own code. Today's table, unchanged since the claimant's fetch, shows 213-691 for the cell, and 213 < 214 <= 691. The published rebuild ends in PASS on a different compiler and architecture than the original, with the recorded step count. My own replay, using my own seed conversion, reproduces the object byte for byte. It depends only on the hash-checked public seed code and the recorded seed and settings.

pass: true
