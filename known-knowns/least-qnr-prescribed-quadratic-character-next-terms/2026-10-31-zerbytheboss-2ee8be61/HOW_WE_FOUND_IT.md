# How We Found It

contributor text, unverified

For a prime $q > 2$ to have $p_1 = 2$ as a quadratic residue, $q \equiv 1$ or $7 \pmod 8$. By Quadratic Reciprocity, for any odd prime $p_i$:
- In **Case A ($q \equiv 1 \pmod 8$)**: $(p_i / q) = +1 \iff (q / p_i) = +1$.
- In **Case B ($q \equiv 7 \pmod 8$)**: $(p_i / q) = +1 \iff (q / p_i) = (-1)^{(p_i - 1)/2}$.

Thus, in each mod-8 branch, the condition that the first $k$ primes are quadratic residues modulo $q$ reduces to purely modular residue constraints on $q \bmod p_i$.

We implemented three distinct bit-parallel Chinese Remainder Theorem (CRT) sieves in C99 (`verify_qnr_sieve.c`):
1. **Stage 1 (`A000229(39..40)`)**:
   - **Enumerator 1** combines $M_1 = 8 \cdot 3 \cdot 5 \cdot 7 \cdot 11 \cdot 13 \cdot 17 \cdot 19 \cdot 23 = 892,371,480$ ($142,560$ admissible CRT residues per mod-8 class) with a 20-prime bit-parallel word sieve over $p_{10} = 29, \dots, p_{29} = 109$ across $k \in [0, 355680]$. Starting from $1$, this simultaneously reproduces `A000229(30..38)`, `A002223(30..38)`, and `A002224(30..41)` and proves `A000229(39) = 317398900373231`.
   - **Enumerator 2** combines the 10-prime wheel $M_2 = M_1 \cdot 29 = 25,878,772,920$ ($1,995,840$ admissible CRT residues) with a 28-prime bit-parallel word sieve over $p_{11} = 31, \dots, p_{38} = 163$, independently finding the exact same four primes $q \equiv 1 \pmod 8$ in $[1, 317398900373231]$ for which the first 38 primes are quadratic residues (`112434732901969`, `134035928676049`, `178936222537081`, `229297977151681`).
2. **Stage 2 (`A000229(41..43)`)**:
   - **Enumerator A** ($M_2 = 25,878,772,920$ + 30 sieve primes $31 \dots 173$) and **Enumerator B** ($M_3 = M_2 \cdot 31 = 802,241,960,520$ + 29 sieve primes $37 \dots 173$) independently search $[1, 1463971373078639]$ across both $1 \bmod 8$ and $7 \bmod 8$, finding the exact same 5 primes having the first 40 primes as quadratic residues (`178936222537081`, `501108392233679`, `831583148698319`, `1152240096017111`, `1463971373078639`). The unique prime in this range with least QNR $179 = p_{41}$ is `1463971373078639` ($7 \bmod 8$), proving `A000229(41) = 1463971373078639` and unblocking `A000229(42) = 178936222537081` and `A000229(43) = 501108392233679`.
