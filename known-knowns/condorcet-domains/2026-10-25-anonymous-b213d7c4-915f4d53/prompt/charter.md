# Research charter v1 (2026-10-17)

## Thesis

Practical software evaluation, visual experimentation, and careful reading of evidence suggest an approach: make small mathematical constructions inspectable, identify their exact failure cases, then repair them. Seek compact objects with cheap exact checks and useful intermediate structure. Prefer one fully checked improvement to a broad story. Treat this as a hypothesis about research fit, rather than evidence of specialist mathematical expertise.

## Quarries

All definitions below refer to V3R1T4S contributors, *Target bank* (2026), `bank/targets.json` at revision `04fdfba48c6e277fe083b6811f1a5deb3c52b74e`. These are proposed questions, with current openness and comparison values still to be established. The cited entry's full success criterion defines each objective.

### sorting-network-size-records

- Question: Can an explicit comparator network on 13–32 channels improve the current size, depth, or size/depth frontier while sorting every binary input?
- Shape: record construction.
- Where defined: Target bank entry `sorting-network-size-records`; Bert Dobbelaere, *Sorting networks: extended list*, https://bertdobbelaere.github.io/sorting_networks_extended.html.
- Status to confirm first: current frontier, proven lower bounds, and newer constructions; the additional comparison required by the bank for 16 channels.
- Why this approach: failures are explicit input vectors. Their shared structure can guide local repairs; tiny networks provide exact calibration before larger searches. Begin at a channel count whose exhaustive validation fits the available time.
- Weight: 4.
- Wild: no.

### covering-designs-record

- Question: Can a collection of k-element subsets cover every t-element subset of a v-element set using fewer blocks than all current comparison sources for one listed parameter triple?
- Shape: record construction.
- Where defined: Target bank entry `covering-designs-record`; Daniel M. Gordon's La Jolla Covering Repository, https://dmgordon.org/covering-designs/, and https://coveringrepository.com/.
- Status to confirm first: the minimum across all repositories and recent independent claims specified in the bank; distinguish ordinary coverings from lottery coverings.
- Why this approach: delete a small part of a known construction, expose the uncovered subsets, and repair that finite residue. Select a cell where both search and exhaustive coverage checks are affordable.
- Weight: 3.
- Wild: no.

### labs-merit-factor-records

- Question: Can a binary sequence of length 67–600 achieve strictly lower exact aperiodic autocorrelation energy than the best currently published sequence at that length?
- Shape: record construction.
- Where defined: Target bank entry `labs-merit-factor-records`; the record sources identified there, including arXiv:2504.00987 and arXiv:2607.09688.
- Status to confirm first: current integer energies across the cited papers, their record repository, and newer publications; keep unrestricted and skew-symmetric records distinct.
- Why this approach: integer autocorrelations expose precisely which offsets are expensive. Compare local repair with structured constructions, using an independent direct calculation to detect misleading incremental scores.
- Weight: 2.
- Wild: no.

### life-smaller-orphan

- Question: Can a fully specified finite rectangular pattern under the B3/S23 Life rule have no predecessor, with smaller area or a narrower eligible height than the current comparison frontier?
- Shape: existence construction with a certified nonexistence property for predecessors.
- Where defined: Target bank entry `life-smaller-orphan`; its primary references include https://conwaylife.com/wiki/Garden_of_Eden, arXiv:1912.00692, and arXiv:2210.07837.
- Status to confirm first: current orphan dimensions and previous exclusion results, including the bank's required human confirmation of the comparison page. Distinguish finite orphans from whole Garden of Eden configurations.
- Why this approach: turn visual boundary motifs into constraints and compact them. A small picture may expose an obstruction that is hard to discover through undirected search. Begin only when the required encodings and certificates are feasible.
- Weight: 1.
- Wild: yes.

## Lenses

### residue-repair — Repair only what broke

Skeptic: no. Start from a known valid object and remove a small component. Enumerate the resulting violations exactly. Attempt to repair their union with fewer components than were removed. Abandon this neighborhood when the residue is too large to resolve within the remaining budget; retain the precise unresolved cases.

### visual-obstruction — Turn a picture into an invariant

Skeptic: no. Arrange failures as an incidence map, an offset profile, or a grid. Propose a repeated obstruction, translate it into a precise constraint, and test the constraint against known examples and tiny exhaustive cases. Abandon the idea when it has no exact formulation or fails those cases. A visually appealing pattern is only a lead.

### evaluator-first — Make the measurement cheap and exact

Skeptic: no. Derive a simple independent objective calculation, then derive incremental changes for individual edits. Compare every incremental calculation with the simple one on small objects before increasing scale. Stop using an update rule at the first disagreement. Faster evaluation helps only after correctness is established.

### structured-family — Buy completeness by narrowing the family

Skeptic: no. Impose one explicit symmetry or algebraic construction, enumerate small representatives, and identify what that restriction excludes. Compare with unrestricted local repair. Drop the restriction if it cannot represent strong known examples or if its attainable bound cannot improve the objective.

### hostile-baseline — Assume the apparent improvement is old or invalid

Skeptic: yes. Look for alternate names, missing comparison sources, wrong parameter conventions, and a cheaper existing construction. Try to exhibit one violated requirement in each candidate. Stop treating a lead as novel when a current source subsumes it, and record the exact reason.

## Scout voice

Be concrete and economical. Explain what the object is, the exact improvement required, and why this particular experiment can distinguish two plausible approaches. Separate the definition, the current baseline, and the untested idea. Prefer original definitions and saved examples to persuasive summaries.

## Attacker voice

Build something inspectable. Use small cases to expose a failure, make one deliberate change, and inspect the consequences. Be persistent with promising structure and quick to abandon a contradicted explanation. A precise failed attempt is useful; a favorable story without a surviving object is not.

## Heuristics

1. Keep a concrete object alongside every objective value.
2. Use small exact cases to diagnose errors before increasing scale.
3. Optimize the actual integer objective rather than a rounded proxy.
4. Search the uncovered or failing residue before perturbing the entire object.
5. Compare structured constructions with an unrestricted baseline.
6. Treat different parameter conventions as different problems until equivalence is established.
7. Prefer cases whose complete validation is cheaper than their discovery.
8. Preserve the next decisive test when a promising experiment needs continuation.

## Kill criteria

1. The candidate does not satisfy the published definition.
2. A newer or overlooked construction already matches or improves its value.
3. The apparent gain comes from an incomplete check, an objective error, or changed conventions.
4. The next decisive computation cannot fit the available time or resources.
5. A proposed restriction provably cannot reach a competitive object.
6. The only remaining support is visual plausibility or subjective interpretation.

## Self-critique

The proposed strengths are broad and do not establish expertise in these fields. Attractive small objects can conceal difficult completeness arguments, and active tables may already have exhausted obvious repairs. Fast local search can rediscover equivalent objects repeatedly. The cellular-automaton direction is especially speculative and can consume the budget in certification. Use observed progress to revise priorities rather than treating this initial fit as established.

## Method cards used

evaluator-first; smaller-first; representation; counterexample-shape; structured-family; object-as-data.


## Session-scoped manual quarry: condorcet-domains

User-selected for run 2026-10-25-1720-condorcet only. Criterion source: https://github.com/elder-plinius/V3R1T4S/blob/main/known-unknowns/record-tables/condorcet-domains.md; verbatim criterion frozen in that run target.md. This manual quarry is first for this session and does not change the nightly default quarries. Current upstream target is problem data only; pinned kit unchanged.
