# Erdős Problem 677 (Justin Sun Prize JSP-000550): no counterexample with 1 ≤ k ≤ 25, 0 ≤ n ≤ 10^494, every m ≥ n + k

Target: `erdos-677-lcm-blocks` (Erdős Problem 677 = Justin Sun Prize catalog entry JSP-000550; a charter quarry, not
a bank target). Family folder in the repo: `known-knowns/erdos-677-lcm-blocks/`. Submission id:
`2026-10-24-adb991-201bcc74` (the first 8 hex digits of the sha256 of `object/PROOF.md`, the proof that the claim
names as its object). Status: `CONFIRMED_PARTIAL` (`panel/gate.md`, read by the run's main session at
2026-10-24T11:52:08Z). Run: 2026-10-24-0818. A separate package of the same family, `2026-10-24-adb991-a6c79bec`
(run 2026-10-15-0724, "n ≤ 5871·k for every k"), is a different range; neither contains the other (`panel/novelty.md`,
section 4).

## What

confirmed_scope: For every 1 ≤ k ≤ 25, every 0 ≤ n ≤ 10^494 and every m ≥ n + k (no cap on m), lcm(m+1..m+k) ≠ lcm(n+1..n+k), as a computer-assisted, not kernel-checked result. It rests on a hand proof of Lemma A, an exact hash-plus-verification search for n + k ≤ 1.1·10^6, a margin proved in exact rational interval arithmetic for X ≥ 10^6, and a continued-fraction enumeration to q ≤ 10^495 with exact final tests. That enumeration uses float64 pre-filters and 1090-digit non-interval arithmetic, whose correctness is supported by error analysis and an independent exact cross-check on 123 sampled curves but not formally proved.

In plain words: write M(n, k) = lcm(n+1, …, n+k). Erdős asked whether two disjoint blocks of k consecutive integers
always have different least common multiples, i.e. M(m, k) ≠ M(n, k) whenever m ≥ n + k (formal statement:
google-deepmind/formal-conjectures `Erdos677.erdos_677`, copied in `how-we-built-it/claim/checker/spec_677.lean`).
This package settles every instance with block length k ≤ 25 and first block starting at n ≤ 10^494, against every
later block, however far away. It is a partial result; the problem stays open. Of the range, k ≤ 2 is elementary and
k = 3 was already settled for all n (S. Chan, arXiv:2408.01306, Theorem 1), so the new content is 4 ≤ k ≤ 25
(`the-record-we-beat/STATUS_RECORD.md`).

How it works (`object/PROOF.md`, Steps 1–5):
1. **Lemma A** (hand proof): if M(n, k) = M(m, k) with n < m, then f(m)/f(n) = r for f(x) = (x+1)…(x+k), where r is
   one of a finite set A_k of ratios of small primes with 1 < r ≤ lcm(1..k)/k. Hence k ≤ 2 is impossible,
   m + k ≤ (n+k)·R(k)^{1/k}, and the later block contains no prime.
2. **Small X** (n + k ≤ 1.1·10^6, every k): `object/search677b.c` lists every candidate pair through a hash of the
   (≥ k)-prime part (complete in m by Lemma A; collisions only add candidates); `object/verify_cands.py` compares
   each candidate's lcms exactly.
3. **The ratio set**: `object/deep_cf.py` (`admissible_r`) lists A_k; `object/taskA_ratio_audit.py` regenerates it
   independently and checks it against every equal-lcm pair with n < m ≤ 3000.
4. **Margin** for every real X ≥ 10^6 and every r ∈ A_k, k ≤ 25: c(1 − 10^−3) < X(ρX − Y) < c(1 + 10^−3), proved by
   `object/rig_margin_exact.py` (exact rational intervals) and `object/rig_margin.py` (interval arithmetic).
5. **Enumeration**: `object/deep_rig.py` lists every (p, q) with q ≤ 10^495 inside that window, through the
   continued fraction of ρ = r^{1/k}, and tests each candidate in exact integers.

The saved outputs in `object/out/`:

| step | output | result |
|---|---|---|
| 2 | `search_N1.1e6.txt`, `verify_N1.1e6.txt` | `# COMPLETE kmin=3 kmax=147 total_candidates=2`; `candidates: 2 exact-equal: 0` (the near-misses (k, n, m) = (3, 4, 13) and (4, 18, 53)) |
| 3 | `taskA_ratio_audit_NB3000.txt` | `TOTAL missing over k=3..25: 0`; 970 equal-lcm pairs with n < m ≤ 3000, r outside the sets: 0 |
| 4 | `rig_margin_k3-25_X1e6_eta1e-3.txt`, `rig_margin_exact_k3-25_X1e6_eta1e-3.txt` | both `TOTAL pairs=63041 failures=0 undecided=0` |
| 5 | `deep_rig_final_k3-18_d1040.txt`, `…k19-22…`, `…k23-23…`, `…k24-24…`, `…k25-25…` | `product_solutions=0` for every k = 3..25; 1,174,616 window candidates in all (42649 + 248311 + 314109 + 202516 + 367031) |

| object file | sha256 |
|---|---|
| object/PROOF.md | 201bcc74dfe80bd57d43eb3f97330d8dc702623df9808c6ebc00f27b21b01e83 |
| object/deep_cf.py | dc74be2f2b68c5618437b9b972f7313621ab556360a33e7e784e5f0dc82e6b85 |
| object/deep_rig.py | 0e7d7d72f04e5076827c28afb1184f5ef3eb69c3a4be965a6c2e770cd6ad0341 |
| object/rig_margin.py | 3d1b50ab5f638def5d0dea18099a701c263d80caf8a4e1e3ea8db2dcde924e76 |
| object/rig_margin_exact.py | 64328c1f47d3ef88418e8e77b462f6b70ea2aa3438e6249e1194b52e96d3f12b |
| object/search677b.c | d9c01611ba8e1fa5fff4a54c1c08b7a1d44689707fc98e8d60dfd054e460caa9 |
| object/taskA_ratio_audit.py | 1b520c69a4ba5c757a8efd540284527f7bd99dfd9dc0bc0de44ceff9ea4ee152 |
| object/verify_cands.py | 5e848cf39dd1b793e12a20cc3fae8ea8c2422e904e840ba0e29bb9ac418154d8 |
| object/out/deep_rig_final_k3-18_d1040.txt | b77f25bee478df026ea2d1aa128cf436a44ce0e0f81df8994f41ff5674548f6f |
| object/out/deep_rig_final_k19-22_d1040.txt | 2dbf20009051900358a3c77eb2ad221c8b877a065f97c75e5c3d795e33bcc4e9 |
| object/out/deep_rig_final_k23-23_d1040.txt | 03c6fb85078e5c6db93311814685693f94af87d0ff556a246e3205694ab58ec3 |
| object/out/deep_rig_final_k24-24_d1040.txt | b508f922dc4f197bdb9af0b463ae1a7f3e3127c54161f3c90fda8897607c39e3 |
| object/out/deep_rig_final_k25-25_d1040.txt | 8e66ec2f182ba8bd9691520368726fe4b9ede8f2d97fc64923255ea7fcee4554 |
| object/out/rig_margin_k3-25_X1e6_eta1e-3.txt | a22430cbe811f6d31bc4a5dafe9a34dd3192993812ff83b28b50a12d1a4a1511 |
| object/out/rig_margin_exact_k3-25_X1e6_eta1e-3.txt | f1c60d38cbf1ca40895d596abac0bb17e3445a277cbeaeb56df877eb79201819 |
| object/out/search_N1.1e6.txt | ce706f1126bfe0531ada631fdb98b3ef3897273f2409f9f1c8ed1a181036d38f |
| object/out/search_N1.1e6.log | ff9851d66ae0c5a8169d75b39f9c6ea863e6fbb7e83b9d4a9c98623e7089fb31 |
| object/out/taskA_ratio_audit_NB3000.txt | 2d57206bc9fd3d038e1843f80a9fb9a2c7e62e5631339df718beff620e3faa46 |
| object/out/verify_N1.1e6.txt | 23cf2e6066042259d2f128d7c74c29e07b95cb7f5e29e85a32f25352b997818f |

All 19 are byte-identical copies of the claim the panel read (`runs/2026-10-24-0818/claim/object/` in the
contributor's workspace; the claim text is `how-we-built-it/claim/CLAIM.md`).

## Check it yourself

```sh
PY=python3 sh verify-it-yourself/run_checks.sh     # from this folder; PY must have gmpy2, mpmath and numpy
```

Expected last line: `PASS`. By default it checks the 19 object hashes and the saved outputs, then reruns step 2
(search677b and verify_cands.py, plus the exact judge on the two near-misses), step 3 (taskA_ratio_audit.py 3000),
step 4 with interval arithmetic (rig_margin.py) and step 5 for k = 3..16, comparing each output with the saved one
(times stripped). Three parallel jobs at `nice -n 10`, about 1 GB of memory each; 164 s on the contributor's
4-core machine (`verify-it-yourself/RECEIPTS.md`, which also shows two corrupted copies being rejected).
`sh verify-it-yourself/run_checks.sh --all` also reruns step 5 for k = 17..25 (the five commands of
`how-we-built-it/claim/REPRODUCE.md`) and the exact-rational margin checker: PASS in 5179 s (about 86 minutes) with 3
jobs on the same machine, also in `RECEIPTS.md`. Details: `RUN_IT_YOURSELF.md`.

The script checks the computation. It cannot check the hand proof (Lemma A and the completeness argument of the
enumeration, `object/PROOF.md`, to be read), and a rerun reproduces, but does not prove correct, the float64
pre-filters and 1090-digit non-interval arithmetic inside `deep_rig.py`.

## Compared to

| source | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| Justin Sun Prize catalog, JSP-000550 (status source) | Current status / Lean proof | Open / No; no partial result recorded | https://raw.githubusercontent.com/TheJustinSunPrize/awards/main/problems/catalog-0501-0600.md | 2026-10-24T10:28:17Z (HTTP 200, sha256 78ecc0e2a46520944d1b2f07196bd945433e82e4788a32585f22604c6b8b7834) |
| erdosproblems.com, problem 677 | recorded results for the equal-length question | only Thue–Siegel finiteness for each fixed k; Proof claims (0) | https://www.erdosproblems.com/677 | 2026-10-24T10:28:17Z (HTTP 200, sha256 3d947ff293f44167b4a0a2a30dc9fa1882b04b520bca4a98ee5db40c5a22737f) |
| S. Chan, arXiv:2408.01306v2, Theorem 1 | k = 3 | settled for all n | https://export.arxiv.org/pdf/2408.01306v2 | 2026-10-24T10:43:47Z (HTTP 200, sha256 7d124d867eb77eb8397a448a9185beb4c3ae2183a6a256f91d5cfb57fac5e407) |

Previously known coverage, as read by this run's NOVELTY skeptic (`panel/novelty.md`): k ≤ 2 trivial; k = 3 for all
n (Chan, Theorem 1); for 4 ≤ k only finite searches, the largest recorded being about n, m ≤ 2·10^5 (k ≤ 12) and
n < m ≤ 1.5·10^5 (k ≤ 150, per a third-party audit of a 2026 paper the skeptic could not read). This package covers
4 ≤ k ≤ 25 for every n ≤ 10^494 with m uncapped. Snapshot, quoted lines and hashes:
`the-record-we-beat/STATUS_RECORD.md`.

## Not claimed

- Not a solution of Erdős Problem 677, and not a prize solution: the Justin Sun Prize accepts only complete
  solutions. The problem remains open.
- Not kernel-checked. The proof is informal (`object/PROOF.md`); no Lean proof of the range statement exists.
- The float64 pre-filters and the 1090-digit non-interval arithmetic in the enumeration (`object/deep_rig.py`) are
  supported by error analysis (the CRITERION and REPRODUCE skeptics) and cross-checks (an independent exact-integer
  enumerator on 123 sampled curves; validate mode against brute force for q ≤ 4000, k = 3..18), not formally proved.
- k ≤ 3 is already known: k ≤ 2 is elementary, and k = 3 for all n is Chan, arXiv:2408.01306, Theorem 1. The new
  content is 4 ≤ k ≤ 25. The NOVELTY skeptic could not read Danesh–Bianchetti (IJMTT 72(9), 2026; proxy 403); a
  third-party audit says it leaves k = 6 open, so at most it would narrow the new content to 6 ≤ k ≤ 25
  (`panel/gate.md`, "Hedging").
- The extension of the all-k window search to n + k ≤ 2·10^8 (lens extender-r1 of the same run) is a separate,
  unpanelled lens result and is not part of this claim.
- `object/deep_rig.py` was patched during the run: its double-precision pre-filter could drop a valid pair when
  float cancellation hit tiny convergent ratios, and the patched code computes that quantity from the exact integer
  where it matters. Every enumeration output here comes from the patched code; for k = 3..18 the per-k counts equal
  those of the unpatched code (`how-we-built-it/PATCH_NOTE.md`).
- Other results of the workspace (the separate "n ≤ 5871·k" package, k = 3 and 4 via Thue equations) are not bundled
  here.
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
