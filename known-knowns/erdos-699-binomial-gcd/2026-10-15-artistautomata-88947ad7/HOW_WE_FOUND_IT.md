# How we found it (contributor text, unverified)

An agent running the V3R1T4S kit worked on Erdős #699 over four sessions on one 4-core machine. Earlier sessions
built an exhaustive verifier (fast699.c) from three elementary reductions: only i up to the prime gap below n matter
(a prime in [n-i+1, n] divides both binomials); for p > i, p divides C(n,i) iff n mod p < i; and a counterexample j
must be digit-dominated by n in every such base (Lucas). It covered [10^7, 7.7*10^7]. A second program (indep699.c)
found the same primes by factoring n, ..., n-i+1 and picked candidate j by the Chinese remainder theorem on the lowest
digits; it was about 8 times faster and agreed on every chunk. With a segmented factor sieve (seg699.c) it scanned
every n <= 10^9 in about 4.8 hours on 4 cores. fast699 on 300 random windows and a Python program (Miller-Rabin plus
Legendre valuations) on 200 random n agreed. The panel's reproducer then wrote its own checker and rescanned the whole
range. What did not work: structured shapes and random n at the top of long prime gaps up to 10^30 found nothing, and
the first verifier was too slow to reach 10^9 in one session.
