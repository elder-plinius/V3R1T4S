# Honesty gate (dimer-constant-cubic-lattice-rigorous-bounds)

status: CONFIRMED_PARTIAL
confirmed_scope: A certified Z^4 dimer-constant bound l4 <= 0.5840147694 (0.584015 rounded up) from the four-dimensional diagonal-layer matrix at (3,3,2), against the cited Butera-Federbush-Pernici table value ln(8!)/16 = 0.66278769, resting on a written but unpublished extension of He's argument that I re-derived with no gap; whether a better published Z^4 upper bound exists is not settled by this report.

## Gate notes
- Objects: 2 files under object/ (sha256 of each in the package folder's INDEX.csv and SHA256SUMS).
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the package folder; the object's builder (Gemini, Argon) is a different model family from every skeptic.
- Partial win p3: l4 <= 0.5840147694 (exact 0.584014769338, rounded up; 0.584015 to six places) on the Z^4 dimer constant, below the Butera-Federbush-Pernici upper bound ln(8!)/16 = 0.66278769. The author printed 0.5840147693, which is rounded down and not an upper bound; the folder corrects it. The four-dimensional extension of He's argument is the author's own and unpublished; it was checked step by step by the cross-family review and the criterion and reproduce skeptics.
- Before the panel, the four derivations were reviewed read-only by a model of a different family (OpenAI gpt-6.1-sol): it found He's Theorem 2.1 applied within its hypotheses, the periodic-slab trap avoided by He's construction, the iterated Collatz-Wielandt direction correct, and both unpublished extensions proved; it saw the derivations only, not the certificates, which the panel then checked.
