# Still-life counts in other Life-like rules: any unpublished term of A175000 (HighLife), A166476 (2x2), A175001 (Move) or A175002 (Maze)

🕸️ **Graphs, games and automata** · harvest (many cells or partial wins within reach) · tractability ★★★★☆ · compute: laptop-hours · open as of 2026-11-09

## The problem

OEIS lists the number of strict still lifes with n live cells, up to rotation and reflection, for several Life-like rules. Christian Schroeder (2010) and Nathaniel Johnston (2009) computed short initial runs, and Joel Cruz Cabrera extended them in November 2026. On 2026-11-09 the live entries reach HighLife B36/S23 (A175000) a(16) = 2872, 2x2 B36/S125 (A166476) a(11) = 322, Move/Morley B368/S245 (A175001) a(17) = 376 and Maze B3/S12345 (A175002) a(9) = 669, and a pending OEIS draft adds Maze a(10) = 2938. Strict means the pattern is stable under the rule and its 8-connected islands cannot be grouped into two or more still lifes of that rule (the convention that reproduces these OEIS entries and Life's A019473). Pseudo still lifes are excluded. HighLife and Life share S23, so a HighLife still life is a Life still life in which no dead cell has exactly 6 live neighbours. Strictness must still be re-decided under the HighLife rule.

## What counts as a win

A new exact term of any of the four sequences: any a(n) that is not yet published at claim time, in the live OEIS entry, in a pending OEIS draft (oeis.org/draft/A...) or on LifeWiki. On 2026-11-09 the first such terms are A175000(17), A166476(12), A175001(18) and A175002(11). It must come from two independent enumerators that agree. Each must reproduce every published term of that sequence, draft terms included, and one must be a general Life-like-rule enumerator, not a filter of a Life still-life list. Report the objects as RLE or apgcodes so a skeptic can re-check stability and strictness one by one.

## Partial wins

- **p1:** Any one new term as above (each unpublished term counts once).

## How a win is checked

Re-step every reported object under the stated rule with an independent stepper (lifelib supports arbitrary outer-totalistic rules) and check stability. Check strictness by testing every grouping of the pattern's 8-connected islands into two or more still-life parts (or with Cook's skew-symmetric-graph method adapted to the rule). Canonicalise under the 8 symmetries and count. Compare small n with OEIS.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://oeis.org/A175000>

## Sources

- <https://oeis.org/A175000>
- <https://oeis.org/A166476>
- <https://oeis.org/A175001>
- <https://oeis.org/A175002>

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Strictness depends on the rule. A Life-strict object can be pseudo in another rule, and the reverse.
- Births can only happen in the one-cell ring around the pattern (no rule here has B0), but that ring must be checked under the rule's own birth set: B6 and B8 kill many Life still lifes in HighLife, 2x2 and Move.
- LifeWiki pages for these rules (Cloudflare-blocked here) may already list longer counts. A term already published there is a re-derivation, not a new result, so check before claiming.
- Strictness is decided over whole 8-connected islands, not arbitrary subsets of cells. Splitting arbitrary cells makes the Life long barge (two tubs) pseudo and gives A019473(8) = 8 instead of 9. Calibrate on Life A019473 before trusting any count.
- A strict still life is connected at Chebyshev distance 2, and no rule here has S0, so every island has at least 2 cells. Its bounding box therefore has width and height at most n + floor(n/2) - 1, a cheap proved bound for bounding-box enumerators.
- These counts move fast: all four sequences were extended or drafted between 6 and 8 November 2026. Check the OEIS draft page (oeis.org/draft/A...) and history as well as the approved entry, at the start and again just before claiming. A term in a pending draft is already published.
- LifeWiki and the ConwayLife forums answer automated fetches with a Cloudflare challenge, so they need a human check. OCA:Maze (last edited 2026-10-21) lists Maze counts for 1 to 9 cells only.
- Many strict Maze still lifes have two or more islands, so filtering polyplets (connected patterns) is not an enumerator for Maze.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/graphs-games-automata/lifelike-rules-still-life-counts.md
```

Already set up? Say `run V3R1T4S on lifelike-rules-still-life-counts`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `lifelike-rules-still-life-counts`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
