# The published values and status sources this claim is compared against

## 1. Target `status_source` (`https://www.voynich.nu/transcr.html`)
- **URL**: `https://www.voynich.nu/transcr.html`
- **Fetched by the run (scout step)**: `2026-10-23T18:16:05Z`, HTTP `200`, `60410` bytes, `Last-Modified: Sat, 31 May 2025 00:16:05 GMT`, `sha256: 57f8aaf6b1cdd6a292361b3a94e723f8fb14f0960b2cb349acee142fbadb19a5`.
- **Re-fetched independently by the NOVELTY skeptic**: `2026-10-24T15:15:37Z`, HTTP `200`, `60410` bytes, `sha256: 57f8aaf6b1cdd6a292361b3a94e723f8fb14f0960b2cb349acee142fbadb19a5`.
- **Canonical IVTFF transliterations linked on the page**:
  - `ZL3b-n.txt` (`sha256: bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`)
  - `IT2a-n.txt` (`sha256: 7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`)
  - `RF1b-e.txt` (`sha256: 9ac7a0cd32d0cd63fa316cf6fe870bb9c3a50091da22ab9301e62d3803cb104e`)

## 2. Primary benchmark for partial win `p2` (`https://arxiv.org/abs/2604.19762`)
- **URL**: `https://arxiv.org/abs/2604.19762`
- **Fetched by the run (scout step)**: `2026-10-23T18:18:04Z`, HTTP `200`, `41942` bytes, `Last-Modified: Mon, 24 Aug 2026 19:41:09 GMT`, `sha256: f43d3885b01f235d338191f4fa2053ef6b6e044ba9e246f23a7a571570a66ad3`.
- **Re-fetched independently by the NOVELTY skeptic**: `2026-10-24T15:15:38Z`, HTTP `200`, `41942` bytes, `sha256: f43d3885b01f235d338191f4fa2053ef6b6e044ba9e246f23a7a571570a66ad3`.
- **Official reproduction code**: `https://github.com/labyrinthinesecurity/currier-signatures` (`verifier.py`, `signatures_v27.py`, `grille.py`).

## 3. Extracted comparator table (`object/reference_calibration.json`)

| Generator / Model | Hand-Executable Budget | `A/ZL3b` Joint Pass | `B/ZL3b` Joint Pass | `A/IT2a` Joint Pass | `B/IT2a` Joint Pass | Why Published Baselines Fail |
|---|---|---:|---:|---:|---:|---|
| **Published Slot Generator** (`signatures_v27.py`, `arXiv:2604.19762`) | Parametric slot tables | `10.0%` (`2/20`) | `0.0%` (`0/20`) | `10.0%` (`2/20`) | `0.0%` (`0/20`) | Fails 10-chunk `MI` (`0.1396 < 0.2508` on B; `0.1771 < 0.2910` on A) and `Shape` (`50% Intermediate`) |
| **Published Cardan Grille** (`grille.py`, `arXiv:2604.19762`, `G0/G1/G2/G6`) | 36-cell table + grilles | `0.0%` (`0/20`) | `0.0%` (`0/20`) | `0.0%` (`0/20`) | `0.0%` (`0/20`) | Fails `E->S` directionality (`0.30% - 17.76% < 60.0%`) |
| **Unmodified Naibbe Cipher** (`naibbe.py`, Greshko 2025) | 6 tables (156 entries), 0 state bits | `0.0%` fixed/Zipf (`10.0%` adap) | `0.0%` fixed/Zipf (`100.0%` adap) | `0.0%` fixed/Zipf (`10.0%` adap) | `0.0%` fixed/Zipf (`100.0%` adap) | Fails `E->S` (`52.9% - 53.2% < 60.0%`) and strict `Shape` (`40/40 Intermediate`) |
| **This Claim (`VBCLC-152`, `object/vbclc.py`)** | **152 table entries, 1 state bit** | **`100.0%` (`200/200`)** | **`100.0%` (`200/200`)** | **`100.0%` (`200/200`)** | **`100.0%` (`200/200`)** | Passes all 4 signatures jointly on `200/200` streams per cell across `A/ZL3b`, `B/ZL3b`, `A/IT2a`, `B/IT2a`, `A/RF1b-e`, `B/RF1b-e` |

The pages themselves are not copied into this package.
