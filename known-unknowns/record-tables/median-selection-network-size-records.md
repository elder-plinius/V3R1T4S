# Median selection networks: reduce a current comparator count for 10–25 inputs

📊 **Record tables** · harvest (many cells or partial wins within reach) · tractability ★★★★☆ · compute: laptop-hours to laptop-days for evolutionary search or SAT-assisted local replacement; exhaustive zero-one verification at n≤25 fits laptop memory and minutes to hours · open as of 2026-10-25

## The problem

Bert Dobbelaere’s maintained List of median selection networks gives explicit size/depth trade-offs. On 2026-10-25 (page updated that day), the least listed comparator counts for n=10 through 25 are respectively 22,25,29,32,38,41,46,49,55,58,63,66,74,77,82,85. These are construction records, not proofs of optimality. Its history lists updates through 2026-10-25 (that day: smaller networks for 46 to 49 and 61 inputs, and minor improvements for sizes between 22 and 54) and credits Mason Hemmer and Touko Ursin. Re-read the page on the day of any claim. For odd n one designated output is the middle order statistic. For even n two designated outputs are the two middle order statistics, possibly unordered. The page also describes reductions from networks with nearby input sizes. Median selection differs from full sorting and adaptive comparison selection.

## What counts as a win

For any listed n, give an input-independent sequence of compare-exchange pairs, output positions, and an exact correctness certificate, using strictly fewer comparators than the listed minimum for that n. A comparator replaces its ordered pair of wires by (min,max). For even n return the two middle input values as an unordered pair; averaging is outside the network. Count every comparator including any added at the outputs. Depth is reported but unconstrained. Also strictly improve the best comparable published result at claim time, including compatible compositions of published objects. State whether the candidate is a composition and identify its components. Values in unmerged pull requests do not set the bar.

## How a win is checked

Check pair indices and count comparators, then evaluate every binary input in {0,1}^n using packed bitsets or batches. For odd n the selected bit must be 1 iff the input contains at least (n+1)/2 ones. For even n compare the sorted selected pair with binary order statistics n/2 and n/2+1. The threshold principle for comparator circuits extends this exhaustive binary check to all totally ordered inputs, including ties. A SAT UNSAT certificate for a violating input is an alternative, provided the encoding is independently reconstructed and the proof checked.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://bertdobbelaere.github.io/median_networks.html>

## Sources

- <https://bertdobbelaere.github.io/median_networks.html>
- <https://github.com/bertdobbelaere/SorterHunter>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Delete or reroute comparators in the recent records and use counterexamples to repair the network.
- Seed from nearby input sizes using the table’s documented trimming and central-pair constructions.
- Resynthesize a small suffix exactly while freezing the prefix; verify the resulting whole network.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Count comparator elements, not the separate min/max subcomponent cost.
- For even n the middle two outputs may be unordered; averaging is outside the network.
- Random testing is not a correctness certificate.
- Nearby-size constructions are part of the comparison bar.
- The upstream full sorting-network target shares SorterHunter, but asks a different question.
- The page is actively improved, including AI-assisted contributions in October 2026 for n >= 25; re-read it the day of any claim.
- Negative-run exclusion (2026-10-31): every single-comparator deletion across 82 minimum-size published/direct/recursive networks for 10 <= n <= 25 (with every output-wire choice, 4,999 cases) fails, and every 1- or 2-position directed comparator replacement around two 37-comparator n = 14 near-misses (666 position-pair cores, 21.8M proposals) plus 479 bounded SAT window-resynthesis instances is UNSAT; radius-1 and radius-2 local edits do not suffice at n = 14.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/record-tables/median-selection-network-size-records.md
```

Already set up? Say `run V3R1T4S on median-selection-network-size-records`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `median-selection-network-size-records`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
