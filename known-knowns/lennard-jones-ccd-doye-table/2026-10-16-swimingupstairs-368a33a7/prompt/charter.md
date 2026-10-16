# Research charter v1 (2026-10-15)

## Thesis
An interest in how physical systems settle (energy minima, flow, packing) meets an interest in how memory orders and retains information. The edge is patience and physical intuition: let one machine relax particle systems night after night, and treat "sequences that must contain everything without repeating" as memory problems. Quarries pair energy-landscape records with ordering/sequence records, plus one wild cellular-automaton bet.

## Quarries
1. id: thomson-problem-live-tables — Lower the best known Coulomb energy of N points on a sphere for some listed N. Shape: record. Defined: bank entry thomson-problem-live-tables (status_source deetour.net/oppp/thomson/). Status first: live table values. Why us: physical relaxation intuition plus nightly basin-hopping patience. Weight 5. Wild: no.
2. id: lennard-jones-ccd-doye-table — Lower a putative global minimum in the Cambridge Cluster Database LJ tables. Shape: record. Defined: bank entry lennard-jones-ccd-doye-table. Status first: Doye/CCD LJ pages. Why us: same settling intuition, different potential. Weight 4. Wild: no.
3. id: packomania-scu-spheres-in-cube — Beat a per-N record radius for equal spheres in a cube. Shape: record. Defined: bank entry packomania-scu-spheres-in-cube. Status first: packomania scu radius.txt. Why us: packing as a physical "jamming" process. Weight 3. Wild: no.
4. id: superpermutations-n7-n8 — Shorter superpermutation for n=7 (<5905) or n=8 (<46204). Shape: record. Defined: bank entry superpermutations-n7-n8. Status first: superpermutators group / literature. Why us: a pure "remember every arrangement" memory object. Weight 3. Wild: no.
5. id: labs-merit-factor-records — Lower energy (higher merit factor) ±1 sequence for some length 67..600. Shape: record. Defined: bank entry labs-merit-factor-records. Status first: arXiv 2607.09688 table. Why us: a spin-glass energy landscape — physics methods in a combinatorial setting. Weight 3. Wild: no.
6. id: snake-coil-in-the-box — Longer snake or coil in Q_n, 9<=n<=13. Shape: record. Defined: bank entry snake-coil-in-the-box. Status first: minortriad.com/snake. Why us: a path that must never revisit its own neighbourhood — a self-avoiding memory trace. Weight 2. Wild: no.
7. id: langton-ant-highway — Finite configuration with machine-checkable proof the ant never builds a highway. Shape: counterexample. Defined: bank entry langton-ant-highway. Status first: arXiv 2505.05426. Why us: emergent order from a memoryless rule. Weight 1. Wild: yes.

## Lenses
- relaxer: Physical annealing. You treat every object as a particle system: gradient descent from many random/perturbed starts, basin-hopping, warm start from the table's best. Dead when 10^4 basins from the best structure find nothing lower. Skeptic: no.
- swimmer: Far-import from fluid dynamics. You add "drag"/damped dynamics (FIRE, momentum with friction) and flow-like collective moves instead of single-point moves. Dead when it only reproduces known minima across 3 seeds. Skeptic: no.
- archivist: Object-as-data (method card). You load the best known object and hunt regularities (symmetry, layering, repeated motifs) its authors did not exploit, then build a structured family. Dead when the family's best is above record at all tested sizes. Skeptic: no.
- evaluator-first: You spend the first hour on an exact, fast evaluator (exact integer energy, mpmath verification), then brute-scale. Dead when throughput cannot plausibly cover the space in a week of nights. Skeptic: no.
- contrarian: You try to show the quarry is already settled: newer arXiv records, ties, table errata. Dead (for the quarry) when the record has moved beyond reach. Skeptic: yes.

## Scout voice
Read like a coach watching tape: what changed recently, where the frontier is stale, which N or length has the fewest recent attackers.

## Attacker voice
Patient and physical: perturb, let it settle, keep the best, repeat for hours; small clean improvements over grand ones.

## Heuristics
- Prefer N or lengths where the table has not moved in years.
- Warm-start from the best known object; random starts second.
- Exploit symmetry, then break it deliberately.
- Verify every candidate at high precision before believing it.
- A tie is never a record.

## Kill criteria
- Record moved past reach on the live table.
- Improvement only below verification precision.
- Search cost exceeds a week of nights with no trend.
- Object reproduces a known structure exactly.

## Self-critique
Energy-minimum tables are crowded with strong optimisers; "physical intuition" may add nothing over standard basin-hopping. The memory/consciousness framing is metaphor, not a method, and can tempt drift toward unverifiable work.

## Method cards used
object-as-data, far-import, evaluator-first (chosen, not randomly drawn).
