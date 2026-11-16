context: Claude Code subagent, fresh context [Sonnet 5.5]

Verdict on the criterion: the object meets partial win p2 on the x^7 + x^3 + 1 branch, and I found no hidden quantifier or stretched definition.

Condition-by-condition checks. I re-ran the package's own checker and wrote an independent scalar evaluator in a working copy (not shipped).
- Gate basis: object/gf128_0x89_81gates.slp.txt has exactly 81 lines, each AND or XOR, plus the begin/end SLP markers. Count is 32 AND and 49 XOR, so it uses no XNOR, NOT or other gate types.
- No constants: the only wires are A0..A6, B0..B6, t-wires and C0..C6. The package checker explicitly rejects constants and wire redefinition.
- Standard polynomial basis in and out: my evaluator takes inputs A_i = coefficient of x^i and reads outputs C_k the same way. It compares against carry-less multiplication reduced by 0x89 (x^7 + x^3 + 1).
- All input pairs: I checked all 128 x 128 = 16384 pairs and found 0 mismatches. The package's run_checks.sh prints PASS with pairs_checked 16384.
- Gate threshold: p2 allows at most 84 gates for this polynomial. 81 is at most 84.
- File identity: the sha256 matches the claimed 36e8f04d....
- Gate depth: 6 for the package's checker, which matches the package. Depth is not a criterion condition.

"Below any smaller published circuit". This is the one condition I could only partly settle.
- The package lists the NIST and Peralta CMT circuits at 85 gates and Swapnil Jain's circuit at 83 gates; 81 is below all three. I did not re-fetch the NIST or CMT pages.
- I did fetch Jain's README (not shipped in this package). It says only "GF(2^7) in 83 gates", without naming the polynomial, so it neither contradicts nor confirms the 83-gate claim for 0x89.
- I did not search for other published circuits below 81. That is the NOVELTY skeptic's job.

Hidden quantifiers and null models. The claim's own wording stays inside p2. It states that it does not resolve the 25-product problem, and it names the 0x89 branch rather than silently using the easier 0x91 branch. No null model applies, because the claim is an exact exhaustive circuit check. The 81-gate count is an upper bound on circuit size, not a claimed optimum.

Caveats.
- The package's maintainer-review rule says a tie or later upstream value counts against the claim. The claim is two gates better than the best published value it found (83), so a tie is not at issue unless the novelty search finds an 81-or-fewer circuit.
- how-we-built-it/PREREG.md froze p2 at 82 or fewer gates for 0x89. The package met that stricter target, so there is no goalpost shift.

confirmed_scope: object/gf128_0x89_81gates.slp.txt is an 81-gate (32 AND, 49 XOR, no constants) straight-line circuit that multiplies correctly in the standard polynomial basis modulo x^7 + x^3 + 1 on all 16384 input pairs, which is at most the 84-gate p2 threshold and below the 85-gate NIST/CMT circuit and the 83-gate Jain circuit, and it settles neither the 25-product 8-term problem nor p1 or p3.

pass: true
