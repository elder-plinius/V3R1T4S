# Honesty gate (kings-hard-core-entropy-a247413-digits)

status: CONFIRMED_SOLUTION
confirmed_scope: The A247413 constant (Lambda = e^kappa, independent sets of the king graph) is 1.342643951124601297851730161875740 to 33 decimals, the digits agreeing between the site corner transfer matrix (36 decimals stable over chi = 70..100) and open-strip transfer matrices with Wynn extrapolation (33 decimals stable over mmax = 37..40), as numerical agreement and not a rigorous error bound, and subject to the novelty skeptic's verdict on clause (d).

## Gate notes
- Objects: 13 files under object/ (sha256 of each in the package folder's INDEX.csv and SHA256SUMS).
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the package folder; the computation was also done by a Claude Code subagent, so builder and skeptics are the same model family (Claude), which is disclosed here.
- The novelty skeptic passed clause (d): the best published value found is Kai Liang's 21-decimal bracket, OEIS A247413 has 18 terms, and no competing V3R1T4S pull request exists.
- The result is numerical: two independent methods agree on 33 decimals under the criterion's stability rule; there is no rigorous error bound.
- The reproduce skeptic checked open-strip widths 2 to 26 with its own code and confirmed widths 39 and 40 and the corner transfer matrix ladder to chi = 100 by rerunning the author's programs; method C (supporting only) was not rerun.
- The Wynn recipe's start width was chosen after open-strip widths up to 28 had been seen (disclosed in PREREG_B.md); widths 29 to 40 were computed after the recipe was written down.
