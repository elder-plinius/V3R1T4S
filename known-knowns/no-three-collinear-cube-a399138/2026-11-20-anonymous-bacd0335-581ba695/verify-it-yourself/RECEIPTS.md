== 1. independent line enumeration from the definition ==
grid points: 343
total lines with >= 3 points: 4429
axis-parallel lines: 147
PASS: 4429 total / 147 axis-parallel, matches the claim

== 2. counting identity (each point on exactly 3 axis lines) ==
every one of the 343 points lies on exactly 3 axis-parallel lines
3 * 98 = 294 ; 2 * 147 = 294
PASS: identity holds -- a 98-point admissible set would need EXACTLY 2 points on every axis-parallel line

== 3. the shipped CNF matches this encoding, clause by clause ==
header: 343 vars, 17456 clauses
shipped clause-length histogram: {3: 16427, 6: 1029}
expected clause-length histogram (from the bare definition): {3: 16427, 6: 1029}
PASS: shipped CNF's clause-length histogram matches the at-most-2 / at-least-2 encoding of this definition exactly
my independently rebuilt clause set: 17456 clauses
PASS: shipped CNF is clause-for-clause IDENTICAL to my independent rebuild from the bare definition (17456 clauses, exact set match, zero differences)

== 4. re-verify the shipped DRAT proof ==
 detected empty clause; start verification via backward checking

c 6864 of 17456 clauses in core                            

c 12970 of 19145 lemmas in core using 198268 resolution steps

c 0 RAT lemmas in core; 2606 redundant literals in core lemmas

s VERIFIED

c verification time: 0.356 seconds
PASS: drat-trim verified the shipped proof

== 5. tamper check: a corrupted object must be REJECTED ==
PASS: tampering with the object (one digit flipped) made verification fail, as it must: c verification time: 0.213 seconds

PASS
(literal run_checks.sh output on a clean checkout)
