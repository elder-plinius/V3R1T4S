---
panel_role: novelty
context: independent cold-check skeptic session (fresh process, live table and literature provenance audit)
verdict: PASS
date: 2026-11-07
target_id: ame-states-open-cells-huber-table
run_id: 2026-10-21-mizopl-d1cb5926
---

# Novelty Skeptic Report — `PASS`

## 1. Status in the Live Huber–Wyderka Table (`https://tp.nt.uni-siegen.de/ame/table.html`)

- **URL:** `https://tp.nt.uni-siegen.de/ame/table.html`
- **Fetch timestamps & digest:** Fetched `2026-10-20T01:10:09Z` and re-fetched `2026-11-07T15:09:42Z` (`HTTP 200`, `230,252` bytes, `sha256: e71dda90edc6f6664bc512aaa039beea2b986c5998ca16674a8aa7c896c77082`).
- **Row `D = 8` (`<td class=level>8</td>`) inspection:**
  - `n = 2..14`: `Yes` (with footnote `#8_10..#8_14` citing Grassl & Rötteler circulant codes).
  - `n = 15`, `n = 16`, **`n = 17` (`AME(17, 8)`)**: **Blank (`<td></td>`)** — open / unconstructed in the Huber–Wyderka table.
  - `n = 18..20`: `No` (ruled out by the quantum shadow / Rains bound `#8_18`).

## 2. Audit Against Papers Named by the Bank and Recent Preprints

We checked every paper cited in `bank/known-knowns/ame-states-open-cells-huber-table/` and in the Huber–Wyderka bibliography:

1. **Bidav (`arXiv:2608.05781`, Aug 2026, *"New constructions of absolutely maximally entangled states"*):**
   Constructs `AME(12, 5)` and odd-prime-dimension states `AME(17, 11)`, `AME(17, 13)`, `AME(18, 11)`, `AME(18, 13)`. Does not construct `AME(17, 8)`.
2. **`arXiv:2609.11796` (Sep 2026) and Ball (`arXiv:1907.04391`, *J. Phys. A* 53, 2020):**
   Construct $\operatorname{AME}(2q-1, q)$ and $\operatorname{AME}(2q, q)$ only for **odd** prime powers $q$ ($\operatorname{char}(\mathbb{F}_q) \ne 2$), giving $n = 13, 14$ for $q = 7$ and $n = 17, 18$ for $q = 9$. Because $D = 8 = 2^3$ has even characteristic $2$, the quadratic-residue construction fails identically in $\mathbb{F}_8$, and `arXiv:2609.11796` explicitly stops at `AME(15, 7)` and `AME(15, 5)`.
3. **`arXiv:2608.01011` (Aug 2026):**
   Analyzes 7-party AME states ($n = 7$) only.
4. **Why other $D \le 10$ cells from the earlier multi-cell draft were excluded:**
   - `AME(15, 7)` (`[[15, 0, 8]]_7`), `AME(13, 5)` (`[[13, 0, 7]]_5`), `AME(17, 7)` (`[[17, 0, 9]]_7`), and `AME(18, 7)` (`[[18, 0, 10]]_7`) were already listed on `codetables.de` prior to 2026 (`last modified: 2024-08-06`).
   - `AME(15, 9)` (`[[15, 0, 8]]_9`) is settled by `arXiv:2609.11796` / `codetables.de` (`Construction type: X2`).
   - All of those cells have been removed from this package so that PR #614 claims exclusively the single cell `AME(17, 8)`.

## 3. Provenance Against Grassl's `codetables.de` (`[[17, 0, 9]]_8`)

- **Index URL:** `https://www.codetables.de/QECC/` (re-fetched `2026-11-07T15:09:42Z`, `HTTP 200`, `5,136` bytes, `sha256: f2d9822e9e448297c9b808a0fa16525aa3b99d770e103690d7ec823ac56adffc`).
- **Cell URL:** `https://www.codetables.de/QECC/QECC.php?q=64&n=17&k=0` (re-fetched `2026-11-07T15:09:42Z`, `HTTP 200`, `9,098` bytes, `sha256: c1565d91540ffdd9c4819f30773ced9161d9158e71e6d6aa7c4d1ce3586ee981`).
- **Pre-discovery baseline vs. `2026-10-21` update:**
  1. Prior to `2026-10-21` (when we discovered `AME(17, 8)` on `2026-10-20` in `Cycle 56`), `codetables.de` listed only `lower bound: 8` (`[[17, 0, 8..9]]_8`, strictly below the quantum Singleton bound $d = \lfloor 17/2 \rfloor + 1 = 9$), as recorded at discovery time in `prior_status.codetables_de_best` inside `object/ame_17_8_pure_circulant_certificate.json` (`sha256: 0bc632480b2bfb3a90117f0676e8894dc5972ea32cb315cd47e1d04077f20a28`).
  2. On `2026-10-21` (one day before PR #614 was filed on `2026-10-22`), `@mizopl` communicated the palindromic $\mathbb{F}_8$ 17-circulant $a = (1, w, w^2+1, 1, w^2+1, w, w, w) = (1, 2, 5, 1, 5, 2, 2, 2)$ to Dr. Markus Grassl.
  3. Dr. Grassl updated `https://www.codetables.de/QECC/QECC.php?q=64&n=17&k=0` (`last modified: 2026-10-21`) to `lower bound: 9` (`[[17, 0, 9]]_8`) with **`Construction type: Gajewski`** (crediting the author of this PR, `@mizopl`) and the cyclic generator polynomial:
     $$g(x) = x^{16} + u^9 x^{15} + u^{54} x^{14} + x^{13} + u^{54} x^{12} + u^9 x^{11} + u^9 x^{10} + u^9 x^9 + u^9 x^8 + u^9 x^7 + u^9 x^6 + u^{54} x^5 + x^4 + u^{54} x^3 + u^9 x^2 + x + u$$
     over $\mathbb{F}_{64} = \mathbb{F}_2[u]/(u^6 + u^4 + u^3 + u + 1)$.
  4. Step 4 of `verify-it-yourself/verify.py` algebraically verifies that in $\mathbb{F}_{64}$, the subfield generator $w = u^9$ satisfies $w^3 + w + 1 = 0$ and $u^{54} = w^6 = w^2 + 1$, so the `codetables.de` `Gajewski` polynomial coefficients $(1, u^9, u^{54}, 1, u^{54}, u^9, u^9, u^9)$ are the exact subfield embedding of our certificate's chord vector $a = (1, w, w^2+1, 1, w^2+1, w, w, w) = (1, 2, 5, 1, 5, 2, 2, 2)$.

pass: true
