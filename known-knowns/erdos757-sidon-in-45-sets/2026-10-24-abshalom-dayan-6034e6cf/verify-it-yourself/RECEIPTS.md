# RECEIPTS: real output of sh verify-it-yourself/run_checks.sh

run at 2026-11-07T00:12:54Z (UTC), python3 3.14.7, exit code 0

```
calibration A_base: n 14 m 12 {'three_uniform': True, 'edges_distinct': True, 'linear': True, 'middles_distinct': True, 'middles_not_first_or_last': True, 'm_at_most_n_minus_2': True, 'f7_free': True} alpha 8 OK
object: n 101 m 99 {'three_uniform': True, 'edges_distinct': True, 'linear': True, 'middles_distinct': True, 'middles_not_first_or_last': True, 'm_at_most_n_minus_2': True, 'f7_free': True}
alpha 56 claimed 56 ratio 56/101 below 5/9: True below 4/7: True at least 9/17: True
PASS
control A_base: m 12 true middles realizable affine image of A_base True assignments {'realizable': 948, 'extra_ap': 465, 'coincide': 183} OK
object: induced edges on [1, 2, 3, 4, 95, 97, 98, 99] [(1, 2, 4), (1, 3, 98), (2, 95, 97), (2, 98, 99), (3, 4, 95), (3, 97, 99)] as stated
object: distinct-middle assignments 95 {'extra_ap': 60, 'coincide': 35}
not H(A) for any weak Sidon set A: True
PASS
```

Earlier run, 2026-10-24T12:52:41Z (UTC), python3 3.14.7, exit code 0, before check_not_realizable.py was added: the first four lines above, identical.
