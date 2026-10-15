# RECEIPTS: real output of `sh verify-it-yourself/run_checks.sh` from a clean copy of this package

Run at 2026-10-15T09:13:55Z (macOS, Python 3.9.6); the exit status follows the output.

```
== lb_check.py (variance form and literal loss-difference definition), exit 0
environments: 2
distinct report pairs: 4
LB_variance_form: 1652448303171916717080006468042849/70681471350112364987160770000000000
LB_literal_definition: 1652448303171916717080006468042849/70681471350112364987160770000000000
LB_float: 0.023378804538
bar: 31/1326 (0.023378582202)
two_computations_agree: yes
LB_strictly_greater_than_bar: yes
margin: 612886837595654297197253671111/2756577382654382234499270030000000000 (2.223e-07)
verdict: LOWER_BOUND_BEATS_BAR
== independent_recheck.py (normalised-posterior route), exit 0
independent LB: 1652448303171916717080006468042849/70681471350112364987160770000000000
float: 0.023378804538274
bar 31/1326 = 0.023378582202112
strictly greater than bar: yes
margin: 2.223362e-07
== check_declared_fields.py (declared mu and reports against the structure), exit 0
env 0 expert 0: weight 1/2, theta ['0', '33307/40000'], mu 417121/1000000, reports ['6693/40000', '33307/40000']
env 0 expert 1: weight 1/2, theta ['0', '33307/40000'], mu 417121/1000000, reports ['6693/40000', '33307/40000']
env 1 expert 0: weight 1/2, theta ['6693/40000', '1'], mu 582879/1000000, reports ['6693/40000', '33307/40000']
env 1 expert 1: weight 1/2, theta ['6693/40000', '1'], mu 582879/1000000, reports ['6693/40000', '33307/40000']
declared fields consistent: yes
three exact computations agree: LB = 1652448303171916717080006468042849/70681471350112364987160770000000000 > 31/1326; declared fields consistent
PASS
exit status: 0
```

## Corrupted-object test (on a second copy, 2026-10-15T09:13:56Z)

The same rule `kit/check_run.py` uses: change the middle digit of `object/mixture.json`. It lands in a declared field
(`mu` of the first environment) that the two bound computations do not read, so they still print the true bound; the
field check rejects the file. Last lines of the output:

```
changed one digit (the rule kit/check_run.py uses): line 49 "mu": "417121/1000000" -> "mu": "417121/1000001"
problem: env 0: declared mu 417121/1000001 but prior and states give 417121/1000000
declared fields consistent: no
mismatch: lb_check exit 0 (variance 1652448303171916717080006468042849/70681471350112364987160770000000000, literal 1652448303171916717080006468042849/70681471350112364987160770000000000, verdict LOWER_BOUND_BEATS_BAR); independent_recheck exit 0 (1652448303171916717080006468042849/70681471350112364987160770000000000, greater yes); declared fields exit 1 (no); expected 1652448303171916717080006468042849/70681471350112364987160770000000000
FAIL
exit status of run_checks.sh: 1
```

## Every single-digit change (2026-10-15T09:08:02Z to 09:17:09Z, on a copy of this package)

Each of the object's digits in turn was changed by the same rule (to `1`, or to `0` if it was `1`), and
`sh verify-it-yourself/run_checks.sh` was run on the changed copy. Output:

```
digit positions tried: 343; corrupted copies that still PASS: 0
```
