# REPRODUCE skeptic verdict
context: subagent (Claude Code Agent tool, opus, fresh context, saw only claim/)
verdict time (date -u): 2026-11-09T13:34:01Z
injection_suspected: none

## What was checked

Claim: object/union_free_n8_80.txt is a union-free family of 80 distinct nonempty subsets of {1..8} (2 of size 2, 15 of size 3, 63 of size 4).

Files seen (sha256):
- object/union_free_n8_80.txt `8daadc5f6c94a0b0e2364d01cfb9db7931fff7e815d182b329dc4b5cd3293560` (81 lines: 1 comment line plus 80 members)
- tools/check_union_free.py `63da411fea3dbfb49e23a08b1b6799ea7482123c7dd3ad71e9d25f4b9d420f58` (read only after my own checks were done)
- CLAIM.md `5e8ddd10...`, REPRODUCE.md `e479708f...`, table/status_record.md

Python 3.14.8, standard library only, every script run with `python3 -I`. I wrote my checker (mychk.py, sha256 `7677703c...`) in my scratch folder, outside claim/, before opening tools/. I ran all commands from the folder that contains claim/, which is why the paths in the commands below begin with `claim/`.

## Definition used

Quoted from the success criterion in CLAIM.md: "no member S equals the union of the other members contained in S". OEIS A347025 phrases it as "no member is the union of other members", with members distinct and nonempty. The two say the same thing. If some subcollection C of other members has union S, every member of C lies inside S, so the union of all other members inside S is S. In the other direction, the members inside S are themselves such a subcollection. A union of one other member equal to S would be a duplicate, which distinctness rules out. The empty subcollection gives the empty set, which never equals a nonempty S. The DATA value a(0) = 0 confirms that the empty set is not allowed as a member.

I implemented the definition in two ways that work differently from the REPRODUCE.md hint, which takes the union of all proper subsets of S:
- **Method A (per element):** S passes iff some element e of S is contained in no other member T with T a subset of S.
- **Method B (literal, no subset lemma):** S fails iff S is in the set of unions of all nonempty subcollections of the other members. That set is built by closure over all other members, including those not inside S. It can hold at most 2^n masks, so it is exact and fast.

The parser is strict. The first line must be a `#` comment. After that, every line must be nonblank and use single spaces, every token must be a canonical decimal integer in 1..n, no element may repeat within a line, members are compared as sets (order-insensitive), and members must be nonempty.

## 1. Calibration by exhaustive search

`systemd-run --user --scope -q -p CPUQuota=100% nice -n 10 python3 -I mychk.py calib` (brute force over every family of nonempty subsets, with Methods A and B run on every family):
```
n=1: families=2 disagreements(A vs B)=0 max=1 witness=[[1]]
n=2: families=8 disagreements(A vs B)=0 max=2 witness=[[1], [2]]
n=3: families=128 disagreements(A vs B)=0 max=4 witness=[[2], [1, 2], [3], [1, 3]]
n=4: families=32768 disagreements(A vs B)=0 max=7 witness=[[1, 2], [3], [1, 3], [2, 3], [4], [1, 4], [2, 4]]
real 0m0.808s
```
Number of union-free families, which shows the test rejects non-trivially: n=2 7 of 8, n=3 61 of 128, n=4 2480 of 32768 (30288 rejected). Methods A and B agree on all 32768 families at n=4.

a(5) comes from a complete branch-and-bound search (`python3 -I mychk.py search N`). Union-freeness is hereditary, because removing members cannot create a union. The search considers candidates in nondecreasing size order. When it reaches T, every proper subset of T has already been decided, and no chosen member can be a proper superset of T. So T is admissible iff the union of the chosen proper subsets of T is not T. The search prunes only when the number chosen plus the number of undecided candidates that are still admissible is at most the best size found so far. This bound is valid because admissibility can only shrink along a branch. I validated the search engine against the brute force above in two ways:
- With pruning turned off, it enumerates exactly 2, 7, 61 and 2480 union-free families for n = 1..4, the same counts the brute force gives.
- With pruning on, it returns a(1..4) = 1, 2, 4, 7.

`systemd-run --user --scope -q -p CPUQuota=100% nice -n 10 python3 -I mychk.py search 5`:
```
a(5) = 13 (exhaustive branch-and-bound, nodes=59640, 0.2s)
witness: [[1], [2], [1, 3], [2, 3], [1, 4], [2, 4], [3, 4], [1, 2, 5], [1, 3, 5], [2, 3, 5], [1, 4, 5], [2, 4, 5], [3, 4, 5]]
witness re-check: A bad=[] B bad=[] distinct=True
```
This reproduces a(1..5) = 1, 2, 4, 7, 13, matching the DATA recorded in table/status_record.md. A further try at a(6) with the same search was stopped by a 240 s timeout (exit 143, no result) and is not used as evidence.

## 2. Full check of the claimed family

`python3 -I mychk.py file claim/object/union_free_n8_80.txt 8 80`:
```
members read: 80
distinct as sets: 80
empty members: 0
members by size: {2: 2, 3: 15, 4: 63}
Method A: members checked=80, members that are unions of other members inside them=0 []
Method B: members checked=80, members equal to a union of a nonempty subcollection of other members=0 []
RESULT: OK
```
A second run gave byte-identical output (`cmp` reported no difference). The parser reported no errors: every token lies in 1..8, no element repeats within a line, there are no CR characters, and the file is pure ASCII.

The check by hand is short. No singletons are present, so neither 2-set ({2,4}, {5,6}) contains another member. These two 2-sets are disjoint, so a 3-set contains at most one of them, and one 2-set cannot cover three elements. For the 4-sets, I printed for each of the 63 the elements left uncovered by the members inside it, and every list was nonempty. Example: [1, 2, 3, 4] has [2,4] and [1,2,4] inside it, and 3 is uncovered. The 7 four-element subsets missing from the family are [1,2,4,5], [1,2,4,6], [1,2,5,6], [1,4,5,6], [2,4,5,6], [2,4,7,8] and [3,5,6,7]. Each of them is exactly the union of the family members inside it, which is why they were left out (70 − 7 = 63). The value claimed, 80, is above the bar of 79 recorded in table/status_record.md and below Loo's bound of 89 quoted in CLAIM.md.

## 3. Mutation tests of my checker, to show it can fail

Mutants live in my scratch folder: (a) adds `1 2 4 5`, which equals {1,2,4} ∪ {1,2,5}; (b) adds `4 2`, a reordered duplicate; (c) adds `1 2 9`; (d) deletes the last line, leaving 79 members; (e) adds `1 3 5 6`, a duplicate; (f) turns `1 2 3 7` into `1 2 3 7 1`; (g) adds `1 2 4 5 6`, a union.
My checker gives `RESULT: FAIL` on all 7 mutants, each with the expected reason: the union condition was violated at the added member for (a) and (g), duplicate members for (b) and (e), an element outside 1..8 for (c), count 79 != claimed 80 for (d), and a repeated element for (f).

## 4. The author's tool, run only after the steps above

I read tools/check_union_free.py. It uses only the standard library. Its definition is the one quoted above: for every S, the union of all members that are proper subsets of S must not be S. It calibrates by brute force on n = 1..4, and its PASS depends on the calibration, on membership in {1..N}, on distinctness, on the union condition and on len >= MIN_SIZE. Nothing is hardcoded and no hash is involved.

`python3 -I claim/tools/check_union_free.py claim/object/union_free_n8_80.txt 8 80`:
```
calibration a(1..4) by brute force: [1, 2, 4, 7] (expected [1, 2, 4, 7])
members 80 (distinct True, nonempty subsets of {1..8}: True), union-free: True
size profile: {2: 2, 3: 15, 4: 63}
PASS
real 0m0.071s
```
A second run gave byte-identical output. Every count matches mine.

On the same mutants the author's tool prints FAIL for (a), (b), (c), (d), (e) and (g), but PASS for (f). Its parser builds each member with frozenset, so a repeated element within a line is silently dropped. This leniency in the tool does not affect the claim: my strict parser confirms that the claimed file has no repeated elements and that every token is canonical.

## Scope note

I compared the value 80 only against the OEIS values recorded in table/status_record.md: bar 79, DATA a(0..7) = 0, 1, 2, 4, 7, 13, 24, 44. I did not re-fetch OEIS or check the literature. That status question is outside a reproduction check.

## Verdict

Both of my independent methods and the author's tool agree on every count. The claimed file holds 80 distinct nonempty subsets of {1..8}, with 2/15/63 members of sizes 2/3/4, and none of them is the union of other members. My checker reproduces a(1..5) = 1, 2, 4, 7, 13 by exhaustive search, rejects every mutant, and gives deterministic output over repeated runs. I found no mismatch, no missing object and no non-determinism. The only issue found is that the author's parser tolerates repeated elements within a line, which does not matter for this file.

pass: true
