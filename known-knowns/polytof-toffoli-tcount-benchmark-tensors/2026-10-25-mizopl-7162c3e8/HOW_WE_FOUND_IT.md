# How We Found It (`contributor text, unverified`)

*Note: contributor text, unverified.*

## 1. Complete `p3` Re-Verification Audit of `ZIB-IOL/polytof` (`data/paper/`)

We built a standalone, bitpacked $\mathbb{F}_2$ verification pipeline (`verify-it-yourself/verify.py`) to audit every decomposition and basis-change matrix in `ZIB-IOL/polytof` (`commit 0dcac107d15adc34dc646242d222f21ae7d32699`) against `docs/tensors.md` (`sha256: f83839d0589888d75fb0ac357f8e251bc3f743d5c1749757cb51beec26676dc3`) and `data/tensors/*.npy`:

1. **Full Pool & Base Coverage (`185` Decomposition Files, `13,537` CP Schemes + `88` Waring Schemes):**
   - Upstream's `scripts/verify_paper_schemes.py` checks only `row = data[0]` of each `data/paper/cpd/topp/*.npy` file, skipping the `13,440` additional schemes stored in rows `1..` of the `14` multi-row pool files (`13 x 1,000 + 454 = 13,454` pool schemes, `13,528` total `cpd/topp` schemes), and does not read `data/paper/cpd/base/*.npy` (`9` bilinear $\mathrm{GF}(2^k)$ multiplication files `0525`..`0533`).
   - By packing 64 CP schemes at a time into `uint64` bitwise words, `verify-it-yourself/verify.py` verifies all `13,528` `cpd/topp` schemes, all `9` `cpd/base` schemes, and all `88` `waring` schemes (under the full linear, quadratic, and cubic phase-polynomial signature in both BCO and original bases) in `~4.3` seconds single-thread CPU time on a 16 GB M1 laptop.
2. **Discrepancies Uncovered (`5` Waring Rank Discrepancies & `2` Qubit-Dimension Discrepancies):**
   - While all `97 / 97` CP files (`88` `cpd/topp` + `9` `cpd/base`) match the `CP` column of `docs/tensors.md`, **5 posted Waring files in `data/paper/waring/` have strictly higher row counts than the `Waring` value claimed in `docs/tensors.md`** despite their variant prefix (`01`, `07`, or `08`) being listed in the `data/paper/` column:
     - `0105` (`CSLA MUX_3`): `0105-00041.npy` has rank `41` vs table `39` (`+2`),
     - `0108` (`Ham15 (low)`): `0108-00077.npy` has rank `77` vs table `73` (`+4`),
     - `0115` (`Mod Red_21`): `0115-00055.npy` has rank `55` vs table `51` (`+4`),
     - `0728` (`GF(2^5) Mult`): `0728-00061.npy` has rank `61` vs table `59` (`+2`; `0128-00059.npy` achieves `59`),
     - `0817` (`QCLA Com_7`): `0817-00063.npy` has rank `63` vs table `59` (`+4`).
   - In addition, **2 `01xx` tensors have different qubit counts $n$ from the shared `Circuit Benchmarks` table row**:
     - `0108` (`Ham15 (low)`): actual $n = 42$ in `data/tensors/0108.npy` vs table $n = 46$ (`0808` has $n = 46$),
     - `0114` (`Mod Mult_55`): actual $n = 11$ in `data/tensors/0114.npy` vs table $n = 12$ (`0814` has $n = 12$).

## 2. Repairing the Four Circuit Waring Schemes (`how-we-built-it/hunt_all_benchmarks.py`)

Using our open-source **`we*` (`we-star`)** framework (`https://github.com/mizopl/we-star`, **Law `M7`: Interface Gauge Freedom & Solution-Fiber Scan**), `how-we-built-it/hunt_all_benchmarks.py` generated diverse minimal-rank Stage-1 CP pools via $\mathrm{GL}(3, \mathbb{F}_2)$ factor gauges and symmetric flip-graph walks and ran Stage-2 `FastTODD` across the fiber, recovering explicit full-signature Waring decompositions matching `docs/tensors.md` for all four circuit variants:
- `object/waring/0105-00039.npy` (`41 -> 39`),
- `object/waring/0108-00073.npy` (`77 -> 73`),
- `object/waring/0115-00051.npy` (`55 -> 51`), and
- `object/waring/0817-00059.npy` (`63 -> 59`).
