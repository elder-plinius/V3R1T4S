> Note added 2026-11-07 (packaging, after maintainer review): paths under `claim/` and `CLAIM.md` below are this panel's local
> working files and are not included in this package. They correspond to:
> - claim/sol_i20.json: object/sol_i20.json (same bytes; sha256 in INDEX.csv)
> - claim/IHTP_Validator.cc: https://ihtc2024.github.io/assets/files/IHTP_Validator.cc (sha256 0b56fa75ea7de1d4a7e3dbd2d5b88e7ac779d69e4287e1247305d873a06a8afa)
> - claim/i20.json: the i20.json entry of https://ihtc2024.github.io/assets/files/ihtc2024_competition_instances.zip (archive sha256 365a05227c156029d3653d6997ddf28392a728521722f37ad9edf4368ac6f681, entry sha256 f5c19fbd4035d3f6ef4e66a04f73177a496fb141732c268d558df2e60b559540)
> - claim/published_sol_i20.json: the organisers' i20 solution, https://ihtc2024.github.io/assets/files/solutions/public/IHTP/sol_i20.json
> - claim/ihtp_table.html: https://ihtc2024.github.io/ihtp/index.html as fetched 2026-10-31T00:02:47Z (sha256 2b69fe2e2b6e0a978472aa3916c8c53a774e223e666f20966156802f9ce2f363); see the-record-we-beat/snapshot.md
> - claim/json.hpp: nlohmann/json single_include/nlohmann/json.hpp (https://github.com/nlohmann/json)
> - CLAIM.md: summarised in README.md and INDEX.csv
> The text below is otherwise unchanged.

> Restated 2026-11-07 at the maintainer's request (same evidence, packaging wording only); the original line is kept below.
confirmed_scope: Under the organisers' official validator IHTP_Validator.cc (https://ihtc2024.github.io/assets/files/IHTP_Validator.cc, sha256 0b56fa75ea7de1d4a7e3dbd2d5b88e7ac779d69e4287e1247305d873a06a8afa, compiled with g++ -O2 -std=c++17), object/sol_i20.json on instance i20 (the i20.json entry of https://ihtc2024.github.io/assets/files/ihtc2024_competition_instances.zip; archive sha256 365a05227c156029d3653d6997ddf28392a728521722f37ad9edf4368ac6f681, entry sha256 f5c19fbd4035d3f6ef4e66a04f73177a496fb141732c268d558df2e60b559540) reports 0 hard-constraint violations and total cost 28812. That is 230 below 29042, the i20 value in the organisers' upper-bound table (https://ihtc2024.github.io/ihtp/index.html), which was captured at 2026-10-31T00:02:47Z (page sha256 2b69fe2e2b6e0a978472aa3916c8c53a774e223e666f20966156802f9ce2f363) and still listed 29042 when re-fetched on 2026-11-07. This meets partial win p1.

# Honesty gate (main session), cell i20

reproduce: pass: true (own checker and official validator: 0 violations, 28812)
novelty: pass: true (live table re-fetched by the panelist at 2026-10-31T00:27:12Z, i20 listed 29042; best literature value found 29098; no PR, known-knowns or trophy-case value at or below 28812)
criterion: pass: true (partial win p1; instance hash matches the organisers' archive)
Main-session review: all three files read; none hedges its verdict; three fresh subagent contexts that saw only claim/;
panel table fetch under 6 hours old; one cell, one object; no evasion. Claimed scope: partial win p1, one cell.

status: CONFIRMED_PARTIAL
Original confirmed_scope (2026-10-31): Under IHTP_Validator.cc (sha256 0b56fa75...a8afa, compiled g++ -O2 -std=c++17 by this panelist), claim/sol_i20.json on instance i20 (byte-identical to the i20.json entry of ihtc2024_competition_instances.zip, sha256 f5c19fbd...59540) reports 0 hard-constraint violations and total cost 28812, strictly below the 29042 in the i20 row of the organisers' upper-bound table as captured in claim/ihtp_table.html at 2026-10-31T00:02:47Z, which meets partial win p1 only; the full criterion's literature/special-issue clause is left to the NOVELTY panelist and the live re-fetch was not repeated here.
