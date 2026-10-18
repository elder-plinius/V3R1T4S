# Honesty Gate Verdict (`ihtp-ihtc2024-upper-bounds` — Instance `i27`)

- `target_id`: `ihtp-ihtc2024-upper-bounds`
- `status`: `CONFIRMED_SOLUTION`
- `confirmed_scope`: An explicit feasible IHTC-2024 solution claim/sol_i27.json (209,120 bytes, sha256 900443ab5205ab28d6ad4713b0023593f931007812ecf0e3410a4e49e1006cf7) for benchmark instance i27 (claim/i27.json, sha256 a4c3d597021eca59eb2ce37ef4de189eed25a8a91d51a466bbde5c42c54e4134) verified by the official C++ validator claim/IHTP_Validator.cc and standalone checker claim/author_checker_ihtp_check.py with Total violations = 0 and Total cost = 50,063, strictly improving on the best known upper bound of 50,976 listed on ihtc2024.github.io by 913 points (-1.791%).

## Panel Summary

| Role | Context | Verdict | Key Findings |
|---|---|---|---|
| `REPRODUCE` | Antigravity fresh subagent (`invoke_subagent`, role `REPRODUCE`) | `pass: true` | Wrote standalone checker `indep_ihtp_check.py` from the mathematical definition before reading `author_checker_ihtp_check.py` or `IHTP_Validator.cc`, tested 5 negative mutations (`MandatoryUnscheduledPatients`, `UncoveredRoom`, `PatientRoomCompatibility`, `AdmissionDay`, `NursePresence`), and verified `claim/sol_i27.json` (`sha256: 900443ab5205ab28d6ad4713b0023593f931007812ecf0e3410a4e49e1006cf7`) across all three verifiers (`Total violations = 0`, `Total cost = 50063`). |
| `NOVELTY` | Antigravity fresh subagent (`invoke_subagent`, role `NOVELTY`) | `pass: true` | Performed single honest GETs of `https://ihtc2024.github.io/ihtp/index.html` (`50976`, Kletzander, Mischek & Musliu) and `published_sol_i27.json` (`Total cost = 50976`), searched arXiv, GitHub, `TROPHY_CASE.md`, and all open V3R1T4S PRs (confirming `50,063` strictly beats both the live table `50,976` by `-913` and open PR `#359` `50,125` by `-62`). |
| `CRITERION` | Antigravity fresh subagent (`invoke_subagent`, role `CRITERION`) | `pass: true` | Audited every clause of the bank's verbatim `success_criterion`, verified compilation and sub-second execution (`0.032s` warm) of `IHTP_Validator.cc`, ran 4 perturbation/corruption controls and a 100-seed random feasible NRA null model (`mean = 91,599.57`), and established `confirmed_scope`. |
