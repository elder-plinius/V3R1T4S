# MoleculeACE CHEMBL244 (FX): cliff-subset MSE 0.5502 vs the repo's own best baseline 0.6346

## What

**Status: PROMISING, not CONFIRMED** — see the disclosure at the end of this section and the
panel files in `panel/`. This package is submitted as a draft by the contributor's explicit
decision; the panel's NOVELTY skeptic did not pass it (2 of 3 skeptics passed).

On the official MoleculeACE CHEMBL244_Ki split (Polaris benchmark moleculeace-chembl244-ki, whose live API split[1] equals the 621 split=='test' rows of data/CHEMBL244_Ki.csv with targetCols ['y']), result/M1_predictions.json achieves sklearn mean_squared_error 0.5501943375378687 on the 296 test molecules with cliff_mol==1, strictly lower than the 0.634573831368627 of the repo-config SVM/ECFP baseline (result/B_predictions.json; C=10, epsilon=0.1, gamma=0.01, rbf, ECFP radius 2 / 1024 bits, retrained from the official train rows and matching the paper's corrected rmse 0.715156602 to ~1e-9), while also being lower on the 325 non-cliff test molecules (0.33343039149183445 vs 0.39931062625682384), with the real result beating all 400 label-shuffle null controls on overall test MSE.

That sentence is the panel CRITERION skeptic's confirmed_scope, quoted verbatim; it
satisfies the bank target's partial win p2: "A cliff-subset result: on one target, lower MSE
than a faithfully reproduced MoleculeACE paper baseline (the repo's own best descriptor+model
for that target, run by the attacker and reported with its code) restricted to the test
molecules with cliff_mol==1, with at least 40 such molecules, while not being worse on the
non-cliff subset."

**Honest disclosure (read before reviewing):** open PR #568 (2026-10-19, same bank target)
ships a 30-target CLSS sweep whose CHEMBL244 entry ALSO satisfies p2 and beats this package
on two of three metrics (see "Compared to" below); our cliff-subset value is lower than
theirs (0.550194 vs 0.554219) but our non-cliff (0.333430 vs 0.324309) and overall
(0.436751 vs 0.433896) are worse. The panel's NOVELTY skeptic therefore refused a
"strictly beats everything known" verdict; the run's honesty gate set status: PROMISING.
This submission is consequently NOT a claimed record for the cell — it is a genuine,
fully-verified p2 result (vs the repo's own baseline) and the lowest cliff-subset MSE we
found published for this cell, submitted for maintainer judgment with the prior art named.

## Check it yourself

One command from this folder (needs python with scikit-learn + rdkit; the MoleculeACE CSV is
fetched from its public source and pinned by sha256 — no dataset ships in this package):

```
sh verify-it-yourself/run_checks.sh
```

Expected last line: `VERIFY_P2: PASS` (rough time: ~1 minute on a laptop, plus one CSV fetch).
The verdict numbers it recomputes: `M1  cliff 0.550194 noncliff 0.333430` /
`B cliff 0.634574 noncliff 0.399311`, baseline recomputation from the definition (max diff
0.00e+00), and InChIKey train/test disjointness.

## Compared to

| what | value | source | fetched |
|---|---|---|---|
| reproduced comparison bar (criterion p2): repo-config SVM/ECFP cliff RMSE | 0.797 (paper) / 0.796601 (our faithful rerun, MSE 0.634574) | molML/MoleculeACE main, Data/results/MoleculeACE_results.csv row CHEMBL244_Ki/SVM/ECFP (corrected post-2023-erratum results) | 2026-11-18 |
| same row, overall RMSE | 0.715 (paper) / 0.715157 (our rerun) | same | 2026-11-18 |
| best published per-target on this split (GraphCliff, Nov 2025): overall RMSE 0.668 / cliff RMSE 0.752 (MSE 0.5655) | our M1: overall 0.6609 / cliff 0.7418 (MSE 0.5502) — better than both | arXiv 2511.03170v2, Table 5 (part 2/3), CHEMBL244 column | 2026-11-18 |
| Polaris leaderboard `moleculeace-chembl244-ki` (context only, not the p2 bar): sole listed entry autosota-moleculeace-chembl244-ki | MSE 0.4749981512616306 | https://polarishub.io/benchmarks/molecularml/moleculeace-chembl244-ki (HTTP 200, re-fetched 2026-11-18T03:41Z) | 2026-11-18 |
| **prior art, same cell (open PR #568, 2026-10-19, same bank target): CLSS sweep entry** | overall MSE 0.433896 / cliff 0.554219 / noncliff 0.324309 — our M1 is lower ONLY on cliff (0.550194); our noncliff 0.333430 and overall 0.436751 are worse | V3R1T4S open PR #568, object/moleculeace_30_sweep_manifest.json (CHEMBL244_Ki row), fetched 2026-11-18 | 2026-11-18 |

MAPCliff-WMGR (JCIM 2025-11-18, 10.1021/acs.jcim.5c01915) reports per-target MoleculeACE
results but its source data sits behind an ACS bot check (HTTP 403 on a single honest GET; not
retried per the project's table-access rules) — unverifiable here, recorded as pending a
human check.

## Not claimed

- **No CONFIRMED status.** The panel's NOVELTY skeptic refused this claim (open PR #568's CLSS
  entry beats our non-cliff and overall on this cell); the honesty gate set status: PROMISING.
  The kit's package checker therefore rejects this package on the status rule by design; it
  is submitted as a draft by the contributor's explicit decision, for maintainer review.
- No claim of a record for this cell (only the cliff-subset metric favors us vs PR #568).

- No claim against the Polaris leaderboard cell (that is partial win p1: beating every listed
  MSE with a 5% margin and a ≥95% bootstrap; NOT attempted here and NOT satisfied: our overall
  test MSE 0.436751 does beat the listed best 0.474998, but the p1 bootstrap/margin protocol
  was not preregistered for this target — the run's preregistered attack was p2 only).
- No claim on any other MoleculeACE target; no claim about the cliff-subset of any other
  split; no claim of state-of-the-art overall; one target, one partial win, nothing wider.
- The 2022 JAK1 (CHEMBL2835) p1 attempt in the same run FAILED (candidate test MSE 0.1728 vs
  listed best 0.16617) and is reported as a negative in how-we-built-it/HOW_WE_FOUND_IT.md.

## Credits

- Derek van Tilborg, Alisa Alenicheva, Francesca Grisoni — "Exposing the Limitations of
  Molecular Machine Learning with Activity Cliffs", JCIM 2022 62(23) 5938-5951,
  doi:10.1021/acs.jcim.2c01073 (data, baseline model and configs; 2023 correction
  doi:10.1021/acs.jcim.3c01576); the molML/MoleculeACE repository
  (github.com/molML/MoleculeACE) for the benchmark CSV, per-target configs and corrected
  results table.
- GraphCliff: "GraphCliff: Short-Long Range Gating for Subtle Differences but Critical
  Changes" (arXiv 2511.03170v2, Nov 2025) — per-target comparison values on the same split.
- MAPCliff-WMGR (J. Chem. Inf. Model. 2025, doi:10.1021/acs.jcim.5c01915) — compared where
  readable; per-target source data unreachable through the bot check.
- Polaris Hub (polarishub.io) — leaderboard records for moleculeace-chembl244-ki.
