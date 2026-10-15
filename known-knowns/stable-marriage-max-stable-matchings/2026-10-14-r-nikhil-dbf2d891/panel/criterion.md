# CRITERION skeptic: stable-marriage-max-stable-matchings, claimed cell n = 28

context: subagent (Claude Code Agent tool, fresh context, sees only claim/)

Files read: CLAIM.md, REPRODUCE.md, instance_n28.prefs, smcount3.c, count_stable.py, A357271.txt and a357271_1.txt, all in the
claim folder. Nothing else in the run folder was opened. All work was done in ../panel/scratch_criterion/ (a copy of the claim folder plus my
own scripts in ../panel/scratch_criterion/scripts/: sm_indep.py, check1.py, poset_count.py, build_alt.py). At the end, `diff -r` of the claim folder
against the scratch copy printed nothing, so the claim folder was not modified.

## 1. The criterion, word by word

> for an n whose maximum is not known, give a stable-marriage instance (complete strict preference lists for n men and n women) with
> strictly more stable matchings than the best known instance of size n. Cells in order: n = 13 (beat 7,123), n = 15 (beat 27,059),
> n = 14 (beat 20,176; no search has touched it), and n = 7 (beat 81) as a cheap calibration cell. Do not aim at n = 6, 8, 10, 12 or 16,
> which are conjectured exact. Shape: record (explicit preference lists; stable matchings counted exactly by your own enumerator: closed
> subsets of the rotation poset, or exhaustive enumeration, cross-checked).

Requirements:
- R1: n must be one "whose maximum is not known".
- R2: n must not be 6, 8, 10, 12 or 16.
- R3: how n relates to the four named cells (13, 15, 14, 7).
- R4: the object must be a stable-marriage instance with complete strict preference lists for n men and n women.
- R5: it must have strictly more stable matchings than the best known instance of size n.
- R6 (shape): explicit lists; an exact count by the claimant's own enumerator, using closed subsets of the rotation poset or exhaustive enumeration; cross-checked.
- R7: one cell and one instance.

## 2. Requirement-by-requirement check

**R1: met.** A357271.txt, %C line: "At the time of publication, the bounds were known to be exact up to n=4. A357269 shows that they are
also exact for n=5." The status source gives exact maxima only for n <= 5, so the maximum for n = 28 is not known.

**R2: met.** From my script (check1.py on A357271.txt): `conjectured-exact sentence: a(6), a(8), a(10), a(12), and a(16) are also
conjectured to be exact.` 28 is not in the excluded list.

**R3: n = 28 is admitted, but it is not a named cell.** Read literally:
- The success condition is the first sentence. It quantifies over "an n whose maximum is not known", and n = 28 satisfies that.
- "Cells in order: ..." ranks four cells and gives their bars. It contains no word of exclusivity.
- The next sentence explicitly excludes n = 6, 8, 10, 12 and 16. That exclusion only means something if the opening clause admits n
  beyond the four listed cells.

So n = 28 is admitted under the opening clause. It is none of the four named cells, and the criterion has no enumerated partial wins, so
the claim can only count as the general (full) success clause. It is not a win on cell 13, 15, 14 or 7.

**R4: met.** Output of my own strict parser (check1.py), which shares no code with the claim:
```
instance comment lines: 1
data rows: 56  row lengths: [28]
order n = 28 ; all 56 rows are permutations of 1..28 (complete, strict, no ties): True
instance sha256: dbf2d89155213b672ef7514493d16c7f02225a84dbcc31f4ae30068f085e1ad0
```
That is 28 men's lists followed by 28 women's lists, each a permutation of 1..28. So the instance is square and complete, and ties are
impossible. The claim's C reader enforces the same thing (`check_perms`) and accepted the file, reporting `n: 28`. The hash matches CLAIM.md:
```
$ shasum -a 256 instance_n28.prefs a357271_1.txt A357271.txt
dbf2d89155213b672ef7514493d16c7f02225a84dbcc31f4ae30068f085e1ad0  instance_n28.prefs
95735e185c5435e7cbe4c6753fe4e4ee120321457279f1f3283523654db5cd47  a357271_1.txt
fd27d7c9ede8781f1fac606a633c62938a7bda778fc04f8557f26278a7c95143  A357271.txt
```

**R5: met against the status source, and also against the stronger "derivable from the status source" reading.**

The bar. The status source's data line:
```
$ grep -E '^%S|^%T|^%U' A357271.txt
%S A357271 1,2,3,10,16,48,71,268,330,1000,1231,6472,6720,20176,25011,195472,
%T A357271 200832,456300,637336,3419680,3506880,11221136,15481956,126112960,
%U A357271 127885440,262860800,384418176,2000043808
```
The same check from check1.py:
```
offset: 1 ; number of terms: 28 ; a(28) = 2000043808 ; last term = 2000043808
a357271_1.txt lb lines: [('7', '81'), ('9', '365'), ('11', '1690'), ('13', '7123'), ('15', '27059')]
a357271_1.txt example orders: [('7', '81'), ('9', '365'), ('11', '1690'), ('13', '7123'), ('15', '27059')]
```
The offset is 1 and there are 28 terms, so 2000043808 is the 28th and last term, a(28). The newer instance file states improved bounds only
for n = 7, 9, 11, 13 and 15, and contains instances only for those orders. The %N line says a(n) is "based on composing smaller instances",
so a(28) is itself a composition bound.

The count: 2497797760, from three counters that agree.

(a) The claim's memoised rotation-poset count. I ran a copy of smcount3.c whose only change is the initial memo capacity. The unmodified
binary grows its 88-byte-entry table from 2^23 to 2^24 entries, which costs 2214592512 bytes at peak (sizeof(Memo) = 88), above my 2 GB budget. The counting logic
is unchanged:
```
189c189
<     if (!memo) { memo_init(1 << 14); const char *e = getenv("MEMO_MAX_STATES"); if (e) memo_max = (size_t)atol(e); }
---
>     if (!memo) { memo_init(1 << 24); const char *e = getenv("MEMO_MAX_STATES"); if (e) memo_max = (size_t)atol(e); }
```
```
$ MEMO_MAX_STATES=40000000 smcount3_presized count instance_n28.prefs 0
file: instance_n28.prefs
n: 28
rotations: 362
memo_states: 6324107
count_poset: 2497797760
seconds_poset: 2.0324
          1478737920  maximum resident set size
```

(b) The claim's reverse-search enumeration, which visits every ideal and re-checks the matching it produces against the stability
definition. First run, started in the background (nohup, nice -n 15), ran to completion:
```
$ MEMO_MAX_STATES=40000000 smcount3_presized enumerate instance_n28.prefs
count_poset: 2497797760
enumerated_ideals: 2497797760
unstable_matchings_found: 0
n: 28
rotations: 362
seconds_enumerate: 2879.19
agree: yes
      402.21 real      2075.10 user        15.05 sys
          1478721536  maximum resident set size
                   0  signals received
```
To keep to one CPU thread, I paused this run three times with SIGSTOP/SIGCONT, each time for under 30 s, while my own checks ran. Pausing
cannot change the result. The `real` figure from /usr/bin/time does not match the user CPU time or the program's own monotonic timer.
Treat it as unreliable; it has no bearing on the printed counts. The status of a second run (stopped unfinished) is reported below.

Second run. After a session pause, a re-run was requested, on the mistaken premise that the first run had been killed. I started it
with the same binary and command (nohup, nice -n 15) at 08:16Z. Machine load then rose to between 130 and 160 on 18 cores, so it could not
finish within my time budget. I stopped it unfinished at 09:17Z, after 39:42.86 of CPU time (more than the first run's whole 2075 s, because of the
load); it produced no output. This does not weaken the evidence. The first run above is
complete: its output has every final line, and /usr/bin/time recorded a normal exit with 0 signals received. The count is deterministic,
and counters (a) and (c) reproduce it independently.

A minor documentation note: REPRODUCE.md says the enumeration uses "memory O(rotations)", but enumerate mode also builds the full memo
table. The measured maximum resident set size was 1478721536 bytes. This does not affect the result, but it does affect anyone
reproducing on a small machine.

(c) An independent counter I wrote for this check (poset_count.py). It shares no code with the claim:
- It finds rotations as the cycles of next_M along one chain from the man-optimal matching.
- It derives the rotation order only from exposure semantics. For each rotation s, it starts at the man-optimal matching and greedily
  eliminates every exposed rotation except s. The rotations that never get eliminated are exactly Up(s). Every matching on every greedy
  path is re-checked as a stable perfect matching, with an explicit bijection test.
- It counts ideals with a forward layer DP over the transitive reduction. It does not use the claim's rule-based predecessor sets.
```
file: instance_n28.prefs | n: 28 | sha256: dbf2d89155213b67...
rotations: 362 | covering relations: 696 | greedy matchings re-checked stable: 8598 | DP max layer: 62500 | DP total states: 6324108
independent_ideal_count: 2497797760
seconds: 5.3
```
Before relying on it at n = 28, I validated this counter on smaller members of the same family against all 5040 perfect matchings and
against my own break-marriage walk. Lines from check1.py and poset_count.py:
```
brute force (all 5040 permutations) recovered order-7 base: 85 (0.0s)
brute force (all 5040 permutations) Ong order-7: 81 (0.0s)
break-marriage walk recovered order-14: 24992 (3.5s)
break-marriage walk Ong O[K2] order-14: 23744 (3.1s)
file: base7_recovered.prefs | n: 7 | ... independent_ideal_count: 85
file: ong7.prefs | n: 7 | ... independent_ideal_count: 81
file: mid14_recovered.prefs | n: 14 | ... independent_ideal_count: 24992
file: ong14_OK2.prefs | n: 14 | ... independent_ideal_count: 23744
```
The claim's own tools agree on the same small instances:
- smcount3 on the recovered order-14 instance: `count_poset: 24992`, `count_lattice_verified: 24992`, `agree: yes`.
- smcount3 on the recovered order-7 instance: `count_poset: 85`, `count_lattice_verified: 85`, `agree: yes`.
- count_stable.py on the recovered order-7 instance: `lattice_count: 85`, `brute_count: 85`, `counters_agree: True`.
- count_stable.py on the Ong order-7 instance from a357271_1.txt: `minizinc_blocks_match_paired_table: True`, `lattice_count: 81`,
  `brute_count: 81`, `matches_claimed_in_file: True`.

Strictly more:
```
claimed - a(28)            = 497753952 ; ratio 1.2489
```

Hidden quantifier, "best known". a(28) is stale even relative to its own status source. Applying the same construction (O[K2] twice) to
the status source's own order-7 instance (Ong et al., 81 stable matchings) already gives more than a(28). Both my counter and the claim's
binary give the same value:
```
file: ong28_OK2K2.prefs | n: 28 | sha256: 75817a9836781a06...
rotations: 330 | covering relations: 632 | greedy matchings re-checked stable: 7502 | DP max layer: 62500 | DP total states: 5777088
independent_ideal_count: 2369365120
$ MEMO_MAX_STATES=40000000 smcount3_presized count ong28_OK2K2.prefs 0
rotations: 330
memo_states: 5777087
count_poset: 2369365120
```
The other product orders of the same instance at order 28 give less: K2[K2[O7]] gives `independent_ideal_count: 437894526`, and
K2[O7[K2]] gives `independent_ideal_count: 1132731904`.

The claimed count is still strictly larger than this derived baseline:
```
claimed - Ong-derived       = 128432640 ; ratio 1.0542
Ong-derived - a(28)        = 369321312 ; share of the gap over a(28) explained by the stale bar: 74.2%
```
So 74.2% of the claimed margin over a(28) is the stale-bar effect. The remainder comes from using an order-7 base with 85 stable matchings
instead of 81.

Residual item outside the evidence. CLAIM.md attributes that base to "Jo's (2026)" Zenodo preprint, which is newer than the status source
and is not in the package. Nothing here shows whether that preprint reports any n = 28 value. The confirmed scope below is therefore
stated relative to the status source and the derived baseline. It does not say "best known".

Side finding for the n = 14 cell (not part of this claim). O[K2] of the status source's own order-7 instance has 23744 stable matchings,
which exceeds that cell's bar of 20,176 by 3568. Any n = 14 claim should be judged against at least 23744.

**R6: met.**
- Explicit lists: yes.
- Own enumerator: yes. smcount3.c is the claimant's own code ("Written for V3R1T4S lane A").
- Method: yes. The criterion names "closed subsets of the rotation poset", and both the count mode and the enumerate mode use it.
  Exhaustive enumeration over all perfect matchings is impossible at n = 28.
- Cross-checked: yes. Counters (a) and (b) agree. They share the claim's rotation and predecessor construction, so I also added counter
  (c), which shares nothing with them and gives the same number. The DP state counts also match: 6324107 memo states versus 6324108
  layer states. The claim's memo covers levels 0 to R-1; my layers cover 0 to R, and the extra state is my final one-state layer.
- One minor code note: the claim's `is_stable` does not test that its argument is a bijection. That is immaterial here, given that (c) agrees.

**R7: met.** One cell (n = 28) and one instance file.

## 3. Hunt for stretched definitions
- Ties or incomplete lists: none. Every row is a permutation of 1..28.
- Non-square instance: no. 28 men's rows and 28 women's rows, each of length 28.
- Counting unstable matchings: no. Counter (b) found 0 unstable among all 2497797760 enumerated matchings. Counter (c) derives the order
  from stable matchings only. Ideals of the rotation poset correspond one-to-one with stable matchings (Gusfield and Irving, chapters 2-3).
- Double counting: no. The DP counts distinct closed subsets, the reverse search visits each ideal once, and the three counts agree.
- Composition that only re-lists a known value: no, within the evidence. My decomposition shows the instance is exactly O7[K2][K2]:
  ```
  order-28 = O14[J2] decomposition exists: True
  inner J (0-indexed): men [[0, 1], [1, 0]] women [[1, 0], [0, 1]]
  order-14 = O7[J2] decomposition exists: True
  product(O7, J) == O14: True
  product(O14, J) == instance: True
  recovered order-7 base, men lists (1-based): [[1, 2, 7, 5, 6, 3, 4], [2, 1, 4, 3, 6, 5, 7], [3, 4, 1, 2, 7, 5, 6], [4, 3, 6, 2, 1, 5, 7], [5, 6, 3, 4, 7, 2, 1], [6, 5, 7, 4, 1, 2, 3], [7, 2, 6, 5, 1, 4, 3]]
  recovered order-7 base, women lists (1-based): [[5, 6, 7, 4, 3, 2, 1], [6, 5, 3, 4, 7, 1, 2], [7, 1, 2, 5, 4, 3, 6], [1, 7, 6, 5, 2, 3, 4], [2, 3, 4, 7, 1, 6, 5], [3, 2, 1, 7, 4, 5, 6], [4, 3, 5, 6, 1, 7, 2]]
  ```
  The base O7 has 85 stable matchings (brute force over all 5040 perfect matchings). The count 2497797760 appears nowhere in the status
  source, and the status source's own a(28) is itself a composition bound. So the object is a new explicit instance with a larger exact
  count than the table value, and also larger than the same construction applied to the status source's own instance.

  It is derivative. The base is third-party; its attribution to Jo (2026) is not verifiable from the package, though its count of 85 is
  verified. The construction is the classical lexicographic doubling, and about three quarters of the margin over a(28) comes from the
  table being stale.

## 4. Null model
No statistical null test is needed. The claim is a deterministic exact count of one fixed explicit object, compared with a fixed table
value. Nothing is sampled, estimated or tested for significance, and a search that selected the object cannot bias an exact count.

The meaningful null here is deterministic: what the same construction yields from the status source's own instances. That baseline is
2369365120 for O[K2] twice applied to Ong's n = 7 instance, and less for the other product orders. The claim exceeds it by 128432640.

## 5. Decision
- The result meets the full success criterion literally:
  - n = 28 is admitted by the opening clause and not excluded;
  - the object is a valid complete, strict, square instance;
  - its exact count, 2497797760, is cross-checked by three counters, one of them fully independent;
  - that count is strictly greater than the status source's n = 28 value, 2000043808.
- It is not one of the four named cells, and no enumerated partial win applies.
- The win is genuine in that the count is exact and beats both the table value and the deterministic baseline derivable from the status
  source.
- The win is non-subsumed within the evidence: no value at or above 2497797760 for n = 28 appears in, or is derivable by these products
  from, the status source.
- Caveats for whoever publishes:
  - It is a derivative composite of a third-party order-7 instance.
  - 74.2% of the margin over a(28) is a stale-bar effect.
  - The contents of the Jo (2026) preprint for n = 28 were not available to this check.

confirmed_scope: instance_n28.prefs is a valid order-28 stable marriage instance (28 men and 28 women, every list a permutation of 1..28) that equals the O[K2] doubling applied twice to an order-7 instance with 85 stable matchings, and it has exactly 2497797760 stable matchings by three agreeing exact counters (the claim's memoised rotation-poset count, the claim's reverse-search enumeration with 0 unstable matchings, and an independent counter), which is strictly more than the n = 28 value a(28) = 2000043808 in the status source A357271.txt and than the 2369365120 stable matchings obtained by applying the same doubling twice to the status source's own order-7 instance in a357271_1.txt.
pass: true
