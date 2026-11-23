# Honesty gate (eulerian-synchronizing-szykula-vorel-bound)

status: CONFIRMED_SOLUTION
confirmed_scope: The explicit 7-state, 5-letter complete Eulerian DFA in object/eulerian_n7_k5_rt24.json is strongly connected, has in-degree 5 at every state, is synchronizing with exact reset threshold 24 > 23 = floor((7^2-3)/2), which contradicts Szykula-Vorel Conjecture 19 as stated (any alphabet size, n >= 3), and no more than that single counterexample is claimed.

## Gate notes
- Object: object/eulerian_n7_k5_rt24.json, sha256 1a9b35e5b03b6b665ba08d9ec9305772bdf78e8ff094537163c4ef85d68e084b.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim folder; the object's builder (Gemini) is a different model family from every skeptic.
- Two independent programs: the reproduce skeptic computed the exact reset threshold 24 by four methods (subset BFS from the full set, a backward fixed point, a BFS over the transition monoid and iterative-deepening DFS), and a separate subset-BFS checker gives 24 (122 subsets reached); all confirm the automaton is complete, Eulerian (in-degree 5 at every state), strongly connected and synchronizing, with five distinct letters.
- Conjecture 19 of arXiv:1604.02879, quoted by the criterion skeptic: 'For n >= 3, (n^2 - 3)/2 is an upper bound for the reset threshold of an n-state Eulerian synchronizing automaton.' It has no alphabet-size hypothesis. Volkov's living list (arXiv:2508.15655 v4) and Szykula's survey (arXiv:2608.24245), read on 2026-11-17, still list it as open; the 2016 exhaustive searches covered 4 letters up to 7 states and 8 letters up to 5 states, not 5 letters at 7 states.
