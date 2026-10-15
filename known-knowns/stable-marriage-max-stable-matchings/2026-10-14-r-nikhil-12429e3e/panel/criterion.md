# Criterion skeptic (V3R1T4S panel): "order-18 instance with exactly 530528 stable matchings"

context: subagent (Claude Code Agent tool, fresh context, sees only claim/)

Inputs: only the claim folder (CLAIM.md, REPRODUCE.md, instance_n18.prefs, smcount3.c, count_stable.py, A357271.txt,
a357271_1.txt). Every path below is relative to that folder. All programs ran on a byte-identical copy of it (`diff -r`: identical;
sha256 values in R5). The claim folder was not modified. One CPU thread; `nice -n 15` on the longer runs. Programs marked
"skeptic scratch" were written by this skeptic and are not part of the claim. Process note: while checking where to write this
file, the file names in the panel folder were listed once. None of those files was opened, and nothing outside claim/ informed
this verdict.

## 1. The criterion, word by word

CLAIM.md quotes this as verbatim from the research charter. The charter itself was not visible to this skeptic, so the quotation could not be checked against it.

> for an n whose maximum is not known, give a stable-marriage instance (complete strict preference lists for n men and n
> women) with strictly more stable matchings than the best known instance of size n. Cells in order: n = 13 (beat 7,123),
> n = 15 (beat 27,059), n = 14 (beat 20,176; no search has touched it), and n = 7 (beat 81) as a cheap calibration cell.
> Do not aim at n = 6, 8, 10, 12 or 16, which are conjectured exact. Shape: record (explicit preference lists; stable
> matchings counted exactly by your own enumerator: closed subsets of the rotation poset, or exhaustive enumeration,
> cross-checked).

Requirements:
- R1 "for an n whose maximum is not known": the maximum for the chosen order must not be known.
- R2 "Do not aim at n = 6, 8, 10, 12 or 16": these orders are excluded.
- R3 Which n are admitted. The success condition is the opening clause, which ranges over n ("an n"). "Cells in order: ..." ranks four
  cells and gives their bars (13, 15, 14, then 7 "as a cheap calibration cell"). It says "in order", not "only", and the separate
  exclusion sentence (R2) would be pointless if the four cells were the only ones allowed. Literal decision: any n that meets R1 and is
  not in R2 is admitted. n = 18 is admitted by the opening clause. It is NOT one of the four named cells, so it can pass only under
  the full criterion (the opening clause), not as a named cell. The criterion lists no partial wins.
- R4 "a stable-marriage instance (complete strict preference lists for n men and n women)": n men and n women, complete lists, strict lists.
- R5 "strictly more stable matchings than the best known instance of size n": the count must exceed the bar. The bar comes from the
  status source: the A357271 data line plus its linked Ong et al. file. The charter's four cell bars come from this same source
  (7,123, 27,059 and 81 from the Ong file; 20,176 from the A357271 data line).
- R6 "explicit preference lists; ... counted exactly by your own enumerator: closed subsets of the rotation poset, or exhaustive
  enumeration, cross-checked".
- R7 One cell: a single order n is claimed.

## 2. Requirement-by-requirement check

R1 MET. The A357271.txt comments (pasted from the skeptic-scratch file check below) say: exact up to n = 4 (Thurber) and n = 5
(A357269); a(6), a(8), a(10), a(12), a(16) are "conjectured to be exact". Nothing is stated for n = 18. If the count in R6 is
right, a(18) = 456300 cannot be the maximum anyway.

R2 MET. 18 is not in {6, 8, 10, 12, 16}.

R3 MET, through the opening clause only (see the decision above). n = 18 is not a named cell.

R4 MET. Skeptic-scratch parser output (independent of the claim's code):
```
comment_lines: 1
data_rows: 36
row_lengths: [18]
n: 18  rows == 2n: True  every row a permutation of 1..n (complete, strict, no ties/repeats): True
non-integer tokens: 0
sha256(instance_n18.prefs): 12429e3eb7c67d315bddabe7ac71edc070cfbaae1760c67f66b8d2fa1e61b488
```
Both claim counters also reject non-permutation rows: `check_perms` in smcount3.c and the assert in count_stable.py.

R5 MET against the status source. See residual A for the part the package cannot settle.
```
$ shasum -a 256 instance_n18.prefs a357271_1.txt A357271.txt
12429e3eb7c67d315bddabe7ac71edc070cfbaae1760c67f66b8d2fa1e61b488  instance_n18.prefs
95735e185c5435e7cbe4c6753fe4e4ee120321457279f1f3283523654db5cd47  a357271_1.txt
fd27d7c9ede8781f1fac606a633c62938a7bda778fc04f8557f26278a7c95143  A357271.txt
$ grep -E '^%S|^%T|^%U' A357271.txt
%S A357271 1,2,3,10,16,48,71,268,330,1000,1231,6472,6720,20176,25011,195472,
%T A357271 200832,456300,637336,3419680,3506880,11221136,15481956,126112960,
%U A357271 127885440,262860800,384418176,2000043808
```
Skeptic-scratch file check: it concatenates %S/%T/%U, uses the %O offset, extracts the Ong lb lines and block headers, and searches for 530528.
```
offset (%O first index): 1  number_of_terms: 28
a(13) = 6720
a(14) = 20176
a(15) = 25011
a(16) = 195472
a(17) = 200832
a(18) = 456300
a(19) = 637336
530528 > a(18): True  margin: 74228
%C A357271 a(n) is from Appendix C of Thurber's 2002 paper, using the maximum from each row. At the time of publication, the bounds were known to be exact up to n=4. A357269 shows that they are also exact for n=5. This sequence is not to be confused with A069156, also from Thurber's Appendix C, which uses only the first column, making for looser bounds for n > 11. a(6), a(8), a(10), a(12), and a(16) are also conjectured to be exact.
%C A357271 Improved lower bounds for n=7, 9, 11, 13, 15 are shown in linked Ong et al. (2025) file.
lb lines: [('7', '81'), ('9', '365'), ('11', '1690'), ('13', '7123'), ('15', '27059')]
example headers (order, count): [('7', '81'), ('9', '365'), ('11', '1690'), ('13', '7123'), ('15', '27059')]
mentions of other sequences: ['A371810']
'530528' appears in A357271.txt: False | '18' order block in A357271.txt: False
'530528' appears in a357271_1.txt: False | '18' order block in a357271_1.txt: False
```
Results: the 18th term (offset 1) is a(18) = 456300. The hashes match CLAIM.md and REPRODUCE.md. The Ong et al. file improves only
n = 7, 9, 11, 13, 15, and neither status file contains 530528 or any order-18 instance. 530528 - 456300 = 74228 > 0.

R6 MET. All three package methods were run as REPRODUCE.md specifies, plus an independent definition-only exhaustive enumeration (section 3).

R7 MET. One cell, n = 18 (CLAIM.md: "cell: n = 18").

## 3. Counters (pasted output)

Package, C. Compiled with `cc -O2 -o smcount3 smcount3.c -lm` and run in the byte-identical copy. The count is the rotation-poset ideal DP,
cross-checked by the 128-bit lattice walk, which re-checks every visited matching against the definition and exits 3 on failure:
```
$ ./smcount3 count instance_n18.prefs 1
file: instance_n18.prefs
n: 18
rotations: 137
memo_states: 70214
count_poset: 530528
seconds_poset: 0.0300
count_lattice_verified: 530528
seconds_lattice: 0.9939
agree: yes
(exit 0)
$ nice -n 15 ./smcount3 enumerate instance_n18.prefs
count_poset: 530528
enumerated_ideals: 530528
unstable_matchings_found: 0
n: 18
rotations: 137
seconds_enumerate: 0.16
agree: yes
(exit 0)
```
Package, Python. The lattice walk uses a visited set of matchings, asserts each one stable, and asserts that the woman-side extreme matching is reached:
```
$ nice -n 15 python3 -I count_stable.py --prefs instance_n18.prefs
n: 18
lattice_count: 530528  (55.89s)
(exit 0)
```
Skeptic scratch, independent of rotations, lattices and Gale-Shapley. This is backtracking over all perfect matchings (men in order,
each given an untaken woman). A branch is pruned as soon as two assigned pairs form a blocking pair. The pruning is sound because such
a pair blocks every completion, and complete because a stable matching has no blocking pair. Every counted matching is then
re-checked against all 18 x 18 pairs.
```
$ nice -n 15 ./brute instance_n18.prefs
n: 18
brute_count_definition_only: 530528
search_nodes: 22372619
full_recheck_failures: 0
```
Core of the skeptic-scratch counter (C). `asg[m]` is the woman assigned to man m. `mrank` and `wrank` are rank tables (0 = best).
```
static void rec(int m, uint32_t taken) {
    nodes++;
    if (m == n) { if (!full_stable()) recheck_fail++; cnt++; return; }
    for (int p = 0; p < n; p++) {
        int w = mpref[m][p]; if (taken >> w & 1) continue;
        int ok = 1;
        for (int m2 = 0; m2 < m; m2++) {
            int w2 = asg[m2];
            if ((mrank[m][w2] < mrank[m][w] && wrank[w2][m] < wrank[w2][m2]) ||
                (mrank[m2][w] < mrank[m2][w2] && wrank[w][m2] < wrank[w][m])) { ok = 0; break; }
        }
        if (!ok) continue;
        asg[m] = w; wpart[w] = m;
        rec(m + 1, taken | (1u << w));
    }
}
/* full_stable(): no (m, w) with mrank[m][w] < mrank[m][asg[m]] and wrank[w][m] < wrank[w][wpart[w]] */
```
Calibration against published counts. The skeptic scratch converted each Ong et al. ranking table in a357271_1.txt to preference lists.
The definition-only counter ran on orders 7, 9 and 11, and the package's smcount3 `count FILE 1` ran on all five:
```
== order 7 (published: 81)
brute_count_definition_only: 81
full_recheck_failures: 0
count_poset: 81
count_lattice_verified: 81
agree: yes
== order 9 (published: 365)
brute_count_definition_only: 365
full_recheck_failures: 0
count_poset: 365
count_lattice_verified: 365
agree: yes
== order 11 (published: 1690)
brute_count_definition_only: 1690
full_recheck_failures: 0
count_poset: 1690
count_lattice_verified: 1690
agree: yes
== order 13 (published: 7123)
count_poset: 7123
count_lattice_verified: 7123
agree: yes
== order 15 (published: 27059)
count_poset: 27059
count_lattice_verified: 27059
agree: yes
```
Five counts of the claimed object agree at 530528, from three algorithm families: rotation-poset DP, lattice walks and reverse search
(all resting on rotation theory), and definition-only exhaustive enumeration (no theory beyond the definition). This meets "counted
exactly ... cross-checked" both ways the criterion allows.

## 4. Hunt for stretched definitions

- Ties or incomplete lists: none. Each of the 36 rows is a permutation of 1..18 (R4).
- Non-square instance: none. 18 men lists and 18 women lists, 18 entries each.
- Unstable matchings counted: none. Every counter re-checks every counted matching against the definition:
  `unstable_matchings_found: 0`, the lattice walks would exit or assert on failure, and the scratch counter reports `full_recheck_failures: 0`.
- Double counting: none. The lattice walks de-duplicate by matching, the scratch counter counts distinct leaves of an assignment tree,
  and the ideal counts (DP and reverse search) equal both.
- Ranks read as preferences, or men and women swapped: the format is preference lists, best first (CLAIM.md "Files"). Swapping sides
  does not change the count. The skeptic's conversion of the Ong ranking tables to preference lists reproduces 81, 365, 1690, 7123
  and 27059, and with the same conversion the instance is rebuilt exactly (next item).
- Composition that merely re-lists a known value: no. The skeptic scratch rebuilt the lexicographic product O[K2] of the Ong et al.
  order-9 instance (365) with Knuth's order-2 instance (men m1: w1>w2, m2: w2>w1; women w1: m2>m1, w2: m1>m2; the same inner block in
  every cell). The result equals instance_n18.prefs row for row:
  ```
  instance == O9(Ong, 365)[K2] lexicographic product: True
  rebuilt O9[K2] byte-compare with instance (data rows only):
  identical data rows
  ```
  Its exact count, 530528, appears in neither status file and is larger than the listed a(18) = 456300. So this is a new explicit
  order-18 instance with a larger exact count than the table's value, not a re-listing. It is, however, a classical composition applied
  to a published 2025 instance, not the result of a search. The criterion asks only for an instance and does not require search.
  Under the charter's own usage, values obtainable by composing listed instances do not count as "known" until they are listed (see
  the consistency check in section 5).

## 5. Null models

No null or statistical test is needed. The claim is a deterministic integer property of one fixed, hashed object, computed by
exhaustive exact methods and compared with a fixed table value. There is no sampling, estimate or p-value, and no selection effect can
inflate an exact count of a given file. The checks that do apply are calibration and trivial baselines. The calibration is in section 3:
the counters reproduce all five published Ong et al. counts. Trivial constructions from listed values all stay below the bar (skeptic scratch):
```
== block-respecting part only: 365 * 2^9 = 186880
== disjoint unions of status-source instances: 9+9: 133225  7+11: 136890  5+13: 113968  3+15: 81177  2+16: 390944  1+17: 200832
```
Padding up from order 17 gives at most a(17) = 200832. Every baseline is below 456300, so beating the bar depends on the stable
matchings of the product that do not respect blocks, and those are exactly what the counters count.

Consistency check on how the charter uses "best known" (a side observation, not part of this claim). The same doubling applied to the
published order-7 instance gives an order-14 count above the charter's n = 14 bar:
```
== null/consistency: O7(Ong,81)[K2], order 14 (charter's n=14 bar is 20176)
n: 14
brute_count_definition_only: 23744
count_poset: 23744
count_lattice_verified: 23744
agree: yes
```
The charter still lists 20,176 for n = 14. So the charter's operative bars are the listed status-source values, not values derivable by
composing listed instances. That is the reading used in R5.

## 6. Residuals (cannot be settled from the package)

- A. The bar is established only within the status source. a357271_1.txt itself says lb(15) was "previously 25011, or 26424 shown in
  A371810", which names a third OEIS sequence that once held a better-than-A357271 value at n = 15. A371810 is not in the package, so
  it cannot be determined here whether A371810, the Ong et al. poster, or other literature lists an order-18 instance with at least
  530528 stable matchings. CLAIM.md's sentence "so a(18) is the best known value for n = 18" is therefore supported only within A357271
  and its linked file. The confirmed scope below is worded against the fetched a(18), not against "best known" in general. The
  status/novelty check must settle this before any public wording uses "best known".
- B. The criterion text was taken from CLAIM.md's quotation. Its fidelity to the charter could not be checked.
- C. REPRODUCE.md says enumerate takes about 10 s; it took 0.16 s here. Python took 55.89 s against the stated "about 45 s". Machine-dependent timings; no bearing on the result.

## 7. Verdict

Every requirement R1-R7 is literally met, with the bar taken from the designated status source. n = 18 is admitted by the opening
clause, not as a named cell. The object is genuine: an explicit, complete, strict, square instance with an exact count confirmed five
ways, including a definition-only exhaustive enumeration. The win is not subsumed by any value in the status source. It is a composition
of published ingredients rather than a search result, which the criterion does not exclude. Residual A must be settled by the
status/novelty check.

confirmed_scope: The explicit order-18 instance instance_n18.prefs (sha256 12429e3eb7c67d315bddabe7ac71edc070cfbaae1760c67f66b8d2fa1e61b488; 18 men and 18 women, each of its 36 lists a complete strict permutation of 1..18; row for row the lexicographic product of the order-9 instance with 365 stable matchings in a357271_1.txt with Knuth's order-2 instance) has exactly 530528 stable matchings by five agreeing exact counts (the package's rotation-poset DP, its verified C lattice walk, its verified reverse-search enumeration, its Python lattice walk, and this skeptic's definition-only exhaustive backtracking), which is strictly more than a(18) = 456300 in the fetched OEIS A357271 data line, a term that the fetched instance file a357271_1.txt (which improves only n = 7, 9, 11, 13, 15) does not improve.
pass: true
