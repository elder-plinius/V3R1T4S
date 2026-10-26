# Honesty gate (shannon-capacity-odd-cycles)

status: CONFIRMED_SOLUTION
confirmed_scope: For C15 only, the schedule in object/schedule.json (BPZ grammar, d = 3792, M with 3275 digits) gives Theta(C_15) >= M^(1/3792) strictly above the BPZ Lean repository head value and the 9a.md comment value, assuming the Lean-certified base vector and the BPZ framework; no explicit independent set is exhibited.

## Gate notes
- Objects: 3 files under object/ (sha256 of each in INDEX.csv and SHA256SUMS).
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the package folder; the object's builder (Gemini, Argon) is a different model family from every skeptic.
- Lower bound on the Shannon capacity of C15 from a new schedule in the Buys-Polak-Zuiddam substitution grammar (same rules, terminal codes and base sizes as their Lean-verified CertC15), beating the BPZ Lean head (aa21eeb12b75) value and the older value quoted on Tao's 9a.md page; the margin is small (about 1e-7 to 7e-7) and is a re-tuning inside the published framework, not a new method.
- The base seven-family vectors are taken from the BPZ Lean-verified data; the explicit base vertex sets are not shipped. Every substitution table and terminal code used was checked for separation (Definition 6) in the folder and tested on explicit vertex sets by the reproduce skeptic; the folder reproduces the Lean integer from the Lean schedule as a known answer. The exact schedule here has not been through Lean's kernel.
- Literature search: the arXiv export API was rate-limited (429); the arXiv HTML search found nothing newer than Tandon (arXiv:2608.30273, 31 Aug 2026). Records in this cascade move every few weeks; re-fetch before merging.
