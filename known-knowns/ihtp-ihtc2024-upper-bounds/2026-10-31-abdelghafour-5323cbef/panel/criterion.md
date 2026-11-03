# CRITERION panelist: m19

context: subagent (Claude Code Agent tool, fresh context)

## Checks performed (all independently re-run)
- Instance identity: downloaded ihtc2024_final_instances.zip once (sha256 f2037aaf982531f6e21c13334f82c74d7baabbdf4fcda481147c30426b1a10fd); exact entry `m19.json` (ignoring `__MACOSX/._m19.json`) has sha256 8a8b556980e7e99b6e2cd3610830a0f09043a533ec2075dd357cccd25ada6786, identical to claim/m19.json. It is instance m19 of the final/hidden (m01-m30) set.
- Validator: claim/IHTP_Validator.cc sha256 0b56fa75...8afa matches both raw.githubusercontent.com (ihtc2024/ihtc2024.github.io main) and the ihtc2024.github.io asset copy. Compiled with g++ -O2 -std=c++17 against the supplied json.hpp (v3.11.3 hash as stated).
- Candidate: `IHTP_Validator m19.json sol_m19.json` -> Total violations = 0 (all nine hard constraints 0), Total cost = 21752.
- Null model: the organisers' published sol_m19.json (live hash a096c6f0...519c, identical to claim/published_sol_m19.json) validates to 0 violations, cost 21776, matching the table, so validator build and instance are consistent with the table.
- Table: re-fetched https://ihtc2024.github.io/ihtp/index.html live today (HTTP 200); byte-identical to the scout copy (sha256 2b69fe2e...f363). The m19 row sits under the "Hidden dataset" heading with Cost 21776. 21752 < 21776 strictly (improvement 24, ~0.11%); not a tie.

## Word-by-word reading
- "one instance from ... ihtc2024_final_instances.zip (m01-m30)": met (m19).
- "official IHTP_Validator.cc (compiled from the organisers' repository)": met (hash-verified against repo).
- "ZERO hard-constraint violations": met.
- "STRICTLY LOWER ... than the cost listed ... re-fetched live immediately before claiming": met (live table re-fetched, unchanged, 21776).
- "and lower than any value for that instance found by the NOVELTY check in the 2025-2026 special issue ... and other papers": NOT assessed here; deferred to the separate NOVELTY panelist. Hence the full success criterion is not confirmed by this panelist.
- Partial win p1 ("Strictly improve the listed upper bound on any one of the 60 instances, validated with zero violations"): met literally. p1 is the claimed win; it is a genuine strict improvement of a listed bound, not a tie, not a reinterpretation of the bound or instance set, and not subsumed by a weaker reading. p2 (needs 5+ instances) and p3 (lower bound, i-instances) are not met or claimed.
- No stretched definitions found: "listed upper bound" = the table's m19 cost; "validated" = official validator, zero violations.

confirmed_scope: Under the official IHTP_Validator (hash-matched to the organisers' repository), sol_m19.json for IHTC-2024 final/hidden instance m19 (hash-matched to ihtc2024_final_instances.zip) has 0 hard-constraint violations and total cost 21752, strictly below the 21776 listed for m19 on the live-fetched organisers' table, which satisfies partial win p1; whether it also beats values in the literature (the remaining clause of the full criterion) is left to the NOVELTY panelist.

pass: true
