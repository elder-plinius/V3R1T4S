# Verification Receipts — `2026-10-25-mizopl-7162c3e8` (`polytof-toffoli-tcount-benchmark-tensors`)

## Command Executed
```sh
sh verify-it-yourself/run_checks.sh
```

## Real Output (`4.28 s` Single-Thread Audit on 16 GB M1 MacBook Air)
```text
[PASS] Pinned polytof commit 0dcac107d15a & docs/tensors.md (sha256=f83839d05898...) parsed.
[PASS] Audited all 185 decomposition files in data/paper/: 88 cpd/topp (13528/13528 schemes across 74 single-row + 14 pool files), 9 cpd/base (9/9 bilinear schemes), and 88 waring (88/88 full-signature valid).
[PASS] Recomputed p3 discrepancies vs docs/tensors.md: 5 Waring rank discrepancies (0105: 41 vs 39, 0108: 77 vs 73, 0115: 55 vs 51, 0728: 61 vs 59, 0817: 63 vs 59) and 2 dimension discrepancies (0108: n=42 vs 46, 0114: n=11 vs 12).
[PASS] Repaired Waring scheme object/waring/0105-00039.npy (CSLA MUX_3, n=21): posted=41 -> repaired=39 == table=39 (full signature BCO & orig bases: PASS, sha256=b0009293a2f7...)
[PASS] Repaired Waring scheme object/waring/0108-00073.npy (Ham15 (low), n=42): posted=77 -> repaired=73 == table=73 (full signature BCO & orig bases: PASS, sha256=5418608b809f...)
[PASS] Repaired Waring scheme object/waring/0115-00051.npy (Mod Red_21, n=28): posted=55 -> repaired=51 == table=51 (full signature BCO & orig bases: PASS, sha256=86ca689e0bac...)
[PASS] Repaired Waring scheme object/waring/0817-00059.npy (QCLA Com_7, n=42): posted=63 -> repaired=59 == table=59 (full signature BCO & orig bases: PASS, sha256=a328bc20a19c...)
[PASS] Complete p3 audit recomputed and verified in 4.28s.
PASS
```
