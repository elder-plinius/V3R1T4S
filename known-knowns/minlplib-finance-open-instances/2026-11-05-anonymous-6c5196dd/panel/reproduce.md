# REPRODUCE verdict — pricing050 partial win p1

context: subagent

## Definition used (quoted from instance/gms_pricing050.gms)

- Maximize `objvar` with `e1: (-sum_i c_i x_i) - objvar =E= 0`, hence `objvar = -sum c_i x_i`.
- Constraints `e2..e6`: `(-sum_i a_ji x_i exp(-b_ji x_i^{p_ji})) =L= -rhs_j`, i.e. `sum_i a_ji x_i exp(...) >= rhs_j`, with `(rhs_2..rhs_6) = (500, 651, 615, 788, 984)`.
- Bounds: `x2..x51` each in `[0,10]`.
- Decimal model coefficients read as exact decimals (CLAIM.md).
- Instance sha256 of `instance/gms_pricing050.gms`: `192dd92d69cdcd131462d40c137df73dc101afef0739cc7ba98c130a79313715` (recomputed, matches CLAIM.md).

Equivalent minimize `F = sum c_i x_i`. Weak Lagrangian duality with multipliers `lambda >= 0`:

```
theta(lambda) = sum_j lambda_j * rhs_j + sum_i min_{x in [0,10]} h_i(x)
h_i(x) = c_i x - sum_j lambda_j * a_ji * x * exp(-b_ji * x^{p_ji})
```

Any rigorous lower bound `LB <= theta(lambda)` yields upper bound `U = -LB` on `max objvar`.

## Own checker (written before reading code/)

- Parsed all of `e1..e6` from `instance/gms_pricing050.gms` independently (249 NL terms: 50+50+50+49+50; e5 omits x22; objective zeros at x5,x10,x27,x43).
- Multipliers from `object/lambda.txt`: e2=0, e3=0, e4=0, e5=3.04890112, e6=2.16775096 (matches `object/cert_arb_leaves.json`).
- Exhaustive check of all 1958 leaves in `object/cert_arb_leaves.json`:
  - each variable's `leaf_list` covers `[0,10]` with no gaps (Decimal endpoints);
  - for every leaf `[lo,hi]` with claimed lower bound `L`, adaptive Arb ball arithmetic (python-flint, prec 256) proves `h_i(x) >= L` on that interval.
- Decisive command output lines:

```
parsed e2: 50 terms
parsed e3: 50 terms
parsed e4: 50 terms
parsed e5: 49 terms
parsed e6: 50 terms
total NL terms 249 nonzero c 46
lambda OK {'e2': '0', 'e3': '0', 'e4': '0', 'e5': '3.04890112', 'e6': '2.16775096'}
...
x51: leaves=15 min_claimed=-4.261819966845019571305261E-8 ok_so_far=1958 fails=19
n_leaves 1958 n_ok 1958 failures 19
```

(`failures 19` were only digit-serialization mismatches between each var's `lower` field and `min(leaf_list claims)`; differences ~1e-23..1e-33. All 1958 leaf inequalities verified.)

- Reassembled dual bound from verified printed leaf claims:
  - `const = sum lambda_j*rhs_j = 4535.60102720`
  - `LB_leaf = const + sum_i min(leaf claims) = 1813.829075713452364776297282`
  - `U_leaf = -LB_leaf = -1813.829075713452364776297282`
- JSON `LB_lower = 1813.82907571345236477629709126` equals truncated `const + sum(var.lower fields)` and is `<= LB_leaf`, hence also a valid LB.
- Claimed `U = -1813.829075713452364776297` matches that truncated dual value.
- Success criterion check (status/minlplib.solu `=best= pricing050 -1813.8290780000`):
  - `tol_U = -1813.829078 + 1e-6*| -1813.829078| = -1813.827264170922`
  - `U_leaf <= tol_U` and `U_leaf <= -1813.829075713452` (claimed bound).

## Finding

Independent Arb-ball verification of all 1958 covering leaves, plus dual reassembly from `object/lambda.txt` and the leaf log, confirms `max objvar <= -1813.829075713452...`, within `1e-6 * |best|` of the posted primal `-1813.829078`.

pass: true
