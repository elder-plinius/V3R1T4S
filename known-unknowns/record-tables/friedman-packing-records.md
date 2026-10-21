# Erich Friedman Packing Center: beat a listed packing

📊 **Record tables** · harvest (many cells or partial wins within reach) · tractability ★★☆☆☆ · compute: laptop-hours · open as of 2026-10-20

## The problem

Friedman's Packing Center lists best known packings of n congruent shapes (circles, squares, triangles, pentagons, hexagons, octagons and others) into containers of various shapes. Mostly the goal is the smallest container for n unit shapes, or the largest shapes for a unit container. Several pages were updated in Sep-Oct 2026, including AI-team records (Numaro, Jul 2026, unequal-circle total-radius records) and new proofs (Vu-Le, Sep 2026). Submissions are by email, with sizes to 5 decimals; extensions of existing categories are accepted up to n=50. 92 of the 121 category stamps on the index are dated October 2026 (27 of them 10/20/26), so multiple agents sweep the pages daily; re-fetch the specific category page on the day of any claim. Submission is by email, which is an outbound message on the human's behalf and requires explicit permission from the human.

## What counts as a win

Success means explicit placements (centers plus rotation angles) for n shapes that meet all of the following. (1) Pairwise interiors are disjoint and every shape lies inside the container, certified rigorously by interval arithmetic or exact rational/algebraic computation. (2) The objective is STRICTLY BETTER, in the page's own direction (smaller container, or larger shape/total radius), than the value on the specific live Friedman page re-fetched immediately before verification, by at least 1e-5 at Friedman's 5-decimal precision. (3) The category and n are listed on the page, or n <= 50 for an extension of an existing category. The claim is for the verified construction; emailing Friedman needs explicit permission from the human.

## Partial wins

- **p1:** A Packomania record: a circles-in-square or circles-in-circle packing, rigorously certified, whose objective strictly beats the live Packomania value for that n at its listed precision.
- **p2:** An EinsteinArena sum-of-radii record: a circle packing for one of the EinsteinArena AlphaEvolve-style sum-of-radii problems, with containment and non-overlap certified in interval or exact arithmetic, whose exactly computed score strictly beats the live arena leaderboard best.

## How a win is checked

Use an independent checker. Represent polygons by exact vertices after applying the rotation with rational approximations to cos/sin, or bound them with interval arithmetic. Test pairwise overlap with the separating axis theorem in interval arithmetic, requiring positive separation or exact touching certified. Check containment of every vertex (and for circles, the center distance to each container edge >= r). Compute the objective and compare with the page value.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://erich-friedman.github.io/packing/>

## Sources

- <https://erich-friedman.github.io/packing/>
- <https://erich-friedman.github.io/packing/submit.html>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Avoid circles-in-squares and circles-in-circles (Packomania-saturated). Target odd shape/container pairs (pentagons in triangles, octagons in squares, triangles in pentagons) where the record is an old hand construction.
- Use penalty-method optimization with a contracting container (minimize container scale plus a squared overlap penalty from SAT-based penetration depth), with L-BFGS and random restarts across 10 cores.
- Use a 'jamming plus rattler removal' pipeline: compress a random packing (Lubachevsky-Stillinger event-driven for circles, a rigid-body MD analogue for polygons), then optimize the rotation angles.
- Transfer lattice cuts. Cut good periodic packings of the shape with the container and locally repair boundary pieces.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Comparing in the wrong direction. Some pages minimize container side, others maximize total radius or perimeter.
- Numerical 'touching' that is actually a tiny overlap. Require rigorous certification.
- Circle packing pages are heavily optimized already. The AlphaEvolve sum-of-radii benchmarks are separate EinsteinArena problems.
- Pages are being updated daily (Sep 30 - Oct 3 2026), so re-fetch the specific page immediately before claiming.
- Submitting to Friedman is an email on the human's behalf and needs explicit permission. Claim the verified construction, not the submission.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/record-tables/friedman-packing-records.md
```

Already set up? Say `run V3R1T4S on friedman-packing-records`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `friedman-packing-records`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
