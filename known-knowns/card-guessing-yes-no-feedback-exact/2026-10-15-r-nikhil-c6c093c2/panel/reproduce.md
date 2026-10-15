context: subagent (Claude Code Agent tool, fresh context)

# REPRODUCE skeptic report: card-guessing-yes-no-feedback-exact (P+_{2,n}, n = 2..16)

## Role and method

I started from "the claim is wrong".
- I read only the claim folder: README.md, REPRODUCE.md, values.json, SHA256SUMS, status/status_record.md, cert/.
- I wrote my own checker from the definition quoted in README.md before opening checker/ or solver/.
- I ran it on every state of every certificate n = 2..16.
- Only after that did I read and run the author's brute force, the author's checker and the author's solver.

My scripts and logs are in my work directory panel/reproduce_work/, a sibling of the claim folder. Claim files are
named relative to the claim folder. The claim folder was not modified: after all runs, `shasum -a 256 -c SHA256SUMS`
reports all 23 entries OK, and no file in it is newer than SHA256SUMS.

## 0. Outcome in brief

- **My own checker:** PASS for every n = 2..16. That covers every listed state (37,295,049 states in total), every
  layer and every action (174,529,297 actions, of which 21,367,952 are exhausted-label guesses).
  - The split identity C(s) = C(yes) + C(no) was asserted at each of the 153,161,345 active-label actions.
  - Each of the 11,110 successors absent from the tables has C = 0 by my own (A.1) computation.
  - Every listed state is reachable.
  - The initial value W/C equals the values.json fraction, which is in lowest terms, for every n.
- **Counts and decimals:** state counts equal values.json certificate_states for every n. The decimal20 entries equal
  the exact values truncated to 20 decimals.
- **Mutation tests:** all 17 mutated certificates are rejected, and the unmodified copy passes.
- **My certificate-free solvers agree with values.json:**
  - Luo's recursion verbatim on full label-indexed vectors (no canonicalisation): n = 2, 3, 4, 5.
  - The raw game over all arrangements: (n,m) = (2,2), (3,2); also (2,3) = 41/10 and (3,3) = 2383/560.
- **The author's code:**
  - Brute force: (3,2) = 271/90 and (4,2) = 1279/420, both equal to values.json.
  - Checker (run after mine): PASS for n = 2..13, with state and action counts identical to mine.
  - Solver, rebuilt from source: its output for n = 2..11 is byte-identical to cert/n{n}.txt.gz after decompression.
- **Finding F1 (calibration note in README.md; not a reproduction failure):**
  - README says every published DGS entry other than n = 7 "agrees under rounding and truncation alike". That is false
    for n = 10: the exact 3.0185984954... rounds to the published 3.0186 but truncates to 3.0185.
  - So no single convention matches all nine quoted entries. Rounding misses n = 7 (3.0324 vs 3.0323), and truncation
    misses n = 10 (3.0185 vs 3.0186).
- **Process deviation (F2):** for about 25 minutes, a third process of mine ran at the same time as the two long runs.
  That exceeds the 2-thread limit, and memory may briefly have neared 2 GB. Details in section 6.

## 1. Definition implemented

Quoted from README.md ("The game (definition, from Luo arXiv:2609.25062 v1, abstract and Appendix A)"):

> A deck contains n labels, each appearing m times, and is shuffled uniformly. The cards are guessed one at a time,
> and after each guess the player is told only whether it was correct. P+_{m,n} is the maximum expected score over
> all adaptive strategies. Appendix A: after successful positions are deleted, r = (r_1..r_n) are the multiplicities
> of cards at positions whose labels remain undetermined, f = (f_1..f_n) count the positions forbidding each label,
> M = sum r_i, L = M - sum f_i. (A.1): C(r,f) = (1/prod r_i!) sum_{0<=k_i<=min(r_i,f_i)} (-1)^K (M-K)! prod_i
> binom(f_i,k_i) (r_i)_{k_i}, K = sum k_i. If C(r,f) > 0 and L >= 1, p_i(r,f) = C(r-e_i,f)/C(r,f) for r_i > 0 and
> p_i = 0 for r_i = 0. V+(r,f) = 0 when L = 0; for L >= 1, V+(r,f) = max_{i in [n]} { p_i [1 + V+(r-e_i,f)] +
> (1-p_i) V+(r,f+e_i) }; branches of probability zero are omitted. The initial state r = (m,...,m), f = 0 gives
> P+_{m,n}.

Certificate convention used (README.md, "Objects"):
- Each state is one line `<g>|<r>:<f>,<r>:<f>,...|<W>`, listing the pairs (r_i, f_i) of the labels with r_i >= 1,
  sorted ascending. The files sort them numerically: 2:2 comes before 2:10.
- g is the total number of forbidden positions belonging to exhausted labels. L = M - sum f_i - g. The number of
  exhausted labels is n - #pairs.
- W = C(r,f) V+(r,f) is an integer.
- Layers run over L = 0..2n in increasing order, each headed by `# L=<L> states=<count>`.
- Transitions:
  - success on i: (r_i, f_i) -> (r_i - 1, f_i); when r_i reaches 0 the pair is dropped and g += f_i;
  - failure on i: (r_i, f_i) -> (r_i, f_i + 1);
  - failure on an exhausted label: g += 1.

### Implementation

The code is in panel/reproduce_work/cgdef.py and panel/reproduce_work/my_checker.py: Python 3.9, standard library
only, exact integers throughout.

**Computing C from (A.1).** Labels with r_i = 0 contribute the factor 1, since only k_i = 0 occurs. I evaluate the
nested sum over (k_1..k_n) grouped by K:

  C = (1/prod r_i!) sum_K (-1)^K (M-K)! [x^K] prod_i Q_i(x),  Q_i(x) = sum_{k<=min(r_i,f_i)} binom(f_i,k) (r_i)_k x^k

This is the same finite sum of integers, summed in a different order. Exact divisibility by prod r_i! is asserted.
Self-test, `python3 test_C.py`, real output:

    brute-force vs (A.1) agree on 1330 random states (M <= 8, m <= 3)
    literal (A.1) vs grouped (A.1) agree on 2947 random m=2 states with up to 16 labels
    C = C(yes) + C(no) verified by brute force on 800 random states with L >= 1
    ALL C SELF-TESTS PASSED

"Brute force" here means direct enumeration of the arrangements.

**Streaming.** The checker streams the gzip file and keeps two layers in memory. Each state is packed into one
integer key. The stored value holds W, C and a reachability bit. Terminal states store only the bit, and their C is
recomputed from (A.1) whenever layer 1 needs it.

**Checks on every listed state of every certificate (no sampling):**
1. Strict parsing: token tables for g and for "r:f" with r in {1,2}, and W a canonical decimal >= 0. Pairs are sorted
   ascending, #pairs <= n, and #pairs = n implies g = 0.
2. M - sum f - g equals the announced layer L. No state appears twice in a layer. Since L is a function of the
   state, this rules out duplicates anywhere in the file.
3. C > 0 by my (A.1), and C <= (2n)!/2^n.
4. If L = 0, then W = 0.
5. If L >= 1, W equals the maximum of:
   - C(yes) + W(yes) + W(no), over one representative of each distinct pair class;
   - when #pairs < n, the exhausted-label guess W(g+1, same pairs).

   Successor values are taken from the table's previous layer. A successor absent from the table must have C = 0 by
   my own (A.1); otherwise the result is FAIL "missing successor". C(s) = C(yes) + C(no) is asserted for every active
   action, and the exhausted-guess successor must carry C(s).
6. Every state of layer L-1 must be a positive-probability successor of some listed state of layer L. The top layer
   L = 2n can only hold the initial state, since it forces M = 2n and sum f = g = 0. So every listed state is
   reachable, and with check 5 the table is exactly the reachable set.
7. File structure:
   - layer headers for every L = 0..2n with the announced counts;
   - nothing after the last layer, and the gzip stream read to its end, so its CRC is checked;
   - total states equal to values.json certificate_states[n].
8. The top layer is exactly the initial state (g = 0, n pairs 2:0), with C_init = (2n)!/2^n. W_init/C_init must equal
   the values.json fraction, and that fraction must be in lowest terms.

The checker also prints a SHA-256 digest over (state, W) in file order, used for the determinism comparison.

## 2. Mutation tests (the checker is not vacuous)

The tests are negative_tests.py, negative_tests2.py and negative_tests3.py. They run on copies in
panel/reproduce_work/neg/, using the final checker version. Every mutation is REJECTED. Real messages, on n = 5:
- W+1 on an interior state: "W mismatch at '0|1:1,1:1,1:1,2:1,2:1|280': listed 280, recomputed 279".
- W-1 on an interior state: "listed 299, recomputed 300".
- W = 1 on a terminal state: "terminal state with W != 0".
- W+1 on the initial state: "listed 345499, recomputed 345498".
- A deleted state: "missing no-successor (C=19956)".
- A duplicated state: "duplicate state".
- Reversed pair order: "pairs not sorted ascending".
- A layer-1 state moved into layer 0: "has L=1, listed in layer 0".
- An inserted `0|2:2|0`: "C <= 0 for listed state".
- A truncated file: "premature EOF".
- A leading zero in W: "non-canonical".
- A g > 0 state with n active labels: "g > 0 with no exhausted label".
- A wrong claim given unreduced (57584/18900): "not in lowest terms".
- A wrong claim in lowest terms (57583/18901): "initial value 57583/18900 != claimed 57583/18901".

On n = 6:
- A deleted terminal state: "missing no-successor (C=12)".
- W+1 on a layer-1 state.
- W-1 on a layer-2 state.

An unmodified recompressed copy passes ("PASS n=6").

To exercise check 6 on its own, I made a copy of the checker with the "#pairs = n implies g = 0" test disabled. It
still rejects the inserted g > 0 state, with "1 states of layer 0 are not successors of any state of layer 1".
For n = 5, all 607 C > 0 terminal states are listed, so no other kind of valid unreachable state exists to insert.

## 3. Commands and real output (my checker)

The commands were run from panel/reproduce_work/, all under `nice -n 15`. Each run is one process handling one
certificate at a time, streaming two layers. The machine was heavily loaded by unrelated processes (load average
40-270), so the wall-clock times are inflated. For example, n = 16 needed 1,311 s of CPU but 4,761 s of wall time.

    python3 test_C.py
    python3 run_my_checker.py ../../claim 2 3 4 5 6 7 8 9 10 11 12 13 14     # log_my_n2_14.txt
    python3 run_my_checker.py ../../claim 15                                 # log_my_n15.txt
    python3 run_my_checker.py ../../claim 16                                 # log_my_n16.txt

| n | states (= values.json) | layers | actions (exhausted-label) | absent successors, C=0 | value W_init/C_init (= values.json) | wall time | max RSS |
|---|---|---|---|---|---|---|---|
| 2 | 21 | 5 | 27 (3) | 15 | 17/6 | 0.0 s | 12 MB |
| 3 | 118 | 7 | 194 (27) | 45 | 271/90 | 0.0 s | 12 MB |
| 4 | 496 | 9 | 968 (142) | 92 | 1279/420 | 0.0 s | 12 MB |
| 5 | 1727 | 11 | 3890 (574) | 156 | 57583/18900 | 0.0 s | 12 MB |
| 6 | 5311 | 13 | 13510 (1973) | 237 | 1136743/374220 | 0.1 s | 12 MB |
| 7 | 14903 | 15 | 42108 (6045) | 335 | 206528731/68108040 | 0.3 s | 13 MB |
| 8 | 38967 | 17 | 120575 (16974) | 450 | 61829276953/20432412000 | 1.0 s | 15 MB |
| 9 | 96163 | 19 | 322242 (44440) | 582 | 6298009733989/2084106024000 | 2.9 s | 19 MB |
| 10 | 226091 | 21 | 812989 (109825) | 731 | 170757866939041/56568592080000 | 9.8 s | 31 MB |
| 11 | 509906 | 23 | 1952906 (258485) | 897 | 137912544707079557/45735706696680000 | 29.6 s | 48 MB |
| 12 | 1109092 | 25 | 4496408 (583384) | 1080 | 228254911260131056513/75738330289702080000 | 92.6 s | 74 MB |
| 13 | 2336473 | 27 | 9975628 (1269386) | 1280 | 3901622163101296907981/1295524070744904000000 | 361.9 s | 147 MB |
| 14 | 4784071 | 29 | 21417878 (2674495) | 1497 | 28008675189200821587458897/9304453876089900528000000 | 908.0 s | 270 MB |
| 15 | 9548576 | 31 | 44659908 (5475723) | 1731 | 811893265752470943966781067/269829162406607115312000000 | 2846.6 s | 597 MB |
| 16 | 18623134 | 33 | 90710066 (10926476) | 1982 | 287519620950287971428538054033/95596617538340806567680000000 | 4760.6 s | 926 MB |

For n = 16, `time -l` also reports a peak memory footprint of 1,076,216,984 bytes.

Real output lines for the target range (the run for each n prints these, then `PASS n={n}`):

    n=11 m=2 states=509906 layers=23 actions=1952906 (exhausted-guess actions 258485, absent successors with C=0: 897)
      W_init=1654950536484954684 C_init=548828480360160000
      value=137912544707079557/45735706696680000 = 3.015423936088228510259641809668...
    n=12 m=2 states=1109092 layers=25 actions=4496408 (exhausted-guess actions 583384, absent successors with C=0: 1080)
      W_init=456509822520262113026 C_init=151476660579404160000
      value=228254911260131056513/75738330289702080000 = 3.013730437244220730560599717177...
    n=13 m=2 states=2336473 layers=27 actions=9975628 (exhausted-guess actions 1269386, absent successors with C=0: 1280)
      W_init=148261642197849282503278 C_init=49229914688306352000000
      value=3901622163101296907981/1295524070744904000000 = 3.011616882469757158399803419846...
    n=14 m=2 states=4784071 layers=29 actions=21417878 (exhausted-guess actions 2674495, absent successors with C=0: 1497)
      W_init=56017350378401643174917794 C_init=18608907752179801056000000
      value=28008675189200821587458897/9304453876089900528000000 = 3.010243864089224173899114668216...
    n=15 m=2 states=9548576 layers=31 actions=44659908 (exhausted-guess actions 5475723, absent successors with C=0: 1731)
      W_init=24356797972574128319003432010 C_init=8094874872198213459360000000
      value=811893265752470943966781067/269829162406607115312000000 = 3.008915932255774179574939772031...
      layer counts: 2604035 1930821 1421530 1038738 753294 541876 386621 273413 191654 133046 91482 62231 41901
                    27874 18339 11903 7632 4815 3000 1830 1101 644 371 205 112 57 29 13 6 2 1
    n=16 m=2 states=18623134 layers=33 actions=90710066 (exhausted-guess actions 10926476, absent successors with C=0: 1982)
      W_init=12075824079912094799998598269386 C_init=4015057936610313875842560000000
      value=287519620950287971428538054033/95596617538340806567680000000 = 3.007633830087898920929157204686...
      layer counts: 4966991 3707714 2750270 2026450 1483116 1077662 777411 556444 395202 278296 194346 134453 92187
                    62554 42039 27922 18356 11903 7632 4815 3000 1830 1101 644 371 205 112 57 29 13 6 2 1

For n = 2..14 the layer counts printed by my checker equal the `# L=` headers shown in the logs. The n = 16 counts
equal the header listing I took before checking.

Values, decimals and calibration. I checked the following with exact Fractions:
- Each values.json fraction is reduced and equals my W_init/C_init.
- Each decimal20 entry equals the exact value truncated to 20 decimals.

Four-decimal comparison with the DGS figures quoted in README.md and status/status_record.md (both conventions match
for n = 2, 3, 4, 5, 6, 8 and 9):

| n | exact value | rounded | truncated | DGS quoted |
|---|---|---|---|---|
| 7 | 3.0323693... | 3.0324 | 3.0323 | 3.0323 |
| 10 | 3.0185985... | 3.0186 | 3.0185 | 3.0186 |

Luo Prop. B.1, 17/6 for n = 2, is matched.

## 4. Cross-checks

**(a) My certificate-free solvers** (panel/reproduce_work/indep_solvers.py, written before reading solver/):
- `luo`: Luo's recursion exactly as written, on full label-indexed vectors (r, f). There is no canonicalisation and
  no g-merging. It uses Fractions, with p_i = C(r-e_i,f)/C(r,f) and C from the literal nested (A.1) sum. Results:
  - n=2: 17/6 (36 states);
  - n=3: 271/90 (540);
  - n=4: 1279/420 (7344);
  - n=5: 57583/18900 (94581).
- `brute`: the game itself. The guesser may name any label at any position and hears only yes/no. The recursion runs
  over the set of arrangements consistent with the history; no sufficient statistic is assumed. Results:
  - (2,2): 17/6 (6 arrangements);
  - (3,2): 271/90 (90);
  - (2,3): 41/10 (20);
  - (3,3): 2383/560 = 4.2553571429 (1680 arrangements). This rounds to the E(3,3,3) = 4.26 quoted in README.md, and
    equals the value REPRODUCE.md gives for the author's brute force.

**(b) The author's brute force.** Command: `python3 -I ../../claim/solver/bruteforce_raw_definition.py 3 2`, then the
same with `4 2`. Real output:

    n=3 m=2 words=90 memo_states=4558 P+=271/90 = 3.0111111111 time=0.1s
    n=4 m=2 words=2520 memo_states=1632553 P+=1279/420 = 3.0452380952 time=69.9s

Both equal values.json. The script uses the same design as my brute force: bitmask sets of words, memoised on
(t, S).

**(c) The author's checker**, run only after mine had run. The runner run_author_checker.sh executes
`python3 -I checker/verify_cert.py cert/n{n}.txt.gz --claimed <values.json>` from inside the claim folder. Results:

| n | states | actions | result |
|---|---|---|---|
| 2 | 21 | 27 | PASS |
| 3 | 118 | 194 | PASS |
| 4 | 496 | 968 | PASS |
| 5 | 1727 | 3890 | PASS |
| 6 | 5311 | 13510 | PASS |
| 7 | 14903 | 42108 | PASS |
| 8 | 38967 | 120575 | PASS |
| 9 | 96163 | 322242 | PASS |
| 10 | 226091 | 812989 | PASS |
| 11 | 509906 | 1952906 | PASS |
| 12 | 1109092 | 4496408 | PASS |
| 13 | 2336473 | 9975628 | PASS |

The values are identical to values.json, and the state and action counts are identical to mine. I did not run it for
n = 14..16 (optional; under this load it would take hours). Its logic matches mine: (A.1) grouped by K, absent
successor implies C = 0, the split identity, and one action per class plus the exhausted guess. It does not check
reachability, canonical number text, a lowest-terms claim or the values.json counts; my checker does.

**(d) Determinism.**
- My checker's (state, W) digests are identical between two separate runs: a first version on n = 2..13 and the
  final version on n = 2..16. For example, n = 13 gives 201ae4dcc9237a74... both times. Certificates are read
  identically and nothing in the check depends on hashing order.
- The author's solver was compiled with the clang++ command of REPRODUCE.md section 3, with output in
  panel/reproduce_work/rebuild/. `cg_solver {n} 2 n{n}_rebuilt.txt.gz` for n = 2..11 gives decompressed files whose
  SHA-256 equals that of `gzip -dc cert/n{n}.txt.gz`, all ten identical. Its printed value, states and actions equal
  values.json and my counts.

No object named in README.md is missing.

## 5. Re-derivation of the README proof steps

**(R1) What (A.1) counts, and the split C(s) = C(yes_i) + C(no_i).**

Each guessed position receives exactly one guess. So a failed position forbids exactly one label, and the positions
forbidding different labels are disjoint.

Make the r_i copies of label i distinguishable. Call a copy of label i lying on a position that forbids i a "bad
incidence". A set of bad incidences can occur together exactly when it is a partial matching. For label i, a
matching with k_i incidences is:
- a choice of k_i of its f_i forbidding positions: binom(f_i, k_i) ways;
- an injective assignment of copies to them: (r_i)_{k_i} ways.

Matchings for different labels never collide, because their positions and copies are disjoint. Each such set extends
to (M-K)! bijections. Inclusion-exclusion then gives

  sum_k (-1)^K (M-K)! prod_i binom(f_i, k_i) (r_i)_{k_i}

consistent bijections, and dividing by prod r_i! (the copies are really indistinguishable) gives (A.1). A label
with r_i = 0 admits only k_i = 0 and contributes the factor 1, so C depends on neither its f_i nor g. I confirmed
this count by enumeration on 1,330 random states.

Now suppose L >= 1, and let q be the next free position. Every consistent arrangement has exactly one label at q.
- Arrangements with label i at q correspond one-to-one to consistent arrangements of r - e_i on the other M - 1
  positions. Their number is C(r - e_i, f). If r_i - 1 = 0, (A.1) ignores f_i, which matches the fact that a position
  forbidding an absent label constrains nothing.
- Arrangements without label i at q are exactly those consistent with q forbidding i. Their number is C(r, f + e_i).

Hence C(r,f) = C(r - e_i, f) + C(r, f + e_i), that is, 1 - p_i = C(no_i)/C(s). For an exhausted i,
C(r, f + e_i) = C(r, f). This was verified by enumeration on 800 states, and asserted at all 153,161,345 active
actions of the 15 certificates.

**(R2) Why Luo's recursion is the game's value.**

For a fixed deterministic strategy, the observed history has likelihood 1 under every arrangement consistent with it
and 0 otherwise. With the uniform prior, the posterior is therefore uniform on the consistent arrangements.

After deleting the successfully guessed positions and their cards, three quantities depend only on (r, f):
- the number of consistent arrangements;
- the probability C(r - e_i, f)/C(r, f) that the next free position holds label i;
- the next state: (r - e_i, f) on "yes" and (r, f + e_i) on "no".

This holds because positions forbidding the same label are interchangeable. So the optimal expected future score is
a function of (r, f), it satisfies Luo's recursion, and it is 0 when no free position remains. The raw-arrangement
brute forces in section 4 assume none of this, and they agree.

**(R3) L = M - sum_active f - g, and every transition lowers L by one.**

The M undetermined positions fall into three groups:
- free positions: L of them;
- failed positions forbidding an active label: sum_active f_i of them;
- failed positions forbidding an exhausted label: g of them.

Effect of each transition on M, sum f and g:
- success on (2, f): M - 1, sum f and g unchanged, so L - 1;
- success on (1, f): M - 1, the pair is dropped (sum f - f) and g + f, so L - 1;
- failure: sum f + 1, so L - 1;
- an exhausted guess: g + 1, so L - 1.

The only state with L = 2n is the initial one. Labels never become active again and g grows only through exhausted
labels, so #pairs = n forces g = 0 on every reachable state.

**(R4) V+ is a function of (g, sorted active pairs), for fixed n.**

(a) Label symmetry. For a permutation sigma of the labels, (A.1) is invariant: re-index the k-vector. Hence:
- C(sigma r, sigma f) = C(r, f);
- p_{sigma(i)}(sigma s) = p_i(s);
- successors commute with sigma.

By induction on L, V+(sigma s) = V+(s). So V+ depends only on the multiset of pairs.

(b) Exhausted labels. If r_i = 0, then C and every p_j are independent of f_i (R1), and L sees such f_i only through
their sum g. Induction on L:
- If L = 0, V+ = 0.
- If L >= 1, there are two kinds of option:
  - An active label i. Here p_i depends only on the active pairs. Its successors are:
    - (g, (r_i,f_i) -> (r_i - 1, f_i)), or (g + f_i, pair removed) if r_i = 1;
    - (g, (r_i,f_i) -> (r_i, f_i + 1)).
  - An exhausted label. Here p = 0, and the only successor is (g + 1, same pairs), reached with probability 1.
- By the induction hypothesis every successor value is a function of its (g', pairs'). The available options depend
  only on the active pairs and on whether an exhausted label exists, which is the case iff #pairs < n.
- Labels with equal pairs give identical options, and all exhausted labels give the same option. So the max over
  i in [n] equals the max over one representative per class plus one exhausted guess (when #pairs < n). This is what
  both checkers evaluate.

Hence V+ = Phi_n(g, sorted active pairs), and the number of exhausted labels is n - #pairs.

**(R5) W = C V+ is an integer, and W = max [C(yes) + W(yes) + W(no)].**

For L >= 1 and C(s) > 0, (R1) gives p_i = C(yes_i)/C(s) and 1 - p_i = C(no_i)/C(s). Multiply Luo's recursion by
C(s) > 0. C(s) does not depend on i, so the maximiser is unchanged:

  C(s)V+(s) = max_i { C(yes)[1 + V+(yes)] + C(no) V+(no) } = max_i { C(yes) + W(yes) + W(no) },

where W(x) := C(x)V+(x) for listed x.
- A zero-probability branch is omitted in Luo's recursion. Its term is then 0, which matches C = 0 and an absent
  state.
- The exhausted option contributes W(g + 1, same pairs), since C is unchanged.

Integrality follows by induction on L: W = 0 at L = 0, and for L >= 1, W is a maximum of sums of integers. W(s) is
the optimal total score summed over the C(s) equally likely consistent arrangements.

**What the passing check proves.** By induction on L over the listed states, every listed W equals C V+:
- Base L = 0: W = 0 = C * 0.
- Step: every successor with C > 0 is listed (checked) and satisfies W = C V+ by the induction hypothesis. Every
  absent successor has C = 0 (checked) and contributes 0. So the listed W equals the right-hand side of (R5), which is
  C(s)V+(s).

Therefore P+_{2,n} = V+(init) = W_init/C_init, which is the values.json fraction for every n = 2..16. Check 6, plus
the completeness from check 5, shows the table is exactly the set of reachable states, as README claims.

## 6. Findings and caveats

- **F1 (README calibration note, documentation error).**
  - README.md, under "Comparison values", says that apart from n = 7 "every other entry agrees under rounding and
    truncation alike". This is false for n = 10: the exact 3.01859849539... truncates to 3.0185, not the published
    3.0186.
  - So, against the DGS figures as quoted, no single convention reproduces all nine entries. Under rounding, which
    DGS state, n = 7 differs by one unit in the fourth decimal (3.0324 vs 3.0323). Under truncation, n = 10 differs.
  - The exact n = 7 value is established here three ways: by my checker against Luo's recursion; by the definitional
    re-derivation (R2); and by the raw-game agreement for small decks. The one-unit difference is therefore on the
    published four-decimal side, or in its quotation; I did not fetch the paper.
  - This does not affect any certified value. Whether the calibration clause of the success criterion counts as met
    is for the criterion review; the README itself discloses the n = 7 point.
- **F2 (my own process deviation).**
  - A queue trigger of mine fired early: my first brute-force attempt failed on shell quoting and wrote "exit=" lines
    that met the trigger. As a result, from about 23:22 to 23:47 local time, three of my processes ran concurrently,
    all at nice 15. The third ran my n=5 and (3,3) solvers and the author's checker for n = 2..13. This exceeded the
    2-thread limit for about 25 minutes.
  - The author's checker reached 1.37 GB maximum RSS on n = 13. My n = 16 run (at most 395 MB at that point) and n = 15
    run (at most 258 MB) were running at the same time, so combined memory may briefly have neared 2 GB around 23:45.
  - Results are unaffected, and every other run respected the limits. The two long runs peaked at 926 MB (n = 16) and
    597 MB (n = 15).
- **F3 (load).** Wall-clock times are inflated by unrelated system load and say nothing about the claim.
- **No mismatch, missing object or non-determinism** was found in anything the claim asks to reproduce.

## 7. Verdict

Every state of every certificate cert/n2.txt.gz .. cert/n16.txt.gz was verified by my own checker. The checker was
written from the definition, uses my own exact (A.1), and recomputes the max over all labels from the table's own
successors. Every initial value equals the reduced fraction in values.json.

The README's proof steps hold as re-derived above. The author's brute force for (3,2) and (4,2) agrees, the author's
checker agrees for n = 2..13, and the author's solver reproduces cert/n2..n11 byte for byte.

The only discrepancy is F1, a misstatement in the README's comparison note about published four-decimal figures.
It does not touch the reproduced objects, and I flag it for the panel.

pass: true
