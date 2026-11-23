# Panelist Report: NOVELTY (`ame-states-open-cells-huber-table` — `p2`)

> **Dated Scope Note (`2026-10-29`):** Per `@elder-plinius`'s review on closed PR `#576`, this standalone follow-up package is scoped strictly to **Partial Win `p2`** (1,008-cell Huber–Wyderka table-maintenance audit and `[[15, 0, 8]]` stabilizer purity erratum), explicitly cites the prior September 2026 public Lean 4 formalizations (`niketp03/atlas-fc-verified` [14 Sep 2026] / `facebookresearch/atlas-lean` for `AME(9, 10)` and `KitaKen1/ame-11-10-lean` [22 Sep 2026] for `AME(11, 10)`) and Yunus Bidav (`arXiv:2608.05781`, Aug 2026) for $[12, 6, 7]_{25} \to [[11, 1, 6]]_5$, and carries the exact URL and `sha256` digest of all 17 referenced external pages (`object/huber_wyderka_settled_blanks_audit.json`, `sha256: 61e59c7d803dc3e81b80fdad691633779ff2209bb220e34d8ee6b1bb661dfb12`).

context: Antigravity fresh subagent (invoke_subagent, role NOVELTY)
target_id: ame-states-open-cells-huber-table

## 1. Primary Table & Status Page Fetches (`2026-10-29T19:22:45Z`)

1. **Huber–Wyderka Live Table (`https://tp.nt.uni-siegen.de/ame/table.html`):**
   - `HTTP 200`, `230,252` bytes, `sha256: e71dda90edc6f6664bc512aaa039beea2b986c5998ca16674a8aa7c896c77082`.
   - Contains `485` populated cells and `523` blank cells across $2 \le n \le 113, 2 \le D \le 10$. All `23` settled positive blank cells audited in `object/huber_wyderka_settled_blanks_audit.json` remain blank on the live Huber–Wyderka table.
2. **Markus Grassl's `codetables.de` (`https://www.codetables.de/QECC/` & 14 `QECC.php` Pages):**
   - Master index `https://www.codetables.de/QECC/`: `HTTP 200`, `5,136` bytes, `last modified: 2026-10-21`, `sha256: f2d9822e9e448297c9b808a0fa16525aa3b99d770e103690d7ec823ac56adffc`.
   - `https://www.codetables.de/QECC/QECC.php?q=25&n=15&k=0` (`[[15, 0, 7..8]]_5`, `last modified: 2026-10-21`, `sha256: e2877a2731fae0b79afffddd6e82093b10df08af554f82d7707d0a82bcf67706`): confirms that following our `2026-10-20` impurity finding (`w_pure = 7 < 8`, `190 / 6,435` rank-deficient 7-party cuts), Markus Grassl downgraded the listed lower bound on `2026-10-21` from `8` to `7`, leaving `AME(15, 5)` open and confirming that `arXiv:2609.11796` Fig. 1's green cell at `(15, 5)` is an impure false positive in the published literature.
   - `https://www.codetables.de/QECC/QECC.php?q=49&n=15&k=0` (`[[15, 0, 8]]_7`, `last modified: 2026-10-21`, `sha256: c4511cff304494b4ce074bc38f403676802c1a4d0a9d77880447c43fd4ac54d4`): confirms that on `2026-10-21`, Grassl replaced the pre-`2026-10-21` impure direct-sum matrix (`w_pure = 1`, `3,003 / 6,435` bad cuts) with a pure cyclic `[[15, 0, 8]]_7` stabilizer code over $GF(49)$ (`0 / 6,435` bad cuts, $w_{\text{pure}} = 8$).
3. **`google-deepmind/formal-conjectures` (`FormalConjectures/OpenQuantumProblems/35.lean`):**
   - `https://raw.githubusercontent.com/google-deepmind/formal-conjectures/main/FormalConjectures/OpenQuantumProblems/35.lean`: `HTTP 200`, `40,112` bytes, `sha256: aee9d33c3ec607271a61a7d11752490e486f2689b2b42b58bb34f81b9e19e69e`. Properly cited in `object/huber_wyderka_settled_blanks_audit.json` alongside `niketp03/atlas-fc-verified` (14 Sep 2026) and `KitaKen1/ame-11-10-lean` (22 Sep 2026).

## 2. Verdict

This standalone `p2` package provides the first machine-verifiable 1,008-cell reconciliation of the Huber–Wyderka table against `codetables.de`, 2026 literature, and the September 2026 Lean 4 formalizations, together with the complete algebraic proof and dated `2026-10-20` / `2026-10-21` erratum of the `[[15, 0, 8]]_5` and `[[15, 0, 8]]_7` purity discrepancies correcting `arXiv:2609.11796` Fig. 1.

pass: true
