# Primary Status Table Snapshot (`polytof-toffoli-tcount-benchmark-tensors`)

## 1. Live Status Source Fetched Before Claiming

- **Table URL:** `https://github.com/ZIB-IOL/polytof/blob/main/docs/tensors.md` (raw: `https://raw.githubusercontent.com/ZIB-IOL/polytof/main/docs/tensors.md`)
- **Upstream Commit (`main`):** `0dcac107d15adc34dc646242d222f21ae7d32699` (committed `2026-10-12`)
- **Fetched UTC:** `2026-10-25T18:37:15Z`
- **HTTP Status:** `200 OK`
- **Byte Size:** `8,777` bytes
- **SHA-256 of `docs/tensors.md`:** `f83839d0589888d75fb0ac357f8e251bc3f743d5c1749757cb51beec26676dc3`

## 2. Extracted Benchmark Rows Compared Against (`docs/tensors.md` & `data/paper/`)

| Tensor ID | Circuit Name | Table $n$ | Posted $n$ | Table `CP` | Table `Waring` | Posted `data/paper/waring/` File (Rank) | Our Result (`p2` / `p3` / Sub-Table Waring) |
|---|---|---:|---:|---:|---:|---|---|
| `0112` / `0812` | `Mod 5_4` | 5 | 5 | 1 | 7 | `0112-00007.npy` (7), `0812-00007.npy` (7) | **`p2` Certified Optimal:** `CP = 1` ($\text{nnz}=1>0$) & `Waring = 7` (`0/126` subsets $\le 6$) |
| `0101` / `0801` | `Barenco Tof_3` | 8 | 8 | 2 | 13 | `0101-00013.npy` (13), `0801-00013.npy` (13) | **`p2` Certified Optimal:** `CP = 2` ($\text{rank}_{\mathbb{F}_2}(F_1(T)) = 6 > 3$) |
| `0120` / `0820` | `Tof_3` | 7 | 7 | 2 | 13 | `0120-00013.npy` (13), `0820-00013.npy` (13) | **`p2` Certified Optimal:** `CP = 2` ($\text{rank}_{\mathbb{F}_2}(F_1(T)) = 6 > 3$) |
| `0134` | `Relative Tof_3` | 8 | 8 | 2 | 11 | `0134-00011.npy` (11) | **`p2` Certified Optimal:** `CP = 2` ($\text{rank}_{\mathbb{F}_2}(F_1(T)) = 6 > 3$) |
| `0725` | `GF(2^2) Mult` | 6 | 6 | 3 | 17 | `0725-00017.npy` (17) | **`p2` Certified Optimal:** `CP = 3` (`0/36` rank-1 bilinear pairs span $\{z_0, z_1\}$) |
| `0105` | `CSLA MUX_3` | 21 | 21 | 8 | 39 | `0105-00041.npy` (**41**, `+2` discrepancy) | **`p3` Audit & Repaired:** `0105-00039.npy` (**39**, `-2` vs posted) |
| `0108` | `Ham15 (low)` | 46 | **42** | 17 | 73 | `0108-00077.npy` (**77**, `+4` discrepancy) | **`p3` Audit & Repaired:** `0108-00073.npy` (**73**, `-4` vs posted, $n=42$ vs $46$) |
| `0115` | `Mod Red_21` | 28 | 28 | 11 | 51 | `0115-00055.npy` (**55**, `+4` discrepancy) | **`p3` Audit & Repaired:** `0115-00051.npy` (**51**, `-4` vs posted) |
| `0817` | `QCLA Com_7` | 42 | 42 | 12 | 59 | `0817-00063.npy` (**63**, `+4` discrepancy) | **`p3` Audit & Repaired:** `0817-00059.npy` (**59**, `-4` vs posted) |
| `0728` | `GF(2^5) Mult` | 15 | 15 | 13 | 59 | `0728-00061.npy` (**61**, `+2` discrepancy) | **`p3` Audit:** `0728-00061.npy` has rank `61` (`0128-00059.npy` has `59`) |
| `0114` | `Mod Mult_55` | 12 | **11** | 3 | 17 | `0114-00017.npy` (17) | **`p3` Audit:** `0114` has $n=11$ vs table $n=12$ (`0814` has $n=12$) |
| `0732` | `GF(2^9) Mult` | 27 | 27 | 30 | **147** | `0732-00147.npy` (**147**) | **Sub-Table Waring:** `0732-00139.npy` (**139**, `-8` in `0.17 s` CPU; also `141`, `143`) |
| `0733` | `GF(2^10) Mult` | 30 | 30 | 33 | **173** | `0733-00173.npy` (**173**) | **Sub-Table Waring:** `0733-00161.npy` (**161**, `-12` in `1.42 s` CPU) |
