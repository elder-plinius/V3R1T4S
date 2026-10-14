## Request for review: A(34,8,7) ≥ 603

This draft presents an explicit 603-word certificate and asks for review of its historical provenance and a checker defect. It is **not a claim of completed repository acceptance**. The package remains `PROMISING`.

The certificate contains 603 distinct binary vectors of length 34 and weight 7, with minimum pairwise Hamming distance 8. Its SHA-256 is `18b44fac5d5ff1d4895fd9de1240669eb71543b3e15599f7f864e090aa1491ad`.

Validation completed:

- Exhaustive checks of all 181,503 pairs and the four-subset packing condition.
- Exact reconstruction from the published 602-word baseline by removing 38 words and adding 39.
- Separate fresh-context REPRODUCE, NOVELTY and CRITERION model reviews, each signed off within its role. They were separate contexts sharing a filesystem, not human or external-institution reviews.
- Primary table fetched once at 2026-10-14T03:17:23Z, HTTP 200: 601–1175. Raw response SHA-256: `0f1b51bf71c0ca91aef82eef740cb0dd9f6be6c4014983213d0eefe0eb631cee`.
- Proposed checker patch passes 25 independently frozen regression cases, both acceptance-enlargement witnesses, a digit-separator regression, and all 39 original repository tests.

## Decisions requested

1. The original JSON contract specifies the mathematical criteria and exact checker; archived metadata supports pre-result ordering. A complete original dated `PREREG.md` with the prescribed null declaration is unavailable. Is this disclosed external-construction provenance acceptable?
2. The original `kit/check_run.py` mistakes standard C++ includes for unfilled placeholders. Please review the attached narrow patch. It preserves genuine placeholder and leak checks; it does not exempt entire C++ source files.

The original package gate fails on two include false positives plus the unconfirmed status. With the proposed checker correction, only the deliberately unconfirmed status fails. No upstream adoption or passing formal gate is claimed.

Credits: V3R1T4S's 602-word construction, Jordan Boisclair's credited 601-word seed, A. E. Brouwer's table, and William Echols' separately published 600-word comparison. The literature reviews found no stronger public result for this cell; they do not establish universal unpublished priority or optimality.

## Review layout

This proposed review directory is intentionally outside `known-knowns/`: the package is PROMISING and does not meet the formal claim-submission gate. It requests a maintainer decision, not an exception disguised as a confirmed claim.

- [Certificate and full package](package/README.md)
- [Maintainer note](MAINTAINER_NOTE.md)
- [Proposed checker patch](checker-fix/check_run_cpp_includes.patch), supplied as a patch for review; the repository checker is unchanged.
