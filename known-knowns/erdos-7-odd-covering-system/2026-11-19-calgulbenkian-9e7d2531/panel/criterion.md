context: Claude Code subagent, fresh context [Sonnet 5.5]

# CRITERION report, package 9e7d2531 (erdos-7-odd-covering-system, claimed partial win p2)

Check of p2 word for word: "A rigorous proof raising the lower bound on L strictly above 11,486,475 (Egeozturk, forum Aug 2026), rechecked by independent code."

## Package checks, run in a copy of this package
- `sh verify-it-yourself/run_checks.sh` prints PASS (about 9 s).
- Both exact verifiers pass. The C `__int128` verifier prints VERIFY_C: PASS. The Python `fractions` verifier prints VERIFY_PY: PASS.
- The counts they print are 30147 abundant initial-prime profiles, 7036 band profiles, 2519 refuted by pure deletion and 4517 refuted by a certificate row.
- A corrupted certificate row is rejected (VERIFY_C reports a mismatch, and the script prints FAIL).
- The files listed in SHA256SUMS match.

## My own recheck
I wrote a separate script from the lemma statements in README.md. It enumerates the profiles itself and recomputes the pure-deletion bound and the distortion bound for every row of object/lcm_lower_bound_certificate.tsv.
- The counts match: 30147, 7036, 2519 and 4517.
- All 4517 certificate fractions match exactly.
- The worst covered measure is 16615714572403899891/16710819340101877760, which is below 1.
- Every abundant profile at most B0 scales by a power of 3 into the band.

## Clause-by-clause verdict

1. Is the proof rigorous and complete, covering every L below the claimed bound?
   - I found no hidden quantifier. The reduction is for an arbitrary odd distinct covering with L at most B0 = 168,131,152,814,624. It has three steps.
     - Lemma 1 replaces the primes of L by the first odd primes using base-p digits. This is the Berger-Felzenbaum-Fraenkel argument, and the proof is given in the README.
     - Lemma 2 scales the exponent of 3 into a band that the enumeration covers completely.
     - Lemma 3 completes the pure prime-power classes. The fact that any class meeting an earlier pure class is contained in it makes the replacement valid.
   - Lemma 4(1), the pure-deletion product bound, I recomputed and it is correct.
   - Lemma 4(2) and Lemma 5, the capped fibre kernels and the nested convex comparison, I checked by hand.
     - The algebra for the integral over B_i checks out.
     - The conditional-probability caps are sound.
     - The coordinate-by-coordinate conditioning is sound, because the weights are nonnegative and the later conditioning variables are independent.
     - The convex comparison, the use of nested alpha_j and the counting of active classes by exponent vector all look valid.
   - Weak points:
     - The proof is prose, with no Lean or other formal check.
     - Lemma 5's application is compressed into one paragraph.
     - The 4517 certificate rows are only arithmetic evidence if that paragraph is right.
   - I read it as sound but not fully machine-checked. I did not find an error.

2. Is the recheck code independent?
   - Only partly.
     - The C and Python verifiers run the same algorithm and read the same certificate.
     - They share the same author and the same formulas.
     - They verify only the arithmetic of the formula. They do not check any lemma.
   - My own implementation from the lemmas agrees, but it uses the same formulas too.
   - The p2 clause says only "rechecked by independent code", and this meets it literally. It is not independent of the proof's reasoning.

3. Does the README say "from first principles without external axioms", and is that accurate?
   - The first line of the README says "proved from first principles without external axioms".
   - It is accurate in the informal sense. All five lemmas are proved in the README, and the cited literature is credited for the method, not used as an input.
   - It is not a formal "axiom-free" proof (no Lean and no `#print axioms`). The p2 clause does not require one.

4. Is the claimed number exactly the bound proved?
   - Yes. All L at most 168,131,152,814,624 are excluded, so L is at least 168,131,152,814,625 = 3^4*5^3*7^2*11^2*13*17*19*23*29.
   - That value is odd. The README states that L equal to that value is not excluded, so it does not claim more than is proved.
   - It is a proved bound, not a search limit. The enumeration is complete and exhaustive over all profiles.

## Limits
- I did not check novelty. The README cites arXiv 2611.15110 (Dai et al., 11 Nov 2026) on the same method. If it already gives an L bound at or above this one, a tie is not a record. That belongs to the novelty role.
- The 11,486,475 bar is cleared by a factor of 14,637,315 if the proof stands.

confirmed_scope: Assuming the prose proof's Lemmas 1-5 are sound (I found no error), no covering of Z by distinct odd moduli greater than 1 has lcm L at most 168,131,152,814,624, so L is at least 168,131,152,814,625, which is strictly above 11,486,475. All 7036 band profiles are refuted by exact rational certificates that two package verifiers and my own re-implementation reproduce.

pass: true
