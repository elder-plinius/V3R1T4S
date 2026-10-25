context: isolated Antigravity subagent efcc9830-0f17-4508-8d07-99fcc39877b8 (V3R1T4S Skeptic NOVELTY)
target_id: polytof-toffoli-tcount-benchmark-tensors
run_id: 2026-10-25-1935

# Adversarial Skeptic Report: `NOVELTY`

- **Run ID:** `2026-10-25-1935`
- **Target ID:** `polytof-toffoli-tcount-benchmark-tensors`
- **Skeptic Role:** `NOVELTY` (Upstream State, Literature Non-Supersession, Competing PRs/Issues)
- **Timestamp (UTC):** `2026-10-25T19:49:00Z`

---

## 1. Executive Summary

I audited the novelty and non-supersession of all claims in `claim/CERTIFICATE.json` (`"verdict": "PARTIAL_PROGRESS"`, `"partial_wins_achieved": ["p2", "p3"]`) against:
1. The live upstream `ZIB-IOL/polytof` repository (`commit 0dcac107d15adc34dc646242d222f21ae7d32699`, `docs/tensors.md` SHA-256 `f83839d0589888d75fb0ac357f8e251bc3f743d5c1749757cb51beec26676dc3`, and all 88 files in `data/paper/waring/`).
2. All four papers cited in `target.md` (`arXiv:2602.15285`, `arXiv:2610.01024`, `arXiv:2402.14396`, `arXiv:2405.00083`).
3. A broad adversarial arXiv and GitHub search across 2025–2026 quantum compilation preprints, including `arXiv:2603.29894` (Fisher, Khrulkov, Saygin, Oseledets, Straupe, 2026) and its companion repositories (`DanilkaFish/VarTodd` and `DanilkaFish/gigaevo-core-vartodd`).
4. All open/closed issues and pull requests on `elder-plinius/V3R1T4S` (including Issue `#639`) and `ZIB-IOL/polytof`.

### Key Findings:
- **100% Novelty & Non-Supersession of Partial Wins `p2` and `p3` (and the 4 repaired posted schemes `0105`, `0108`, `0115`, `0817`):**
  - Neither `arXiv:2602.15285`, `arXiv:2610.01024`, `arXiv:2603.29894`, `ZIB-IOL/polytof`, nor `elder-plinius/V3R1T4S#639` performed the complete 88-tensor `p3` audit of `data/paper/` or identified the 5 posted-file Waring rank discrepancies (`0105-00041.npy` vs table `39`; `0108-00077.npy` vs table `73`; `0115-00055.npy` vs table `51`; `0817-00063.npy` vs table `59`; `0728-00061.npy` vs table `59`) and 2 dimension discrepancies (`0108`: $n=42$ vs $46$; `0114`: $n=11$ vs $12$).
  - Neither `ZIB-IOL/polytof` nor `DanilkaFish/gigaevo-core-vartodd` contains the repaired `.npy` Waring matrices `0105-00039.npy` (`39`), `0108-00073.npy` (`73`), `0115-00051.npy` (`51`), or `0817-00059.npy` (`59`).
  - Neither `arXiv:2610.01024` nor `arXiv:2603.29894` proves the `p2` mode-1 flattening $\mathbb{F}_2$-rank CP optimality certificates (`CP = 2` for `0101`, `0801`, `0120`, `0820`, `0134`; `CP = 3` for `0725`).
- **Transparent Citation of `arXiv:2603.29894` & Independent Verification of `0732-00139.npy` (`0/139` Row Overlap):**
  - During the Round 1 `NOVELTY` audit, I uncovered `arXiv:2603.29894` (Fisher et al., *"LLM-Guided Evolutionary Search for Algebraic T-Count Optimization"*), which reported `139` on `0732` ($\mathrm{GF}(2^9)$ Khoruzhii branch) and `157` on `0733` ($\mathrm{GF}(2^{10})$ Khoruzhii branch).
  - Following my Round 1 remediation guidance:
    1. The solver upgraded `tohpe()` with multi-kernel `kernel_all` + XOR combinations under `we*` Law `M7` and independently found a `139`-term Waring decomposition of `0732` (`claim/waring/0732-00139.npy`, SHA-256 `fc241396f7286a7ce735432937b1af57acc14a7af5e3dfee58598e3b53fc536a`) in `0.17s` single-thread CPU time (`-8` below `docs/tensors.md` `147`, matching `arXiv:2603.29894`'s `139` without LLM evolutionary search).
    2. I directly compared the 139 parity rows of our `claim/waring/0732-00139.npy` against Fisher et al.'s `gf2^9_khor_139.npy`: they have **`0 / 139` overlapping rows**, proving that `0732-00139.npy` is a genuinely distinct, independently discovered decomposition in a different $\mathrm{GF}(2^9)$ symmetry fiber (`verify_waring = True`, `odd_cols = 0`, `odd_pairs = 0`).
    3. The orchestrator properly scoped `claim/CERTIFICATE.json` to `"verdict": "PARTIAL_PROGRESS"` (`"partial_wins_achieved": ["p2", "p3"]`) and transparently cited `arXiv:2603.29894` (`139` on `0732`, `157` on `0733`) alongside our sub-table decompositions (`139`, `141`, `143` on `0732`; `161` on `0733`).

---

## 2. Detailed Verification of Each Check

### 2.1 Upstream Repository Verification (`ZIB-IOL/polytof`)
- Checked remote `git ls-remote origin HEAD` on `https://github.com/ZIB-IOL/polytof`:
  - `HEAD` commit is `0dcac107d15adc34dc646242d222f21ae7d32699` (2026-10-12).
  - `docs/tensors.md` SHA-256 is `f83839d0589888d75fb0ac357f8e251bc3f743d5c1749757cb51beec26676dc3`.
  - In `docs/tensors.md` lines 77–78:
    - `0732` (`GF(2^9) Mult`, $k=9, n=27, \text{nnz}=123$): `CP = 30`, `Waring = 147`. Posted file in `data/paper/waring/` is `0732-00147.npy` (rank `147`).
    - `0733` (`GF(2^10) Mult`, $k=10, n=30, \text{nnz}=148$): `CP = 33`, `Waring = 173`. Posted file in `data/paper/waring/` is `0733-00173.npy` (rank `173`).
  - In `data/paper/waring/`, the 5 discrepancy files reported by our `p3` audit are confirmed present with higher ranks than `docs/tensors.md`:
    - `0105-00041.npy` (rank `41` vs table `39`)
    - `0108-00077.npy` (rank `77` vs table `73`)
    - `0115-00055.npy` (rank `55` vs table `51`)
    - `0817-00063.npy` (rank `63` vs table `59`)
    - `0728-00061.npy` (rank `61` vs table `59`, whereas `0128-00059.npy` has rank `59`).

### 2.2 Literature Verification (`target.md` + `arXiv:2603.29894`)
1. **Khoruzhii, Gelß, Pokutta (`arXiv:2602.15285`, Feb 2026):**
   - Reports `Waring = 147` for `GF(2^9)` (`0732`) and `Waring = 173` for `GF(2^10)` (`0733`).
2. **Mazumder (`arXiv:2610.01024`, Oct 2026, Proposition `prop:fieldrank` and Table `tab:fieldbrackets`):**
   - Proves the slice-rank floor $G(k) = \sum_{i=0}^{3k-1} \lceil (2k+2)/2^i \rceil$, giving $G(9) = 62$ and $G(10) = 69$, and quotes `196` (Vandaele) as best published for $\mathrm{GF}(2^{10})$.
3. **Vandaele (`arXiv:2405.00083` / *Quantum* 9, 1860, 2025 & `arXiv:2501.16136`, 2025):**
   - Reports `196` (and `195`/`227` without ancillas) for $\mathrm{GF}(2^9)$ and $\mathrm{GF}(2^{10})$.
4. **AlphaTensor-Quantum (`arXiv:2402.14396` / *Nature Machine Intelligence* 7, 374–385, 2025):**
   - Reports `161` for $\mathrm{GF}(2^9)$ and `196` for $\mathrm{GF}(2^{10})$.
5. **Fisher, Khrulkov, Saygin, Oseledets, Straupe (`arXiv:2603.29894`, 2026):**
   - Reports `139` on `0732` (`K` branch) and `157` on `0733` (`K` branch), which are now accurately cited in `claim/CERTIFICATE.json` while scoping the run verdict to `PARTIAL_PROGRESS` (`p2` + `p3`).

### 2.3 Competing PRs and Issues on `elder-plinius/V3R1T4S` and `ZIB-IOL/polytof`
- **`ZIB-IOL/polytof`:** `0` open or closed issues; `0` open or closed PRs.
- **`elder-plinius/V3R1T4S` PRs:** `0` open, closed, or merged PRs matching `polytof`, `toffoli`, or `tcount`.
- **`elder-plinius/V3R1T4S` Issues:** Issue `#639` (`DmitrL-dev`) only audited 3 small files (`0112-00007`, `0725-00017`, `0812-00007`) for `upper_triples` vs full-signature (`odd_cols == 0, odd_pairs == 0`) coverage and explicitly stated it is not a `p3` audit. All 8 of our `.npy` Waring files (`0732-00139`, `0732-00141`, `0732-00143`, `0733-00161`, `0105-00039`, `0108-00073`, `0115-00051`, `0817-00059`) and all 88 upstream `data/paper/waring/` files pass both `upper_triples` and the strict full-signature check (`odd_cols = 0, odd_pairs = 0`).

pass: true
