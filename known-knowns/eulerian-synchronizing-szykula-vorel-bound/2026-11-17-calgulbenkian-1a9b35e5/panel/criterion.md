context: Claude Code subagent, fresh context [Sonnet 5.5]

# Criterion skeptic report

Checked literally against the success criterion.

- Definition match: Szykula-Vorel (arXiv:1604.02879, fetched, recorded in my fetches log) define Eulerian as strongly connected with in-degree equal to out-degree at every state. With a complete DFA that means in-degree equals |Sigma|, counted with multiplicity, as the target says. Self-loops and parallel edges are allowed (their own figure omits loops).
- Conjecture 19 verbatim: "For n >= 3, (n^2 - 3)/2 is an upper bound for the reset threshold of an n-state Eulerian synchronizing automaton. If |Sigma| = 2, then the bound can be improved to (n^2 - 5)/2." No alphabet-size, minimality or distinct-letter hypothesis. It covers a 5-letter, 7-state automaton. Their exhaustive search covered only 4 letters at n<=7 and 8 letters at n<=5, so 5 letters at n=7 was unsearched, which is consistent with a genuine counterexample. The reset threshold definition (shortest reset word length) matches.
- My own independent check (fresh Python, not the package's code): every state has in-degree 5; forward and backward reachability from state 0 covers all 7 states (strongly connected); subset BFS reaches all 127 nonempty subsets; layer-by-layer image sets from Q first contain a singleton at length 24, so the exact reset threshold is 24 > floor((49-3)/2) = 23. The five letters are pairwise distinct. The file's SHA/rows match the README.
- Two programs: the package ships a Python set-BFS and a C bitmask verifier, both calibrated on A_1..A_3 (11, 39, 83) and Cerny (non-Eulerian). My reproduction is a third check. n=7 <= 30.
- Hidden quantifiers: none found. The claim is full success, not a partial win; it needs only one counterexample. It is not a binary or <=4-letter claim, and the README says so. Not subsumed by any merged package I can see; I did not have bank access to check for a later upstream tie, which is a residual limit.
- Caveat: the two shipped verifiers share an author, so true independence rests on my third check, which agrees.

confirmed_scope: The explicit 7-state, 5-letter complete Eulerian DFA in object/eulerian_n7_k5_rt24.json is strongly connected, has in-degree 5 at every state, is synchronizing with exact reset threshold 24 > 23 = floor((7^2-3)/2), which contradicts Szykula-Vorel Conjecture 19 as stated (any alphabet size, n >= 3), and no more than that single counterexample is claimed.

pass: true
