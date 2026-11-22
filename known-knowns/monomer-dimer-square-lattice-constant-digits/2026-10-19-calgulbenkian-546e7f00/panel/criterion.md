# Criterion report, md-digits-36 (second run)

This is a second run. What changed: the first run could not decide clause (d). The coordinator pointed me to the panel novelty report (panel/novelty.md), which I read as the panel literature record and used to rejudge clause (d) only. Clauses (a) to (c) are unchanged, and I found nothing in the novelty report that alters them.

context: Claude Code subagent, fresh context [Claude Sonnet 5.5]

Role: criterion. I read only the package. Network: two plain GETs (OEIS search for the digits 662798972833, HTTP 200, empty result, same body hash as the author's two empty searches; an arXiv API query returned HTTP 301 and, per the no-retry rule, is unresolved).

## Main criterion, clause by clause

Success: "a decimal value of h2 ... with at least 20 decimals". The value has 36 decimals: MET.

(a) "two independent methods agree on all claimed decimals": MET, with caveats.
- Method A (corner transfer matrix on the vertex model, 256-bit, chi up to 48) and method B3 (open-boundary strip eigenvalues for widths 3 to 29, one-step differences, Wynn epsilon) are different algorithms and code; no A number enters B3 (PREREG_B3.md, checked). The post-hoc periodic variant B2 is not used and its numbers do not enter.
- Agreement: E3(26), E3(27), E3(28), E3(29) against A at chi = 48 share 36, 40, 40, 43 decimals. The 36 claimed decimals agree in both.
- I recomputed B3 myself from the shipped open_strips values (mpmath, 100 digits, my own Wynn epsilon, the recipe of PREREG_B3.md): E3(23..29) agree with the shipped table (33, 35, 35, 36, 40, 40, 43 decimals shared with A) and E3(26..29) share 36 decimals. I did not rerun the strip eigenvalues or the CTM; the reproduce skeptic owns that.
- Weighing the post-hoc elements. The B3 recipe shape (differences plus Wynn on all widths) was borrowed from B2, which was designed after the author saw A's value and a diagnostic that used it. So B3 is blind in its data (open strips unseen) but not in its recipe, and a weak dependence of the recipe choice on A exists. It does not defeat (a): the recipe is a standard generic extrapolation with nothing tuned to A (no free parameter, no selection among columns), no A number enters, the open family is a different quantity from the periodic one, and the 43-decimal agreement with A at mmax = 29 and the self-agreement of B3 at 36 are not plausible by coincidence. It does lower B3's standing as a pre-registered blind method, and the folder discloses it.
- Shared elements: both rely on the same model definition and the checker's reading of it, tested against A028420 for n up to 6 (disclosed). I accept this as one model, two computations.

(b) "inside Kong's bracket and agrees with 0.662798972834 to 12 decimals up to final-digit rounding": MET. 0.6627989728337459... lies in [0.662798972831, 0.662798972845] and rounds at 12 decimals to 0.662798972834.

(c) "stable over at least three truncation increases": MET per method. A: pre-registered ladder rungs 16, 20, 24, 28 share 30 decimals; extended rungs 36, 40, 44, 48 share 43. B3: mmax 26 to 29 share 36. Four successive values each. Disclosed post-hoc point: A's ladder was extended after the pre-registered stop rule fired at chi = 28; under the pre-registered rule alone A supports 30 decimals, so the 36 depends on the extension. The extension only adds rungs with the same program and the same rule and is monotone (26, 30, 33, 37, 39, 41, 43), so it is not optional stopping toward a favourable value, but a strict reader gets 30 from A alone. The claim does state this. The 36 is also the minimum over A's count, B3's count and the A-versus-B3 agreement.

(d) "an arXiv/Google Scholar/OEIS search, re-run immediately before claiming, finds no published value with as many decimals": MET on the panel record, with one residual. Per the novelty report, run on 2026-10-19 after the claim was assembled: four arXiv API queries (all HTTP 200 over https), three OEIS queries (digit searches for 6627989728337 and 1940215351483 empty; no decimal-expansion entry for h2 or e^h2), Kong and Friedland-Peled primary text, TROPHY_CASE.md, known-knowns and a 473-PR snapshot. No published value longer than Kong's 12 printed decimals (11 claimed correct) was found; Friedland-Peled certify 8 (Kong reads 9), Butera-Federbush-Pernici about 9. My own OEIS search for 662798972833 was also empty. Residual: Google Scholar and a general web search were not run by anyone (the rules forbid a browser), so a longer unpublished or Scholar-only value is not excluded; the margin is 36 decimals against 12 and nothing indexed suggests a competitor, so I treat the clause as satisfied as far as it can be searched here. This clause is a literature judgement; the novelty skeptic's verdict agrees.

## Hidden quantifiers and stretched definitions
- The numerical value has no error bound; the digits are numerical agreement of two methods, not a proof.
- "36 decimals" is the minimum of three counts, with A's extension counted. Both methods in fact agree on 43 at their last truncation, so 36 is conservative on the A side but is exactly B3's own four-truncation count.
- B3 open-strip inputs are only converged to about 2e-45 in ln(lambda); the 43-decimal agreement at mmax 29 is nonetheless reproduced by my recomputation from those inputs.
- The direction "more digits" is satisfied relative to the quoted comparators.

## Verdict
Clauses (a), (b) and (c) are met numerically with the disclosed post-hoc elements (B3 recipe shape borrowed from B2; A's ladder extended past its stop rule, 30 decimals under the pre-registered rule) not defeating any of them. Clause (d) is met on the panel's search record, with Google Scholar unrun.

confirmed_scope: The numerical value h2 = 0.662798972833745915155196234397725566 (36 decimals, natural log per site) is reproduced from the shipped data and agrees numerically between the corner-transfer-matrix ladder (four rungs sharing 43 decimals, 30 under the pre-registered stop rule) and the open-strip Wynn extrapolation (four truncations sharing 36 decimals), with no error bound, and exceeds every published value found in arXiv and OEIS searches (Google Scholar not searched).
pass: true
