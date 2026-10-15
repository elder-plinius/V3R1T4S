# Honesty gate (kit/RUN.md step 7), written by the main session of run 2026-10-15-0312 at Thu Oct 15 03:38:34 UTC 2026

Panel: three fresh subagent contexts started by run 2026-10-15-0312 (this run's step 0 first job, as the previous
gate asked), each given only a copy of claim/; their files are panel/reproduce.md, panel/novelty.md and
panel/criterion.md (all end in "pass: true", all name files relative to claim/ only).

Gate reading of the three files:
- REPRODUCE: own exact-Fraction checker written before opening the author's code; the claimed value
  1652448303171916717080006468042849/70681471350112364987160770000000000 reproduced exactly by five routes; every
  stated property of mixture.json verified; the author's scripts give byte-identical output; sha256 hashes verify;
  the paper's own Table 3 mixture reproduces 31/1326 as a control. pass: true.
- NOVELTY: status source https://arxiv.org/abs/2604.24517 fetched once (HTTP 200, v2 of 23 May 2026); Table 1 and
  Theorem 3.4 quote 31/1326 for this cell; v1 PDF fetched once (HTTP 200) and found to carry the same theorem; the
  stray "0.02344" in the first sentence of Section 3.2 is traced to a commented-out draft formula in the LaTeX source
  with no construction or proof anywhere in v1 or v2 (a withdrawn number, not a known bound); 23 web searches, the
  arXiv title search, author searches, OpenAlex and three citing papers (2607.08744, 2606.31020 and a Sep 2026
  empirical study) show no larger lower bound for this cell; TROPHY_CASE.md and the open pull requests have nothing
  on this target. Blocked in one request each and NOT retried: Semantic Scholar citations (429), arXiv API (429), one
  arXiv author search (429), Google Scholar (error page), ACM DL (403). pass: true.
- CRITERION: the clause "an explicit information structure certifying more than 31/1326" is met in the same sense
  the paper itself uses (its Theorem 3.4 is certified by a uniform mixture of two CI structures through Yao's
  principle; a single structure can never give a positive lower bound); definitions match line by line; randomised
  aggregators are covered by convexity; the exact rational strictly exceeds 31/1326 by
  612886837595654297197253671111/2756577382654382234499270030000000000 (about 2.2e-7); no null test needed
  (deterministic exact certificate); not subsumed by the paper. pass: true.

Downgrade triggers checked: no hedging on the result itself (the caveats concern presentation, the tiny margin and
unreachable secondary sources; the primary status source was read); no reproduction mismatch; the value is strictly
better than the live published bound in exact arithmetic (a tie at six printed decimals is not a tie of rationals);
no stretched criterion (the object is the paper's own kind of certifying object); scope no wider than reproduced;
nothing sampled; nothing capped; no probable prime; table access honest (no retries after 429/403); one object, one
cell. The panel's status fetch is less than one hour old at gate time.

Caveats carried into the package and the report (not downgrades): the improvement is 2.2e-7 and invisible at the
paper's six printed decimals, so it must always be stated as "> 31/1326 (exact)"; the authors' Table 3 construction
is the parent of this object and must be credited; the stray 0.02344 sentence must be mentioned; secondary citation
indexes were partly unreachable.

status: CONFIRMED_SOLUTION
confirmed_scope: In the model of Section 2 of arXiv:2604.24517v2 restricted to the class Pi_CI (two experts whose signals are conditionally independent given a binary state whose values in [0,1] are unknown to the aggregator, squared loss, additive regret against the omniscient aggregator), the uniform mixture of the two explicit rational environments in claim/mixture.json certifies through Yao's principle, as in the proof of that paper's Theorem 3.4, that every aggregation function f has worst-case regret at least 1652448303171916717080006468042849/70681471350112364987160770000000000 ≈ 0.0233788045, which exceeds that paper's lower bound 31/1326 by exactly 612886837595654297197253671111/2756577382654382234499270030000000000 ≈ 2.22e-7.
single_context_unpanelled: no
