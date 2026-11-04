# REPRODUCE verdict

context: codex exec (fresh context via codex-fresh)

The saved candidate passes independent reproduction for `po_a400_t10_s00`, `B=100`, `lambda=0.01`. Its exact reference-model objective is **−1,696,664**, improving on the best same-cell value found in the reviewed public evidence, **−1,090,282**, by **606,382**.

## Definition and independence

`CLAIM.md` requires:

> a feasible solution strictly better than the best known objective of an instance in class 06
> (portfolio optimisation: multi-period, transaction costs, short selling) of the Quantum Optimization Benchmarking
> Library, in the objective sense the class defines, where the bar is the better of the library's best-known table and
> any value posted in an open pull request to the library (#44, #64 and #87 when this was written).

I read the claim, definition and source receipts, then wrote `independent_check.py` and `independent_derivation.md` before reading `checker/portfolio_check.py` or `run_checks.sh`. The checker imports neither author code nor an existing evaluator.

The controlling definition is `definition/model.zpl`, with parameters from `definition/parameters.zpl` and canonical counts from `definition/check-readme.md`. Key verbatim expressions are:

```text
round(lambda * tau_i * tau_j * cov[i,j,t] * p[i,t] * p[j,t])
sum <i,m,tau> in SX : tau * x[i,m,tau,t] + sum <c> in CS1 : 2^c * y[c,t] == C;
sum <i,m,tau> in SX : x[i,m,tau,t] + sum <c> in CS2 : 2^c * s2[c,t] == B;
```

The interior objective sum explicitly uses `TX \ { t_beg, t_end }`. I preserved that endpoint convention rather than substituting the overview's informal finance formula.

## Re-derived calculation

1. All input decimals are exact rational numbers. Unit prices are `100000 * raw_p[i,t] / raw_p[i,0]`. The checker validates the complete grid: **4,000 prices and 1,600,000 ordered covariance entries**, with no duplicates, missing indices, unknown symbols or malformed values.
2. For a rational `n/d`, rounding is `sign(n) * floor((2*abs(n)+d)/(2*d))`. It is odd, including half ties. Every one of the **1,600,000 base risk coefficients** is rounded independently. Direction signs therefore multiply the rounded base coefficient; copy indices do not change it.
3. Each of the candidate's **504 position rows** has valid integer long and short counts in `0..3`, a valid period and symbol, and a unique period/symbol key. Omitted entries are zero. Filling copy slots in prefix order constructs all **24,000 binary position variables**.
4. Cash slack is `10 − net`, representable by four bits exactly when it lies in `0..15`. Count slack is `100 − total`, representable by seven bits exactly when it lies in `0..127`. I reconstructed all **110 slack bits** and checked both original equalities in every period.
5. Expanding every nonzero ordered binary pair gives the risk sum. Independently aggregating by signed asset counts gives `sum(Q[i,j,t] * net[i,t] * net[j,t])`. Both calculations agree in every period; neither assumes covariance symmetry nor rounds an aggregate.
6. Cash-interest coefficients are exactly `10*2^k`, giving `−10*cash_slack`. Short positions contribute `round(p/40000)` per copy. Returns contribute `−round(tau*(p[t+1]−p[t]))` in periods **0–8**.
7. For binary `a,b`, `a+b−2ab` counts a changed slot. Counts `u,v` require at least `abs(u−v)` changed slots because overlap cannot exceed `min(u,v)`; prefix assignments attain this on every adjacent pair simultaneously. Explicit binary and count-based transaction calculations agree. Opening costs occur at period 0; rebalancing at **1–8**; liquidation at **9**. There is **no return at 9 and no rebalancing charge from 8 to 9**. No extra term was introduced.
8. Summing the six integer components gives the objective below, matching both the header in `portfolio.sol` and `CLAIM.md` exactly.

| Period | Total positions | Net positions | Cash slack | Count slack | Objective |
|---:|---:|---:|---:|---:|---:|
| 0 | 100 | −4 | 14 | 0 | −269779 |
| 1 | 100 | 10 | 0 | 0 | −203245 |
| 2 | 100 | −4 | 14 | 0 | −228991 |
| 3 | 100 | 4 | 6 | 0 | −163708 |
| 4 | 100 | 10 | 0 | 0 | −121570 |
| 5 | 100 | 10 | 0 | 0 | −229080 |
| 6 | 100 | −2 | 12 | 0 | −186659 |
| 7 | 100 | 2 | 8 | 0 | −146349 |
| 8 | 100 | −4 | 14 | 0 | −147183 |
| 9 | 0 | 0 | 10 | 100 | −100 |

| Component | Candidate | PR #87 | PR #64 |
|---|---:|---:|---:|
| Risk | 64891 | 94133 | 64213 |
| Returns | −1912445 | −1342073 | −677366 |
| Transactions | 150512 | 157295 | 142895 |
| Cash interest | −780 | −800 | −760 |
| Short costs | 1158 | 1163 | 1261 |
| Liquidation | 0 | 0 | 10084 |
| **Objective** | **−1696664** | **−1090282** | **−459673** |

The two incumbent objects, `comparison/pr87-a400.sol` and `comparison/pr64-a400.sol`, also pass every feasibility and objective check.

## Integrity, repeatability and public comparison

`source-audit.json` records **116 successful manifest hash checks**, including the supplemental manifest, and verifies all **18 current receipts** against their bodies, metadata and hashes. The saved database matches the database inside its archive. Historical snapshots retain their historical dates; their changing PR metadata is not misrepresented as nondeterminism.

`independent-all-1.json` and `independent-all-2.out` are byte-identical under hash seeds 17 and 98765. The supplied `run_checks.sh` was then run twice under those seeds; its outputs are also byte-identical, and every component and feasibility row agrees with my checker. See `replay-verification.json`, `author-1.out` and `author-2.out`. Numerical evaluations used one thread and ran sequentially. The independent runs' largest recorded peak RSS was **31,358,976 bytes**, below 1.2 GB.

The mandatory primary-table GET succeeded at **2026-10-15 17:23:37 UTC**, HTTP 200. `independent-primary-table.md` has SHA256 `05a6d23392d960fb16028cc1e9ba8d7547aa445a0e3f30c433f5f4acab56c09a`, matching the supplied table; it contains no a400 row. The request and response headers are in `independent-primary-receipt.json`.

The current QOBLIB response contains 25 open PRs. I examined their titles and bodies and the issue comments, inline review comments and separate review-summary responses for all four portfolio PRs. Counts are respectively **14/0/0**, **3/0/0**, **3/0/0** and **0/0/0** for #44, #64, #87 and #92. No response advertises another page. The older `data/supplemental/coverage.json` records a historical gap; the current review-summary receipts close that gap. PR #44 concerns small instances; #92 concerns two a200 cells. The current heads of #64 and #87 match the pinned solution sources. No comment or review body supplies a stronger same-cell value.

I also checked the complete, untruncated KenWuqianghao and mnn31 repository trees and read their portfolio result documents, saved under `independent-public/`. KenWuqianghao's a400 results use other seeds, periods or risk weights; none is this cell. mnn31's large-family claim points to #87. Further cited public result documents were read once where their bodies were absent from the supplied files: negsearch covers a003–a005; the GNN tables concern OR-Library or synthetic models; the IBM document describes a different mean–variance encoding capped at 15 assets. The supplemental QUBOLib index contains 128 portfolio models, all a010/a050, and no selected-cell entry. The framework abstract reports vehicle-routing and maximum-cut case studies. The supplied trophy case contains no portfolio entry; the 62 current V3R1T4S PRs include two portfolio claims, both a200. These sources provide no disqualifying same-cell result. Requests and hashes for the additional documents are in `independent-public/receipts.json`; no blocked endpoint was retried.

This verifies the complete saved feasible witness and its strict improvement against the reviewed public evidence. No global optimum, lower bound, or exhaustive optimization search is claimed. No sample has been used as an exhaustive-search certificate. No required witness or comparison response is missing, and no arithmetic mismatch or output nondeterminism was found.

pass: true
