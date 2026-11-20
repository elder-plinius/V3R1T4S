# NOVELTY panel verdict — indus-temporal-heldout-structure (object-type claim)

## 1. Status-source fetch (once, honest)
- URL: https://api.github.com/repos/joyboseroy/indus_decipher (GitHub metadata page for the target's
  status source https://github.com/joyboseroy/indus_decipher). One request, HTTP 200, no retries.
- Fetched: 2026-11-17T03:23:41Z. Saved to a scratch status-JSON (a relative temp copy of the status page), sha256
  80134dca083bb6cb01874969d9eaca39c3817ad527c2c330365a68346669b104 — byte-identical to the scout's
  2026-11-17 02:14:51Z record (README's data pins).
- Values: pushed_at 2026-09-07T22:24:48Z, open_issues_count 0, 0 stars/watchers, default_branch main,
  description "…falsification toolkit for the undeciphered Indus Valley script".
- Confirmed: Indus script still undeciphered. No decipherment claim anywhere in the repo page/metadata
  (pinned clone @ cd60034: "Active exploration, not a finished study"; "If you're looking for a
  decipherment claim, this isn't one"). The bank's 2026-10-03 status (Tamil Nadu prize unclaimed,
  2026 claims unaccepted) is unchanged; no movement since (pushed_at 2026-09-07 < 2026-10-03 < now).

## 2. Literature + code search (last 24 months; dates as fetched 2026-11-17)
- Zenodo 10.5281/zenodo.19103880 (Kriger & Hunt 2026-03-19): 179 MD unicorn seals; uniqueness 98.3%,
  positional-entropy profile, stroke numerals 15.4% penultimate, "structured registration codes".
  IN-SAMPLE, in-sample sub-corpus, no temporal split, no object-type prediction, no dual baseline.
- Zenodo 10.5281/zenodo.20040472 (Kriger 2026-05-05, "Credit Cards of the Bronze Age"): builds on
  19103880; interpretation paper (credit-instrument reading). Not a predictive structural result.
- arXiv 2608.02999 (Raghavendra, 2026-08-04, SIGIL non-specificity): the design rationale for
  baseline (ii). Confirms the standard statistics are non-specific; it does not itself predict
  object type across a time split. Design rationale, not competitor.
- arXiv 2604.17828 (2026-04-20, "Synthetic-Baseline Scorecard"): 1,916 dedup inscriptions,
  in-sample 4-metric scorecard vs two non-linguistic baseline families. Not a temporal held-out
  object-type prediction. Closest 2604 Indus paper; does not achieve the claimed object.
- arXiv 2605.12835 (PROMETHEUS) and 2604.23582 (Indus barter network): unrelated to the claim.
- paragorth/Indus- @ d62ec82 (pinned clone): PREREG_RESULTS.md + prereg/*.json (P1-P9, Q1-Q14,
  R1-R13, P4-credential, P5.x) all read directly. P4-credential predictions (frozen 2026-09-29)
  are the only held-out (post-1977) ones: P1 nesting ratio, P2 run-reuse, P3 uniqueness, P4
  foreign sealings — none is object-type prediction. Q13 is the closest temporal item (in-sample
  rate-stability bound; INDETERMINATE, n tiny). Q10 emblem linkage FALSIFIED on dedup corpus.
  papers/ (paper-A heterogeneity, paper-B slot-grammar) are in-sample / register-transfer, not
  temporal object-type. Nothing in the repo claims the object-type result.
- Pinned V3R1T4S repo (origin elder-plinius/V3R1T4S @ 25c9968): TROPHY_CASE.md has NO Indus row
  (six result families + cipher commitments, all non-Indus); known-knowns/ no Indus; bank target
  `indus-temporal-heldout-structure` is `kind: harvest`, status_checked 2026-10-03, open.
- Open/closed PRs on the pinned repo (full history, 824 PRs scanned, 2026-11-17 03:40Z): exactly one
  Indus claim, #570 "[claim] indus-temporal-heldout-structure … M77-CLSS" (created 2026-10-19,
  closed unmerged 2026-11-03). Property: masked-sign top-1 restoration (20.05%/22.67% vs KN3 14.71%,
  p=0.0001) + p3 ligature. CLOSED because it did not meet p3 (its "ligatures" were sign+bigram, not
  graphic ligatures). Different property (masked-sign, not object-type), not merged, no filed
  object-type result. PR #399 is a bank freshness sweep (no Indus result).
- No post-2026-10-03 publication found that already achieves a temporal M77->post-1977 object-type
  predictive result (arXiv Indus listing 15 entries, newest 2026-08-04; Zenodo Indus/Kriger sweeps
  2024-2026; GitHub Indus repos all 2026-10 or earlier and in-sample/decipherment benches).

## 3. Re-run novelty diff (from scratch, code/novelty_diff.py; compared to object/output_novelty_diff.json)
Re-run verdicts identical to stored (21/21 comparators, all NOT equivalent; only ts differs).
My independent judgment per comparator (hardest first):
- Q13 (stability over time, INDETERMINATE): in-sample |rate_early − rate_late| bound on jar-final/
  opener rates across dated periods of the 1977-era corpus. Different statistic (a bound, not
  accuracy), different direction (bound, not predict), different population (in-sample dated
  sub-corpora, n=9/17/34/267, not a 1,613-object held-out pool), no baselines, no object-type.
  NOT equivalent. Not trivially obtainable from Q13 by any small edit.
- P7 (positional entropy gap): in-sample edge-entropy statistic (the non-specific class per SIGIL).
  Claim's property is held-out object-type accuracy, not the entropy gap. NOT equivalent.
- K-H 2026 "registration code / document type": in-sample 179-seal sub-corpus; uniqueness/entropy/
  numeral-position in-sample statistics plus an interpretation. NOT a temporal predictive object-type
  accuracy beating a tuned KN3 + SIGIL control. NOT equivalent. The "document type" reading is
  interpretive, not the predictive object claimed.
- P1-P9, Q1-Q14 (minus Q13): all in-sample (re-derivation/falsifier/exploratory/transfer/equivalence)
  on ending-rate, terminal-class, jar, numeral, bigram, stroke-family, foreign-surprisal,
  emblem-JSD, twin-rate, dictionary-validator. None is a held-out, time-split, dual-baseline,
  multi-site, object-type accuracy. NOT equivalent.
- R1-R13: frozen new-data predictions (repetition, openers, marker exclusivity, voucher values).
  None is object-type prediction with a time split + dual baselines + site replication. NOT equivalent.
- Mahadevan 1977: descriptive 1977 concordance/tables (in-sample). NOT equivalent.
- Rao et al. 2009/2010, Yadav et al.: in-sample EBUDS corpus-level statistics (reciprocity,
  connectivity, beginner/ender asymmetry, non-randomness) — the class SIGIL shows is non-specific.
  NOT a temporal predictive object-type property. NOT equivalent.
- arXiv 2608.02999 (SIGIL): design rationale for baseline (ii); the control's model, not a temporal
  object-type prediction. NOT a competitor; it is the class the claim is designed to beat.
Verdict: the claimed property (temporal M77->post-1977 object-type predictability, dual-baseline,
multi-site, paired-bootstrap) is NOT equivalent to, and NOT trivially editable from, any P1-P9,
Q1-Q14, R1-R13, Mahadevan 1977, Rao/Yadav 2009-10, or Kriger-Hunt 2026 property.

## 4. Object vs published (cell + neighbours)
- Cell (temporal M77->post-1977 object-type, dual-baseline, multi-site, p<0.001): empty. No
  published or filed result occupies it. The only prior filed attempt (PR #570) is a different
  property (masked-sign top-1) and was closed unmerged.
- Neighbouring cells: in-sample positional/entropy (P7, K-H 2026), register-transfer (paper-A/B),
  in-sample scorecard (arXiv 2604.17828), in-sample rate-stability (Q13) — all distinct; none
  subsumes the temporal predictive object-type claim.
- Internal consistency: object/output_nulltest.json (pooled real 0.5846 vs best_control 0.3255,
  p=0.0; MD 0.7098 vs 0.3970, p=0.0; Harappa 0.4017 vs 0.3136, p=0.0) and object/output_sweep_main.json
  property_A_objecttype agree with claim_object.json; claim beats BOTH baselines on pooled, MD and
  Harappa separately (meets (d)). Margin is thinnest on Harappa (real − best_control = 0.0881) but
  still p=0.0 < 0.001.
- Pass criterion (structural, non-record): NOT equivalent/subsumed by any listed comparator AND no
  post-2026-10-03 publication already achieves the exact temporal object-type-predictive object.
  Both conditions hold.

## 5. Final judgment
The claimed property is a genuine, novel structural finding: the first temporal (M77->post-1977)
held-out, dual-baseline (tuned KN3 + SIGIL-style synthetic), multi-site object-type-predictive
result for the Indus script. It is not equivalent to any paragorth P1-P9/Q1-Q14/R1-R13 frozen
prediction or any published positional finding (Mahadevan 1977, Rao/Yadav 2009-10, Kriger & Hunt
2026), and no post-2026-10-03 publication already achieves it. The single closest filed prior work
(PR #570, masked-sign) is a different property and was closed. The Indus script remains undeciphered
(status unchanged). Pass on novelty.
Residual uncertainty: a future/post-2026-10-03 publication achieving the exact object would
supersede it, but none was found; the Harappa margin is the weakest of the three required sites.

context: subagent — fresh isolated OpenClaw subagent that saw only the claim folder + the pinned repo
pass: true
