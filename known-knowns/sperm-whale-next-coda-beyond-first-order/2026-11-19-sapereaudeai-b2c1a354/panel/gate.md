# Honesty gate - partial win p4 (written 2026-11-19T10:37:47Z by the run's main session)

status: CONFIRMED_PARTIAL
confirmed_scope: On the bank's five REC folds of sperm-whale-dialogues.csv (3,418 scored codas), the frozen logistic-regression model, trained on the training folds only and reading only earlier codas of the same REC stream, predicts whether each scored coda carries the same whale label as the previous coda with pooled held-out log-loss 0.7631 bits per coda, 0.0872 bits below a smoothed first-order same-or-switch chain fitted on the pooled training-fold streams (0.8503 bits; additive alpha chosen by inner CV from the R1 grid), with a 95% paired REC-group bootstrap interval of [0.065, 0.117] (10,000 resamples) excluding 0.

Panel files read in full by the main session: reproduce.md (pass: true; 16 checks PASS, own checker, fresh fetch with
matching sha256, frozen pipeline rerun twice byte-identical, own leakage test 0 of 3,418 changed), novelty.md (pass:
true), criterion.md (pass: true). Each was started as a fresh subagent that saw only claim/.

Downgrade checks: no reproduction mismatch; no hedged pass; the value is strictly better than the only public number
for this cell (see below); scope equals the CRITERION sentence; the null test (400 controls) is complete; the status
source was fetched by NOVELTY at 2026-11-19T10:16:39Z (under 6 h old).

Binding conditions from NOVELTY for any filing (the claim/ text the panel saw does not yet contain them):
- V3R1T4S draft PR #1175 by another contributor (created 2026-11-19T09:59:53Z, 4 min 42 s after this run's freeze)
  claims this same p4 cell at 0.780268 vs 0.850317 bits. It was the first public clearance of p4. This claim does not
  derive from it, and it strictly beats it: 0.7631118 vs 0.7802677 bits per coda on identical positions and an
  identical reference, better on every fold, paired REC bootstrap of the difference [0.0034, 0.0334].
- The filing must name #1175, say it cleared p4 first publicly, and say that maintainers may credit p4 only once.
- It must disclose that this claim's switch-pattern-only diagnostic (+0.0595) is below #1175's gain (+0.0700); the
  extra margin comes from the timing, overlap and speaker-share features.
- It must keep WhaleLM's qualitative "predictable turn-taking" credited as prior work.
