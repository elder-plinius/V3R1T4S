# Honesty Gate Verdict (`ihtp-ihtc2024-hidden-m-instances-upper-bounds` — Instance `m28`)

- `target_id`: `ihtp-ihtc2024-hidden-m-instances-upper-bounds`
- `status`: `CONFIRMED_SOLUTION`
- `confirmed_scope`: An explicit feasible IHTC-2024 solution claim/sol_m28.json (307,109 bytes, sha256 d54f4151a022f91800fdc8a12226a5bc4da6d47ce2dcf51c575b36ead51b79c7) for hidden benchmark instance m28 (claim/m28.json, sha256 37061eb156c592feac39f5f148a5cfe4b594a57853638b0f2b041dd84c8f90e0) verified by the official C++ validator claim/IHTP_Validator.cc and standalone checker claim/author_checker_ihtp_check.py with Total violations = 0 and Total cost = 45,873, strictly improving on the best known upper bound of 45,913 listed on ihtc2024.github.io by 40 points.

## Panel Summary

| Role | Context | Verdict | Key Findings |
|---|---|---|---|
| `REPRODUCE` | Antigravity fresh subagent (`invoke_subagent`, role `REPRODUCE`) | `pass: true` | Wrote standalone checker `indep_ihtp_check.py` from the mathematical definition before reading `author_checker_ihtp_check.py` or `IHTP_Validator.cc`, tested 5 negative mutations (`MandatoryUnscheduledPatients`, `UncoveredRoom`, `PatientRoomCompatibility`, `AdmissionDay`, `NursePresence`), and verified `claim/sol_m28.json` (`sha256: d54f4151a022f91800fdc8a12226a5bc4da6d47ce2dcf51c575b36ead51b79c7`) across all three verifiers (`Total violations = 0`, `Total cost = 45873`). |
| `NOVELTY` | Antigravity fresh subagent (`invoke_subagent`, role `NOVELTY`) | `pass: true` | Performed single honest GETs of `https://ihtc2024.github.io/ihtp/index.html` (`45913`, Kletzander, Mischek & Musliu) and `published_sol_m28.json` (`Total cost = 45913`), searched arXiv, GitHub, `TROPHY_CASE.md`, and all open V3R1T4S PRs (confirming `45,873` strictly beats `45,913` by `-40` and no open PR touches `m28`). |
| `CRITERION` | Antigravity fresh subagent (`invoke_subagent`, role `CRITERION`) | `pass: true` | Audited every clause of the bank's verbatim `success_criterion`, verified compilation and sub-second execution of `IHTP_Validator.cc`, ran 3 perturbation/corruption controls, and established `confirmed_scope`. |
