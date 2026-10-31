# CRITERION panelist: m08

context: subagent (Claude Code Agent tool, fresh context)

confirmed_scope: Under the organisers' IHTP_Validator.cc (sha256 0b56fa75...a8afa, matching the raw file fetched from the organisers' GitHub repo today), compiled by me with g++ -O2 -std=c++17, claim/sol_m08.json on instance m08 of ihtc2024_final_instances.zip (entry sha256 cee80f3a...91ce1, byte-identical to claim/m08.json) reports 0 hard-constraint violations and total cost 14877, strictly below the 14976 listed for m08 in the Hidden dataset table of https://ihtc2024.github.io/ihtp/index.html as re-fetched at 2026-10-31T09:45:33Z, which meets partial win p1; whether it also meets the full criterion's "lower than any value ... found by the NOVELTY check" clause is left to the separate NOVELTY panelist.

## Checks (all run by me)
- Instance identity: downloaded ihtc2024_final_instances.zip once; `unzip -Z1` lists 30 non-__MACOSX entries (m01-m30); entry `m08.json` sha256 = cee80f3a7cd25f0d9fdb49fce0d1779ae3ca3feca107ad64e8a7779222791ce1 = sha256 of claim/m08.json. Exact match.
- Table row: re-fetched the upper-bounds page at 2026-10-31T09:45:33Z; byte-identical to claim/ihtp_table.html (sha256 2b69fe2e...2f363). m08 sits under "Hidden dataset", row `m08 | 14976 | sol_m08.json`. The comparison uses the m08 row, not a neighbour (m07 7329, m09 32967).
- Validator provenance: claim/IHTP_Validator.cc sha256 equals the file at raw.githubusercontent.com/ihtc2024/ihtc2024.github.io/main/assets/files/IHTP_Validator.cc, fetched today.
- Claimed solution: Total violations = 0 (all 9 hard-constraint counters are 0); Total cost = 14877 (RoomAgeMix 117, RoomSkillLevel 445, ContinuityOfCare 4195, ExcessiveNurseWorkload 0, OpenOperatingTheater 500, SurgeonTransfer 30, PatientDelay 1340, ElectiveUnscheduledPatients 8250). Weights come from the hash-verified instance file.
- Null model: the organisers' published_sol_m08.json gives 0 violations and 14976, so it reproduces the listed value exactly. The validator, instance and pipeline are therefore consistent with the table, and the 99-point gap (0.66%) is not an artefact of the setup.
- Sanity: the solution lists 200 unique patient ids, all in the instance (200 patients, 130 mandatory), and 28 unique nurses. 33 are unscheduled, the same count as the published solution, and all 33 are optional (MandatoryUnscheduledPatients = 0).

## Literal reading
- p1 ("Strictly improve the listed upper bound on any one of the 60 instances, validated with zero violations"): met. m08 is one of the 60 instances (i01-i30, m01-m30). 14877 < 14976 is a strict improvement, not a tie. Violations are zero under the official validator.
- Full criterion: the validator, instance-set, strict-inequality and live-re-fetch clauses are met. The "lower than any value ... found by the NOVELTY check in the 2025-2026 special issue ... and other papers" clause is outside my remit. I relied on the NOVELTY panelist for it, so I do not confirm the full criterion here.
- p2 (5+ instances, fixed method) and p3 (certified lower bound, i-instances) are not claimed, and nothing here supports them.
- No stretched definitions found. "Listed" refers to the live organisers' table, which was re-fetched and unchanged. "Official validator" means the organisers' file, hash-matched to their repo.

pass: true
