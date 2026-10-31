# CRITERION panelist: i16 (claim p1)

## Checks performed (2026-10-31)
- Instance identity: i16.json extracted by exact name from a fresh download of https://ihtc2024.github.io/assets/files/ihtc2024_competition_instances.zip (entries i01-i30); sha256 96583cbd7a8cf2fdd129ad803a8b55a1beb0f4bd8613ee26d4ac08bfa6b9534f, identical to claim/i16.json. It is i16 of the public (i01-i30) set.
- Validator: claim/IHTP_Validator.cc sha256 0b56fa75...8afa matches a fresh fetch of the organisers' repository (raw main). Compiled with g++ -O2 -std=c++17 against the supplied json.hpp (v3.11.3, sha256 9bea4c80...3ea6).
- Run: sol_i16.json -> Total violations = 0 (all 9 hard categories 0), Total cost = 10054, exit 0.
- Null model / calibration: the organisers' published i16 solution (claim copy byte-identical to the live file linked from the table, sha256 7ae398a3...7189) -> 0 violations, 10139, exactly the listed value, so the validator reproduces the table. The claimed solution differs from it in 125 of 154 patient assignments and in nurse rosters (a genuinely different solution, not a relabelled copy).
- Table: live re-fetch of https://ihtc2024.github.io/ihtp/index.html today has the same sha256 as the scout copy (2b69fe2e...f363); the i16 row is in the "Public dataset" table with cost 10139. Comparison is with the i16 row. 10054 < 10139 strictly (delta 85, 0.84%).

## Literal reading
- p1 ("Strictly improve the listed upper bound on any one of the 60 instances, validated with zero violations"): met literally.
- Full criterion additionally requires being lower than any value found by the NOVELTY check (2025-2026 special issue and other papers). I did not check literature; that clause is delegated to the separate NOVELTY panelist, so the full criterion is NOT confirmed by this panelist.
- p2 (5+ instances, one method) and p3 (certified lower bound) are not claimed and not met; p1 is not subsumed by either.
- Caveats: improvement is from a single seeded SA run on one instance (no method claim); "official" validator = organisers' repo source at the hash above.

confirmed_scope: For IHTC-2024 public instance i16, the organisers' IHTP_Validator.cc (repo sha256 0b56fa75...8afa) reports claim/sol_i16.json with 0 hard-constraint violations and total cost 10054, strictly below the 10139 listed for i16 on https://ihtc2024.github.io/ihtp/index.html as re-fetched on 2026-10-31, satisfying partial win p1 only; novelty versus the literature is left to the NOVELTY panelist.
context: subagent (Claude Code Agent tool, fresh context)
pass: true
