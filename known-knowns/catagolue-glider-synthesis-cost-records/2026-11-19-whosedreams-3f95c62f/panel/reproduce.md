# REPRODUCE skeptic: xs27_08e1ugmicz651346

context: subagent

## Scope
I read the claim package (object/xs27_08e1ugmicz651346.rle, SHA256SUMS, how-we-built-it/TARGET_CRITERION.md, README.md, INDEX.csv, the-record-we-beat/RECORD.md, RUN_IT_YOURSELF.md, verify-it-yourself/RECEIPTS.md and OBJECT_SHA256). I did not read verify-it-yourself/life_check.py, how-we-built-it/code/, or any lifelib/Shinjuku helper. I did not re-fetch the live Catagolue cost; that belongs to NOVELTY.

## Claim under test
object/xs27_08e1ugmicz651346.rle is a 29-glider B3/S23 synthesis of the still life xs27_08e1ugmicz651346.

## Definition quoted (how-we-built-it/TARGET_CRITERION.md, success criterion)
"Success means an RLE pattern in rule B3/S23 that (1) at generation 0 consists ONLY of gliders, each a separate connected component, (2) is a valid synthesis: rewinding every glider backwards by at least 4*(bounding box diameter) generations along its own trajectory produces a pattern with no glider-glider interaction during the rewound interval (so the gliders genuinely come in from infinity), (3) after running forward until the population is periodic, contains exactly the target object (apgcode match, via lifelib or an independent simulator) with NO other live cells and no escaping gliders or spaceships (unless the page's own synthesis convention for that object explicitly allows outgoing gliders, in which case follow it literally), and (4) uses STRICTLY fewer gliders than the cost shown for that apgcode on its Catagolue object page and tabulation ..., re-fetched live immediately before claiming."

Partial win p1: "A strictly cheaper true glider synthesis for any object whose current listed cost is at least 60 gliders, verified as above."

Properties (1) to (3) and the glider count are REPRODUCE's job. Property (4) and the p1 cost threshold need a live cost, so NOVELTY and CRITERION decide those.

## Method: my own checker, written from the definition
I wrote an independent pure-Python B3/S23 simulator (infinite grid, live cells as an unbounded set: no torus, no clipping). It does not use lifelib, life_check.py or verify_synthesis.py. It has its own RLE parser and its own apgcode encoder/decoder, following the LifeWiki "apgcode" page: the pattern is split into five-row strips in extended Wechsler format, with 'z' separating strips; the eight dihedral orientations are tried, and the shortest suffix wins, then the lexicographically smallest. The encoder was checked, before any claim was run, by round-tripping known still lifes (block xs4_33, tub xs4_252, boat xs5_253, beehive xs6_696, loaf xs7_2596, pond xs8_6996, the LifeWiki example xs31_0ca178b96z69d1d96) and all four claimed target codes in this panel; each decoded to a period-1 still life of the advertised population and re-encoded to the same string.

- (1) Generation-0 gliders only: the parser reads the RLE and splits it into 8-connected components. A component is a glider only if it has 5 cells and, evolved alone, keeps population 5 and after 4 generations is the same shape translated by (±1, ±1). That displacement is the heading.
- Toward the reaction: each glider was flown alone and in the full pattern; the first generation at which its solo cells are no longer a subset of the full pattern is its first interaction. The glider must be moving toward that site (positive dot product of the period-4 velocity with the displacement to its last intact position) and must be consumed before the pattern becomes periodic. Distance to the final still-life centroid was recorded over the first 4 generations as a sanity check; it is not a criterion test, and it is not meaningful once a glider has already interacted.
- (2) Rewind: "bounding box diameter" is ambiguous, so I used two values of T, both already multiples of 4: 4 times the longer inclusive side, and 4 times the ceiled Euclidean diagonal of the inclusive bounding box. Every glider was translated backward along its own trajectory (phase preserved when T is a multiple of 4). The combined rewound pattern was then simulated for T generations. At every generation it had to equal the union of the gliders evolved separately. After T generations it had to equal generation 0 exactly.
- (3) Forward: I simulated until a cell set repeated exactly, with no translation, and encoded that pattern with my own apgcode encoder. I also decoded the claimed target and required a D8-plus-translation match, period 1, and population equal to the target, so no debris remains.
- SHA256: sha256 of the object RLE bytes was compared to the SHA256SUMS entry for that path.
- Determinism: a second parse-and-evolve to the recorded stabilization generation produced the same cell set.

## Results (19 November 2026, 10:36 AM ET, America/Coral_Harbour)
- Rule header: B3/S23. Generation-0 population 145, header 1230 × 977, inclusive bounding box 1230 × 977 (cells (0,0) to (1229,976)), ceiled diagonal 1571.
- SHA256 of object/xs27_08e1ugmicz651346.rle is 3f95c62fd56e7ab048352da6b254ffa92e0f031bfac03bd07c09e3723776eae6, equal to the SHA256SUMS entry.
- (1) 29 eight-connected components, sizes all 5, all 29 are gliders (29 × 5 = 145 cells). Velocities in min-(y,x) component order: (1,1), (1,1), (1,1), (-1,1), (-1,1), (1,1), (-1,1), (-1,1), (1,1), (-1,1), (-1,1), (-1,1), (1,1), (1,1), (-1,1), (-1,1), (1,1), (-1,1), (1,1), (-1,1), (1,1), (-1,1), (-1,1), (-1,1), (1,-1), (1,-1), (1,-1), (-1,-1), (1,-1). Count matches the claim of 29.
- Toward the reaction: first-interaction generations 2806, 2089, 2082, 2082, 1572, 1569, 1570, 1073, 1073, 1076, 1082, 1069, 1058, 574, 574, 583, 583, 546, 546, 555, 66, 54, 61, 34, 34, 582, 1058, 1070, 1078. Every path-dot is positive; the last consumption is at generation 2806, before stabilization. Distance to the still-life centroid (708.19, 705.26) decreased over 4 generations for every glider that had not already interacted in that window.
- (2) Rewind T=4920 (4 × 1230) and T=6284 (4 × 1571): no mismatch generation, both recovered generation 0 exactly.
- (3) Exact repeat from generation 2810, period 1, population 27. Encoded apgcode xs27_08e1ugmicz651346, matching the target by both encoding and D8-plus-translation geometry. No other live cells.
- Determinism: second forward run to generation 2810 agreed.

## Limitations
Assigned scope is numerical verification of properties (1)–(3) and the claimed glider count. The package-stated table cost of 62 was not re-fetched and is not judged here. I did not run the author's checker.

The pattern is a 29-glider all-glider synthesis of xs27_08e1ugmicz651346. Properties (1)–(3) hold.

pass: true
