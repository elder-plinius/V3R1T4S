# Covering designs C(v,k,t): beat a repository entry

📊 **Record tables** · harvest (many cells or partial wins within reach) · tractability ★★★☆☆ · compute: laptop-hours · open as of 2026-10-20

## The problem

A (v,k,t) covering design is a collection of k-subsets (blocks) of a v-set such that every t-subset lies in at least one block. C(v,k,t) is the minimum number of blocks. The repository tables list the best known upper bounds for v <= 99, k <= 25, t <= 8 (the live LJCR page states its limit as v <= 100, k <= 25, t <= 8). A design with fewer blocks than the current table entry for any listed (v,k,t) is a new record that can be submitted directly. The dmgordo/LJCR GitHub repository states it is the permanent data location for the La Jolla Covering Repository (the old website is going away), but its covering data file was last committed 2022-12-19; the live LJCR page is https://dmgordon.org/covering-designs/ (site last updated 2026-09-03), which points to coveringrepository.com for more recent improvements, and Zenodo v1.1 (2026-04-08) is a snapshot. coveringrepository.com imported Gordon's data through March 2026 and also hosts lottery-wheel (v,k,t,m) tables. Hobbyist repositories may hold claimed records not yet merged into any table. Example: the TheEslabonGroup/covering-designs README (formerly thebrockchain/covering-designs, which now redirects there; DOI 10.5281/zenodo.21834602) claims C(28,13,4) <= 53 (7 Aug 2026; LJCR data: 54, Fadlaoui 2008) and C(32,13,4) <= 95 (8 Aug 2026; LJCR data: 96, Fadlaoui 2009). The README says Dan Gordon checked the (28,13,4) design with his own code; this was not confirmed on dmgordon.org on 2026-10-03, and coveringrepository.com, which now loads with plain curl (2026-10-20), was not searched for these two parameter sets (its latest-improvements page shows only the newest ~100 entries). Both are hobbyist claims. On 2026-10-18 their block files (records/C28_13_4_53blocks.txt, records/C32_13_4_95blocks.txt) were checked exhaustively: 53 and 95 distinct 13-subsets that cover all 20475 and 35960 4-subsets.

## What counts as a win

Success means b blocks, each a k-subset of a v-set (no repeated points), covering every t-subset (checked exhaustively), where b is STRICTLY SMALLER (direction: min) than EVERY one of the following, each re-fetched at verification time: the live coveringrepository.com plain (v,k,t) value (m=t section, https://coveringrepository.com/), the live LJCR value (https://dmgordon.org/covering-designs/), and the dmgordo/LJCR GitHub/Zenodo value. It must also beat any value found by grepping GitHub/arXiv for that (v,k,t) over the last 6 months, including unverified hobbyist claims (e.g. TheEslabonGroup/covering-designs: C(28,13,4) <= 53, C(32,13,4) <= 95). If a live table cannot be fetched, the claim is 'PENDING TABLE CHECK', not a record. Parameters must be within v <= 99, k <= 25, t <= 8, and b must be at least the Schonheim bound L(v,k,t); going below it means a bug. Same-day claim only if C(v,t) <= 5e9, so the exhaustive coverage check runs on a laptop; larger cases are logged as 'PENDING chunked exhaustive check' and claimed only after that full check completes.

## Partial wins

- **p1:** A lottery-design record: an explicit (v,k,t,m) lottery covering (every m-subset of the v-set meets some block in at least t points, checked exhaustively) with strictly fewer blocks than the live coveringrepository.com lottery-table value for those parameters and any value found on GitHub/arXiv for them.
- **p2:** A new exact lower bound: a certified proof that C(v,k,t) is strictly larger than both the Schonheim bound and every lower bound listed for that cell in the live repositories or literature, for some in-range (v,k,t), delivered as a re-checkable certificate (a DRAT proof checked with drat-trim, or an exact ILP infeasibility certificate re-verified by an independent solver).

## How a win is checked

The verifier writes an independent checker. Parse blocks, assert each has exactly k distinct elements in range, and enumerate all t-subsets (or use a bitmask coverage array indexed by combinadic rank) to confirm each is covered. Compute the Schonheim bound recursively. Fetch the live values from coveringrepository.com, dmgordon.org/covering-designs and the LJCR GitHub/Zenodo data, and grep GitHub/arXiv for recent claims on the same (v,k,t). Claim only if b is below every one of those values, C(v,t) <= 5e9 (otherwise PENDING), and the solver's file hash matches the checked file. For huge C(v,t) (above 1e9), use a streaming check over blocks with a bitset of t-subsets and chunk it if memory is tight.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://coveringrepository.com/>

## Sources

- <https://coveringrepository.com/>
- <https://github.com/dmgordo/LJCR>
- <https://zenodo.org/records/19472830>
- <https://github.com/TheEslabonGroup/covering-designs>
- <https://dmgordon.org/covering-designs/>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Look for soft entries first. Scrape the table for (v,k,t) whose record comes from old generic methods (greedy, 'combining', Turan-type constructions) or that have not changed in 15+ years, especially large k with t=4..5. The Aug 2026 wins were exactly (28,13,4) and (32,13,4).
- Use automorphism prescription. Fix a group G (cyclic Z_v, Z_{v-1} plus a fixed point, PSL(2,q), AGL(1,q)), so the design is a union of G-orbits of k-sets. Solve the orbit set-cover exactly with OR-Tools CP-SAT or an ILP (pip install ortools). This is the Kramer-Mesner trick applied to coverings.
- Use Nurmela-Ostergard simulated annealing with incremental uncovered-t-set counts, started from the current record minus one block, so the search is to repair a small number of uncovered t-sets.
- Use recursive constructions with fresh ingredients. A new record at (v,k,t) often propagates to (v+1,k,t), (v,k+1,t) and so on through standard combining constructions. After any single win, sweep its neighbors.
- Use a lottery-wheel style local search: swap one element of one block and accept if uncovered count does not increase (tabu). This is cheap and parallelizes over 10 cores with different seeds.
- Auditor note: AI/hobbyist sweeps began in Aug 2026, so prioritise cells whose record is old and not near the (28,13,4)/(32,13,4) neighbourhood that has just been picked over.
- Simulated annealing or tabu search over block sets, with the cost equal to the number of uncovered t-sets and incremental delta updates (Nurmela-Östergård style). Target triples where the LJCR value has the largest ratio to the Schönheim bound.
- Prescribed automorphism groups: require the design to be a union of orbits under Z_v, Z_{v-1}+fixed point, PSL(2,q) or AGL(1,q). The search becomes a small set-cover over orbits, which can be solved exactly with OR-tools CP-SAT (pip install ortools).
- Recursive constructions: combine record coverings for (v1,k1,t1) and (v2,k2,t2) through the standard C(v1+v2,k,t) <= sum over i of C(v1,k1,i)*C(v2,k-k1,t-i)-type product constructions. Scan all splits of every table entry automatically. The 2026 improvements at large v suggest these are under-explored.
- FunSearch/AlphaEvolve-style loop: have an LLM write construction programs (for example, greedy covering with learned priority functions over finite-field structure), score them by block count, and evolve the programs.
- Take a record design and do local surgery: delete 1-3 blocks, then repair the uncovered t-sets with an exact ILP over all k-sets that cover at least one of them.
- Before searching, merge LJCR and coveringrepository.com into one live-min table and rank entries by ratio to the Schoenheim bound; only target entries where both sources agree on the value (no recent Acerbi improvement).

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Comparing against a stale table. The live LJCR page is https://dmgordon.org/covering-designs/ (updated 2026-09-03); the dmgordo/LJCR GitHub data (last commit 2022-12-19) and Zenodo v1.1 (2026-04-08) are snapshots; the old ljcr.dmgordo.org host did not respond on 2026-10-03; coveringrepository.com has newer improvements. Check all of them.
- Off-by-one: the table's v counts points, so check the point labeling (0- vs 1-based) and that no block repeats a point.
- Parameters outside the repository's listed range do not count as a record.
- Coverings with multiplicity (lambda > 1) or (v,k,t,m) lottery coverings are different tables, so do not mix them up.
- coveringrepository.com mixes lottery (v,k,t,m) coverings with plain (v,k,t) designs, so read the right table.
- Independent hobbyist repos (e.g. thebrockchain) may hold claimed records not yet merged into any table. Treat them as values to beat, even when unverified.
- The table may have been updated after the searcher last read it. Always re-fetch it.
- Confusing covering designs with packing designs, or with lotto designs C(v,k,t,m).
- Off-by-one errors in v when points are 1-indexed.
- Duplicate blocks inflate the apparent coverage but not the count. Count unique blocks.
- A result below the Schönheim bound means the checker is wrong, not that the search succeeded.
- LJCR is no longer the most up-to-date source; coveringrepository.com has newer improvements. Beating only LJCR is not a record.
- coveringrepository.com also hosts lotto (v,k,t,m) designs. Make sure the comparison uses the (v,k,t) section with m=t.
- Lottery-wheel hobbyists optimize the small-v entries intensely. Expect wins only at large v, k and t, where verification is costly.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/record-tables/covering-designs-record.md
```

Already set up? Say `run V3R1T4S on covering-designs-record`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `covering-designs-record`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
