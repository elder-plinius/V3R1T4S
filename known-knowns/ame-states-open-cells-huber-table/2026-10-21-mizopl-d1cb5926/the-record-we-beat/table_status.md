# Baseline Snapshot & Provenance Audit — `AME(17, 8)` (`[[17, 0, 9]]_8`)

## 1. Live Huber–Wyderka Online Table (`https://tp.nt.uni-siegen.de/ame/table.html`)

- **Source URL:** `https://tp.nt.uni-siegen.de/ame/table.html`
- **Fetch timestamps:** `2026-10-20T01:10:09Z` and re-fetched `2026-11-07T15:09:42Z`
- **HTTP status / size / SHA-256:** `HTTP 200`, `230,252` bytes, `sha256: e71dda90edc6f6664bc512aaa039beea2b986c5998ca16674a8aa7c896c77082`
- **Table domain:** Local dimensions $D \in \{2..10\}$ (`485` filled cells across rows $D = 2..10$, columns $n = 2..20$).
- **Exact row `D = 8` (`<td class=level>8</td>`) in `https://tp.nt.uni-siegen.de/ame/table.html`:**

| $n$ | $2..9$ | $10..14$ | $15$ | $16$ | **$17$ (`AME(17, 8)`)** | $18..20$ |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Table entry** | `Yes` (`#8_2..#8_9`) | `Yes` (`#8_10..#8_14`, Grassl & Rötteler circulant codes) | **Blank (`<td></td>`)** | **Blank (`<td></td>`)** | **Blank (`<td></td>`)** | `No` (`#8_18`, Rains / shadow bound) |

Cell $(n = 17, D = 8)$ is **Blank** (`<td></td>`, open / unknown) in the live Huber–Wyderka table.

## 2. Audit Against Papers Named by the Bank

We checked all references in `bank/known-knowns/ame-states-open-cells-huber-table/`:

1. **Bidav (`arXiv:2608.05781`, Aug 2026, *"New constructions of absolutely maximally entangled states"*):**
   Constructs `AME(12, 5)`, `AME(17, 11)`, `AME(17, 13)`, `AME(18, 11)`, and `AME(18, 13)`. Does not construct `AME(17, 8)`.
2. **`arXiv:2609.11796` (Sep 2026) and Ball (*J. Phys. A* 53, 2020, `arXiv:1907.04391`):**
   Construct $\operatorname{AME}(2q-1, q)$ and $\operatorname{AME}(2q, q)$ for **odd** prime powers $q$ ($\operatorname{char}(\mathbb{F}_q) \ne 2$), yielding $n = 13, 14$ for $q = 7$ and $n = 17, 18$ for $q = 9$. Because $D = 8 = 2^3$ has even characteristic $2$, the odd-characteristic quadratic-residue construction does not apply to $\mathbb{F}_8$, and `arXiv:2609.11796` stops at `AME(15, 7)` and `AME(15, 5)`.
3. **`arXiv:2608.01011` (Aug 2026):**
   Covers $n = 7$ only.

## 3. Provenance Against Grassl's `codetables.de` (`[[17, 0, 9]]_8`)

- **QECC Index URL:** `https://www.codetables.de/QECC/` (re-fetched `2026-11-07T15:09:42Z`, `HTTP 200`, `5,136` bytes, `sha256: f2d9822e9e448297c9b808a0fa16525aa3b99d770e103690d7ec823ac56adffc`).
- **Specific entry URL (`q = D^2 = 64, n = 17, k = 0`):** `https://www.codetables.de/QECC/QECC.php?q=64&n=17&k=0` (re-fetched `2026-11-07T15:09:42Z`, `HTTP 200`, `9,098` bytes, `sha256: c1565d91540ffdd9c4819f30773ced9161d9158e71e6d6aa7c4d1ce3586ee981`).
- **Chronological record:**
  1. **Before `2026-10-21` (at discovery on `2026-10-20`):** `codetables.de` listed only `lower bound: 8` (`[[17, 0, 8..9]]_8`, strictly below the quantum Singleton bound $d = \lfloor 17/2 \rfloor + 1 = 9$), as recorded at the time in `prior_status.codetables_de_best` inside `object/ame_17_8_pure_circulant_certificate.json` (`sha256: 0bc632480b2bfb3a90117f0676e8894dc5972ea32cb315cd47e1d04077f20a28`).
  2. **On `2026-10-21` (one day before PR #614 was opened on `2026-10-22`):** The author of this PR (`@mizopl`) sent the palindromic $\mathbb{F}_8$ 17-circulant $a = (1, w, w^2+1, 1, w^2+1, w, w, w) = (1, 2, 5, 1, 5, 2, 2, 2)$ to Dr. Markus Grassl.
  3. **Update on `https://www.codetables.de/QECC/QECC.php?q=64&n=17&k=0` (`last modified: 2026-10-21`):** Dr. Grassl updated the `[[17, 0, 9]]_8` page from lower bound `8` to lower bound `9` under **`Construction type: Gajewski`** (crediting the submitter of this PR) with the cyclic generator polynomial:
     $$g(x) = x^{16} + u^9 x^{15} + u^{54} x^{14} + x^{13} + u^{54} x^{12} + u^9 x^{11} + u^9 x^{10} + u^9 x^9 + u^9 x^8 + u^9 x^7 + u^9 x^6 + u^{54} x^5 + x^4 + u^{54} x^3 + u^9 x^2 + x + u$$
     over $\mathbb{F}_{64} = \mathbb{F}_2[u]/(u^6 + u^4 + u^3 + u + 1)$, where $w = u^9$ generates $\mathbb{F}_8 \subset \mathbb{F}_{64}$ ($w^3 + w + 1 = 0$) and $u^{54} = w^6 = w^2 + 1$. Step 4 of `verify-it-yourself/verify.py` verifies this exact subfield isomorphism automatically.
