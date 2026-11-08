# Research charter v1 (2026-10-30)

## Thesis
Pursue useful small results, surprising discoveries, and progress on old questions across biology and medicine, space and Earth, engineering, and ciphers. The organizing idea is to test explanations against independent evidence and reuse constraint-based methods across fields. No specialist background is assumed; records are secondary to clear, reproducible understanding.

## Quarries

### pycox-metabric-gbsg-breast-cancer-survival
- Question: How stable are survival-model comparisons across data splits, and can calibration improve without losing discrimination?
- Shape: reproducibility / prediction
- Where defined: bank entry `pycox-metabric-gbsg-breast-cancer-survival` in `bank/targets.json`; primary source: https://www.jmlr.org/papers/volume20/18-424/18-424.pdf
- Status to confirm first: current primary-source status, subsequent literature, and whether the proposed result already exists. Bank status is provisional.
- Why this direction: Start with the enumerated variance study; a reproducible negative result is useful.
- Weight: 5
- Wild: no

### massbalancemachine-norway-test-glaciers-rmse
- Question: Can a simple model predict unseen glaciers well, or independently reproduce the published scores?
- Shape: prediction / reproduction
- Where defined: bank entry `massbalancemachine-norway-test-glaciers-rmse` in `bank/targets.json`; primary source: https://tc.copernicus.org/articles/19/5801/2025/
- Status to confirm first: current primary-source status, subsequent literature, and whether the proposed result already exists. Bank status is provisional.
- Why this direction: Prefer the small-model and independent-reproduction partial wins.
- Weight: 5
- Wild: no

### iea37-cs1-circular-wind-farm-layout
- Question: Do published wind-farm layouts satisfy their constraints and reproduce their claimed energy output?
- Shape: reproduction / explicit construction
- Where defined: bank entry `iea37-cs1-circular-wind-farm-layout` in `bank/targets.json`; primary source: https://github.com/byuflowlab/iea37-wflo-casestudies
- Status to confirm first: current primary-source status, subsequent literature, and whether the proposed result already exists. Bank status is provisional.
- Why this direction: Start with the independent wake-model evaluator and feasibility report, rather than record hunting.
- Weight: 4
- Wild: no

### catwise-cold-brown-dwarf-candidate-uncatalogued
- Question: Can a bounded archival search identify an overlooked moving cold-object candidate?
- Shape: discovery candidate
- Where defined: bank entry `catwise-cold-brown-dwarf-candidate-uncatalogued` in `bank/targets.json`; primary source: https://irsa.ipac.caltech.edu/TAP/sync?QUERY=SELECT+TOP+1+source_name,ra,dec,pmra,pmdec,w1mpro,w2mpro+FROM+catwise_2020&FORMAT=csv
- Status to confirm first: current primary-source status, subsequent literature, and whether the proposed result already exists. Bank status is provisional.
- Why this direction: Search one manageable region and retain candidates only when independent observations agree.
- Weight: 3
- Wild: no

### cryptocellar-truppenschluessel-1941
- Question: Can constraint-based search explain one remaining historical hand-cipher message?
- Shape: decipherment
- Where defined: bank entry `cryptocellar-truppenschluessel-1941` in `bank/targets.json`; primary source: https://www.cryptocellar.org/bgac/1941-msg-list.html
- Status to confirm first: current primary-source status, subsequent literature, and whether the proposed result already exists. Bank status is provisional.
- Why this direction: Prefer a narrow reproducible key search over subjective readings.
- Weight: 3
- Wild: no

### eterna100-v2-vienna2-algorithmic-solve
- Question: Can counterexample-guided constraint solving design an RNA sequence by excluding rival folds?
- Shape: explicit construction / certificate
- Where defined: bank entry `eterna100-v2-vienna2-algorithmic-solve` in `bank/targets.json`; primary source: https://github.com/eternagame/eterna100-benchmarking
- Status to confirm first: current primary-source status, subsequent literature, and whether the proposed result already exists. Bank status is provisional.
- Why this direction: Transfer engineering-style constraint repair into RNA inverse folding; stop if setup or search exceeds local resources.
- Weight: 2
- Wild: yes

## Lenses
- **Reproduce before extending** (skeptic: yes): Reconstruct the definition and evaluator; attempt to falsify the starting claim. Stop a comparison if its inputs or baseline cannot be matched.
- **Smallest useful experiment** (skeptic: no): Start with a bounded case and a simple baseline. Stop scaling when the measured resource cost no longer fits a short session.
- **Constraints across fields** (skeptic: no): Borrow constraint propagation from cipher search and engineering design for RNA or layout problems. First encode a tiny exact case; abandon the transfer if it loses the defining physics or energy model. This is an experimental cross-field lens, not an assumed personal expertise.
- **Independent observations** (skeptic: no): Prefer repeated measurements and independent catalogs over a single anomalous score. Kill candidates explained by blending, leakage, or known objects.
- **Simple explanations first** (skeptic: no): Compare a low-parameter mechanism with a flexible predictor using an untouched evaluation set. Kill added complexity when it cannot beat the simpler explanation reproducibly.

## Scout voice
Be curious, concrete, and skeptical. Explain why a question matters without inflating its scope. Prefer accessible data and a test that can make progress in a short session.

## Attacker voice
Work patiently on a precise question. Treat an informative failure or reproduced result as useful work; do not chase a ranking at the expense of understanding. Resume meaningful partial progress across manually initiated sessions.

## Heuristics
- Start with one target and the smallest decisive experiment.
- Favor calibration, reproducibility, and explanatory simplicity.
- Use independent data to challenge an attractive explanation.
- Separate an observed candidate from an established discovery.
- Keep an unchanged evaluation set throughout a comparison.
- A method transferred between fields must preserve the original definition.
- A useful replication is not automatically a novel result.

## Kill criteria
- Required data or terms are unavailable.
- The claimed open question is already settled.
- Measured memory or runtime exceeds the local budget without a smaller valid experiment.
- A baseline cannot be reproduced well enough to support the comparison.
- An apparent gain depends on leakage or an altered metric.
- A candidate fails independent confirmation.

## Self-critique
Breadth can fragment effort, and one-hour sessions may mostly establish baselines. The bank often rewards records even when the motivating question is practical. Replications and uncertainty studies may be useful without being novel or satisfying a bank win. Cross-field methods are hypotheses, not evidence of a personal advantage. Astronomy candidates and computational biomedical findings require careful limits on interpretation.

## Method cards used
smaller-first; evaluator-first; solver; far-import; counterexample-shape; same-object
