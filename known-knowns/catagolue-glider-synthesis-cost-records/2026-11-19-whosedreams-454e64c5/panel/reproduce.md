# REPRODUCE skeptic: xs31_g8e1ugmmzd553w643

context: subagent

## Scope
I read the claim package (object/xs31_g8e1ugmmzd553w643.rle, SHA256SUMS, how-we-built-it/TARGET_CRITERION.md, README.md, INDEX.csv, the-record-we-beat/RECORD.md, RUN_IT_YOURSELF.md, verify-it-yourself/RECEIPTS.md and OBJECT_SHA256). I did not read verify-it-yourself/life_check.py, how-we-built-it/code/, or any lifelib/Shinjuku helper. I did not re-fetch the live Catagolue cost; that belongs to NOVELTY.

## Claim under test
object/xs31_g8e1ugmmzd553w643.rle is a 14-glider B3/S23 synthesis of the still life xs31_g8e1ugmmzd553w643.

## Definition quoted (how-we-built-it/TARGET_CRITERION.md, success criterion)
"Success means an RLE pattern in rule B3/S23 that (1) at generation 0 consists ONLY of gliders, each a separate connected component, (2) is a valid synthesis: rewinding every glider backwards by at least 4*(bounding box diameter) generations along its own trajectory produces a pattern with no glider-glider interaction during the rewound interval (so the gliders genuinely come in from infinity), (3) after running forward until the population is periodic, contains exactly the target object (apgcode match, via lifelib or an independent simulator) with NO other live cells and no escaping gliders or spaceships (unless the page's own synthesis convention for that object explicitly allows outgoing gliders, in which case follow it literally), and (4) uses STRICTLY fewer gliders than the cost shown for that apgcode on its Catagolue object page and tabulation ..., re-fetched live immediately before claiming."

Partial win p1: "A strictly cheaper true glider synthesis for any object whose current listed cost is at least 60 gliders, verified as above."

Properties (1) to (3) and the glider count are REPRODUCE's job. Property (4) and the p1 cost threshold need a live cost, so NOVELTY and CRITERION decide those.

## Method: my own checker, written from the definition
I wrote an independent pure-Python B3/S23 simulator (infinite grid, live cells as an unbounded set: no torus, no clipping). It does not use lifelib. It has its own RLE parser and its own apgcode encoder/decoder, following the LifeWiki "apgcode" page: extended Wechsler over the 8 dihedral orientations, shortest suffix, then lexicographically smallest. The encoder was checked, before this claim was run, by round-tripping known still lifes (block xs4_33, tub xs4_252, beehive xs6_696, pond xs8_6996, boat xs5_253, loaf xs7_2596, the LifeWiki example xs31_0ca178b96z69d1d96) and both claimed target codes.

- (1) Generation-0 gliders only: the parser reads the RLE and splits it into 8-connected components. A component is a glider only if it has 5 cells and, evolved alone, keeps population 5 and after 4 generations is the same shape translated by (±1, ±1). That velocity is the heading.
- Toward the reaction: each glider was flown alone and in the full pattern; the first generation at which its solo cells are no longer a subset of the full pattern is its first interaction. The glider must be moving toward that site (positive dot product of velocity with the displacement to its last intact position) and must be consumed before the pattern becomes periodic. Distance to the final still-life centroid was also required to decrease over the first 4 generations. (Distance to the generation-0 centroid of all gliders is not this test: far inbound gliders can pull that centroid off the construction site.)
- (2) Rewind: "bounding box diameter" is ambiguous, so I used two values of T, both already multiples of 4: 4 times the longer inclusive side, and 4 times the ceiled Euclidean diagonal of the inclusive bounding box. Every glider was translated backward along its own trajectory (phase preserved when T is a multiple of 4). The combined rewound pattern was then simulated for T generations. At every generation it had to equal the union of the gliders evolved separately. After T generations it had to equal generation 0 exactly.
- (3) Forward: I simulated until a cell set repeated exactly, with no translation, and encoded that pattern with my own apgcode encoder. I also decoded the claimed target and required a D8-plus-translation match, period 1, and population equal to the target, so no debris remains.
- SHA256: sha256 of the object RLE bytes was compared to the SHA256SUMS entry for that path.
- Determinism: a second parse-and-evolve to the recorded stabilization generation produced the same cell set.

## Results (18 November 2026, 7:43 PM ET, America/New_York)
- Rule header: B3/S23. Generation-0 population 70, header 903 × 721, inclusive bounding box 903 × 721 (cells (0,0) to (902,720)), ceiled diagonal 1156.
- SHA256 of object/xs31_g8e1ugmmzd553w643.rle is 454e64c5bf7e7b17ab5db6edb0ca6e4b35dd77f88f5233ec179b36c99169748a, equal to the SHA256SUMS entry.
- (1) 14 eight-connected components, sizes all 5, all 14 are gliders (14 × 5 = 70 cells). Velocities in min-(y,x) component order: (1,1), (1,1), (1,1), (-1,1), (1,1), (1,1), (-1,1), (-1,-1), (1,-1), (1,-1), (-1,-1), (-1,-1), (-1,-1), (1,-1). Count matches the claim of 14.
- Toward the reaction: first-interaction generations 1058, 552, 546, 64, 71, 67, 34, 33, 546, 1058, 1062, 1772, 1794, 1794. Every path-dot is positive; every glider's distance to the still-life centroid (452.90, 260.23) decreases over 4 generations; the last consumption is at generation 1794, before stabilization.
- (2) Rewind T=3612 (4 × 903) and T=4624 (4 × 1156): no mismatch generation, both recovered generation 0 exactly.
- (3) Exact repeat from generation 1819, period 1, population 31. Encoded apgcode xs31_g8e1ugmmzd553w643, matching the target by both encoding and D8-plus-translation geometry. No other live cells.
- Determinism: second forward run to generation 1819 agreed.

## Limitations
Assigned scope is numerical verification of properties (1)–(3) and the claimed glider count. The package-stated table cost of 60 was not re-fetched and is not judged here. I did not run the author's checker.

The pattern is a 14-glider all-glider synthesis of xs31_g8e1ugmmzd553w643. Properties (1)–(3) hold.

pass: true
