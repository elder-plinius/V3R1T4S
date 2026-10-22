# Honesty gate (constant-weight-codes)

status: CONFIRMED_PARTIAL
confirmed_scope: The exact rational Delsarte dual certificate in object/cert_A29_6_14.json proves A(29,6,14) <= 322266, which is strictly below the table-implied upper bound 328162 (margin 5896; the live cell prints no upper bound) as of the Andw.html page with sha256 15b15c8d...3349 fetched 2026-10-18; it is an upper-bound certificate only (enumerated partial win p2 under the PR #350 table-implied reading) and says nothing about any lower bound or code.

## Gate notes
- Object: object/cert_A29_6_14.json, sha256 476121c35ae7940812cb385b77eb7deb27e15263db71db60d36927cc0d10e18f.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the package folder; the object's builder (Gemini, Argon) is a different model family from every skeptic.
- Partial win p2 only: an exact rational Delsarte LP dual certificate (pure Delsarte, no table inputs) proving an upper bound; no code and no lower bound is claimed. One cell per claim.
- The live cell prints no upper bound (the page: "For n > 28 unmarked upper bounds are from the Johnson bound"). The bar used is the table-implied bound (printed bounds, merged V3R1T4S bounds and both Johnson rules applied recursively), per the maintainer ruling on pull request #350; novelty and criterion each recomputed it independently and the claim is strictly below it.
- Reproduce: own exact Fraction checker (Eberlein eigenvalues, orthogonality self-test, dual feasibility at every Johnson distance, floor of the objective), plus an exact simplex showing the certificate objective is the LP optimum.
- The certificate JSON carries the author's own bookkeeping fields (for example table_upper_bound, table_cell_as_printed); they are not part of the claim and some are stale; the README uses the panel's values.
- No downgrade triggers found.
