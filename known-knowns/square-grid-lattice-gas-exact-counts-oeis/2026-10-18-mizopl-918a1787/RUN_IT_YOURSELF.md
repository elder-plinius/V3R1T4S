# Run It Yourself — OEIS A089980 Antidiagonal d = 79 (`p2`)

## Fast Verification (~2 seconds)

From the package root directory:

```sh
sh verify-it-yourself/run_checks.sh
```

This runs `verify-it-yourself/check_a089980_ad79.py`, which:
1. Brute-forces the definition of $T(w, m)$ (independent sets on $P_w \times P_m$) for all $0 \le w, m \le 4$ against `verify-it-yourself/b089980.txt`.
2. Recomputes all $814$ published cells for $w = 0..10$ ($w + m \le 78$) and the new antidiagonal-79 entries $T(w, 79 - w)$ for $w = 0..10$ in pure-Python exact big-integer column-transfer arithmetic (`0` mismatches), and checks `object/antidiag79_indep_bigint.tsv` for $w = 0..16$.
3. Independently reconstructs all `40` canonical widths $w = 0..39$ via CRT from `object/residues_hs_mod.tsv` (`1,000` rows, primes in $(2^{30}, 2^{31})$) and from `object/residues_far.tsv` (`1,027` rows, primes in $(0, 2^{30})$), verifying deterministic Miller-Rabin primality of all moduli, 100% prime-set disjointness (`0` shared primes), strict CRT product bounds $\prod p > F(w+2)^{79-w}$, held-out check-prime agreement on all `40/40` widths in both decompositions, and 100% exact decimal string equality across all `80` entries (`n = 3160..3239`) in `object/a089980_antidiag79.txt` and `object/a089980_antidiag79.tsv`.
4. Runs a live fresh-prime DP sweep (`p = 1000000007`, outside both prime sets) at $w = 16, m = 63$ using `verify-it-yourself/hs_mod.py`.
5. Runs a negative control (corrupting line 1 of `a089980_antidiag79.txt`) and confirms it is rejected.

## Full Two-Decomposition Recomputation from Scratch

To recompute any width $w \in \{0, \dots, 39\}$ from scratch using Decomposition 1 (`how-we-built-it/hs_mod.py`):

```sh
python3 how-we-built-it/hs_mod.py exact 20 59
```

To run Decomposition 2 (`how-we-built-it/far.py`) self-test or drive widths $w_0 \dots w_1$:

```sh
python3 how-we-built-it/far.py selftest
```
