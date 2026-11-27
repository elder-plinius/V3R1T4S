# REPRODUCE verdict: constant-weight-codes, cell A(29,6,6)
context: fresh reviewer (new subagent context started for the REPRODUCE role only; saw only the claim package and public pages; no access to other reviewers' files)
verdict_utc: 2026-11-27T18:55:51Z

## 1. Independent check of the object

I wrote my own checker from the definition (my scratch folder, mycheck.py, Python 3 standard library, run with `-I`) before opening verify-it-yourself/. It reads every non-`#` line of object/A-29-6-6-1207words.txt, requires exactly 29 characters from {0,1}, converts each to a Python int, asserts popcount == 6, asserts all words are distinct, and computes popcount(x ^ y) for every pair (no sampling).

Output:

```
sha256 1c25d94ca5861e9762b92ce4dc28d493bf2c2d5827466cb73cdf949c73079642
header lines 1 first line starts with #: True
words 1207
pairs 727821 expected 727821
hist 6:74765 8:189907 10:316695 12:146454
min distance 6
OK
```

`shasum -a 256` of the object gives the same hash. Everything matches README.md and RUN_IT_YOURSELF.md: 1207 words, all 727821 pairs checked, the same distance histogram, minimum distance 6. After running my own checker I read verify-it-yourself/check_cw.py. It does the same checks (all pairs, length, alphabet, weight, distinctness, bounds), and I found nothing wrong in it.

## 2. Table cell

One plain curl request to https://aeb.win.tue.nl/codes/Andw.html (headers and body saved in my scratch folder):

- HTTP status: 200
- Date: Fri, 27 Nov 2026 18:53:53 GMT
- Last-Modified: Fri, 27 Nov 2026 00:32:42 GMT
- Content-Length: 130587 (file size 130587 bytes)
- ETag: "1fe1b-6613732bff19f"
- sha256: ad1196547427dbaa0ee7eb1970c445d4d7f4890c39860ebd8433bc9df6ceefad

These are the same Last-Modified, ETag, length and sha256 that the-record-we-beat/RECORD.md records, so the page has not changed since the claimant fetched it.

In section "Bounds on A(n,6,w)" the columns are w = 4..14. Row 29, third column (w = 6), reads:

```
<td><a href="cwc/d6/a29.6.6.1205H">1205</a><sup>Pil</sup>-1459</td>
```

The "Values of A(n,6,6)" subtable gives the same value: `<td>1205<sup>Pil</sup>-1459</td>`. The label Pil reads "research group Pilcraft, email 2026-11-21, with 3 new codes." The mirror cell A(29,6,23) is not printed separately, because the table lists only w up to 14 for n = 29. By complement symmetry A(29,6,23) = A(29,6,6), so the same bounds apply.

Check: 1205 < 1207 <= 1459 holds. The margin is 2, and the size is below the upper bound.

## 3. Rebuild

I copied the package into my scratch folder and ran `nice -n 15 sh how-we-built-it/rebuild.sh` once from the copy. The compiler was Apple clang version 21.0.0 (clang-2100.3.34.2) on arm64, so no -mpopcnt flag was used. The original runs were on Linux x86-64 with g++. Wall time was 2026-11-27T18:54:25Z to 18:55:24Z. Exit status 0. Output:

```
seed sha256 898cb1edd43ef9ebacc3abc6bca16eeb95e04ecdef4ac3c72f7a301d5d589c8f
seed words: 1205
step 1: size 1206, random seed 1001: RESULT FOUND pen 0 steps 3035422 restarts 3 cpu 20.2
step 2: size 1207, random seed 1011: RESULT FOUND pen 0 steps 5010566 restarts 5 cpu 30.4
search output equals the object (without its first line), byte for byte
PASS
```

The step counts (3035422, 5010566) and restart counts match logs/original-runs.tsv and logs/rebuild-run.log exactly. Only the CPU times differ.

What the replay depends on: I read how-we-built-it/cwbst.cpp, seed_to_rows.py, chain.tsv and rebuild.sh.
- Inputs: rebuild.sh downloads only the seed file, rejects it unless its sha256 is 898cb1ed..., and converts it in file order with seed_to_rows.py (hex `$BASE=16` lines become 29-bit rows).
- Randomness: cwbst.cpp uses only std::mt19937, seeded from chain.tsv's random seed. Every random choice goes through `rng() %`, which is fully specified by the standard.
- Padding: the extra word is chosen from a library built by enumerating all C(29,6) = 475020 words in Gosper order. For these parameters the random-sample branch is not taken, because 475020 <= 5e7 and 475020*1205 <= 4e9. The unordered_set is used only for membership tests, so its iteration order cannot matter.
- CPU limit: the 3600 s limit only decides whether a run stops early. It cannot change the path a run takes.
- Chaining: step 2 starts from step 1's output, and the tabu settings are those listed in chain.tsv.

Identical step counts across two compilers and two architectures confirm that the result does not depend on the machine.

Honesty of the comparison: rebuild.sh requires each step's RESULT line to start with `RESULT FOUND pen 0 steps` followed by the recorded step count. It then runs `grep -v '^#' object/A-29-6-6-1207words.txt | cmp -s - "$prev"`, where `$prev` is the last step's output file. That compares the object without its single `#` comment line, byte for byte, against freshly computed output, and the object file is never written. The program also re-checks the penalty from scratch before writing (check_penalty). I found no shortcut, cached file or hard-coded output.

## 4. Seed code

One plain curl request to https://aeb.win.tue.nl/codes/cwc/d6/a29.6.6.1205H (the URL named in README.md):

- HTTP status: 200
- Date: Fri, 27 Nov 2026 18:55:35 GMT
- Last-Modified: Sat, 21 Nov 2026 18:18:37 GMT
- Content-Length: 10854
- sha256: 898cb1edd43ef9ebacc3abc6bca16eeb95e04ecdef4ac3c72f7a301d5d589c8f, the same as SEED_SHA in how-we-built-it/rebuild.sh

My script (my scratch folder, overlap.py) decodes the seed file the same way the rebuild does. The seed has 1205 distinct words, all of length 29 and weight 6, with minimum distance 6. Of the object's 1207 words, 1155 are also in the seed code, compared as the same 0/1 strings in the same orientation that the rebuild uses. The other 52 words are new or moved. So the object is a local modification of the hosted 1205-word code that adds 2 words, which is what README.md says.

## Problems found

None.

The arXiv comparisons (arXiv:2608.13906, arXiv:2607.19550, newer papers) that the success criterion also requires are outside the REPRODUCE role and were not checked here.

## Reasoning

- The object is what the claim says: sha256, size, weight, distinctness and every pairwise distance are verified by my own checker.
- It beats the lower bound of the current table cell (1205) and stays within the upper bound (1459). The page has not changed since the claimant's fetch.
- It can be rebuilt from the published seed code with the recorded seeds and settings, on a different compiler and architecture. The rebuild ends in PASS with identical step counts and a byte-for-byte match.

pass: true
