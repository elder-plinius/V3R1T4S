# Criterion skeptic verdict: p1 for 1RB1LC_1LC0RD_0LE1LA_0RF1RA_1LA0LA_---0RB

context: subagent (fresh context, Claude Code Agent tool)

Scope of review: only the claim folder (CLAIM.md, REPRODUCE.md, result/rules.json, code/*, data/*). I read every
code file. I ran code/remote_checks.sh in full on the compute server, plus two checks of my own: four extra mutation
controls, and a coverage-instrumented copy of code/replay_v2.c. The remote directory was deleted afterwards. I also
made one live fetch of the Holdouts_lists page at 2026-10-17T17:19Z.

Claimed win: p1 only. The full success criterion is not claimed: there is no non-halting certificate and no halting
count, and the claim says the halting status stays open. I therefore judge p1 alone.

## (a) "a machine in the newest BB(6) holdout file": MET
- In data/holdouts_lists.html (sha256 383b2762...2762), the top row of the BB(6) table is "October 16th, 2026 @mxdys 663
  BB6_holdouts_663.txt". The rows below it are 698 (Oct 15), 740 (Oct 10), 778 (Oct 7) and 797 (Sep 30).
- data/BB6_holdouts_663.txt has sha256 cfb2540f8101f2f2f20a14f9bc848252e34e45de2920fdd6b257096093844ee9 (recomputed)
  and 663 lines. Line 523 is exactly the machine string.
- My live re-fetch at 17:19Z still shows BB6_holdouts_663.txt (October 16th, 2026) as the newest BB(6) row.
- The claim names the list it targets: the informal holdout inventory.

## (b) "whose wiki/holdout notes give no accelerated rule set": MET (literal reading, snapshot of 2026-10-17T17:10Z)
- I reran code/notes_check.py on data/. It searches for the machine and all 240 images under mirroring and B..F state
  permutations.
  - No hits on the Holdouts_lists page, the BB(6) page, or the sheet tab gid806905077 (a list of simulation-depth
    tables).
  - One hit in the annotated sheet tab gid1330361301, line 789: Status empty, Classification "Quadratic Mess", Notes
    empty, Sources empty, Done By empty.
  - One hit in the 4319 spreadsheet, line 3567: every other cell is empty.
- The machine's own wiki page returned HTTP 404 (data/notes/machine_page.html).
- "Quadratic Mess" is a label for the kind of behaviour. It is not a rule set. The two nearby holdouts at distance 2
  (lines 2 and 633) also have empty notes.
- The Discord #bb6 channel is not "wiki/holdout notes". CLAIM.md correctly presents the Discord material as unfetched
  human reports. The one reported hit is a 2024 message listing the machine as undecided and unclassified, which
  supports the absence of a rule set. p1's clause does not depend on Discord.
- Residual caveat: the wiki full-text search was done by the human, not by an agent, and it is unverified here. The
  saved pages themselves are conclusive for the pages they cover.

## (c) "explicit set of parametric rules ... proven for ALL parameter values by a symbolic checker": MET
I read code/prove.py line by line.

**Linear rules (even, odd, Eodd, Dstep)**
- The parameter is k = j + K with j a symbolic nonnegative integer, and K = 1 for every rule. That equals each
  domain's lower bound (k >= 1), so no concrete cases are needed and none are used. The log shows "concrete cases
  k<K: []".
- Each symbolic run of 1s is held as a block (11)^j.
- Acceleration uses ctx_shift_sim and shift_sim. Each simulates one block copy together with its concrete travelling
  context, inside a closed window: leaving the window, halting, or more than 400/5000 steps rejects the shift.
  Success requires the same state, the same relative head position and an unchanged context. That is a valid
  induction step, so the shift holds for every copy count n >= 0, and the step count is added as (per-copy) * n.
- The tape is bounded by E markers. Reading one raises Fail, so cells outside the window are provably untouched.
- The output is matched by structural equality of the canonical token lists, with sympy polynomial equality on the
  exponents and on the step count. Equal token lists imply equal strings for every j, so this direction is sound.
- Both values of x are checked.

**Drain rules (even_drain, Ddrain1, Ddrain3)**
- prove_induction checks the base case k = 0 by concrete simulation.
- Each step k -> k+1 composes previously PROVED rules in explicit contexts. It checks the domain of each sub-rule
  instance with a polynomial test, allows the induction hypothesis only at exactly k, and requires the step sum to
  equal the stated count at k+1, symbolically.
- Real induction over all k.

**Results of the run on the server**
- RESULT PROVED for all 7 rules: four linear with K=1, three by induction.
- The free-text proof fields in rules.json match the engine's logged shifts:
  - even: right shift in state A with context 011 and head at offset 0, 10 steps per copy; left shift with empty
    context, 2 steps per copy.
  - Eodd: shifts with head@2 and head@0.
  - Dstep: right shift in state B with context 1111.
  - Drain step terms: 12k+9, 24k+25 and 24k+37.
- Controls:
  - All 12 controls in code/main_controls.py are rejected. They are meaningful: they include off-by-one step counts,
    a flipped bit, a shifted head, an x-dependence, a truncated window, a wrong induction step, a circular induction
    hypothesis, and a wrong exponent.
  - My 4 extra controls are also rejected: a step polynomial wrong only for k >= 3 (12k-3+(k-1)(k-2)), Dstep and odd
    with domains widened to k >= 0, and an altered output.
  - The parser test passes. Exponents and step counts using j, including the complex-literal trap "2j", are rejected.
- The independent naive brute force (code/bruteforce.py, own parser and simulator, k <= 12, random exteriors) passes
  every real rule and catches every mutant.

**Latent checker gap (not triggered)**
- build_tape silently drops a negative constant part of an input exponent, because Python's [b]*c with c < 0 is [].
- With K = 1, every input exponent here has a positive constant (2j+2, 2j+3, 2j+3, 2j+5), and peeling and regrouping
  never create negative constants. These seven proofs are therefore unaffected.
- The checker is custom Python and sympy, not Lean or Rocq. p1 explicitly allows "a symbolic checker".

## (d) "every rule application also matching a naive simulation for the first 1e8 steps": MET
**Scheduling in code/replay_v2.c (match_all)**
- At every time t <= 1e8 when the state is A, the scheduler tests every rule's input pattern anchored at the head.
- Each pattern's 1-run is bounded by 0s on both sides, so k is determined uniquely at each position and exhaustive
  matching needs no other choice.
- Domains are respected: k >= 1 for even, odd, Eodd and Dstep (r>=2, r>=3, q>=3, m>=5); k >= 0 for the drains,
  including the trivial k = 0 cases.
- This checks every occurrence in the naive run, which is a superset of the applications an accelerated simulator
  would make.

**Checks at the due time t + steps**
- The state must be A.
- The head must be at L + hoff.
- The full window must match (memcmp).
- The head must never step outside [L, R]. This is enforced by sentinel counters at L-1 and R+1; the head moves one
  cell per step, so it cannot leave without landing on one of them.
- Applications that start at t <= 1e8 are followed until they resolve, at t = 103007095.

**Result**
- 8,365,935 applications scheduled, all passed, 0 failures, 0 pending.
- The steps+1 control and the flipped-output-bit control each give 0 passes.

**BB(5) validation**
- The champion runs for 47,176,869 defined transitions and then halts reading E0. That is step 47,176,870 when the
  halting step is counted, and it leaves 4097 ones because the undefined halting transition writes nothing. This
  matches the bbchallenge convention.
- The sim path uses the same parse and step code as the rule path, so it validates the semantics.

**Composition of the count**
- 8,316,353 of the 8,365,935 applications are the even rule.
- 174 are zero-step trivial drains.
- This inflates the headline number but not its truth.

## (e) Hidden quantifiers, stretched definitions, bundling, subsumption, null model
- **Quantifiers.** "For ALL parameter values" holds within each stated domain, which is the meaning p1 intends.
  "Every application ... first 1e8 steps" is read as every start time t <= 1e8, and it is satisfied in that strong
  form.
- **Bundling.** p1 asks for "a set of parametric rules", so seven rules count as one set. All seven are proved and
  replayed; none is carried by another.
- **Stretched "macro-rule reduction", tested with a null model.** Local identities could be true but irrelevant to
  the run, so I instrumented the replay to measure coverage.
  - The union of the time intervals of non-trivial applications covers essentially all of the first 1e8 steps
    (102,991,294 steps covered, the intervals running past 1e8).
  - A greedy accelerated run (take the longest matching rule, otherwise one naive step) reproduces the first 1e8
    steps with 268 macro applications plus 15,801 naive steps.
  - So the rules are a genuine acceleration of this run, not vacuous patterns.
  - They are not a closed rule system for the whole behaviour: naive steps remain between applications, and nothing
    is said about halting. CLAIM.md says this itself.
- **Form of the rules.** The rules are local window rules with context ("0^k A0 1^(2k) 00 -> A000 1^(3k)"), not
  whole-configuration rules A(n) -> A(f(n)). p1 offers that form only as "e.g.", so this is acceptable.
- **Subsumption.** No saved wiki or sheet source gives these or equivalent rules for the machine or any of its 240
  images, and the classification "Quadratic Mess" is not a rule set. A general accelerated simulator with an
  automatic proof system might derive similar rules, but p1's test is the wiki/holdout notes, and the notes do not
  contain them.

## Verdict
- Every clause of p1 is met literally on the saved evidence, which I re-ran. The one notes item that remains
  human-reported (the wiki full-text search) is not needed for the literal clause.
- The full success criterion is not met and was not claimed.

confirmed_scope: For 1RB1LC_1LC0RD_0LE1LA_0RF1RA_1LA0LA_---0RB (line 523 of BB6_holdouts_663.txt, the newest BB(6) file on Holdouts_lists, whose saved wiki pages and annotated-sheet notes as fetched 2026-10-17T17:10Z contain no rule set), the seven context-preserving parametric rules in result/rules.json are proved for every parameter value in their stated domains by the sympy-based checker code/prove.py (block-copy induction for even/odd/Eodd/Dstep, k-induction for the three drains), and all 8,365,935 occurrences of their input patterns starting at steps 0..1e8 of the blank-tape run match naive single-step simulation; this is a partial acceleration only and says nothing about whether the machine halts.

pass: true
