# Claim: Erdős 677 has no counterexample with k ≤ 25 and n ≤ 10^494

**Target id:** erdos-677-lcm-blocks. This is Erdős Problem 677, also Justin Sun Prize catalog JSP-000550.

**One-sentence claim:** For every k with 1 ≤ k ≤ 25, every n with 0 ≤ n ≤ 10^494 and every m ≥ n + k (no cap on m),
lcm(m+1, …, m+k) ≠ lcm(n+1, …, n+k).

**What it is.** A partial result, not a solution. It is an exhaustive, uncapped-in-m verification of the statement
`Erdos677.erdos_677` for the stated range of (n, k). It is computer-assisted and not kernel-checked.

## Success criterion (verbatim, from the run's target.md)

Prize catalog, JSP-000550, "Problem description": "Must two disjoint equal-length intervals of consecutive integers
have different least common multiples?"

formal-conjectures `Erdos677.erdos_677` (FormalConjectures/ErdosProblems/677.lean, fetched 2026-10-24T08:21:40Z):
"Denote by $M(n, k)$ the least common multiple of the finite set $\{n+1, \dotsc, n+k\}$. Is it true that for all
$m \geq n + k$, we get $M(m, k) \neq M(n, k)$?"
```
theorem erdos_677 :
    ∀ (m n k : ℕ), k > 0 → m ≥ n + k → lcmInterval m k ≠ lcmInterval n k
```
with `lcmInterval n k := (Finset.Ioc n (n + k)).lcm id`.
Success = a kernel-checked proof of this statement or of its negation (a counterexample).

Partial wins (workspace only, NOT prize solutions): an exhaustive, uncapped verification of the statement for a
stated range of (n, k) with a checkable certificate; a machine-checked proof for a fixed small k.

## The certificate (object/)

- **The proof:** `object/PROOF.md`. Steps 1–5: Lemma A; the small-X window search; the ratio set; the margin; the
  enumeration. Each step is labelled PROVED-HERE, COMPUTED or KNOWN.
- **Step 2:** `object/search677b.c` and `object/verify_cands.py`.
  - Outputs: `object/out/search_N1.1e6.txt`, `object/out/search_N1.1e6.log` and `object/out/verify_N1.1e6.txt`.
  - Result: complete for n + k ≤ 1.1·10^6, every k. 2 candidates, (3,4,13) and (4,18,53), with 0 exact-equal.
- **Step 3:** `object/deep_cf.py` (`admissible_r`) lists the ratio set.
  - Independent audit: `object/taskA_ratio_audit.py`, output `object/out/taskA_ratio_audit_NB3000.txt`.
  - Result: missing 0 and extra 0 for k = 3..25, 63041 ratios in total. All 970 equal-lcm pairs with
    n < m ≤ 3000, k ≤ 25 have their ratio in the set.
- **Step 4 (margin, rigorous):** two checkers, `object/rig_margin.py` (interval arithmetic, mpmath.iv at 320 bits)
  and `object/rig_margin_exact.py` (exact rational intervals, no floating point).
  - Outputs: `object/out/rig_margin_k3-25_X1e6_eta1e-3.txt` and `object/out/rig_margin_exact_k3-25_X1e6_eta1e-3.txt`.
  - Each ends "TOTAL pairs=63041 failures=0 undecided=0".
- **Step 5 (enumeration):** `object/deep_rig.py`, with QMAX = 10^495, 1040 + 50 digits, η = 0.001 and X0 = 10^6.
  - Outputs: `object/out/deep_rig_final_k3-18_d1040.txt`, `…_k19-22_…`, `…_k23-23_…`, `…_k24-24_…` and `…_k25-25_…`.
  - Every k = 3..25 has product_solutions = 0; there are 1,174,616 window candidates in total.

## Things a skeptic should know

- **deep_rig.py was patched tonight.** Its double-precision pre-filter on g = q(qρ − p) originally computed
  u = r' + s·Qn in float. r' and s have opposite signs, so this cancels when Qn = q_i/q_{i+1} is tiny, and a valid
  pair could be dropped. The patched code computes u from the exact integer q whenever Qn < 10^−4 or
  3.4·10^−16·(R+1)/Qn > 10^−9. Elsewhere the float u's relative error is ≤ 10^−9, against the filter's 10^−6
  tolerance.
  - The enumeration outputs above all come from the patched code.
  - For k = 3..18, the per-k counts of the patched and unpatched code are identical.
  - For k = 19..23, the window-candidate counts equal those of an earlier unpatched run (2026-10-15):
    77951, 46823, 52854, 70683 and 314109.
- **Only path lines differ from the lens copies.** In the three rigor-margin scripts, the import path of deep_cf.py
  was changed to the script's own folder; nothing else differs. deep_rig.py, deep_cf.py, search677b.c and
  verify_cands.py are byte-identical to the lens copies.
- **Window bounds are not interval arithmetic.** L and U in deep_rig.py are computed in 1090-digit mpmath. The proved
  margin is the open interval with η = 10^−3. A 150-digit sanity solve showed true solutions lie within a relative
  4·10^−11 of c (NUMERICAL), far inside the window.
- **The two near-misses** (3,4,13) and (4,18,53) also appeared in a 2026-10-15 run. Both have different lcms.

## Status record (scout of this run, 2026-10-24; files in source/)

| source | URL | fetched (UTC) | HTTP | sha256 | status |
|---|---|---|---|---|---|
| prize catalog | https://raw.githubusercontent.com/TheJustinSunPrize/awards/main/problems/catalog-0501-0600.md | 2026-10-24T08:21:40Z | 200 | 78ecc0e2a46520944d1b2f07196bd945433e82e4788a32585f22604c6b8b7834 | JSP-000550 "Current status \| Open", "Lean proof \| No" |
| problem page | https://www.erdosproblems.com/677 | 2026-10-24T08:21:38Z | 200 | fc9bde5b511ac69b62b441fb8a75596ec11420e1bf2409e04f34d860f26e5cad | open; "Proof claims (0)"; text in source/erdosproblems_677.txt |
| forum | https://www.erdosproblems.com/forum/thread/677 | 2026-10-24T08:21:39Z | 200 | 2ecb1aa7d4990847253d30c3ddf49470b0aa75209b73d9af9e7dc91188118d0a | 8 comments, no range verification |
| formal-conjectures | https://raw.githubusercontent.com/google-deepmind/formal-conjectures/main/FormalConjectures/ErdosProblems/677.lean | 2026-10-24T08:21:40Z | 200 | cc682a41950449c693578cdfc83060505bcd482abc12ab33233eaea483681bd0 | `research open`; source/fc_677.lean |

The status source for NOVELTY is the prize catalog URL above, together with the problem page.

A related, separate claim from an earlier run of this workspace is not part of this claim: "no counterexample with
n ≤ 5871·k". Neither claim contains the other: that one covers every k but only n ≤ 5871·k, while this one covers
k ≤ 25 with n up to 10^494.
