# CRITERION skeptic verdict: cell a200_t10_orig_b050_l1e-02 (QOBLIB class 06 portfolio)

context: subagent (Claude Code Agent tool, fresh context, model opus)

What I read: only the claim package (claim/) and a private work folder. No web access. Whether the bar is complete and whether the files match upstream are left to NOVELTY. The session was paused once by a usage limit and resumed in the same context, with no new inputs. The claim folder was not modified: its sha256 manifest and file tree were identical before and after every run.

## Method

- Recomputed the sha256 of all 12 files listed in claim/CLAIM.md. All 12 match.
- Wrote my own evaluator directly from the ZIMPL text of claim/definition/bqp_u3_c10.zpl and claim/definition/parameter_u3_c10.zpl. It is not derived from claim/checker/pf_eval.py. It:
  - expands the counts into binary x[i,m,tau,t] using the canonical slot fill;
  - builds the slack registers y (4 bits) and s2 (7 bits) and checks rows c2 and c3 as literal equalities;
  - evaluates every objective term in exact rationals, with selectable tie rules;
  - records exact .5 ties and the closest coefficient to a rounding boundary.
- Ran claim/checker/pf_eval.py as claim/REPRODUCE.md describes (python3 -I). I also reviewed its source line by line against the ZIMPL model and found no discrepancy. It handles the risk over ordered pairs, return only for t = 0..8, the XOR transaction cost for transitions 0->1 .. 7->8, the first-day buy cost, the liquidation at t = 9, the cash interest from the cash-slack bits, and the short cost at every t.
- Both evaluators agree exactly on all three files:

| file | feasible | risk | return | transaction | cash interest | short cost | liquidation | objective |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| claim/solution/a200_t10_orig_b050_l1e-02_solution.sol | yes | 58939 | -825237 | 75179 | -1040 | 535 | 0 | **-691624** |
| claim/bar/PR87_a200_t10_orig_b050_l1e-02_solution.sol | yes | 65873 | -693306 | 76537 | -1030 | 541 | 0 | -551385 |
| claim/bar/PR64_a200_t10_orig_b050_l1e-02_solution.sol | yes | 48706 | -422571 | 70489 | -940 | 545 | 3124 | -300647 |

Both third-party headers (-551385 and -300647) are reproduced exactly, but only under the class's documented rounding rule: exact rationals, round half away from zero.

## Criterion conditions and findings

The criterion is clause (b) as quoted in claim/CLAIM.md, read together with the operator's clarification.

1. **Class 06, multi-period with transaction costs and short selling.** The operator restricted the quarry to class 06, and the claim is a class 06 claim. The reference ZIMPL model contains all three features. MET.

2. **"an instance": one cell named, existential quantifier.** The cell is instance po_a200_t10_orig with B = 50 and lambda = 1e-2.
   - The packaged instance files are consistent with that name: 200 symbols, days 0..9 (matching t_beg = 0 and time_intervals = 10 in the model), 400000 covariance entries (complete, symmetric, positive diagonal), and positive prices.
   - lambda = 1e-2 is one of the eight lambda values used in the official table.
   - B = 50 is the value of `param B` in claim/definition/parameter_u3_c10.zpl. It is also the budget that both independent pull requests (#64 and #87) use for this cell.
   - The official table shows no a200 budget, and the package has no model listing for a200. So "B = 50 is the class's a200 budget" is supported but not proven here.
   - Whether the packaged files match upstream is for NOVELTY.

   MET, as far as the package can show.

3. **Feasible.** The class's rows are:
   - c2: net + cash slack = C = 10, with the cash slack in 0..15, i.e. net in [-5, 10];
   - c3: total + count slack = B = 50, with the count slack in 0..127.

   Unit counts must be 0..3 per (asset, direction). Per period t = 0..9:
   - net = 0, -2, -2, -4, 10, 0, 0, -4, -2, 0
   - total = 50 in t = 0..8, and 0 at t = 9

   All rows hold. MET.

4. **Objective sense.** The model uses `minimize`, and the objective is an exact integer under Zimpl rounding. The value is -691624.
   - The only exact .5 ties are the 25 short-cost coefficients at t = 0, each round(5/2). This happens because every unit price at t = 0 is exactly 100000.
   - Half away from zero (the class rule) gives -691624. Half-to-even gives -691649. Plain float64 gives -691627.
   - The closest non-tie coefficient is 1.8e-4 from a rounding boundary, so how the decimal inputs are parsed cannot change the value.

   MET.

5. **"listed best-known objective" and the operator's bar.** The official table (claim/bar/06-portfolio-solutions-README.md) has 129 rows: a003, a010_b004 and a050_b020. It has no a200, a400 or b050 row; "a200" appears only in the naming example.
   - Under the charter text alone, there would be no listed value to beat.
   - The clarification sets the bar "for any instance" as the better of the table and any value posted in an open QOBLIB pull request. So the bar for this cell is the best open-PR value.
   - In the package: PR #87 posts -551385 and PR #64 posts -300647. Both re-evaluate exactly to those values. According to the status record, PR #44 has no a200 path.
   - The bar is therefore -551385 (PR #87). Whether it is complete (newer open PRs, or values posted outside the solution files) cannot be checked from the package and is left to NOVELTY.

   MET, with the bar as recorded.

6. **Strictly better, and not a tie.** -691624 < -551385, a margin of 140239. This is a strict integer improvement in the minimising direction. The margin is robust:
   - under the half-to-even tie rule: -691649 vs -551411;
   - under float64 evaluation: -691627 vs -551389;
   - if the 8->9 rebalancing, which the reference model does not charge, were charged (4813 for the claim, 4764 for the bar): -686811 vs -546621.

   It also beats PR #64's -300647. MET.

7. **One cell per claim, no bundling.** There is one solution file with one header (instance, budget, lambda and objective each appear once) for one cell. The bar files are context only. MET.

8. **Canonical format, with header and cell agreeing.** The file uses comment lines and four-field position lines `period symbol long short`. It has 285 lines with at most one per (period, symbol), all symbols are in the instance, periods are 0..8 only, counts are 0..3, and there are no all-zero lines. The header (budget 50, lambda 0.01 = 1/100, instance po_a200_t10_orig) matches b050, l1e-02 and the instance folder. MET.

9. **Partial wins.** None are enumerated, and the operator excluded clause (a). This is a claim under the full clause (b) only. MET.

## Stretches and hidden quantifiers examined

- **Last period.** The claim holds nothing at t = 9. The reference model gives no return at t = 9 and does not charge the 8->9 rebalancing. The claim, like PR #87, closes its whole book at t = 9 for free. This is the class's own objective and applies equally to the bar, and charging the closing cost would not change the outcome (see condition 6). Not an exploit.
- **Long and short of the same asset at once.** None in the claim. PR #64 has 23 such lines; this does not affect the claim.
- **Counts above the per-asset limit.** None: the maximum count is 3.
- **Budget and net-position rows.**
  - The budget row is used exactly: total = 50 with count slack 0 in t = 0..8.
  - Five periods are net short (cash slack 12-14, above C = 10). This is inside the class's feasible range [C-15, C]: it follows from ZIMPL row c2 with CS1 = {0..3} and is stated explicitly in claim/definition/06-portfolio-check-README.md. PR #87 does the same in six periods.
  - The class README's prose ("restrict the total available cash to not exceed C units") could be read more strictly, as net >= 0. That reading contradicts the formal row and would make the bar infeasible too, so it is not the class definition.
  - The extra cash interest involved is about 140, which is immaterial to the margin.
- **Not a copy of the bar.** Only 85 of the claim's 285 lines are identical to PR #87's, and every period 0..8 differs. The claimant's file comment describes a mix of chain DP and descent; being derived from a public solution does not affect the literal criterion.
- **Null model.** No statistical claim is made. This is a deterministic, exact evaluation of one object against a fixed bar, so no null model is needed, and I agree. Note that the bar is a heuristic community value: PR #87's header says there is no optimality proof. The result is therefore "better than the best posted value", not optimal or near-optimal.

confirmed_scope: The canonical count file claim/solution/a200_t10_orig_b050_l1e-02_solution.sol is feasible for QOBLIB class 06 instance po_a200_t10_orig (instance files as packaged in claim/instance/) with B = 50 and lambda = 0.01, and its exact objective under the class's minimised reference model (claim/definition/bqp_u3_c10.zpl with claim/definition/parameter_u3_c10.zpl, lambda set to 0.01, Zimpl rounding half away from zero) is -691624, strictly below (by 140239) the bar of -551385, which is the exactly re-evaluated objective of the PR #87 solution file copied in claim/bar/ and, per the claim's status record, the best value posted in an open QOBLIB pull request for cell a200_t10_orig_b050_l1e-02, a cell for which the official best-known table (copy in claim/bar/06-portfolio-solutions-README.md) has no row.

pass: true
