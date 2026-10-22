# Honesty gate (monomer-dimer-square-lattice-constant-digits)

status: CONFIRMED_SOLUTION
confirmed_scope: The numerical value h2 = 0.662798972833745915155196234397725566 (36 decimals, natural log per site) is reproduced from the shipped data and agrees numerically between the corner-transfer-matrix ladder (four rungs sharing 43 decimals, 30 under the pre-registered stop rule) and the open-strip Wynn extrapolation (four truncations sharing 36 decimals), with no error bound, and exceeds every published value found in arXiv and OEIS searches (Google Scholar not searched).

## Gate notes
- Objects: 50 files under object/ (sha256 of each in the package folder's INDEX.csv and SHA256SUMS).
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the package folder; the computation was also done by a Claude Code subagent, so builder and skeptics are the same model family (Claude), which is disclosed here.
- The digits are numerical agreement of two independent methods (corner transfer matrix A, open-strip transfer matrices with Wynn extrapolation B3) under the criterion's stability rule; there is no rigorous error bound.
- Disclosed post-hoc elements: the first periodic-strip method under its pre-registered recipe reached only 15 decimals; a periodic variant chosen after seeing method A is not one of the two methods; B3's data were computed after its recipe was written, but its recipe shape was borrowed from that variant; A's 36+ decimals rest on a ladder extended after its pre-registered stop (which gave 30).
- The criterion skeptic's first run failed clause (d) as undecidable from the package folder alone; on its one permitted re-run it judged (d) against the novelty skeptic's literature record and passed. The searches cover arXiv and OEIS, not Google Scholar or the general web.
- The reproduce skeptic confirmed open-strip widths 3 to 26 with its own code and reran the author's programs (strips to width 28, corner transfer matrix to chi = 48) with byte-identical output; width 29 was not rerun (memory).
