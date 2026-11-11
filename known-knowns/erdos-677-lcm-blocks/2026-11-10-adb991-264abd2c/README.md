# Erdős Problem 677 (Justin Sun Prize JSP-000550): no counterexample with k = 29, 0 ≤ n ≤ 10^494, every m ≥ n + k

Target: `erdos-677-lcm-blocks` (Erdős Problem 677 = Justin Sun Prize catalog entry JSP-000550; a charter quarry, not
a bank target). Family folder in the repo: `known-knowns/erdos-677-lcm-blocks/`. Submission id:
`2026-11-10-adb991-264abd2c` (the first 8 hex digits of the sha256 of `object/PROOF.md`). Status: `CONFIRMED_PARTIAL`
(`panel/gate.md`). Claim built in run 2026-11-09-0917, panelled in run 2026-11-10-0917. It extends the separate
packages `2026-10-24-adb991-201bcc74` (k ≤ 25) and `2026-11-07-adb991-b461c702` (26 ≤ k ≤ 28), with the same method
and code, to k = 29; none contains another.

## What

confirmed_scope: For k = 29, every 0 ≤ n ≤ 10^494 and every m ≥ n + 29 (m unbounded), lcm(m+1, …, m+29) ≠ lcm(n+1, …, n+29), established by a computer-assisted, not kernel-checked certificate (Lemma A, a complete small-X search for n + 29 ≤ 1.1·10^6, an exact-rational-interval margin for X ≥ 10^6, and a continued-fraction enumeration to q ≤ 10^495 whose window bounds and candidate generation use high-precision/float arithmetic with error bounds and brute-force validation rather than interval arithmetic) — a workspace partial win for `Erdos677.erdos_677`, not a prize solution.

In plain words: write M(n, k) = lcm(n+1, …, n+k). Erdős asked whether two disjoint blocks of k consecutive integers
always have different least common multiples, i.e. M(m, k) ≠ M(n, k) whenever m ≥ n + k (formal statement:
google-deepmind/formal-conjectures `Erdos677.erdos_677`, copied in `how-we-built-it/claim/spec_677.lean`). This
package settles every instance with block length k = 29 and first block starting at n ≤ 10^494, against every later
block however far away. It is a partial result; the problem stays open.

How it works (`object/PROOF.md`, Steps 1–5): Lemma A (a hand proof) reduces an equality to f(m)/f(n) = r for a finite
set of 114817 ratios r and bounds m; small X (n + k ≤ 1.1·10^6) is searched completely (`object/search677b.c`,
`object/verify_cands.py`); the ratio set (`object/deep_cf.py`) is audited independently
(`object/taskA_ratio_audit_k.py`); a margin is proved for X ≥ 10^6, with the reduction to two sign conditions written
out in PROOF.md (`object/rig_margin_exact.py`, exact rational intervals, run on 4 shards through
`object/shard_margin.py`; `object/rig_margin.py`, interval arithmetic, whole list); and the continued-fraction
enumeration (`object/deep_rig.py`, run through `object/shard_rig.py` on 4 shards) tests every candidate to q ≤ 10^495
exactly.

| step | saved output (`object/out/`) | result |
|---|---|---|
| 2 | `search_N1.1e6.txt`, `verify_N1.1e6.txt` | `# COMPLETE kmin=3 kmax=147 total_candidates=2` (k = 29: cand = 0); `candidates: 2 exact-equal: 0` |
| 3 | `taskA_ratio_audit_k29.txt` | 114817 ratios, `TOTAL missing over k=29..29: 0` |
| 4 | `rig_margin_k29.txt`; `rig_margin_exact_k29_shard0.txt` … `shard3.txt` | `TOTAL pairs=114817 failures=0 undecided=0`; shards 28705 + 3 × 28704 pairs, each `failures=0 undecided=0` |
| 5 | `deep_rig_shard0.txt` … `deep_rig_shard3.txt`, `shard_sums.txt` | product_solutions=0 in every shard; 114817 ratios, 3332527 enumerated pairs, 3288852 window candidates |

| object file | sha256 |
|---|---|
| object/PROOF.md | 264abd2c67286ea32fdde54b1b01e2a956b4ac9891ee229f22665e0dec71e132 |
| object/deep_cf.py | dc74be2f2b68c5618437b9b972f7313621ab556360a33e7e784e5f0dc82e6b85 |
| object/deep_rig.py | 0e7d7d72f04e5076827c28afb1184f5ef3eb69c3a4be965a6c2e770cd6ad0341 |
| object/out/deep_rig_shard0.txt | 16d004a8fbc4c02a18632d810473477365fe4322ff562a52d232d6b6fde54bb2 |
| object/out/deep_rig_shard1.txt | ea444f3b10fb9644e063d07e5e1776b69c075a8b3f066aeef78925e8b1ac9ad3 |
| object/out/deep_rig_shard2.txt | d4c408d9325673bd569968dbfa52482e74b7730cb8b1c10c8d4a57c31f8d528d |
| object/out/deep_rig_shard3.txt | 2b934a233485b48358426687c4d83ed27294e687dc66514450dcad69a3511f6c |
| object/out/rig_margin_exact_k29_shard0.txt | 3ae46f90bea6ff22af7c187f60087ded72fb639725f32475b2faa98acdb1134f |
| object/out/rig_margin_exact_k29_shard1.txt | dbcc144740517c9d70aff8314397caf3ffdbb399f77093054edae2b09bc6d42a |
| object/out/rig_margin_exact_k29_shard2.txt | 76a602a97802e934107dd58bc7b1314fa1ddf710e82e55f8ce0df18f4715f5d0 |
| object/out/rig_margin_exact_k29_shard3.txt | d8fdc7fd7ca6f3c39205ae2b6fb7f08eb7b05fce1ab87138a1a547687fd9bd68 |
| object/out/rig_margin_k29.txt | 8ecc84c9c7461f3c9ed2246f131521be39834f9e38abc5eb059bacac0c316cca |
| object/out/search_N1.1e6.txt | e41f6bebc56bb287037b8e3c87cd94dab8a8fbc5d485531431caa01b216942c9 |
| object/out/shard_sums.txt | f81b126fdfd1253ad357ddd7a3a1177e5ac6a88495485cac073ee4c6dbece59d |
| object/out/taskA_ratio_audit_k29.txt | 3ee4a7fbd54db58fd87bb96526b263ce1538e81fe46a8125d1667f1ac050a036 |
| object/out/verify_N1.1e6.txt | cdb23f4c10d1207dd2507068a65d0f96449a52252d433ef7d6c9ae13d7626e2a |
| object/out/wrap_test/wrap_test_shard0.txt | f0d021f34e154b1a98a61ebc2eb5e0d664911ee38ca55c97ded660da9dd7f4aa |
| object/out/wrap_test/wrap_test_shard0of1.txt | 793653b458a14638b1746cc134ecc06a93988dd97875c02fcf37b34264c6ea4f |
| object/out/wrap_test/wrap_test_shard1.txt | fefd512694b19ea167a63b5e539d840571f450f87c757579f7bac30b8e873f34 |
| object/out/wrap_test/wrap_test_shard2.txt | baa9ac34033a4948e453e8ae542e3c0befd3cb9597c3308979871423c401fc29 |
| object/out/wrap_test/wrap_test_unsharded.txt | 25c3ccbbc23d1f635c43c0046497ea0d57db3c449765c33cfdfbe715639fc127 |
| object/rig_margin.py | 3d1b50ab5f638def5d0dea18099a701c263d80caf8a4e1e3ea8db2dcde924e76 |
| object/rig_margin_exact.py | 64328c1f47d3ef88418e8e77b462f6b70ea2aa3438e6249e1194b52e96d3f12b |
| object/search677b.c | d9c01611ba8e1fa5fff4a54c1c08b7a1d44689707fc98e8d60dfd054e460caa9 |
| object/shard_margin.py | f41ce5409fe3f5983beda160a6ff135d8a6f9857ae171ddf617315c3c8303cf3 |
| object/shard_rig.py | 41cdb740e45b1b9fd7ed219be63cfcc8f1916a3f1924d6522568287b1a90d130 |
| object/sum_shards.py | bebff93f5e06f9cf019ae79cf7b41ccb7dfc8879631d05a5c62aac0e1c521642 |
| object/taskA_ratio_audit_k.py | ce6fa546045e398f00b5fd1980e74a04c5d59ffecea547fe25d7384f900871e5 |
| object/verify_cands.py | 5e848cf39dd1b793e12a20cc3fae8ea8c2422e904e840ba0e29bb9ac418154d8 |

All 29 are byte-identical copies of the claim the panel read (the claim text is `how-we-built-it/claim/CLAIM.md`).

## Check it yourself

```sh
PY=python3 sh verify-it-yourself/run_checks.sh     # from this folder; PY must have gmpy2, mpmath and numpy
```

Expected last line: `PASS`. By default it checks the object hashes and the saved outputs, then reruns step 2, step 3
(ratio audit) and step 4 with interval arithmetic on the whole ratio list, comparing each output with the saved one
(times stripped): PASS in 342 s on the contributor's 4-core machine (`verify-it-yourself/RECEIPTS.md`). `--all` also reruns the 4 exact-margin shards and
the 4 enumeration shards (about 2.5 hours on 4 cores). Details: `RUN_IT_YOURSELF.md`.

The script checks the computation. It cannot check the hand proof (Lemma A, the Step 4 reduction and the completeness
argument of the enumeration, `object/PROOF.md`, to be read), and a rerun reproduces, but does not prove correct, the
float64 pre-filters and 1090-digit non-interval arithmetic inside `deep_rig.py`.

## Compared to

| source | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| Justin Sun Prize catalog, JSP-000550 (status source) | Current status / Lean proof | Open / No; no partial result recorded | https://raw.githubusercontent.com/TheJustinSunPrize/awards/main/problems/catalog-0501-0600.md | 2026-11-10T09:20:41Z (HTTP 200, sha256 78ecc0e2a46520944d1b2f07196bd945433e82e4788a32585f22604c6b8b7834) |
| erdosproblems.com, problem 677 | recorded results | Thue–Siegel finiteness for each fixed k; Proof claims (0) | https://www.erdosproblems.com/677 | 2026-11-10T09:20:41Z (HTTP 200, sha256 bcafdf8fd4deee80f97ec3cf82d6c70d8a768c64d0bf062c7426882f53990e4c) |
| laaielichter/erdos-677 (GitHub, 2026-10-27) | k = 29 | no solution with m + k ≤ 10^8 | https://github.com/laaielichter/erdos-677 | read by the NOVELTY skeptic, 2026-11-10 |

Snapshot and the other searches: `the-record-we-beat/STATUS_RECORD.md` and `panel/novelty.md`.

## Not claimed

- Not a solution of Erdős Problem 677, and not a prize solution (the Justin Sun Prize accepts only complete
  solutions). The problem remains open.
- Not kernel-checked. The proof is informal (`object/PROOF.md`); no Lean proof of the range statement exists.
- The float64 pre-filters and the 1090-digit non-interval arithmetic in the enumeration are supported by error
  analysis and reruns, not formally proved (`panel/criterion.md`).
- Only k = 29. k ≤ 28 are the separate packages 2026-10-24-adb991-201bcc74 and 2026-11-07-adb991-b461c702; nothing for
  k ≥ 30.
- The panel recorded small text issues that do not affect the computation: PROOF.md Step 5 item 4 says the
  admissible s form "an interval" where they can form two pieces (the code handles both); deep_rig.py's docstring says
  1050 digits (the code uses 1090); the enumeration outputs do not print η or the digit count (`panel/criterion.md`,
  `panel/reproduce.md`).
- No pull request, issue or message was sent to anyone by the runs.

## Credits

- Paul Erdős, who posed the problem (Erdős Problem 677; [Er79], [Er79d], [ErGr80] on the problem page).
- T. F. Bloom's Erdős Problems website, https://www.erdosproblems.com/677 (statement, recorded results, forum).
- The Justin Sun Prize catalog, entry JSP-000550, https://github.com/TheJustinSunPrize/awards (the status source).
- google-deepmind/formal-conjectures, https://github.com/google-deepmind/formal-conjectures
  (`FormalConjectures/ErdosProblems/677.lean`, the formal statement `Erdos677.erdos_677` and `lcmInterval`).
- S. Chan, arXiv:2408.01306 (Period. Math. Hung. 2025), Theorem 1, which settles k = 3.
- V3R1T4S, https://github.com/elder-plinius/V3R1T4S (the run protocol, panel and gate).
- Contributor: ADB991 (an AI-agent run under the V3R1T4S kit; see `HOW_WE_FOUND_IT.md` and `prompt/`).
