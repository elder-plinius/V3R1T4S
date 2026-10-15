# CRITERION skeptic verdict

context: subagent (Claude Code Agent tool, fresh context, saw only its copy of claim/)

Inputs read: claim/CLAIM.md, claim/STATUS_RECORD.md, claim/REPRODUCE.md, claim/definition/* (bqp_u3_c10.zpl,
parameter_u3_c10.zpl, 06-portfolio-README.md, 06-portfolio-check-README.md, 06-portfolio-instances-README.md),
claim/checker/pf_eval.py, claim/bar/*, claim/solution/*, claim/instance/po_a200_t10_s00/*.
Scratch script written outside claim/: work/indep.py (my own evaluator, see clause 2).

## Criterion (verbatim, from CLAIM.md)

> a feasible solution strictly better than the best known objective of an instance in class 06 (...) of the
> Quantum Optimization Benchmarking Library, in the objective sense the class defines, where the bar is the better
> of the library's best-known table and any value posted in an open pull request to the library (#44, #64 and #87
> when this was written).

Widening of the bar by the human: best value posted anywhere public (e.g. KenWuqianghao/qoblib-solvers). No partial
wins are enumerated, so only the full criterion can pass.

## 0. Integrity of the package

All 14 sha256 values listed in CLAIM.md match the files (`shasum -a 256`), including
solution/a200_t10_s00_b050_l1e-02_solution.sol = 8650bc1e...efe62 and both bar files.

## 1. "a feasible solution" — PASS

Provided checker, per REPRODUCE.md (`python3 -I checker/pf_eval.py instance/po_a200_t10_s00 solution/...`):

```
instance po_a200_t10_s00: 200 assets, 10 periods; B=50 lambda=1/100
t= 0 net=  4 total= 50 cash_slack=6 count_slack=0 ok
t= 1 net= -2 total= 50 cash_slack=12 count_slack=0 ok
t= 2 net= -2 total= 50 cash_slack=12 count_slack=0 ok
t= 3 net= 10 total= 50 cash_slack=0 count_slack=0 ok
t= 4 net=  4 total= 50 cash_slack=6 count_slack=0 ok
t= 5 net= 10 total= 50 cash_slack=0 count_slack=0 ok
t= 6 net= -2 total= 50 cash_slack=12 count_slack=0 ok
t= 7 net=  6 total= 50 cash_slack=4 count_slack=0 ok
t= 8 net=  8 total= 50 cash_slack=2 count_slack=0 ok
t= 9 net=  0 total=  0 cash_slack=10 count_slack=50 ok
breakdown: risk=63057, ret=-784113, trans=76812, cash=-640, short=542, liq=0
objective = -644342
claimed objective matches
FEASIBLE
exit=0
```

Independent spot checks of the constraints most likely to be stretched:
- Budget row (c3), B = 50, slack s2 has 7 bits so slack in [0,127]: totals are 50 in t=0..8 and 0 in t=9; slack in
  {0, 50}, within [0,127]; total never exceeds B. Not stretched.
- Capital row (c2), C = cash/unit = 10, slack y has 4 bits so slack in [0,15]: net in {-2,0,4,6,8,10}, slack in
  {0,2,4,6,10,12}, all integers in [0,15]. Net -2 is allowed by the model (net range [C-15, C] = [-5,10], stated
  in the check README). Not stretched.
- Counts 0..3 and format conventions (check README): awk over the 305 position lines gives
  `bad=0 dup=0 long&short same line=0 all-zero lines=0`; header `budget 50`, `lambda 0.01`, `instance
  po_a200_t10_s00`; periods 0..9 and all symbols exist (my evaluator asserts both).
- Cash-interest term recomputed by hand: slacks 6,12,12,0,6,0,12,4,2,10 with coefficients round(nu*unit*2^k) =
  10,20,40,80 give 60+120+120+0+60+0+120+40+20+100 = 640, matching `cash=-640`.
- Note (not a stretch, a property of the reference model): t_end has no rebalancing cost term in bqp_u3_c10.zpl,
  only liquidation cost on x[.,t_end]; the solution empties the book at t=9 (liq=0). The bar file (PR #87) does the
  same, so the comparison is like-for-like.

## 2. "in the objective sense the class defines" — PASS

The class reference model is bqp_u3_c10.zpl (`minimize`), as stated in the check README. I wrote my own evaluator
(work/indep.py) that does not use the count shortcut: it expands each count into explicit binaries x[i,m,tau,t]
(copies 1..u), and evaluates the ZPL objective term by term, including the literal XOR transaction term
x[t-1]+x[t]-2x[t-1]x[t], the full SX*SX risk double sum, the cash-interest y bits from the c2 equality and the
short cost, with t_beg = 0, t_end = 9 read from the parameter file (instance days are 0..9, 200 symbols per day;
covariance file has 400000 data rows = 200*200*10). Output:

```
solution/a200_t10_s00_b050_l1e-02_solution.sol B=50 lam=1/100 feasible=True claimed=-644342 {'away': -644342, 'even': -644365, 'up': -644342, 'down': -644365, 'tozero': -644365} half-integer risk coeff terms: 0
bar/PR87_a200_t10_s00_b050_l1e-02_solution.sol B=50 lam=1/100 feasible=True claimed=-401535 {'away': -401535, 'even': -401558, 'up': -401535, 'down': -401558, 'tozero': -401558} half-integer risk coeff terms: 0
bar/PR64_a200_t10_s00_b050_l1e-02_solution.sol B=50 lam=1/100 feasible=True claimed=-192428 {'away': -192428, 'even': -192453, 'up': -192428, 'down': -192453, 'tozero': -192453} half-integer risk coeff terms: 0
```

Under ZIMPL's rule ("away") my evaluator reproduces −644342 exactly. Because the binaries are the canonical
(filled-copy) assignment, this is the literal value of a binary point of the shipped model, not only the count
formulation's value.

## 3. "strictly better" than the bar — PASS

Minimisation; −644342 < −401535, difference −242807 (exact integers, not a tie).

Convention dependence: the comparison does not depend on the round-half-away-from-zero rule. Under five tie rules
(away, half-even, half-up, half-down, half-toward-zero) the claim scores −644342 / −644365 and the bar −401535 /
−401558; tie-rule effects are about 23 units against a gap of about 242800. No risk coefficient used by either file
is an exact half-integer.

## 4. The bar is for exactly this cell — PASS (with the stated caveat)

- bar/PR87 file header: `instance po_a200_t10_s00`, `budget 50`, `lambda 0.01`, claimed −401535; checker
  re-evaluates −401535, FEASIBLE, exit 0 (output in clause 2 and below).
- bar/PR64 file header: `instance po_a200_t10_s00`, `budget 50`, `lambda 1e-2` (parsed as 1/100), claimed
  −192428; checker re-evaluates −192428, FEASIBLE, exit 0.
- Official table (bar/06-portfolio-solutions-README.md, same sha256 as the recorded fetch): `grep -n -i -E
  'a200|s00|b050|1e-02|0\.01'` hits a200 only on line 7 (the naming example); there is no a200 row, so the table
  contributes nothing to this cell. The table's Instance column is keyed by the full cell name (e.g.
  `a050_t10_s00_b020_l1e-02`), so treating instance+B+lambda as "an instance" follows the library's own usage, not
  a stretched definition.
- Better of {table: none, PR #87: −401535, PR #64: −192428} = −401535. PR #44 is recorded as covering a003–a010
  only. The KenWuqianghao repository is recorded as posting no value for this lambda.

PR #87 checker run:

```
breakdown: risk=86967, ret=-562250, trans=73926, cash=-740, short=562, liq=0
objective = -401535
claimed objective matches
FEASIBLE
exit=0
```

What I could NOT verify inside the sandbox: whether these are the current PR heads/values, whether other public
sources post a better value (the widened bar), and whether the instance gzip files equal upstream. Those are
NOVELTY/reproduction questions, outside this criterion check; I rely on STATUS_RECORD.md for them. I also cannot
confirm from inside claim/ that the library ships a b050_l1e-02 model file for a200. Two independent open PRs post
values for exactly this cell, and the check README says B and lambda are the only parameters that vary between
variants, so I treat the cell as a legitimate class-06 instance whose best known objective is the posted PR value.

## 5. Bundling and honesty

One cell, one object, one number. The claim says plainly that the official table has no row for this cell, so this
beats posted (open-PR) values rather than a curated table entry. The criterion explicitly counts open-PR values as
the bar, so this is a literal win under the criterion as written, not a widened one. A reader should not take it as
"beats the official QOBLIB best-known table".

## 6. Null model

No statistical inference is involved. The object is an explicit, frozen solution, and the comparison is an exact
integer from a deterministic exact-rational evaluator (reproduced by two independent implementations) against a
posted value that I also re-evaluated exactly. No chance process could produce a false "win" here, so a null test
adds nothing. That reasoning holds.

## Verdict

Every clause of the full criterion is met literally. The comparison survives a change of tie rule, and the bar files
are for the same instance, B and lambda. The only residual reliance is on STATUS_RECORD.md for the completeness and
currency of the public-value search, which belongs to the NOVELTY skeptic.

confirmed_scope: The frozen solution file (sha256 8650bc1e...efe62) is feasible for QOBLIB class 06 instance po_a200_t10_s00 with B = 50 and lambda = 0.01 under the reference model bqp_u3_c10.zpl and has exact minimised objective −644342, strictly below the best value posted in the open-PR files supplied for this cell (PR #87, −401535; PR #64, −192428), a cell for which the official best-known table has no row.

pass: true
