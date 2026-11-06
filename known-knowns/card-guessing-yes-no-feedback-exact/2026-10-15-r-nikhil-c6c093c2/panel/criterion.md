context: subagent (Claude Code Agent tool, fresh context)

# CRITERION skeptic: claim `card-guessing-yes-no-feedback-exact` (P+_{2,n}, yes/no feedback)

**Literal verdict: the full success criterion is NOT met. The named partial win p1 (n = 11, 12, 13) IS met.**
The full criterion fails its calibration clause (DGS Table 3 at n = 7) when that clause is read literally. p1 has no
calibration clause, and every obligation it does have was confirmed by a checker I wrote myself, independently.

## 0. Ground rules followed
- I read only the claim folder: README.md, REPRODUCE.md, SHA256SUMS, values.json, status/status_record.md, solver/,
  checker/ and cert/. I wrote my own checker from the definition quoted in README.md before opening
  checker/verify_cert.py.
- Everything I created is in `../panel/criterion_work/` (relative to the claim folder), written `$W` below. All
  commands were run from the claim folder under `nice -n 15`, with at most two single-threaded jobs at once. The
  largest peak RSS I observed was 0.68 GB (my checker on n = 14, measured with BSD `time -l`). The claim's own
  brute force at n = 4 reached 0.49 GB.
- I made one network request, to the status source (section 9). I did not fetch DGS or Luo. The printed DGS
  entries used below are the ones quoted in status/status_record.md and README.md.
- `shasum -a 256 -c SHA256SUMS` reports all 23 entries OK, so the claim folder matches its manifest. I modified
  nothing in it.
- A usage-limit pause interrupted the session from about 14:20 to 18:52 UTC. The n = 14 check that was running then
  was killed and re-run (section 3).

## 1. The criterion, split into literal obligations
- C1: exact values of P+_{2,n} as reduced rationals for EVERY n = 11..16.
- C2: each value comes with a Bellman certificate, "the table of V+(r, f) over all reachable canonical states".
- C3: a checker verifies that table "state by state against Luo's recursion": p_i = C(r-e_i,f)/C(r,f);
  V+ = max_i {p_i[1+V+(r-e_i,f)] + (1-p_i)V+(r,f+e_i)}; V+ = 0 when no free position remains.
- C4: "The same code must reproduce Table 3 of Diaconis-Graham-Spiro for n = 2..10 to four decimals".
- C5: "any newer published values found via the status source must be matched or exceeded in range".
- p1 (verbatim): "Certified exact P+_{2,n} for n = 11, 12 and 13 (the first values beyond the published table)."
  This text has no calibration clause.

## 2. The canonical-state quotient, re-derived
Let S = (r, f) be a Luo state with C(S) > 0. Call a label active if r_i >= 1 and exhausted if r_i = 0. Define
kappa(S) = (g, sorted multiset of active pairs (r_i, f_i)), where g = the sum of f_i over the exhausted labels.
1. C is a function of the active pairs alone; g does not enter at all. In (A.1), M = sum r_i is a sum over the
   active labels only. For an exhausted label the k_i-sum has the single term k_i = 0, with factor
   binom(f_i,0)(0)_0 / 0! = 1. The remaining sum is symmetric under permuting the active labels.
2. L = M - (sum of active f_i) - g, so L is a function of kappa.
3. Transitions respect kappa. Guessing an active label with pair (a,b):
   - yes gives (a-1,b), or, when a = 1, the pair is dropped and g += b;
   - no gives (a,b+1).
   Guessing an exhausted label: p_i = 0 and only the no-branch exists, with f_i+1, i.e. g+1. That successor is the
   same for every exhausted label, and the action exists exactly when #pairs < n.
4. Induction on L then shows that V+(S) depends only on kappa(S) and n:
   - L = 0: V+ = 0.
   - L >= 1: every term of the max depends only on kappa(S) together with either the chosen pair value or the tag
     "exhausted". Identical pairs give identical terms, and all exhausted labels give the same term.
   So max over all n labels = max over (distinct pair classes) together with one exhausted representative.

Conclusion: g plus the sorted active pairs is a legitimate canonical form for Luo's (r, f). V+ and C are functions of
it, and the README's justification is correct. Storing W = C*V+ instead of V+ is an exact encoding, since
V+ = W/C with C recomputed from (A.1), and C > 0 for every listed state.

Integer form. The arrangements consistent with S split by the label at the next free position, so
C(no_i) = C - C(yes_i). For an exhausted i, C(yes_i) = 0 and C(no_i) = C. Multiplying by the constant C > 0 gives
C*[p_i(1+V_yes) + (1-p_i)V_no] = C(yes_i) + W(yes_i) + W(no_i), where an omitted branch has C = 0 and contributes
0. Multiplying a max by the same positive constant preserves it. So W = max_i [C(yes_i)+W(yes_i)+W(no_i)] is
exactly equivalent to Luo's recursion. Because W = 0 on layer L = 0 and each layer is determined by the layer below
it, a table that passes these checks is the unique solution: there is no slack for a wrong table.

Empirical confirmation that the quotient changes nothing:
```
# no quotient at all: full n-vectors, (A.1) summed term by term over all k-vectors, max over all n labels, Fractions
nice -n 15 python3 -I $W/rawluo.py {n} 2
n=2 m=2 rawLuo=17/6 (36 raw states memoised)
n=3 m=2 rawLuo=271/90 (540 raw states memoised)
n=4 m=2 rawLuo=1279/420 (7344 raw states memoised)
n=5 m=2 rawLuo=57583/18900 (94581 raw states memoised)
# label symmetry only (all n pairs sorted, exhausted labels kept with their own f_i, NO g-merge), rational form
nice -n 15 python3 -I $W/symluo.py {n} 2
n=4 m=2 symLuo=1279/420 = 3.0452380952 (510 states)
n=5 m=2 symLuo=57583/18900 = 3.0467195767 (1821 states)
n=6 m=2 symLuo=1136743/374220 = 3.0376329432 (5774 states)
n=7 m=2 symLuo=206528731/68108040 = 3.0323693209 (16770 states)
```
All of these equal values.json. In addition, my literal checker (section 3) evaluates C(r-e_i,f) and C(r,f+e_i) on
full n-vectors, with the exhausted f's placed on specific labels. For every state and every label it asserts that
these equal the C of the canonical successor; this held throughout for n = 2..8.

## 3. The certificates against the recursion: my own checker
`$W/my_checker.py` (literal mode) recomputes, for every listed state:
- C from (A.1) on a full n-vector, and requires C > 0 and L(state) = the layer, with no duplicates and sorted pairs;
- W = 0 on layer 0;
- for L >= 1, a loop over ALL n labels (exhausted ones included, with p_i = 0) that checks
  C(yes)+C(no) = C and requires every positive-probability successor in layer L-1. A missing successor is accepted
  only if its (A.1) count is 0. It then checks both the integer max and the Fraction form
  max_i p_i(1+V_yes)+(1-p_i)V_no = W/C;
- that the top layer is exactly the initial state, and that W/C equals the claimed value, which must also be
  reduced.

`$W/my_checker_fast.py` checks the same things in integer form only, with one representative per pair class plus
one exhausted label. That is equivalent by section 2. It streams two layers at a time.
```
for n in 2..8: nice -n 15 python3 -I $W/my_checker.py cert/n$n.txt.gz --claimed <values.json> --literal
n=2 m=2 states=21 label-actions=30 V0=17/6                         claimed=17/6 reduced=True equal=True  errors=0 PASS
n=3 m=2 states=118 label-actions=237 V0=271/90                     claimed=271/90 reduced=True equal=True  errors=0 PASS
n=4 m=2 states=496 label-actions=1288 V0=1279/420                  claimed=1279/420 reduced=True equal=True  errors=0 PASS
n=5 m=2 states=1727 label-actions=5600 V0=57583/18900              claimed=57583/18900 reduced=True equal=True  errors=0 PASS
n=6 m=2 states=5311 label-actions=20838 V0=1136743/374220          claimed=1136743/374220 reduced=True equal=True  errors=0 PASS
n=7 m=2 states=14903 label-actions=69153 V0=206528731/68108040     claimed=206528731/68108040 reduced=True equal=True  errors=0 PASS
n=8 m=2 states=38967 label-actions=209552 V0=61829276953/20432412000  claimed=61829276953/20432412000 reduced=True equal=True  errors=0 PASS
```
Here label-actions = (number of states with L >= 1) x n, i.e. literally every label. For example, n = 2 gives
15 x 2 = 30 and n = 3 gives 79 x 3 = 237. No "zero-probability successor listed" note was printed.
```
for n in 2..13: nice -n 15 python3 -I $W/my_checker_fast.py cert/n$n.txt.gz --claimed <values.json>
n=2  states=21 ...  V0=17/6 ... reduced_and_equal=True errors=0 PASS          (n = 2..8 all PASS, same V0 as above)
n=9  states=96163 max_layer=30619 distinct-actions=322242 V0=6298009733989/2084106024000  reduced_and_equal=True errors=0 PASS
n=10 states=226091 max_layer=69977 distinct-actions=812989 V0=170757866939041/56568592080000  reduced_and_equal=True errors=0 PASS
n=11 states=509906 max_layer=153537 distinct-actions=1952906 V0=137912544707079557/45735706696680000  reduced_and_equal=True errors=0 PASS
n=12 states=1109092 max_layer=325275 distinct-actions=4496408 V0=228254911260131056513/75738330289702080000  reduced_and_equal=True errors=0 PASS
n=13 states=2336473 max_layer=668123 distinct-actions=9975628 V0=3901622163101296907981/1295524070744904000000  reduced_and_equal=True errors=0 PASS
     (n=13: 560.54 real, 180.45 user, 211 MB max RSS, 323 MB peak footprint)
n=14 states=4784071 max_layer=1335320 distinct-actions=21417878 V0=28008675189200821587458897/9304453876089900528000000  reduced_and_equal=True errors=0 PASS
     (n=14: re-run after the pause, 433.86 real, 269.65 user, 682 MB max RSS)
```
For n = 15 and 16 I ran only structural checks, because my Python checker would exceed the 1 GB budget there. The
state-by-state check of those two belongs to the REPRODUCE skeptic. The structural checks, with real output:
```
gzip -dc cert/n$n.txt.gz | nice -n 15 python3 -I -c '<count layers, last line, W0/C0 with C0=(2n)!/2^n>' $n
n=14 layers=0..28(29) announced=4784071 listed=4784071 values.json_states=4784071 last_is_initial=True W0/C0=28008675189200821587458897/9304453876089900528000000 equals_claimed=True gcd=1
n=15 layers=0..30(31) announced=9548576 listed=9548576 values.json_states=9548576 last_is_initial=True W0/C0=811893265752470943966781067/269829162406607115312000000 equals_claimed=True gcd=1
n=16 layers=0..32(33) announced=18623134 listed=18623134 values.json_states=18623134 last_is_initial=True W0/C0=287519620950287971428538054033/95596617538340806567680000000 equals_claimed=True gcd=1
```

## 4. Reachability and closure ("all reachable canonical states")
Both checkers require two things. For every listed state with L >= 1, every positive-probability successor must be
listed in layer L-1. And the top layer must contain the initial state (g = 0, n pairs (2,0)). By induction downward
from L = 2n, every state reachable from the initial state is therefore listed and checked. This covers every action,
including guesses of exhausted labels, not only optimal play.

Independently, `$W/reach.py` runs a forward breadth-first search from the initial state over all
positive-probability branches (C > 0 by (A.1)), including exhausted-label guesses. It finds that the listed set
EQUALS the reachable set layer by layer, so there are no missing states and no extras:
```
nice -n 15 python3 -I $W/reach.py {n} cert/n{n}.txt.gz
n=2 reachable=21 certificate=21 exact_set_equality_all_layers=True
... (n = 3..9 likewise: 118, 496, 1727, 5311, 14903, 38967, 96163)
n=10 reachable=226091 certificate=226091 exact_set_equality_all_layers=True
n=11 reachable=509906 certificate=509906 exact_set_equality_all_layers=True
```

## 5. The reference checker (checker/verify_cert.py), audited after writing my own
- It recomputes C from (A.1), not from the table. The table contains no C at all. `count_C` evaluates the (A.1)
  sum regrouped by K, asserts exact division by prod r_i!, and requires C >= 0.
- It checks every line; there is no sampling. Per-layer counts must equal the headers, layers must run 0, 1, ...,
  n*m in order, duplicates are rejected, pairs must be sorted with 1 <= r <= m and f >= 0, and the layer must equal
  L(state).
- It handles a missing successor correctly. `lookup()` recomputes `count_C` and fails if C > 0, so a missing
  successor is never silently given W = 0.
- It includes the exhausted-label action (`if k < n`) and checks C(no) = C for it, and it checks C(yes)+C(no) = C
  for every class.
- Gaps, none of which affects the claimed values:
  - `--claimed` is compared as a Fraction, so an UNREDUCED claimed fraction still passes. Demonstrated:
    `--claimed 115166/37800` on cert/n5.txt.gz printed PASS. Reducedness is covered by my own gcd check
    (section 6).
  - g >= 0, and g = 0 when no label is exhausted, are not validated. Such states are unreachable, so this cannot
    affect the initial value.
  - With `--persistence`, the `continue` at line 216 skips the `--literal` comparison. That option is not used for
    the claim.

Runs:
```
for n in 2..8: nice -n 15 python3 -I checker/verify_cert.py cert/n$n.txt.gz --claimed <values.json> --literal
n=2 m=2 states=21 actions=27 value=17/6 = 2.833333333333  PASS
n=3 m=2 states=118 actions=194 value=271/90 = 3.011111111111  PASS
n=4 m=2 states=496 actions=968 value=1279/420 = 3.045238095238  PASS
n=5 m=2 states=1727 actions=3890 value=57583/18900 = 3.046719576720  PASS
n=6 m=2 states=5311 actions=13510 value=1136743/374220 = 3.037632943188  PASS
n=7 m=2 states=14903 actions=42108 value=206528731/68108040 = 3.032369320861  PASS
n=8 m=2 states=38967 actions=120575 value=61829276953/20432412000 = 3.026039067390  PASS
nice -n 15 python3 -I checker/verify_cert.py cert/n11.txt.gz --claimed 137912544707079557/45735706696680000
n=11 m=2 states=509906 actions=1952906 value=137912544707079557/45735706696680000 = 3.015423936088  PASS   (346 MB max RSS)
```
These action counts equal my fast checker's distinct-action counts.

Negative controls on n = 5 (tampered copies in $W/tamper/):
```
bump one W (0|1:0,1:0,1:4,2:0|12 -> 13):
  reference: FAIL: recursion fails at (0, ((1, 0), (1, 0), (1, 4), (2, 0))): table W=13, max over labels=12
  mine:      ERROR W mismatch 0|1:0,1:0,1:4,2:0|13 12   (FAIL)
delete state 0|2:0,2:1|7 (layer count fixed up):
  reference: FAIL: successor (0, ((2, 0), (2, 1))) missing from table but C=3>0
  mine:      ERROR missing positive-probability no successor 0|2:0,2:0|17 0|2:0,2:1 3   (FAIL)
wrong claimed 57584/18900:  reference: FAIL: initial value 57583/18900 != claimed 57584/18900
unreduced claimed 115166/37800:  reference: PASS (gap noted above);  mine: errors=1 FAIL
```

## 6. Exact reduced rationals and decimals
```
python3 -I $W/calib.py values.json      (gcd and decimal20 part)
n= 2..16: gcd=1 for all 15 fractions; decimal20 equals the 20-digit TRUNCATION of the fraction for all 15
          (it differs from 20-digit rounding for n = 4,5,7,8,9,10,11,13,14,16; values.json never calls it rounded)
```
All values in values.json are reduced fractions, and the decimals follow from them as truncations. The initial
counts C0 = (2n)!/2^n are asserted by my checker, so V0 = W0/C0 is the reduced claimed fraction for every
n = 2..16. For n = 15 and 16 this comes from the structural check only.

## 7. "The same code": solver rebuilds
solver/cg_solver.cpp and solver/cg_solver_v2.cpp differ only in the f bit-width (FSHIFT 5 against 6 for m <= 3).
I compiled both exactly as in REPRODUCE.md section 3 (clang++ -O2 -std=c++17, GMP, zlib; binaries in $W) and
compared the decompressed sha256 of the output with cert/:
```
n=2..11, cg_solver and cg_solver_v2: rebuilt_sha == cert_sha for all 20 runs (same=yes), values identical to values.json
  e.g. n=7  cg_solver    cert_sha=d8e03113f6f13a4a rebuilt_sha=d8e03113f6f13a4a same=yes 206528731/68108040 3.03236932086138435344 14903
       n=11 cg_solver_v2 cert_sha=cf22ddfea1cc0158 rebuilt_sha=cf22ddfea1cc0158 same=yes 137912544707079557/45735706696680000 ... 509906
n=12, cg_solver: cert/n12 decompressed sha256 be12ebcc...79d755c == rebuilt be12ebcc...79d755c
```
So the code that computes the calibration values n = 2..10 is the code that produced cert/n11 and cert/n12. I did
not rebuild n = 13..16.

There is a minor inconsistency in the claim's own text. A v2 comment says the wider field is "needed for n >= 16 at
m = 2", while README.md says cg_solver.cpp handles n <= 16. In a reachable n = 16 state f_i <= 30: M <= 32, and
M = 32 forces every r_i = 2, so f_i <= M - r_i. The no-successor key therefore has f <= 31, which fits v1's 5-bit
field. The comment looks over-cautious, and it does not matter here.

## 8. Raw-definition cross-checks (no sufficient statistic assumed)
```
nice -n 15 python3 -I $W/rawgame.py 2 2  ->  n=2 m=2 rawgame=17/6 (6 sequences)         [my own brute force]
nice -n 15 python3 -I $W/rawgame.py 3 2  ->  n=3 m=2 rawgame=271/90 (90 sequences)
nice -n 15 python3 -I solver/bruteforce_raw_definition.py 3 2  ->  n=3 m=2 words=90 memo_states=4558 P+=271/90 = 3.0111111111
nice -n 15 python3 -I solver/bruteforce_raw_definition.py 4 2  ->  n=4 m=2 words=2520 memo_states=1632553 P+=1279/420 = 3.0452380952 time=129.0s (488 MB)
values.json: 3 -> 271/90, 4 -> 1279/420
```
I read the claim's brute force, and it implements the raw game: the posterior is uniform over consistent words,
any label can be guessed at any step, and it memoises on the (time, consistent set) pair. My own rawgame.py is
written the same way, with Fractions. Luo Prop. B.1 gives P+_{2,2} = 17/6, which matches.

## 9. C5: the status source
```
curl -sS -A 'V3R1T4S-criterion-skeptic/1.0 (research status check)' 'https://arxiv.org/search/?query=card+guessing+feedback&searchtype=all&abstracts=show&order=-announced_date_first&size=25'   (one GET, no retries)
2026-10-15 14:13:52 UTC  HTTP 200 bytes 98792
sha256 b457009a53b9c7f9ccf724ce8f7c247446977de8a5eb819340e5d339e80ed6fd   (identical to the scout's recorded hash)
"Showing 1-19 of 19 results"; newest: 2610.17479, 2609.25063, 2609.25062 (Luo), 2607.10418, 2602.12928, 2602.07920, 2601.16607, ...
```
I read the abstracts of the partial-feedback entries. 2609.25062 (Luo) gives bounds on P+_{m,n} and P-_{m,n};
2010.05059 gives an m + O(m^{3/4} log m) bound; 2012.04019 (DGS) is about heuristics. None of them reports an exact
P+_{2,n} for n >= 11. No newer published value was found, so C5 holds vacuously. The claimed range, n <= 16, extends
past the published n <= 10.

## 10. C4: the calibration requirement, ruled literally
```
python3 -I $W/calib.py values.json      (calibration part; printed values as quoted in status/status_record.md)
 n= 2 exact=2.83333333 round4=2.8333 trunc4=2.8333 printed=2.8333  round_ok=True  trunc_ok=True  exact-printed=+0.0000333
 n= 3 exact=3.01111111 round4=3.0111 trunc4=3.0111 printed=3.0111  round_ok=True  trunc_ok=True  exact-printed=+0.0000111
 n= 4 exact=3.04523809 round4=3.0452 trunc4=3.0452 printed=3.0452  round_ok=True  trunc_ok=True  exact-printed=+0.0000381
 n= 5 exact=3.04671957 round4=3.0467 trunc4=3.0467 printed=3.0467  round_ok=True  trunc_ok=True  exact-printed=+0.0000196
 n= 6 exact=3.03763294 round4=3.0376 trunc4=3.0376 printed=3.0376  round_ok=True  trunc_ok=True  exact-printed=+0.0000329
 n= 7 exact=3.03236932 round4=3.0324 trunc4=3.0323 printed=3.0323  round_ok=False trunc_ok=True  exact-printed=+0.0000693  |diff|<0.5e-4:False |diff|<1e-4:True
 n= 8 exact=3.02603906 round4=3.0260 trunc4=3.0260 printed=3.0260  round_ok=True  trunc_ok=True  exact-printed=+0.0000391
 n= 9 exact=3.02192386 round4=3.0219 trunc4=3.0219 printed=3.0219  round_ok=True  trunc_ok=True  exact-printed=+0.0000239
 n=10 exact=3.01859849 round4=3.0186 trunc4=3.0185 printed=3.0186  round_ok=True  trunc_ok=False exact-printed=-0.0000015
 (no exact ties at the 5th decimal)
```
Ruling:
- Under the table's own stated convention ("rounded to four decimal places"), the code reproduces 8 of the 9
  entries. At n = 7 it gives 3.0324 where the table prints 3.0323.
- The README offers a fallback: "every other entry agrees under rounding and truncation alike". That is FALSE. At
  n = 10 the exact value 3.01859849... truncates to 3.0185, but the table prints 3.0186. (My brief repeated the
  same statement; it is incorrect.)
- So no single four-decimal convention reproduces all nine printed entries:
  - rounding fails n = 7;
  - truncation, i.e. "the first four decimals agree", fails n = 10;
  - "error under half a unit in the 4th place" fails n = 7 (6.93e-5 > 5e-5);
  - only the loose reading |difference| < 1e-4 passes all nine.
- "Reproduce Table 3 ... to four decimals" is therefore **not met literally**.
- The criterion's "Table 3 for n = 2..10" does not fit the record, which puts n = 2..5 in Table 2. That does not
  matter here: n = 7 is in Table 3 either way.

Substance, which does not change the literal ruling: the n = 7 value 206528731/68108040 is robust.
- My literal certificate check, my label-symmetric recursion without g-merging, the claim's solver, and a variant
  that forbids exhausted-label guesses all give it:
  `symluo_noburn.py 7 2 -> 206528731/68108040`, and the noburn variant also equals values.json for n = 3..6.
- The raw-game brute force agrees wherever it is feasible (n = 2, 3, 4).

The mismatch is therefore most plausibly a truncated or misprinted DGS entry, not an error in the code. It
undermines none of the certified values. But the criterion says the code "must reproduce" the table, and at n = 7
it does not.

## 11. Decision
- Full criterion: **not met**.
  - C4 fails literally at n = 7, as above.
  - Separately, I verified C2/C3 state by state only for n = 2..14. cert/n15.txt.gz and cert/n16.txt.gz passed
    structural checks only.
  - C1 (reduced rationals for 11..16) holds for the fractions as written. C5 holds vacuously.
- Partial win p1: **met**. For each of n = 11, 12, 13, my independent checker verified:
  - closure: every canonical state reachable from the initial state through a positive-probability branch is
    listed;
  - every listed state against Luo's recursion, with max over all labels, zero-probability branches omitted,
    V+ = 0 at L = 0, and C recomputed from (A.1);
  - that the initial value is the reduced fraction in values.json.
  Further evidence:
  - for n = 11, an independent BFS shows the listed set equals the reachable set exactly, and the reference
    checker also passes;
  - cert/n11.txt.gz and cert/n12.txt.gz are rebuilt byte-identically by the same solver code.
  - Novelty: none of these values appears via the status source.
- Interpretive caveat: p1 is read literally, with no calibration clause. If the panel decides that p1 inherits the
  main criterion's calibration sentence, the same n = 7 issue would make the outcome "neither".

confirmed_scope: Only partial win p1 is confirmed: the reduced fractions P+_{2,11} = 137912544707079557/45735706696680000, P+_{2,12} = 228254911260131056513/75738330289702080000 and P+_{2,13} = 3901622163101296907981/1295524070744904000000 are certified by cert/n11.txt.gz, cert/n12.txt.gz and cert/n13.txt.gz, each verified by my independently written checker state by state over all reachable canonical states (C recomputed from (A.1), max over every label including exhausted ones, closure from the initial state) against Luo's Appendix A recursion (cert/n2.txt.gz to cert/n10.txt.gz and cert/n14.txt.gz also pass that check, which does not complete the full criterion); the full criterion is not met literally, because the code's n = 7 value 206528731/68108040 = 3.0323693... rounds to 3.0324 whereas DGS Table 3 prints 3.0323 under its stated rounding (and truncation would instead fail n = 10, 3.0185 against 3.0186), and because cert/n15.txt.gz and cert/n16.txt.gz were not verified state by state by me.

pass: true
