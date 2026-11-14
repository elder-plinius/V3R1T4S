# How We Found It (`contributor text, unverified`)

> *Note: This section is contributor text, unverified by the automated check runner. All verified claims rest solely on `object/` and `verify-it-yourself/run_checks.sh`.*

## 1. Diagnosing Why All 1,040 Challenge Detectors Failed on Chargino-Neutralino Production (`chaneut_cha300_neut100` and `chaneut_cha400_neut200`)
In the Dark Machines Unsupervised Challenge (Aarrestad et al., SciPost Phys. 12, 043, 2022), every single one of the 1,040 submitted detectors (spanning autoregressive spline flows, VAEs, $\beta$-VAEs, ConvVAEs, DeepSetVAEs, KDEs, DAGMMs, ALADs, and DeepSVDD hybrids) stalled at $\text{TI} \le 1.10$ on `chaneut_cha300_neut100` and $\text{TI} \le 1.00$ on `chaneut_cha400_neut200` in Channel `2a` ($\ge 3$ leptons, $E_T^{\text{miss}} > 50\text{ GeV}$).

Why? Raw four-vector density estimators and autoencoders spread model capacity evenly across azimuthal angles ($\phi$), pseudorapidities ($\eta$), and low-$p_T$ jet radiation. In $pp \to \tilde{\chi}_1^\pm \tilde{\chi}_2^0 \to W^\pm Z \tilde{\chi}_1^0 \tilde{\chi}_1^0$, the $Z \to \ell^+\ell^-$ pair sits right on the Standard Model $Z$-boson mass peak ($M_{\ell\ell} \approx M_Z = 91.1876\text{ GeV}$), making the event look like ordinary SM $WZ$ diboson background to a density estimator. The BSM excess hides specifically in **upper-tail relativistic endpoint violations**:
1. The transverse mass $M_T(\ell_W, E_T^{\text{miss}})$ of the third lepton (after pairing the opposite-sign same-flavor $Z$ candidate) violating the SM Jacobian endpoint $M_W = 80.379\text{ GeV}$ (`mt_lw_wz`),
2. The stransverse mass $M_{T2}(Z, \ell_W; \vec{p}_T^{\text{miss}})$ (`mt2_z_lw`) and dilepton stransverse mass $M_{T2}(\ell_1, \ell_2; \vec{p}_T^{\text{miss}})$ (`mt2_ll12`), and
3. Missing-energy calorimeter significance $E_T^{\text{miss}} / \sqrt{L_T}$ (`met_lt_sig`) and $E_T^{\text{miss}} / \sqrt{H_T}$ (`met_had_sig`).

## 2. 27-Invariant Upper-Tail Log-Survival POT & Multiplicity-Stratum Conditioning
Instead of fitting black-box neural networks on raw coordinates, we engineered a deterministic C featurizer (`how-we-built-it/dm_featurize.c`) that maps variable-length LHC object lists onto 27 fundamental Lorentz-invariant, stransverse ($M_{T2}$), contransverse ($M_{CT}$), and missing-energy significance observables.

On the odd-`event_ID` Standard Model background of each channel, we apply a one-sided **Peaks-Over-Threshold (POT) log-survival transformation**:
$$u_j(x) = \max\bigl(0, -\ln(2(1 - \hat{F}_{j,\text{bg}}(x_j)))\bigr)$$
with linear Generalized Pareto tail extrapolation above the $99.9\%$ empirical background quantile, de-weighted by squared positive correlation crowding $w_j \propto (\sum_k \max(0, R_{jk})^2)^{-1}$. Combining the $L_1$, $L_2$, and $L_3$ upper-tail norms (`PotHull_Hybrid_Lp3`), positive random support-hull exceedances (`PotHull_L1_L2_Hull`), or multiplicity-stratum $(n_j, n_b, n_\ell)$ upper-tail Z-scores (`PotStrataZ_Lp3`) immediately lifts `chaneut_cha300_neut100` to **`TI = 1.4000` / `1.6000`** (`> 1.1000`), lifts `chaneut_cha400_neut200` to **`TI = 1.6000` / `1.7000`** (`> 1.0000`), and raises the minimum TI across all 19 BSM signals to **`1.0000 >= 0.9000`**.
