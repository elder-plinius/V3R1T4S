# Research charter v1 (2026-10-27)

## Thesis
This person reads option prices as costs, not stories: fluent in pricing, quotes and the tape, and used to paying spread and slippage. Their edge is turning a widely repeated claim about same-day-expiry (0DTE) index options into one frozen statistic, then confirming or refuting it on free public data with frictions included. The charter hunts published 0DTE and option-return claims that can be reproduced or broken by a script a stranger can rerun.

## Quarries
- **Q1 put-premium-replication** — Does the negative average return of short-dated index puts reported by Coval & Shumway, "Expected Option Returns" (J. Finance, 2001) and Bondarenko, "Why Are Put Options So Expensive?" (Q. J. Finance, 2014) still hold out-of-sample on free public data, net of a stated half-spread? Shape: counterexample/replication with certified statistic. Defined: those two papers. Status first: exact sample, return definition and whether free daily SPX/SPY option closes exist for a later window. Why us: cost-aware replication. Weight 4. Wild: no.
- **Q2 0dte-volatility-claim** — Do published studies claiming 0DTE trading does (or does not) raise intraday S&P 500 volatility survive re-estimation on free data? Shape: counterexample to a stated finding. Defined: to be located during scouting (a peer-reviewed or SSRN paper on 0DTE and underlying volatility, named exactly before any work). Status first: which paper, its exact test and sample. Why us: knows the tape-level mechanism the claim rests on. Weight 4. Wild: no.
- **Q3 vix1d-definition-check** — Does Cboe's published VIX1D methodology, applied to free public data, reproduce the published index values, and where does it break (quiet days, event days)? Shape: counterexample to a published formula's stated behaviour. Defined: Cboe VIX1D white paper / methodology document (to be located and opened). Status first: whether free historical VIX1D values and enough free option quotes exist. Why us: pricing fluency. Weight 3. Wild: no.
- **Q4 variance-ratio-intraday** — Does the Lo & MacKinlay variance-ratio test (Rev. Financial Studies, 1988) reject the random walk for SPX/SPY returns on 0DTE-era data versus the pre-0DTE era, with a frozen sample split? Shape: bound/statistic with null controls. Defined: Lo & MacKinlay 1988. Status first: free intraday or daily data source and existing replications. Why us: tests a folklore claim ("0DTE made markets mean-revert"). Weight 3. Wild: no.
- **Q5 static-arbitrage-in-free-quotes** — In free public end-of-day option chains, are there quotes that violate the no-arbitrage conditions of Breeden & Litzenberger (J. Business, 1978) (convex call prices) after crossing the spread? Shape: existence of explicit violating quotes, or a certified "none at cost". Defined: Breeden & Litzenberger 1978 plus Merton (1973) price bounds. Status first: a free, legally usable chain source without login. Why us: knows quote-vs-trade frictions. Weight 2. Wild: no.
- **Q6 minlplib-finance-open-instances** (bank id) — Beat saa_2 or close pricing050 with a certificate. Shape: record/bound. Defined: bank/targets.json entry. Status first: MINLPLib current best points. Why us: portfolio intuition carried into a solver problem. Weight 2. Wild: yes.

## Lenses
- **cost-first** (skeptic no): You price every claimed edge at the quoted spread before computing anything else. First moves: fix fill rule (mid, bid/ask) in PREREG. Dead sign: result flips sign between mid and touch.
- **replicate-exactly** (skeptic no): You rebuild the paper's sample and statistic to the digit before extending it. First: match one published table cell. Dead sign: cannot match within stated tolerance after two attempts.
- **regime-split** (skeptic no, method card: drop-assumption): You drop the assumption that the market is stationary across the 0DTE introduction; pre-register the split date. Dead sign: effect equal in both halves.
- **tape-reader** (skeptic no, most distant fluency: order book reading): You ask what a quote or print must have looked like for the claim to hold and test that observable directly. Dead sign: needed observable is only in paid data.
- **already-settled** (skeptic yes): You try to show the quarry is already answered, trivial or ill-posed—search for later replications, errata, comments. Dead sign for the quarry: a published replication covers it.
- **counterexample-shape** (skeptic no, method card): You ask what a single day or quote breaking the claim would look like, and hunt there. Dead sign: no candidate days in 400 controls differ from shuffled.

## Scout voice
Read like a trader checking a pitch: what exactly is measured, over which dates, at what price, after what costs. Note every claim that is folklore without a source. Mark unverified facts pending.

## Attacker voice
Blunt and economical. Assume the edge is a cost illusion until the numbers say otherwise; enjoy a clean refutation as much as a confirmation.

## Heuristics
1. Mid-price results are hypotheses; touch-price results are evidence.
2. Freeze the date range before looking at the chart.
3. A claim with no published definition is not a quarry.
4. Free data only; if the test needs paid tape, stop and record it.
5. Prefer one sharp statistic over many plots.
6. Compare against at least 400 shuffled or random-date controls.
7. Report the null as loudly as the hit.

## Kill criteria
1. Needed data is paid, login-only, or terms forbid the use.
2. The source paper cannot be named and opened.
3. Result depends on fill assumption alone.
4. A published replication already settles the exact question.
5. Effect does not beat every null control.
6. More than a week of nights of compute.

## Self-critique
Free public 0DTE data is thin; most quarries may die on data access. Q2 and Q3 depend on sources still to be located. The person's pull toward market claims risks drifting into prediction; the frozen-statistic rule is the guard. Replications may be "not novel" to a NOVELTY skeptic.

## Method cards used
drop-assumption, counterexample-shape, evaluator-first
