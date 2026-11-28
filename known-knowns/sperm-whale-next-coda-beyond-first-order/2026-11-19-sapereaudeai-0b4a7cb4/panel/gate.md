# Honesty gate - FULL success criterion (written 2026-11-19T12:29:14Z by the run's main session)

status: CONFIRMED_SOLUTION
confirmed_scope: On sperm-whale-dialogues.csv (sha256 1856c8bf...5da2), with the bank's REC streams, tokens, folds, training-fold bin edges and 3,418 scored codas, the frozen log-linear model `full` of code/seqlib.py, reading only earlier codas of the same REC stream, scores 2.1238 bits per coda pooled over the 5 held-out folds, which is 0.6563 bits below R1 (2.7802 under the claim's inner-CV convention, and at least 0.65 bits below R1 at every alpha of the grid) and 0.5311 bits below its pre-registered single-previous-coda twin with a 95% paired REC bootstrap interval (10,000 resamples) of [0.4571, 0.6325] (0.5226, [0.4463, 0.6273], against the post hoc literal truncated-input twin), so conditions (1) and (2) of the full success criterion are met.

The confirmed_scope above is the CRITERION panelist's sentence, verbatim.

## Panel files read in full by the main session

- **reproduce.md — pass: true.** Fetched the data itself (one request, HTTP 200, 500,380 bytes, matching sha256).
  Regenerated folds, scored set and bin edges from the definition with its own checker before reading author code:
  all equal. Independent reimplementation (own features, exact Newton optimizer) gives pooled twin 2.654906 vs the
  saved 2.654909 and pooled full 2.123844 vs 2.123847; it identified the cause (optimizer tolerance, the author's
  solution at most 7.4e-8 nats from the optimum, plus rounding of at most 2.2e-4 in four tail features) and
  reproduced the saved vectors from its own features times the author's theta to 3.8e-7. The frozen pipeline rerun
  exits 0 with the same sha256 on folds.csv, probs_R1/twin/full.csv and content_summary.json. Its own leakage test
  altered every field of the predicted coda in 4 patterns plus two stream cuts: 20,508 recomputed vectors each for
  R1, twin and full, none changed; two positive controls flagged at 3,418 of 3,418.
- **novelty.md — pass: true**, as a **record improvement, not first evidence**. See the binding conditions below.
- **criterion.md — pass: true**, conditional on three items, all now discharged (next section). It checked the
  criterion clause by clause, recomputed R1 under five conventions, tested the literal cut twin and the
  observed-vocabulary R1, and enumerated 13 stretched-definition or hidden-quantifier candidates, none of which
  changes the verdict.

Each panelist was a fresh subagent that saw only `claim/` and the bank entry.

## CRITERION's three conditions, and how each was discharged

- **(a) N2 null, 400 controls, real gain above every one.** DISCHARGED. 400 of 400 complete,
  no missing index, one duplicated index (2) whose two values agree to about 3e-12. Best control +0.010643
  against a real +0.531062, a 49.9x margin; zero controls at or above the real gain; mean +0.000402, sd 0.002584.
  Verified independently by this session as well as by `make_null_test.py` (claim/null/null_test.md,
  `real_beats_all_controls: yes`). Context, not a gate: under the same null the model's gain over R1 reaches at
  most +0.059, below condition (1)'s 0.10 threshold, so neither condition is clearable by the null process.
- **(b) The freeze preceded every held-out score.** DISCHARGED, with its limit stated: see panel/freeze_audit.md.
  The skeptic could not check this because the development outputs sit outside the claim package. This session
  read all six pre-freeze output files. None contains a score on an evaluation fold; the dev row counts match the
  dev folds exactly (p4 `dev scored 907` = folds 2+4 = 508+399; Dominica `dev scored 2895` of 8,501); and all
  seven comparable quantities are *worse* on the evaluation folds than on the dev folds, which is the signature of
  genuine held-out scoring. mtimes cannot prove nothing was deleted, and that limit is recorded in the audit.
- **(c) Package fixes before filing.** DONE. `null_test.md` now exists at claim/null/null_test.md with all 400
  controls (the provisional file is kept beside it); CLAIM.md's decomposition sentence is corrected (see below);
  both R1 conventions are now named in CLAIM.md.

## Downgrade checks (kit/RUN.md step 7), each considered

- **Hedging panelist:** no. REPRODUCE is unconditional. CRITERION's conditions are discharged above. NOVELTY's
  pass is unconditional on the value and explicit that the novelty is the improvement, not the effect.
- **Reproduction mismatch:** no. The independent reimplementation agrees to 3e-6 bits with the cause identified
  and bounded, and the frozen rerun is byte-identical by sha256.
- **Value not strictly better than the live table:** no. 2.1238 vs the only known in-cell value 2.564371
  (draft PR #1159), strictly better by 0.4406 bits. TROPHY_CASE.md does not cover this cell. Status source
  fetched 2026-11-19T10:16:39Z, 2.21 h old at this gate, so no refetch was required.
- **Stretched criterion or hidden quantifier:** no. 13 candidates enumerated by CRITERION; the claim uses the
  *strongest* (lowest) fair R1, and both conditions hold under every fair reading and both twin readings.
- **Scope wider than what was reproduced:** no. The scope sentence is CRITERION's, and REPRODUCE reproduced
  every number in it.
- **Sample presented as complete / capped search as exclusion / probable prime as proof / table value by evasion:**
  not applicable. Refused fetches were recorded and not retried or worked around.
- **Several objects bundled as one claim:** no. This gate covers one object (the model's per-position
  probabilities on the dialogues file). p4 and p3 are separate claims with their own gates.
- **Unresolved benchmark baseline (step 3c):** resolved. baseline/README.md was wrong on two points and has been
  corrected: a public in-cell value now exists (#1159), and WhaleLM does plot absolute perplexities under its own
  tokens. The bank entry repeats the WhaleLM misstatement; that goes upstream under "Needs you".

## Binding conditions for any filing (from NOVELTY; not yet in the claim/ text the panel saw, now added to CLAIM.md)

- Name **draft PR #1159** (another contributor, 2026-11-18) as the **first public clearance** of the full
  criterion for this cell: order-3 n-gram, 2.564371 bits, R1 2.794781, twin 2.850952. This claim's novelty is the
  strictly lower cross-entropy and the larger twin gain, not the existence of the effect.
- Explain the R1 difference (2.7802 here vs 2.794781 there) as an inner-CV convention difference: recutting the
  bin edges inside the inner CV, or scoring all transitions, gives 2.794781. Both are fair; this claim uses the
  harder one. CRITERION reproduced the other value exactly.
- Correct baseline/README.md (done) and report the bank's WhaleLM wording upstream.
- Credit whale-coda-dynamics (stream-level run-length and repertoire gains on overlapping DSWP recordings) and
  Bond 2026 (in-sample higher-order accuracy on this file) as neighbouring prior work.
- Record the two unread secondary sources (OpenReview PDF 403, phys.org 403).

## What this status does NOT say (carried into REPORT.md)

The bank's criterion, as worded, can be cleared by per-recording context alone, and #1159 showed that a plain
order-3 n-gram clears it. Of the 0.5311-bit twin gain, +0.0896 is run-length and repeat-rate features (which
depend on order), +0.2302 is an order-free bag of the stream's earlier codas, and +0.2112 is ordered and recency
structure beyond a stream-local reference. An earlier draft of CLAIM.md wrongly described 0.3198 bits as
order-free; corrected after CRITERION flagged it. "Dependence beyond the previous coda" is established; "syntax"
is not, and this gate makes no such claim.

Two package defects are disclosed rather than fixed, because the code is frozen and its sha256 list is
pre-registered, so editing it post-freeze would invalidate the freeze: the frozen code adds a
`code/../../evaluator/code` path that does not exist inside the package (no effect, but the package is not
self-contained), and REPRODUCE.md step 2 writes its rerun folder inside the claim folder.
