# Criterion skeptic

context: fresh subagent; read only the claim package and my own evidence, with no other run, attempt, or panel material.

confirmed_scope: The supplied object proves A(35,6,6) >= 2225.

## Independent mathematical evidence

I wrote and ran `panel/criterion-evidence/check_exact.py` before opening `claim/verify.py`. It implements Hamming distance directly as the count of unequal characters and exhaustively checks every unordered pair. It uses no search engine, seed, or author's checker logic. Run it with ordinary `python3` (without `-O`, since assertions enforce validation).

`panel/criterion-evidence/exact-result.json` confirms:

- Exactly 2225 distinct strings, each exactly 35 characters from the alphabet {0,1}, each with exactly six ones.
- All 2,474,200 unordered pairs examined. Minimum distance is exactly six; distance counts are 134,252 at six, 526,478 at eight, 1,094,176 at ten, and 719,294 at twelve.
- File SHA256 matches the claim: `dc410a8170c014dec4c8b728a2da9d03dd29cc55a5f1c13fae80d22858d009de`.
- A positive control of two disjoint weight-three words passes. Separate negative controls for cardinality, width, alphabet, weight, distinctness, inadequate distance, and odd target distance are rejected for the intended reason.
- I explicitly constructed every bitwise complement and repeated the full checks for length 35, weight 29, distance six, cardinality 2225. The distance histogram is identical. Thus the same certificate proves A(35,6,29) >= 2225; complement symmetry is not an assumption about the file.

Only after that completed did I read and run `claim/verify.py`. Its integer XOR all-pairs test and additional four-subset test agree; execution evidence is in `panel/criterion-evidence/author-result.txt`.

## Literal target and hidden quantifiers

The full primary success condition in `claim/target.md` is a strict lower-bound improvement for some constant-weight cell, not optimality. The supplied finite list is the explicit witness: there is no omitted universal quantifier over seeds, random runs, or every possible code. There is a universal quantifier over every pair of distinct listed words, which the exhaustive check discharges. Evenness of d is satisfied by d=6.

Taking the comparison numbers in `claim/CLAIM.md` as inputs, 2225 > 2217 by eight and 2225 > the stronger pending value 2218 by seven. Also 2225 <= 3249, so the supplied object does not exceed the reported tabulated upper bound. Neither equality with a former lower bound nor the partial p1 exception is being used. This is not an improved-upper-bound claim and does not invoke p2. It makes no optimality claim.

The target additionally quantifies over the live table and mirror cell, both named arXiv papers, and any newer arXiv paper. `claim/PREREG.md` additionally requires the strongest pending-PR value and Johnson propagation. Merely verifying 2225 > 2218 does not establish all those dated premises. The claim package's table record is metadata, not a complete live table or literature audit. This report therefore does not certify global literature completeness, the current upper-bound source, or the absence of a stronger bound propagated from another cell. Those are explicitly reserved to the separate novelty reviewer: it must confirm a strongest relevant lower bound strictly below 2225, the mirror comparison, and a current upper bound at least 2225. If any applicable lower bound is already 2225 or greater, this remains a valid code but fails the full strict-improvement target.

The null-test exception is explicit in `claim/PREREG.md` and applies: this claim is an explicit combinatorial object checked deterministically, not a statistical performance or beats-chance claim. Positive and negative validator controls are supplied nonetheless. No null distribution, search success probability, or stochastic benchmark is required to prove this existential bound.

## Verdict

All mathematical evidence needed for the full lower-bound witness is present and independently verified. This positive criterion verdict is contingent only on the separate novelty reviewer confirming the dated comparison baseline required above; there is no missing certificate or mathematical check. It must not be interpreted as an unconditional global novelty verdict.

pass: true
