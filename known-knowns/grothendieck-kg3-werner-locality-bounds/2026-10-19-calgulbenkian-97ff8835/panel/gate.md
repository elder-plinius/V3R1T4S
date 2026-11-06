# Honesty gate (grothendieck-kg3-werner-locality-bounds)

status: CONFIRMED_PARTIAL
confirmed_scope: For the paper's d=8 E8 instance (120 x 120 matrix 3G-13I, signs and order arbitrary), the local bound max a^T A b is exactly 6104, so Q/L = 9240/6104 = 165/109 is a proven lower bound for K_G(8); this converts the heuristic value to a proven one (partial win p2) and says nothing about K_G(3).

## Gate notes
- Objects (corrected 2026-11-06, after the review on #525; the line first read "2 files under object/" when object/ held only the matrix): 2 files under object/, dual_certificates.txt (the main object, sha256 in INDEX.csv) and lower_bound_witness.txt, both moved there from verify-it-yourself/data/; the sha256 of each is in SHA256SUMS. The instance matrix d8_n1_120x120.mat is no longer shipped; run_checks.sh fetches it from Zenodo record 10.5281/zenodo.13693164 and checks sha256 a78361f200b669741a4a0636bb4e1027a1e6cdfeca174c84ef67269a17bbeaac.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the package folder; the object's builder (Gemini, Argon) is a different model family from every skeptic.
- Partial win p2 only: a proof that the classical maximum of the E8 instance is exactly 6104, so K_G(8) >= 165/109; the paper already prints 165/109 as a heuristic value, so the new content is the proof, not the number.
