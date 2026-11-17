# Honesty gate (run 2026-11-13-0523), written 2026-11-13T05:51:39Z

status: CONFIRMED_PARTIAL
confirmed_scope: code/p3_recompute.py deterministically and byte-reproducibly (object/p3_table.csv sha256 e01db6ee9d55baf24c06fa801c2fdfee27d9c1f70d1d513b9e98b75bd6d2f804) recomputes, from the 247 in-season model-output files of github.com/CDCgov/rsv-forecast-hub at commit e947ca8fe8d50a581a181e6aefacfe922ba95af5 (reference dates 2025-09-20..2026-05-30, all unchanged at head 1985aee45bca6b655e22b8bc2096b515bd6327f2) and that commit's target-data/oracle-output.parquet, the per-model mean 23-level quantile WIS, MAE, 50%/95% coverage, shared-task comparisons with RSVHub-ensemble and pairwise relative WIS scaled to RSVHub-baseline of every model directory with 2025-26 quantile forecasts (8 for wk inc rsv hosp, 5 for wk inc rsv prop ed visits), with its data rules in object/p3_exclusions.txt and no hub score file to compare against, while the separate scripts code/p3_reconcile_k2.py and code_reconcile/ reproduce the named arXiv 2605.16238 v2 repository, EpiBenchmark and tapestry score sets to within 2e-12 absolute under the truth vintages and task rules the claim states, for the pinned oracle only and with p3's "released" clause met only once this package is published.

confirmed_scope note: copied exactly from the final CRITERION skeptic's file (panel/criterion.md).

Claim gated: bank partial win p3 for CDCgov/rsv-forecast-hub 2025-26 (independent per-model season-WIS recomputation).
Object: object/p3_table.csv, sha256 e01db6ee9d55baf24c06fa801c2fdfee27d9c1f70d1d513b9e98b75bd6d2f804, unchanged since
run 2026-11-13-0233 round 2. This run changed the claim text (no completeness or exclusivity statements; the Puerto
Rico rule and 5,936/5,824 counts; the tapestry google-comparison folder described and reconciled; plots listed) and
the line endings of the text outputs (CRLF -> LF; content identical; p3_table.csv byte-identical).

Panel (three fresh contexts, Agent tool, subagent types reproduce / novelty / criterion; none saw earlier panels):
- REPRODUCE pass: true. Own scorer reproduces all 13 x 16 cells; REPRODUCE.md run literally gives every stated sha256
  and DONE; all third-party reconciliations reproduce with its own code. Notes: "within 1e-12" is ambiguous between
  absolute and relative (1.82e-12 absolute, 2e-16 relative, on one per-location sum); python -I writes __pycache__.
- NOVELTY pass: true. Status source fetched 2026-11-13T05:34:35Z (HTTP 200, head 1985aee, no score file); object new
  for its cell; prior-art statements accurate in substance; one non-material mislabel (#295 is a pull request).
  Residual risk named: the CDC RSV page returned HTTP 403 (not read, not retried).
- CRITERION pass: true, with required text corrections R1 (within 2e-12 absolute, not 1e-12), R2 (disclosure 3 bounds
  0.1009 and 0.0463, not 0.1008 and 0.046), R3 (the reconciliations and the hub-tree check are this work's, not
  code/p3_recompute.py's), and the condition that "released" is met only when this package is published. Its
  confirmed_scope already carries R1 and R3.

Gate checks: no hedging verdict (all three write pass: true; CRITERION's conditions are text corrections applied in the
package's DISCLOSURES.md item 10 and README, and the NOVELTY #295 label is fixed there too); no reproduction mismatch;
p3 has no table value to beat (the hub publishes no score file; the bank's p3 asks for the recomputation); no stretched
criterion (CRITERION read each clause literally; "released" stays pending, as stated); scope no wider than reproduced
(the confirmed_scope sentence names the pinned oracle and the conditions); no sample presented as complete; no evasion
in any fetch (the 403 was not retried); one object (one table). Status-source fetch by the panel is 0.3 h old.

Decision: status CONFIRMED_PARTIAL (bank partial win p3), subject to check_run. Package in outbox/ (name ends
-e01db6ee). Not submitted: a draft PR needs the human's explicit "yes".
