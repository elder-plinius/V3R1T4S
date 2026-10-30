context: isolated Antigravity subagent efcc9830-0f17-4508-8d07-99fcc39877b8 (V3R1T4S Skeptic NOVELTY)
target_id: polytof-toffoli-tcount-benchmark-tensors
run_id: 2026-10-25-1935

# Adversarial Skeptic Report: `NOVELTY`

- **Run ID:** `2026-10-25-1935`
- **Target ID:** `polytof-toffoli-tcount-benchmark-tensors`
- **Skeptic Role:** `NOVELTY` (Upstream State, Literature Non-Supersession, Competing PRs/Issues)
- **Timestamp (UTC):** `2026-10-25T19:49:00Z` (Updated `2026-10-30` for `p3`-only package split `2026-10-25-mizopl-7162c3e8`)

---

## 1. Executive Summary

I audited the novelty and non-supersession of `object/p3_audit_certificate.json` (`partial_win: p3`) and the 4 repaired Waring schemes (`object/waring/0105-00039.npy`, `object/waring/0108-00073.npy`, `object/waring/0115-00051.npy`, `object/waring/0817-00059.npy`) against:
1. The live upstream `ZIB-IOL/polytof` repository (`commit 0dcac107d15adc34dc646242d222f21ae7d32699`, `docs/tensors.md` SHA-256 `f83839d0589888d75fb0ac357f8e251bc3f743d5c1749757cb51beec26676dc3`, and all `185` decomposition files in `data/paper/`).
2. All papers cited in `target.md` (`arXiv:2602.15285`, `arXiv:2610.01024`, `arXiv:2402.14396`, `arXiv:2405.00083`) and 2026 compilation preprints (`arXiv:2603.29894`).
3. All open/closed issues and pull requests on `elder-plinius/V3R1T4S` (including Issue `#639` and `@DmitrL-dev`'s cross-check on PR `#761`) and `ZIB-IOL/polytof`.

### Key Findings:
- **Novelty & Non-Supersession of Partial Win `p3` and the 4 Repaired Posted Schemes (`0105`, `0108`, `0115`, `0817`):**
  - Neither `arXiv:2602.15285`, `arXiv:2610.01024`, `arXiv:2603.29894`, `ZIB-IOL/polytof`, nor `elder-plinius/V3R1T4S#639` published the complete `p3` audit of `data/paper/` (`185` decomposition files, `13,528` stored `cpd/topp` schemes across `74` single-row and `14` pool files, `9` `cpd/base` bilinear schemes, and `88` full-signature `waring` schemes) or reported the 5 posted-file Waring rank discrepancies (`0105-00041.npy` vs table `39`; `0108-00077.npy` vs table `73`; `0115-00055.npy` vs table `51`; `0728-00061.npy` vs table `59`; `0817-00063.npy` vs table `59`) and 2 dimension discrepancies (`0108`: $n=42$ vs $46$; `0114`: $n=11$ vs $12`).
  - Neither `ZIB-IOL/polytof` nor any external repository contains the repaired `.npy` Waring matrices `0105-00039.npy` (`39`), `0108-00073.npy` (`73`), `0115-00051.npy` (`51`), or `0817-00059.npy` (`59`).
  - `@DmitrL-dev` independently cross-checked our PR `#761` and confirmed all findings (`97/97` CP files matching table, `83/88` Waring files matching and the exact same `5` Waring discrepancies, `13,528/13,528` valid `cpd/topp` pool schemes, `9/9` valid `cpd/base` schemes, and all `4` repaired Waring `.npy` schemes passing the full-signature check).

pass: true
