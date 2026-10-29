# Self-break summary (contributor text, unverified)

Summary of the run's own attempt to refute the claim, done by a fresh Opus subagent in the run before the panel. Its
verdict was SURVIVES. The full file names the run's private working folders and is not shipped; the facts below are
copied from it.

- **Own checker, written from the definition before reading the author's.** Three methods on the object: (A) an exact
  check of the full 8,643,600-entry tensor (denominators cleared, integer arithmetic proven overflow-free first),
  (B) exact rational evaluation of C = AB on three random integer pairs, (C) the same evaluation mod 2^61-1. All pass;
  1709 terms, no zero factor, no index out of range or duplicated, no two terms with proportional paired factors (so
  no merge lowers the count), every fraction in lowest terms, the denominator set equals the list in CLAIM.md.
- **Eight mutants, all rejected:** drop the last term; drop term 700; add 1/39 to one v coefficient; flip the sign of
  one w coefficient; transpose u in every term; transpose w to the C^T convention; transpose u in term 5 only; empty w
  factor in term 3.
- **Author's checkers** (`run_checks.sh`): output identical to the expected output, about 3 min 55 s.
- **Rebuild** from LITA's published 15x15x15 rank-1977 scheme with python-flint 0.9.0 and numpy 2.5.4: the five printed
  step lines and the final `SAME` match REPRODUCE.md; sha256 of the parent file 94515288...a102a33 and its git blob
  sha1 65821484d954b4aade06cbda624932ba2a481f7b (listed in LITA's repository tree) match.
- **The run's own two exact checkers named in PREREG.md** (integer expansion of every term after clearing denominators,
  and exact slice products with python-flint) both printed PASS on the saved scheme, and had been tested on a merged
  record (PASS) and on planted negatives (FAIL) before use.
- **Criterion read literally:** the four sources gave 1789 (fmm_sota.json), 1798 (Lille per-format page), min of 1798,
  1798 and 1790 (Perminov docs/ranks.md) and no scheme (MerlijnW70/fmm-schemes), all fetched with HTTP 200 between
  07:03:39Z and 07:05:03Z on 2026-10-25; 1709 is below the minimum 1789 (margin -80) and below the repository's own
  1716 (merged) and 1715 (closed pull request #6). The composition clause does not apply: 1709 is not a listed value
  for this format, and the construction is a slice-and-reduce of a published scheme, not a composition, padding or
  block split.
- **Table access audit:** one plain GET per source with the User-Agent "V3R1T4S-research-agent (honest single GET)",
  no cookies, no retries; the three HTTP 000 rows in the fetch log are local argument errors that sent nothing (see
  the-record-we-beat/TABLE_RECORD.md).
- **Caveats it listed (none changes the verdict):** the pull-request list and TROPHY_CASE.md were last fetched about
  68 minutes before the claim (the NOVELTY skeptic re-read all of them at 10:09-10:14Z, see panel/novelty.md); every
  source must be re-fetched immediately before filing; the Perminov README and MerlijnW70 README were not read at that
  point (docs/ranks.md and the full repository tree were; the NOVELTY skeptic read the MerlijnW70 README).
