# CRITERION panelist: i08 (IHTC-2024 IHTP)

confirmed_scope: Under the official IHTP_Validator.cc (sha256 0b56fa75...a8afa, matching the organisers' repository and site copies), claim/sol_i08.json for public instance i08 (byte-identical to i08.json in ihtc2024_competition_instances.zip, sha256 fa142d39...d2f7) has 0 hard-constraint violations and total cost 6225, strictly below the 6243 listed for i08 on https://ihtc2024.github.io/ihtp/index.html as re-fetched 2026-10-31, which meets partial win p1 only; the full criterion's literature/special-issue condition is left to the separate NOVELTY panelist and is not confirmed here.
context: subagent (Claude Code Agent tool, fresh context)

## Checks done
- Instance identity: downloaded ihtc2024_competition_instances.zip (zip sha256 365a0522...f681; 30 i??.json entries, __MACOSX ignored), extracted the entry named exactly `i08.json`: sha256 fa142d395afd6181957ad553dee03906844ba1027e7c028c6962da69b057f2d7, identical to claim/i08.json.
- Validator: claim/IHTP_Validator.cc sha256 0b56fa75ea7de1d4a7e3dbd2d5b88e7ac779d69e4287e1247305d873a06a8afa equals both raw.githubusercontent.com/ihtc2024/ihtc2024.github.io/main/assets/files/IHTP_Validator.cc and ihtc2024.github.io/assets/files/IHTP_Validator.cc, fetched now. Compiled myself with g++ -O2 -std=c++17.
- Run on the zip's i08.json: sol_i08.json gives Total violations = 0 (all nine hard constraints 0), Total cost = 6225 (RoomAgeMix 115, RoomSkillLevel 0, ContinuityOfCare 1144, ExcessiveNurseWorkload 646, OpenOperatingTheater 1600, SurgeonTransfer 90, PatientDelay 2430, ElectiveUnscheduledPatients 200).
- Null model / baseline: the organisers' published_sol_i08.json gives 0 violations and 6243, reproducing the listed value, so the validator and instance match the table's scoring.
- Row: re-fetched the table now; sha256 is the same as the scout copy (2b69fe2e...f363) and the i08 row reads 6243 (i07 = 4985 and i09 = 6608 are separate rows). 6225 < 6243: strict improvement of 18, not a tie.
- Structure: solution has 174 patient entries matching the instance's 174 patients; 1 elective left unscheduled (counted as a soft cost); MandatoryUnscheduledPatients = 0.

## Literal reading
- p1 ("Strictly improve the listed upper bound on any one of the 60 instances, validated with zero violations"): met literally for i08. It is a genuine win and is not subsumed by another named partial win. Its scope is the listed table value, not the best value anywhere.
- Full criterion: also needs the total to be below any value found by the NOVELTY check (2025-2026 IHTP special issue and other papers). I did not check this; I am relying on the NOVELTY panelist. So I do not confirm the full criterion.
- p2 (5+ instances, one method, fixed settings) and p3 (certified lower bound) are not claimed and not met.
- Caveats: the result is a 150 s + 300 s simulated-annealing refinement seeded from the organisers' own solution. That is a one-instance improvement, not evidence of a method. That is fine for p1, which asks for no method.

pass: true
