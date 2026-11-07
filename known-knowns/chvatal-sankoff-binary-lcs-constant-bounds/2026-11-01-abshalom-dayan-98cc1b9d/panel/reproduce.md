# REPRODUCE skeptic: gamma_2 >= 13332272/2^24 = 833267/1048576 = 0.794665336609

context: subagent

## Verdict

The certificate and the proof both hold up. My own checker, written from the definition, accepts all 242,084,334 states of object/ with exact integers (C1, C2, C3). It reports min E = 13332272, exactly the claimed m. All three shipped checkers agree. All negative controls reject, the sha256 values match, and I re-derived every proof step and found no gap.

Three items are outside what this folder can settle; they are listed under "Open items". The most important is that the folder shows no search for newer arXiv or Zenodo claims.

## Checker definition (quoted)

PROOF.md section 1:

> ROW: read a = a_{x+1}. Put F'_0 = F_0 and, for p = 0..N-1, F'_{p+1} = max(F_{p+1}, F'_p, F_p + m_p), where m_p = 1 if b_p = a, else 0.

> SHIFT: read c = b_{y+1}. New frontier (F_1, ..., F_N, F_N), new window (b_1..b_{N-1}, c) in positions 0..N-1. y and l increase by 1. Reward r = h_0 = F_1 - F_0.

PROOF.md section 5:

> (C1) (h = 0, b) is in S for every canonical b. (C2) S is closed: for s in S, canon of both successors under pi(s) are in S. (C3) for s in S with pi(s) = ROW: V(next_0) + V(next_1) - 2 V(s) >= m; for s in S with pi(s) = SHIFT, with r = h_0: 2 K r + V(next_0) + V(next_1) - 2 V(s) >= m.

I wrote the checker after reading PROOF.md and FORMAT.md and before opening any shipped code. How it works:
- **Successors:** it computes ROW successors from the max rule on absolute F values, and asserts the section 2 increment form on every call.
- **Lookups:** it uses dense per-window tables, not binary search.
- **Format checks:** it validates file sizes, h range and strict ascending order.
- **Arithmetic:** all sums are int64.

## Checker outputs (real)

My checker, full certificate:
```
N=17 K=16777216 m=13332272 total_states=242084334
rows=107272712 shifts=134811622 C1_starts=65536 Vmin=10073540 Vmax=217519211
minE=13332272 minE_row=13332272 minE_shift=13332277 tight_count=3 first_tight(h=32865,b=1,row=1) E_digest=34f4199d937b6c0e
violations_below_m=0
ACCEPT C1 C2 C3 on 242084334 states, m=13332272 K=16777216
```
The run took 7.64 s with a peak of 6.5 MB resident. A second run gave the same digest. That second run came after I added the in-memory control code, and it used the same accept path.

My checker on the small certificates in object/small/:
| N | states | min E | result |
|---|---|---|---|
| 3 | 15 | 12326115 | ACCEPT, equals stated m |
| 4 | 36 | 12621691 | ACCEPT, equals stated m |
| 5 | 159 | 12776965 | ACCEPT, equals stated m |
| 8 | 5530 | 13020558 | ACCEPT, no m given in FORMAT.md |

Shipped checkers, built and run per REPRODUCE.md:
```
check_a17: N=17 states=242084334 row_action_states=107272712 K=16777216 min_E=13332272 Vmin=10073540 Vmax=217519211
           ACCEPT claimed m=13332272, L=m/K=13332272/16777216=0.794665336609
check_d:   rowStates=107272712 shiftStates=134811622; minE=13332272 (attained by 3 states, first index 4751); failures: structure=0 C1=0 C2=0 C3=0
           ACCEPT m=13332272 K=16777216
check_e:   statesWithE=242084334 minE=13332272 sumE=3227536924871139 meanE=13332283.306160 violations C1=0 C2=0 C3=0
           ACCEPT m=13332272 K=16777216
```
All four checkers agree on the state count, the action split, min E and the tight state (b=1, h=32865). The checkers that report them also agree on Vmin and Vmax, and on the count of 3 tight states. These are ROW states; the other two are h=32913 and h=33041 at b=1.

Peak resident memory: check_a17 1,696.9 MB, check_d 69.6 MB, check_e 3.4 MB. REPRODUCE.md says "a few MB" for check_d, which is a small understatement.

### Negative controls on c17

All 12 rejected, each with exit 1.

| control | check_a17 | check_d | check_e | mine |
|---|---|---|---|---|
| m + 1 | REJECT min_E 13332272 < 13332273 | REJECT, C3=3 | REJECT, C3=3 | REJECT, 3 below m |
| perturb (V + 1 at tight state) | REJECT min_E 13332271 | REJECT, C3=1 | REJECT, C3=1 | REJECT, min E 13332271 |
| drop (middle state 121042167) | REJECT, closure at b=37999 h=27126, next 91126 missing | REJECT, same state | REJECT, same state | REJECT, same state |

### Mutation test of my checker on N = 4, 5 (rejected/accepted)

| fault | N=4 | N=5 |
|---|---|---|
| policy flip | 34/2 | 139/20 |
| h bit 0 flip | 36/0 | 159/0 |
| h high bit set | 36/0 | 159/0 |
| V + 1 | 8/28 | 28/131 |
| drop state | 36/0 | 159/0 |
| truncate states | 1/0 | 1/0 |
| truncate V | 1/0 | 1/0 |
| extra V | 1/0 | 1/0 |
| m + 1 | 1/0 | 1/0 |

The accepted cases are expected but were not separately confirmed:
- **V + 1:** this passes on states with slack in C3 and in their predecessors.
- **Policy flip:** acceptance means C1 to C3 still hold for the flipped policy, which would be a valid certificate under the same proof. I did not confirm those mutants with a second checker.

### Hashes and arithmetic

- **sha256:** matches REPRODUCE.md before and after all runs: c17.counts 46f3504c..., c17.states b35375dd..., c17.V 6016451b... (full values compared).
- **File sizes:** counts 262144 = 4 x 2^16; states 726253002 = 3 x 242084334; V 968337336 = 4 x 242084334.
- **Exact fractions:** 13332272/2^24 = 833267/1048576 = 0.7946653366...
- **Margins:** it beats the 0.792665992 bar by 0.00199934 and the frozen 0.7939155565 threshold by 0.00074978. Both exceed 1e-6.
- **Determinism:** repeated runs of each checker gave identical figures.

## Proof steps

Each step was re-derived by hand; the tests add evidence on small cases.

| step | content | verdict | evidence |
|---|---|---|---|
| Fekete sup | gamma_2 = sup E L(n,n)/n | CONFIRMED | Concatenation gives superadditivity and the sequence is bounded by 1. Exact for m + n <= 8. |
| 1 | Reward sum telescopes to F_0(t) | CONFIRMED | SHIFT moves F_1 to F_0; ROW keeps F_0. |
| 2 | Increment form in {0,1} | CONFIRMED | The three max terms are F_p + h_p, F_p + v_p, F_p + m_p. Exhaustive for N <= 9 (699,048 cases), and asserted on every ROW call in the full c17 run. |
| 3 | F_p <= L(x, l+p) | CONFIRMED | Induction holds, including p = N on SHIFT. All 262,144 string pairs of length 9 for N = 3, 4, 5, 8 had 0 violations. tests/exact_small.py had 0 violations at T = 12. |
| 4 | Complement symmetry | CONFIRMED | Row(h, not b, not a) = Row(h, b, a) and the SHIFT analogue, exhaustive for N <= 9. Real-string runs use raw windows with canon lookups. |
| 4 | Markov property, uniform next character | CONFIRMED | The next index depends only on characters already read, and that character is unread. E R_T over all real string pairs equals the forward-chain value exactly, as Fractions (1.578125, 1.5, 1.0078125 for N = 3, 4, 5). |
| 5 | C1, C2, C3 | CONFIRMED | Four checkers over all states, as above. |
| 6 | Telescoping | CONFIRMED | Exact Fractions for every T up to 200 on N = 3, 4, 5, including the bound E R_T >= T m/(2K) - 2 V_max/K. |
| 7, Lemma 1 | E L(x,y) <= n gamma_2/2 | CONFIRMED | Concatenating A_x A'_y with B_y B'_x and exchangeability give it. Exact 2 E L(x,y) <= E L(n,n) for all x + y = n <= 8. tests/lemma1_small.py passes. |
| 7, Lemma 2 | E max <= n gamma_2/2 + sqrt(n ln n) + 2 | CONFIRMED | McDiarmid with difference 1 over n characters gives exp(-2 ln n) = 1/n^2. The union over n + 1 pairs gives (n+1)/n^2, and the bad event costs at most n times that. Bounded differences and tails checked exhaustively for n <= 8, and E max is well inside the stronger form with E L(n,n)/2. |
| 7, limit | m/K <= gamma_2 | CONFIRMED | R_T <= L(x_T, y_T) <= max over x + y = N + T holds for every outcome, so random x_T, y_T are covered. Dividing by T, the V_max and square-root terms vanish. |

Limits of these tests:
- **N = 8 real-string run:** it has T = 1 at n = 9, so it is nearly vacuous.
- **N > 5 for step 3:** the evidence is sampled: tests/sim_check.py at N = 8, and my N = 17 runs. Those are spot checks of the proof logic, not of the certificate, whose check is exhaustive.
- **Formal status:** the re-derivation is by hand, with no formal proof assistant.

### Shipped small-case tests (all exit 0)

| test | result |
|---|---|
| tests/exact_small.py, N = 3 | gain 2rho = 0.7346938776 >= m/K = 0.7346937060 |
| tests/exact_small.py, N = 4 | 2rho = 0.7523116270 >= 0.7523114085 |
| tests/exact_small.py, N = 5 | 2rho = 0.7615666640 >= 0.7615664601 |
| tests/sim_check.py, N = 8 | no violation in 12,000 steps; rate2 0.77567, true rate 0.80929 |
| tests/lemma1_small.py | holds |
| tests/sim_rate17.c | 2R/T = 0.794670 over 2e8 steps |

## Simulation reading (numerical only, not evidence for the bound)

My own simulator on c17, real strings with a plain LCS DP, T = 60000:
```
seed=12 x=30634 y=29383 checkpoints=30 violations=0 min_slack=11 2R/T=0.79457 L(x,y)=24340 2L/(x+y)=0.81110
seed=13 x=30724 y=29293 checkpoints=30 violations=0 min_slack=13 2R/T=0.79370 L(x,y)=24295 2L/(x+y)=0.80960
```

**The low reading.** My first long rate run gave 2R/T = 0.794643 with stderr 0.000014 over 3e8 steps, which is 1.6 standard errors below m/K. I did not assume it was noise, and ran two further checks:
- **Fresh seeds, 1e9 steps each:** 0.794655 (se 0.000010) and 0.794667 (se 0.000008). These straddle m/K.
- **Martingale control:** K R_T + V(s_T) - V(s_0) - sum E(s_t)/2 has mean zero. Results at 2e8 steps:
```
seed=31 2R/T=0.7946536 se=0.0000194 meanE/K=0.794665962 minE_visited=13332275 residual=-1.228e-05 z=-0.63
seed=32 2R/T=0.7946922 se=0.0000237 meanE/K=0.794665962 minE_visited=13332275 residual=2.628e-05 z=1.11
```

**Resolution: noise.**
- My five long runs pool to about 0.794661 over 2.7e9 steps, roughly 0.8 standard errors below the low-noise gain estimate of 0.79466596. That gain estimate is above m/K. The pooled figure is hand-computed from batch stderrs that are themselves rough.
- No visited state fell below m. The three tight states were not visited in those 4e8 steps.

## Dead lines

Each hypothesis I tried ended without finding a fault. Guessed chances and actions are in NOTES.md in my work folder (14 hypotheses).

- **Model mismatch.** Checkers encoding a process other than the proved one: dead. The max-rule checker and real-string LCS comparison agree with it.
- **Information leak.** The adaptive policy leaking future characters: dead. Chain and string expectations are exactly equal.
- **Reward overcount.** Reward exceeding a real common subsequence: dead.
- **Normalization.** Reading unequal amounts of A and B inflating the rate: dead. Lemmas 1 and 2 handle it, and rows are about 51.1% of steps.
- **Complement boundary.** Symmetry failing at SHIFT: dead.
- **File tricks.** Unsorted entries, high bits, trailing bytes: dead. All rejected, with no binary-search dependence in my checker.
- **Overflow.** Dead. Vmax is 217,519,211 and sums are int64.
- **Closure on a sub-block only** (imported from statistical physics): dead. C2 was checked on every state.
- **Optimizer-created spurious accept** (imported from compilers): not seen. Four separate programs agree, and m + 1 rejects exactly at min E + 1.
- **Optional-stopping failure** (imported from martingale theory): dead. T is fixed, V is bounded, and the union bound covers random x_T, y_T.
- **Hard-linked files changing mid-run** (strange): dead. The files have link count 2, but hashes are identical before and after.
- **Last column undercounting** (strange): harmless. Undercounting only lowers the reward.
- **Low simulation reading:** resolved as noise, above.

## Open items

These do not change my result on the mathematics, but they are outside it.

1. **Bar freshness and arXiv.**
   - The saved records are consistent: the table/ hashes match table/scout.md, the page's rigorous lower bar is 0.792665992, 0.79970 is labeled Monte Carlo, Zenodo record v5 covers upper bounds, and no open PR changes the binary lower bound by my keyword scan.
   - I had no web access.
   - table/scout.md lists no search for newer arXiv or other Zenodo claims, which the criterion requires. That needs doing at the gate.
   - data/v3_pulls.json is cited in table/scout.md but is not in this folder, so that row is unverifiable here.
2. **Reading of the criterion.** It asks lower bounds for "the finite-length computation with exact or outward-rounded arithmetic". This is an exact-integer potential certificate plus an infinite-horizon proof, not a finite-length value of E L(n,n). I judge it rigorous, but whether it fits that wording is for the panel.
3. **Not verified here.**
   - The certificate was not rebuilt. Its validity does not depend on the producer.
   - The PREREG N = 16 byte-for-byte regression and the claim that it was written before N = 17 output cannot be checked from this folder.
   - I read only rebuild/mdp3.c among the producer sources, and not rebuild/prod4.c.
   - I did not compare object/small_old/ with object/small/ byte for byte.

Documentation slips, with no effect on the result:
- FORMAT.md says testvec/, but the files are in object/small/.
- table/scout.md says data/, but the files are in table/.

## Run notes

- No tool-guard or classifier block and no HTTP 401, 403 or 429 occurred.
- **Memory limit, possible brief overrun:** check_a17 alone peaks at 1,696.9 MB. While the first shipped queue was running, I also ran small commands (compiles, a short Python status read), so my total may have briefly passed 1.7 GB by a few MB during those check_a17 runs. I did not measure that total. Other runs stayed far below the limit; sim17m peaked near 711 MB.
- All processes I started have ended, and claim/ was not modified.

pass: true
