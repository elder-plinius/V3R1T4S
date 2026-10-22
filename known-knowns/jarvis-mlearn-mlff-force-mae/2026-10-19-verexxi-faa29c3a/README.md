# mlearn Mo forces: from-scratch MACE ensemble, test force MAE 0.097400 eV/A

Target: bank id `jarvis-mlearn-mlff-force-mae`, cell `mlearn_Mo_forces` (JARVIS-Leaderboard, NIST). One element, one package.

## What
A 3-seed ensemble of from-scratch MACE models (32 channels, r_max 4.5, trained on the 194 official train ids, seeds 1 to 3) gets a force MAE of 0.097400 eV/A on the 23 official mlearn_Mo_forces test ids. This is 47.2% below the 0.184341 best listed in the snapshot (fetched 2026-10-19T22:52:53Z). Re-running the saved models reproduces the predictions to 2.4e-7 eV/A. This covers only mlearn Mo forces, and it is not a verified comparison against the numeric results of Zuo et al. 2020 or of any other literature.

Files of this package: the predictions file is `object/predictions_Mo_forces_test.csv`, the three trained models are `object/models/mace_Mo_seed1.model` to `seed3.model`, the training scripts are in `how-we-built-it/`, and the checker is `verify-it-yourself/check_predictions.py`.

## Check it yourself
```sh
sh verify-it-yourself/run_checks.sh
```
Needs internet once (it downloads the benchmark json from GitHub and checks its sha256). Expected last line: `PASS` (it exits non-zero and prints `FAIL` otherwise; it also fails if a digit of anything in `object/` is changed). Rough time: a few seconds. If a Python with numpy, ase, torch and mace-torch is available (set `MLFF_PYTHON`), it also downloads the public jarvis 'mlearn' structures (about 2.5 MB, sha256-checked) and re-runs the three saved models on the test structures; the maximum difference to the predictions file must be at most 1e-6 eV/A (about 30 s on a laptop CPU).

## Compared to
| item | value | source |
|---|---|---|
| best listed force MAE on the live task page when staged | 0.18434104563832232 (snap_mlearn) | https://pages.nist.gov/jarvis_leaderboard/AI/MLFF/mlearn_Mo_forces/ , fetched 2026-10-19T22:52:53Z, HTTP 200, page sha256 63899ab54bb1fc94cce6f3bba19f29eaa58c2568a3738b36feff9604aaae2d34 |
| this package (3-seed ensemble) | 0.09739976116095339 | `object/predictions_Mo_forces_test.csv` |
| improvement over the live best | 47.2% (the criterion asks for at least 5%) | computed by the checker |
| seed MAEs (sd 0.001358) | 0.106269, 0.104097, 0.106594 | `how-we-built-it/test_scores.json` |
| zero-force baseline / train-mean-force baseline | 0.9496 / 0.9496 | same test ids |
| ALIGNN 2.0 table (arXiv 2609.19487, marked there as pending verification) | 0.1121 | https://arxiv.org/abs/2609.19487 (same train/test sizes) |
| Zuo et al. 2020 | errors are only in its Figure 3 on its own split; no number was extracted here | https://arxiv.org/abs/1906.08888 |

## Not claimed
- Only the force task of this one element. No claim on energies, stresses or any other element in this package (the partial wins p1 and p2 were not attempted).
- Not a claim that the model is a good general potential: it was fitted to this element's few hundred DFT configurations only.
- The Zuo et al. 2020 comparison is qualitative (figure-only numbers, a different split).
- Test results for every element attempted in this run (the claim is for Mo only; an element is claimed only if its own package exists):

| element | ensemble test MAE (eV/A) | seeds 1 / 2 / 3 | zero-force baseline | live best when staged | vs live best |
|---|---|---|---|---|---|
| Mo | 0.097400 | 0.106269 / 0.104097 / 0.106594 | 0.9496 | 0.18434104563832232 | 47.2% below |
| Li | not scored on test in this run | | | | |
| Si | not scored on test in this run | | | | |
| Ge | not scored on test in this run | | | | |
| Ni | not scored on test in this run | | | | |
| Cu | not scored on test in this run | | | | |

## Review record
Three skeptic files and the gate are in `panel/` (subagents started in the same session on the same machine, each shown only the claim folder; the gate is the main session's own). `panel/gate.md` records the final status.

## Credits
- JARVIS-Leaderboard: Kamal Choudhary and co-workers, NIST (npj Comput. Mater. 2024), https://github.com/usnistgov/jarvis_leaderboard , task pages at https://pages.nist.gov/jarvis_leaderboard/ .
- mlearn datasets: Yunxing Zuo, Chi Chen, Xiangguo Li, Zhi Deng, Yiming Chen, Joerg Behler, Gabor Csanyi, Alexander Shapeev, Aidan Thompson, Mitchell Wood, Shyue Ping Ong, J. Phys. Chem. A 124, 731 (2020), https://arxiv.org/abs/1906.08888 ; https://github.com/materialsvirtuallab/mlearn .
- The listed entry compared against (snap_mlearn) and the other listed entries are their contributors' work on the leaderboard.
- MACE: Ilyes Batatia, David Kovacs, Gregor Simm, Christoph Ortner, Gabor Csanyi, https://github.com/ACEsuit/mace (mace-torch 0.3.16 was used for training).
- ASE (Atomic Simulation Environment), PyTorch, jarvis-tools (structures from the figshare 'mlearn' archive, https://doi.org/10.6084/m9.figshare.22721047).
- ALIGNN 2.0 authors (Lee, Campbell, Ajith, Kalinin, Wolverton, Choudhary), arXiv 2609.19487, for the later reference values quoted above.
