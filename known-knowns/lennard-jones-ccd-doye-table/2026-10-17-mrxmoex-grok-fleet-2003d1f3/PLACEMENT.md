# Placement note (for moe; not part of the upstream text)

**What this replaces.** This package supersedes the held LJ-only package `../ccd-lj-errata-combined/` (left untouched for reference). Section (A) carries over its five LJ errata unchanged. Section (B) adds the Morse 63C sign erratum. File only this package, not both.

**Category.** These are data-integrity errata for two tables of the Cambridge Cluster Database (Cambridge/Wales group): the Lennard-Jones tables (A) and the Morse table (B). They are not record claims and go through the errata path, not the record-claim review. This is the same category as our CCD Morse 32E file-swap erratum, issue #240.

**Recommendation: ONE PR, ONE family dir, both sections together:**
`known-knowns/lennard-jones-ccd-doye-table/2026-10-17-mrxmoex-grok-fleet-<id>/`
- `<id>` = first 8 hex of the sha256 of the main object, set at filing time. **Placeholder, not yet filled in.** This package ships no coordinate object, so moe decides at filing what counts as the main object: README.md/PR_BODY.md, or SOURCES.csv. We suggest SOURCES.csv, because it is the evidence manifest. Recompute after any final edit.
- Use PR_BODY.md as the body.
- Cross-reference #240: (A) follows the #240 convention for the CCD LJ errata family, and (B) 63C is a second Morse-table erratum next to the 32E file swap in #240.

**Why one dir, not two siblings.** The repo's bank entry `lennard-jones-ccd-doye-table` already covers the CCD Morse table (its partial win p2 points at the Morse tables page), and the 32E Morse package for #240 was itself staged under `known-knowns/lennard-jones-ccd-doye-table/2026-10-16-mrxmoex-grok-fleet-aff76a3b/`. Splitting would give two dirs that share one SOURCES.csv, one run_checks.sh and one PR body. Keeping one dir with sections (A) and (B) keeps the repro, hashes and body self-consistent.
- Fallback, only if the maintainer wants Morse errata separate: a sibling dir `known-knowns/lennard-jones-ccd-doye-table/2026-10-17-mrxmoex-grok-fleet-<id2>/` holding only (B). That needs a split SOURCES.csv, run_checks.sh and body. We do not recommend it.

Why a PR rather than an issue:
- The maintainer asked for related findings to be folded into one package.
- This package ships a runnable repro plus SOURCES.csv, like scu-errata-combined. An issue suits a finding with nothing to run, like the 32E note.

If the maintainer prefers CCD errata as issues (as with #240), the README body works unchanged as a single issue.

**Check before filing.** Confirm that `known-knowns/lennard-jones-ccd-doye-table/` is still the family path on upstream main (it is the bank-entry slug and the path used for 32E). The earlier LJ-only draft suggested `cambridge-cluster-database-lj` as an alternative. Use that only if the family dir does not exist.

**Not included on purpose.** Eight unresolved Morse cells (31D, 47A, 66B, 70B, 75B, 147A x3) are mentioned only as a one-line open question in Not claimed. They are not errata.

**Status.** Review-ready. Nothing has been filed, pushed or sent. moe presses the button.
