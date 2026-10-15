# How we found it (contributor text, unverified)

A V3R1T4S research lane running OpenAI Codex (gpt-6-astra) attacked the completeness question in several runs on
2026-10-15. The lines that worked: projecting call products, a zero-sum normalisation that reduces the game's 48
behavioural probabilities to 32 coordinates, and comparisons over every possible opening, which show player 1 never
opens with a bet in any Nash equilibrium. Once the opening is fixed, the equilibrium conditions on the 18 coordinates
that matter can be solved in closed form and matched against the Szafron–Gibson–Sturtevant Tables 2–3 family, and the
terminal-history law can be checked deal by deal (24 ordered deals × 13 terminal histories). Monolithic generators hit
their time caps twice; the proof was split into checkpointed stages, and wrong polynomial decompositions and a missing
strictness argument were caught and corrected before the objects were frozen. No capped search takes part in the proof.
