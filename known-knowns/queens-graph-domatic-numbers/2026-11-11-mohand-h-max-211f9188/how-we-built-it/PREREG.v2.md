# PREREG.v2 — correction of the checker clause only (written 2026-11-11T18:38:36Z, AFTER a result existed)

PREREG.md named two checkers for a tdom claim: check.py and check_bits.py "called with kind tdom". The negative control
run in this session (attempts/skeleton-tdom/output/check-found-Q10.txt) shows that check_bits.py ignores the kind and
tests plain domination only: it printed PASS for a grid that is not a total domatic partition. It is therefore not a
valid judge for tdom and is dropped. Nothing else in PREREG.md changes (criterion, cells, search design, null design).
Judges for a tdom claim from now on: check.py with kind tdom (rejects both negative controls), a third check written
from the definition in this run (same output file), and the three-skeptic panel's own checkers.
This change makes the rule stricter, not looser: the dropped checker was the one that could not fail.
