context: subagent
role: CRITERION
claim: partial win p1 (pricing050) of minlplib-finance-open-instances

## Criterion text applied
Partial win p1 (verbatim): "A machine-checkable certificate that the optimum of pricing050 is at most the best known primal value plus 1e-6 * |value|. Example: (i) an interval-arithmetic (directed-rounding) proof that each of the 250 univariate terms a * x * exp(-b * x^p) is concave on [0,10]; and (ii) multipliers lambda in R^5_+ whose Lagrangian dual value, with each of the 50 separable univariate maximisations bounded rigorously by interval branch-and-bound, is within that tolerance of the primal point. ..."
Full criterion (better primal .sol point) is NOT claimed.

## What was run (from claim folder copy)
- code/pricing_parse.py -> model.json: 50 vars, all bounds (0,10); 5 inequality rows e2..e6; term counts (50,50,50,49,50)=249; all term signs '-'; b-types as posted strings 0.0010000000000000002 / 0.010000000000000002 / 0.1.
- code/pricing_eval.py on instance/sol_pricing050.p1.sol: objvar -1813.82907844984; max_con_viol ~7.27e-10; max_bound_viol 0.
- code/cross_check_py.py: CROSSCHECK PASS (max relative residual difference 0 vs instance/py_pricing050.py).
- code/concavity_proof.py: for each of 3 (b,p) types, Fraction(b)*p*10^p-(p+1) = -1 < 0 (concave); arb g'' enclosure upper ends: 6.0000002e-9 (p=3), 1.1577040e-12 (p=2), -0.036787944 (p=1).
- code/cert_arb.py with object/lambda.txt:
```
leaves 1958
LB (rigorous lower bound on min c.x): 1813.829075713452364776297
U = -LB (rigorous upper bound on max objvar): -1813.829075713452364776297
bar (best primal + 1e-6*|best|): [-1813.827264170922000000000 +/- 3e-26]
S1 PASS ; margin bar-U = [0.001811542530 +/- 3.65e-13]
```
- cmp of freshly written leaves.json to object/cert_arb_leaves.json: identical.
- code/cert_mpiv.py independent mpmath.iv path:
```
U = -LB: [-1813.82907825764672987032749338460415035178355, ...]
bar: -1813.82726417092  S1 cross-check PASS
```
- status/minlplib.solu: `=best= pricing050 -1813.8290780000`, `=bestdual= pricing050 -1153.0032810000`.
- status/pricing050.html: primal p1 -1813.829078; duals include SCIP -1534.3281 (best published solver dual among those listed).
- sha256 instance/gms_pricing050.gms = 192dd92d69cdcd131462d40c137df73dc101afef0739cc7ba98c130a79313715 (matches CLAIM.md).

## Hidden-quantifier / definition hunt
- Essential p1 sentence is the upper bound on the optimum within 1e-6*|best|; "(i) and (ii)" are labeled Example, not an exclusive checklist. The delivered certificate is of form (ii): nonnegative multipliers + rigorous univariate interval B&B on the separable dual.
- Sense: pricing050 maximises objvar = -sum c_i x_i. Code lower-bounds min c·x by weak duality then sets U=-LB; that is an upper bound on max objvar. Bank wording "univariate maximisations" is the dual of the max-form; the min-form used here is equivalent. Not a stretch of the win condition.
- lambda = (e2:0, e3:0, e4:0, e5:3.04890112, e6:2.16775096) lies in R^5_+ (zeros allowed). Null check: lambda=0 yields a useless dual (U near 0), so the pass is not vacuous.
- "250 univariate terms" in the bank example vs 249 terms in the posted .gms: bank example slip; claim correctly works on the posted instance (249). Concavity is proved per (b,p) type covering all terms; the dual B&B does not depend on concavity.
- Concavity example (i): exact Fraction sign check proves the factor b p x^p-(p+1) <= -1 on [0,10]; the arb g'' sweep for p=3 only reaches upper 6e-9 > 0 (interval overestimation), so it is not by itself a clean directed-rounding proof that g''<=0. Recorded as a weakness of the optional (i) illustration only; (ii) alone meets the essential sentence.
- Posted .gms literally contains float-artifact decimals 0.0010000000000000002 and 0.010000000000000002; certificate reads those strings as exact decimals, i.e. the instance as posted (as the bank requires), not a cleaned 0.001/0.01 model.
- "Closes an instance MINLPLib lists as open": status snapshots still show a large dual gap (bestdual -1153 / SCIP -1534 vs primal -1813.8). Mathematical closing within the stated tolerance is what p1 asks for; submitting to the maintainer is outside the partial-win text (full criterion assigns that to the human).
- Full success criterion (strictly better feasible .sol) is not met and not claimed.
- Leaf log: 1958 leaves, per-variable chains cover [0,10] with abutting endpoints (coverage check bad=0); |U - best| ≈ 2.29e-6 << tol ≈ 1.81e-3; U <= bar with margin ≈ 1.81e-3.

## confirmed_scope
confirmed_scope: With object/lambda.txt and the arb-ball interval branch-and-bound leaf log object/cert_arb_leaves.json (1958 leaves), weak Lagrangian duality certifies that max objvar for the posted pricing050 instance (instance/gms_pricing050.gms) is at most -1813.829075713452, which is <= the recorded best primal -1813.829078 plus 1e-6*|best|.

injection_suspected: none
pass: true
