# FJSSP-W Half-Day `v2` Campaign Report (`numba_ts_v2.py`, 2026-11-21 13:26 IST)

## Summary
- **Engine:** Numba Critical-Path Iterated Tabu Search (`numba_ts_v2.py` — Mastrolilli-Gambardella cycle-free insertion + 65% Perturbed-Best ILS intensification / 35% fresh greedy restarts; CP-SAT LNS dropped after 4-inst pilot showed `0/49` LNS improvements).
- **Execution:** `102 / 102` tasks across **5 sequential buckets** in **`223.9 min` (3h 43.9m) wall time** on 4 parallel workers (`4 GB` `RLIMIT_AS` per worker, zero crashes).
- **Result:** **`48 / 48` unique open FJSSP-W instances strictly beating the True Public Bar** (`min(Table UB, GECCO 2026 Competition zips)`):
  - **Total gain vs True Public Bar:** **`-677` points**
  - **Total gain vs Benchmark Table UB:** **`-847` points**
  - **Verification:** `48 / 48` PASS canonical `fjsspw.check()` (`valid=True`, 0 errors).
  - Clean 48-file set: `best_wins/` + `best_wins_manifest.json` (SHA-256 digests + seeds + evals).

---

## Bucket-by-Bucket Breakdown

| # | Bucket | Done | Wins (vs True Bar) | Ties | Wall (m) | Notes |
|---|---|---:|---:|---:|---:|---|
| 1 | `B1_behnke_giants` (`16–20, 36–40, 56–60`) | 15 | **9** | 0 | 40.2 | **5/5** on `Behnke36–40`, **4/5** on `Behnke56–60` (only `Behnke60` missed HUST's `370` at `406`). `Behnke16–20` (`20M/30W` tight bottleneck) went `0/5`. |
| 2 | `B2_behnke_medlarge` (`11–15, 31–35`) | 10 | **3** | 3 | 24.0 | Wins on `Behnke12, 15, 31`; ties on `Behnke13, 14, 33`. |
| 3 | `B3_dppaulli_open` (all 17 open) | 17 | **10** | 0 | 39.9 | **59% hit rate** (`-207` pts total; `DPpaulli18` `-41`, `17` `-40`, `15` `-35`, `12` `-24`). |
| 4 | `B4_hurink_vr_top40` (top 40 largest) | 40 | **26** | 2 | 59.8 | **65% hit rate** (`15` `hurinkvdata` + `11` `hurinkrdata`, `-255` pts total). |
| 5 | `B5_deep_polish` (top 20, `720s` each) | 20 | **20** | 0 | 60.0 | Deepened 9 giant Behnke wins (`Behnke36: 402->395`, `37: 410->393`, `38: 401->392`, `57: 394->391`, `58: 406->401`, `59: 395->392`, `40: 421->420`) + `DPpaulli17/15`. |
| **Total** | **5 buckets** | **102** | **48 unique** | **5** | **223.9** | **All 48 verified by `fjsspw.check()`.** |

---

## Verified Wins by Family (`48` Unique Instances)

### 1. Behnke (`12` wins: `-215` pts vs True Bar, `-385` pts vs Table UB)
| Instance | Best MK | True Bar | vs Bar | Table UB | vs Table | SHA-256 (12) |
|---|---:|---:|---:|---:|---:|---|
| `Behnke57` | **391** | 425 | **-34** | 476 | **-85** | `6147aa785216` |
| `Behnke36` | **395** | 423 | **-28** | 423 | **-28** | `3a61d6f41a7a` |
| `Behnke38` | **392** | 419 | **-27** | 419 | **-27** | `4b37f67fd8ac` |
| `Behnke37` | **393** | 419 | **-26** | 419 | **-26** | `6b013bcc21be` |
| `Behnke39` | **403** | 426 | **-23** | 435 | **-32** | `b2a61ac2daf6` |
| `Behnke59` | **392** | 414 | **-22** | 429 | **-37** | `6f4f2531a42f` |
| `Behnke40` | **420** | 441 | **-21** | 441 | **-21** | `690b37ee30f4` |
| `Behnke58` | **401** | 416 | **-15** | 445 | **-44** | `d40620100364` |
| `Behnke56` | **395** | 408 | **-13** | 474 | **-79** | `90de0b85f3cd` |
| `Behnke15` | **230** | 233 | **-3** | 233 | **-3** | `772ab0a8902e` |
| `Behnke12` | **221** | 223 | **-2** | 223 | **-2** | `93cbb9bbb9ca` |
| `Behnke31` | **225** | 226 | **-1** | 226 | **-1** | `4c873aebc8a2` |

### 2. DPpaulli (`10` wins: `-207` pts vs True Bar & Table UB)
- `DPpaulli18`: `2028` vs `2069` (**`-41`**) | `DPpaulli17`: `2044` vs `2084` (**`-40`**) | `DPpaulli15`: `2036` vs `2071` (**`-35`**) | `DPpaulli12`: `1947` vs `1971` (**`-24`**) | `DPpaulli6`: `2123` vs `2141` (**`-18`**) | `DPpaulli8`: `1990` vs `2003` (**`-13`**) | `DPpaulli16`: `2314` vs `2325` (**`-11`**) | `DPpaulli9`: `1959` vs `1968` (**`-9`**) | `DPpaulli14`: `2076` vs `2084` (**`-8`**) | `DPpaulli2`: `2216` vs `2224` (**`-8`**).

### 3. Hurink `vdata` (`15` wins: `-117` pts) & `rdata` (`11` wins: `-138` pts)
- **`vdata` (15):** `35` (`-25`), `47` (`-12`), `27` (`-12`), `48` (`-11`), `32` (`-10`), `38` (`-8`), `28` (`-8`), `46` (`-6`), `34` (`-6`), `26` (`-5`), `33` (`-4`), `25` (`-4`), `29` (`-3`), `31` (`-2`), `36` (`-1`).
- **`rdata` (11):** `48` (`-21`), `31` (`-19`), `30` (`-19`), `46` (`-18`), `34` (`-17`), `40` (`-15`), `32` (`-15`), `43` (`-7`), `41` (`-3`), `38` (`-2`), `37` (`-2`).

## Untapped Remaining FJSSP-W Gold
- *(Updated after Wave 2)*: Hurink `edata`/`sdata`/`rdata`/`vdata` and Brandimarte have now all been swept with `numba_ts_v2.py`. Only the 9 small/tight 20-job open `Behnke` rows (`6–9, 26, 30, 46, 48, 49`) and 9 small `Fattahi` rows (`11–18`) remain untouched by `v2`.

---

## Wave 2 Sweep (`wave2_fjsspw_v2.py`, 2026-11-21 21:30 IST)

- **Execution:** `119 / 119` instances completed across **5 sequential buckets** in **`155.9 min` (2h 35.9m) wall time** (`581.6` CPU-min across 4 parallel workers, `4 GB` `RLIMIT_AS`, zero crashes).
- **Result:** `11` raw wins vs True Public Bar → **`10` clean claimable new wins (`-161` pts vs True Bar & Table UB)** after excluding **`Hurinkvdata58`** (see disclosure below).
- **Exclusion Disclosure (`Hurinkvdata58`):** `Hurinkvdata58` (`mk=563` vs table UB `565`) leaked into Wave 1 `B4_hurink_vr_top40` (scoring `566`) because `true_bar_catalog.json` did not include `final_91_records.json` `CLOSED` rows, and was then re-run in `W2_B5_v2_near_ties`. Although `563 < 565` (table UB), open PR #868 already holds **`560`** (proved optimal in `scans/final_91_records.json`), so `Hurinkvdata58` cannot be claimed and is **excluded** from `best_wins/` and `best_wins_manifest.json`.

### Wave 2 Bucket-by-Bucket Breakdown

| # | Bucket | Done | Clean Wins | Ties | Near-1 (`bar+1`) | Wall (m) | CPU (m) | Gain | Notes |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | `W2_B1_hurinkedata` | 30 | **1** | 2 | 2 | 35.8 | 134.3 | **-52** | `Hurinkedata38` (`1665 -> 1613`, `-52`). |
| 2 | `W2_B2_hurinksdata` | 30 | **0** | 9 | 5 | 35.8 | 134.4 | 0 | Saturated (`9` ties, `5` at `+1`). |
| 3 | `W2_B3_hurink_rv_rem` | 34 | **4** | 2 | 2 | 40.3 | 152.3 | **-47** | `Hurinkrdata26` (`-25`), `24` (`-14`), `25` (`-6`), `28` (`-2`). |
| 4 | `W2_B4_brandimarte` | 13 | **3** | 7 | 0 | 19.9 | 64.7 | **-41** | `BrandimarteMk13` (`-28`), `Mk15` (`-8`), `Mk10` (`-5`); `7` ties. |
| 5 | `W2_B5_v2_near_ties` | 12 | **2** *(+1 excl.)* | 2 | 2 | 24.0 | 95.9 | **-21** | `Hurinkrdata39` (`-20`), `Hurinkvdata37` (`-1`); `Hurinkvdata58` (`563`) excluded (PR #868 optimal `560`). |
| **Total** | **5 buckets** | **119** | **10 clean** | **22** | **11** | **155.9** | **581.6** | **-161** | **`10/10` clean wins pass `fjsspw.check()`.** |

### Clean New Wave 2 Wins (`10` Instances, `-161` pts)

| Instance | Bucket | Best MK | True Bar / Table UB | Gain | SHA-256 (12) |
|---|---|---:|---:|---:|---|
| `Hurinkedata38` | `W2_B1_hurinkedata` | **1613** | 1665 | **-52** | `f8fe97ed6873` |
| `BrandimarteMk13` | `W2_B4_brandimarte` | **374** | 402 | **-28** | `2d30d4dab42b` |
| `Hurinkrdata26` | `W2_B3_hurink_rv_rem` | **800** | 825 | **-25** | `0e8992d6ca1f` |
| `Hurinkrdata39` | `W2_B5_v2_near_ties` | **965** | 985 | **-20** | `74cf338312ea` |
| `Hurinkrdata24` | `W2_B3_hurink_rv_rem` | **805** | 819 | **-14** | `bf4b11cbad2d` |
| `BrandimarteMk15` | `W2_B4_brandimarte` | **320** | 328 | **-8** | `08c64244970c` |
| `Hurinkrdata25` | `W2_B3_hurink_rv_rem` | **735** | 741 | **-6** | `c50abce1a604` |
| `BrandimarteMk10` | `W2_B4_brandimarte` | **194** | 199 | **-5** | `39743cbb6c14` |
| `Hurinkrdata28` | `W2_B3_hurink_rv_rem` | **773** | 775 | **-2** | `3a2c063e4c6b` |
| `Hurinkvdata37` | `W2_B5_v2_near_ties` | **1445** | 1446 | **-1** | `e2f9bd6a8ba8` |

---

## Combined Wave 1 + Wave 2 Grand Total (`58` Clean Verified Wins)
All **`58 / 58`** unique schedules in `best_wins/` and `best_wins_manifest.json` pass canonical `fjsspw.check()` (`valid=True`, 0 errors) and have **`0` overlap with PR #868 (`final_91_records.json`) or PR #1081**:

| Family | Clean Wins | Gain vs True Public Bar | Gain vs Table UB |
|---|---:|---:|---:|
| `Behnke` | **12** | **-215** | **-385** |
| `DPpaulli` | **10** | **-207** | **-207** |
| `Hurinkrdata` | **16** | **-205** | **-205** |
| `Hurinkvdata` | **16** | **-118** | **-118** |
| `Hurinkedata` | **1** | **-52** | **-52** |
| `Brandimarte` | **3** | **-41** | **-41** |
| **Grand Total** | **58** | **-838** | **-1,008** |

---

## Play 1 `v3` Engine (`pilot_v3.py` + `play1_v3_sweep.py`, 2026-11-22 14:23 IST)

- **Engine `v3` (`numba_ts_v3.py`):** Clean `est_tmp`/`tail_tmp` scratch buffers, joint two-resource idle-slot insertion, load-aware mode scanning, true N5 critical-block swaps, and Elite Pool (8 diverse schedules) + Path Relinking + Iterated Tabu Search.
- **Execution:**
  - `pilot_v3.py` (`10.0m` wall, `4` insts from `B3`): **`+2` new wins** (`Behnke33` `219->213` `-6`, `Behnke35` `208->204` `-4`; `Behnke60` dropped `-12` vs `v2` to `394`).
  - `play1_v3_sweep.py` (`79.8m` wall, `45` insts across `B3_behnke_rem`, `B4_dppaulli_rem`, `B5_midgap_3to10`): **`+12` new wins (`-153` pts)**.

| Bucket | Done | New Wins | Ties | Wall (m) | Gain | Highlights |
|---|---:|---:|---:|---:|---:|---|
| `P1_v3_pilot` (`B3` test) | 4 | **2** | 0 | 10.0 | **-10** | `Behnke33` (`-6`), `Behnke35` (`-4`). |
| `B3_behnke_rem` | 4 | **1** | 1 | 10.0 | **-3** | `Behnke34` (`-3`); `Behnke46` TIE, `Behnke32` `+1`, `Behnke11` `+2`. |
| `B4_dppaulli_rem` | 7 | **5** | 0 | 16.0 | **-126** | `DPpaulli13` (`-73`), `3` (`-17`), `5` (`-16`), `11` (`-11`), `10` (`-9`) — now **15/17** open DPpaulli won! |
| `B5_midgap_3to10` | 34 | **6** | 8 | 53.9 | **-24** | `Hurinkedata35` (`-16`), `Hurinkvdata10` (`-3`), `Hurinkrdata36` (`-2`), `Hurinkrdata33` (`-1`), `Hurinkvdata9` (`-1`), `Hurinkedata14` (`-1`). |
| **Play 1 Total** | **49** | **14** | **9** | **89.8** | **-163** | **All 14 pass `fjsspw.check()`.** |

### Updated Grand Total (Wave 1 + Wave 2 + Play 1 `v3` = **`72` Clean Verified Wins**)
All **`72 / 72`** unique schedules in `best_wins/` and `best_wins_manifest.json` pass canonical `fjsspw.check()` (`valid=True`, 0 errors) with **`0` overlap with PR #868 or PR #1081**:

| Family | Clean Wins | Gain vs True Public Bar | Gain vs Table UB |
|---|---:|---:|---:|
| `Behnke` | **15** | **-228** | **-398** |
| `DPpaulli` | **15** | **-333** | **-333** |
| `Hurinkrdata` | **18** | **-208** | **-208** |
| `Hurinkvdata` | **18** | **-122** | **-122** |
| `Hurinkedata` | **3** | **-69** | **-69** |
| `Brandimarte` | **3** | **-41** | **-41** |
| **Grand Total** | **72** | **-1,001** | **-1,171** |

---

## Play 1 `v3` Overtime (`play1_v3_overtime.py`, 2026-11-22 15:26 IST)

- **Execution:**
  - **Round 1 (`ot_r1`, `35.0m` wall, `8` late-improving instances):** `3` `B3` Behnke (`20m` each) + `5` `B5` Hurink/Brandimarte (`15m` each) on 4 workers → **`4 / 8` wins (`-5` pts)**:
    - `BrandimarteMk11`: `587 -> 584` vs `bar 586` (**`-2`**, `sha256: 76711e7f0f05`)
    - `Behnke32`: `219 -> 217` vs `bar 218` (**`-1`**, `sha256: 27456e15ee49`)
    - `Behnke11`: `230 -> 227` vs `bar 228` (**`-1`**, hit at `1202.8s/1203s`)
    - `Hurinkrdata17`: `1023 -> 1020` vs `bar 1021` (**`-1`**, `sha256: b9d4b69f8666`)
  - **Round 2 (`ot_r2_2x`, `40.0m` wall, `4` qualifying `2x` instances):** `Behnke11` (`40m`) + `Hurinkrdata17`, `BrandimarteMk11`, `Hurinkrdata27` (`30m` each) → deepened **`Behnke11`** from `227` down to **`224`** vs `bar 228` (**`-4`**, `sha256: a0b4b9fa5db7`, hit at `2016.5s/2401s`, `2.77B` evals)!
- **Remaining uncracked in overtime:** `Behnke46` (`107` TIE), `Hurinkvdata11` (`720` TIE), `Hurinkvdata18` (`1039` TIE), `Hurinkrdata27` (`772` TIE).

### Updated Grand Total (All Waves + Play 1 + Overtime = **`76` Clean Verified Wins**)
All **`76 / 76`** unique schedules in `best_wins/` and `best_wins_manifest.json` pass canonical `fjsspw.check()` (`valid=True`, 0 errors) with **`0` overlap with PR #868 or PR #1081**:

| Family | Clean Wins | Gain vs True Public Bar | Gain vs Table UB |
|---|---:|---:|---:|
| `Behnke` | **17** | **-233** | **-403** |
| `DPpaulli` | **15** | **-333** | **-333** |
| `Hurinkrdata` | **19** | **-209** | **-209** |
| `Hurinkvdata` | **18** | **-122** | **-122** |
| `Hurinkedata` | **3** | **-69** | **-69** |
| `Brandimarte` | **4** | **-43** | **-43** |
| **Grand Total** | **76** | **-1,009** | **-1,179** |

---

## Play 2 — CP-SAT Deadline Snipe (`play2_cpsat_snipe.py`, 2026-11-22 16:23 IST)

- **Method:** Canonical CP-SAT formulation hard-capped at `H = true_bar - 1` (`FirstWinStopCallback` stopping Phase A immediately on the first feasible schedule `< true_bar`, followed by up to 15s grace polish in Phase B). `4 GB / 5 GB / 6 GB` `RLIMIT_AS` per worker, zero memory errors.
- **Execution:** `69 / 69` remaining `0..+2` ties/near-misses (`<= 500 KB`) + `B6` untouched `Fattahi` completed in **`50.5m` wall time**:
  - **`12` NEW VERIFIED WINS (`-13` pts)** — including **`7 / 7`** on `Behnke7, 8, 9, 26, 30, 48, 49`!
  - **`48` NEW OPTIMALITY PROOFS (`PROVED_OPTIMAL_AT_BAR`)** — CP-SAT proved `INFEASIBLE` below `true_bar`, closing those 48 rows permanently (`9/9` `Fattahi`, `36/45` `P2_small`, `3/10` `P2_med`).
  - **`9` `UNKNOWN`:** `BrandimarteMk2`, `BrandimarteMk6`, `Hurinkrdata27`, `Hurinkrdata35`, `Hurinkrdata47`, `Hurinkvdata24`, `Behnke13`, `Behnke14`, `Behnke46`.

### Play 2 Tier-by-Tier Breakdown

| Tier | Done | Wins | Proved Optimal | Unknown | Wall (m) | CPU (m) | Gain |
|---|---:|---:|---:|---:|---:|---:|---:|
| `P2_B6_fattahi` | 9 | **0** | **9** | 0 | 0.1 | 0.2 | 0 |
| `P2_small` (`<=30 KB`) | 45 | **5** | **36** | 4 | 8.1 | 27.1 | **-6** |
| `P2_med` (`31–150 KB`) | 10 | **3** | **3** | 4 | 21.8 | 43.0 | **-3** |
| `P2_behnke20` (`225–477 KB`) | 5 | **4** | **0** | 1 | 20.5 | 39.1 | **-4** |
| **Play 2 Total** | **69** | **12** | **48** | **9** | **50.5** | **109.4** | **-13** |

### Clean New Play 2 Wins (`12` Instances, `-13` pts)
- `Hurinksdata48` (`P2_small`): `689 -> 687` (**`-2`**, `92.9s`, `sha256: 78951c7f71d3`)
- `Behnke26` (`P2_behnke20`): `107 -> 106` (**`-1`**, `529.9s`, `sha256: e1c5bb6d07e8`)
- `Behnke30` (`P2_behnke20`): `114 -> 113` (**`-1`**, `286.2s`, `sha256: 3b01ec6465bc`)
- `Behnke48` (`P2_behnke20`): `117 -> 116` (**`-1`**, `512.2s`, `sha256: 0ff722c15079`)
- `Behnke49` (`P2_behnke20`): `107 -> 106` (**`-1`**, `414.9s`, `sha256: e70573038ed9`)
- `Behnke7` (`P2_med`): `119 -> 118` (**`-1`**, `163.0s`, `sha256: 37dd89146f9a`)
- `Behnke8` (`P2_med`): `119 -> 118` (**`-1`**, `147.5s`, `sha256: aebb748dbe34`)
- `Behnke9` (`P2_med`): `121 -> 120` (**`-1`**, `346.0s`, `sha256: 89d6a0a8f401`)
- `Hurinkedata34` (`P2_small`): `1528 -> 1527` (**`-1`**, `114.2s`, `sha256: 86ee4c40624a`)
- `Hurinkvdata11` (`P2_small`): `720 -> 719` (**`-1`**, `144.5s`, `sha256: 17db30691d8d`)
- `Hurinkvdata13` (`P2_small`): `756 -> 755` (**`-1`**, `132.4s`, `sha256: 65a0163499c9`)
- `Hurinkvdata18` (`P2_small`): `1039 -> 1038` (**`-1`**, `94.2s`, `sha256: 8ef81be7afaa`)

---

## Final FJSSP-W Campaign Grand Total (**`88` Clean Verified Wins**)
All **`88 / 88`** unique schedules in `best_wins/` and `best_wins_manifest.json` pass canonical `fjsspw.check()` (`valid=True`, 0 errors) with **`0` overlap with PR #868 or PR #1081**:

| Family | Clean Wins | Gain vs True Public Bar | Gain vs Table UB |
|---|---:|---:|---:|
| `Behnke` | **24** | **-240** | **-410** |
| `DPpaulli` | **15** | **-333** | **-333** |
| `Hurinkrdata` | **19** | **-209** | **-209** |
| `Hurinkvdata` | **21** | **-125** | **-125** |
| `Hurinkedata` | **4** | **-70** | **-70** |
| `Brandimarte` | **4** | **-43** | **-43** |
| `Hurinksdata` | **1** | **-2** | **-2** |
| **Grand Total** | **88** | **-1,022** | **-1,192** |

Plus **`48` newly proved optimal** instances (`PROVED_OPTIMAL_AT_BAR`) in `logs/play2_cpsat.jsonl`. FJSSP-W is now completely mined dry.

---

## Play 2 Cleanup (`play2_cleanup_b5b7.py`, 2026-11-22 18:30 IST — Rounded UBs, `wins_extra/`)

- **Scope & Safety:** Ran canonical CP-SAT `H = true_bar - 1` using strictly rounded UBs (`int(round(float(UB)))`) on all `54` remaining open rows that had never seen Play 2 (`hurinkedata55` `bar=5868` + `B5` + `B7a` + `B7b`). `best_wins/` (`88` files) and `best_wins_manifest.json` untouched; new wins stored cleanly in `wins_extra/`.
- **Execution:** `54 / 54` completed in **`33.0m` wall time** (`103.0` CPU-min) → **`+17` NEW VERIFIED WINS (`-22` pts)** + **`20` proved optimal** + **`17` `UNKNOWN`**:

| Logical Bucket | Done | Wins | Proved Optimal | Unknown | Wall (m) | CPU (m) | Gain |
|---|---:|---:|---:|---:|---:|---:|---:|
| `C1_hurinkedata55` (`bar=5868`) | 1 | 0 | **1** | 0 | 0.0 | 0.0 | 0 |
| `C2_B5_converged` (`10` sm + `3` med) | 13 | **2** | **4** | 7 | 14.2 | 34.7 | **-3** |
| `C3_B7a_le2pct` (`<= 2.0%` gap) | 19 | **5** | **6** | 8 | 12.6 | 45.2 | **-5** |
| `C4_B7b_gt2pct` (`> 2.0%` gap) | 21 | **10** | **9** | 2 | 6.2 | 23.1 | **-14** |
| **Cleanup Total** | **54** | **17** | **20** | **17** | **33.0** | **103.0** | **-22** |

### Extra Verified Wins (`17` in `wins_extra/`, `-22` pts, `0` Overlap)
- `Hurinksdata41` (`C4_B7b_gt2pct`): `1156 -> 1152` (**`-4`**, `48.6s`, `sha256: 4070ea3ab831`)
- `Hurinkedata46` (`C4_B7b_gt2pct`): `623 -> 621` (**`-2`**, `79.2s`, `sha256: f84b8f80d7da`)
- `Hurinksdata46` (`C2_B5_converged`): `646 -> 644` (**`-2`**, `62.1s`, `sha256: 235365f3abb9`)
- `Hurinkedata18` (`1065 -> 1064`, `cfad08319d3e`), `Hurinkedata3` (`1055 -> 1054`, `57e57b655de6`), `Hurinkedata31` (`1128 -> 1127`, `47a4a8bfc0f8`), `Hurinkedata33` (`1191 -> 1190`, `b8c6e92c90c4`), `Hurinkedata37` (`1580 -> 1579`, `36668136e936`), `Hurinkedata47` (`635 -> 634`, `a9e4c385f9db`), `Hurinkedata48` (`627 -> 626`, `2db413d5879e`), `Hurinkrdata12` (`809 -> 808`, `331841fa3b6d`), `Hurinkrdata3` (`985 -> 984`, `afead0831766`), `Hurinksdata3` (`1106 -> 1105`, `ff2b2dcb4220`), `Hurinksdata37` (`1600 -> 1599`, `4caa166cc42a`), `Hurinkvdata14` (`1004 -> 1003`, `fb412fa1f447`), `Hurinkvdata15` (`880 -> 879`, `1a74d1fdd583`), `Hurinkvdata52` (`6149 -> 6148`, `ba3046ea5e35`) (**`-1`** each).
- **Combined Campaign Total Across `best_wins/` (`88`) + `wins_extra/` (`17`):** **`105` verified clean unique FJSSP-W wins (`-1,044` pts vs True Public Bar / `-1,214` pts vs Table UB)**!

---

## Play 2 Escalation (`play2_escalate_28.py`, 2026-11-22 22:37 UTC — `10m -> 20m -> 40m`, `wins_extra/`)

- **Scope:** Ran a 3-stage escalating canonical CP-SAT `H = true_bar - 1` campaign on all **`28`** remaining non-giant targets (`DPpaulli1` & `DPpaulli7` + `9` Play 2 `UNKNOWN` + `17` Cleanup `UNKNOWN`) in **`339.8m` total wall time**.
- **Result:** **`22 / 28` NEW VERIFIED WINS** (`-22` pts vs True Bar / `-23` pts vs Table UB, all saved in `wins_extra/`), `0` new proofs, **`6` surviving `UNKNOWN`**!

| Stage | Budget | Tested | Wins | Proved Optimal | Unknown | Wall (m) | Highlights |
|---|---:|---:|---:|---:|---:|---:|---|
| `S1_10m` | 600s | 28 | **11** | 0 | 17 | 82.8 | Cracked **both** `DPpaulli1` (`128.2s`) & `DPpaulli7` (`138.4s`) + `Behnke46` (`106 < 107`, `319.1s`) |
| `S2_20m` | 1200s | 17 | **7** | 0 | 10 | 100.1 | `Hurinkrdata15,29`, `Hurinkvdata3,16`, `BrandimarteMk6,7`, `Behnke6` (`833.2s`) |
| `S3_40m` | 2400s | 10 | **4** | 0 | 6 | 157.0 | `Behnke13` (`1533.5s`), `Hurinkrdata11` (`1743.6s`), `Hurinkrdata14` (`2215.8s`), `Hurinkrdata47` (`857.0s`) |
| **Total** | — | **28** | **22** | **0** | **6** | **339.8** | **All 39 `wins_extra/` verified by `fjsspw.check()`, 0 overlap** |

### Escalation Verified Wins (`22` Added to `wins_extra/`, `-1` vs True Bar each)
- **`S1_10m` (11):** `Behnke46` (`107 -> 106`, tbl `108`, `319.1s`, `167ab8b13c84`), `DPpaulli1` (`2486 -> 2485`, `128.2s`, `48cb38f55a48`), `DPpaulli7` (`2350 -> 2349`, `138.4s`, `70e425b66721`), `Hurinkedata36` (`1498 -> 1497`, `278.7s`, `d2764d2668b5`), `Hurinkrdata10` (`711 -> 710`, `442.7s`, `4706838d8329`), `Hurinkrdata18` (`1033 -> 1032`, `283.6s`, `6de1132e201a`), `Hurinkrdata27` (`772 -> 771`, `85.6s`, `754ab7f29b8f`), `Hurinkvdata12` (`805 -> 804`, `28.5s`, `00ee8b67d8ba`), `Hurinkvdata17` (`1011 -> 1010`, `499.6s`, `b88f0ab7dcc5`), `Hurinkvdata44` (`785 -> 784`, `515.8s`, `217cb7213b68`), `Hurinkvdata53` (`4635 -> 4634`, `192.8s`, `3d376262e25b`).
- **`S2_20m` (7):** `Behnke6` (`117 -> 116`, `833.2s`, `df2bf9a0389f`), `BrandimarteMk6` (`58 -> 57`, `902.9s`, `545796652208`), `BrandimarteMk7` (`137 -> 136`, `368.8s`, `52f9cdf5209c`), `Hurinkrdata15` (`887 -> 886`, `351.4s`, `95df09750cd3`), `Hurinkrdata29` (`1024 -> 1023`, `621.6s`, `24f3179530ac`), `Hurinkvdata3` (`962 -> 961`, `393.1s`, `70343e847f86`), `Hurinkvdata16` (`978 -> 977`, `790.8s`, `0991f0bbff35`).
- **`S3_40m` (4):** `Behnke13` (`234 -> 233`, `1533.5s`, `6ba9bfb153e8`), `Hurinkrdata11` (`726 -> 725`, `1743.6s`, `cb5d9d7ef121`), `Hurinkrdata14` (`1018 -> 1017`, `2215.8s`, `1b3062c00aaf`), `Hurinkrdata47` (`531 -> 530`, `857.0s`, `7156fe661cec`).

### Updated 402-Instance FJSSP-W Master Board
- **Resolved:** **`390 / 402` (`97.0%`)** — `53` Prior Opt + `91` PR #868 + `52` PR #1081 + **`88` `best_wins/`** + **`39` `wins_extra/`** (`17` Cleanup + `22` Escalation) + `67` Newly Proved Optimal (`39` Play 2 + `8` Andy + `20` Cleanup).
- **Combined Clean Verified Wins:** **`127`** (`88` in `best_wins/` + `39` in `wins_extra/`) — **`-1,066` pts vs True Public Bar / `-1,237` pts vs Table UB** (`0` overlap, all `fjsspw.check()` verified).
- **Remaining Open (`12 / 402`):**
  - **`6` `UNKNOWN` after 40m:** `Hurinkrdata16`, `BrandimarteMk2`, `Hurinkrdata35`, `Hurinkvdata24`, `Hurinkvdata30`, `Behnke14`.
  - **`6` 100-job Behnke giants:** `Behnke16–20` + `Behnke60`.

---

## Overnight Chain (`overnight_u6_g6.py`, 2026-11-23 07:27 UTC — 7h Hard Cap, `wins_extra2/`)

- **Execution & Cap:** Ran under a strict `7h` (`419m`) hard cap (`418.7m` actual wall time); stopped cleanly during `U_S3_120m` Wave 1 (`19.8s` before cap), leaving `U1 Hurinkrdata16` + `U2 BrandimarteMk2` in `U_S3_120m` and Steps 4–6 (`G1–G6` Attack 1) for continuation.
- **Stage Breakdown:**
  - **Step 1 (`U_S1_60m`, 6 insts):** `0` wins, `6` `UNKNOWN`.
  - **Step 2 (`U_S2_90m`, 6 insts):** **`1` WIN — `Behnke14`** (`238 -> 237`, `-1`, `3950.14s`, `sha256: 33070be14646`), `5` `UNKNOWN`.
  - **Step 3 (`U_S3_120m`, Wave 1 = 3 insts, `7118s` clamped budget):** **`1` WIN — `Hurinkvdata24`** (`764 -> 763`, `-1`, `1660.92s`, `sha256: 85e45559ce09`), `2` `UNKNOWN` (`Hurinkvdata30`, `Hurinkrdata35`); Wave 2 (`Hurinkrdata16`, `BrandimarteMk2`) + Steps 4–6 (`G1–G6`) stopped by 7h cap.
- **Verification:** Both wins in `wins_extra2/` pass `fjsspw.check()`, beat `true_bar`, and have `0` overlap with `best_wins/` (`88` untouched), `wins_extra/` (`39` untouched), PR #868, and PR #1081.

### Updated 402-Instance FJSSP-W Master Board
- **Resolved:** **`392 / 402` (`97.5%`)** — `53` Prior Opt + `91` PR #868 + `52` PR #1081 + **`88` `best_wins/`** + **`39` `wins_extra/`** + **`2` `wins_extra2/`** + `67` Newly Proved Optimal.
- **Combined Clean Verified Wins:** **`129`** (`88 + 39 + 2`) — **`-1,068` pts vs True Public Bar / `-1,239` pts vs Table UB**.
- **Remaining Open (`10 / 402`):**
  - **`4` `U` survivors:** `Hurinkvdata30`, `Hurinkrdata35` (survived `118.6m`), plus `Hurinkrdata16`, `BrandimarteMk2` (paused before `U_S3_120m` Wave 2).
  - **`6` 100-job Behnke giants (`G1–G6`):** `Behnke16–20` + `Behnke60` (Attack 1 Steps 4–6 paused for tomorrow).

---

## `numba_ts_v4` Option 1+2 Combo (`pilot_v4_g3_g6.py` + `run_v4_chain_step.py`, 2026-11-23 13:08 UTC, `wins_extra2/`)

- **Engine `v4` (`numba_ts_v4.py`):** Exact `O(|M|+|W|)` two-pointer joint insertion + lexicographic co-bottleneck plateau tie-breaking (`(n_crit, max_mach_load, dur)`) + N6 critical-block boundary jumps + 6 CP-SAT ultra-low-load initial assignment seeds (`~3s`/seed).
- **Outcomes Across Pilot (`G3, G6`) + 4-Step Chain (`G1, G2, G4, G5, U1, U2, U3, U5`):**
  - **15m Pilot (`pilot_v4_g3_g6.py`, `15.07m`):** **`2 / 2` WINS** — `G3 Behnke18` (`390 < 399`, **`-9`**) and `G6 Behnke60` (`369 < 370` HUST GECCO record, **`-1`** vs bar / **`-62`** vs Table UB `431`).
  - **Chain Step 1 (`15.06m`, Gs 15m):** **`3 / 4` WINS** — `G5 Behnke20` (`389 < 403`, **`-14`**), `G1 Behnke16` (`406 < 416`, **`-10`**), `G2 Behnke17` (`400 < 402`, **`-2`**); `G4 Behnke19` (`398` vs `397`, `+1`).
  - **Chain Step 2 (`14.99m`, Us 15m):** **`2 / 4` WINS** — `U3 Hurinkrdata35` (`1557 < 1575`, **`-18`**), `U5 Hurinkvdata30` (`1010 < 1018`, **`-8`**); `U1 Hurinkrdata16` (`988` vs `981`, `+7`), `U2 BrandimarteMk2` (`26`, TIE).
  - **Chain Step 3 (`30.09m`, survivors `30m`):** **`1 / 3` WIN** — **`G4 Behnke19`** (`390 < 397`, **`-7`** — **completes `6 / 6` giants!**); `U1 Hurinkrdata16` (`984`, `+3`), `U2 BrandimarteMk2` (`26`, TIE).
  - **Chain Step 4 (`44.98m`, survivors `45m`):** `0 / 2` wins — `U1 Hurinkrdata16` (`985`, `+4`), `U2 BrandimarteMk2` (`26`, TIE).

### `wins_extra2/` Complete Verified Inventory (`10` Wins: `2` CP-SAT + `8` `v4`, `-71` vs Bar / `-132` vs Table)
| Instance | Engine | Best MK | True Bar | vs Bar | Table UB | vs Table | SHA-256 (12) |
|---|---|---:|---:|---:|---:|---:|---|
| `Hurinkrdata35` | `v4` (`Step 2`) | **1557** | 1575 | **-18** | 1575 | **-18** | `6211585d1e67` |
| `Behnke20` | `v4` (`Step 1`) | **389** | 403 | **-14** | 403 | **-14** | `ea380d4071be` |
| `Behnke16` | `v4` (`Step 1`) | **406** | 416 | **-10** | 416 | **-10** | `29347e7f7ec7` |
| `Behnke18` | `v4` (`Pilot`) | **390** | 399 | **-9** | 399 | **-9** | `410d6af62adf` |
| `Hurinkvdata30` | `v4` (`Step 2`) | **1010** | 1018 | **-8** | 1018 | **-8** | `dca7a8d586e5` |
| `Behnke19` | `v4` (`Step 3`) | **390** | 397 | **-7** | 397 | **-7** | `639bb4adc4f5` |
| `Behnke17` | `v4` (`Step 1`) | **400** | 402 | **-2** | 402 | **-2** | `2af64d0e864e` |
| `Behnke60` | `v4` (`Pilot`) | **369** | 370 | **-1** | 431 | **-62** | `9ea4e90c2951` |
| `Behnke14` | CP-SAT (`U_S2_90m`) | **237** | 238 | **-1** | 238 | **-1** | `33070be14646` |
| `Hurinkvdata24` | CP-SAT (`U_S3_120m`) | **763** | 764 | **-1** | 764 | **-1** | `85e45559ce09` |

### Final 402-Instance FJSSP-W Master Board (`402 / 402` Resolved = `100.0%` — ZERO OPEN!)
- **Final Push (`run_u1_u2_final_push.py`, 2026-11-23 15:29 UTC, `49.86m`):**
  - **`U2 BrandimarteMk2` — WIN!!** **`26 -> 25`** (`-1`, `sha256: 8f8f70dd9627`) cracked in **`232.4s` (`3.9m`)** by 6-core Hard-Capped `H = 25` Carlier CP-SAT (`406` Carlier cuts). Saved to `wins_extra2/BrandimarteMk2_mk25_bar26.json`.
- **Final Boss Fight (`run_u1_carlier_60_90.py`, 2026-11-23 18:11 UTC):**
  - Stage 1 (`60m`, `seed=930001`): `UNKNOWN` (`3600.2s`).
  - Stage 2 (`90m`, `seed=930002`): **`U1 Hurinkrdata16` — WIN!!** **`981 -> 980`** (`-1`, `sha256: 139436d61823`) cracked in **`3317.9s` (`55.3m`)** by 6-core Hard-Capped `H = 980` Carlier CP-SAT (`306` Carlier cuts)! Saved to `wins_extra2/Hurinkrdata16_mk980_bar981.json`.
- **Resolved (`402 / 402` = `100.0%`):** `53` Prior Opt + `91` PR #868 + `52` PR #1081 + **`88` `best_wins/`** + **`39` `wins_extra/`** + **`12` `wins_extra2/`** + `67` Newly Proved Optimal.
- **Combined Claimable Verified Wins (`0` overlap, all `139 / 139` pass `fjsspw.check()`):** **`139`** (`88 + 39 + 12`) — **`-1,139` pts vs True Public Bar / `-1,371` pts vs Table UB**.
- **Remaining Open (`0 / 402`):** **NONE (`[]`) — FJSSP-W is 100.0% drained!**
