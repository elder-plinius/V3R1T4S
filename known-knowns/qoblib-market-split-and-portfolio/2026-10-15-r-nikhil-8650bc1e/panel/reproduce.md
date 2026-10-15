# REPRODUCE skeptic verdict: cell a200_t10_s00_b050_l1e-02 (QOBLIB class 06)

context: subagent (Claude Code Agent tool, fresh context, saw only its copy of claim/)

Claim checked: `solution/a200_t10_s00_b050_l1e-02_solution.sol` is feasible for `instance/po_a200_t10_s00`
with B = 50 and lambda = 0.01, and its exact objective under `definition/bqp_u3_c10.zpl` +
`definition/parameter_u3_c10.zpl` (minimised) is -644342. The bar files evaluate to -401535 (PR87) and -192428 (PR64).

Order of work: I read `CLAIM.md`, `REPRODUCE.md`, `STATUS_RECORD.md` and everything in `definition/`. Then I wrote my own
checker (`my_check.py`, in the working directory next to `claim/`) and ran it on all three files and on 5 negatives.
I opened `checker/pf_eval.py` only after that.
Python 3.9.6, standard library only, `python3 -I`, one thread, `nice -n 15`.

## 1. Definition lines implemented (quoted from definition/bqp_u3_c10.zpl and parameter_u3_c10.zpl)

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
subto c2: forall <t> in TX :
      sum <i,m,tau> in SX : tau * x[i,m,tau,t] + sum <c> in CS1 : 2^c * y[c,t] == C;
subto c3: forall <t> in TX :
      sum <i,m,tau> in SX : x[i,m,tau,t] + sum <c> in CS2 : 2^c * s2[c,t] == B;
```
```
param cash := 1000000;  param unit := 100000;  param delta := 0.001;  param nu := 0.0001;
param rho := 0.000025;  param ub := 3;  param upscale := 1;  param C := cash / unit;
param t_beg := 0;  param t_end := t_beg + time_intervals - 1;
param ucnt[<s> in S] := unit / raw_p[s,t_beg];
param p[<s,tt> in S*T] := raw_p[s,tt] * ucnt[s];
set CS1 := { 0 .. 3 };  set CS2 := { 0 .. 6 };  set SC := { 1 .. ub };  set SL := { 1, -1 };
set SX := S * SC * SL;  var x[SX*TX] binary;  var y[CS1*TX] binary;  var s2[CS2*TX] binary;
```

Count format (from `definition/06-portfolio-check-README.md`): lines `<period> <symbol> <long units> <short units>`,
with units in {0..ub}, at most one line per (period, symbol), and unlisted pairs hold nothing. "A count vector
corresponds to the canonical assignment that fills copies 1,...,u".

How my checker works:
- It maps the counts to an explicit binary point: x[i,m,tau,t] = 1 iff m <= u[i,tau,t].
- It sets y and s2 to the binary expansions of C - net and B - total. If either falls outside [0,15] or [0,127], the
  solution is infeasible. It then re-checks rows c2 and c3 with those slacks.
- It evaluates the ZIMPL objective term by term on that binary point, over all pairs of set variables, with every
  coefficient rounded half away from zero on exact `Fraction`s.
- As a second route it recomputes the objective from the counts (rebalancing as |u_t - u_{t-1}|, risk as
  coef * u * u'). Both routes must agree.
- It also validates the instance: 200 symbols x 10 periods of prices with no gaps or duplicates, and exactly
  200*200*10 = 400000 covariance entries.

## 2. My checker's output (copied from `my_check_run1.txt`)

Command (from the working directory):
`nice -n 15 python3 -I my_check.py claim/instance/po_a200_t10_s00 claim/solution/a200_t10_s00_b050_l1e-02_solution.sol claim/bar/PR87_a200_t10_s00_b050_l1e-02_solution.sol claim/bar/PR64_a200_t10_s00_b050_l1e-02_solution.sol` gives exit 0, and:

```
instance claim/instance/po_a200_t10_s00: 200 assets, 10 periods, 400000 cov entries
== claim/solution/a200_t10_s00_b050_l1e-02_solution.sol
model: B=50 lambda=1/100 ub=3 C=10 CS1=0..3 CS2=0..6 instance-header=po_a200_t10_s00
t=0: net=4 total=50 y-slack=6 s2-slack=0 ok
t=1: net=-2 total=50 y-slack=12 s2-slack=0 ok
t=2: net=-2 total=50 y-slack=12 s2-slack=0 ok
t=3: net=10 total=50 y-slack=0 s2-slack=0 ok
t=4: net=4 total=50 y-slack=6 s2-slack=0 ok
t=5: net=10 total=50 y-slack=0 s2-slack=0 ok
t=6: net=-2 total=50 y-slack=12 s2-slack=0 ok
t=7: net=6 total=50 y-slack=4 s2-slack=0 ok
t=8: net=8 total=50 y-slack=2 s2-slack=0 ok
t=9: net=0 total=0 y-slack=10 s2-slack=50 ok
risk        63057
return      -784113
transaction 76812
cash_int    -640
short_cost  542
liquidation 0
objective (literal binary evaluation) = -644342
objective (count-formula cross-check) = -644342
claimed objective -644342 matches
FEASIBLE
RESULT claim/solution/a200_t10_s00_b050_l1e-02_solution.sol: PASS
== claim/bar/PR87_a200_t10_s00_b050_l1e-02_solution.sol
...(per-period lines all ok)...
risk        86967
return      -562250
transaction 73926
cash_int    -740
short_cost  562
liquidation 0
objective (literal binary evaluation) = -401535
objective (count-formula cross-check) = -401535
claimed objective -401535 matches
FEASIBLE
RESULT claim/bar/PR87_a200_t10_s00_b050_l1e-02_solution.sol: PASS
== claim/bar/PR64_a200_t10_s00_b050_l1e-02_solution.sol
...(per-period lines all ok)...
risk        75690
return      -344327
transaction 71626
cash_int    -950
short_cost  662
liquidation 4871
objective (literal binary evaluation) = -192428
objective (count-formula cross-check) = -192428
claimed objective -192428 matches
FEASIBLE
RESULT claim/bar/PR64_a200_t10_s00_b050_l1e-02_solution.sol: PASS
```
(Two abbreviated blocks are marked `...`. The full text is in `my_check_run1.txt`.)

Results: claim -644342, PR87 -401535, PR64 -192428. All three are feasible.

Determinism: a second run (`my_check_run2.txt`) is byte-identical. Both files have sha256
`3af89b3be54eff0f908f0bc839467b6e719de087940a8863780aad73b2f53a42`.

### Negative tests (corrupted copies of the claimed solution, in `negatives/`)

Output from `my_check_negatives.txt`:
```
== negatives/neg_budget_row.sol        (0 META 1 0 -> 0 META 2 0)
t=0: net=5 total=51 y-slack=5 s2-slack=-1 VIOLATED
INFEASIBLE
== negatives/neg_capital_row.sol       (3 BX 0 1 -> 3 BX 1 0)
t=3: net=12 total=50 y-slack=-2 s2-slack=0 VIOLATED
INFEASIBLE
== negatives/neg_dup.sol               (duplicate line 0 META 1 0)
INVALID: line 8: duplicate (period,symbol)
== negatives/neg_objective.sol         (objective -644343)
claimed objective -644343 DOES NOT MATCH
== negatives/neg_unit4.sol             (0 GE 3 0 -> 0 GE 4 0)
INVALID: line 15: unit count outside 0..3
my_check negatives/neg_budget_row.sol exit=1
my_check negatives/neg_capital_row.sol exit=1
my_check negatives/neg_dup.sol exit=1
my_check negatives/neg_objective.sol exit=1
my_check negatives/neg_unit4.sol exit=1
```
My checker rejects all five.

## 3. Author's checker (`checker/pf_eval.py`, run per `REPRODUCE.md` from inside `claim/`, after my checker)

`python3 -I checker/pf_eval.py instance/po_a200_t10_s00 <file>` (under `nice -n 15`), copied from `author_run1.txt`:
```
== solution/a200_t10_s00_b050_l1e-02_solution.sol
instance po_a200_t10_s00: 200 assets, 10 periods; B=50 lambda=1/100
t= 0 net=  4 total= 50 cash_slack=6 count_slack=0 ok
...
t= 9 net=  0 total=  0 cash_slack=10 count_slack=50 ok
breakdown: risk=63057, ret=-784113, trans=76812, cash=-640, short=542, liq=0
objective = -644342
claimed objective matches
FEASIBLE
exit=0
== bar/PR87_a200_t10_s00_b050_l1e-02_solution.sol
breakdown: risk=86967, ret=-562250, trans=73926, cash=-740, short=562, liq=0
objective = -401535
claimed objective matches
FEASIBLE
exit=0
== bar/PR64_a200_t10_s00_b050_l1e-02_solution.sol
breakdown: risk=75690, ret=-344327, trans=71626, cash=-950, short=662, liq=4871
objective = -192428
claimed objective matches
FEASIBLE
exit=0
```
The per-period net, total and slack values match mine line for line, and every breakdown term matches my term.
The second run (`author_run2.txt`) is byte-identical to the first. Both have sha256
`70c31fcf854cfeed180e2768c02f04671f2392e2ada70f41234551d2b1bf3220`.

On the same negatives the author's checker returns: budget-row 21 (INFEASIBLE), capital-row 21 (INFEASIBLE),
dup 10 (MALFORMED), objective 10 (CLAIMED OBJECTIVE MISMATCH), unit4 10 (MALFORMED). The full text is in
`author_negatives.txt`.

## 4. sha256 (shasum -a 256, run inside claim/), compared with CLAIM.md

```
d18dc2de89b6fda43707532e28fbd6566d74365f3c1daa3c8e8392107b90fd6e  REPRODUCE.md
d382dcca4799bc36a9e50acad58c1c8237b3a72d79b5b3c74a53fba9e0199cdf  STATUS_RECORD.md
05a6d23392d960fb16028cc1e9ba8d7547aa445a0e3f30c433f5f4acab56c09a  bar/06-portfolio-solutions-README.md
b730b88b45af60c58c19b2fb9f4e729f5f1e8d6cf272afe11851f09ab8cf63ef  bar/PR64_a200_t10_s00_b050_l1e-02_solution.sol
e886f65ac1b722f117c2333810266ff8ef2aff8a9a5f21d799755bcfcb2ba377  bar/PR87_a200_t10_s00_b050_l1e-02_solution.sol
9d3379f914acddb7e53ce504a270a7f5d23454353c1ddde4d1653b17b64f8289  checker/pf_eval.py
fb04ca5beb2ba05b2adc9457db7547764ab384db3fd43d3fd09303c671f74f15  definition/06-portfolio-README.md
da08e16e09a2aef577b5efbdadd5e8619a89430479fa5fb42d71bda33acfd048  definition/06-portfolio-check-README.md
5d0d79a89f7828886b29b132ee45ba3dbb0c71e614863796664a4908f1db61eb  definition/06-portfolio-instances-README.md
8962c6a83db1eed11557c8d68dae229d39e14eb31e59b8a16579fc577697513d  definition/bqp_u3_c10.zpl
a3dccc0aa5196166d0caae80f63671a5a651b033498fe11fb08a35404e8dddca  definition/parameter_u3_c10.zpl
5214e9ddb522339f86485e0bdc86f519542d552cfc744fc137bd7dcabfa31167  instance/po_a200_t10_s00/covariance_matrices.txt.gz
189292e71736fdfb55a75d4dfe5269829668a9ac73513bedd4fc5b30bf38fee9  instance/po_a200_t10_s00/stock_prices.txt.gz
8650bc1e720ff19bd4f17cedefb5b4021dbcd1a3315c8a79abd6d79cf82efe62  solution/a200_t10_s00_b050_l1e-02_solution.sol
```
All 14 match the table in CLAIM.md, including the frozen solution hash `8650bc1e...2efe62`.

## 5. Discrepancies and notes

- **No discrepancy.** My checker and the author's give the same feasibility, the same totals and the same per-term
  breakdown for all three files and all five negatives. Each checker gives byte-identical output across two runs.
- **The rounding rule matters, and the claim uses the documented one.** `sensitivity.py` / `sensitivity_out.txt`
  show exact .5 ties.
  - All of them come from the period-0 short cost: `rho*p[i,0] = 0.000025*100000 = 5/2`.
  - Half away from zero (the rule the check README specifies, and the one this panel was told is ZIMPL's) gives
    -644342.
  - Half-even would give -644365 / -401558 / -192453, i.e. 23, 23 and 25 lower: one per period-0 short unit.
  - Under either rule the claim stays strictly below the bar.
- **Decimal parsing does not matter.** Reading the instance numbers as IEEE doubles instead of exact decimals gives
  the same three values: -644342, -401535, -192428.
- **A model quirk, not a defect.** The reference model has no rebalancing term for the step from t_end-1 to t_end.
  The claimed solution (like PR87) holds 50 positions at t=8 and nothing at t=9, so liquidation is 0 and closing the
  positions costs nothing. That is what the model as written says (`TX \ { t_beg, t_end }`), and the claim is made
  under that model, so it does not affect the verdict.
- **Feasibility is attained by a real binary vector.** The canonical copy-filling x together with the unique y and s2
  slacks satisfies c2 and c3 in all 10 periods. The literal objective on that point is -644342.
- **Not checked here.** Novelty, i.e. whether -401535 really is the best public value, belongs to another skeptic.
  I only confirmed that the two bar files in `bar/` evaluate to the values CLAIM.md states.

Verdict: my own independent code confirms that the solution is feasible and that its exact objective is -644342.
The author's checker agrees, all hashes match, and the results are deterministic.

pass: true
