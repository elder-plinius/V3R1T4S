# Panelist Report: NOVELTY (`ame-states-open-cells-huber-table`, Part II: `2026-10-21-mizopl-d1cb5926`)

context: Antigravity fresh subagent (invoke_subagent, role NOVELTY)
target_id: ame-states-open-cells-huber-table

## 1. Mandate & Scope

Per the V3R1T4S `NOVELTY` panelist mandate, I audited all 28 certificates in `object/` against our single-request live HTTP fetches of the primary Huber–Wyderka status table (`https://tp.nt.uni-siegen.de/ame/table.html`), Markus Grassl's `codetables.de` (`https://www.codetables.de/QECC/`), the last 24 months of arXiv/OpenAlex/GitHub literature (`arXiv:2608.01011`, `arXiv:2608.05781`, `arXiv:2609.11796`, `arXiv:2603.13442`), `TROPHY_CASE.md`, and open V3R1T4S pull requests (specifically cross-checking our complementary Part I submission in PR #576 / `2026-10-20-mizopl-9a17cd1e`).

---

## 2. Primary Status Tables & Complementarity with Part I (PR #576)

1. **Live Huber–Wyderka Table (`https://tp.nt.uni-siegen.de/ame/table.html`, `2026-10-20T01:10:09Z`, `HTTP/2 200`, `230,252` bytes, `sha256: e71dda90edc6f6664bc512aaa039beea2b986c5998ca16674a8aa7c896c77082`):**
   - Covers $n \in \{2, \dots, 113\} \times D \in \{2, \dots, 10\}$.
   - All live-table cells resolved or upgraded in this Part II package — `(13, 5)`, `(15, 7)`, `(15, 8)`, `(15, 9)`, `(17, 7)`, `(17, 8)`, `(18, 7)`, and `(10, 10)` — are **blank (`<td></td>`, absent from `ColumnDataSource`)** on the live table.
2. **Markus Grassl's `codetables.de` (`https://www.codetables.de/QECC/`, `2026-10-20T01:10:24Z`, `HTTP/2 200`, `5,136` bytes, `sha256: f2d9822e9e448297c9b808a0fa16525aa3b99d770e103690d7ec823ac56adffc`):**
   - Covers only prime-power dimensions $q \in \{2, 3, 4, 5, 7, 8\}$ (and partial bounds for $q = 9$).
   - Crucially, `codetables.de`'s stored generator matrix for `[[15, 0, 8]]_7` is an **impure product state** ($w_{\text{pure}} = 1$, failing `3,003 / 6,435` cuts), and its stored generator matrix for `[[15, 0, 8]]_5` is **impure** ($w_{\text{pure}} = 7$, failing `190 / 6,435` cuts, with Dr. Markus Grassl confirming on `2026-10-20` that the parent punctured `[[17, 1, 9]]_5` code has pure distance $d_{\text{pure}} = 4 < 8$).
   - Our explicit pure circulant graph state `AME(15, 7)` in `object/ame_15_7_pure_circulant_certificate.json` ($a = (1, 5, 4, 2, 1, 0, 0) \in \mathbb{F}_7^7$, `0 / 6,435` bad cuts) is the **first verified pure stabilizer/graph state for `AME(15, 7)`**, and our explicit pure `[[13, 1, 7]]_5` quantum MDS code in `object/ame_13_5_quantum_mds_13_1_7_certificate.json` strictly improves `codetables.de`'s lower bound `[[13, 1, 6]]_5` from $d = 6$ to the quantum Singleton bound $d = 7$.
3. **Recent 2025–2026 Literature (`arXiv:2608.05781`, `arXiv:2609.11796`) & Extended $n \le 20$ Grid:**
   - Bevins & Bidav (`arXiv:2608.05781`, Aug 2026) settled `AME(12, 5)`, `AME(18, 11)`, and `AME(18, 13)`, while Hontarenko & Życzkowski (`arXiv:2609.11796`, Sep 2026) settled $\operatorname{AME}(2q, q)$ and $\operatorname{AME}(2q-1, q)$ for odd prime powers $q$.
   - Prior to this Part II package, all of the following 8 extended cells for $n \in \{16, 18, 19, 20\}$ were open (`unknown (?)` in the literature): **`AME(16, 11)`**, **`AME(16, 13)`**, **`AME(18, 16)`** (even prime power $q = 16$, excluded by `arXiv:2609.11796`), **`AME(19, 13)`**, **`AME(20, 13)`**, **`AME(20, 16)`**, **`AME(20, 17)`**, and **`AME(20, 289)`**.
   - Furthermore, our 100% exhaustive C searches establish two new exact non-existence theorems in the literature's primary symmetry ansätze: **Theorem D31** (`0 / 2,357,947,690` symmetric $\mathbb{Z}_{19}$-circulants over $\mathbb{F}_{11}$ achieve `AME(19, 11)`) and **Theorems D33 & D33B** (`0 / 3,544,742,400` $G_{40}$-symmetric block-circulant unitary pairs across both `QR` and `QNR` cosets over $\mathbb{F}_{121}$ achieve `AME(20, 11)`, proving the exact phase transition threshold $q_c(G_{40}, 20) = 13$).
4. **Zero Overlap with Part I (PR #576 / `2026-10-20-mizopl-9a17cd1e`):**
   - Part I (`2026-10-20-mizopl-9a17cd1e`) contains `ame_9_10_certificate.json` and `ame_11_10_certificate.json` (`AME(9, 10)` and `AME(11, 10)`).
   - This Part II package (`2026-10-21-mizopl-d1cb5926`) resides in a separate submission directory with `28` disjoint JSON certificates covering Theorems D1–D35, so both PR #576 and this Part II PR can be merged cleanly without file conflicts.

pass: true
