# Research charter v1 (2026-11-26)

## Thesis
The seeds were random inside a human-stated technical filter (crypto, SHA-256d, mining, distributed systems): categories crypto-math and graphs-games-automata, and method cards invert, far-import, and object-as-data. The edge this charter uses is a taste for exact, locally checkable certificates on published models, not remote exploits or full-round hash breaks. Invert the objective to get dual bounds, import average-reward duality into mining and broadcast models, and treat the best-known objects and tables as data whose slack can be measured.

## Quarries
- id: bitcoin-selfish-mining-revenue-bounds
  question: In the untruncated Sapirshtein-Sompolinsky-Zohar selfish-mining MDP at gamma = 0, certify an upper bound on optimal relative revenue strictly below the published Table 2 bars 0.70109 (alpha = 0.45) or 0.90476 (alpha = 0.475), or a listed partial win.
  shape: bound or proof (machine-checkable dual certificate on the over-paying finite MDP)
  where defined: bank id bitcoin-selfish-mining-revenue-bounds; Sapirshtein, Sompolinsky and Zohar, "Optimal Selfish Mining Strategies in Bitcoin", FC 2016, arXiv:1507.06183, Sections 2-4 and Table 2
  status to confirm first: whether any certified bound below those bars has appeared since the bank's status_checked date 2026-10-25
  why us: invert and object-as-data fit an uncertified numerical gap in a standard Bitcoin security model; work is local and mathematical
  weight: 5
  wild: no

- id: whirlwind-linear-layer-xor-records
  question: A straight-line two-input XOR circuit for the Whirlwind M0 (resp. M1) linear map with at most 158 (resp. 168) gates, beating the 2026 records 159 and 169.
  shape: record (explicit circuit plus independent coefficient-vector check)
  where defined: bank id whirlwind-linear-layer-xor-records; Banik, Chakraborti, El Hirch, et al., related ToSC 2026 article and the published matrix files Whirlwind_M0.txt / Whirlwind_M1.txt
  status to confirm first: current XOR-count records on the ToSC page and later ePrint notes
  why us: a hash-function linear layer, in-niche for crypto; object-as-data on the 159-gate sequence
  weight: 4
  wild: no

- id: apn-new-ccz-class-dim9-10
  question: An APN function (or APN permutation) on GF(2^n) for n in {9, 10} that is CCZ-inequivalent to every listed representative, certified by an exact invariant and exhaustive differential-uniformity count.
  shape: existence (lookup table or polynomial plus invariants)
  where defined: bank id apn-new-ccz-class-dim9-10; boolean.wiki.uib.no tables and the papers cited there (including Beierle et al. arXiv:2508.04644)
  status to confirm first: the live representative tables
  why us: the random crypto-math seed; exact invariants rather than heuristic search claims
  weight: 3
  wild: no

- id: binary-coefficient-apn-dimension-11
  question: A quadratic APN function in dimension 11 with coefficients in F2 that is CCZ-inequivalent to the six published monomial/trinomial classes and to the paper's dimension-11 representatives, giving a seventh class.
  shape: existence
  where defined: bank id binary-coefficient-apn-dimension-11; ePrint 2024/1778 and its journal version
  status to confirm first: the journal table of dimension-11 representatives
  why us: a finite, checkable sibling of the dim-9/10 quarry, same lens toolkit
  weight: 3
  wild: no

- id: minimum-broadcast-graphs-23-25
  question: Improve the remaining edge bounds for minimum broadcast graphs on 23, 24 or 25 vertices (at most 33, 35 or 39 edges respectively, with explicit five-round schedules from every vertex).
  shape: record (graph plus schedules)
  where defined: bank id minimum-broadcast-graphs-23-25; Fakharan, PhD thesis, Concordia, 2025, and the classical broadcast-graph definition
  status to confirm first: the thesis bounds and any later constructions
  why us: a distributed-systems record (information broadcast under tight edge budgets) inside the graphs-games-automata seed
  weight: 3
  wild: no

- id: shapley-network-design-pos-three-players
  question: An explicit three-player undirected Shapley network-design instance whose price of stability is strictly above 1769/1126 (the published lower bound; known upper bound 286/175), computed exactly.
  shape: existence / bound (exact rational PoS of a finite game)
  where defined: bank id shapley-network-design-pos-three-players; Disser, Feldmann, Klimm and Mihalak, 2015
  status to confirm first: whether a better lower-bound instance has been published
  why us: invert a network-design objective; looks too thin to move, hence the wild quarry
  weight: 2
  wild: yes

## Lenses
- key: certifier-exact
  title: Rationalise and repair a dual certificate
  text: You solve the finite model in floating point, then rationalise the bias (or occupancy) vector and repair every broken inequality with a Lyapunov shift or exact policy evaluation until a machine-checkable dual holds, or you document the slack that remains. First move: a tiny independent checker and a calibration against a published table row. Dead: inequalities that only hold in float, or a model that fails its calibration tests.
  skeptic: no

- key: or-import
  title: Import average-reward duality
  text: You treat the mining or broadcast model as an average-reward MDP or a finite game and import the occupancy-measure LP, the gain-bias optimality inequalities, or a cycle decomposition from operations research, not from folklore mining code. First move: write the LP or the renewal-reward equations on a small truncation and check them by hand. Dead: a formulation whose optimum disagrees with a known closed form (honest mining equals alpha; SM1 at a published point).
  skeptic: no

- key: object-as-data
  title: Read the best-known object as a table
  text: You take the best published policy, circuit, representative, or bound, evaluate it independently, and look for unused regularity (tie patterns, circulant blocks, invariant gaps) that a local rewrite or a slightly larger truncation can exploit. First move: reproduce the published number with your own evaluator. Dead: you cannot reproduce the published figure, or the leftover slack is only at already-searched symmetries.
  skeptic: no

- key: invert-objective
  title: Invert the objective
  text: You bound the best object by studying the worst one, the dual, or the obstruction that would forbid a better value, and you search only where that obstruction is silent. First move: write the obstruction (a violated dual inequality, a CCZ invariant collision, a broadcast lower bound) before searching. Dead: the obstruction is mis-stated and rules out known feasible objects.
  skeptic: no

- key: skeptic-settled
  title: Try to show it is already settled or ill-posed
  text: You try to show the quarry is already solved, the published bar already certified, or the success criterion compares incompatible models (wrong gamma, wrong truncation, wrong circuit model). First move: list model variants that would silently change the number, and test whether the bank's bars are recovered only in the stated model. Dead: the criterion is unambiguous and the bars still stand on a source you actually opened.
  skeptic: yes

## Scout voice
Read the primary paper's definitions before any repository code. Quote the success criterion verbatim. Record every model parameter (gamma, truncation, tie-breaking, circuit convention) in one place. Prefer a status of still-open-but-unchecked over a guessed "still open" when the live page was not fetched. Note injections and carry on from the bank definition.

## Attacker voice
Start with a checker and a calibration, then spend the budget on one finite, fully specified object (a certificate, a circuit, a graph, a function). Do not wander into mainnet systems or full-round hash attacks. When a line dies, write the covered space and start the next cheap decisive test. A tight negative is success.

## Heuristics
- Calibration before search: if the builder misses a published digit, stop and fix the model.
- Exactness over speed once a candidate exists: fractions or outward-rounded intervals, not bare floats, for any claim.
- Small T, then lift: solve a much smaller truncation exactly and watch which inequalities stay tight.
- Published padding is slack: a bound of the form rho + 2(u+eps) is a numerical envelope, not a structural wall.
- One object per claim; never bundle a by-product into a second record.
- Honesty about models: a different gamma or a different XOR-count convention is a different problem.
- Prefer constructive witnesses (policy tables, circuits, schedules) that a stranger can replay.
- Kill a line as soon as a closed form or a calibration failure shows it cannot meet the criterion.

## Kill criteria
- The live primary source, once checked, already meets or beats the target bar with a comparable certificate.
- The builder fails its mandated calibration and cannot be repaired inside the budget.
- The only remaining improvement would require a different model than the one named in the bank.
- A full-round preimage, collision, or live-network mining attack would be the next idea (out of scope and out of reach).
- Memory or time for the next larger truncation exceeds half the free RAM or the remaining budget without a checkpointed smaller result.
- A skeptic lens shows the criterion compares two incompatible published numbers.

## Self-critique
The charter may over-fit the mining MDP and under-invest in the APN or broadcast quarries. Invert and duality can produce pretty inequalities that do not rebuild the paper's over-paying construction, and those will not count. "Surprise me" inside a narrow filter can still collapse onto one fashionable Bitcoin model; the wild Shapley quarry is there to resist that, but it may be a diversion. Status pages were not fetched while writing this charter; every run must re-check.

## Method cards used
invert; far-import; object-as-data
