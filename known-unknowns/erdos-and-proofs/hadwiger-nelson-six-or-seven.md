# Hadwiger–Nelson: does the plane require six colours or seven?

✏️ **Erdős problems and proofs** · moonshot (famous, long odds) · tractability ★☆☆☆☆ · compute: laptop-hours for bounded graph searches; a full resolution may require substantially more compute or new mathematics · open as of 2026-11-03

## The problem

The Hadwiger–Nelson problem asks for the least number of colours in a colouring of every point of the Euclidean plane such that points at distance exactly one receive different colours. Aubrey D. N. J. de Grey established the lower bound five in 2018. OpenAI's September 2026 paper, The Euclidean plane is not five-colorable, and its published Lean formalization report the lower bound six for arbitrary colourings, without measurability or continuity assumptions, and the upper bound seven including boundary points. The seven-colour upper bound is historically credited to John R. Isbell. Google DeepMind's Formal Conjectures entry for Erdos problem 508 (FormalConjectures/ErdosProblems/508.lean) records 6 <= chi(R^2) <= 7 and tags the exact value 'research open', and erdosproblems.com/508 lists the same bounds (both checked 2026-11-03). Determine which of six and seven is the answer. These source statements are not an independent audit of the published proofs. The finite-witness question for five colours is a separate bank target (hadwiger-nelson-smaller-5-chromatic-udg).

## What counts as a win

Resolve chi(R^2) = 6 or chi(R^2) = 7, with an independently checkable certificate or a kernel-checked formal proof (Lean, Rocq or Isabelle; no sorry, admitted goals or axioms beyond the system's standard ones). For the finite-obstruction route to seven: supply a finite simple graph, distinct exact planar coordinates for all vertices, a proof that every listed edge has squared length exactly one, and a checkable certificate that the graph has no proper six-colouring. Supply the complete encoding and an UNSAT proof (DRAT or LRAT) checked by drat-trim, cake_lpr or another separately implemented checker, not just a solver verdict. The published seven-colour upper bound then completes the equality. Alternatively supply a kernel-checked formal proof of non-six-colourability of the plane. For six: supply a kernel-checked formal proof of a proper six-colouring of the entire plane, covering all points and all unit-distance pairs, including boundaries; the published lower bound six completes the equality. All routes must verify the supporting bound, assumptions and current literature before claiming a resolution; a previously published resolution is not a new win.

## How a win is checked

For a finite graph, independently parse the coordinates and edge list; reject loops, invalid endpoints and coincident vertices. Use exact algebraic arithmetic (with specified roots/isolating intervals where needed) or machine-checked equalities to verify every edge's squared distance is one. Unlisted unit-distance pairs need not be edges: a non-six-colourable subgraph suffices. Independently regenerate the six-colouring CNF from the supplied graph: each vertex has exactly one of six colours and endpoints of every edge have different colours. Verify the UNSAT certificate against that regenerated formula with a separately implemented proof checker. Omit symmetry-breaking constraints unless their satisfiability-preserving reduction is independently proved. Record hashes, pinned tools and rerunnable commands. For a formal-proof route, build in a clean pinned environment, inspect the theorem statement and transitive axioms, and reject admitted goals, sorryAx or custom axioms assuming the result. For a six-colouring, verify total coverage of R^2 rather than a bounded sample, measurable-only variant or almost-everywhere statement. Independently verify the supporting published bound and recheck the live status and novelty.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/508.lean>

## Sources

- <https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/508.lean>
- <https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/docs/158.md>
- <https://www.erdosproblems.com/508>
- <https://arxiv.org/abs/1804.02385>
- <https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/The-Euclidean-plane-is-not-five-colorable-September-23-2026/paper.pdf>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- HEURISTIC: Search exact algebraic unit-distance constructions by composing and rotating rigid graph gadgets, then test six-colourability with a proof-producing SAT solver.
- HEURISTIC: Use small certified obstructions from failed colour assignments to guide subsequent constructions; retain exact coordinates throughout.
- HEURISTIC: Explore periodic six-colour constructions only with a plan to prove coverage and all unit-distance exclusions, including tile boundaries.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- The known lower bound six does not show that a seven-chromatic finite unit-distance graph exists. This search may fail because the plane is six-colourable.
- A five- or six-chromatic graph does not settle the remaining six-versus-seven question. This proposal defines no partial wins.
- Floating-point distances near one are not unit-distance proofs. An abstract non-six-colourable graph without an exact planar unit-distance realization is insufficient.
- A solver timeout or an UNSAT string without a verified certificate is not a proof. An incorrect CNF or unjustified symmetry breaking can manufacture false obstructions.
- Non-measurable colourings are allowed. Ruling out only measurable, periodic or other restricted six-colourings does not rule out arbitrary six-colourings.
- The Formal Conjectures repository contains statement placeholders with sorry and links to external proofs; those placeholders are not proofs. Inspect and verify the actual linked proof and its dependencies.
- A smaller 5-chromatic unit-distance graph is a finite-witness record under hadwiger-nelson-smaller-5-chromatic-udg, not progress here.
- Written proofs that are not kernel-checked do not count, however convincing; they need peer review elsewhere first.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/erdos-and-proofs/hadwiger-nelson-six-or-seven.md
```

Already set up? Say `run V3R1T4S on hadwiger-nelson-six-or-seven`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `hadwiger-nelson-six-or-seven`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
