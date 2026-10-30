# Penney's Game for Permutations: Rigorous Certification of Conjecture 6.1 for S_4 (Partial Win p1)

## What

Partial win p1: rigorous certification that Bob's right cyclic rotation beats Alice's pattern with Pr(sigma precedes tau) < 1/2 across all 24 permutations in S_4, each certified by an exact big-integer horizon certificate (A(H)+R(H))/H! < 1/2 at H <= 36; accompanied by exact two-sided rational intervals for all 120 permutations of S_5 at H = 16.

## Check It Yourself

Run the standalone verification suite:
```bash
sh verify-it-yourself/run_checks.sh
```

This verifies:
1. Presence of all 24 permutations in $S_4$ in `object/s4_certificates.json`.
2. For each permutation, tau is the right cyclic rotation $(\sigma_4, \sigma_1, \sigma_2, \sigma_3)$.
3. Exact partition equality $A(H) + B(H) + R(H) == H!$ in exact big integer arithmetic.
4. Rigorous tail inequality $2(A(H) + R(H)) < H!$, certifying $\Pr(\sigma \prec \tau) < 1/2$.
5. Complementary Bob win inequality $2 B(H) > H!$, certifying $\Pr(\tau \prec \sigma) > 1/2$.
6. Bit-for-bit exact reproduction of the $2341 \to 1234$ benchmark at $H=36$.
7. Presence of all 120 permutations of $S_5$ in `object/s5_rational_intervals.json` across 60 complement-symmetry classes.
8. Exact integer partition $A(16) + B(16) + R(16) == 16! == 20,922,789,888,000$.
9. Invariance under complement symmetry: $(A, B, R)(\sigma) == (A, B, R)(\sigma^c)$.
10. Conjectural direction audit: $B(16) > A(16)$ for all 120 permutations, confirming zero counterexamples to Conjecture 6.1 in $S_5$ with minimum conditional win ratio $B/(A+B) \ge 54.78\%$.

## Compared To

- **Prior Literature**: Sergi Elizalde and Yixin Lin (*Penney’s Game for Permutations*, Discrete Mathematics & Theoretical Computer Science 28:1 (2026), arXiv:2404.06585) proved Conjecture 6.1 for $S_3$ analytically, but presented only numerical approximations by truncating series at $n = 11$ for $S_4$ and $S_5$, leaving the remaining tail uncertified.
- **Our Advance**: We provide the first mathematically rigorous big-integer certificates proving that Bob's right rotation beats Alice's pattern for every single permutation in $S_4$ (Partial Win p1), and compute exact large-horizon rational bounds and integer counts for all 120 permutations of $S_5$.

## Not Claimed

- We do not claim an analytical proof of Conjecture 6.1 for arbitrary $k$.
- We do not claim full finite-horizon crossing certificates $(A(H)+R(H))/H! < 1/2$ for all of $S_5$, as $R(16)/16! \approx 0.852$ leaves the tail wide; we provide exact two-sided rational intervals $[A/16!, (A+R)/16!]$ and verified that Bob's win ratio $B/(A+B) > 54.78\%$ holds across all 120 permutations of $S_5$ with zero counterexamples.
- We do not claim a counterexample refuting Conjecture 6.1 (our searches in $S_4, S_5, S_6$ found zero counterexamples).

## Credits

- Sergi Elizalde and Yixin Lin for formulating Penney's game for permutations and posing Conjecture 6.1 (DMTCS 2026, arXiv:2404.06585).
- Walter Penney for inventing the original nontransitive pattern-matching game (1969).
