# Honesty gate (monomer-dimer-square-lattice-constant-digits)

status: CONFIRMED_PARTIAL
confirmed_scope: For the monomer-dimer entropy h2 of the square lattice (natural log, per site), the shipped certificate vectors for the cylinder transfer matrices of circumference 22 and 24 give, through exact integer Collatz-Wielandt ratios and the two proved inequalities, the rigorous enclosure 0.6627989728337138109756 <= h2 <= 0.6627989728337490653104, certifying 13 decimals; nothing wider is confirmed (no claim on the main criterion, none on novelty beyond the two quoted comparators).

## Gate notes
- Objects: 7 files under object/ (sha256 of each in the package folder's INDEX.csv and SHA256SUMS).
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the package folder; the computation was also done by a Claude Code subagent, so builder and skeptics are the same model family (Claude), which is disclosed here.
- Partial win p1. The proof and checker were reviewed before the panel by a model of a different family (OpenAI gpt-6.1-sol, read-only, verdict clean with fixes); its three display and wording fixes were applied before the panel and are listed in the claim record (not shipped).
- The reproduce skeptic rebuilt the width-22 and width-24 cylinder checks with its own C and big-integer code and re-derived both inequalities; the ratios and the enclosure agree digit for digit.
- Rigorous: an enclosure from exact-integer Collatz-Wielandt certificates with outward-rounded logarithms; the certificate vectors are published in object/.
