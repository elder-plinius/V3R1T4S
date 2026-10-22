# Honesty gate (dimer-constant-cubic-lattice-rigorous-bounds)

status: CONFIRMED_PARTIAL
confirmed_scope: The folder reproduces all 12 entries of He's Table 2, (2,2) to (6,3) at p = 4 and (5,5) at p = 2, rounded up to six decimals by exact integer arithmetic (seven confirmed by my own exact-integer recomputation, the rest by the folder's records), and it is a reproduction only, not a new bound.

## Gate notes
- Objects: 3 files under object/ (sha256 of each in the package folder's INDEX.csv and SHA256SUMS).
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the package folder; the object's builder (Gemini, Argon) is a different model family from every skeptic.
- Partial win p1: an independent exact reimplementation reproducing all 12 entries of He's Table 2 to six decimals rounded up, including 0.452130 at (5, 5); reproduction only, as p1 defines it. The author's RESULTS.md has two wrong ten-digit figures, (5,4) and (6,3); the six-decimal values are unaffected.
- Before the panel, the four derivations were reviewed read-only by a model of a different family (OpenAI gpt-6.1-sol): it found He's Theorem 2.1 applied within its hypotheses, the periodic-slab trap avoided by He's construction, the iterated Collatz-Wielandt direction correct, and both unpublished extensions proved; it saw the derivations only, not the certificates, which the panel then checked.
