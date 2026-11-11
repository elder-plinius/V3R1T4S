# Honesty gate (kit/RUN.md step 7), run 2026-11-10-1136, claim: partial win p2

gate_written: Tue Nov 10 12:19:09 UTC 2026 (date -u)

status: CONFIRMED_PARTIAL
confirmed_scope: On the pinned 12,287-row CRyPTIC reuse table, for ethionamide (HIGH-quality R/S phenotypes) and one fixed genome-wide 10-nearest-neighbour model on the released CRyPTIC SNP distances, sensitivity at >= 95% specificity is 0.3496 on the frozen 12-SNP single-linkage cluster-aware split v2 versus 0.5135-0.6678 (mean 0.6003) on all 400 pre-registered random isolate-level splits of the same TEST size, a random-split inflation of 0.2507 on average (at least 0.1639), of which 0.15 to 0.21 remains in the panel's post hoc composition controls; this is shown for this distance-based model and this drug only.

Panel read by the run's main session:
- reproduce.md (round 2, fresh subagent, after the repair): pass: true. Rebuilt split v2 byte for byte, recomputed all
  401 ETH values with its own code (0 mismatches), peak 230.8 MB. Observation, not a mismatch: if only the negatives'
  scores were candidate thresholds, the split-v2 value would be 0.3459 and all 400 controls would still be above it.
- novelty.md (round 1, fresh subagent): pass: true. Status source re-fetched 11:56:58Z (HTTP 200, byte-identical).
  Closest prior: a public repository on the same table (one random vs one k-means cluster-disjoint split, ETH AUROC
  0.94 vs 0.91, figure only, no split files or null); precedents on other data: Hu et al. 2024, PLOS Biol 2025. The
  package names all three. This verdict was written for the pre-repair package; the repair changed one control value
  (seed 333) and no claim sentence, so it does not bear on novelty.
- criterion.md (round 2, fresh subagent, after the repair): pass: true; confirmed_scope above, quoted exactly.
- Round 1 (panel/round1/): reproduce.md pass: false (floating-point boundary in the <= 5% test, one control, seed 333);
  criterion.md pass: true. The repair (attempts/leakage-knn-repair/REPAIR.md) used the one repair round of a standard run.

Downgrade checks: no hedging verdict; no reproduction mismatch in round 2; no table value involved (methodology
partial win; status source unchanged, fetched under 6 hours ago); scope quoted from CRITERION and narrower than the
evidence (one model, one drug, composition caveat); no sample presented as complete (all 400 controls recomputed);
baseline record present and resolved (engine check 13/13). Main success criterion: not met, not claimed.
Nothing here is clinical advice.
