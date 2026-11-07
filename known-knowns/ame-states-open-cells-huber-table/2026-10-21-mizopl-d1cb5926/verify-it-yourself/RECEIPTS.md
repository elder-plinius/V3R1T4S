# Verification Receipts — `AME(17, 8)` (`[[17, 0, 9]]_8`)

## 1. Execution of `sh verify-it-yourself/run_checks.sh`

- **Command:** `sh verify-it-yourself/run_checks.sh`
- **Working directory:** `known-knowns/ame-states-open-cells-huber-table/2026-10-21-mizopl-d1cb5926`
- **Timestamp (UTC):** `2026-11-07T15:19:19Z`
- **Exit code:** `0`

```text
========================================================================
V3R1T4S Exhaustive Verifier — AME(17, 8) / [[17, 0, 9]]_8 (Huber Table)
========================================================================
Certificate file     : object/ame_17_8_pure_circulant_certificate.json
Certificate SHA-256  : 0bc632480b2bfb3a90117f0676e8894dc5972ea32cb315cd47e1d04077f20a28 (4176 bytes)
Field                : GF(8) = GF(2)[w]/(w^3 + w + 1)
Chord d=1..8 (GF(8)) : [1, 2, 5, 1, 5, 2, 2, 2] = ['1', 'w', 'w^2+1', '1', 'w^2+1', 'w', 'w', 'w']
GF(8) 8-party cuts   : 24,310 / 24,310 full rank 8 (bad=0, 0.40s)
GF(2) 51-qubit cuts  : 24,310 / 24,310 full rank 24 (bad=0, 0.66s)
codetables.de [[17,0,9]]_8 (Gajewski, 2026-10-21) GF(64) subfield match : EXACT
Controls             : C_5 AME(5,2)=10/10 PASS | AME(4,2)=0/64 | Mutant(edge->0)=184 bad | Mutant(d1->0)=918 bad | BestRandom400(seed=42)=24140/24310 (170 bad)
Total runtime        : 2.24s
PASS
```

## 2. Execution of `how-we-built-it/search_and_verify_ame_17_8_circulant.py`

- **Command:** `/opt/homebrew/bin/python3 how-we-built-it/search_and_verify_ame_17_8_circulant.py`
- **Exit code:** `0`

```text
Target AME(17, 8) chord [1, 2, 5, 1, 5, 2, 2, 2]: 24310/24310 full-rank cuts (0 bad cuts)
Null control (400 random GF(8) 17-circulants, seed=42, 4.63s): pass_count=0/400, best_control=24140/24310 (min_bad_cuts=170, best_chord=[5, 1, 0, 1, 7, 0, 4, 6])
```

## 3. External Baseline Fetch Receipts (`2026-11-07T15:09:42Z`)

| Resource | URL | HTTP Status | Size (bytes) | SHA-256 Digest |
| :--- | :--- | :--- | :--- | :--- |
| **Huber–Wyderka Live Table** | `https://tp.nt.uni-siegen.de/ame/table.html` | `200` | `230,252` | `e71dda90edc6f6664bc512aaa039beea2b986c5998ca16674a8aa7c896c77082` |
| **Grassl `codetables.de` QECC Index** | `https://www.codetables.de/QECC/` | `200` | `5,136` | `f2d9822e9e448297c9b808a0fa16525aa3b99d770e103690d7ec823ac56adffc` |
| **Grassl `codetables.de` `[[17,0,9]]_8`** | `https://www.codetables.de/QECC/QECC.php?q=64&n=17&k=0` | `200` | `9,098` | `c1565d91540ffdd9c4819f30773ced9161d9158e71e6d6aa7c4d1ce3586ee981` |
