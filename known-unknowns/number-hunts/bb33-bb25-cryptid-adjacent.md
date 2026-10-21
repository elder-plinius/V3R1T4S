# BB(3,3) non-Bigfoot holdouts and BB(2,5) non-Hydra holdouts

🔢 **Number hunts** · harvest (many cells or partial wins within reach) · tractability ★★☆☆☆ · compute: laptop-hours · open as of 2026-10-20

## The problem

BB(3,3) has 6 holdouts (4 up to equivalence): Bigfoot, #397 ('similar to Wily Coyote'), the equivalent pair #153/#758 (flagged as a potential Cryptid) and the Wily Coyote pair #531/#532 (BB(3,3) page last edited 2026-09-17; the three Rocq formalizations of 2026-03-15, machines 650, 412, 279, are not among the 6). BB(2,5) has 59 formal holdouts (60 after mxdys' Rocq deciders of 2026-09-08; on 2026-10-09 prurq showed 1RB3LA1LA2RB2LB_1LB2RA4RA0RB--- halts using a Rocq-certified longitudinal simulator) and an informal list of 37 (2026-10-09; BB(2,5) page last edited 2026-10-17), including Hydra 1RB3RB---3LA1RA_2LA3RA4LB0LB0LA and the Bonus Cryptid 1RB3RB---3LA1RA_2LA3RA4LB0LB1LB; the 22-machine difference is covered by pending, not yet independently verified GPT6/Aristotle Lean proofs. Target: decide a non-Bigfoot BB(3,3) holdout or a BB(2,5) machine on the 37-list other than Hydra and the Bonus Cryptid, with a formal or independently checked certificate.

## What counts as a win

CONFIRMED under the same certificate rules as bb6-holdout-certificates (newest holdout file linked from https://wiki.bbchallenge.org/wiki/Holdouts_lists AT VERIFICATION TIME, normal-form match with file sha256, whole-language closure check by an independent checker or Lean/Rocq proof with no admits and a clean axiom audit, two-simulator step count for halting, not marked decided on the wiki/sheet/Discord, else 'NEW, PENDING COMMUNITY CHECK'), applied to BB(3,3) #397, #153/#758 or #531/#532, or to a BB(2,5) machine on the newest informal list other than Hydra and the Bonus Cryptid and not covered by the pending AI Lean proofs. Deciding one member of an equivalent pair counts once. Progress on Bigfoot, Hydra or the Bonus Cryptid does NOT count here.

## Partial wins

- **p1:** Independent audit of a pending AI proof: for one of the 22 BB(2,5) machines covered by the pending GPT6/Aristotle Lean proofs, either an independent confirmation (clean build, #print axioms showing only standard axioms, top-level statement diffed against Coq-BB5-style semantics, plus a cross-check by a certificate checker sharing no code) or a concrete defect (a sorry/axiom, a statement mismatch, or a failing step), where the wiki does not already record that machine's proof as independently verified at verification time. This is not a new decision.
- **p2:** Verified reduction: for BB(3,3) #397, #153/#758 or #531/#532, a mechanically checked proof (symbolic checker or Lean/Rocq) that the machine halts if and only if an explicitly stated arithmetic map/condition holds, where the machine's wiki page does not already give an equivalent proven reduction at verification time.

## How a win is checked

Independent certificate checker (whole-language inclusion test) plus a 1e9-step naive simulation for consistency; Lean/Rocq compile in a clean project with an axiom audit and statement diff. For the audit partial win, the verifier rebuilds the pending proof itself and reruns the independent cross-check.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://wiki.bbchallenge.org/wiki/BB(3,3)>

## Sources

- <https://wiki.bbchallenge.org/wiki/BB(3,3)>
- <https://wiki.bbchallenge.org/wiki/BB(2,5)>
- <https://wiki.bbchallenge.org/wiki/Holdouts_lists>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Extract each holdout's macro rules with an accelerated simulator. Many 'almost-Cryptids' reduce to a map with one parity split plus an exploitable invariant mod 2^k or mod 3^k (a finite automaton on residues), giving a proof by finite residue-class closure.
- 2-adic/3-adic invariants: show the orbit never enters the halting residue class by exhibiting a set of residues mod M closed under the map. Search M up to 2^20 x 3^10.
- Search for a Lyapunov/potential function as an integer linear combination of tape-block counters that strictly increases, using LP/ILP over symbolic rule effects.
- Cross-check with the Rocq repository's existing proof patterns and reuse their certificate format to make formal adoption easy.
- Auditing the pending AI Lean proofs is cheap and useful; finding a statement mismatch matters as much as confirming one.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Bigfoot/Hydra are Collatz-hard; heuristic 'probviously' arguments do not count.
- Duplicating the active AI Lean campaign on BB(2,5).
- Equivalence classes: deciding one member may already be implied by a decided twin.
- 153/758 is flagged as a potential Cryptid, so expect Collatz-hardness.
- The 22 AI Lean proofs on BB(2,5) are unverified. Independently checking one is a useful contribution but is NOT a new decision.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/number-hunts/bb33-bb25-cryptid-adjacent.md
```

Already set up? Say `run V3R1T4S on bb33-bb25-cryptid-adjacent`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `bb33-bb25-cryptid-adjacent`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
