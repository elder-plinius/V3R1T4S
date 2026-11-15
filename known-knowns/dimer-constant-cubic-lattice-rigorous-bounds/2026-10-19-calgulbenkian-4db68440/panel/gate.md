# Honesty gate (dimer-constant-cubic-lattice-rigorous-bounds)

status: CONFIRMED_PARTIAL
confirmed_scope: The 3D monomer-dimer entropy h3 of Z^3 (growth of the total number of matchings at unit activity, FKLM's sup over density) satisfies h3 <= 0.7859681, by exact integer Collatz-Wielandt on the full 1048576-state monomer-dimer diagonal-layer matrix at (m,n) = (5,4) (ratio 1891821269973664/281869529, log/20 = 0.7859680768...), below FKLM's 0.7862023450 by 2.34e-4, resting on a written but unpublished extension of He's argument that I re-derived with no gap; the currency of the comparator is left to the novelty skeptic.

## Gate notes
- Objects: 4 files under object/ (sha256 of each in the package's INDEX.csv and SHA256SUMS).
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim package; the object's builder (Gemini, Argon) is a different model family from every skeptic.
- Partial win p2: h3 <= 0.7859681 (exact 0.785968076809, rounded up) on the 3D monomer-dimer entropy at unit activity, by exact integer Collatz-Wielandt on the full 2^20-state monomer-dimer diagonal-layer matrix at (m,n)=(5,4), below the published rigorous 0.7862023450 (Friedland and Peled; Friedland, Krop, Lundow and Markstrom) by 2.34e-4. The derivation is the same unpublished extension of He (arXiv 2607.28810) used for the (3,3) bound, re-derived at (5,4) by the criterion skeptic.
- This supersedes the author's own open PR #537 (h3 <= 0.7860441 at (3,3)) on the same target; on the operator's instruction the package replaces #537's in place rather than filing a second PR.
- Before the panel, the derivation (at (3,3)) was reviewed read-only by a model of a different family (OpenAI gpt-6.1-sol); only (m,n) changes here, and the criterion skeptic checked every (m,n)-dependent step.
