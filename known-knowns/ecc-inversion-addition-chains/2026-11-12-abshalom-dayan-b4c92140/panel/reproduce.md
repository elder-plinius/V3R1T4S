# Reproduce skeptic report: secp256k1 scalar inversion, addition chain of length 281

context: subagent (fresh context, own copy of claim/)
role: REPRODUCE skeptic of a three-skeptic panel; default was to fail unless the claim could be confirmed from the saved files.
date: 2026-11-12; machine: macOS arm64, Python 3.14.7, Apple clang 21.0.0; no network used.

## The claim checked

claim/object/chain.txt is an addition chain of length 281 (251 doublings and 30 other additions) for E = N - 2, N the secp256k1 group order, strictly shorter than 290 (Brian Smith's page), 293 / 290 (addchain doc/results.md) and 282 (the chain on additionchains.com credited to Brian Smith 2026), and it was found by a search seeded from the dictionary of that 282 chain.

## The definition I worked from (quoted from the criterion in claim/CLAIM.md)

> an explicit addition chain 1 = a_0, a_1, ..., a_L = E [...] in which every a_i (i >= 1) equals a_j + a_k for some j, k < i (j = k is a doubling), checked with exact integer arithmetic, and whose length L is STRICTLY LESS (direction: min) than the best of: Brian Smith's live page, addchain's live doc/results.md, and any shorter chain for the same exponent published elsewhere

## Order of work

1. Read claim/CLAIM.md only.
2. Wrote my own checker my_check.py (Python integers only, nothing imported from claim/) before opening anything under claim/checkers/ or claim/rebuild/. sha256 of my_check.py: 5623235c0600557481777a46e8367278912385eb3b91ef07224389701e51ff27.
3. Ran it twice; the two outputs are byte-identical.
4. Only then read and ran the author's scripts.

## Results of my own checker (my_check.py)

N: typed from my own knowledge of SEC 2 v2.0 section 2.4.1 as FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFE BAAEDCE6 AF48A03B BFD25E8C D0364141.

| check | result |
|---|---|
| N has 256 bits and passes Miller-Rabin (12 fixed + 64 random bases), so x^(N-2) is the inverse of x mod N | ok |
| claim/table/results.md, section "secp256k1 (Bitcoin) Scalar Inversion": N equals my N, d = 2, N-d = fffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd036413f equals my N - 2 | ok |
| same section prints Length 293, Best Known 290 | ok |
| sha256 of claim/object/chain.txt = b4c92140602faf399a6aad09073210f46b902351a6b7db3bfa1c848e06d4ce9b, as in claim/CLAIM.md | ok |
| format: two header lines, then lines of exactly two decimal indices; header hex equals my N - 2 | ok |
| every element t = 1..L is a[i] + a[j] with i, j < t (strictly earlier) | ok, all 281 steps |
| a_0 = 1; last element equals N - 2 exactly (as an integer, not only mod N) | ok |
| length L | 281 |
| doublings (i = j) / other additions | 251 / 30 |
| value-level recount, ignoring the written indices: each value is a sum of two earlier values; values that are twice an earlier value | ok; 251 |
| 282 distinct values, strictly increasing, no dead step (every non-final element is used later) | ok |
| x * x^E = 1 mod N, x^E computed by following the chain with modular products, and equal to pow(x, -1, N) | ok for 300 values of x (2, 3, 5, 7, N-1, N-2, (N+1)/2 and 293 random), 0 failures |

## The published 282 chain, replayed with my own code

claim/table/secp256k1-scalar-inverse-example.txt (sha256 ff57a8519d4fdc4ee5c154390d30ca83824c14cdfddb1907b9f736c30a050ccf, 283 values, CRLF line ends):

- starts at 1; every later value is the sum of two earlier values; no repeated value: valid chain.
- last value equals my N - 2: same exponent.
- length 282 = 251 doublings + 31 other additions.
- Ours, 281, is strictly shorter than 282 (by exactly 1), and than 290 and 293.

## The other bars, from the saved fetches (no network)

- sha256 of all five files in claim/table/ equal the hashes in claim/table/RECORD.md and claim/table/FETCHES.txt (smith.html 7b688992..., results.md c805367c..., LargeChains.html 55d0846d..., secp256k1-scalar-inverse-example.txt ff57a851..., tt_secp256k1_288.json 4f8fc44a...).
- claim/table/smith.html: the secp256k1 scalar section ends with "Total length: 290 = 253 doubles + 37 adds".
- claim/table/LargeChains.html: the row "secp256k1 scalar inversion 282 ... 251 + 31 ... Brian Smith (2026)".
- claim/table/tt_secp256k1_288.json: replayed with my code, 288 steps, valid, ends at N - 2, 253 doublings.
- Lowest value in the saved files: 282. I could not re-check that nothing shorter is published elsewhere (that needs the network and is outside this role); I only confirm what the saved files say.

## The author's commands (claim/REPRODUCE.md)

| command | expected | observed |
|---|---|---|
| sh checkers/run_checks.sh | "length 281 = 251 doublings + 30 additions", then "CHECK: PASS", then "PASS" | exactly these lines, exit 0; run twice, outputs byte-identical |
| python3 checkers/check_values.py table/secp256k1-scalar-inverse-example.txt | "values 283, length 282", "all steps valid: True", "ends at target n-2: True" | "values 283, length 282, steps that can be doublings 251, distinct True"; "all steps valid: True"; "ends at target n-2: True" |
| python3 rebuild/build_wide.py 2 "<30 values>" rebuilt.txt 3000, then cmp with object/chain.txt | identical, about a minute | "secp256k1 scalar: chain length 281 (doublings 251, additions 30); DP predicted 281; checks PASS"; cmp says identical; 37 s. Repeated with another PYTHONHASHSEED: identical again. sha256 of both rebuilds b4c92140602faf399a6aad09073210f46b902351a6b7db3bfa1c848e06d4ce9b |
| optional: cc -O2 -o acw_big acw_big.c, then python3 trivial_edits.py 2 22 seed_dictionary.txt 2048 one_edit_again.txt (4 workers) | histogram "282:11 283:183 284:150 285:3 308:1 309:37 310:229 311:49" | same histogram, all 663 candidates scored (a full redo, not a sample); 17 s here, not the "about 5 minutes" stated. The new file differs from claim/baseline/one_edit.txt in the first header line only (see mismatch 1) |

No non-determinism seen in any of the checker, replay, rebuild or baseline runs. All four commands of claim/REPRODUCE.md match what it says.

## Composition and seed statement, checked from files (my_dict_check.py)

| stated fact | result |
|---|---|
| claim/rebuild/search_init.txt holds 27 values | ok, 27 distinct; claim/baseline/seed_dictionary.txt is byte-identical (sha256 f93a991a...) |
| the seed is the 27 values below 2^21 of the published 282 chain | ok, exactly equal |
| final dictionary has 30 values | ok; the list in the REPRODUCE.md command equals the last line of claim/rebuild/search_out.txt ("281 30 252") and equals the 30 values below 2^21 of claim/object/chain.txt |
| 24 in common with the seed | ok |
| dropped: 139552, 419427, 1398106 | ok |
| added: 289, 70033, 559236, 699062, 1258297, 1817533 | ok |
| top ladder: runs of 21, 42, 84 and 126 ones, as in the seed chain | ok: 2^21-1, 2^42-1, 2^84-1, 2^126-1 occur in both chains and are the only all-ones values above 1 in either; above 2^21 the two chains share their first 128 values (up to 146 bits) and then differ; 173 values in common in total |
| ours 251 doublings + 30 additions, the seed chain 251 + 31 | ok |
| claim/baseline/one_edit.txt: seed plus 662 one-edit neighbours, none below 282 | ok: header says 663 candidates, histogram sums to 663, lowest key 282, 11 rows at 282 (the base and 10 edits). My own count of the neighbourhood: 1 deletion + 340 insertions + 321 replacements + base = 663 |
| not glued from published chains | consistent: the object is a single chain rebuilt by the author's dynamic program from the 30-value dictionary; I found no evidence of concatenation |

## Mismatches and caveats (none changes the verdict)

1. claim/baseline/one_edit.txt, first header line, names the dictionary file as "smith2/init2.txt"; the redo with the packaged file writes "seed_dictionary.txt". Every other byte is equal. A stale path in a saved output; the numbers are the same.
2. Stale folder names in comments: claim/checkers/run_checks.sh says "sh verify-it-yourself/run_checks.sh"; claim/checkers/check_chain.py refers to "the-record-we-beat/RECORD.md". The commands in claim/REPRODUCE.md work as written.
3. The baseline redo took 17 s on 4 cores, not about 5 minutes. Harmless.
4. The one-edit baseline is scored by a beam-limited dynamic program (beam 2048). "Nothing below 282" is a statement about that evaluator on those 663 dictionaries; it is not a lower bound, and the claim does not present it as one.
5. The search trace in claim/rebuild/search.log was NOT reproduced; this is the one open point. The search is not among the commands of claim/REPRODUCE.md and the package does not record its command line (temperatures T0 and T1, the cycle length CYC). As an extra I compiled claim/rebuild/acw.c (cc -O2) and ran it from claim/rebuild/search_init.txt with the logged seed 1009, width 21, beam 256 and the program's default settings (T0 0.9, T1 0.15, CYC 200000), one process:
   - The first log line is reproduced exactly: "curve 2 L=256 Jb=129 BW=21 KB=256 init cost 284 (dict 26, main 258) states 38675".
   - A 420 s run ended at iteration 22400 and a 780 s run at iteration 41792, both with best still 284. The saved log reports "it 30065 best 283 (dict 29)". So with the default settings the logged path does not occur. Reaching the logged end (iteration 841216) would take about 4.4 hours at the speed seen here (about 53 iterations per second), so the full run was not attempted.
   - The program's path is deterministic for fixed settings (two 40 s runs of a quick setup ended with identical iteration, evaluation and state counts), so the difference is not randomness: the logged run used settings other than the defaults, or another build. Only the stopping point depends on the wall clock.
   - What does hold: each of the four dictionaries in claim/rebuild/search_out.txt, scored from scratch by the packaged program (EVAL=1, beam 256), gives exactly the logged totals and main-line costs: 284 (26 + 258), 283 (29 + 254), 282 (29 + 253), 281 (29 + 252). So the saved improvements are consistent with the packaged evaluator, the start is the seed, and the last dictionary rebuilds the object byte for byte.
   - Suggested fix before filing: add the exact command line and environment of the logged search run to claim/REPRODUCE.md, or say there that the trace is a record and is not expected to replay.
   I did not count this as a failure of the claim: no stated command or expected output is contradicted, and the object, its value and the seed relation are confirmed independently of the search path. The sentence "It was found by a search that started from the dictionary of that published 282 chain" is supported by the files as described above, but the path of the search itself is unverified.
6. The margin is the smallest possible: 281 against 282.
7. That no shorter chain is published anywhere else rests on claim/table/COMPARATORS.md; not checkable in this role.

## Verdict

Every property of the object and the claimed value were confirmed with my own checker from the definition, the published 282 chain was replayed and is a valid chain of length 282 for the same exponent, the author's commands give the stated outputs, the rebuild from the dictionary is byte-identical twice, and every file-checkable fact of the seed statement holds. Open point, not blocking: the saved search trace did not replay under the program's default settings (caveat 5); the package should record the search command line.

pass: true
