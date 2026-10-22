# Polaris MoleculeACE Activity-Cliff MSE (`moleculeace-chembl287-ki` & 30-Benchmark CLSS Sweep)

## What

A single fixed, deterministic, CPU-only CLSS recipe (claim/run_clss_moleculeace.py) fit strictly on stereo-stripped InChIKey[:14]-disjoint training splits (overlap == 0 across all 30/30 benchmarks) achieves test MSE 0.40802135 on moleculeace-chembl287-ki (claim/CHEMBL287_Ki_test_predictions.csv, sha256 05d8ae3a3797f666ed320364280c2ba0c099417174d42a0a4736f0366726623c, n_train = 1,061, n_test = 267, n_cliff = 103) vs live Polaris best 0.50318131 (-18.9117% relative) and MoleculeACE paper best 0.51009699 (-20.0110% relative) with 99.97% paired bootstrap win rate vs reproduced SVM+ECFP and 97.98% scalar bootstrap win rate vs Polaris best across 10,000 resamples (seed=0), while lowering cliff_mol==1 MSE (n = 103, at least 40) to 0.50213600 vs paper best 0.61875106 (-18.8468%) and non-cliff MSE to 0.34891276 vs 0.41681673 (-16.2911%, p2), and beating live Polaris best MSE on 29/30 MoleculeACE benchmarks (21/30 with at least 5% relative margin and at least 95% bootstrap win rate, p3) with 30-target macro-average cliff RMSE 0.7211 (overall RMSE 0.6303).

Path note: the sentence above is quoted word for word from `panel/gate.md`, and it names the panel's `claim/` folder. In this package the same files, with identical bytes, are in `object/` (headlined by `object/CHEMBL287_Ki_test_predictions.csv`, `object/CHEMBL287_Ki_manifest.json`, `object/moleculeace_30_sweep_manifest.json`, and `object/predictions/CHEMBL*_test_predictions.csv`) and `how-we-built-it/run_clss_moleculeace.py`.

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: `python3` with `numpy`, `pandas`, `scikit-learn`, `scipy`, `rdkit` (and `lightgbm` if running optional end-to-end retraining).
- **Rough laptop time**: about 6 to 15 seconds for all 30 saved benchmarks and 400 permutation controls (~45 seconds if re-running end-to-end training on `CHEMBL287_Ki`).
- **Expected last line**: `ALL CHECKS PASS`

## Compared to

| Source | Benchmark / Subset | Listed Best MSE | Ours (CLSS MSE & Relative Margin) | URL | UTC fetch time |
|---|---|---:|---|---|---|
| Live Polaris Leaderboard (`autosota-moleculeace-chembl287-ki`) | `moleculeace-chembl287-ki` (`CHEMBL287_Ki`, overall test $n=267$) | `0.50318131` | **`0.40802135`** (**`-18.9117%`**, `97.98%` scalar bootstrap, `99.97%` paired bootstrap) | https://polarishub.io/benchmarks/molecularml/moleculeace-chembl287-ki | 2026-10-19T15:07:54Z |
| MoleculeACE Paper (`SVM+ECFP`, van Tilborg et al., *JCIM* 2022) | `CHEMBL287_Ki` (overall test $n=267$) | `0.51009699` | **`0.40802135`** (**`-20.0110%`**, `99.97%` paired bootstrap) | https://raw.githubusercontent.com/molML/MoleculeACE/main/MoleculeACE/Data/results/MoleculeACE_results.csv | 2026-10-19T11:44:45Z |
| MoleculeACE Paper (`RF+PHYSCHEM` / `MLP+ECFP`, *JCIM* 2022) | `CHEMBL287_Ki` (`cliff_mol == 1`, $n=103$, `p2`) | `0.61875106` | **`0.50213600`** (**`-18.8468%`** vs Paper best, **`-23.7555%`** vs `SVM+ECFP` `0.65858689`) | https://raw.githubusercontent.com/molML/MoleculeACE/main/MoleculeACE/Data/results/MoleculeACE_results.csv | 2026-10-19T11:44:45Z |
| Live Polaris 3-Entry Leaderboard (`CHEMBL234_Ki`) | `moleculeace-chembl234-ki` ($n=733$, 3 entries) | `0.37022063` | **`0.36037801`** (**`-2.6586%`** vs Polaris, **`-6.7498%`** vs Paper `0.38646355`) | https://polarishub.io/benchmarks/molecularml/moleculeace-chembl234-ki | 2026-10-19T15:07:55Z |
| Live Polaris 3-Entry Leaderboard (`CHEMBL236_Ki`) | `moleculeace-chembl236-ki` ($n=521$, 3 entries) | `0.44968493` | **`0.44350711`** (**`-1.3738%`** vs Polaris, **`-8.5015%`** vs Paper `0.48471536`) | https://polarishub.io/benchmarks/molecularml/moleculeace-chembl236-ki | 2026-10-19T15:07:56Z |
| All 30 Live Polaris MoleculeACE Benchmarks (`p3`) | 30-Target Sweep (`object/moleculeace_30_sweep_manifest.json`) | `30` live tables | **`29 / 30` strict wins** (`21 / 30` with $\ge 5\%$ margin + $\ge 95\%$ bootstrap; macro cliff RMSE **`0.7211`** vs `Monroe` `0.737` & `SVM+ECFP` `0.7511`) | https://polarishub.io/benchmarks/molecularml/moleculeace-chembl287-ki | 2026-10-19T15:07:54Z |

Snapshot metadata, with HTTP status and page sha256: `the-record-we-beat/README.md`.

## Not claimed

- On 1 of the 30 MoleculeACE benchmarks (`CHEMBL2835_Ki`, JAK1 kinase, where the test set has $n = 126$ molecules and small variance), our universal recipe achieves `MSE = 0.175724` vs the listed `0.166184` (`29 / 30` wins overall).
- Zero external pre-training or multi-target ChEMBL lookup was used; each of the 30 models was fit strictly on its own target's `InChIKey[:14]`-disjoint `split == 'train'` subset.
- Not peer reviewed. Checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Credits

- **Derek van Tilborg, Alisa Alenicheva, and Francesca Grisoni** (*Exposing the Limitations of Molecular Machine Learning with Activity Cliffs*, *Journal of Chemical Information and Modeling* 2022, https://github.com/molML/MoleculeACE), authors of the MoleculeACE benchmark suite and baseline results (`the-record-we-beat/MoleculeACE_results.csv`).
- **Polaris Hub** (`polarishub.io`, https://polarishub.io/benchmarks/molecularml/moleculeace-chembl287-ki), host of the 30 `molecularml/moleculeace-*` leaderboards.
- Contributor credit: `mizopl`.
