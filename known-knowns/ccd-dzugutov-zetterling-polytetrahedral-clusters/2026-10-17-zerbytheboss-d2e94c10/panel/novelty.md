# Panel Skeptic Audit: NOVELTY (`ccd-dzugutov-zetterling-polytetrahedral-clusters`)

- `role`: novelty
- `context`: subagent (fresh invocation)
- `target_id`: `ccd-dzugutov-zetterling-polytetrahedral-clusters`
- `audited_utc`: `2026-10-18T05:10:18Z`

## 1. Single Honest HTTP Fetch of Primary Sources (No Retries)

Using Python `urllib.request.urlopen` (single request per URL, zero retries) at `2026-10-18T05:10:18Z`:

1. **Cambridge Cluster Database — Dzugutov Index & Table (`https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/Dzugutov.html` / `Dzugutov.html`)**:
   - **Index URL**: `https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/Dzugutov.html` (HTTP `200`, `2267` bytes, `Last-Modified: Mon, 23 Feb 2026 08:30:18 GMT`, SHA-256 `80789f7bb6b5b54307f9bb53a025ec3c54430fcb30bdcd272cfba8921b7367ad`)
   - **Dzugutov Table URL (`N = 3..100`)**: `https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/Dzugutov/table.html` (J. P. K. Doye, D. J. Wales, and S. I. Simdyankin, *Faraday Discuss.* 118, 159-170, 2001; `https://arxiv.org/abs/cond-mat/0011018`, HTTP `200`, `19928` bytes, `Last-Modified: Thu, 25 Jul 2024 14:43:48 GMT`, SHA-256 `3749780be2e35aeca9dffd0e80fcb1098b6494662984612d818d329da5467678`)
   - **Potential Specification URL**: `https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/Dzugutov/potential.html` (HTTP `200`, `3534` bytes, `Last-Modified: Thu, 25 Jul 2024 14:43:49 GMT`, SHA-256 `f352ca8b31c571a7b2a7663903f356e4f50de8e26ca4f9209a2a15bdd52b341e`)
   - **Fetched UTC**: `2026-10-18T05:10:18Z`

2. **Cambridge Cluster Database — Modified-Dzugutov Table (`https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/mDzugutov/table.html` / `mDzugutov.html`)**:
   - **URL**: `https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/mDzugutov/table.html` (J. P. K. Doye and D. J. Wales, *Physical Review Letters* 86, 5719-5722, 2001)
   - **HTTP Status**: `200` (`43166` bytes, `Last-Modified: Thu, 25 Jul 2024 14:43:56 GMT`, SHA-256 `68d9e0face9713fba7cb3cf45d447a0c26ea5a6e9a3c72436419dbcb3ac82c2f`)
   - **Fetched UTC**: `2026-10-18T05:10:18Z`
   - **Quoted Live Table Values (4 Target Sizes)**:
     - `mDzugutov_74` (`N = 74`): `-180.982763` (polished posted point file: `-180.9827625507`)
     - `mDzugutov_134` (`N = 134`): `-343.386067` (polished posted point file: `-343.3860669382`)
     - `mDzugutov_177` (`N = 177`): `-462.579581` (polished posted point file: `-462.5795807885`)
     - `mDzugutov_241` (`N = 241`): `-641.793084` (polished posted point file: `-641.7930841365`)

3. **Cambridge Cluster Database — Zetterling-Dzugutov `Z1` and `Z2` Index & Table (`https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/Zetterling.html` / `Zetterling.html`)**:
   - **Index URL**: `https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/Zetterling.html` (HTTP `200`, `1798` bytes, `Last-Modified: Mon, 23 Feb 2026 08:34:15 GMT`, SHA-256 `2c16436e8ecc1e3d06ea5e1f5464613c9b37fa208fa4dbb20cbc97dc7c6b6004`)
   - **Table URL (`Z1` and `Z2`, `N = 3..80`)**: `https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/Zetterling/table.html` (J. P. K. Doye, D. J. Wales, F. H. M. Zetterling, and M. Dzugutov, *Journal of Chemical Physics* 118, 2792-2799, 2003; HTTP `200`, `24072` bytes, `Last-Modified: Thu, 25 Jul 2024 14:43:39 GMT`, SHA-256 `b1e48112d2f69d7158c07626e181861159b65376febd8943e65bb77147e6f64f`)
   - **Fetched UTC**: `2026-10-18T05:10:18Z`
   - **Quoted Live Table Values (`10` `Z1` and `6` `Z2` Target Sizes)**:
     - `Z1_38` (`N = 38`): `-99.874893` (polished posted point file: `-99.8748926730`)
     - `Z1_42` (`N = 42`): `-111.113917` (polished posted point file: `-111.1139167919`)
     - `Z1_44` (`N = 44`): `-116.579062` (polished posted point file: `-116.5790623474`)
     - `Z1_54` (`N = 54`): `-146.333923` (polished posted point file: `-146.3339233530`)
     - `Z1_65` (`N = 65`): `-176.220446` (polished posted point file: `-176.2204455807`)
     - `Z1_67` (`N = 67`): `-182.418355` (polished posted point file: `-182.4183551831`)
     - `Z1_68` (`N = 68`): `-185.275450` (polished posted point file: `-185.2754498575`)
     - `Z1_74` (`N = 74`): `-202.558045` (polished posted point file: `-202.5580451897`)
     - `Z1_75` (`N = 75`): `-205.448065` (polished posted point file: `-205.4480651688`)
     - `Z1_76` (`N = 76`): `-208.375341` (polished posted point file: `-208.3753408216`)
     - `Z2_35` (`N = 35`): `-92.270480` (polished posted point file: `-92.2704795533`)
     - `Z2_43` (`N = 43`): `-113.534760` (polished posted point file: `-113.5347599666`)
     - `Z2_56` (`N = 56`): `-148.936593` (polished posted point file: `-148.9365930045`)
     - `Z2_59` (`N = 59`): `-157.230650` (polished posted point file: `-157.2306502954`)
     - `Z2_69` (`N = 69`): `-184.286813` (polished posted point file: `-184.2868137269`)
     - `Z2_80` (`N = 80`): `-213.815040` (polished posted point file: `-213.8150397720`)

## 2. Literature, Trophy Case, and Pull Request Audit

1. **Last 24 Months of Literature (2024-2026)**:
   - Searched 2024-2026 literature and citations of Doye, Wales, and Simdyankin (2001), Doye and Wales (2001), and Doye, Wales, Zetterling, and Dzugutov (*J. Chem. Phys.* 118, 2792, 2003).
   - No publication in the last 24 months (or any prior work) reports energies below the live Cambridge Cluster Database tables for any of the 20 claimed cluster sizes (`mDzugutov` `N = 74, 134, 177, 241`; `Z1` `N = 38, 42, 44, 54, 65, 67, 68, 74, 75, 76`; `Z2` `N = 35, 43, 56, 59, 69, 80`).

2. **Repository `TROPHY_CASE.md`**:
   - Inspected `TROPHY_CASE.md`: confirmed zero existing entries for `ccd-dzugutov-zetterling-polytetrahedral-clusters`.

3. **Open and Merged Pull Requests on `elder-plinius/V3R1T4S`**:
   - Queried `https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100` across pages 1 to 3 (300 total open/closed/merged PRs).
   - Confirmed `0` open, closed, or merged pull requests targeting `ccd-dzugutov-zetterling-polytetrahedral-clusters`.

## 3. Strict Improvement Verification Across All 20 Claimed Structures

- **Artifact**: `object/dzugutov_zetterling_20_records_and_502_audit.json` (SHA-256 `3797a33831b0b1ff9bfd5e14964e32ec0ce2d2b39b5f5f42d7909f59a5900b96`, verified via `verify-it-yourself/run_checks.sh`).
- **All 20 Claimed Minima Strictly Beat Live CCD Table Values and Polished Posted Point Files by at least `1e-4` (up to `-0.411479`)**:
  1. **`mDzugutov_74` (`N = 74`)**: `E* = -180.9875532166` vs CCD `-180.982763` (polished: `-180.9827625507`), change **`-0.004790`** (`47.9x` the `1e-4` threshold).
  2. **`mDzugutov_134` (`N = 134`, `p1`)**: `E* = -343.3900404390` vs CCD `-343.386067` (polished: `-343.3860669382`), change **`-0.003973`** (`39.7x` the `1e-4` threshold).
  3. **`mDzugutov_177` (`N = 177`, `p1`)**: `E* = -462.5826604786` vs CCD `-462.579581` (polished: `-462.5795807885`), change **`-0.003079`** (`30.8x` the `1e-4` threshold).
  4. **`mDzugutov_241` (`N = 241`, `p1`)**: `E* = -641.7941625208` vs CCD `-641.793084` (polished: `-641.7930841365`), change **`-0.001079`** (`10.8x` the `1e-4` threshold).
  5. **`Z1_38` (`N = 38`)**: `E* = -100.1301837463` vs CCD `-99.874893` (polished: `-99.8748926730`), change **`-0.255291`**.
  6. **`Z1_42` (`N = 42`)**: `E* = -111.1739767527` vs CCD `-111.113917` (polished: `-111.1139167919`), change **`-0.060060`**.
  7. **`Z1_44` (`N = 44`)**: `E* = -116.8727164354` vs CCD `-116.579062` (polished: `-116.5790623474`), change **`-0.293654`**.
  8. **`Z1_54` (`N = 54`)**: `E* = -146.3500928888` vs CCD `-146.333923` (polished: `-146.3339233530`), change **`-0.016170`**.
  9. **`Z1_65` (`N = 65`)**: `E* = -176.4054458998` vs CCD `-176.220446` (polished: `-176.2204455807`), change **`-0.185000`**.
  10. **`Z1_67` (`N = 67`)**: `E* = -182.6367678185` vs CCD `-182.418355` (polished: `-182.4183551831`), change **`-0.218413`**.
  11. **`Z1_68` (`N = 68`)**: `E* = -185.3634223842` vs CCD `-185.275450` (polished: `-185.2754498575`), change **`-0.087972`**.
  12. **`Z1_74` (`N = 74`)**: `E* = -202.8773603525` vs CCD `-202.558045` (polished: `-202.5580451897`), change **`-0.319315`**.
  13. **`Z1_75` (`N = 75`)**: `E* = -205.8062213765` vs CCD `-205.448065` (polished: `-205.4480651688`), change **`-0.358156`**.
  14. **`Z1_76` (`N = 76`)**: `E* = -208.6187854827` vs CCD `-208.375341` (polished: `-208.3753408216`), change **`-0.243444`**.
  15. **`Z2_35` (`N = 35`)**: `E* = -92.2845205483` vs CCD `-92.270480` (polished: `-92.2704795533`), change **`-0.014041`**.
  16. **`Z2_43` (`N = 43`)**: `E* = -113.9462385534` vs CCD `-113.534760` (polished: `-113.5347599666`), change **`-0.411479`** (`4114x` the `1e-4` threshold).
  17. **`Z2_56` (`N = 56`)**: `E* = -149.2304029120` vs CCD `-148.936593` (polished: `-148.9365930045`), change **`-0.293810`**.
  18. **`Z2_59` (`N = 59`)**: `E* = -157.2398070630` vs CCD `-157.230650` (polished: `-157.2306502954`), change **`-0.009157`**.
  19. **`Z2_69` (`N = 69`)**: `E* = -184.6267084482` vs CCD `-184.286813` (polished: `-184.2868137269`), change **`-0.339895`**.
  20. **`Z2_80` (`N = 80`)**: `E* = -214.1928466438` vs CCD `-213.815040` (polished: `-213.8150397720`), change **`-0.377807`**.
- **Complete 502-File Calibration & Discrepancy Audit (`p2`)**: All 502 posted point files across `Dzugutov` (`98`), `mDzugutov` (`248`), `Z1` (`78`), and `Z2` (`78`) are calibrated and audited inside `object/dzugutov_zetterling_20_records_and_502_audit.json`, documenting both the 10x Table I parameter typo (`b = 4.2e6` vs printed `4.2e7` for `Z2` in *J. Chem. Phys.* 118, 2792, 2003) and the 5 corrupted central-atom coordinate tokens (`Z1_13`, `Z1_25`, `Z1_33`, `Z1_37`, `Z2_25`).

pass: true
