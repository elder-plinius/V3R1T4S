# IHTC-2024 i18: a schedule of cost 37625 (table 37650)

## What
Under IHTP_Validator.cc (sha256 0b56fa75…a8afa, compiled by me with g++ -O2 -std=c++17), claim/sol_i18.json scores 0 hard-constraint violations and total cost 37625 on public instance i18 (byte-identical to i18.json in ihtc2024_competition_instances.zip, sha256 0cb52506…0ad3e), strictly below the 37650 in the i18 row of the organisers' upper-bound table as snapshotted 2026-10-31T00:02:47Z, which meets partial win p1; the full criterion's literature/special-issue condition is left to the NOVELTY panelist, and I did not re-fetch the table live or independently check the validator's repository origin.

## Check it yourself
    sh verify-it-yourself/run_checks.sh
Expected last line: PASS. Under a minute on a laptop (one download of the organisers' instance archive).
For the official check, compile the organisers' IHTP_Validator.cc and run
`./IHTP_Validator i18.json object/sol_i18.json`: Total violations = 0, Total cost = 37625.

## Compared to
The organisers' upper-bound table https://ihtc2024.github.io/ihtp/index.html, cell i18, listed value 37650,
fetched 2026-10-31T00:02:47Z (the-record-we-beat/snapshot.md).

## Not claimed
Not optimality and no lower bound. Not a competition-rules result (no time limit applied). Synthetic benchmark data:
says nothing about real patient outcomes. One cell only.

## Credits
- Problem, instances, validator and the upper-bound table: Sara Ceschia, Roberto Maria Rosati, Andrea Schaerf,
  Eugenia Zanazzo (University of Udine), Pieter Smet, Greet Vanden Berghe (KU Leuven): https://ihtc2024.github.io/
- The seed of this search is the organisers' published best solution for i18.
- JSON parsing for the official validator: nlohmann/json, https://github.com/nlohmann/json
- Literature checked: Guericke et al., arXiv:2511.04685, https://arxiv.org/abs/2511.04685
- Credit for this result: Abdelghafour.
