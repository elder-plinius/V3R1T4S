# Shorter superpermutations for n=7 (below 5905) or n=8 (below 46188)

📊 **Record tables** · harvest (many cells or partial wins within reach) · tractability ★★☆☆☆ · compute: laptop-hours · open as of 2026-10-20

## The problem

Find a string over {1..n} containing all n! permutations as contiguous substrings that is shorter than the best known. For n=7 the record is 5905 (Teodorescu, 17 Aug 2026); the lower bound is 5884, and Lean-checked lower bounds of 5898 (group thread, Aug 2026) and 5899 (Jakub Halfar, 8 Oct 2026) have been posted to the superpermutators group. For n=8 it is 46188 (superpermutators/superperm PR #56 by rumstd, merged 2026-10-01). For n=9 it is 408947 (Theo H., posted to the group 2026-10-01) and for n=10 it is 4034855 (Jay Pantone, posted 2026-10-06, improving 4034873); n=11..14 words have also been posted (n=12: 522,737,174 on 2026-10-19).

## What counts as a win

Success means a string over the alphabet {1..n} (n in 7..10) in which all n! permutations occur as length-n substrings, verified exhaustively, whose length is STRICTLY SMALLER (direction: min) than the best length at verification time on https://en.wikipedia.org/wiki/Superpermutation and the superpermutators group (context on 2026-10-20: 5905 for n=7, 46188 for n=8, 408947 for n=9, 4034855 for n=10). For n=7 the length must also be >= 5884; anything shorter means a bug.

## Partial wins

- **p1:** A superpermutation for n in 11..13, verified exhaustively, strictly shorter than the live record for that n (context: Raudvere 43,948,807 / 522,910,088 / 6,749,568,009, but an n=12 word of 522,737,174 was posted to the group on 2026-10-19; re-check the group).
- **p2:** A lower bound for n=7 strictly above 5899 (the Lean-checked bound posted 2026-10-08), delivered as a re-runnable computer-assisted proof (exact ILP or exhaustive search with certificate) that the skeptic re-executes, after confirming no stronger lower bound is published.

## How a win is checked

Slide a window of length n and add each window that is a permutation (n distinct symbols) to a set. Assert the set size is n!, the alphabet is exactly {1..n}, and the length is below the record. For n=10 the string is ~4M characters, which is trivial to check.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://groups.google.com/g/superpermutators>

## Sources

- <https://groups.google.com/g/superpermutators>
- <https://github.com/superpermutators/superperm>
- <https://www.gregegan.net/SCIENCE/Superpermutations/Superpermutations.html>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- For n=8, apply the Egan/Houston kernel method with the newer 2026 tricks Raudvere used. Search palindromic kernels of higher weight and use the 2-cycle graph cover with a cheaper ATSP solve (LKH via pip 'lkh' or elkai) on the 7!-node 'cycle graph'.
- Treat it as ATSP on the permutation graph with edge weights 1..n and use an exact or near-exact solver on reduced quotient graphs (by symmetry). For n=7, solve on the 5040-node graph with elkai/LKH and many restarts, exploiting symmetry to restrict the search.
- Lift a better n=7 solution through the Williams/Egan-style constructions to n=8 and beyond, which gives cascading improvements.
- Look for a structural insight in Teodorescu's 5905: identify which 'weight-3 or weight-4 edges' it saves and generalize.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Counting a window with repeated symbols as a permutation.
- Alphabet/length off-by-one.
- The n=7 record changed in Aug 2026 and n=8 in Jul 2026. Always re-check the superpermutators group.
- Raudvere's n=11-13 lengths (43,948,807; 522,910,088; 6,749,568,009) are also live baselines if one lifts constructions upward.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/record-tables/superpermutations-n7-n8.md
```

Already set up? Say `run V3R1T4S on superpermutations-n7-n8`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `superpermutations-n7-n8`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
