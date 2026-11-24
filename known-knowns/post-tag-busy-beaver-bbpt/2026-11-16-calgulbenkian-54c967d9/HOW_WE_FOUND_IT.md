# How We Found It

_Note: contributor text, unverified._

1. **Macro/champion search (`champion-and-macro-explorer`)**: High-speed simulation across `S = 8..11` confirmed none of the `7` size-8 holdouts halts within `10^8` steps, pointing toward regular-language inductive invariants rather than late halting.
2. **Counterexample-guided Moore-minimal DFA synthesis (`dfa-invariant-synthesizer`)**: Bounded `k`-substring closure (`sligocki`'s `closed_tape_subset(4)`) fails on chaotic size-8 holdouts like `010_2_0` (`Chaotic 2`), `01010_1`, `010_21_`, and `0120__0` because local factors lose parity synchronization between the 2-symbol deletion head and variable-length appended words `w_a`. Synthesizing full deterministic finite automata `A = (Q, Sigma, delta, 0, F)` via synchronized `Q x Q` product counterexample-guided refinement (`cegis_dfa.py`) closed all `368` non-cycler non-halting canonical classes (`10` to `62` states on the `7` wiki holdouts), proving `BB_PT(8) = 19` with fast exact product-automaton verification.
