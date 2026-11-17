# PREREG.v2 (frozen 2026-11-11T10:47:00Z; a design fix after a technical failure, before any PRE-condition score exists)

PREREG.md stays in force except for the one change below. This file was written because the first PRE run
(group v2022-10-05, 10:44:32Z) failed on every case: LIRICAL 2.4.1 aborts each analysis with
"NodeNotPresentInGraphException: Item not found in the graph: HP:0001180" because the 2022 phenotype.hpoa cites HPO
terms that are obsolete or alternative ids in hp.json v2026-06-06 (attempts/lirical-temporal/output/v2022-10-05_PRE.log;
its CSV is empty). No PRE score exists. The condition-C CSVs already written (group v2022-10-05; v2023-10-09 in
progress) have not been scored or opened; their data directory is unchanged.

## Change
- PRE data directories use the historical phenotype.hpoa with its HPO ids mapped onto the v2026-06-06 ontology that
  LIRICAL loads (the same convention as run 1's audit): alt_id -> primary id; obsolete with replaced_by ->
  replacement; any term that is still not a live (non-deprecated) node of hp.json v2026-06-06 -> that annotation row
  is dropped (HP cells in onset/frequency/modifier likewise mapped or blanked). Code: attempts/lirical-temporal/code/map_hpoa.py;
  counts: attempts/lirical-temporal/output/map_hpoa.out (at most 2,243 rows remapped and 94 dropped per release, of
  about 236,000-283,000 rows). Applied to v2026-06-06 the mapping is the identity (byte-identical file), so condition
  C is unchanged.
- Why this and not release-specific hp.json files (the other declared option): it holds the ontology fixed, so the
  C-vs-PRE difference isolates the annotations (the quantity p3 asks about), it needs no further download, and it
  cannot drop phenopacket terms that a 2022 ontology lacks differently between the two conditions.
- Groups whose PRE run started before the swap are rerun with the mapped file (same command). Everything else
  (sample, order, statistics, null, escape hatches, claim rule) is unchanged; E1's 11:25:00Z cap still applies to
  the main sequence, and reruns go after it only if time allows inside the same cap.
