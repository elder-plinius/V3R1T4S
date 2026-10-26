# Criterion report, shannon-c23

context: Claude Code subagent, fresh context [claude-sonnet-5-5]

Target: shannon-capacity-odd-cycles, cell C23. Claim: a recursive construction of 3088 digits in C_23^(box 2928), a full win (no partial win claimed). Compared against: BPZ Lean repository head CertC23.lean (d=3040, 11.3345579227...) and the 9a.md comment value 11.328224257774.

Success criterion (quoted from the target's success criterion): "an explicit independent set S in C_m^{box d} ... verified exhaustively, or a fully specified recursive construction whose every finite ingredient is explicitly listed and verified and whose limiting rate is independently re-derived, giving a lower bound on Theta(C_m) (|S|^(1/d), computed with mpmath to 30 digits) STRICTLY GREATER (direction: max) than the best lower bound for that m at verification time ... using the record's exact digits. A finite-dimension set must beat the asymptotic record itself, not just an earlier fixed-dimension value."

Package hashes checked against the contributor's hash list: all OK.

## Clause by clause

1. Route. No explicit set is shipped (the set has about 10^3087 elements), so only the second route applies. Met as a route only if clause 2 holds.

2. Every finite ingredient explicitly listed and verified. MET, with one dependency stated.
   - The base seven-family vector w0 (sizes for the base port system, from the Lean-verified data of the BPZ repository) is listed in the schedule file. It is not re-verified in the folder (open question 1). It is corroborated twice: the folder's checker recomputes the Lean repository's own published integer for this cycle from the same w0 (known-answer test passes in RECEIPTS.md), so w0 and the tables match what Lean certifies; and the base data is third-party formally verified. I take this as 'verified' for the criterion because the claim is a schedule inside a published formally verified grammar, but I note it is a citation of verification, not a re-run.
   - The substitution tables and terminal codes are listed in rules.json as data; the folder's checker verifies Definition 6 admissibility and pairwise separation of the terminal code (RECEIPTS.md, 0 violations), and two negative controls reject a corrupted table and a changed base entry.
   - There are no Tandon-style certificates here; every ingredient is the BPZ grammar. The combination of children of different exponents rests on BPZ's Proposition 1 (general, published, and formalised there), not on a new lemma.
   Residual risk: the new schedule itself is not in the Lean repository, so Lean's kernel has not checked this exact DAG; the validity is the validity of the grammar plus the checked tables. That is the same standard the record being beaten (the Lean head value) meets, and it satisfies 'fully specified recursive construction'.

3. Limiting rate independently re-derived. The bound is a finite-d value M^(1/d); there is no limit. Not applicable; the exact integer and its root were recomputed by triage's separate checker, per the claim record (not shipped), and by my own root comparison from the shipped integer.

4. Strictly greater than the best lower bound. Met. Own check: the root 11.33455800536622830135329115399285797338312702840016... exceeds the Lean head root and the 9a.md comment value; the bank's 'best known' for these cycles is the max over the table's comments and newer sources, and the Lean head is the higher of the two (so beating it is the binding comparison). Margins are about 1e-7 to 1e-8, far above the 30-digit precision the bank requires, so no rounding issue. The bank text lists no live-table row for C23 beyond the comment; the Lean head was re-checked live (unchanged head aa21eeb12b75).

5. Null model and subsumption. The improvement is a different schedule at a different degree inside the same grammar (d=2928), not a power or truncation of a listed set. A bound M^(1/d) at a different d does not follow from the record's integer by any propagation rule, so the PR 350 rule does not subsume it. It is, however, a small re-tuning (order 1e-7 or 1e-8), not a new idea; the criterion asks only for strictly greater, so that does not matter. Hidden quantifiers: the criterion requires 'the best lower bound for that m at verification time', including newer arXiv results; I could not complete an arXiv search (HTTP 429), so currency rests on the novelty skeptic.


Live check (one fetch, 2026-10-20T03:16Z): the 9a.md file has sha256 92f6e1ee5d72...d9899, HTTP 200, byte-identical to the copy the-record-we-beat/README.md reports, so the primary table has not moved (Tandon remains the top C7 entry; the other odd cycles appear only as BPZ version-1 comment values). The BPZ Lean repository commit list (GitHub API, HTTP 200) still has head aa21eeb12b75 dated 2026-08-10. The arXiv API returned HTTP 429 twice (03:16Z and 03:17Z), so I could not search for newer arXiv results; that is left to the novelty skeptic and is recorded as unresolved.
Own arithmetic check (my own script, not shipped in this package; mpmath at 80 digits, reading M from the shipped contributor JSON and the record integers from the-record-we-beat/records.json): digits of M, d, and the roots reproduce the numbers in README.md; M^(1/d) is strictly greater than every listed record, compared by logarithms (log M / d against log M_rec / d_rec). I did not re-derive M from the schedule (that is the reproduce role).

Verdict: the claim is a fully specified schedule in a published, formally verified grammar, its tables are checked in the folder, its base data is Lean-certified and cross-checked by a known-answer reproduction, and its bound strictly exceeds the record. By the literal text it meets the full success criterion, conditional on the novelty skeptic finding no newer public value.

confirmed_scope: For C23 only, the schedule in object/schedule.json (BPZ grammar, d = 2928, M with 3088 digits) gives Theta(C_23) >= M^(1/2928) strictly above the BPZ Lean repository head value and the 9a.md comment value, assuming the Lean-certified base vector and the BPZ framework; no explicit independent set is exhibited.

pass: true
