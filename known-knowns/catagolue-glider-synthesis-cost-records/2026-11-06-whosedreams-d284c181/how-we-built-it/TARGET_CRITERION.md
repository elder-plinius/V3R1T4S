# Game of Life: a cheaper glider synthesis than Catagolue's best-known cost for a still life or oscillator

🕸️ **Graphs, games and automata** · harvest (many cells or partial wins within reach) · tractability ★★★☆☆ · compute: laptop-hours · open as of 2026-10-28

## The problem

A glider synthesis builds a Game of Life (B3/S23) object by colliding gliders only; its cost is the number of gliders. Catagolue's Syntheses section (Adam P. Goucher's Catagolue, assembled from Jeremy Tan's Shinjuku database of synthesis components with contributions from Mark Niemiec, Martin Grant, Goldtiger997 and many others) lists the cheapest known synthesis cost for every synthesised object. Coverage includes every strict still life up to 22 cells (the xs22 tabulation lists 680,289 objects) and a partial set of larger still lifes: the xs24 tabulation lists 118,117 objects, far fewer than the roughly 4.05 million strict 24-cell still lifes (OEIS A019473). The most expensive xs24 entry, xs24_03lozg5u05b8oz11, costs 167 gliders (true synthesis) as of 2026-10-28. Oscillators are listed by period (xp2, xp3, ...). The tables are recomputed every four hours as new components arrive. Many costs are far above what the component library could achieve with a smarter assembly. Open target: a valid all-glider synthesis of some tabulated object that uses STRICTLY fewer gliders than the live listed cost, or a first synthesis of a still life/oscillator the tables do not list.

## What counts as a win

Success means an RLE pattern in rule B3/S23 that (1) at generation 0 consists ONLY of gliders, each a separate connected component, (2) is a valid synthesis: rewinding every glider backwards by at least 4*(bounding box diameter) generations along its own trajectory produces a pattern with no glider-glider interaction during the rewound interval (so the gliders genuinely come in from infinity), (3) after running forward until the population is periodic, contains exactly the target object (apgcode match, via lifelib or an independent simulator) with NO other live cells and no escaping gliders or spaceships (unless the page's own synthesis convention for that object explicitly allows outgoing gliders, in which case follow it literally), and (4) uses STRICTLY fewer gliders than the cost shown for that apgcode on its Catagolue object page and tabulation (https://catagolue.hatsya.com/census/b3s23/synthesis-costs/<class>), re-fetched live immediately before claiming. For objects listed with a '(pseudo)' cost, compare against that listed number but report the result as a true synthesis improvement only if the new synthesis is all-glider. A first synthesis of a strict still life or oscillator absent from the tables also counts if its apgcode does not appear on the tabulation page for its class.

## Partial wins

- **p1:** A strictly cheaper true glider synthesis for any object whose current listed cost is at least 60 gliders, verified as above.
- **p2:** A strictly cheaper synthesis for an oscillator class page (xpN) object, verified with the same checker, including a check that the final object oscillates with the listed period.
- **p3:** A reusable new synthesis component (a converter from an object with a known synthesis to another object, at a stated glider cost) that, combined with existing listed costs, lowers the cost of at least 10 distinct tabulated objects, each re-verified end-to-end as a full all-glider synthesis.

## How a win is checked

Install python-lifelib (Adam P. Goucher). Load the claimed RLE, decompose generation 0 into connected components and confirm every component is a glider (apgcode xq4_153 in some phase/orientation). Rewind each glider independently along its direction and check by forward simulation that the rewound pattern evolves into the generation-0 pattern unchanged (no early interaction). Run forward until periodic, classify with lifelib's apgcode function, and confirm the result is the single target object with nothing else. Count gliders. Fetch the object page https://catagolue.hatsya.com/object/<apgcode>/b3s23 and read the '#CSYNTH <apgcode> costs N gliders' line. Cross-check with an independent numpy Life simulator.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://catagolue.hatsya.com/syntheses>

## Sources

- <https://catagolue.hatsya.com/syntheses>
- <https://catagolue.hatsya.com/census/b3s23/synthesis-costs>
- <https://catagolue.hatsya.com/textcensus/b3s23/synthesis-costs/xs24>
- <https://gitlab.com/parclytaxel/Shinjuku>
- <https://gitlab.com/apgoucher/lifelib>
- <https://pypi.org/project/python-lifelib/>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Shortest-path view: treat Shinjuku components as weighted edges between apgcodes and run Dijkstra from the empty board; any object whose shortest path is cheaper than its listed cost is an immediate candidate (the published tables are a running min, not always a global shortest path after new components arrive).
- Target the most expensive objects first (xs24 ranks 1-50 cost 90-167 gliders): look for a cheaper predecessor still life that differs by one 'tail' or 'hook' and a known cheap converter.
- Import from organic chemistry retrosynthesis: run a retrosynthetic search (Corey-style disconnections, Monte Carlo tree search as in AiZynthFinder) from the target backwards to cheap 'reagent' objects, where each reaction is a Shinjuku component.
- Import from compiler peephole superoptimisation: exhaustively enumerate 2- and 3-glider collisions against small objects near the target's frontier cells (a bounded 'superoptimiser' over glider phases and lanes) to discover new one-step converters.
- Soup mining: Catagolue's census of random soups contains natural formations of many objects; search the census for small 'seed' constellations (2-4 still lifes) that evolve into the target, then synthesise the seed cheaply.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- A pattern that contains anything other than gliders at generation 0 (a block, a boat, a stray cell) is not a glider synthesis, even if it builds the object.
- Gliders that already overlap or interact when rewound are an impossible 'from infinity' setup; skipping the rewind check gives false records.
- Leftover debris, a stray blinker, or an escaping glider means the target was not built cleanly; the final apgcode must match exactly.
- The CSV textcensus encodes costs with an offset: values of 10^17 or more are true syntheses with cost value-10^17, smaller values are '(pseudo)' costs. Read the object page's #CSYNTH line instead of the raw CSV number.
- Costs drop often as people submit new components. A cost that was beatable yesterday may already be lower; re-fetch the object page immediately before claiming.
- Pseudo still lifes and strict still lifes are different classes; a synthesis of a pseudo still life is not a synthesis of a strict one with the same cell count.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/graphs-games-automata/catagolue-glider-synthesis-cost-records.md
```

Already set up? Say `run V3R1T4S on catagolue-glider-synthesis-cost-records`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `catagolue-glider-synthesis-cost-records`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
