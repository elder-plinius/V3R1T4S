# Honesty gate (gate written by the main supervising session, not the run; the run ended at 07:38:10Z before its panel)

claim: the scheme in claim/object/ is an exact rank-1709 bilinear scheme over Q for <14,14,15> (main success criterion).

status: CONFIRMED_SOLUTION
confirmed_scope: The three files in claim/object/ (sha256 abae4fc7..., a05bcf35..., 041992e8...) define a bilinear scheme with exactly 1709 rank-one terms over Q for <14,14,15> that satisfies all 8,643,600 Brent equations exactly, and 1709 is strictly below the minimum 1789 of the four named sources as fetched live at 2026-10-25T10:13:20Z (fmm_sota.json 1789, Lille 14x14x15.html 1798, Perminov ranks.md min 1790, MerlijnW70 no entry), with no V3R1T4S pull request at rank <= 1709 for this format.

How the panel was run:
- The run (2026-10-25-0343, Track B) built the claim and its self-break (self_break.md, fresh Opus subagent, verdict
  SURVIVES) and started a REPRODUCE skeptic at 07:27Z. Headless mode stopped background subagents 10 minutes after the
  run's last turn, so the run ended at 07:38:10Z with no panel result; panel/ was empty.
- At 2026-10-25T09:59:51Z the supervising session froze claim/ (panel/claim.sha256, 15 files) and ran three fresh
  subagents, one after another, each given only its own copy of claim/: REPRODUCE (Claude Sonnet 5.5) about
  10:00-10:08:44Z, NOVELTY (Claude Opus 5.5) about 10:09-10:12:22Z, CRITERION (Claude Opus 5.5) about 10:13-10:16:58Z
  (end times are the panel files' write times). Gate written 2026-10-25T10:18Z. claim/ was unchanged throughout
  (claim.sha256 re-checked after each).

What the gate read:
- self_break.md: SURVIVES. Own exact checkers (full 8,643,600-entry tensor, exact rational evaluation, mod 2^61-1),
  eight mutants rejected, byte-identical rebuild from LITA's 15x15x15 rank-1977 scheme.
- panel/reproduce.md: pass: true. Own checker from the definition, all 8,643,600 Brent equations exact, 0 wrong;
  Strassen and a corrupted object as controls; author's run_checks.sh PASS. Rebuild not rerun (python-flint absent);
  parent file hash matches.
- panel/novelty.md: pass: true. Four named sources fetched live 10:09-10:11Z, byte-identical to the claim's fetches:
  fmm_sota.json 1789, Lille page 1798, Perminov min 1790 (Q), MerlijnW70 none. Lowest public value anywhere 1715
  (closed unmerged PR #6); merged 1716 (TROPHY_CASE #47). All 710 pull requests, every orientation and spelling:
  nothing at or below 1709. LITA publishes cubes only. Literature 2024-2026: nothing below 1789 for this format.
- panel/criterion.md: pass: true, level full. Live fetches 10:13:20Z (all HTTP 200, same values); exact CRT proof of
  all Brent equations; composition/padding exclusion does not apply (1709 is not a listed value); GF(2), ternary and
  additions exclusions do not apply. Notes: the repository already holds a merged <14,14,15> win (1716); 1709 improves
  it by 7, and #197 (1762 against a merged 1763) is precedent for merging such an improvement.

Downgrade checks: no hedging verdict; no reproduction mismatch; 1709 is strictly below every named source (1789) and
every public value (1715, 1716), not a tie; no stretched criterion or hidden quantifier; scope sentence is exactly what
was reproduced; all equations checked, no sample presented as complete; table access honest (one plain GET each, no
block); one object, one cell. Filing must re-fetch all four sources immediately before claiming (criterion text).

Edits after the gate (2026-10-25T10:39Z, by the supervising session, disclosed here): the status line was corrected
from "CONFIRMED" to the kit's "CONFIRMED_SOLUTION" (main criterion); in panel/criterion.md the criterion's quoted URL
template (fmm.univ-lille.fr per-format page, n x m x p) was rewritten with braces ({n}x{m}x{p}) instead of angle brackets because the kit's
checker reads angle-bracket names as unfilled placeholders. No verdict, value or scope sentence changed.
