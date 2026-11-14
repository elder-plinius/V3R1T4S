# Baseline Record Provenance — `darkmachines-unsupervised-median-total-improvement`

- **Primary Benchmark Repository**: https://github.com/bostdiek/DarkMachines-UnsupervisedChallenge
- **Official Hackathon Dataset (Zenodo 3961917)**: https://zenodo.org/records/3961917
- **Challenge Paper**: Aarrestad et al., *The Dark Machines Anomaly Score Challenge: Benchmark Data and Model Independent Event Classification for the Large Hadron Collider*, SciPost Phys. 12, 043 (2022), https://arxiv.org/abs/2105.14027
- **Live Fetch Timestamp (UTC)**: `2026-11-07T16:40:00Z`

## SHA-256 Hashes of Official Challenge Evaluation Files (`bostdiek/DarkMachines-UnsupervisedChallenge`)

| File Path | Size (Bytes) | SHA-256 Digest |
| :--- | ---: | :--- |
| `data/AE.csv` | `2255` | `3387472cc523389b832b7643f2876c0d0fb2704194d3bf8829ead2bba907ff88` |
| `data/VAE.csv` | `331765` | `09b5bbb043d017179eede1439427bbf50c2ddd6a2c690b75fb9bd02066cd2f36` |
| `data/DeepSetVAE.csv` | `17574` | `825a45a041c920bf148e4ae9ea44eeebc89735a8febca0d5f48c8f606358678f` |
| `data/ConvVAE_and_Flows.csv` | `27415` | `69e4876de6d184125157909d5b06f3b303a07d1fc2ce631e65a40d3b6c32ebc0` |
| `data/CNN_VAE.csv` | `3202` | `a2da11fd0a945622346b156bff089e19573165b8786898f85b9aebf69ff08e0d` |
| `data/CNN_BVAE.csv` | `3373` | `e36097acc888e82bf754e3ed18f3d8f697ee4b17a7c40aee7ce98c8ac8b263d4` |
| `data/KDE.csv` | `126204` | `9acc029214c10fbd3ee78defe506bafa68c84c058b35299646f2cbfa1c08d3bc` |
| `data/Flow.csv` | `4838` | `e2e17152c3222f6ea089706836a6b0f274a041c717a1138c93669629536098e0` |
| `data/DeepSVDD.csv` | `154715` | `5264a53506373a30f93f5b095f6ca14eef62710f448efd5c30d74bff9e52fb27` |
| `data/Combined.csv` | `19439` | `7754b06b4a820769ac38986e94b299a54c2e1e845ae30e013e99a4bbc3c5f3b6` |
| `data/DAGMM.csv` | `1737028` | `baa7ec77a80d98308f620f75daf2a0cc243c2c9fa582208980d3c40434c1ba65` |
| `data/ALAD.csv` | `459932` | `b2fcce32e0c5fb69e672ce9e4a1856b847e22ac2abecefffdf8f3fba69bc0604` |
| `data/MethodsInLatentSpaceOfVAE.csv` | `1127162` | `696d4ab1290b7cbcc56fadca08fd6a33d351f6563b6da332599bb29a67f59e6f` |

## Baseline Records Audited Across All 1,040 Challenge Detectors

1. **`p1` Target — Chargino-Neutralino Bottleneck Signals in Channel 2a**:
   - Across all 1,040 unsupervised detectors in `bostdiek/DarkMachines-UnsupervisedChallenge` evaluated across all 4 channels (`1`, `2a`, `2b`, `3`), the best Total Improvement ($\text{TI} = \max_{\text{chan}, \epsilon_B \in \{10^{-2}, 10^{-3}, 10^{-4}\}} \epsilon_S / \sqrt{\epsilon_B}$) on the two hardest electroweakinos is:
     - `chaneut_cha300_neut100` (Channel 2a): **Best 1,040 detector TI = `1.1000`** (`Flow-Efficient_Likelihood`, with $\epsilon_S(10^{-2}) = 0.11, \epsilon_S(10^{-3}) = 0.01, \epsilon_S(10^{-4}) = 0.01$).
     - `chaneut_cha400_neut200` (Channel 2a): **Best 1,040 detector TI = `1.0000`** (`Combined-AVG-DeepSVDD-Flow` and `Combined-PROD-DeepSVDD-Flow`; `Flow-Efficient_Likelihood` achieves `0.9000`).
2. **Minimum TI Floor Across All 19 Signals**:
   - The full-win minimum-TI floor is `0.90` (`Flow-Efficient_Likelihood` min TI = `0.9000` on `chaneut_cha400_neut200`), and the `p2` minimum-TI floor is `0.80`.
3. **Forensic Audit of `Flow-Efficient_Likelihood`'s 15.0 Median TI**:
   - In `data/Flow.csv`, `Flow-Efficient_Likelihood` reports identical $\epsilon_S(10^{-3}) == \epsilon_S(10^{-4})$ in **34 out of 34** signal-channel rows (`sha256: e2e17152c3222f6ea089706836a6b0f274a041c717a1138c93669629536098e0`). When evaluated under the strict non-tie exceedance rule ($\text{mean}(s_{\text{bg}} \ge \tau) \le \epsilon_B$), tied/saturated upper-tail scores cannot claim the $10\times$ $\text{SI}$ multiplier from $\epsilon_B = 10^{-3} \to 10^{-4}$.
