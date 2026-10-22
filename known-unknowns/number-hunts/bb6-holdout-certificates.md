# Decide official BB(6) holdout machines with independently checkable certificates

🔢 **Number hunts** · harvest (many cells or partial wins within reach) · tractability ★★☆☆☆ · compute: laptop-hours · open as of 2026-10-20

## The problem

The bbchallenge collaboration keeps lists of 6-state 2-symbol Turing machines whose halting status from a blank tape is undecided. BB(6) has 663 holdouts up to equivalence and 1417 without in @mxdys's list of 16 October 2026 (BB(6) wiki page, revision of 2026-10-17; the informal count there is still 998; late September: 815 and 1674). The newest count on Holdouts_lists is 663 machines (@mxdys, 2026-10-16, file BB6_holdouts_663.txt; lists of 797, 778, 740 and 698 were posted between 2026-09-30 and 2026-10-15), after FAR and other deciders removed many machines, so what remains is the hard residue. Target: prove that one or more machines on the newest official BB(6) list never halts (or halts), with a machine-checkable certificate. (BB(2,5) and BB(3,3) holdouts are handled by the separate target bb33-bb25-cryptid-adjacent; Cryptids such as Antihydra by antihydra-collatz-cryptid.)

## What counts as a win

CONFIRMED requires all of the following, checked against the live primary table https://wiki.bbchallenge.org/wiki/Holdouts_lists at verification time (direction: min; each newly decided holdout lowers the live count). (1) The machine's standard-format string, or its bbchallenge lexical normal form after state/symbol permutation and mirror normalization, appears in the NEWEST BB(6) holdout file linked from https://wiki.bbchallenge.org/wiki/Holdouts_lists AT VERIFICATION TIME (on 2026-10-20 the newest linked file is BB6_holdouts_663.txt of 2026-10-16 by @mxdys; new lists appear every few days, which makes check (4) essential). Record the file name, its date and its sha256. The claim must name which list it targets (informal or formal holdout list). (2) Non-halting: a finite certificate, such as a CTL/FAR automaton, inductive symbolic templates, or a Lean/Rocq proof with no sorry/admit/new axioms. For a Lean/Rocq proof, the formal TM model must be shown equal to the bbchallenge semantics (start state A, blank tape of 0s, the bbchallenge head-move convention, halting exactly when an undefined transition is read) and must be tested on known machines: under the formal model the BB(5) champion must halt at step 47,176,870. Any use of native_decide (which adds the Lean.ofReduceBool axiom) must be flagged in the report together with the #print axioms / Print Assumptions output. A checker that shares no code with the search must verify three things over the WHOLE certificate language, not only over configurations seen in simulation: (a) the blank-tape start configuration is in the language; (b) the language is closed under one TM step, checked as a language inclusion with automata operations or symbolic case analysis covering every template instance; (c) no configuration in the language reads a halting (undefined) transition. (3) Halting: an exact step count reproduced by two independent simulators, at least one of them a published accelerated simulator, plus a naive single-step simulator if the count is <= 1e10. (4) The machine is not marked decided on the BB(6) wiki page, the linked sheet, or the bbchallenge Discord #bb6 channel when it can be checked. If decided status cannot be confirmed, report 'NEW, PENDING COMMUNITY CHECK', not a record. Heuristic ('probviously') arguments never count.

## Partial wins

- **p1:** Verified macro-rule reduction: for a machine in the newest BB(6) holdout file whose wiki/holdout notes give no accelerated rule set, an explicit set of parametric rules (e.g. A(n) -> A(f(n))) proven for ALL parameter values by a symbolic checker or Lean/Rocq (no sorry), with every rule application also matching a naive simulation for the first 1e8 steps.
- **p2:** Cryptid-style reduction: for such a machine, a mechanically checked proof that it halts if and only if an explicitly stated arithmetic (Collatz-like) condition holds, where the wiki has no equivalent reduction for that machine (or any machine equivalent to it under normal form) at verification time.

## How a win is checked

Download the newest holdout file, compute the canonical normal form of the claimed machine, and grep for it. Run an independent checker (about 100 lines of Python) for the certificate class. For automaton certificates it checks closure as an inclusion test with automata operations (product/complement emptiness), not by sampling. Simulate 1e8 naive steps as a sanity check. For Lean/Rocq, build in a clean project, run #print axioms / Print Assumptions, and diff the top-level statement against the Coq-BB5-style TM semantics (start state A, blank 0 tape, head-move convention, halt on an undefined transition). Run the formal model on the BB(5) champion (must halt at step 47,176,870) and on a known non-halting machine before trusting it, and flag native_decide. For partial wins, re-derive each macro rule symbolically and replay it against a naive simulator.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://wiki.bbchallenge.org/wiki/Holdouts_lists>

## Sources

- <https://wiki.bbchallenge.org/wiki/Holdouts_lists>
- <https://wiki.bbchallenge.org/wiki/BB(6)>
- <https://arxiv.org/pdf/2509.12337>
- <https://wiki.bbchallenge.org/wiki/BB(2,5)>
- <https://bbchallenge.org>
- <https://github.com/M-Abozaid/bb6-nonhalt-1RB1RC_1LC0RF>
- <https://wiki.bbchallenge.org/wiki/BB(3,3)>
- <https://arxiv.org/abs/2509.12337>
- <https://wiki.bbchallenge.org/wiki/Cryptids>
- <https://wiki.bbchallenge.org/w/images/6/69/BB6_holdouts_663.txt>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Pull the BB(6) holdout list and cluster machines by behavior signatures: tape-growth exponent, repeated macro-symbols, counter-like Collatz rules. Attack the largest cluster of 'translated cycler with growing counter' machines with one parametric certificate generator instead of one machine at a time.
- Implement a weighted-automaton or 'regular language + linear counter' certificate class (a Presburger-closed tape language). It strictly generalizes CTL, and existing FAR deciders miss counter-dependent invariants.
- Run accelerated simulation to extract the inductive rules (A(n) -> A(f(n))). For machines whose rule is affine with no parity split, derive the non-halting proof mechanically by solving a linear recurrence, then emit a symbolic certificate.
- Use the bbchallenge 'Collatz-level' taxonomy: target machines whose extracted map is Collatz-like but with a contracting drift that is provably monotone (a 2-adic Lyapunov function), which avoids the Antihydra-type parity problem.
- Do not rebuild FAR: the remaining 797 survived FAR, CTL and loop deciders. Spend effort on certificate classes that strictly generalize them (counter-augmented regular languages, Presburger-closed tape languages).
- Check the bbchallenge Discord and wiki for same-day AI-agent (GPT6/Aristotle) activity on the chosen machine before investing in it.
- Run the cheap deciders on every holdout first (cyclers, translated cyclers, bouncers, FAR with growing DFA size via SAT/pysat). Then cluster the residue by behaviour, such as counters, bouncers with growing gaps, and Collatz-like rules.
- Symbolic rule extraction: compress the tape into run-length macro blocks, infer affine 'shift rules' (block^n patterns maps to block^{an+b}), and prove the inferred rule system non-halting by induction with Z3 (pip install z3-solver). Then emit a Lean proof skeleton.
- Weighted or counter automata certificates (WFAR) found by an ILP search over weights. These catch machines with unbalanced counters that plain DFAs miss.
- Translate a holdout's macro-dynamics into a Fractran program or Collatz-like map. Where the map has an obvious invariant, such as mod-2^k drift or a monotone potential, that proves non-halting. Where it is Hydra-like, mark it as a cryptid and move on.
- BB(3,3) and BB(2,5) residues are tiny. Aim the full ten-core budget at one machine for a whole day rather than many.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Machines decided on Discord or the Google Sheet but not yet removed from the file. Report these as 'pending community check'.
- Off-by-one or normalization errors: a machine equivalent under symbol/state permutation may already be decided.
- Certificates that check closure only for reachable configurations seen in simulation, not for all configurations in the language.
- 'Probviously' heuristic arguments (random-walk estimates) are NOT proofs.
- Cryptids (Antihydra, Hydra, Bigfoot, Space Needle, Lucy's Moonlight) encode Collatz-like problems. Do not count heuristic progress on them here.
- The remaining machines (663 on 2026-10-16) survived FAR, CTL and loop deciders. A 'new' decider that only reproduces FAR will find nothing.
- Other agents (GPT6/Aristotle) are already active on bbchallenge holdouts, so check for duplication the same day.
- A machine may be solved between list updates. Check the wiki and Discord-mirrored lists at claim time.
- Equivalence: proving the mirror image of an already-decided machine is not new.
- Lean proofs using sorry, axiom, or unchecked native_decide. The wiki notes some 'proofs in Lean using GPT6' are pending verification.
- Cryptids (Antihydra, Hydra, Bigfoot) encode open Collatz-like problems. Heuristic or probabilistic arguments do not count.
- Simulation-only 'non-halting' evidence.
- A Lean proof of the wrong statement, where the TM encoding or semantics differs from bbchallenge's (start state, tape conventions, an off-by-one step count). Test the formal model on known machines.
- The informal and formal holdout lists differ. Say which one the claim targets.
- Many agents (Aristotle, GPT6-based) are attacking the same lists. Re-check the wiki and Discord-mirrored lists at claim time.
- Newest-list confusion: a count can be announced before its file is posted (on 2026-10-03 the 797 count of 2026-09-30 had no file; it is now BB6_holdouts_797.txt), and an older file still contains machines decided since. Membership in a file is not proof that a machine is still undecided.
- A formal model that has not been run on the BB(5) champion (halts at step 47,176,870) may encode the wrong semantics; native_decide is a trusted-compiler axiom and must be reported, not hidden.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/number-hunts/bb6-holdout-certificates.md
```

Already set up? Say `run V3R1T4S on bb6-holdout-certificates`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `bb6-holdout-certificates`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
