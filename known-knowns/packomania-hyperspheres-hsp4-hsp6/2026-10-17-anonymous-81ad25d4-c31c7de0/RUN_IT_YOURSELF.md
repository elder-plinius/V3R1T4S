# Reproduce the saved object

From this directory run `python verify-it-yourself/check.py`; the expected final line is PASS. No dependencies beyond Python standard library are required. All geometric inequalities are evaluated as exact rational inequalities, with no tolerance, at the reported conservative radius. Source provenance and the comparison witnesses are in the-record-we-beat/. The original independent mpmath50 results appear in panel/.

For the full 50-digit source-object check, install the optional pinned requirements in a local virtual environment. Obtain hsp4-119.txt from Packomania's HSP4 coordinate archive and hsp4_119.txt from Moki & Julio's HSP4 ZIP, using the URLs and hashes in record.json. Keep original bytes. Run `python verify-it-yourself/recheck_source_objects.py PATH_TO_hsp4-119.txt PATH_TO_hsp4_119.txt`. This checks both member hashes, every pair and wall, baseline parser sanity, the two improvement margins, and the non-isometry witness. Third-party coordinate data are deliberately not redistributed.

To rebuild through search, follow how-we-built-it/README.md and its exact command. Search is capped by wall clock and is not promised to reproduce the same trajectory or object. Live record and queue comparisons can change; the offline checkers validate only the recorded snapshot comparison.
