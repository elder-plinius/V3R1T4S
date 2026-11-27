# How we found it (contributor text, unverified)

The run's charter was seeded at random (number hunts and packings; method cards "footnotes", "same-object",
"oldest-source"). Its first quarry was A000229(39), but the scout found that an earlier pull request
(elder-plinius/V3R1T4S#862) already covered A000229(39..43) and, in its "Not claimed" note, left A002224(42) open, a
next index that the bank target names directly.

Since every prime q = 1 mod 8 has (p/q) = (q/p), the condition is a set of residue classes. A CRT wheel modulo
8*3*5*...*31 (about 30 million admissible residues) with cheap byte-table filters ran through 3.7e11 candidates up to
10^16 in a few minutes on 4 cores. It reproduced A002224(30..41) from 1 and found 6072205049848081 as the least prime
with the first 42 primes QR (in fact the first 44). A second, separately written enumerator (different modulus,
residues by direct scan, Euler's criterion directly) produced the identical list of 95,181 primes. Three fresh
skeptic sessions then checked it: one ran its own doubly focused enumeration from 1 to the value. Nothing failed along
the way except the first target (already taken).
