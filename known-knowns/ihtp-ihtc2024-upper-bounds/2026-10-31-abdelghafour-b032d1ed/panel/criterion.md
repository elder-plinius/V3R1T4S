# Criterion panelist: i20 (IHTC-2024, public set)

confirmed_scope: Under IHTP_Validator.cc (sha256 0b56fa75...a8afa, compiled g++ -O2 -std=c++17 by this panelist), claim/sol_i20.json on instance i20 (byte-identical to the i20.json entry of ihtc2024_competition_instances.zip, sha256 f5c19fbd...59540) reports 0 hard-constraint violations and total cost 28812, strictly below the 29042 in the i20 row of the organisers' upper-bound table as captured in claim/ihtp_table.html at 2026-10-31T00:02:47Z, which meets partial win p1 only; the full criterion's literature/special-issue clause is left to the NOVELTY panelist and the live re-fetch was not repeated here.
context: subagent (Claude Code Agent tool, fresh context)

## Checks performed
- Instance identity: downloaded the competition zip once (zip sha256 365a0522...6f681, 30 non-__MACOSX entries); extracted exact entry `i20.json`; sha256 f5c19fbd4035d3f6ef4e66a04f73177a496fb141732c268d558df2e60b559540 equals claim/i20.json.
- Table row: claim/ihtp_table.html (sha256 2b69fe2e...2f363 matches CLAIM) has exactly one `<td>i20</td>` row, in the "Public dataset" upper-bound table, value 29042 (60 instance rows total).
- Validator: claim/IHTP_Validator.cc sha256 matches the hash stated in CLAIM; source scanned, no hardcoded costs, env reads or shell calls. Upstream hash not independently fetched by this panelist.
- Run on the zip's i20.json: sol_i20.json gives Total violations = 0, Total cost = 28812 (RoomAgeMix 79, RoomSkillLevel 1890, ContinuityOfCare 981, ExcessiveNurseWorkload 460, OpenOperatingTheater 1400, SurgeonTransfer 22, PatientDelay 3480, ElectiveUnscheduledPatients 20500).
- Null model / control: published_sol_i20.json gives 0 violations and 29042, reproducing the listed value, so the validator/instance pairing is consistent with the table. Solution covers all 188 patients and 33 nurses; 41 unscheduled (all elective, consistent with 500 x 41).

## Literal reading
- Full criterion: needs (a) zero violations (met), (b) strictly below the live table value (met against the 00:02:47Z capture; live re-fetch not repeated by this panelist), and (c) below any value found by the NOVELTY check (not assessed here; delegated to the NOVELTY panelist). Full criterion therefore not confirmed by this panelist.
- p1 "Strictly improve the listed upper bound on any one of the 60 instances, validated with zero violations": met for i20 (28812 < 29042, margin 230, about 0.79%). Not a tie.
- p2 not claimed (one instance; two SA runs, no fixed one-seed protocol). p3 not claimed (no lower bound).
- Caveat: improvement is a seeded local-search refinement of the organisers' own published solution; p1 counts any strict improvement, so this does not disqualify it.

pass: true
