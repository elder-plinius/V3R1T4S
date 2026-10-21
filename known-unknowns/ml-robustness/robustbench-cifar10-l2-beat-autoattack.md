# RobustBench CIFAR-10 L2 (eps 0.5): lower a listed model's robust accuracy below the leaderboard value with a stronger L2 attack

🛡️ **ML robustness** · standard · tractability ★★☆☆☆ · compute: laptop-hours · open as of 2026-10-20

## The problem

The RobustBench CIFAR-10 L2 eps=0.5 leaderboard (model_info/cifar10/L2, 21 JSON files as of 2026-10-09; the website table is JS-rendered, the GitHub JSONs are the primary machine-readable record) lists 20 robust open-weight models plus the undefended 'Standard' baseline, each evaluated with standard AutoAttack (L2 APGD-CE, APGD-T, FAB-T, Square). Only ONE entry carries an 'external' (adaptive-attack) value, Amini2024MeanSparse_S-WRN-70-16 (autoattack_acc 87.28, external 84.33); for the other 19 robust models the single-seed AutoAttack number is the best known. The last commit touching the L2 model_info files is dated 2024-12-20 ('add model info, RodriguezMunoz2024Characterizing models'; GitHub history checked 2026-10-20). The L2 threat model has had far less adaptive-attack scrutiny than Linf: A3 and MALT are Linf-only; the strongest recent published L2 effort, Adversarial Frontiers (arXiv:2607.19855, Jul 2026, minimum-norm ensembles incl. FMN/ALMA/DDN-style solvers/APGDmin) matched but did NOT lower AutoAttack's value on the L2-trained CIFAR-10 models it tested (Augustin, Engstrom, Rade, Sehwag) on 1000-sample subsets, while it did lower AA on Linf-trained models evaluated under L2. Beating the table on a genuinely L2-trained model on the full 10,000-image test set is therefore open and non-trivial. CPU-realistic entries: Rade2021Helper_R18_ddpm (76.15), Rebuffi2021Fixing_R18_cutmix_ddpm (75.86), Sehwag2021Proxy_R18 (74.41), Rice2020Overfitting PreActRN18 (67.68), Ding2020MMA WRN-28-4 (66.09); WRN-28-10 / WRN-34-10 entries overnight. (Numbers quoted are the 2026-10-09 snapshot; the live JSON is authoritative.)

## What counts as a win

Success means a saved float32 tensor x_adv of shape 10000x3x32x32 of adversarial inputs for the FULL standard CIFAR-10 test set (torchvision test split, ToTensor only, pixel range [0,1], no normalisation outside the model) against ONE model loaded unmodified via robustbench.utils.load_model(model_name, dataset='cifar10', threat_model='L2') in eval mode, such that (a) for every image the single float64 L2 norm of the flattened 3072-dim perturbation satisfies ||x_adv - x||_2 <= 0.5 + 1e-6 and 0 <= x_adv <= 1; (b) the robust accuracy recomputed by the skeptic's OWN forward pass (fraction of the 10,000 images whose clean prediction is correct AND whose adversarial argmax is still correct; ties count as not fooled) is STRICTLY LOWER (direction: min) than the model's best-known value min(autoattack_acc, external) in https://raw.githubusercontent.com/RobustBench/robustbench/master/model_info/cifar10/L2/<Model>.json, re-fetched live immediately before claiming, by at least 20 images (0.20 percentage points; AutoAttack's own single-seed variance is of order 0.1 points and a multi-seed union of standard AutoAttack alone can shave ~10 images, so 10 images is noise); and (c) the value is also strictly lower (by >= 20 images) than any FULL-test-set robust accuracy already published for the same model under L2 eps=0.5 in arXiv papers of the last 24 months found by the NOVELTY skeptic (minimum-norm / FMN / ALMA / DDN / APGDmin evaluations included). Values published on subsets (e.g. the 1000-sample numbers in arXiv:2607.19855 Table 6) are not full-test-set values and do not replace the table, but the author must cite them. Only models present in the live model_info/cifar10/L2 directory count; the undefended 'Standard' entry (0.00) is excluded.

## Partial wins

- **p1:** The same full-test-set result (strictly lower by >= 20 images than live min(autoattack_acc, external), under the L2-norm, range, shape and dtype checks) for a model whose live L2 model_info JSON has NO 'external' value AND for which the NOVELTY skeptic finds no published full-test-set L2 eps=0.5 robust accuracy below the autoattack_acc; i.e. clause (c) is vacuous for that model. Must be re-fetched live. 'Standard' excluded.
- **p2:** For a model whose live L2 model_info JSON carries an 'external' value (today only Amini2024MeanSparse_S-WRN-70-16), a full-test-set robust accuracy strictly lower by >= 20 images than BOTH the live autoattack_acc and the live 'external' value (re-fetched), under the same checks.
- **p3:** A reproducible per-image attack-strength finding: at least 50 CIFAR-10 test images (indices listed), for one RN18/PreActRN18 L2 model, on which the skeptic's OWN run of standard AutoAttack (autoattack package, version='standard', norm='L2', eps=0.5, seed 0, full 4-attack ensemble, run on exactly those indices) finds no adversarial example but the attacker's saved perturbations (checked for L2 norm <= 0.5 + 1e-6, range, and misclassification by the skeptic's forward pass) do. This is NOT a leaderboard change and must be reported as such; it does not count if the attacker's x_adv merely reproduce AutoAttack with other seeds (the attacker must disclose the method and seeds).

## How a win is checked

Skeptic writes their OWN checker (never runs the author's): pip install robustbench autoattack torch torchvision; model = robustbench.utils.load_model(<Model>, dataset='cifar10', threat_model='L2').eval; record sha256 of the downloaded weight file and the robustbench version; load the torchvision CIFAR-10 test set (10,000 images, ToTensor only) in canonical order; load the author's x_adv tensor and manifest (sha256 of the tensor file must match the manifest frozen in REPRODUCE.md); assert shape 10000x3x32x32 and dtype float32; in float64 compute per-image d = ||(x_adv - x).reshape(10000, -1)||_2 and assert d.max <= 0.5 + 1e-6 (one norm over all 3072 pixels per image, never per channel/row) and x_adv.min >= 0, x_adv.max <= 1; compute clean and adversarial predictions in batches on CPU in eval mode (RN18 ~5-10 min, WRN-28-10 ~30-60 min); robust_acc = mean(clean_correct & adv_correct) with argmax ties counted as not fooled. Re-fetch https://raw.githubusercontent.com/RobustBench/robustbench/master/model_info/cifar10/L2/<Model>.json live (plain curl, default UA, no retries through 403/429), quote value and fetch time, compare against min(autoattack_acc, external) with the 20-image margin. The NOVELTY skeptic searches arXiv (last 24 months) for full-test-set L2 eps=0.5 values for the same model (FMN, ALMA, DDN, APGDmin, Adversarial Frontiers arXiv:2607.19855, HO-FMN arXiv:2407.08806 which is Linf-only) and fails the claim if any is lower. For p3: run autoattack.AutoAttack(model, norm='L2', eps=0.5, version='standard', seed=0) on exactly the listed indices and confirm it finds no adversarial example on >= 50 of them while the author's perturbations misclassify under the skeptic's own forward pass. If the GitHub JSON cannot be fetched today, the comparison is PENDING TABLE CHECK and no meets_* may be true.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://robustbench.github.io/>

## Sources

- <https://robustbench.github.io/>
- <https://github.com/RobustBench/robustbench/tree/master/model_info/cifar10/L2>
- <https://github.com/fra31/auto-attack>
- <https://arxiv.org/abs/2607.19855>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Minimum-norm attacks as a complement to fixed-eps APGD: run FMN-L2 / DDN / ALMA to find the smallest fooling perturbation per image, then keep those with norm <= 0.5; minimum-norm methods often beat fixed-budget projected methods on exactly the borderline images AutoAttack misses.
- APGD-L2 with many restarts and long schedules on the residual robust set of an RN18 model, with targeted versions against all 9 classes and per-image loss selection (CE, DLR, CW-margin).
- Transfer-seeded starts from other L2 robust models and from the same model's Linf adversarial examples rescaled to the L2 ball.
- Boundary polishing: after any success, binary-search the perturbation scale toward the clean image to free budget, then re-run a few APGD steps from the boundary point; also try Linf-to-L2 'corner' starts (sign patterns scaled to norm 0.5).
- Square Attack L2 with large query budgets on the residual images of a small model.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Computing the L2 norm per channel or per row, or in float32 where rounding masks violations; always a single float64 norm over all 3072 pixels per image.
- Loading the Linf-trained variant of a model name instead of the L2 variant (threat_model argument), or attacking in normalised input space.
- Clipping to [0,1] after the norm check (clipping can only shrink the norm, but the saved tensor must itself be checked).
- Seed variance and tiny margins; fewer than 10 images is noise. Also compare with the live JSON, not the website or a cached copy.
- Novelty: minimum-norm attack papers (FMN, ALMA, DDN) report L2 robust accuracies for several RobustBench models; the NOVELTY skeptic must search for them.
- Prior art: Adversarial Frontiers (arXiv:2607.19855, Jul 2026) Table 6 reports L2 eps=0.5 robust accuracy on 1000-sample subsets for Augustin, Engstrom, Rade and Sehwag L2 models and did NOT beat AutoAttack on them (equal or +0.1); it did beat AA on Linf-trained models under L2, which are NOT on the L2 leaderboard. Do not confuse the two, and do not compare a 10k-image number against a 1k-subset number.
- Cheap non-wins: re-running standard AutoAttack with several seeds and taking the per-image union, or adding restarts, gains a handful of images; that is why the margin is 20 images, and the author must disclose the method and seeds. A multi-seed AA union by itself is not a 'stronger attack' finding.
- Shape/dtype: the saved tensor must be the full 10,000 images in canonical torchvision order (not a subset, not shuffled); a per-image index map is not acceptable for the full criterion or p1/p2.
- Compute: FMN/DDN-style attacks on an RN18 over 10k images are CPU-hours; APGD-L2 with many restarts or the full standard AutoAttack on the whole test set is CPU-days on a WRN; do not claim a full-set result from a partial run.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/ml-robustness/robustbench-cifar10-l2-beat-autoattack.md
```

Already set up? Say `run V3R1T4S on robustbench-cifar10-l2-beat-autoattack`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `robustbench-cifar10-l2-beat-autoattack`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
