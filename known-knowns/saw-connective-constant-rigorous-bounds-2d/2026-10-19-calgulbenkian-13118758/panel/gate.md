# Honesty gate (saw-connective-constant-rigorous-bounds-2d)

status: CONFIRMED_PARTIAL
confirmed_scope: Assuming the exact ratio 169287/92732 on the matrix defined by object/AUTOMATON.md and the shipped vector is reproduced, mu(4.8^2) <= 1.825551050339 is a proved rigorous upper bound (Grimmett-Li Theorem 4.3 and Proposition 4.2 for bridge growth, a complete pocket-pruning proof), below Alm's published 1.829254 and the bank's 1.82926 by about 3.7e-3, meeting p1 for the 4.8^2 lattice only.

## Gate notes
- Objects: 18 files under object/ (sha256 of each in the package's INDEX.csv and SHA256SUMS).
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim package; the object's builder (Gemini, Argon) is a different model family from every skeptic.
- Partial win p1 (the 4.8^2 lattice): mu <= 169287/92732 = 1.825551050339 (rounded up) from a loop-length-34 automaton (16,873,086 states) with two finite-pocket pruning tests and an ordered subset-inclusion invariant, below the published rigorous 1.829254 (Alm 2005; 1.82926 in Jensen 2004 Table 3) by about 3.7e-3. The certified ratio is for the shipped vector, rounded to a 16-bit mantissa to fit the package limit; it is 2.8e-5 above the author's figure 1.825523195381, which is not claimed.
- The pruning tests are new relative to the k = 30 and k = 32 bounds. Their soundness rests on a written proof (object/THEOREM.md), which uses the Grimmett-Li bridge theorem (Locality of connective constants, Theorem 4.3 with Proposition 4.2), with every hypothesis checked for 4.8^2. No published source for this exact pruning was found; it is the author's own adaptation of ideas of Alm, Couronne and Ponitz-Tittmann.
- Before the panel, the proof and checker were reviewed read-only by a model of a different family (OpenAI gpt-6.1-sol): CLEAN WITH FIXES, seven findings, all applied before the panel and confirmed present by the reproduce skeptic.
- The author's generator has an indexing slip in its second pass (candidate lists indexed by all free neighbours); a corrected copy gives the same states and ratio, and the checker follows the corrected definition.
- This supersedes the k = 32 bound now in the author's open PR #534 (which replaced the k = 30 bound there); on the operator's instruction the package replaces #534's in place.
