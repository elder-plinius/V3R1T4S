# CRITERION skeptic

context: codex exec (fresh context via codex-fresh)

criterion: B — full on-path completeness
confirmed_scope: Every behavioral Nash equilibrium of the three-player Kuhn poker game defined in Section 2 of Szafron, Gibson and Sturtevant (2013) agrees at every information set it reaches with positive probability with some member of their Tables 2–3 family.

## Literal criterion and quantifiers

I read `target.md` before author code and compared the game and family with Section 2, Table 1, and Tables 2–3 in `data/original.txt`. The submitted result meets direction B through the exact-certificate alternative. This is a statement about every equilibrium, including boundary equilibria and arbitrary unreached actions, rather than a search for selected equilibria. Its polynomial variables range over real feasible probabilities; rational coefficients and exact arithmetic do not restrict the quantified equilibria to rational profiles.

The proof also implies p1 and p2, but those are subsumed consequences of this full win and are not separately credited. No direction-A counterexample is claimed.

## Independent verification

I wrote `criterion_independent/audit.py` and `criterion_independent/controls.py`. Neither imports supplied executable code. The former independently generates the game by an acting queue, antes, bets, calls, folds, and showdown, over all 24 distinct ordered deals; it uses a separate polynomial representation and replays the five certificates in `attempts/solver/output/`. It checked 759 full-game events, 848 no-opening/normalization/completion events, 634 restricted-game events, and all 312 joint deal/history identities. Results are in `criterion_independent/audit_output.json`.

The semantic steps required by the certificate are valid:

- P1's later call coordinates and P2's calls following their own checks are realization probabilities, with constraints call <= 1 - initial bet. These domains represent all behavioral profiles and all unilateral deviations, including initial-bet probability one. The optimality rules follow from feasible coordinate changes or comparisons with vertices of these domains.
- The opening certificate excludes a11+a21>0 and proves all four opening probabilities zero on the complementary branch. The nonnegative opening coordinates make these branches exhaustive. Initial checking is therefore proved before restricting the game.
- Normalization retains each player's free coordinates and changes only that player's fixed coordinates. Projection and embedding preserve feasibility. Its three dominance polynomials use domain facts alone for the deviator, with only proved opponent equalities substituted. Nash optimality gives u_i(x) >= u_i(T_i x_i,x_-i) >= u_i(Tx); zero-sum utilities force equality for each player. Applying the same dominance inequality to every reduced deviation establishes that Tx is a reduced Nash equilibrium.
- Completion covers c11=0, c11=1/2, and 0<c11<1/2. With r=b11, s=b21, and y the realization coordinate for b23, the proved s<=1/4 makes b23=y/(1-s) well defined. The case inequalities establish the literal Table-3 ranges and beta=max(r,s). Choosing unused b32=1/2 and c33=c34=0 satisfies their ranges.
- The final identities compare the original equilibrium to the completed family member separately for every deal and terminal action history. At any information set, summing the corresponding joint cells gives reach R and aggressive-action mass A; when R>0, its probability is A/R. Thus these identities imply exactly the requested reached-action agreement.

Separately, `criterion_independent/run_supplied.py` reproduced `attempts/certifier/code/verify_completeness.py` and all 26 submitted tests; see `criterion_independent/supplied_output.txt`. The proof is not accepted merely because that program prints PASS.

## Null models and overstatement checks

`criterion_independent/controls_output.json` records seven exact family equilibria spanning all three cases and important endpoints, with exact best responses over all card-specific pure plans. A beta=0 equilibrium altered at a33 and c32 remains Nash and has the same joint law: off-path disagreement is correctly not treated as a win.

All-check/fold, all-half, and a positive-P1-opening perturbation are rejected as equilibria. Two additional profiles have identical public terminal-history marginals but different joint deal/history laws, demonstrating why public marginals alone would be insufficient. The actual certificate checks the stronger law. Four independently introduced corruptions—opening assumption, omitted terminal, terminal identity, and family-case assumption—are rejected. These finite controls calibrate the implementation; the universal result comes from the certificate.

## Non-subsumption within the supplied evidence

The defining paper proves family membership implies equilibrium and leaves completeness open. The saved Ganzfried QP text explicitly describes its differences as off path (`data/current/quoter/output/texts/paper_2509_25618v3.txt`). Billingham explicitly did not investigate disconnected branches in the unrestricted game (`data/current/quoter/output/texts/billingham2018.txt`); his exhaustive simplified-game analysis forbids lowest-card betting (`data/current/quoter/output/texts/billingham_full_street_2017.txt`). Finding an equilibrium, numerical continuation, or classifying that restricted game does not subsume this universal unrestricted-game theorem.

The historical comparisons provide affirmative evidence of different game definitions: the adjacent Prisner excerpt describes two players and three card ranks (`data/prisner_tournament_excerpt.txt`), and the original historical models named in Ballard's title are explicitly two-person models (`SOURCE_BRIDGE.md`, `data/source_bridge/MODEL_SCOPE.md`). The missing full analytical chapter and Ballard article remain unread; their complete contents are not certified here. No supplied earlier theorem establishes the target conclusion. I do not turn bounded literature retrieval or missing text into an assertion of exhaustive novelty.

All independent code and outputs are saved under `criterion_independent/`. Execution used one thread, standard-library arithmetic, and observed peak resident memory below 47 MB; reproduction details are in `criterion_independent/README.md`.

pass: true
