# Research charter v1 (2026-11-05)

## Thesis
A player's eye for odds and min-maxed build spaces, joined to an insistence that every number be re-checked by an
independent party. The charter aims that pair at small combinatorial games, puzzles and "choose k disjoint pieces
that each cover everything" problems, where a reformulation plus exact enumeration beats raw compute on one thread,
and at tag-system busy beavers, where a tested certificate zoo exists and the open part is known precisely.

## Quarries
- id: queens-graph-domatic-numbers; question: close one of the remaining open pairs in Lauri's corrected table (dom(Q_12), idom(Q_12), tdom(Q_10), tdom(Q_11), tdom(Q_12)) or settle n = 13; shape: record (explicit partition) or certified bound; defined in: J. Lauri, Improved bounds on the domatic numbers of queens graphs, Discrete Math. Lett. 16 (2025), doi 10.47443/dml.2025.112, and its Corrigendum, Discrete Math. Lett. 18 (2026), doi 10.47443/dml.2026.195; status to confirm first: any later erratum, and the live OEIS entry A292192; why us: disjoint-dominating-set packing, exhaustive enumeration of minimal sets and exact LP duals already worked for dom(Q_11); weight: 5; wild: no.
- id: post-tag-busy-beaver-bbpt; question: settle BB_PT(8) by certifying its remaining holdouts, or beat a size 8-11 champion; shape: bound or proof (exhaustive classification with certificates) or record; defined in: bbchallenge wiki, "Post Tag System" page, and S. Ligocki's post_tag code and notes; status to confirm first: the current holdout list; why us: cycler, periodic-stream, bouncer and aligned-token certificates for tag systems, with independent re-checkers; weight: 3; wild: no.
- id: cyclic-tag-busy-beaver-bbct; question: settle BBCT(8) or beat a size 8-14 champion; shape: bound or proof, or record; defined in: bbchallenge wiki, "Cyclic Tag" page; status to confirm first: published champions and holdouts; why us: same certificate zoo, plus exhaustive window games that show where local certificates cannot work; weight: 2; wild: no.
- id: three-heap-wythoff-fraenkel-a1-11; question: prove Fraenkel's three-heap Wythoff conjecture for smallest heap 11, extending the automated proofs that stopped at 10; shape: proof (machine-checkable, from finite P-position tables); defined in: X. Sun and D. Zeilberger's three-heap Wythoff paper and accompanying page (Rutgers, "wythoff"); status to confirm first: whether a = 11 has been done since; why us: game-position intuition plus exact table generation and independent checking; weight: 3; wild: no.
- id: sokoban-max-moves-small-boards; question: a board with n floor squares and k boxes whose shortest solution is longer than the archived maximum; shape: record (explicit board + optimal solution length, re-solved independently); defined in: the Sokoban maximum-moves archive by DeStefano and qqwref, and OEIS A195667; status to confirm first: the archive's current best values; why us: puzzle "build space" intuition plus exhaustive breadth-first solving; weight: 2; wild: no.
- id: lifelike-rules-still-life-counts; question: the next unknown still-life count for one Life-like rule (HighLife, 2x2, Move or Maze); shape: bound or proof (exact count by two independent enumerators); defined in: OEIS A175000, A166476, A175001, A175002; status to confirm first: the live OEIS terms; why us: patience plus two genuinely different enumerators that must agree; weight: 2; wild: no.
- id: tiny-tag-busy-beaver-exact; question: certify one of the chaotic length-11 holdouts as non-halting, or find a halting one, using an argument that is global rather than local; shape: proof or counterexample; defined in: bbchallenge wiki, "Tiny Tag" page; status to confirm first: whether f(11) is now listed; why us: the holdouts are already isolated and every local certificate class has been shown to fail on them; weight: 1; wild: yes.

## Lenses
- key: packing-certifier; title: Cover with disjoint pieces; text: You recast the question as packing pairwise disjoint pieces that each cover the board. You enumerate the smallest pieces exhaustively, with two independent enumerators, price them with an exact rational dual, and only then search for constructions in the gap the bound leaves. A line is dead when the bound is slack and the remainder search stalls twice. skeptic: no.
- key: odds-player; title: Read it like a min-maxer; text: You treat the object as a build: you ask which resources are scarce, which choices dominate, and where an expected-value estimate says a record should hide. Then you search exactly there and nowhere else. A line is dead when the estimate and the exact search disagree twice in the same direction. skeptic: no.
- key: evaluator-first; title: Fast exact evaluator first; text: You spend the first stretch on the fastest exact evaluator you can write, calibrated on every published small value, and let speed decide what is reachable. A line is dead when the evaluator cannot reproduce a published value. skeptic: no.
- key: certificate-zoo; title: Certify, don't simulate; text: You classify each holdout by the cheapest certificate that could apply (repeated state, periodic stream, bouncer, token substitution, window game) and you write an independent checker for each class before trusting it. A line is dead when a complete game or exhaustive window test shows the class cannot contain the object. skeptic: no.
- key: global-drift; title: Follow the whole population; text: You stop following single lineages and reason about the whole queue or population at once: invariants of densities, counting identities, regular languages of configurations. You accept only arguments a program can check exactly. A line is dead when its relaxation stays feasible for known halting cases. skeptic: no.
- key: source-skeptic; title: It is already settled; text: You try to show the quarry is solved, trivial, ill-posed or already claimed: you read errata, footnotes, histories of the tables and open and closed public contributions. A line ends when one primary source settles it, or when an honest bounded search finds nothing. skeptic: yes.

## Scout voice
Read primary definitions first and quote them exactly. Distrust a table until its date and its source agree. Say plainly
what could not be read.

## Attacker voice
Patient, economical and stubborn about re-checking: you would rather settle one small cell cleanly than move ten by
assertion, and you change the representation before you add compute.

## Heuristics
- Calibrate every program on the published small values before using it on an open case.
- Two programs written differently must agree before a count or a list is trusted.
- Reformulate first: a packing, a game, a certificate class.
- Use exact arithmetic for every certificate; floating-point solvers only find candidates.
- Record the precise boundary of every completed search.
- Prefer the smallest open cell over the most famous one.

## Kill criteria
- A primary source or public contribution already settles the cell.
- A program fails to reproduce a published value.
- An exhaustive test shows the method's class cannot contain the target.
- The estimated compute exceeds a week of single-thread nights.

## Self-critique
The odds-player instinct can make a pretty estimate look like evidence. Two independent programs can share one wrong
reformulation. Tag-system holdouts may be chaotic in a way that makes every finite certificate hopeless, and the wild
quarry may consume time with nothing to show.

## Method cards used
evaluator-first; structured-family; obstruction-first; small-data. Chosen from the niche card (not drawn at random).
