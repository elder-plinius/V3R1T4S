# Primary Status Table Snapshot (`polytof-toffoli-tcount-benchmark-tensors` — `p3` Audit)

## 1. Live Status Source Fetched Before Claiming

- **Table URL:** `https://github.com/ZIB-IOL/polytof/blob/main/docs/tensors.md` (raw: `https://raw.githubusercontent.com/ZIB-IOL/polytof/main/docs/tensors.md`)
- **Upstream Commit (`main`):** `0dcac107d15adc34dc646242d222f21ae7d32699` (committed `2026-10-12`)
- **Fetched UTC:** `2026-10-25T18:37:15Z`
- **HTTP Status:** `200 OK`
- **Byte Size:** `8,777` bytes
- **SHA-256 of `docs/tensors.md`:** `f83839d0589888d75fb0ac357f8e251bc3f743d5c1749757cb51beec26676dc3`

## 2. Discrepancy Rows Identified by the `p3` Audit (`docs/tensors.md` vs `data/paper/` & `data/tensors/`)

| Tensor ID | Circuit Name | Table $n$ | Actual `data/tensors/` $n$ | Table `CP` | Table `Waring` | Posted `data/paper/waring/` File (Rank) | `p3` Audit Finding & Shipped Repair |
|---|---|---:|---:|---:|---:|---|---|
| `0105` | `CSLA MUX_3` | `21` | `21` | `8` | `39` | `0105-00041.npy` (**`41`**, `+2` discrepancy) | **Repaired:** `object/waring/0105-00039.npy` (**`39`**, `-2` vs posted) |
| `0108` | `Ham15 (low)` | `46` | **`42`** | `17` | `73` | `0108-00077.npy` (**`77`**, `+4` discrepancy) | **Repaired + Dim Discrepancy:** `object/waring/0108-00073.npy` (**`73`**, `-4` vs posted; actual $n=42$ vs table $46$) |
| `0115` | `Mod Red_21` | `28` | `28` | `11` | `51` | `0115-00055.npy` (**`55`**, `+4` discrepancy) | **Repaired:** `object/waring/0115-00051.npy` (**`51`**, `-4` vs posted) |
| `0817` | `QCLA Com_7` | `42` | `42` | `12` | `59` | `0817-00063.npy` (**`63`**, `+4` discrepancy) | **Repaired:** `object/waring/0817-00059.npy` (**`59`**, `-4` vs posted) |
| `0728` | `GF(2^5) Mult` | `15` | `15` | `13` | `59` | `0728-00061.npy` (**`61`**, `+2` discrepancy) | **Waring Discrepancy:** `0728-00061.npy` has rank `61` (`0128-00059.npy` has `59`) |
| `0114` | `Mod Mult_55` | `12` | **`11`** | `3` | `17` | `0114-00017.npy` (`17`) | **Dimension Discrepancy:** `0114` has $n=11$ vs table $n=12$ (`0814` has $n=12$) |
