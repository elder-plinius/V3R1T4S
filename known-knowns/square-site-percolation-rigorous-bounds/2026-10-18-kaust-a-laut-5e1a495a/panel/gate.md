# Honesty gate (RUN.md step 7): run 2026-10-18-1841, square-site lower bound

Gate written 2026-10-18T19:02:24Z by the run's main session, the setup session (Claude Code, claude-opus-5-5) working with the
human in chat. The panel ran in three fresh subagent contexts started from this session. Each was given only its own
copy of claim/ (panel/work/<role>/claim, identical to claim/ by MANIFEST.sha256) and told not to read anything else
in the workspace.

Read: panel/reproduce.md, panel/novelty.md and panel/criterion.md, each read in full by this session. Each ends with
pass: true and has a fresh-context line.

Downgrade checks:
- **Hedging panelist:** none.
  - CRITERION's confirmed_scope states its two dependencies plainly: the cited theorems of Fisher and Strassen, and
    the literature record for "best published". Both are the honest scope of a proof and of a novelty claim, not
    hedges.
  - NOVELTY says plainly that a search cannot prove a negative and that the Menshikov-Pelikh paper itself was not
    read. Both are true and both are standard.
- **Reproduction mismatch:** none.
  - REPRODUCE wrote its own exact checker from PROOF.md before reading the code. Its margins at depths 0-3 equal
    indep.py's exactly, and window.py's to within the outward rounding (always lower, by under 1e-13).
  - Its brute-force growth-process enumeration (no Lemma 2, three total orders) matched Lemma 2's formula in every
    history.
  - REPRODUCE.md runs twice were byte-identical.
  - CRITERION independently audited all 40 hull and round_out calls with an exact containment test and enumerated
    real histories up to step 4.
- **Value strictly better than the record:** yes. 0.5567 > 0.556, and > 0.5560829, the exact optimum of the 1996
  method.
  - NOVELTY's fetches ran from 2026-10-18T18:50:24Z to 18:54:23Z, under 6 hours before this gate.
  - Sources checked: the Ermakov thesis, all 51 works citing the 1996 paper (OpenAlex), arXiv API queries, Russian
    and Chinese searches, and the upstream TROPHY_CASE.md and 148 open PRs.
  - Nothing above 0.556 was found. Two blocked URLs (403, 503) were not retried.
- **Scope wider than reproduced, sample presented as complete, capped search as exclusion, probable prime as proof,
  table evasion, bundling:** none. This is one claim, one inequality.

Corrections the panel asked for. None affects the result. claim/ is left exactly as panelled; these go into the
package as an errata file.
- table/literature_record.md mis-describes arXiv:2405.07345. It is Koehler-Schindler and Sulser, "Critical
  probabilities for positively associated, finite-range dependent percolation models", which uses a lower bound for
  site percolation on the truncated square lattice as an input. It is not a bound for Z^2 (NOVELTY).
- PROOF.md, Section 0: the total order should be of type omega, for example an enumeration of Z^2 starting at O, so
  that "the least vertex with ..." always exists (REPRODUCE).
- PROOF.md, Lemma 2: the displayed density omits the factor 1[eps(O) open]. That factor is implied after the first
  step (REPRODUCE).
- The root step is checked in code/validate.py, which prints its margin but does not assert it is positive, and is
  not recorded in result/bound.json. It was confirmed independently by REPRODUCE and CRITERION (1.470118695e-2)
  (CRITERION).
- CLAIM.md's phrase "enlarged to the whole exploration-tree history" should read "exact to depth 3, with universal
  outer cones beyond" (CRITERION).

status: CONFIRMED_SOLUTION
confirmed_scope: Assuming Fisher's inequality p_c(S) + p_c(S*) >= 1 and Strassen's coupling theorem, claim/ proves p_c^site(Z^2) >= 5567/10000 = 0.5567 by the van den Berg-Ermakov growth-process comparison, with the deciding computations (window.py's depth-2 and depth-3 cone checks at p = 4433/10000 and validate.py's root step) in exact rational arithmetic and recheckable from claim/ with the Python standard library; that this beats the best published rigorous lower bound rests on the package's literature record naming 0.556 as that bound.
