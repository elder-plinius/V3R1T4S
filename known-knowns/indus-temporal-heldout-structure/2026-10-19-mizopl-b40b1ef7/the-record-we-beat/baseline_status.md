# Baseline Status Snapshot (`indus-temporal-heldout-structure`)

## 1. Primary Upstream Repository Status (`joyboseroy/indus_decipher` & `paragorth/Indus-`)

- **Fetched URL 1 (`joyboseroy/indus_decipher` commits)**: `https://api.github.com/repos/joyboseroy/indus_decipher/commits?per_page=5`
- **Fetched UTC**: `2026-10-19T20:27:50Z`
- **HTTP Status**: `HTTP/2 200`
- **Selected Headers**: `content-type: application/json; charset=utf-8`, `x-ratelimit-remaining: 59`
- **Response Size**: `21,810` bytes
- **Response SHA-256**: `8dddd5d5682f942f45fc1ebd17f4b98bc19fb2fb1cec68be70abc62ee0b329d9`
- **Latest Commit**: `1f925b85ca8fa138b874252546f435a333b14df6` (`2026-02-23T17:16:33Z`)

- **Fetched URL 2 (`paragorth/Indus-` commits)**: `https://api.github.com/repos/paragorth/Indus-/commits?per_page=5`
- **Fetched UTC**: `2026-10-19T20:31:59Z`
- **HTTP Status**: `HTTP/2 200`
- **Response Size**: `20,448` bytes
- **Response SHA-256**: `05284f6051d7165cc143897edf89cca47e42794b74ccec782130eb5b3ea038af`
- **Latest Commit**: `d62ec82d58642038640da25a97177d7a1fddc9d9` (`2026-10-07T13:59:19Z`, branch `claude/indus-script-dictionary-u3dzf8`), providing:
  - `data/im77/im77_corpus_lines.csv` (`559,170` bytes, `sha256: 385b82bd6a9629e0ab215af46db84ca0c9ec4f6044a2a2ea58a3c64121f26211`)
  - `data/derived/bridge_extended.json` (`2,070` bytes, `sha256: ba0949e1e2dd8e9b5d6d3aea70da5ad3c1d213e76a8bbd38d993814068d7541c`)
  - `data/derived/merged-corpus-canonical.v2.json` (`2,315,998` bytes, `sha256: b68c950bee1b7ded02267c0717b5e7e5d8730b7f72de6f46d4dea086ac9e7a5f`)
  - `data/derived/dark/loop24_pairs.json` (`1,919,320` bytes, `sha256: 638027b53fdffc4b915cb61aa683326cd1c312b5018eac65c9c8b11e1f2efed2`)
  - `data/derived/identity-directory.json` (`82,012` bytes, `sha256: fd5d42b65ec96ff248bbce3ffee4352bab452ff5faa8e4e4084c87a76932c03f`)

- **Fetched URL 3 (V3R1T4S `TROPHY_CASE.md`)**: `https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md`
- **Fetched UTC**: `2026-10-19T20:28:09Z`
- **HTTP Status**: `HTTP/2 200`
- **Response Size**: `31,235` bytes
- **Response SHA-256**: `b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1`
- **Status in `TROPHY_CASE.md`**: `0` entries for `indus-temporal-heldout-structure` or `undeciphered-scripts`.

## 2. Extracted Baseline Cell Values Compared Against (`10,000` Resamples / Permutations, `seed = 0`)

| Benchmark / Stratum (`M77 <= 1977` Frozen -> Post-1977 Held-Out) | `M77-CLSS` (Ours) | `KN3-Left` ($p_{\text{boot}}$) | `KN3-Bidir` ($p_{\text{boot}}$) | `KN3-BlanketF` ($p_{\text{boot}}$) | `SIGIL` Null ($p_{\text{boot}}$) |
|---|---:|---:|---:|---:|---:|
| **Top-25 Frozen `M77` Telescoping Pairs (`p3`)** | **`30` shared frames** | — | — | — | `7.6427` mean, `max = 23` (**`0.0001`**) |
| **Pooled Post-1977 Mode 1 (`n = 3,731` tokens)** | `0.200482` (`748`) | `0.147146` (`549`, **`0.0001`**) | `0.188957` (`705`, **`0.0001`**) | `0.194586` (`726`, `0.0048`) | `0.093809` (`350`, **`0.0001`**) |
| **Mohenjo-daro Post-1977 Mode 1 (`n = 1,041` tokens)** | `0.209414` (`218`) | `0.154659` (`161`, **`0.0001`**) | `0.195005` (`203`, `0.0019`) | `0.206532` (`215`, `0.2988`) | `0.098943` (`103`, **`0.0001`**) |
| **Harappa Post-1977 Mode 1 (`n = 1,593` tokens)** | `0.212806` (`339`) | `0.155053` (`247`, **`0.0001`**) | `0.202134` (`322`, `0.0147`) | `0.205901` (`328`, `0.0188`) | `0.101067` (`161`, **`0.0001`**) |
| **Dholavira Post-1990 Mode 1 (`n = 414` tokens)** | `0.161836` (`67`) | `0.115942` (`48`, **`0.0001`**) | `0.154589` (`64`, `0.2452`) | `0.157005` (`65`, `0.3696`) | `0.072464` (`30`, **`0.0001`**) |
| **Cohort B Strict CISI 3.1/3.2 Range (`n = 2,031` tokens)** | `0.192024` (`390`) | `0.143279` (`291`, **`0.0001`**) | `0.182176` (`370`, `0.0055`) | `0.187100` (`380`, `0.0680`) | `0.092565` (`188`, **`0.0001`**) |
| **Pooled Post-1977 Mode 2 CC Bridge (`n = 3,731` tokens)** | `0.226749` (`846`) | `0.160547` (`599`, **`0.0001`**) | `0.216028` (`806`, **`0.0005`**) | `0.219512` (`819`, `0.0012`) | `0.090592` (`338`, **`0.0001`**) |
| **Mohenjo-daro Post-1977 Mode 2 (`n = 1,041` tokens)** | `0.254563` (`265`) | `0.176753` (`184`, **`0.0001`**) | `0.240154` (`250`, `0.0081`) | `0.242075` (`252`, `0.0081`) | `0.094140` (`98`, **`0.0001`**) |
| **Harappa Post-1977 Mode 2 (`n = 1,593` tokens)** | `0.232894` (`371`) | `0.164470` (`262`, **`0.0001`**) | `0.221594` (`353`, `0.0196`) | `0.229127` (`365`, `0.1561`) | `0.099184` (`158`, **`0.0001`**) |
| **400 Independent `SIGIL` Controls (`null_test.md`)** | `0.200482` | — | — | — | `best_control = 0.096221` (`yes`) |
