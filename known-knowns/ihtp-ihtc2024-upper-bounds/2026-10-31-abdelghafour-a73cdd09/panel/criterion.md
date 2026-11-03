# CRITERION panelist: i18 (IHTC-2024 IHTP upper bounds), partial win p1

confirmed_scope: Under IHTP_Validator.cc (sha256 0b56fa75…a8afa, compiled by me with g++ -O2 -std=c++17), claim/sol_i18.json scores 0 hard-constraint violations and total cost 37625 on public instance i18 (byte-identical to i18.json in ihtc2024_competition_instances.zip, sha256 0cb52506…0ad3e), strictly below the 37650 in the i18 row of the organisers' upper-bound table as snapshotted 2026-10-31T00:02:47Z, which meets partial win p1; the full criterion's literature/special-issue condition is left to the NOVELTY panelist, and I did not re-fetch the table live or independently check the validator's repository origin.
context: subagent (Claude Code Agent tool, fresh context)

## Checks performed
- Instance identity: downloaded ihtc2024_competition_instances.zip once (30 non-__MACOSX entries, i01-i30); extracted entry `i18.json` by exact name; sha256 0cb5250654114f73c90933cb6096b1bcb11bbd6669dae96eeff37abb51f0ad3e equals claim/i18.json.
- Table row: claim/ihtp_table.html (sha256 2b69fe2e…f363), "Upper bounds" section, "Public dataset" table, row `i18` -> Cost 37650. This is the i18 public-set row (not an m-instance).
- Validator run (my build): sol_i18.json -> Total violations = 0, Total cost = 37625 (RoomAgeMix 5, RoomSkillLevel 121, ContinuityOfCare 792, ExcessiveNurseWorkload 0, OpenOperatingTheater 750, SurgeonTransfer 7, PatientDelay 2650, ElectiveUnscheduledPatients 33300).
- Null model: published_sol_i18.json -> 0 violations, 37650, matching the table, so the validator/instance pairing reproduces the listed bound; improvement is 25 (about 0.066%).
- Structure sanity: solution lists all 257 instance patients (unique, all IDs valid) and all 41 nurses; 111 unscheduled in both claimed and published solutions, so no patient is silently dropped.

## Literal reading of the criterion
- "ZERO hard-constraint violations": met.
- "STRICTLY LOWER ... than the cost listed": 37625 < 37650, met (not a tie).
- "re-fetched live immediately before claiming": evidence is a snapshot taken 2026-10-31T00:02:47Z; not re-fetched by me (one-download limit). Not verified beyond the snapshot.
- "compiled from the organisers' repository": source hash is as stated in CLAIM.md; I did not fetch the repository to confirm it.
- "lower than any value ... found by the NOVELTY check": delegated to the NOVELTY panelist; not judged here.
- Partial win p1 ("Strictly improve the listed upper bound on any one of the 60 instances, validated with zero violations"): met on the evidence above. p2 and p3 are not claimed and not met (one instance; no lower bound). The p1 win is the one claimed and is not subsumed by a larger claim.

pass: true
