# Erdős Problem 677 (Justin Sun Prize JSP-000550): no counterexample with 26 ≤ k ≤ 28, 0 ≤ n ≤ 10^494, every m ≥ n + k

Target: `erdos-677-lcm-blocks` (Erdős Problem 677 = Justin Sun Prize catalog entry JSP-000550; a charter quarry, not
a bank target). Family folder in the repo: `known-knowns/erdos-677-lcm-blocks/`. Submission id:
`2026-11-07-adb991-b461c702` (the first 8 hex digits of the sha256 of `object/PROOF.md`). Status: `CONFIRMED_PARTIAL`
(`panel/gate.md`). Claim built in run 2026-11-06-0918, panelled in run 2026-11-07-0919. It extends the separate
package `2026-10-24-adb991-201bcc74` (k ≤ 25, same method and code) to k = 26, 27, 28; neither contains the other.

## What

confirmed_scope: For every k ∈ {26, 27, 28}, every n with 0 ≤ n ≤ 10^494 and every m ≥ n + k (m uncapped), lcm(m+1, …, m+k) ≠ lcm(n+1, …, n+k), as established by a computer-assisted, not kernel-checked argument (Lemma A, an exhaustive search for n + k ≤ 1.1·10^6, a margin proved in exact rational interval arithmetic for X ≥ 10^6, and a high-precision but not interval-arithmetic continued-fraction enumeration up to q ≤ 10^495), which is enumerated partial win 1 and not a solution of Erdős Problem 677.

In plain words: write M(n, k) = lcm(n+1, …, n+k). Erdős asked whether two disjoint blocks of k consecutive integers
always have different least common multiples, i.e. M(m, k) ≠ M(n, k) whenever m ≥ n + k (formal statement:
google-deepmind/formal-conjectures `Erdos677.erdos_677`, copied in `how-we-built-it/claim/checker/spec_677.lean`).
This package settles every instance with block length k = 26, 27 or 28 and first block starting at n ≤ 10^494,
against every later block however far away. It is a partial result; the problem stays open.

How it works (`object/PROOF.md`, Steps 1–5): Lemma A (a hand proof) reduces an equality to f(m)/f(n) = r for a finite
set of prime ratios r and bounds m; small X (n + k ≤ 1.1·10^6) is searched completely (`object/search677b.c`,
`object/verify_cands.py`); the ratio set (`object/deep_cf.py`) is audited independently
(`object/taskA_ratio_audit_k.py`); a margin is proved for X ≥ 10^6 (`object/rig_margin_exact.py`, exact rational
intervals; `object/rig_margin.py`, interval arithmetic); and the continued-fraction enumeration (`object/deep_rig.py`,
run through `object/shard_rig.py` on 4 shards of the ratio list) tests every candidate to q ≤ 10^495 exactly.

| step | saved output (`object/out/`) | result |
|---|---|---|
| 2 | `search_N1.1e6.txt`, `verify_N1.1e6.txt` | `# COMPLETE kmin=3 kmax=147 total_candidates=2`; `candidates: 2 exact-equal: 0` |
| 3 | `taskA_ratio_audit_k26-28.txt` | `TOTAL missing over k=26..28: 0` (21262, 16402, 21262 ratios) |
| 4 | `rig_margin_k26-28.txt`; `rig_margin_exact_k26.txt`, `_k27.txt`, `_k28.txt` | `TOTAL pairs=58926 failures=0 undecided=0`; each k `failures=0 undecided=0` |
| 5 | `deep_rig_shard0.txt` … `deep_rig_shard3.txt`, `shard_sums.txt` | product_solutions=0 for every shard and k; window candidates 490397 + 411576 + 553418 = 1455391 |

| object file | sha256 |
|---|---|
| object/PROOF.md | b461c7024f94a9487ab922b5558e017fcc747c56ce123b07d5083862307a2f81 |
| object/deep_cf.py | dc74be2f2b68c5618437b9b972f7313621ab556360a33e7e784e5f0dc82e6b85 |
| object/deep_rig.py | 0e7d7d72f04e5076827c28afb1184f5ef3eb69c3a4be965a6c2e770cd6ad0341 |
| object/out/deep_rig_shard0.txt | de27e17ffa4585c3511fb782af030b9570ab772d8b9ed707f00708b1950b1c13 |
| object/out/deep_rig_shard1.txt | 566af51ccbd48cafb54dccd6c03ec79becfc018a3ab8b85160d75c7ed4779555 |
| object/out/deep_rig_shard2.txt | 82de59df6124ce9853c51de197c101d20fe6c4780f388548be5a536e6f95a187 |
| object/out/deep_rig_shard3.txt | 481346c412fcf3d853ec98b87bc88d53f1c30a1b03c3412646c671f6cdbeca9a |
| object/out/rig_margin_exact_k26.txt | 0f5ad4e060971074a4378281d9696fcbe4917516987b3198ee37a2b6b55e75f0 |
| object/out/rig_margin_exact_k27.txt | 14226025f900d5353be52a4f8a7134d2737cfd299642ae434fcf7eb3988b6e60 |
| object/out/rig_margin_exact_k28.txt | dfef8b097f9134b51f9330edb8e3c39d8725d25dac733c00175e20230f0c7cf8 |
| object/out/rig_margin_k26-28.txt | 588060cf03232bb2e65289fc0bb6a4993aa79e9623e0bac05abcdf46f19bda02 |
| object/out/search_N1.1e6.log | 20f5ee6956166e16f7b700e08cf47321d7adad0d45de0916ba9c42627afae052 |
| object/out/search_N1.1e6.txt | c3c75fb3fad9a5d125b3c9262df62a0b4524b6bcbf09e3aa28a7a3bcb487ee34 |
| object/out/shard_sums.txt | 22c9f291140b5fa541674b2cbe41516be62fed6cabb4a81f36a0d3816bddc82e |
| object/out/taskA_ratio_audit_k26-28.txt | 124a8fc4605b695c56a627bd141e4f82c1da51d84770ae9a0e1c5301763084da |
| object/out/verify_N1.1e6.txt | 560873dc0712ddd08d822d18eb3f54097bc5a40c8274d33510c8729e1334ff84 |
| object/rig_margin.py | 3d1b50ab5f638def5d0dea18099a701c263d80caf8a4e1e3ea8db2dcde924e76 |
| object/rig_margin_exact.py | 64328c1f47d3ef88418e8e77b462f6b70ea2aa3438e6249e1194b52e96d3f12b |
| object/search677b.c | d9c01611ba8e1fa5fff4a54c1c08b7a1d44689707fc98e8d60dfd054e460caa9 |
| object/shard_rig.py | 41cdb740e45b1b9fd7ed219be63cfcc8f1916a3f1924d6522568287b1a90d130 |
| object/sum_shards.py | bebff93f5e06f9cf019ae79cf7b41ccb7dfc8879631d05a5c62aac0e1c521642 |
| object/taskA_ratio_audit_k.py | ce6fa546045e398f00b5fd1980e74a04c5d59ffecea547fe25d7384f900871e5 |
| object/verify_cands.py | 5e848cf39dd1b793e12a20cc3fae8ea8c2422e904e840ba0e29bb9ac418154d8 |

All 23 are byte-identical copies of the claim the panel read (`runs/2026-11-06-0918/claim/object/` in the
contributor's workspace; the claim text is `how-we-built-it/claim/CLAIM.md`).

## Check it yourself

```sh
PY=python3 sh verify-it-yourself/run_checks.sh     # from this folder; PY must have gmpy2, mpmath and numpy
```

Expected last line: `PASS`. By default it checks the object hashes and the saved outputs, then reruns step 2, step 3
(ratio audit), step 4 with interval arithmetic and step 5 for k = 27 on shard 0 of 4, comparing each output with the
saved one (times stripped): PASS in 531 s with 4 jobs on the contributor's 4-core machine (`verify-it-yourself/RECEIPTS.md`). `--all` reruns all four shards for
k = 26..28 and the exact-rational margin checker per k (about 2 to 3 hours on 4 cores). Details: `RUN_IT_YOURSELF.md`.

The script checks the computation. It cannot check the hand proof (Lemma A and the completeness argument of the
enumeration, `object/PROOF.md`, to be read), and a rerun reproduces, but does not prove correct, the float64
pre-filters and 1090-digit non-interval arithmetic inside `deep_rig.py`.

## Compared to

| source | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| Justin Sun Prize catalog, JSP-000550 (status source) | Current status / Lean proof | Open / No; no partial result recorded | https://raw.githubusercontent.com/TheJustinSunPrize/awards/main/problems/catalog-0501-0600.md | 2026-11-07T09:20:31Z (HTTP 200, sha256 78ecc0e2a46520944d1b2f07196bd945433e82e4788a32585f22604c6b8b7834) |
| erdosproblems.com, problem 677 | recorded results | Thue–Siegel finiteness for each fixed k; Proof claims (0) | https://www.erdosproblems.com/677 | 2026-11-07T09:20:32Z (HTTP 200, sha256 837f45777da64c53a1cd319f3df5173968d686c0e3c7ae8f310b5def282bc6de) |
| laaielichter/erdos-677 (GitHub, 2026-10-27) | k ≤ 100 | no solution with m + k ≤ 10^8 | https://github.com/laaielichter/erdos-677 | read by the NOVELTY skeptic, 2026-11-07 |

Snapshot and the other searches: `the-record-we-beat/STATUS_RECORD.md` and `panel/novelty.md`.

## Not claimed

- Not a solution of Erdős Problem 677, and not a prize solution (the Justin Sun Prize accepts only complete
  solutions). The problem remains open.
- Not kernel-checked. The proof is informal (`object/PROOF.md`); no Lean proof of the range statement exists.
- The float64 pre-filters and the 1090-digit non-interval arithmetic in the enumeration are supported by error
  analysis and reruns, not formally proved (`panel/criterion.md`).
- Only k = 26, 27, 28. k ≤ 25 is the separate package 2026-10-24-adb991-201bcc74; nothing for k ≥ 29.
- The CRITERION skeptic noted documentation gaps that do not affect the computation: the Step 4 reduction to two
  polynomial positivity conditions is described in the code's header but not written out in `object/PROOF.md`, and
  PROOF.md refers to a patch note that sits in `how-we-built-it/PATCH_NOTE.md` here rather than in CLAIM.md.
- No pull request, issue or message was sent to anyone.

## Credits

- Paul Erdős, who posed the problem (Erdős Problem 677; [Er79], [Er79d], [ErGr80] on the problem page).
- T. F. Bloom's Erdős Problems website, https://www.erdosproblems.com/677 (statement, recorded results, forum).
- The Justin Sun Prize catalog, entry JSP-000550, https://github.com/TheJustinSunPrize/awards (the status source).
- google-deepmind/formal-conjectures, https://github.com/google-deepmind/formal-conjectures
  (`FormalConjectures/ErdosProblems/677.lean`, the formal statement `Erdos677.erdos_677` and `lcmInterval`).
- S. Chan, arXiv:2408.01306 (Period. Math. Hung. 2025), Theorem 1, which settles k = 3.
- V3R1T4S, https://github.com/elder-plinius/V3R1T4S (the run protocol, panel and gate).
- Contributor: ADB991 (an AI-agent run under the V3R1T4S kit; see `HOW_WE_FOUND_IT.md` and `prompt/`).
