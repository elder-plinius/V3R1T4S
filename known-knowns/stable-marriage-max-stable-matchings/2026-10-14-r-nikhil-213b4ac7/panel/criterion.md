# CRITERION skeptic verdict: claim "order-22 instance with 12277568 stable matchings"

context: subagent (Claude Code Agent tool, fresh context, sees only claim/)

Read: CLAIM.md, REPRODUCE.md, instance_n22.prefs, A357271.txt, a357271_1.txt, smcount3.c, count_stable.py. Nothing else in
the run folder or workspace was opened. Every run used a byte-identical scratch copy of claim/ (checked with `diff -r`),
one thread, under `nice -n 15`. Paths below are relative to claim/. Disclosure: a process listing I ran to see whether my
counters had finished also showed the command lines of unrelated processes; I opened none of their files and used nothing
from them.

## 0. Integrity (scratch copy; matches the sha256 values stated in CLAIM.md and REPRODUCE.md)
```
213b4ac73bfb4218a4295514410d0d53b6a87f48e8f1462d61382579efdd5b37  instance_n22.prefs
95735e185c5435e7cbe4c6753fe4e4ee120321457279f1f3283523654db5cd47  a357271_1.txt
fd27d7c9ede8781f1fac606a633c62938a7bda778fc04f8557f26278a7c95143  A357271.txt
```

## 1. The criterion, word by word
> for an n whose maximum is not known, give a stable-marriage instance (complete strict preference lists for n men and n
> women) with strictly more stable matchings than the best known instance of size n. Cells in order: n = 13 (beat 7,123),
> n = 15 (beat 27,059), n = 14 (beat 20,176; no search has touched it), and n = 7 (beat 81) as a cheap calibration cell.
> Do not aim at n = 6, 8, 10, 12 or 16, which are conjectured exact. Shape: record (explicit preference lists; stable
> matchings counted exactly by your own enumerator: closed subsets of the rotation poset, or exhaustive enumeration,
> cross-checked).

Requirements I extract:
- R1 (domain) "for an n whose maximum is not known".
- R2 (exclusion) "Do not aim at n = 6, 8, 10, 12 or 16".
- R3 (cells) "Cells in order: 13, 15, 14, 7". This sentence orders named cells and gives their bars. It does not say "only".
  Read literally, the domain is R1 minus R2. If the four cells were the whole domain, R2 would add nothing, because
  6, 8, 10, 12 and 16 are not among them. So n = 22 is admitted by the opening clause. It is not one of the four named
  cells. "for an n" is existential, so one cell (one n) is enough.
- R4 (object) an explicit instance of n men and n women, each person with a complete strict list over the other side.
- R5 (bar) "strictly more stable matchings than the best known instance of size n". No bar is named for n = 22, so it
  comes from the status source. The charter takes its own bars from the same source: 7,123, 27,059 and 81 come from the
  linked Ong et al. file, and 20,176 for n = 14 is the A357271 data-line value.
- R6 (counting) an exact count by the claimant's own enumerator (closed subsets of the rotation poset, or exhaustive
  enumeration), cross-checked.

## 2. Independent parse (my own script, no claimant code imported; output verbatim)
```
[instance] file: instance_n22.prefs
[instance] comment_lines: 1  data_lines: 44  other_blank_lines: 0
[instance] row_lengths: [22]
[instance] n: 22  men_rows: 22  women_rows: 22
[instance] rows_that_are_permutations_of_1..n: 44 of 44
[instance] non-permutation rows: none
[instance] man-optimal (own Gale-Shapley) stable: True  woman-optimal stable: True  distinct: True
[A357271.txt] offset: 1  number_of_terms: 28
[A357271.txt] a(11) = 1231
[A357271.txt] a(14) = 20176
[A357271.txt] a(18) = 456300
[A357271.txt] a(21) = 3506880
[A357271.txt] a(22) = 11221136
[A357271.txt] a(23) = 15481956
[A357271.txt] revision line: %I A357271 #23 May 26 2025 15:56:20
[A357271.txt] improvement comment: %C A357271 Improved lower bounds for n=7, 9, 11, 13, 15 are shown in linked Ong et al. (2025) file.
[compare] claimed 12277568 > a(22) 11221136: True  difference: 1056432  ratio: 1.0941
[a357271_1.txt] paired tables (order, SM): [(7, 81), (9, 365), (11, 1690), (13, 7123), (15, 27059)]
[a357271_1.txt] MiniZinc n = blocks: [7, 9, 11, 13, 15]
[a357271_1.txt] lb(n) lines: [(7, 81), (9, 365), (11, 1690), (13, 7123), (15, 27059)]
[a357271_1.txt] any order-22 table or n = 22 block: False
[a357271_1.txt] lines mentioning other sequences: ['lb(15)=27059 (previously 25011, or 26424 shown in A371810)']
[block 7] stated SM: 81  paired table consistent with MiniZinc block: True
[block 9] stated SM: 365  paired table consistent with MiniZinc block: True
[block 11] stated SM: 1690  paired table consistent with MiniZinc block: True
[O[K2] rebuild] O[K2] of the published order-11 block equals instance_n22.prefs exactly: True
[block 13] stated SM: 7123  paired table consistent with MiniZinc block: True
[block 15] stated SM: 27059  paired table consistent with MiniZinc block: True
```

R1, MET. A357271.txt says: "At the time of publication, the bounds were known to be exact up to n=4. A357269 shows that
they are also exact for n=5. ... a(6), a(8), a(10), a(12), and a(16) are also conjectured to be exact." Nothing in claim/
says the maximum for n = 22 is known.

R2, MET. 22 is not in {6, 8, 10, 12, 16}.

R3, MET. n = 22 is admitted under the opening clause. It is NOT a named priority cell, so this is a win under the
criterion's general clause, not under cell 13, 15, 14 or 7.

R4, MET. There is 1 comment line (ignored by both parsers), then 44 data lines of 22 entries each. All 44 rows are
permutations of 1..22: rows 1-22 are the men's lists and rows 23-44 the women's lists. So there are no ties, no
incomplete lists and no non-square shape. My own Gale-Shapley gives man-optimal and woman-optimal matchings that are
distinct and both stable.

R5, MET relative to the status source. The OEIS offset is 1, so the 22nd term is a(22) = 11221136. a357271_1.txt holds
tables and MiniZinc blocks only for orders 7, 9, 11, 13, 15, and its lb lines are the same five orders. It has no
order-22 instance and no order-22 value. 12277568 - 11221136 = 1056432 > 0.

## 3. Counters (smcount3.c built with `cc -O2 ... -lm`; output verbatim)
`./smcount3 count instance_n22.prefs 1` runs the rotation-poset ideal DP, then a visited-set lattice walk that re-checks
every visited matching against the blocking-pair definition:
```
file: instance_n22.prefs
n: 22
rotations: 211
memo_states: 489227
count_poset: 12277568
seconds_poset: 0.1177
count_lattice_verified: 12277568
seconds_lattice: 19.1974
agree: yes
exit=0
       19.87 real        16.09 user         0.32 sys
          1196049608  peak memory footprint
```
`./smcount3 enumerate instance_n22.prefs` is a reverse search over all ideals. It turns each ideal into its matching and
re-checks that matching against the definition:
```
count_poset: 12277568
enumerated_ideals: 12277568
unstable_matchings_found: 0
n: 22
rotations: 211
seconds_enumerate: 6.63
agree: yes
exit=0
        6.79 real         6.25 user         0.08 sys
           185057760  peak memory footprint
```
R6, MET. There are three agreeing exact counts of 12277568, from the claimant's own program ("Written for V3R1T4S lane
A"). These are closed subsets of the rotation poset, cross-checked as the criterion asks.

Calibration of the same binary on the five published blocks of a357271_1.txt. The names ongK.prefs are my scratch .prefs
conversions of the order-K tables. They are not claim files.
```
ong7.prefs  count_poset: 81 count_lattice_verified: 81 agree: yes 
ong9.prefs  count_poset: 365 count_lattice_verified: 365 agree: yes 
ong13.prefs  count_poset: 7123 count_lattice_verified: 7123 agree: yes 
ong15.prefs  count_poset: 27059 count_lattice_verified: 27059 agree: yes 
file: ong11.prefs
count_poset: 1690
count_lattice_verified: 1690
agree: yes
```
All five published values (81, 365, 1690, 7123, 27059) are reproduced.

## 4. Stretched-definition hunt
- Ties, incomplete lists, non-square instance: none (section 2).
- Unstable matchings counted: none. The lattice walk calls is_stable on every visited matching and exits with code 3 on
  any failure; it exited 0. The reverse search reports `unstable_matchings_found: 0`.
- Double counting: the lattice walk stores each whole matching as an exact 110-bit key (5 bits x 22 men in a 128-bit
  integer) and compares keys exactly, so its 12277568 are distinct matchings. The reverse search gives each ideal one
  parent (the ideal minus its highest-index rotation). The DP, the walk and the reverse search agree.
- What rests on theory: the theory-free part is that at least 12277568 distinct matchings each satisfy the definition,
  and that alone decides "strictly more". "Exactly" (no further stable matchings) rests on the rotation-lattice theory of
  Gusfield and Irving, which the criterion explicitly accepts.
- Composition / re-listing. My independent rebuild shows instance_n22.prefs is exactly the O[K2] product of the order-11
  block published in a357271_1.txt with Knuth's order-2 instance (`... equals instance_n22.prefs exactly: True`). That
  block has 1690 stable matchings by both counts (section 3). This does not make the claim a re-listing of a known value:
  the status source has no order-22 instance and no order-22 value of at least 12277568. The value also cannot be read
  off the published count. The block-only lower bound for O[K2] is 1690*2^11 = 3461120, which is below the bar, so the
  exact count was needed. The object is a new explicit order-22 instance whose exact count is above the table's value.
- Context only, not part of this claim. The same doubling applied to the published order-7 and order-9 blocks also
  beats the table: 23744 > a(14) = 20176 and 530528 > a(18) = 456300 (program output below). So the gain at n = 22 is a
  mechanical consequence of the published order-11 improvement under a classical composition, not a search result. The
  criterion does not restrict the method. The charter's own n = 14 bar (20,176) is also a table value that this doubling
  exceeds, which shows the charter treats recorded values as the bar, not values that could be derived by composition.
```
=== ong7_K2.prefs
count_poset: 23744
count_lattice_verified: 23744
agree: yes
=== ong9_K2.prefs
count_poset: 530528
count_lattice_verified: 530528
agree: yes
```
(ong7_K2.prefs and ong9_K2.prefs are my scratch O[K2] products of the order-7 and order-9 blocks, at orders 14 and 18.)

## 5. Null models
No null test is needed. The claim is one explicit, hashed object counted by deterministic exact programs and compared
with one fixed published integer. There is no sampling, no randomness in the counts, and no selection among noisy
estimates, so there is no statistical claim for a null model to calibrate. The relevant baselines are the bar itself,
the counters' reproduction of all five published block values, and the block-only bound (3461120), which does not beat
the bar.

## 6. Residual items (none fails a literal requirement)
- a357271_1.txt says "lb(15)=27059 (previously 25011, or 26424 shown in A371810)". So another OEIS entry once held a value
  above the A357271 data line at n = 15. A371810 is not in claim/ and I had no web access, so I could not check whether it
  lists an order-22 value. Under the charter's own convention (section 1, R5) the bar is a(22) = 11221136. A novelty
  check outside claim/ should look at A371810 before anything is published.
- n = 22 is not a named priority cell (R3). The result is a composition of a published block, not a search result.

## Verdict
The claim meets the criterion's opening clause literally at n = 22, an admitted and non-excluded order. It is a genuine
win over the status-source value and is not subsumed by any value in the status source.

confirmed_scope: The explicit order-22 instance instance_n22.prefs (22 men and 22 women with complete strict preference lists, equal to the O[K2] doubling of the order-11 block published in a357271_1.txt) has 12277568 stable matchings according to three agreeing exact counts (a rotation-poset ideal DP, a visited-set lattice walk and a reverse-search enumeration, the last two re-checking every matching against the blocking-pair definition), which is strictly more than the order-22 value a(22) = 11221136 in the saved OEIS A357271 entry, whose linked instance file lists no order-22 instance.
pass: true
