# Baseline Status Snapshot (`indus-temporal-heldout-structure`)

## 1. Primary Upstream Repository Status (`joyboseroy/indus_decipher` & `Indus-`)

- **Fetched URL 1 (`joyboseroy/indus_decipher` commits)**: `https://api.github.com/repos/joyboseroy/indus_decipher/commits?per_page=5`
- **Fetched UTC**: `2026-10-19T20:27:50Z`
- **HTTP Status**: `HTTP/2 200`
- **Selected Headers**: `content-type: application/json; charset=utf-8`, `x-ratelimit-remaining: 59`
- **Response Size**: `21,810` bytes
- **Response SHA-256**: `8dddd5d5682f942f45fc1ebd17f4b98bc19fb2fb1cec68be70abc62ee0b329d9`
- **Latest Commit**: `1f925b85ca8fa138b874252546f435a333b14df6` (`2026-02-23T17:16:33Z`)

- **Fetched URL 2 (V3R1T4S `TROPHY_CASE.md`)**: `https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md`
- **Fetched UTC**: `2026-10-19T20:28:09Z`
- **HTTP Status**: `HTTP/2 200`
- **Response Size**: `31,235` bytes
- **Response SHA-256**: `b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1`
- **Status in `TROPHY_CASE.md`**: `0` entries for `indus-temporal-heldout-structure` or `undeciphered-scripts`.

## 2. Extracted Baseline Cell Values Compared Against

| Benchmark / Stratum (`M77 <= 1977` Frozen -> Post-1977 Held-Out) | Baseline Method | Baseline Value | Our Frozen `M77-CLSS` Value | Paired Bootstrap / Permutation $p$ |
|---|---|---:|---:|---:|
| **Pooled Post-1977 Mode 1 (`n = 3,731` tokens)** | `KN3-Left` (`ngram.py`) / `SIGIL` (`adversarial_null_model.py`) | `0.147146` (`549/3,731`) / `0.093809` (`350/3,731`) | **`0.200482` (`748/3,731`)** | **`0.000100 < 0.001`** (`0/10,000`) |
| **Mohenjo-daro Post-1977 Mode 1 (`n = 1,041` tokens)** | `KN3-Left` / `SIGIL` | `0.154659` (`161/1,041`) / `0.098943` (`103/1,041`) | **`0.209414` (`218/1,041`)** | **`0.000100 < 0.001`** (`0/10,000`) |
| **Harappa Post-1977 Mode 1 (`n = 1,593` tokens)** | `KN3-Left` / `SIGIL` | `0.155053` (`247/1,593`) / `0.101067` (`161/1,593`) | **`0.212806` (`339/1,593`)** | **`0.000100 < 0.001`** (`0/10,000`) |
| **Dholavira Post-1990 Mode 1 (`n = 414` tokens)** | `KN3-Left` / `SIGIL` | `0.115942` (`48/414`) / `0.072464` (`30/414`) | **`0.161836` (`67/414`)** | **`0.000100 < 0.001`** (`0/10,000`) |
| **Cohort B Strict CISI 3.1/3.2 Range (`n = 2,031` tokens, `p1`)** | `KN3-Left` / `SIGIL` | `0.143279` (`291/2,031`) / `0.092565` (`188/2,031`) | **`0.192024` (`390/2,031`)** | **`0.000100 < 0.001`** (`0/10,000`) |
| **Pooled Post-1977 Mode 2 CC Bridge (`n = 3,731` tokens)** | `KN3-Left` / `SIGIL` | `0.160547` (`599/3,731`) / `0.090592` (`338/3,731`) | **`0.226749` (`846/3,731`)** | **`0.000100 < 0.001`** (`0/10,000`) |
| **Top-25 Frozen `M77` Telescoping Pairs (`p3`)** | Frequency-Matched Random Permutation (`10,000` perms) | `7.6427` mean (`max = 23`) shared frames | **`30` shared parallel frames** | **`0.000100 < 0.001`** (`0/10,000`) |
| **400 Independent `SIGIL` Controls (`null_test.md`)** | Best of `400` `SIGIL` Controls (`seed = 1..400`) | `0.096221` (`median = 0.088984`) | **`0.200482`** | **`real_beats_all_controls: yes`** |
