# Computationally decidable open number-theory Erdős problems (erdosproblems.com)

🔢 **Number hunts** · harvest (many cells or partial wins within reach) · tractability ★★☆☆☆ · compute: laptop-hours · open as of 2026-10-20

## The problem

erdosproblems.com lists 1221 problems; the teorth/erdosproblems data file (2026-10-20) gives 588 'open' and 5 'open (Lean)' plus 49 in other open-type states (falsifiable 25, decidable 8, verifiable 7, not disprovable 6, not provable 3), about 642 in all. The site has a blog post titled 'Erdős problems in the OpenAI proofs' (08 Oct 2026), so re-check each problem's status on the day. Some number-theoretic ones are decidable by a finite certificate: an explicit counterexample, a finite exceptional set, or an explicit construction disproving a quantitative conjecture. FrontierMath Erdős (Adamczewski-Bloom, arXiv 2609.25050, 2026-09-06) selected 68 open problems, on which the best model (GPT-6 Astra) scored 3%. The teorth/erdosproblems wiki tracks AI contributions (e.g. #396, #513, #650 in Feb-Apr 2026). Target: pick an open problem whose resolution, or a clearly stated sub-question, is a finite checkable object, and produce it.

## What counts as a win

CONFIRMED only if: (1) the problem's page on https://www.erdosproblems.com/ shows status OPEN on the day of the claim, its comment/forum thread reports no resolution, and the teorth AI-contributions wiki has no entry resolving it; (2) the claimed result is a finite object (counterexample/construction/certificate) plus a short reduction proving that this object resolves the problem AS STATED on the site (exact quantifiers and constants; statements containing 'for sufficiently large n' or other asymptotic quantifiers cannot be resolved by a finite counterexample); (3) an independent re-implementation verifies the object. A proof-style resolution needs a Lean proof (elan/lake install allowed) that compiles without sorry and with a clean axiom audit. Otherwise it is reported as 'CLAIM, UNVERIFIED', with no claim.

## Partial wins

- **p1:** Explicit sub-question: a finite, independently re-verified object that settles a specific sub-question or special case that the problem's erdosproblems.com page (or its cited source) explicitly states as open at verification time, with the reduction to that exact sub-question written out.
- **p2:** Bound improvement: an explicit construction, independently re-verified, that strictly improves a numeric bound or constant the problem's page cites as the best known at verification time (direction as stated on the page), without resolving the problem.

## How a win is checked

The verifier fetches the problem page and re-reads the exact statement, checks that the reduction lemma matches it, and re-implements the certificate check from scratch in a separate script (no shared code). For Lean, it runs lake build and #print axioms. It also checks the comment thread, the AI-contributions wiki and the 68-problem FrontierMath Erdős list for prior or parallel work.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://www.erdosproblems.com/>

## Sources

- <https://www.erdosproblems.com/>
- <https://github.com/teorth/erdosproblems/wiki/AI-contributions-to-Erd%C5%91s-problems>
- <https://arxiv.org/abs/2609.25050>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Triage: scrape erdosproblems.com tags for number theory + 'open' and filter for statements with explicit finite parameters or 'is it true that for all n ≥ ...' forms that a counterexample could falsify.
- Use OEIS cross-referencing: many Erdős number theory problems relate to sequences. Extend the sequence far beyond the OEIS b-file and look for a pattern break that disproves the conjecture.
- Use SAT/ILP (pip install python-sat or OR-Tools) for problems about sets of integers with additive/multiplicative restrictions (Sidon-type, primitive sets, covering systems) to find explicit extremal constructions beating conjectured bounds.
- Covering systems: search for coverings with prescribed moduli properties via exact cover + CRT, and verify coverage by enumerating residues mod lcm.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- The #1 failure is that the problem was already solved in the literature or the site's statement differs subtly from the folklore version. The teorth wiki documents many such 'confused with another problem' cases.
- Erdős problems with 'infinitely many' or asymptotic quantifiers cannot be settled by finite data.
- Check this repository's results first to avoid repeating already-attacked items.
- Site status can lag. Also read the problem's comment/forum thread and the 68 FrontierMath Erdős problems list to avoid duplicating benchmarked items.
- An 'explicit counterexample' to a conjecture whose site statement includes 'for sufficiently large n' resolves nothing.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/number-hunts/erdos-problems-computational-nt.md
```

Already set up? Say `run V3R1T4S on erdos-problems-computational-nt`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `erdos-problems-computational-nt`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
