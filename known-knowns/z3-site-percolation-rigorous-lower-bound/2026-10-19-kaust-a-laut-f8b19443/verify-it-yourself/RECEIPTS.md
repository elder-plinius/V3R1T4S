# Receipts (real output, copied from the runs on this machine)

## Default: sh verify-it-yourself/run_checks.sh
```
1. integrity: 26 object files checked
2. definitions: walk counts and every c_f agree for N = 3..8 (enumerated from complete paths)
3. chain: sum c_f(N) = a_(N+1) for 11 consecutive pairs; all 15 tables match OEIS A174319 (a_N and a_(N+1))
4. certificate: K_20(263376/10^6) = 0.999971526024 < 1; K_20(p* + 10^-6) = 1.000041779030 > 1; K_20(5/19) = 0.984758991853 < 1
PASS (fast exact checks: p_c^site(Z^3) >= 263376/10^6; GO=1 or FULL=1 reruns the enumerator)
PASS
```

## GO=1 sh verify-it-yourself/run_checks.sh (start and end times from date -u)
```
Mon Oct 19 19:22:03 UTC 2026
1. integrity: 26 object files checked
2. definitions: walk counts and every c_f agree for N = 3..8 (enumerated from complete paths)
3. chain: sum c_f(N) = a_(N+1) for 11 consecutive pairs; all 15 tables match OEIS A174319 (a_N and a_(N+1))
4. certificate: K_20(263376/10^6) = 0.999971526024 < 1; K_20(p* + 10^-6) = 1.000041779030 > 1; K_20(5/19) = 0.984758991853 < 1
PASS (fast exact checks: p_c^site(Z^3) >= 263376/10^6; GO=1 or FULL=1 reruns the enumerator)
enumerator rebuilt: N = 3..14 and 16 reproduced byte for byte
PASS (go: N = 3..14 and 16 reproduced byte for byte)
Mon Oct 19 19:23:00 UTC 2026
```

## FULL=1 sh verify-it-yourself/run_checks.sh
```
Mon Oct 19 19:23:09 UTC 2026
1. integrity: 26 object files checked
2. definitions: walk counts and every c_f agree for N = 3..8 (enumerated from complete paths)
3. chain: sum c_f(N) = a_(N+1) for 11 consecutive pairs; all 15 tables match OEIS A174319 (a_N and a_(N+1))
4. certificate: K_20(263376/10^6) = 0.999971526024 < 1; K_20(p* + 10^-6) = 1.000041779030 > 1; K_20(5/19) = 0.984758991853 < 1
PASS (fast exact checks: p_c^site(Z^3) >= 263376/10^6; GO=1 or FULL=1 reruns the enumerator)
enumerator rebuilt: N = 3..14 and 16 reproduced byte for byte
Mon Oct 19 19:24:07 UTC 2026
N = 18 reproduced byte for byte
Mon Oct 19 19:33:39 UTC 2026
N = 20 reproduced byte for byte
Mon Oct 19 21:59:56 UTC 2026
N = 20, sum of c_f = 14334995983614
f_max = 23: K_N is increasing on [0, 21/44] = [0, 0.477273]; (j+1)/10^6 inside: True
K_N(263376/10^6) = 0.999971526024  ->  PASS: p_c >= 263376/10^6
K_N(263377/10^6) = 1.000041779030  ->  fails (p* is maximal on the grid)
sanity 1/5 (proven bound; must pass): K = 0.005547
sanity 0.3116 (numerical p_c; must fail): K = 21.417580
PASS (full: N = 3..14, 16, 18 and 20 reproduced byte for byte; K_20(263376/10^6) < 1 on the regenerated table)
Mon Oct 19 21:59:57 UTC 2026
```

## Negative controls of check_fast.py (run on throwaway copies of this package, 2026-10-19)
Each changes one rule in check_fast.py's own implementation of the definitions:
- shortcut gap j - i >= 2 instead of >= 3: exit 1, "FAIL (6 problems)" (N = 3..8 all differ);
- every turn corner forced, ignoring the direction-index comparison: exit 1, "FAIL (6 problems)";
- dropping "y not in F" from E: still PASS. This is expected: every site of F is adjacent to some v_i with i < N,
  so that condition is implied by the adjacency condition;
- reversing the direction-index comparison: still PASS. This is also expected. The reversed order is the order of
  a lattice symmetry, (x, y, z) -> (-z, -y, -x), so it is another valid parent rule, and summed over all walks it
  gives identical tables.
