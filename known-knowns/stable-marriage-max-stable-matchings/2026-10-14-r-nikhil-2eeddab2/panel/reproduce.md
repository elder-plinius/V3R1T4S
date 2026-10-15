# REPRODUCE skeptic: verdict on the n = 14 claim (24992 stable matchings)

context: subagent (Claude Code Agent tool, fresh context, sees only claim/)

Scope and order of work. I read claim/CLAIM.md, then claim/REPRODUCE.md, then the data files claim/instance_n14.prefs,
claim/a357271_1.txt and claim/A357271.txt. I wrote and ran my own parsers and two counters (below) and got my n = 14
result before opening the author's code. After that I only skimmed claim/count_stable.py and claim/smcount3.c for
safety (imports and file writes; the C file writes files only in its `climb`/`anneal` modes, which REPRODUCE.md does
not use) and ran the commands in claim/REPRODUCE.md. Everything ran in a scratch copy of claim/, one process at a time
(1 CPU thread), under `nice`. The claim folder was not modified. The session was paused once for usage limits and then
resumed; the saved n = 14 match lists had the same sha256 after the resume.
No web access was used.

## Definition (quoted verbatim from claim/CLAIM.md)

> Stable marriage instance of order n: n men and n women, each with a complete strict preference list over the other
> side. A matching (bijection men -> women) is stable iff there is no blocking pair (m, w): m prefers w to his partner
> and w prefers m to her partner (Gusfield & Irving, The Stable Marriage Problem, MIT Press 1989, Sec. 1.1). The
> quantity is the number of stable matchings of the instance.

## My own checker (from the definition only; written before reading any author code)

I wrote two separate implementations. Both are exhaustive (no sampling) and use only the definition. Neither uses
rotations, Gale-Shapley or lattice theory.

1. `sm_count.c` (C, men-major, rank tables). It backtracks over all perfect matchings: men 1..n in turn each take an
   unused woman. Optional pruning (flag): a partial assignment is rejected once two assigned couples (j, wj) and (m, w)
   contain a blocking pair. That is (m, wj) where m prefers wj to w and wj prefers m to j, or (j, w) where j prefers
   w to wj and w prefers j to m. Every complete matching the search reaches is re-checked against the definition over
   all n*n (man, woman) pairs, and is counted only if that full check passes. It can also write out every stable
   matching it finds.
2. `sm_count2.py` (Python, women-major). It reads the raw preference lists directly, with "prefers" meaning an earlier
   position in the list. It searches in the opposite order: women 1..n in turn each take an unused man. It uses the
   same pairwise pruning and the same full re-check over all n*n pairs. It also asserts that each complete matching is
   a bijection, and it writes out every stable matching it finds.

My own parsers. `parse_prefs.py` reads the .prefs format described in claim/CLAIM.md: '#' comment lines, then 2n
lines (n men's lists of women, then n women's lists of men, most preferred first). It checks every property and
writes rank tables. `parse_oeis.py` reads claim/a357271_1.txt using the format the file itself states: 'the "1,5" in
row 3, column 4 means that Man 3 ranks Woman 4 as his 1st choice, and she ranks him as her 5th choice'. So each row is
a man, each column is a woman, and each entry is (man's rank of the woman, woman's rank of the man). The parser also
reads the file's MiniZinc arrays rankWomen[w][m] and rankMen[m][w] and checks that they are identical to the tables.

Why the pruned search is still exhaustive and exact (my own derivation). A blocking pair (m, w) of a complete
matching M involves two couples, (m, M(m)) and (M^-1(w), w). When the later of the two couples is fixed, the
pairwise test evaluates exactly the blocking condition for (m, w). So a partial assignment is rejected only when its
fixed couples already contain a blocking pair. No completion changes those agents' partners or preferences, so every
completion is unstable, and pruning loses no stable matching. In the other direction, a complete matching that passes
every pairwise test has no blocking pair. The independent full re-check confirms this: `rejected_by_full_check=0` in
every pruned run below. Test 3 also checks the pruning empirically against unpruned enumeration of all n! matchings.

The core of `sm_count.c`, verbatim (mr[m][w] is the rank 1..n that man m gives woman w; wr[w][m] is the rank woman w
gives man m; smaller means preferred):

```
static int full_check(void) {           /* 1 iff the complete matching has no blocking pair */
  for (int m = 0; m < n; m++)
    for (int w = 0; w < n; w++) {
      if (w == wife[m]) continue;
      int pm = wife[m], pw = husband[w];
      if (mr[m][w] < mr[m][pm] && wr[w][m] < wr[w][pw]) return 0;
    }
  return 1;
}
...
    if (prune) {
      int bad = 0;
      for (int j = 0; j < m && !bad; j++) {
        int wj = wife[j];
        if (mr[m][wj] < mr[m][w] && wr[wj][m] < wr[wj][j]) bad = 1;      /* (m, wj) blocks */
        else if (mr[j][w] < mr[j][wj] && wr[w][j] < wr[w][m]) bad = 1;   /* (j, w) blocks  */
      }
      if (bad) continue;
    }
```

### Test 1: tiny instances checked by hand

- t2, Knuth n=2 (m1: w1 w2; m2: w2 w1; w1: m2 m1; w2: m1 m2). By hand, both matchings are stable: one gives every man
  his first choice, the other gives every woman hers. Expected 2.
- t3, cyclic n=3 (m1: 1 2 3; m2: 2 3 1; m3: 3 1 2; w1: 2 3 1; w2: 3 1 2; w3: 1 2 3). By hand there are exactly 3
  stable matchings, with wives of (m1, m2, m3) = (1 2 3), (2 3 1), (3 1 2). Each of the other 3 permutations has a
  blocking pair, e.g. (m3, w1) blocks (1 3 2). Expected 3.
- t3id, n=3 where everyone ranks 1 2 3. By hand only (1 2 3) is stable. Expected 1.

C counter, unpruned (prune=0) and pruned (prune=1), each followed by the list of stable matchings (wife of man 1..n):
```
== t2 prune=0
n=2 prune=0 nodes=5 complete_matchings_checked=2 stable=2 rejected_by_full_check=0
1 2
2 1
== t2 prune=1
n=2 prune=1 nodes=5 complete_matchings_checked=2 stable=2 rejected_by_full_check=0
1 2
2 1
== t3 prune=0
n=3 prune=0 nodes=16 complete_matchings_checked=6 stable=3 rejected_by_full_check=3
1 2 3
2 3 1
3 1 2
== t3 prune=1
n=3 prune=1 nodes=12 complete_matchings_checked=3 stable=3 rejected_by_full_check=0
1 2 3
2 3 1
3 1 2
== t3id prune=0
n=3 prune=0 nodes=16 complete_matchings_checked=6 stable=1 rejected_by_full_check=5
1 2 3
== t3id prune=1
n=3 prune=1 nodes=8 complete_matchings_checked=1 stable=1 rejected_by_full_check=0
1 2 3
```
Python counter on t3 (the same 3 matchings, found in women-major order):
```
n=3 complete_matchings_checked=3 stable=3 distinct=3 rejected_by_full_check=0
1 2 3
3 1 2
2 3 1
```
All three results match the hand derivation, including which matchings are stable.

### Test 2: the published instances in claim/a357271_1.txt (expected 81, 365, 1690, 7123, 27059)

My parser's output:
```
header lb(n) values: {7: 81, 9: 365, 11: 1690, 13: 7123, 15: 27059}
order 7: stated count 81; table 7x7 parsed; every man row and woman column is a permutation of 1..7
order 9: stated count 365; table 9x9 parsed; every man row and woman column is a permutation of 1..9
order 11: stated count 1690; table 11x11 parsed; every man row and woman column is a permutation of 1..11
order 13: stated count 7123; table 13x13 parsed; every man row and woman column is a permutation of 1..13
order 15: stated count 27059; table 15x15 parsed; every man row and woman column is a permutation of 1..15
order 7: MiniZinc rankWomen/rankMen arrays identical to the ranking table
order 9: MiniZinc rankWomen/rankMen arrays identical to the ranking table
order 11: MiniZinc rankWomen/rankMen arrays identical to the ranking table
order 13: MiniZinc rankWomen/rankMen arrays identical to the ranking table
order 15: MiniZinc rankWomen/rankMen arrays identical to the ranking table
wrote oeis_n7.rank expected 81
wrote oeis_n9.rank expected 365
wrote oeis_n11.rank expected 1690
wrote oeis_n13.rank expected 7123
wrote oeis_n15.rank expected 27059
```
C counter (pruned):
```
n=7 prune=1 nodes=598 complete_matchings_checked=81 stable=81 rejected_by_full_check=0
real 0.00
n=9 prune=1 nodes=4378 complete_matchings_checked=365 stable=365 rejected_by_full_check=0
real 0.00
n=11 prune=1 nodes=29817 complete_matchings_checked=1690 stable=1690 rejected_by_full_check=0
real 0.00
n=13 prune=1 nodes=184992 complete_matchings_checked=7123 stable=7123 rejected_by_full_check=0
real 0.05
n=15 prune=1 nodes=1100301 complete_matchings_checked=27059 stable=27059 rejected_by_full_check=0
real 0.24
```
Python counter. In each case the sorted list of matchings has the same sha256 as the C counter's list:
```
n=7 complete_matchings_checked=81 stable=81 distinct=81 rejected_by_full_check=0
  n=7: same set as C counter
n=9 complete_matchings_checked=365 stable=365 distinct=365 rejected_by_full_check=0
  n=9: same set as C counter
n=11 complete_matchings_checked=1690 stable=1690 distinct=1690 rejected_by_full_check=0
  n=11: same set as C counter
n=13 complete_matchings_checked=7123 stable=7123 distinct=7123 rejected_by_full_check=0
  n=13: same set as C counter
n=15 complete_matchings_checked=27059 stable=27059 distinct=27059 rejected_by_full_check=0
  n=15: same set as C counter
```
All five published counts are reproduced exactly by both of my counters.

### Test 3: pruning compared with fully unpruned enumeration of all n! matchings

Each block below shows the unpruned C run, then the sha256 of the sorted pruned list, then the sha256 of the sorted
unpruned list:
```
n=7 prune=0 nodes=13700 complete_matchings_checked=5040 stable=81 rejected_by_full_check=4959
real 0.00
6dc9b0cf8390380b55f2e300dd019215fbe4618ee3a083ff6417380f13392e01  -
6dc9b0cf8390380b55f2e300dd019215fbe4618ee3a083ff6417380f13392e01  -
n=9 prune=0 nodes=986410 complete_matchings_checked=362880 stable=365 rejected_by_full_check=362515
real 0.02
5cc8e8a46dbec8027e9676454a0b42cc49c699c200362ddfa97d518c672f0f37  -
5cc8e8a46dbec8027e9676454a0b42cc49c699c200362ddfa97d518c672f0f37  -
n=11 prune=0 nodes=108505112 complete_matchings_checked=39916800 stable=1690 rejected_by_full_check=39915110
real 1.92
90ffff09f5a42702a419c0251d11c49e262c593282290e721978f75291ff1bca  -
90ffff09f5a42702a419c0251d11c49e262c593282290e721978f75291ff1bca  -
```
The unpruned runs checked exactly 7! = 5040, 9! = 362880 and 11! = 39916800 complete matchings, and they produced
exactly the same sets as the pruned runs. I did not run an unpruned enumeration at n = 14 (14! is about 8.7e10
matchings, beyond the time budget). At n = 14, exactness rests on the derivation above, on this test, and on the two
implementations agreeing (below).

## Object properties: claim/instance_n14.prefs (my parser)
```
bytes: 1003  CR present: False  TAB present: False  non-ASCII: False  ends with newline: True
total lines: 29  comment lines: 1  data lines: 28  blank data lines: 0
all 28 lists are permutations of 1..14 (complete, strict): True
wrote n14/n14.rank
```
So it is an order-14 instance: 14 men's lists over women 1..14 and 14 women's lists over men 1..14, every one a
complete strict list. The comment line reads
`# outer=85 inner=knuth2 men_flip=fix women_flip=fix seed=0 lattice_count=24992`.

## My count on claim/instance_n14.prefs

C counter, run twice, each run writing every stable matching found:
```
n=14 prune=1 nodes=428359 complete_matchings_checked=24992 stable=24992 rejected_by_full_check=0
real 0.10
n=14 prune=1 nodes=428359 complete_matchings_checked=24992 stable=24992 rejected_by_full_check=0
real 0.08
   24992 n14/run1.list
   24992 n14/run2.list
   49984 total
555a17369cbca83d4fc49d5a069c4084d406c3c76b30570922888afe974e3f17  n14/run1.list
555a17369cbca83d4fc49d5a069c4084d406c3c76b30570922888afe974e3f17  n14/run2.list
388fd424575f4f0923d291fb984b916ad88e74a53e49582e3b4f1b591786a9e5  -
   24992
run1 and run2 lists byte-identical
```
(The last hash is of the sorted list. `24992` on the line after it is the number of distinct matchings, from `sort -u`.)

Python counter. It reads the raw .prefs file directly rather than my rank file, and searches in women-major order.
Run 1, with the sorted-list hashes of the Python and C outputs:
```
n=14 complete_matchings_checked=24992 stable=24992 distinct=24992 rejected_by_full_check=0
real 3.21
388fd424575f4f0923d291fb984b916ad88e74a53e49582e3b4f1b591786a9e5  -
388fd424575f4f0923d291fb984b916ad88e74a53e49582e3b4f1b591786a9e5  -
Python (raw .prefs, women-major) set == C (rank file, men-major) set
```
Run 2:
```
n=14 complete_matchings_checked=24992 stable=24992 distinct=24992 rejected_by_full_check=0
py run1/run2 lists byte-identical
```
Both of my counters give exactly 24992 stable matchings, and they give the same set of matchings. Each of the 24992
matchings was re-checked against the definition over all 196 (man, woman) pairs; that check rejected none.

## The author's commands from claim/REPRODUCE.md (run in the scratch copy)
```
$ python3 -I count_stable.py --prefs instance_n14.prefs --brute --expect 24992
n: 14
lattice_count: 24992  (0.71s)
brute_count: 24992  (1.62s)
counters_agree: True
expected: 24992 PASS
real 2.46
user 2.41
sys 0.03
exit code: 0
```
```
$ cc -O2 -o smcount3 smcount3.c -lm && ./smcount3 count instance_n14.prefs 1
compile exit: 0
file: instance_n14.prefs
n: 14
rotations: 87
memo_states: 11165
count_poset: 24992
seconds_poset: 0.0015
count_lattice_verified: 24992
seconds_lattice: 0.0094
agree: yes
exit code: 0

$ ./smcount3 enumerate instance_n14.prefs
count_poset: 24992
enumerated_ideals: 24992
unstable_matchings_found: 0
n: 14
rotations: 87
seconds_enumerate: 0.01
agree: yes
exit code: 0
```
Second run of all three (filtered to the result lines):
```
lattice_count: 24992  (0.67s)
brute_count: 24992  (1.54s)
counters_agree: True
expected: 24992 PASS
exit 0
count_poset: 24992
count_lattice_verified: 24992
agree: yes
enumerated_ideals: 24992
unstable_matchings_found: 0
agree: yes
```
Every line REPRODUCE.md says will be printed was printed, with the stated values, in both runs.

## sha256 of the saved files (original claim folder and scratch copy)
```
== sha256 (original claim folder)
2eeddab210507ca8fecf7cb18e88a27245dd861ab7497acfc0d023766cf76965  instance_n14.prefs
95735e185c5435e7cbe4c6753fe4e4ee120321457279f1f3283523654db5cd47  a357271_1.txt
fd27d7c9ede8781f1fac606a633c62938a7bda778fc04f8557f26278a7c95143  A357271.txt
== sha256 (scratch copy)
2eeddab210507ca8fecf7cb18e88a27245dd861ab7497acfc0d023766cf76965  instance_n14.prefs
95735e185c5435e7cbe4c6753fe4e4ee120321457279f1f3283523654db5cd47  a357271_1.txt
fd27d7c9ede8781f1fac606a633c62938a7bda778fc04f8557f26278a7c95143  A357271.txt
```
All three match the values stated in claim/CLAIM.md (object and a357271_1.txt) and claim/REPRODUCE.md (all three).

## The bar (from the saved files)

I parsed the data lines (%S/%T/%U) and the offset (%O) of claim/A357271.txt with a script:
```
== bar from saved A357271.txt
offset 1 a(13)= 6720 a(14)= 20176 a(15)= 25011  24992>a(14): True
== does a357271_1.txt contain an order-14 instance or lb(14)?
no match
```
In the saved entry, a(14) = 20176. The entry's comment says the linked Ong et al. (2025) file improves only
n = 7, 9, 11, 13 and 15. So, as of the saved snapshot (revision #23, May 26 2025), 20176 is the best known lower bound
for n = 14, and 24992 > 20176.

## Determinism

My C counter ran twice and produced byte-identical lists (sha256 555a1736...), with identical counts and node counts.
My Python counter ran twice and produced byte-identical lists. The author's three commands ran twice with identical
results.

## Mismatches and discrepancies

- Numbers: none. Every count, property and hash matches the claim exactly.
- Citation (does not change any number): the `bar:` line of claim/CLAIM.md says the 20176 comes "from Ong, Ang, Ho,
  Eilers, Marks, Buzi (2025): lb(14)=20176, the explicit instance in the file linked from OEIS A357271
  (a357271_1.txt ...)". That is wrong as written. claim/a357271_1.txt contains no order-14 instance and no lb(14); it
  has only orders 7, 9, 11, 13 and 15 (see the grep above). The value 20176 is a(14) in the A357271 data line, which
  the entry attributes to Appendix C of Thurber (2002), built by composing smaller instances. The bar value itself is
  correct; the claim text should be corrected to cite the data line.
- Outside what the saved files can settle: "best known" is checked only against the saved OEIS snapshot. The claim's
  own origin note cites a 2026 order-7 instance with 85 stable matchings, more than the snapshot's lb(7) = 81, so the
  literature has moved past that snapshot. Whether any newer source beats 24992 at n = 14 is a status question for
  another panel member; I did no web check.

## Verdict

- Order 14, 14 + 14 complete strict lists: confirmed.
- Object sha256 2eeddab2...: confirmed.
- Exactly 24992 stable matchings: confirmed by two independent definition-only exhaustive counters of mine, which
  produced the same set. Both were validated on hand-checked instances, on all five published instances and against
  full n! enumeration.
- 24992 > 20176 = a(14) in the saved A357271 entry: confirmed.
- The author's three counters reproduce as stated in REPRODUCE.md.
- All results are deterministic.

The only discrepancy is the mis-citation of the bar's source described above, which does not affect the object, the
count or the comparison.

pass: true
