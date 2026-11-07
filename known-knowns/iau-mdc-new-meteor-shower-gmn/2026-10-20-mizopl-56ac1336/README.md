# `iau-mdc-new-meteor-shower-gmn` — Multi-Year, Per-Meteor Multi-Country September Cepheus Meteor Shower Candidate (`GMN_NEW_SHOWER_M1_CEPHEUS_MC_163`)

## What

16-meteor multi-year, per-meteor multi-country September Cepheus shower candidate (`GMN_NEW_SHOWER_M1_CEPHEUS_MC_163`, 2023–2026) in public Global Meteor Network trajectory summary tables (`2018–2026`), where every counted meteor is unique (`min Delta_t = 1,332.4 s`), triangulated by `3..8` independent stations across `2..3` countries (`15` countries and `62` stations total), cohesive within `max D_SH(mean, member) = 0.0730 < 0.10` (`max D_SH(median, member) = 0.0795 < 0.10`), isolated from all `2,197` rows of the 3 November 2026 IAU Meteor Data Center list (`min D_SH = 0.2819 >= 0.20`, minimum radiant separation `19.52 deg > 5.0 deg` within `+-5 deg` solar longitude), and exceeding the local sporadic background above `5 sigma` both before (`14.26 sigma` Gaussian / `7.66 sigma` Poisson) and after look-elsewhere correction across `103` ecliptic `3.5 deg` windows (`7.03 sigma`) and `43,228` MDC-isolated multi-country seed trajectories (`6.11 sigma`).

---

## Single-Claim Scope & Deduplication Summary

In accordance with `kit/SUBMIT.md` (§1, one claim per package), this package files strictly **one** claim: the multi-year, per-meteor multi-country September Cepheus meteor shower candidate **`GMN_NEW_SHOWER_M1_CEPHEUS_MC_163`** (`M1_Cepheus_MC`, provisional designation *September $\xi$-Cepheids*, $N = 16$).

1. **Each meteor is counted strictly once:** Minimum pairwise time separation across all 16 member trajectories is **`1,332.405 s` (`22.21 minutes`)**. The duplicate trajectory solution `20260907031956_h3OXu` (solved `0.105 s` after `20260907031956_faRoT`) and all 8 single-country trajectories of the earlier `M1_Cepheus_Core` slice (including `20250904204409_BKOSN`) are excluded.
2. **Every member individually meets `>= 3` independent stations in `>= 2` countries:** All `16/16` (`100%`) trajectories have `IAU No == -1`, `num_stat >= 3` (`3..8` stations per meteor, matching `len(stations)`), and `n_countries >= 2` (`2..3` countries per meteor). Across the 16 trajectories, the cluster spans **`4` consecutive years** (`2023`: 2, `2024`: 3, `2025`: 4, `2026`: 7), **`15` countries** (`AT, BA, BE, BG, CZ, DE, DK, FR, HR, HU, IT, NL, RO, SI, UK`), and **`62` distinct GMN stations**.
3. **Orbital cohesion ($D_{\text{SH}} < 0.10$):**
   - **Mean Orbit ($N = 16$):** $q = 0.957282\text{ AU}$, $e = 0.719091$, $i = 41.843721^\circ$, $\Omega = 163.309066^\circ$, $\omega = 208.374550^\circ$, $\lambda_\odot = 163.305463^\circ$, $\alpha_g = 304.770747^\circ$, $\delta_g = +59.829877^\circ$, $V_g = 26.413168\text{ km/s}$.
   - **Median Orbit ($N = 16$):** $q = 0.958641\text{ AU}$, $e = 0.722692$, $i = 42.179553^\circ$, $\Omega = 163.010853^\circ$, $\omega = 207.878130^\circ$, $\lambda_\odot = 163.007009^\circ$.
   - **Medoid Trajectory:** `20260907031956_faRoT` (mean $D_{\text{SH}}$ to the other 15 members $= 0.053828$, maximum $D_{\text{SH}}$ to any member $= 0.070696 < 0.10$).
   - **Maximum Member $D_{\text{SH}}$:** $\max D_{\text{SH,exact}}(\text{mean}, \text{member}) = 0.073001 < 0.10$ ($\text{planar} = 0.071959 < 0.10$); $\max D_{\text{SH,exact}}(\text{median}, \text{member}) = 0.079486 < 0.10$ ($\text{planar} = 0.083053 < 0.10$); single-linkage clustering at threshold $D_{\text{SH}} \le 0.10$ forms a single connected component of all 16 members.

---

## All 16 Member Trajectories (`object/m1_cepheus_mc_gmn_lines.txt`)

Verbatim GMN lines are stored in `object/m1_cepheus_mc_gmn_lines.txt` (`sha256: 4f0bf9a2e5e1c56ac61f582a63923c4af28d6536a00bd1df7bf6203796b5212d`):

| # | Trajectory ID | UTC Timestamp | $\lambda_\odot$ ($^\circ$) | $\alpha_g$ ($^\circ$) | $\delta_g$ ($^\circ$) | $V_g$ (km/s) | $q$ (AU) | $e$ | $i$ ($^\circ$) | $\Omega$ ($^\circ$) | $\omega$ ($^\circ$) | `num_stat` | `n_countries` (Countries) | Stations | $D_{\text{SH,exact}}(\text{mean})$ |
| :-: | :--- | :--- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :--- | :--- | :-: |
| 1 | `20230905191934_2YuSb` | `2023-09-05 19:19:34.560504` | `162.6514` | `303.922` | `+56.664` | `25.524` | `0.9511` | `0.7396` | `39.555` | `162.6542` | `209.935` | `3` | `2` (`HR,HU`) | `HR0024,HU0001,HU0002` | `0.0479` |
| 2 | `20230906022249_hhc3N` | `2023-09-06 02:22:49.990169` | `162.9363` | `308.220` | `+61.467` | `27.445` | `0.9537` | `0.7033` | `44.139` | `162.9401` | `209.652` | `6` | `3` (`BE,DE,NL`) | `BE0002,BE0006,DE0001,DE000Q,NL0009,NL000A` | `0.0452` |
| 3 | `20240906215308_leULY` | `2024-09-06 21:53:08.103729` | `164.4469` | `305.375` | `+62.800` | `27.041` | `0.9640` | `0.6948` | `43.651` | `164.4499` | `206.612` | `4` | `2` (`HR,IT`) | `HR001E,HR001P,HR0021,IT000A` | `0.0441` |
| 4 | `20240907011358_DU4pM` | `2024-09-07 01:13:58.132113` | `164.5823` | `305.038` | `+62.915` | `28.005` | `0.9655` | `0.7492` | `44.728` | `164.5859` | `205.570` | `6` | `2` (`AT,CZ`) | `AT0002,CZ0001,CZ0009,CZ000H,CZ000K,CZ000N` | `0.0657` |
| 5 | `20240908005446_04U3u` | `2024-09-08 00:54:46.108468` | `165.5402` | `304.168` | `+62.176` | `27.831` | `0.9652` | `0.7722` | `43.999` | `165.5439` | `205.360` | `3` | `3` (`CZ,DE,DK`) | `CZ0006,DE000S,DK0008` | `0.0730` |
| 6 | `20250904204411_UgwAd` | `2025-09-04 20:44:11.776135` | `162.2168` | `301.663` | `+57.214` | `25.248` | `0.9584` | `0.7326` | `39.292` | `162.2204` | `207.995` | `8` | `3` (`BE,NL,UK`) | `BE0009,NL000M,UK006D,UK00AN,UK00B1,UK00B2,UK00BJ,UK00CA` | `0.0505` |
| 7 | `20250904213132_JGqu4` | `2025-09-04 21:31:32.993233` | `162.2486` | `309.015` | `+62.251` | `27.566` | `0.9542` | `0.6797` | `44.802` | `162.2517` | `209.850` | `3` | `2` (`BA,HR`) | `BA0001,BA0004,HR002M` | `0.0668` |
| 8 | `20250904233003_0EHCU` | `2025-09-04 23:30:03.184882` | `162.3284` | `303.361` | `+57.973` | `24.820` | `0.9556` | `0.6787` | `39.270` | `162.3325` | `209.463` | `4` | `2` (`BE,FR`) | `BE000P,BE0011,FR000X,FR0013` | `0.0616` |
| 9 | `20250905030107_S2X3S` | `2025-09-05 03:01:07.495188` | `162.4704` | `305.910` | `+61.252` | `27.679` | `0.9589` | `0.7402` | `44.101` | `162.4746` | `207.761` | `4` | `2` (`BE,NL`) | `BE000D,BE000E,NL0001,NL0010` | `0.0484` |
| 10 | `20260904215007_GPg1D` | `2026-09-04 21:50:07.864071` | `162.0092` | `305.949` | `+55.677` | `25.531` | `0.9418` | `0.7320` | `39.476` | `162.0125` | `212.466` | `4` | `2` (`BA,HR`) | `BA0001,BA0005,HR0025,HR002L` | `0.0623` |
| 11 | `20260905002604_C1nyH` | `2026-09-05 00:26:04.868398` | `162.1141` | `301.037` | `+56.992` | `25.168` | `0.9599` | `0.7387` | `39.048` | `162.1181` | `207.531` | `4` | `2` (`BG,RO`) | `BG000H,RO000H,RO000W,RO0010` | `0.0587` |
| 12 | `20260906001707_8khWR` | `2026-09-06 00:17:07.096622` | `163.0777` | `304.145` | `+57.145` | `25.196` | `0.9518` | `0.7142` | `39.333` | `163.0816` | `210.009` | `5` | `3` (`BE,DE,NL`) | `BE0006,BE000M,DE0001,NL0006,NL000S` | `0.0481` |
| 13 | `20260906003919_yFT3F` | `2026-09-06 00:39:19.501505` | `163.0926` | `304.216` | `+60.133` | `26.591` | `0.9598` | `0.7274` | `42.118` | `163.0964` | `207.606` | `5` | `3` (`CZ,DE,HR`) | `CZ0001,CZ000K,CZ000N,DE0016,HR002X` | `0.0155` |
| 14 | `20260907021357_CscTy` | `2026-09-07 02:13:57.630473` | `164.1265` | `303.785` | `+61.789` | `26.821` | `0.9652` | `0.7169` | `42.860` | `164.1304` | `206.026` | `4` | `3` (`HR,HU,SI`) | `HR002X,HR002Z,HU000D,SI0002` | `0.0308` |
| 15 | `20260907031956_faRoT` | `2026-09-07 03:19:56.733280` | `164.1710` | `304.876` | `+60.664` | `26.577` | `0.9595` | `0.7180` | `42.241` | `164.1750` | `207.717` | `5` | `2` (`BE,FR`) | `BE0006,BE000L,BE000M,BE000Q,FR000Y` | `0.0125` |
| 16 | `20260907204502_dfyFL` | `2026-09-07 20:45:02.580285` | `164.8755` | `306.784` | `+59.914` | `25.568` | `0.9520` | `0.6680` | `40.888` | `164.8784` | `210.442` | `3` | `2` (`BE,DE`) | `BE000V,DE0005,DE0007` | `0.0692` |

---

## Significance Above $5\sigma$ & Number of Windows Searched

1. **Background from the Same Solar-Longitude Window in Other Years & Sidebands:**
   - In the target solar-longitude window $\lambda_\odot \in [162.01^\circ, 165.54^\circ]$ ($\Delta\lambda_\odot = 3.53^\circ$) and orbital ball $D_{\text{SH}} < 0.075$:
     - **Prior 5 baseline GMN years (`2018–2022`):** `0` trajectories in `2018`, `0` in `2019`, `0` in `2020`, `0` in `2021`, and `0` in `2022` (`0` total across 5 baseline years).
     - **20 adjacent $3.5^\circ$ solar-longitude sideband windows** ($\Delta\lambda_\odot \in \{-25^\circ, \dots, -7^\circ, +6^\circ, \dots, +24^\circ\}$ with $\Omega$ shifted by $\Delta\lambda_\odot$): `0` trajectories in all 20 windows (`sideband_mean = 0.0`).
2. **400-Control Shuffled-Solar-Longitude & Orbital-Permutation Monte Carlo Test (`object/null_test_400_controls.json`):**
   - `200` solar-longitude shuffle controls across the $60^\circ$ sideband $\lambda_\odot \in [133.31^\circ, 193.31^\circ]$ + `200` orbital-tuple permutation controls within the $3.5^\circ$ window at $D_{\text{SH}} < 0.075$:
     - Control histogram: `{0: 129, 1: 150, 2: 84, 3: 32, 4: 4, 7: 1}` (`400` controls total).
     - `control_mean` $\mu_{\text{ctrl}} = 1.0925$, `control_std` $= 1.0132$, `effective_bg_sigma` $= \sqrt{1.0925} = 1.0452$, `best_control` $= 7 < 16$ (`real_beats_all_controls = "yes"`).
     - **Single-window Gaussian significance:** $Z = (16 - 1.0925) / 1.0452 = 14.26\sigma > 5.0\sigma$.
     - **Single-window exact Poisson tail:** $P(\text{Pois}(1.0925) \ge 16) = 7.0533 \times 10^{-14}$ ($\log_{10} p = -13.15$, one-sided Gaussian equivalent $Z_{\text{Pois}} = 7.66\sigma > 5.0\sigma$).
3. **Look-Elsewhere Correction Across the Number of Windows Searched:**

| Search Space Level | Number of Windows / Seeds Searched ($N_{\text{trials}}$) | Global $p$-Value ($1 - (1 - p_1)^{N_{\text{trials}}}$) | $\log_{10} p_{\text{global}}$ | Global Gaussian Equivalent $Z_{\text{global}}$ | Status vs $5.0\sigma$ |
| :--- | :-: | :-: | :-: | :-: | :-: |
| **Single target window** ($\Delta\lambda_\odot = 3.5^\circ, D_{\text{SH}} < 0.075$) | `1` | `7.0533e-14` | `-13.15` | **`7.66 sigma`** (`14.26 sigma` linear) | **PASS ($> 5\sigma$)** |
| **Full-ecliptic non-overlapping $3.5^\circ$ solar-longitude windows** ($360^\circ / 3.5^\circ$) | `103` | `7.2649e-12` | `-11.14` | **`7.03 sigma`** | **PASS ($> 5\sigma$)** |
| **Full-ecliptic $1^\circ$ solar-longitude bins** | `360` | `2.5392e-11` | `-10.60` | **`6.85 sigma`** | **PASS ($> 5\sigma$)** |
| **All MDC-isolated multi-country seed trajectories** ($D_{\text{SH}} \ge 0.22, \Delta\theta > 10^\circ$) | `43,228` | `3.0490e-09` | `-8.52` | **`6.11 sigma`** | **PASS ($> 5\sigma$)** |
| **All high-quality unassigned multi-country GMN trajectories** (`num_stat >= 3, n_countries >= 2`) | `173,358` | `1.2227e-08` | `-7.91` | **`5.88 sigma`** | **PASS ($> 5\sigma$)** |

---

## Check It Yourself

From the package root (`known-knowns/iau-mdc-new-meteor-shower-gmn/2026-10-20-mizopl-56ac1336/`):

```sh
sh verify-it-yourself/run_checks.sh
```

The standalone verifier `verify-it-yourself/check_meteor_claim.py` completes in `~0.15 s`, splits every trajectory's station list on commas, checks `len(stations) == num_stat >= 3` and `len(countries) == n_countries >= 2` for all 16 members, verifies pairwise time separation $\Delta t \ge 1,332.4\text{ s}$, recomputes the $16 \times 16$ Southworth–Hawkins $D_{\text{SH}}$ matrix and 156 IAU MDC neighbor distances directly from $(q, e, i, \Omega, \omega)$, verifies the 400-control and look-elsewhere statistics, and prints `PASS` (`exit 0`).

---

## Compared To

Full URL, byte size, row count, and SHA-256 citations are stored in `object/gmn_yearly_manifest.json` and `the-record-we-beat/table_status.md`:

### 1. IAU Meteor Data Center (MDC) Files (`ta3.sk`)

- **Live 3 November 2026 `streamfulldata2026.txt` (`2,197` rows):**
  - URL: `https://www.ta3.sk/IAUC22DB/MDC2022/Etc/streamfulldata2026.txt`
  - Header: `Last update: Nov 03, 20:00:00 UTC, 2026` (retrieved `2026-11-07T15:14:00Z`)
  - Size: `1,558,558` bytes (`2,197` rows `LP = 00001..02650`: `2,004` explicit orbits + `172` radiant-derived Keplerian orbits)
  - SHA-256: `ae1a84a546be1c72ee0cf74835bc5b928a0d1d4c4e01a18a7f17bdaee299e100`
  - All 5 rows added on 3 November 2026 (`LP = 02646..02650`: `M2026-R1`, `M2026-S1` [2 rows], `M2026-S2`, `M2026-U1`) have $D_{\text{SH}} \ge 0.2992$ from `GMN_NEW_SHOWER_M1_CEPHEUS_MC_163`. Across all `2,197` rows, $\min D_{\text{SH}}(\text{mean}, \text{MDC}) = 0.281872 \ge 0.20$ (`LP = 02584`, `53-Draconids / FDR #01206`), $\min D_{\text{SH}}(\text{member}, \text{MDC}) = 0.251127 \ge 0.20$, and $\min \Delta\theta = 19.5245^\circ > 5.0^\circ$ within $|\Delta\lambda_\odot| \le 5.0^\circ$ (`LP = 00731`, `nu-Draconids / NDR #00220`).
- **Initial 20 October 2026 `streamfulldata2026.txt` (`2,192` rows):**
  - URL: `https://www.ta3.sk/IAUC22DB/MDC2022/Etc/streamfulldata2026.txt` (`1,555,028` bytes, `sha256: 08409111125e83ef2f033b27e215fb4383e0f15f6e6a3d202f7dda3a27f027fe`)
- **Working List HTML (`roje_lista.php`, retrieved `2026-11-07T15:13:59Z`):**
  - URL: `https://www.ta3.sk/IAUC22DB/MDC2022/Roje/roje_lista.php` (`370,300` bytes, `sha256: 3d25556bdd5cc627acab13c4baca7d9df85a30afed0ee5e29e93e80e4724c2ef`)
- **New Reports 2023–2026 (`new_reports.php`, retrieved `2026-11-07T15:14:00Z`):**
  - URL: `https://www.ta3.sk/IAUC22DB/MDC2022/Dokumenty/new_reports.php` (`9,216` bytes, `sha256: f59617319b97414766b119e0abe5922dcb6a11521855d4ee643de9a031336d93`)

### 2. Global Meteor Network (GMN) Yearly Trajectory Summary Files (`2018–2026`)

| Year | URL | Bytes | Total Rows | `num_stat >= 3` | Unassigned `>= 3` | Unassigned Multi-Country (`>= 3` stat, `>= 2` countries) | SHA-256 Digest |
| :-: | :--- | --: | --: | --: | --: | --: | :--- |
| `2018` | `https://globalmeteornetwork.org/data/traj_summary_data/yearly/traj_summary_yearly_2018.txt` | `460,180` | `497` | `13` | `12` | `0` | `c89edd266b847874710f4d89bd0cce8a1a19e5ade57492a92904ae138ee34b52` |
| `2019` | `https://globalmeteornetwork.org/data/traj_summary_data/yearly/traj_summary_yearly_2019.txt` | `46,498,742` | `50,263` | `21,163` | `14,649` | `2,056` | `d78c1a04e131d33e291c413a024e6c6566818046f3322c44411e712b469c8f00` |
| `2020` | `https://globalmeteornetwork.org/data/traj_summary_data/yearly/traj_summary_yearly_2020.txt` | `115,779,832` | `125,098` | `50,622` | `35,483` | `5,885` | `c2f90b739ac442817103a43ca73ccea7ce6344ad2b4d1cdd92617d852b7dd68c` |
| `2021` | `https://globalmeteornetwork.org/data/traj_summary_data/yearly/traj_summary_yearly_2021.txt` | `196,153,342` | `211,851` | `91,104` | `61,768` | `10,132` | `cd1526118300abab9234c6c35995253eba364217ea0ba9996147f7b597924c63` |
| `2022` | `https://globalmeteornetwork.org/data/traj_summary_data/yearly/traj_summary_yearly_2022.txt` | `311,120,248` | `334,661` | `159,143` | `106,519` | `19,648` | `262fb31bd7c4e0cc2e7361d14161397fb131846901d9fd9ded9d00e9e728ef8a` |
| `2023` | `https://globalmeteornetwork.org/data/traj_summary_data/yearly/traj_summary_yearly_2023.txt` | `420,839,167` | `451,903` | `233,386` | `161,237` | `30,547` | `b1cf267cdd6fc80b3ecb2855bf27739d30b3490cbb139d37afee9f098fee6ca8` |
| `2024` | `https://globalmeteornetwork.org/data/traj_summary_data/yearly/traj_summary_yearly_2024.txt` | `657,058,618` | `705,964` | `360,095` | `261,207` | `46,407` | `460934bbd0e2a0df296165883dc4a54a241969d7613b2b24451ce19b1a1f72d9` |
| `2025` | `https://globalmeteornetwork.org/data/traj_summary_data/yearly/traj_summary_yearly_2025.txt` | `898,581,735` | `966,063` | `466,273` | `333,324` | `74,289` | `37ae522d249fcd40af68071ba7a8acd2f8151212327eeb46c7399384cdeb8cd0` |
| `2026` | `https://globalmeteornetwork.org/data/traj_summary_data/yearly/traj_summary_yearly_2026.txt` | `701,564,849` | `753,204` | `390,921` | `289,650` | `99,568` | `2e0a73dfc02b5e0a04dfd070de5baa3c0d8759de87912e9ae4e3435d3b9f578e` |
| **Total** | **9 Yearly Tables (`2018–2026`)** | **`3,348,056,713`** | **`3,599,504`** | **`1,772,720`** | **`1,263,849`** | **`288,532`** | — |

### 3. Dated Literature Searches (*eMeteorNews*, *WGN*, CBET, and arXiv)

Executed on **`2026-10-20`** and **`2026-11-07`** (see `the-record-we-beat/table_status.md` and `panel/novelty.md`):
- ***eMeteorNews* (`meteornews.net`, ADS `eMetN`, 2018–Nov 2026):** Queried `"Cepheids" OR "Cepheus" AND ("Global Meteor Network" OR "GMN" OR "CAMS") AND ("163" OR "September")` and radiant cone $\alpha_g \in [295^\circ, 315^\circ], \delta_g \in [+54^\circ, +65^\circ]$ at $\lambda_\odot \in [158^\circ, 168^\circ]$ $\to$ `0` matches.
- ***WGN, Journal of the IMO* (`imo.net`, ADS `JIMO`, vols. 46–54, 2018–2026):** Queried `"Cepheus" OR "Draco" OR "Cygnus" AND ("new meteor shower" OR "working list" OR "GMN")` and coordinate cone around $(\alpha_g = 304.8^\circ, \delta_g = +59.8^\circ, \lambda_\odot = 163.3^\circ)$ $\to$ `0` matches.
- **IAU CBET (`5592, 5599, 5603, 5616`) & `new_reports.php` (2023–Nov 2026):** Checked all newly reported showers (`LP = 02646..02650` on 3 November 2026) $\to$ `0` matches ($\min D_{\text{SH}} = 0.2992$).
- **arXiv (`astro-ph.EP`, `astro-ph.IM`) & NASA ADS (2018–Nov 2026):** Queried `abs:("Global Meteor Network" OR "meteor shower" OR "CAMS") AND abs:("Cepheus" OR "streamfulldata" OR "working list")` and author catalogs (`Vida, Jenniskens, Roggemans, Jopek, Neslušan, Hajduková, Kornoš`) $\to$ `0` matches.

---

## Not Claimed

- We do not claim an official IAU Meteor Data Center number or three-letter code; formal assignment of an IAU number and Working List entry requires submission to the IAU MDC and publication in a peer-reviewed journal or *eMeteorNews* / *WGN* / CBET.
- We do not claim a definitive parent comet or asteroid identification for `GMN_NEW_SHOWER_M1_CEPHEUS_MC_163`.
- Other candidate clusters (`M2_Hercules`, `M3_Camelopardalis`), single-night outbursts (`p1`), and working-list recurrences (`p2`) from our initial exploration are not claimed in this package (`kit/SUBMIT.md` §1, one claim per package).
- The `status: CONFIRMED_SOLUTION` label in `panel/gate.md` represents our own local 3-skeptic review panel check (`panel/reproduce.md`, `panel/novelty.md`, `panel/criterion.md`).

---

## Credits

- **Observational Data:** Global Meteor Network (GMN; Vida et al. 2021, *MNRAS* 506, 5046; `https://globalmeteornetwork.org/data/traj_summary_data/yearly/`) and the hundreds of GMN station operators across `AT, BA, BE, BG, CZ, DE, DK, FR, HR, HU, IT, NL, RO, SI, UK` whose cameras recorded the 16 trajectories.
- **Reference Catalog:** IAU Meteor Data Center (`streamfulldata2026.txt`, `roje_lista.php`, `new_reports.php`; Jopek, Hajduková, Rudawska, Kornoš, Neslušan et al., `https://www.ta3.sk/IAUC22DB/MDC2022/`).
- **Discovery, Deduplication & Verification Pipeline:** `@mizopl` (`we*`).
