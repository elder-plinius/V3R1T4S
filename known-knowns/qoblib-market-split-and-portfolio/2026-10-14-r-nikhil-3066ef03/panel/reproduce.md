# REPRODUCE skeptic verdict: cell a200_t10_orig_b050_l1e-02

context: subagent (Claude Code Agent tool, fresh context, model opus)

Claim under test (`CLAIM.md`): `solution/a200_t10_orig_b050_l1e-02_solution.sol` is feasible for QOBLIB class 06
instance `po_a200_t10_orig` with B = 50 and lambda = 0.01, and its exact objective under `definition/bqp_u3_c10.zpl`
with `definition/parameter_u3_c10.zpl` (minimised) is -691624.

Order of work: I read `CLAIM.md`, `REPRODUCE.md`, `STATUS_RECORD.md`, all of `definition/` and the `.sol` files, treating
them as data. Then I wrote my own checker from the definition and ran it on both positives, ten negatives and the claim
(twice). Only after that did I open and run `checker/pf_eval.py`. I used only `python3 -I` and the standard
library (`fractions`, `gzip`, `math`, `re`) and fetched nothing. A usage-limit pause interrupted the session once,
after all checks had run. On resuming I re-hashed the claim folder (unchanged) and ran my checker on the claim a third
time (byte-identical output).

## 1. Integrity of the package

- All 12 sha256 values in the `CLAIM.md` file table match the files. That includes
  `solution/a200_t10_orig_b050_l1e-02_solution.sol` =
  `3066ef033d46c6e8fdb38d20f562a6e5ff41b67e4b64881c9988a67fdfe58097`.
- The three `.sol` files are pure ASCII, with no CR bytes.
- My parser found the instance complete: 200 symbols x 10 days (0..9) of prices, 400000 = 200 x 200 x 10 covariance rows,
  and no duplicate keys.
- I hashed the claim folder before and after running the author's checker, and again after the pause. Nothing changed
  and no files were added.

## 2. Definition parts I implemented (verbatim quotes)

From `definition/parameter_u3_c10.zpl`:

```
param time_intervals    := 10;  # Default t (overwritten by -Dt=... if desired)
param cash      := 1000000;
param unit      := 100000;
param delta     := 0.001;
param nu        := 0.0001;
param rho       := 0.000025;
param ub        := 3;
param lambda    := 1;
param upscale   := 1;
param B := 50;
param t_beg := 0;
param t_end := t_beg + time_intervals - 1;
param C := cash / unit;
set T               := { read stock_price as "<1n>" comment "#" };
set S               := { read stock_price as "<2s>" comment "#" };
param raw_p[S*T]    := read stock_price as "<2s,1n> 3n" comment "#";
param cov[S*S*T]    := read stock_covariance as "<2s,3s,1n> 4n" comment "#";
param ucnt[<s> in S] := unit / raw_p[s,t_beg];
param p[<s,tt> in S*T] := raw_p[s,tt] * ucnt[s];
set CS1 := { 0 .. 3 };
set CS2 := { 0 .. 6 };
set TX  := { t_beg .. t_end };
set SC  := { 1 .. ub };
set SL  := { 1, -1 };
set SX  := S * SC * SL;
var x[SX*TX]   binary;
var y[CS1*TX] binary;
var s2[CS2*TX] binary;
```

(`num_assets` and `rho_p` are declared but never used by the model. `lambda` is replaced by the variant's 0.01, per the
check README: "Only $B$ (budget, encoded as `bXXX` in model names) and $\lambda$ (risk weight, `lX`) vary between model
variants; all other parameters are fixed.")

From `definition/bqp_u3_c10.zpl` (objective and both constraints, complete):

```
minimize risk:
   upscale * (
      sum <t> in TX : (
         sum <i,m,tau_i,j,n,tau_j> in SX * SX : (
            round(lambda * tau_i * tau_j * cov[i,j,t] * p[i,t] * p[j,t]) 
            * x[i,m,tau_i,t] * x[j,n,tau_j,t]
         ) # risk
         - sum <k> in CS1 : round(nu * unit * 2^k) * y[k,t]  # cash interest
         + sum <i,m,-1> in SX : round(rho * p[i,t]) * x[i,m,-1,t]  # short sell cost
      )
      + sum <t> in TX \ { t_beg, t_end } : (
         - sum <i,m,tau> in SX : (
            round(tau * (p[i,t+1] - p[i,t])) * x[i,m,tau,t]  # return
            - round(delta * p[i,t]) * (x[i,m,tau,t-1] + x[i,m,tau,t]
                                - 2 * x[i,m,tau,t-1] * x[i,m,tau,t])  # transaction cost
         )
      )
      - sum <i,m,tau> in SX : (
         round(tau * (p[i,t_beg+1] - p[i,t_beg])) * x[i,m,tau,t_beg]  # return for the first day
         - round(delta * p[i,t_beg]) * x[i,m,tau,t_beg]  # transaction cost for the first day
      )
      + sum <i,m,tau> in SX : round(delta * p[i,t_end]) * x[i,m,tau,t_end]  # transaction cost for the last day
   )
;

subto c2:
   forall <t> in TX :
      sum <i,m,tau> in SX : tau * x[i,m,tau,t] + sum <c> in CS1 : 2^c * y[c,t] == C;

subto c3:
   forall <t> in TX :
      sum <i,m,tau> in SX : x[i,m,tau,t] + sum <c> in CS2 : 2^c * s2[c,t] == B;
```

From `definition/06-portfolio-check-README.md` (format, mapping, rounding):

> * `long units` and `short units` are integers in $\{0,\dots,ub\}$ (default
>   $ub = 3$): the number of unit copies held long resp. short.
> * At most one line per (period, symbol); omitted pairs hold no position.

> A count vector corresponds to the canonical assignment that fills
> copies $1,\dots,u$, under which the rebalancing cost between consecutive
> periods is $\delta\, p_{i,t}\, |u_{i,\tau,t} - u_{i,\tau,t-1}|$ per (asset,
> direction) — the minimum over all slot assignments realizing the same counts.

> Slack registers are **not** part of the format: they are uniquely determined
> by the positions and are validated and priced (cash interest) by the checker.

> Every coefficient is rounded exactly like Zimpl's `round()`
> (round half away from zero on exact rationals)

## 3. My reading (fixed before I opened the author's code)

- **Data.** Every number in the gzip files is converted exactly from its decimal string to a rational. For example,
  `1.371584238929106e-05` becomes 685792119464553/50000000000000000000. Then
  p[s,t] = raw_p[s,t] * (unit / raw_p[s,0]), so p[s,0] = 100000 exactly. TX = {0..9} matches the instance's days.
- **Counts to binaries.** A line `t s L S` sets x[s,m,+1,t] = 1 for m = 1..L and x[s,m,-1,t] = 1 for m = 1..S. This
  is the canonical fill, copy 1 first. Every other x[.,.,.,t] is 0, and unlisted (t, s) pairs are all zero.
- **Slack bits.** y[c,t] is bit c of C - net_t, and s2[b,t] is bit b of B - total_t, where net_t = sum tau*x and
  total_t = sum x. A binary expansion exists, and is then unique, exactly when 0 <= C - net_t <= 15 and
  0 <= B - total_t <= 127. That means c2 requires -5 <= net_t <= 10 and c3 requires total_t <= 50 in every period.
  After building the bits, I re-checked c2 and c3 literally as equalities on the full binary point (x, y, s2).
- **round().** sign(q) * floor(|q| + 1/2) on the exact rational q, i.e. round half away from zero, as the check README
  states. My checker also lists every exact tie it meets (section 7).
- **Objective.** I evaluated it literally, term by term, at that binary point. Risk runs over every ordered pair of set
  variables, including a variable paired with itself (x*x = x); all other terms vanish. Read literally, the model:
  - counts return only for t = 0..8;
  - charges transaction cost as the buy-in at t = 0, then the XOR term for t = 1..8 (rebalancing 0->1 ... 7->8) priced
    at p[i,t], then the liquidation of positions held at t_end = 9;
  - does not charge the 8->9 rebalancing at all (`TX \ { t_beg, t_end }`);
  - prices cash interest at round(nu*unit*2^k) = 10*2^k per set bit, i.e. 10*(C - net_t) per period.

  The LaTeX formula in `definition/06-portfolio-README.md` sums all terms over t = 1..T. I followed the ZIMPL file,
  which the check README names as the reference model. Section 7 shows that the posted bar values pin down this reading.
- **Cross-check A.** An independent count formula inside the same checker: per ordered asset pair,
  round(lambda*cov*p*p)*net_i*net_j; transaction costs as delta-coefficients times |du|. It must agree with the
  literal evaluation exactly.
- **Diagnostics.** Each round() argument is also computed in IEEE double arithmetic. The checker counts exact ties
  and near-ties and prints the objective under other tie rules.

My checker is a single standard-library script kept in my work folder, outside the claim package
(sha256 `ac21d9ac56e61d47c12c1c48b8e5d8edff0cd4367c60438249289cf8befc68db`).

## 4. Known positives (my checker)

`bar/PR87_a200_t10_orig_b050_l1e-02_solution.sol` (posted -551385):

```
instance po_a200_t10_orig: 200 assets, 10 periods; B=50 lambda=1/100; C=10 ub=3 slack bits 4+7
t= 0: net=  -2 total=  50 cash_slack=  12 count_slack=   0  ok
t= 1: net=  -2 total=  50 cash_slack=  12 count_slack=   0  ok
t= 2: net=   0 total=  50 cash_slack=  10 count_slack=   0  ok
t= 3: net=  -4 total=  50 cash_slack=  14 count_slack=   0  ok
t= 4: net=  10 total=  50 cash_slack=   0 count_slack=   0  ok
t= 5: net=  -2 total=  50 cash_slack=  12 count_slack=   0  ok
t= 6: net=   4 total=  50 cash_slack=   6 count_slack=   0  ok
t= 7: net=  -4 total=  50 cash_slack=  14 count_slack=   0  ok
t= 8: net=  -3 total=  49 cash_slack=  13 count_slack=   1  ok
t= 9: net=   0 total=   0 cash_slack=  10 count_slack=  50  ok
breakdown (literal ZIMPL evaluation on the binary point):
  risk                  65873
  return              -693306
  transaction           76537
  cash interest         -1030
  short cost              541
  liquidation               0
objective (main: exact rationals, round half away from zero) = -551385
objective (cross-check A: count formula, exact) = -551385
diag: round() arguments that are exact half-integers: 26 term(s); by (kind, period, value): [(('short', 0, '5/2'), 26)]
diag: min distance of a non-tie round() argument to a half-integer = 2.36466e-05 (('risk', 4))
diag: coefficients whose IEEE-double rounding differs from exact rounding: 4; all at exact ties: True
diag: objective with tie rule half-to-even = -551411; floor(x+1/2) = -551385; IEEE-double coefficients = -551389
claimed objective -551385 matches
FEASIBLE, objective = -551385
exit 0
```

`bar/PR64_a200_t10_orig_b050_l1e-02_solution.sol` (posted -300647). This file also exercises period-9 holdings
(liquidation term) and simultaneous long and short in one asset:

```
instance po_a200_t10_orig: 200 assets, 10 periods; B=50 lambda=1/100; C=10 ub=3 slack bits 4+7
t= 0: net=   0 total=  50 cash_slack=  10 count_slack=   0  ok
t= 1: net=   0 total=  50 cash_slack=  10 count_slack=   0  ok
t= 2: net=   2 total=  50 cash_slack=   8 count_slack=   0  ok
t= 3: net=  -2 total=  50 cash_slack=  12 count_slack=   0  ok
t= 4: net=   8 total=  50 cash_slack=   2 count_slack=   0  ok
t= 5: net=  -2 total=  50 cash_slack=  12 count_slack=   0  ok
t= 6: net=   0 total=  50 cash_slack=  10 count_slack=   0  ok
t= 7: net=   0 total=  50 cash_slack=  10 count_slack=   0  ok
t= 8: net=   0 total=  50 cash_slack=  10 count_slack=   0  ok
t= 9: net=   0 total=  32 cash_slack=  10 count_slack=  18  ok
breakdown (literal ZIMPL evaluation on the binary point):
  risk                  48706
  return              -422571
  transaction           70489
  cash interest          -940
  short cost              545
  liquidation            3124
objective (main: exact rationals, round half away from zero) = -300647
objective (cross-check A: count formula, exact) = -300647
diag: round() arguments that are exact half-integers: 25 term(s); by (kind, period, value): [(('short', 0, '5/2'), 25)]
diag: min distance of a non-tie round() argument to a half-integer = 2.36466e-05 (('risk', 4))
diag: coefficients whose IEEE-double rounding differs from exact rounding: 1; all at exact ties: True
diag: objective with tie rule half-to-even = -300672; floor(x+1/2) = -300647; IEEE-double coefficients = -300648
claimed objective -300647 matches
FEASIBLE, objective = -300647
exit 0
```

## 5. Known negatives (constructed variants of the claimed file, kept outside the claim package)

All are rejected by my checker. The author's checker results (run later) are shown alongside.

| case | construction | my checker | `checker/pf_eval.py` |
|---|---|---|---|
| N1 over budget | claim + line `0 AAPL 1 1` (period 0: total 52 > B = 50, net unchanged) | exit 21: `t= 0: net=   0 total=  52 cash_slack=  10 count_slack=  -2  VIOLATED / REJECT: capital (c2) or budget (c3) constraint violated` | exit 21: `INFEASIBLE` |
| N2 net above C | `4 TSLA 0 3` -> `4 TSLA 3 0` (period 4: net 16 > C = 10) | exit 21: `t= 4: net=  16 total=  50 cash_slack=  -6 count_slack=   0  VIOLATED / REJECT: capital (c2) or budget (c3) constraint violated` | exit 21: `INFEASIBLE` |
| N3 net below C-15 | `3 META 3 0` -> `3 META 0 3` (period 3: net -10 < -5) | exit 21: `t= 3: net= -10 total=  50 cash_slack=  20 count_slack=   0  VIOLATED / REJECT: capital (c2) or budget (c3) constraint violated` | exit 21: `INFEASIBLE` |
| N4 count above ub | `0 HD 0 3` -> `0 HD 0 4` | exit 10: `REJECT: line 9: unit count above ub=3` | exit 10: `MALFORMED: unit count outside 0..3 at (0, 'HD')` |
| N5 negative count | `0 NVDA 0 1` -> `0 NVDA -1 1` | exit 10: `REJECT: line 7: non-integer field '0 NVDA -1 1'` | exit 10: `MALFORMED: unit count outside 0..3 at (0, 'NVDA')` |
| N6 duplicate pair | claim + second line `0 NVDA 0 1` | exit 10: `REJECT: line 293: duplicate (period, symbol) 0 NVDA` | exit 10: `MALFORMED: duplicate position line for (0, 'NVDA')` |
| N7 unknown symbol | claim + line `0 ZZZZ 1 0` | exit 10: `REJECT: line 293: unknown symbol 'ZZZZ'` | exit 10: `MALFORMED: position (0, ZZZZ) outside the instance` |
| N8 period out of range | claim + line `10 AAPL 1 0` | exit 10: `REJECT: line 293: period 10 out of range` | exit 10: `MALFORMED: position (10, AAPL) outside the instance` |
| N9 malformed line | claim + line `0 AAPL 1` | exit 10: `REJECT: line 293: malformed (3 fields): '0 AAPL 1'` | exit 10: `MALFORMED: malformed line '0 AAPL 1'` |
| N10 wrong claimed objective | header `objective -691624` -> `objective -691625` | exit 10: `REJECT: claimed objective -691625 != recomputed -691624` | exit 10: `CLAIMED OBJECTIVE MISMATCH: claimed -691625, recomputed -691624` |
| N11 budget override | unchanged claim file run with `--budget 49` | exit 21: `t= 0: net=   0 total=  50 cash_slack=  10 count_slack=  -1  VIOLATED / REJECT: capital (c2) or budget (c3) constraint violated` | exit 21: `INFEASIBLE` |

## 6. The claimed solution (my checker)

`python3 -I` my checker, `instance/po_a200_t10_orig` `solution/a200_t10_orig_b050_l1e-02_solution.sol`:

```
instance po_a200_t10_orig: 200 assets, 10 periods; B=50 lambda=1/100; C=10 ub=3 slack bits 4+7
t= 0: net=   0 total=  50 cash_slack=  10 count_slack=   0  ok
t= 1: net=  -2 total=  50 cash_slack=  12 count_slack=   0  ok
t= 2: net=  -2 total=  50 cash_slack=  12 count_slack=   0  ok
t= 3: net=  -4 total=  50 cash_slack=  14 count_slack=   0  ok
t= 4: net=  10 total=  50 cash_slack=   0 count_slack=   0  ok
t= 5: net=   0 total=  50 cash_slack=  10 count_slack=   0  ok
t= 6: net=   0 total=  50 cash_slack=  10 count_slack=   0  ok
t= 7: net=  -4 total=  50 cash_slack=  14 count_slack=   0  ok
t= 8: net=  -2 total=  50 cash_slack=  12 count_slack=   0  ok
t= 9: net=   0 total=   0 cash_slack=  10 count_slack=  50  ok
breakdown (literal ZIMPL evaluation on the binary point):
  risk                  58939
  return              -825237
  transaction           75179
  cash interest         -1040
  short cost              535
  liquidation               0
objective (main: exact rationals, round half away from zero) = -691624
objective (cross-check A: count formula, exact) = -691624
diag: round() arguments that are exact half-integers: 25 term(s); by (kind, period, value): [(('short', 0, '5/2'), 25)]
diag: min distance of a non-tie round() argument to a half-integer = 0.000182319 (('risk', 6))
diag: coefficients whose IEEE-double rounding differs from exact rounding: 3; all at exact ties: True
diag: objective with tie rule half-to-even = -691649; floor(x+1/2) = -691624; IEEE-double coefficients = -691627
claimed objective -691624 matches
FEASIBLE, objective = -691624
exit 0
```

Determinism: three runs (two before the pause, one after) produced byte-identical output, sha256 of the output
`5f9029cfdb969419bb5d95d2c8d8138a8d8b816eaaedd5e743374bac2fac2f89`. The recomputed objective -691624 equals the file header's `objective -691624` and the value in
`CLAIM.md`. Feasibility holds in every period t = 0..9.

## 7. Rounding sensitivity and alternative readings

- **The tie-breaking rule matters here.** Every exact tie among the coefficients actually used is the t = 0 short cost.
  Because p[i,0] = unit, round(rho*p[i,0]) = round(0.000025*100000) = round(5/2). The claimed file has 25 such terms;
  PR87 has 26 and PR64 has 25.
  - Under the definition's rule (half away from zero) each tie is 3. floor(x+1/2) gives the same.
  - Half-to-even would give -691649 for the claim, -551411 for PR87 and -300672 for PR64.
  - Computing the coefficients in IEEE double gives -691627 for the claim and -551389 for PR87, because the double p[i,0]
    lands just on either side of 100000.
  - Both third-party bar values reproduce exactly only under the definition's rule.
- **No other coefficient is fragile.** Every other used round() argument is at least 1.8e-4 (claim) or 2.4e-5 (bars)
  from a half-integer, and every float/exact disagreement falls on an exact tie.
- **The claim stays below the bar under every variant:** -691649 vs -551411, and -691627 vs -551389.

Alternative (wrong) readings, as changes to each file's value:

```
bar/PR87_a200_t10_orig_b050_l1e-02_solution.sol: (a) charge 8->9 rebalancing: +4764   (b) tc at p[t-1]: +262   (c) one round() per period for risk: -63
bar/PR64_a200_t10_orig_b050_l1e-02_solution.sol: (a) charge 8->9 rebalancing: +7437   (b) tc at p[t-1]: +243   (c) one round() per period for risk: +11
solution/a200_t10_orig_b050_l1e-02_solution.sol: (a) charge 8->9 rebalancing: +4813   (b) tc at p[t-1]: +253   (c) one round() per period for risk: +268
```

(a) charges the 8->9 rebalancing; (b) prices the transaction cost at p[t-1]; (c) rounds risk once per period instead of
per ordered pair. Each would move both third-party bar values off their posted numbers, so the posted numbers fix the
literal reading I implemented. Under (a), for instance, the claim would be -686811 against PR87's -546621, still
strictly better.

## 8. Author's checker (`checker/pf_eval.py`), run as in `REPRODUCE.md`

I read the code only after section 6 existed. Its model reading matches mine on every point:
- the same round() rule;
- p = raw_p * unit / raw_p[t_beg];
- risk per ordered (asset, direction) pair times the count product;
- return for t < t_end;
- buy-in at t_beg, |du| rebalancing for t_beg < t < t_end, liquidation only at t_end;
- cash interest from the binary expansion of the cash slack.

It validates less than my checker. It takes the days from the file, does not check that the instance is complete or free
of duplicate rows, and does not reject unknown header keys. None of that affects this cell, whose instance my parser
validated. The code only reads files and prints.

`python3 -I checker/pf_eval.py instance/po_a200_t10_orig solution/a200_t10_orig_b050_l1e-02_solution.sol` (exit 0):

```
instance po_a200_t10_orig: 200 assets, 10 periods; B=50 lambda=1/100
t= 0 net=  0 total= 50 cash_slack=10 count_slack=0 ok
t= 1 net= -2 total= 50 cash_slack=12 count_slack=0 ok
t= 2 net= -2 total= 50 cash_slack=12 count_slack=0 ok
t= 3 net= -4 total= 50 cash_slack=14 count_slack=0 ok
t= 4 net= 10 total= 50 cash_slack=0 count_slack=0 ok
t= 5 net=  0 total= 50 cash_slack=10 count_slack=0 ok
t= 6 net=  0 total= 50 cash_slack=10 count_slack=0 ok
t= 7 net= -4 total= 50 cash_slack=14 count_slack=0 ok
t= 8 net= -2 total= 50 cash_slack=12 count_slack=0 ok
t= 9 net=  0 total=  0 cash_slack=10 count_slack=50 ok
breakdown: risk=58939, ret=-825237, trans=75179, cash=-1040, short=535, liq=0
objective = -691624
claimed objective matches
FEASIBLE
```

A second run was byte-identical (output sha256 `2058744a7dd03791eb049868257c3ed78f86b028fe1a7b26231e7b20bbd46011`). Bars, tail of output, exit 0 each:

```
[bar/PR87_a200_t10_orig_b050_l1e-02_solution.sol]
breakdown: risk=65873, ret=-693306, trans=76537, cash=-1030, short=541, liq=0
objective = -551385
claimed objective matches
FEASIBLE
[bar/PR64_a200_t10_orig_b050_l1e-02_solution.sol]
breakdown: risk=48706, ret=-422571, trans=70489, cash=-940, short=545, liq=3124
objective = -300647
claimed objective matches
FEASIBLE
```

Comparison:

| file | my checker | `checker/pf_eval.py` | posted / claimed |
|---|---|---|---|
| `solution/a200_t10_orig_b050_l1e-02_solution.sol` | feasible, -691624 | feasible, -691624 | -691624 |
| `bar/PR87_a200_t10_orig_b050_l1e-02_solution.sol` | feasible, -551385 | feasible, -551385 | -551385 |
| `bar/PR64_a200_t10_orig_b050_l1e-02_solution.sol` | feasible, -300647 | feasible, -300647 | -300647 |

The breakdowns agree component by component. For the claim, risk 58939, return -825237, transaction 75179, cash
-1040, short 535, liquidation 0. Exit codes also agree on all eleven negatives (section 5).

## 9. Scope and verdict

- **Out of scope.** I did not re-establish the novelty side: which open pull requests exist and the live best-known
  table. That needs network access and belongs to another panel role.
- **Checked locally.**
  - The copied `bar/06-portfolio-solutions-README.md` has no a200 row; "a200" occurs once, in the naming example.
  - The bar file `bar/PR87_a200_t10_orig_b050_l1e-02_solution.sol` recomputes exactly to its posted -551385.
  - -691624 < -551385 strictly, by 140239.
- **Not an exhaustive-search claim.** This is a single-object claim and was checked completely: every period, every
  term, no sampling.
- **Verdict.** My independent checker, written from the definition before I saw the author's code:
  - confirms feasibility (c2 and c3) in all 10 periods;
  - recomputes the exact objective -691624, equal to the claimed value;
  - was deterministic;
  - accepts both known positives at their posted values;
  - rejects every constructed negative.

  The author's checker agrees on every number. The only caveat is that the exact figure depends on the tie rule the
  definition states, half away from zero for the 25 round(5/2) terms. That rule is stated explicitly and is confirmed by
  both third-party bar values.

pass: true
