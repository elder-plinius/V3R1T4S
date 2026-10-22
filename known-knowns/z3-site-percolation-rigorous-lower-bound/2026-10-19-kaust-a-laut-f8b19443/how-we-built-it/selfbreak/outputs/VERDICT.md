# Self-break verdict: p_c^site(Z^3) >= 263376/10^6

verdict: SURVIVES

Context: the run's main session (not a fresh context), plus an outside audit by another AI agent relayed by the
human (it read audit/AUDIT_BUNDLE.md and ran the Python checks itself). The three-skeptic panel (fresh subagents) is
the independent step.

Assumed wrong and attacked:
1. Normalization ("should the criterion be K_N < p?"): the continuation starts at y = v_{N+1}, outside the path;
   y's openness is in B, and B is contained in {|C(y)| = infinity}, so P(B) <= theta exactly. The outside auditor
   withdrew the objection. (The K_N < p variant is valid but weaker: N = 18 gives 0.240626.)
2. Proof steps re-derived (claim/PROOF.md Lemmas 0-4): tree-path NAW property, shortcut and corner closures (strict
   rank comparison only), F disjoint from the path for every NAW, Konig ray, independence on disjoint site sets,
   sign-flip symmetry (corner comparisons involve two different axes, so they depend only on the axes).
3. Ground truth (groundtruth.py A): 300 random configurations, true parent trees: 79,201 tree paths, 148,198
   forced-closed sites all closed, 102,078 children all valid extensions. Negative controls (reversed corner
   comparison; loosened pair gap) fail at once.
4. Independent enumeration from complete paths (groundtruth.py B/C): the full N = 9 table matches; full-depth
   subtrees match at N = 18 (10/10 random 10-step prefixes) and N = 20 (10/10 random 12-step prefixes) against a
   mechanical prefix-mode copy of the production code (whose no-prefix output equals production at N = 12).
   Plain Go (no symmetry) = parallel Go at N = 12 and 14. Walk totals equal NAW counts; a_18 equals the Alm program.
5. Exact arithmetic: verify_cert.py (Fraction): K_20(263376/10^6) < 1, K_20(263377/10^6) > 1, monotone on
   [0, 21/44]; sanity 1/5 passes, 0.3116 fails. Sum of c_f equals a_{N+1} at every N (an internal identity: no NAW
   extension can be a forced-closed site).
6. Criterion read literally: explicit rational p* = 263376/10^6; exhaustive enumeration with exact integers; exact
   rational inequality; code rerunnable; strictly above 0.21103.
7. Table access: grep of attempts/, claim/, selfbreak/, data/ for user agents, cookies, retries or challenge
   bypass: no hits. Every source was fetched once with plain curl (HTTP 200).

Open (not a flaw in the proof): the PREREG asks for an independent implementation reproducing a full table at some
N >= 12; ours reproduce N = 9 fully and N = 18, 20 on subtrees. The REPRODUCE skeptic is asked to supply a full
N >= 12 table. Novelty of the method (folklore risk) is for the NOVELTY skeptic and an expert.
