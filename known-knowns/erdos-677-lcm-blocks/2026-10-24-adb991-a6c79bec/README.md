# Erdős Problem 677 (Justin Sun Prize JSP-000550): no counterexample with 0 ≤ n ≤ 5871·k, every k ≥ 1, every m ≥ n + k

Target: `erdos-677-lcm-blocks` (Erdős Problem 677 = Justin Sun Prize catalog entry JSP-000550; a charter quarry, not
a bank target). Family folder in the repo: `known-knowns/erdos-677-lcm-blocks/`. Submission id:
`2026-10-24-adb991-a6c79bec` (the first 8 hex digits of the sha256 of `object/PROOF.md`, the proof that the claim
names as its object). Status: `CONFIRMED_PARTIAL` (`panel/gate.md`, round 2, 2026-10-24). Run: 2026-10-15-0724.

## What

confirmed_scope: Computer-assisted and relying on the cited explicit prime bounds of Rosser–Schoenfeld 1962 (ψ(x) < 1.03883·x for all x > 0) and Schoenfeld 1976 (a prime in (x, x(1 + 1/16597)) for every x > 2010759.9), object/PROOF.md together with the reproduced run of object/range_nCk.py 5871 shows that lcm(m+1, …, m+k) ≠ lcm(n+1, …, n+k) for every k ≥ 1, every n with 0 ≤ n ≤ 5871·k and every m ≥ n + k with no cap on m, i.e. every instance of Erdos677.erdos_677 with n ≤ 5871·k holds — an informal, not kernel-checked result that meets the first enumerated partial win and is not a solution of the problem.

In plain words: write M(n, k) = lcm(n+1, …, n+k). Erdős asked whether two disjoint blocks of k consecutive integers
always have different least common multiples, i.e. M(m, k) ≠ M(n, k) whenever m ≥ n + k (formal statement:
google-deepmind/formal-conjectures `Erdos677.erdos_677`, copied in `how-we-built-it/claim/checker/spec_677.lean`).
This package settles every instance with n ≤ 5871·k, for every block length k and every later block, however far
away. It is a partial result; the problem stays open.

How it works (`object/PROOF.md`): in a counterexample every element of the later block divides M(n, k), so the later
block contains no prime and its prime powers are at most n + k (S0); comparing products and lcms gives
m + k ≤ c_k·(n + k) with c_k < 2.8260 by Rosser–Schoenfeld (S1); with n ≤ 5871·k, Schoenfeld's prime-in-short-interval
theorem then forces m ≤ 2010759 (S2), which leaves finitely many prime-free blocks (k ≤ 147). `object/range_nCk.py 5871`
enumerates all of them and compares the lcms exactly (S3). Its saved output, `object/out/range_nCk_C5871.txt`:

| quantity | value |
|---|---|
| primes up to 2100000 | 155805 |
| prime-free (m, k) pairs examined | 1449175 (max k 147) |
| candidate N after pinning; exact lcm comparisons | 7567449; 7567420 |
| counterexamples found (n, m, k) | [] |
| last line | `RESULT: no counterexample with n <= 5871 k` |

| object file | sha256 |
|---|---|
| object/PROOF.md | a6c79becb3858a3d64648aa138040aa7f8411f1c98af00787e85c5b8f2312210 |
| object/range_nCk.py | b83f0f45f0324da37bbe56575555560cdc7317fc04df92253a74c80a9a291824 |
| object/out/range_nCk_C5871.txt | 84b1d82fb5d2474686c60663817c5fb49709d7372987c4e044157aac61008d14 |

All three are byte-identical copies of the claim the panel read (`how-we-built-it/claim/CLAIM.md`).

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh      # from this folder; needs python3 (standard library) and sha256sum or shasum
```

Expected last line: `PASS`. It checks the object hashes, reruns `python3 -I object/range_nCk.py 5871` (at
`nice -n 10`), compares the output byte for byte with `object/out/range_nCk_C5871.txt`, and runs the exact judge
`verify-it-yourself/check677.py` on the two known near-misses (both rejected: the lcms differ). One core, about
0.2 GB of memory; 142 s on the contributor's 4-core machine while other jobs were running
(`verify-it-yourself/RECEIPTS.md`, which also shows two corrupted copies being rejected). Details: `RUN_IT_YOURSELF.md`.

The script checks the computation. It cannot check the two cited theorems; the argument that makes the enumeration
complete is `object/PROOF.md`, to be read.

## Compared to

| source | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| Justin Sun Prize catalog, JSP-000550 (status source) | Current status / Lean proof | Open / No; no partial result recorded | https://raw.githubusercontent.com/TheJustinSunPrize/awards/main/problems/catalog-0501-0600.md | 2026-10-24T08:26:00Z (HTTP 200, sha256 78ecc0e2a46520944d1b2f07196bd945433e82e4788a32585f22604c6b8b7834) |
| erdosproblems.com, problem 677 | recorded results for the equal-length question | only Thue–Siegel finiteness for each fixed k; no range verification; 0 proof claims | https://www.erdosproblems.com/677 | 2026-10-24T08:26:00Z (HTTP 200, sha256 c2ed64f6d85f1b970b18641c50d69fb9c4c70b917d2cd3b44dd098a317b0ef19) |

No prior range verification was found, so the "record" is the absence of any recorded range: the round-2 NOVELTY
skeptic (`panel/novelty.md`) read the catalog, the problem page, its history, proof claims and forum, the site's data
file, the forum-linked Lean repository, the AI-contributions wiki, all V3R1T4S and prize-repository pull-request
heads and arXiv (2024-10 to 2026-10), and found no range of the form n ≤ C·k, no explicit range with m uncapped, and
no solution. Snapshot, quoted lines and hashes: `the-record-we-beat/STATUS_RECORD.md`.

## Not claimed

- Not a solution of Erdős Problem 677, and not a prize solution: the Justin Sun Prize accepts only complete
  solutions. The problem remains open.
- Not kernel-checked. The proof is informal (`object/PROOF.md`); no Lean proof of the range statement exists.
- It depends on two cited explicit prime bounds, Rosser–Schoenfeld (1962), ψ(x) < 1.03883·x for x > 0, and
  Schoenfeld (1976), a prime in (x, x(1 + 1/16597)) for x > 2010759.9. The panel checked both numerically within
  reach (max ψ(n)/n for n ≤ 10^8 is 1.0388206 at n = 113; the Schoenfeld property holds on (2010759.9, 10^9)) but
  could not re-read the papers (proxy 403).
- For k ≥ 148 the result is purely analytic (S1 plus Schoenfeld 1976); the computation covers only k ≤ 147.
- For k ≤ 147 the range n ≤ 5871·k (at most n ≤ 863037) lies inside an unpanelled lens computation of the same run
  (signature-search: no counterexample with n + k ≤ 10^8). That lens result is not part of this claim and is not
  claimed here; the computation in this package adds nothing to it in that range.
- The constant 5871 is the natural endpoint of the classical method (Schoenfeld's 16597 caps it), not a new idea;
  the CRITERION skeptic called it a modest result in the regime where the problem is structurally easy.
- Other results of the run (k ≤ 4 via Thue equations, n ≤ 10^5 for every k, larger ranges for small k) are not
  panelled and not bundled here.
- No pull request, issue or message was sent to anyone.

## Credits

- Paul Erdős, who posed the problem (Erdős Problem 677; [Er79], [Er79d] on the problem page).
- T. F. Bloom's Erdős Problems website, https://www.erdosproblems.com/677 (statement, recorded results, forum).
- The Justin Sun Prize catalog, entry JSP-000550, https://github.com/TheJustinSunPrize/awards (the status source).
- google-deepmind/formal-conjectures, https://github.com/google-deepmind/formal-conjectures
  (`FormalConjectures/ErdosProblems/677.lean`, the formal statement `Erdos677.erdos_677` and `lcmInterval`).
- J. B. Rosser and L. Schoenfeld, "Approximate formulas for some functions of prime numbers", Illinois J. Math. 6
  (1962), 64–94.
- L. Schoenfeld, "Sharper bounds for the Chebyshev functions θ(x) and ψ(x). II", Math. Comp. 30 (1976), 337–360.
- V3R1T4S, https://github.com/elder-plinius/V3R1T4S (the run protocol, panel and gate).
- Contributor: ADB991 (an AI-agent run under the V3R1T4S kit; see `HOW_WE_FOUND_IT.md` and `prompt/`).
