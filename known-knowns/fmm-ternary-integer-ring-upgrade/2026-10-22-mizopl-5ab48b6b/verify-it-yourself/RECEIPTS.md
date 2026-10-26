# Verification Receipts (`2026-10-22-mizopl-5ab48b6b`)

## 1. Master Certificate & Object Integrity

- **Master Certificate:** `object/CERTIFICATE.json` (`7,788` bytes, `sha256: 4050811589871e8e0b91e766d8587a39fe00649cce86b6e1fb974e755aae0bcf`)
- **7 Verified Bilinear FMM Schemes (`6` in `ZT = {-1, 0, 1}` + `1` in `Z`):**

| File | Format | Ring | Rank (`m`) | Prev `ZT` | Prev `Z` | Overall `Q` | Delta `ZT` | Delta `Z` | `max_abs` | Complexity | Nonzeros (`U / V / W / Total`) | Brent Equations | Bytes | SHA-256 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `object/6x12x14_m654_ZT.json` | `6x12x14` | `ZT` | **`654`** | `666` | `654` | `645` | **`-12`** | `0` | `1` | `13,241` | `4,149 / 5,477 / 5,007 / 14,633` | `1,016,064` | `114,018` | `5ab48b6b88fd1a7b9fbe8c81670522bd45f290e580be8a4443751e208f2f2bc4` |
| `object/9x10x13_m763_ZT.json` | `9x10x13` | `ZT` | **`763`** | `771` | `763` | `758` | **`-8`** | `0` | `1` | `14,116` | `4,852 / 5,069 / 5,838 / 15,759` | `1,368,900` | `123,209` | `a351d9eef1a62ff9ab7a300e67928a880200e9fcb4ba7f3accffc900e99c1923` |
| `object/9x10x16_m920_ZT.json` | `9x10x16` | `ZT` | **`920`** | `924` | `920` | `916` | **`-4`** | `0` | `1` | `17,397` | `5,856 / 6,056 / 7,469 / 19,381` | `2,073,600` | `153,081` | `42ad6efd9f8b6aab2320058835d85c565300f616d007b57535bf1968c0cb0076` |
| `object/10x15x16_m1484_ZT.json` | `10x15x16` | `ZT` | **`1,484`** | `1,488` | `1,484` | `1,482` | **`-4`** | `0` | `1` | `28,160` | `11,226 / 10,136 / 9,926 / 31,288` | `5,760,000` | `254,512` | `02199a88ebd24b1457c5cae7a5a2dcb895aa396ada9e5daaf0ea1cc4846d09d3` |
| `object/11x15x16_m1629_ZT.json` | `11x15x16` | `ZT` | **`1,629`** | `1,641` | `1,629` | `1,605` | **`-12`** | `0` | `1` | `39,490` | `14,532 / 14,854 / 13,538 / 42,924` | `6,969,600` | `349,814` | `0d2eb6e651f61c7c9fa5d137eb4813f37f287016eaa91e95deae53107016b288` |
| `object/12x13x16_m1546_ZT.json` | `12x13x16` | `ZT` | **`1,546`** | `1,548` | `1,544` | `1,509` | **`-2`** | `+2` | `1` | `64,887` | `18,520 / 25,516 / 24,135 / 68,171` | `6,230,016` | `547,710` | `b639c891628cd5e5042311d19adfa2c29eff95d6c0b1077466c36ce3204e796a` |
| `object/12x13x16_m1541_Z.json` | `12x13x16` | `Z` | **`1,541`** | `1,548` | `1,544` | `1,509` | — | **`-3`** | `2` | `64,983` | `18,608 / 25,480 / 24,169 / 68,257` | `6,230,016` | `548,395` | `911599680fd3bbe0558dbf7fe5e0886deb863c4244915812d28404156660f780` |

## 2. Exact Output of `sh verify-it-yourself/run_checks.sh`

```text
control_positive_strassen_2_2_2: PASS (64/64 equations, mismatches=0)
control_negative_corrupted_brent: PASS (rejected)
control_negative_non_zt_coeff: PASS (rejected)
certificate_sha256=4050811589871e8e0b91e766d8587a39fe00649cce86b6e1fb974e755aae0bcf (PASS)
verified 6x12x14  [ZT] rank= 654 (prev_ZT=666, prev_Z=654, Q=645) max_abs=1 complexity=13241 eqs=1016064 mismatches=0 sha256=5ab48b6b88fd1a7b...
verified 9x10x13  [ZT] rank= 763 (prev_ZT=771, prev_Z=763, Q=758) max_abs=1 complexity=14116 eqs=1368900 mismatches=0 sha256=a351d9eef1a62ff9...
verified 9x10x16  [ZT] rank= 920 (prev_ZT=924, prev_Z=920, Q=916) max_abs=1 complexity=17397 eqs=2073600 mismatches=0 sha256=42ad6efd9f8b6aab...
verified 10x15x16 [ZT] rank=1484 (prev_ZT=1488, prev_Z=1484, Q=1482) max_abs=1 complexity=28160 eqs=5760000 mismatches=0 sha256=02199a88ebd24b14...
verified 11x15x16 [ZT] rank=1629 (prev_ZT=1641, prev_Z=1629, Q=1605) max_abs=1 complexity=39490 eqs=6969600 mismatches=0 sha256=0d2eb6e651f61c7c...
verified 12x13x16 [ZT] rank=1546 (prev_ZT=1548, prev_Z=1544, Q=1509) max_abs=1 complexity=64887 eqs=6230016 mismatches=0 sha256=b639c891628cd5e5...
verified 12x13x16 [Z ] rank=1541 (prev_ZT=1548, prev_Z=1544, Q=1509) max_abs=2 complexity=64983 eqs=6230016 mismatches=0 sha256=911599680fd3bbe0...
VERIFIED: 7/7 schemes (6 ZT + 1 Z), 29648196/29648196 exact integer Brent equations PASS
PASS
```

## 3. Non-Degeneracy & 1-Minimality Receipt

- **Zero rank-1 terms (`all-zero u_q, v_q, or w_q`):** `0` across all 7 schemes.
- **Distinct rank-1 triples `(u_q, v_q, w_q)`:** `654`, `763`, `920`, `1,484`, `1,629`, `1,546`, and `1,541` respectively (`0` duplicate triples).
- **Redundant rank-1 terms:** `0` across all 7 schemes (deleting any single rank-1 term violates the exact integer Brent equations over $\mathbb{Z}$).
