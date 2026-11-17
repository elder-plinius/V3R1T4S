# Claim: Erdős 677 has no counterexample with k = 29 and n ≤ 10^494

**Target id:** erdos-677-lcm-blocks. This is Erdős Problem 677, also Justin Sun Prize catalog JSP-000550.

**One-sentence claim:** For k = 29, every n with 0 ≤ n ≤ 10^494 and every m ≥ n + k (no cap on m),
lcm(m+1, …, m+k) ≠ lcm(n+1, …, n+k).

**What it is.** A partial result, not a solution: an exhaustive, uncapped-in-m verification of the statement
`Erdos677.erdos_677` for the stated range of (n, k). It is computer-assisted and not kernel-checked. It extends the
ranges k ≤ 25 and 26 ≤ k ≤ 28 of separate, earlier confirmed claims of this workspace with the same proof and code;
this claim covers k = 29 only.

**Status:** single-context, unpanelled (run 2026-11-09-0917). The three-skeptic panel did not fit in this run.

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

- **The proof:** `object/PROOF.md` (Lemma A; small-X window search; ratio set; margin; enumeration), each step
  labelled PROVED-HERE, COMPUTED or KNOWN. K = {29}. Step 4 now writes out the reduction of the margin to two sign
  conditions (it was only described in code comments in the earlier claims). The 2026-10-24 patch of the enumeration's
  float pre-filter is documented in `PATCH_NOTE.md` and `deep_rig_patch.diff` (this claim folder).
- **Step 2 (small X):** `object/search677b.c` run as `search677b 1100000 20261109`, then `object/verify_cands.py`.
  Outputs `object/out/search_N1.1e6.txt`, `object/out/verify_N1.1e6.txt`: COMPLETE with K = 147 (≥ 29; the k = 29 line
  has cand = 0), 2 candidates in all, 0 exact-equal.
- **Step 3 (ratio set):** `object/deep_cf.py` (`admissible_r`); independent audit `object/taskA_ratio_audit_k.py 400
  29 29`, output `object/out/taskA_ratio_audit_k29.txt`: 114817 ratios, missing 0, extra 0; all 110 equal-lcm pairs
  with n < m ≤ 400 have their ratio in the set.
- **Step 4 (margin, rigorous):** `object/rig_margin.py` (interval arithmetic, whole list), output
  `object/out/rig_margin_k29.txt`: "TOTAL pairs=114817 failures=0 undecided=0" (worst relative margin lower bound
  0.99999994). `object/rig_margin_exact.py` (exact rational intervals, bytes unchanged) run through
  `object/shard_margin.py` on 4 shards (shard I keeps the ratios at positions j ≡ I mod 4 of `admissible_r(29)`):
  `object/out/rig_margin_exact_k29_shard0.txt` … `shard3.txt`, pairs 28705 + 28704 + 28704 + 28704 = 114817, each
  "failures=0 undecided=0" (worst relative margin lower bound 0.99999994; 3218-3230 s per shard).
- **Step 5 (enumeration):** `object/deep_rig.py` (sha256 0e7d7d72…, byte-identical to the confirmed k ≤ 25 and
  26..28 packages), QMAX = 10^495, 1040 + 50 digits, η = 0.001, X0 = 10^6, run through `object/shard_rig.py` on 4
  shards. Outputs `object/out/deep_rig_shard0.txt` … `shard3.txt`; summed by `object/sum_shards.py`
  (`object/out/shard_sums.txt`): 114817 ratios, 3332527 enumerated pairs, 3288852 window candidates,
  product_solutions = 0. Every shard ends with a TOTAL line with product solutions = 0.

## Things a skeptic should know

- **The splits.** Both long computations loop over ratios independently; shard_rig.py and shard_margin.py only replace
  the list they iterate. Their per-shard ratio counts add up to 114817, the audited size of the ratio set.
  shard_margin.py is new in this claim: on k = 5..12 its single-shard output equals the unsharded output with times
  stripped, and three shards add up to the unsharded counts (`object/out/wrap_test/`: `rig_margin_exact.py 5 12
  1000000 1 1000` unsharded, as SHARD=0/1, and as SHARD=0/3, 1/3, 2/3).
- **Window bounds are not interval arithmetic** (as in the earlier claims): L and U in deep_rig.py are computed in
  1090-digit mpmath; the proved margin is the open interval with η = 10^−3.
- **The two small-X near-misses** (3,4,13) and (4,18,53) have different lcms.

## Status record (scout of this run; files in source/)

| source | URL | fetched (UTC) | HTTP | sha256 | status |
|---|---|---|---|---|---|
| problem page | https://www.erdosproblems.com/677 | 2026-11-09T09:18:58Z | 200 | df78bb5f0509108384c8cc828deabf6cb01f4b92f714b9cdb44c57560cd44a59 | "This page was last edited 30 September 2025"; Proof claims (0); source/erdosproblems_677.html |
| prize catalog | https://raw.githubusercontent.com/TheJustinSunPrize/awards/main/problems/catalog-0501-0600.md | 2026-11-09T09:19:01Z | 200 | 78ecc0e2a46520944d1b2f07196bd945433e82e4788a32585f22604c6b8b7834 | JSP-000550: Current status Open, Lean proof No; source/jsp_catalog_0501-0600.md |
