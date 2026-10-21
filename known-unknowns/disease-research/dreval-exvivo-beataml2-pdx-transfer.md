# DrEval ex vivo transfer: beat the naive baseline when a cell-line drug-response model meets AML patient samples and breast-cancer PDX

🧬 **Disease research** · moonshot (famous, long odds) · tractability ★★☆☆☆ · compute: laptop-days · open as of 2026-10-20

## The problem

Every cancer drug-response model is trained on immortalised cell lines and justified by an implicit promise about patient material. DrEval (Judith Bernett, Pascal Iversen, Mario Picciani, Mathias Wilhelm, Katharina Baum and Markus List; Nature Communications 2026, article 4238; package drevalpy v1.6.0) is the first benchmark to test that promise mechanically: models trained on CTRPv2 cell lines are applied, through the package's own cross-study machinery, to two ex vivo screens - BeatAML2 (about 22,500 drug-sample responses from acute myeloid leukaemia patient samples with RNA-seq) and PDX_Bruna (about 1,500 responses from breast-cancer patient-derived xenografts with microarray profiles). The paper's finding, re-read on 2026-10-15 from the open-access full text, is blunt: performance declines even more substantially on these clinically realistic datasets than in cell-line-to-cell-line transfer, where no model already beats the NaiveMeanEffectsPredictor in squared error. So the open question has a crisp public form - can any model, trained only on cell lines, achieve a positive normalized R-squared (that is, beat the naive mean-effects predictor) on patient-derived material? Everything needed is ungated: the processed response and omics data on Zenodo (record 23159774, 2026-10-05: BeatAML2.zip 162 MB, PDX_Bruna.zip 50 MB, CTRPv2.zip 519 MB, splits.zip 41 MB), the package, the baselines and the metric code. This is the most clinically meaningful cell in the whole drug-response family. Note: the paper's results text says 'some models are able to exceed the Naive Mean Effects Predictor on the PDX_Bruna dataset' (metric not named in the main text; see Supplementary Tables 5-6), and reports no such result for BeatAML2, so BeatAML2 is the cell that is clearly open.

## What counts as a win

Success means a drevalpy model class, trained ONLY on CTRPv2 under the package's documented protocol with the package-generated or Zenodo-provided splits (lnIC50, the same number of cross-validation splits as the public report), evaluated by drevalpy's own cross-study machinery on BeatAML2 (or PDX_Bruna), whose mean normalized R-squared across splits - computed by drevalpy's own evaluation code against the NaiveMeanEffectsPredictor - is STRICTLY GREATER THAN ZERO (direction: max) by at least 0.02 absolute and at least 2x the across-split standard deviation, while its normalized Pearson is not lower than the attacker's same-environment re-runs of RandomForest, GradientBoosting and DIPK. The ex vivo dataset must be used for evaluation only: no response value, response statistic, calibration factor or preprocessing parameter may be derived from it, and the attacker's model and hyperparameters must be fixed on CTRPv2 inner validation and pre-registered in a sha256-stamped file written before any ex vivo scoring. Deliverables: pinned drevalpy version and commit, data sha256s, the pre-registration file with its timestamp, the model source and exact invocation, per-split prediction and ground-truth CSVs, and the same-environment baseline re-runs.

## Partial wins

- **p1:** Strictly positive normalized Pearson and Spearman on BeatAML2 that exceed the attacker's re-run baselines (RandomForest, GradientBoosting, DIPK, NaiveMeanEffectsPredictor) by >= 0.03 each, even if normalized R-squared stays negative. Rank transfer to patient samples is a distinct and useful result.
- **p2:** The same criterion on PDX_Bruna, which is smaller (about 1,500 responses) and profiled on microarrays rather than RNA-seq, so a win there additionally demonstrates robustness to platform change.
- **p3:** A measured decomposition of the ex vivo gap: with the same predictions, quantify how much of the error is attributable to (i) assay and readout differences, (ii) expression-platform shift, (iii) the drug overlap between CTRPv2 and the ex vivo screen, by re-scoring after each correction estimated from unlabelled ex vivo features only, and report which single factor dominates. Checkable from saved prediction files; a diagnostic result, not a record.

## How a win is checked

Skeptic installs pinned drevalpy in a clean virtual environment, downloads CTRPv2, BeatAML2 (or PDX_Bruna), meta and splits from the Zenodo record without registration and compares sha256s with the attacker's manifest, re-runs the attacker's exact invocation including the cross-study evaluation (laptop-hours to a few days on a multi-core laptop), then recomputes normalized R-squared, Pearson and Spearman directly from the written per-split prediction and ground-truth CSVs with their own script, normalising against the NaiveMeanEffectsPredictor predictions that the pipeline always produces. The paper's claim that performance collapses on ex vivo data is re-read live from the Europe PMC full text. Leakage audit: verify the pre-registration file predates the ex vivo logs, grep for any read of ex vivo responses during training or model selection, and confirm no scaler, quantile map or calibration was fitted on ex vivo labels.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13168506/fullTextXML>

## Sources

- <https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13168506/fullTextXML>
- <https://zenodo.org/records/23159774>
- <https://github.com/daisybio/drevalpy>
- <https://drevalpy.readthedocs.io/en/latest/>
- <https://doi.org/10.1038/s41467-026-72903-w>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Conventional: predict ranks or per-drug standardised responses rather than absolute lnIC50, so the model never has to transport a scale across assay platforms, and map back using training-study statistics only.
- Conventional: restrict to mechanistically transferable features - pathway activities, target-gene expression, known AML dependencies - instead of generic landmark genes, and let the model fall back to the mean-effects prediction where the applicability domain is violated.
- Cross-domain import (signal processing / blind equalisation): treat the ex vivo screen as the same signal through a different measurement channel and estimate the channel from UNLABELLED ex vivo features only (quantile matching on the omics, not on responses), which is legitimate transduction rather than fitting on the test labels.
- Cross-domain import (domain adaptation geometry / kernel mean matching): reweight CTRPv2 cell lines by an importance ratio estimated from the leading eigen-directions of the omics covariance to resemble the patient samples, which is the principled form of 'train on the cell lines that look like AML blasts'.
- Cross-domain import (clinical epidemiology / transportability): borrow the formal transportability framework used to carry trial effects to new populations, which tells you in advance which effects are identifiable under a stated covariate shift and which are not - a published negative identifiability result would itself be informative here.
- Cross-domain import (ecology / community similarity): compare the drug-response profile of a patient sample with training cell lines as community-composition profiles and transfer only ordinal structure, which survives effort and platform differences better than absolute values.
- Honest ceiling estimation: estimate the replicate-level noise floor of BeatAML2 responses and report how much of the remaining gap is in principle reachable, which is valuable whether or not the bar is cleared.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Any use of ex vivo responses - for calibration, checkpoint choice, feature scaling or 'validation' - turns this into a fitted-on-test number. The sha256-stamped pre-registration and the leakage grep are the only defences, and the skeptic must check timestamps rather than trust a claim of blindness.
- Drug and sample overlap: drugs shared between CTRPv2 and BeatAML2 are not independent test points in the usual sense, and silently dropping or keeping them changes the number. The overlap handling must match the package's convention and be stated.
- Readout mismatch: BeatAML2 and PDX_Bruna use different viability assays, concentration ranges and curve-fitting conventions from CTRPv2, so raw squared-error comparisons across studies are meaningless; report both raw and per-drug-standardised metrics.
- Normalized versus unnormalized metric confusion: a raw Pearson can look impressive while the normalized metric - the only one that measures differential sensitivity beyond mean drug and sample effects - is negative. Only the normalized metric counts here.
- Subsetting: evaluating on a favourable subset of drugs, samples or splits while comparing against whole-dataset numbers, or quietly discarding samples with extreme responses.
- Over-claiming is especially dangerous on this target: a positive normalized R-squared on ex vivo AML samples would be a genuine first, but it is still a retrospective laboratory measurement, not evidence that any patient should receive any drug.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/disease-research/dreval-exvivo-beataml2-pdx-transfer.md
```

Already set up? Say `run V3R1T4S on dreval-exvivo-beataml2-pdx-transfer`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `dreval-exvivo-beataml2-pdx-transfer`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
