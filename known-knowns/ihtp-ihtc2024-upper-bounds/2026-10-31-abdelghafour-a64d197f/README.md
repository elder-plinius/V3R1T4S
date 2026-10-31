# IHTC-2024 i08: a schedule of cost 6225 (table 6243)

## What
Under the official IHTP_Validator.cc (sha256 0b56fa75...a8afa, matching the organisers' repository and site copies), claim/sol_i08.json for public instance i08 (byte-identical to i08.json in ihtc2024_competition_instances.zip, sha256 fa142d39...d2f7) has 0 hard-constraint violations and total cost 6225, strictly below the 6243 listed for i08 on https://ihtc2024.github.io/ihtp/index.html as re-fetched 2026-10-31, which meets partial win p1 only; the full criterion's literature/special-issue condition is left to the separate NOVELTY panelist and is not confirmed here.

## Check it yourself
    sh verify-it-yourself/run_checks.sh
Expected last line: PASS. Under a minute on a laptop (one download of the organisers' instance archive).
For the official check, compile the organisers' IHTP_Validator.cc and run
`./IHTP_Validator i08.json object/sol_i08.json`: Total violations = 0, Total cost = 6225.

## Compared to
The organisers' upper-bound table https://ihtc2024.github.io/ihtp/index.html, cell i08, listed value 6243,
fetched 2026-10-31T00:02:47Z (the-record-we-beat/snapshot.md).

## Not claimed
Not optimality and no lower bound. Not a competition-rules result (no time limit applied). Synthetic benchmark data:
says nothing about real patient outcomes. One cell only.

## Credits
- Problem, instances, validator and the upper-bound table: Sara Ceschia, Roberto Maria Rosati, Andrea Schaerf,
  Eugenia Zanazzo (University of Udine), Pieter Smet, Greet Vanden Berghe (KU Leuven): https://ihtc2024.github.io/
- The seed of this search is the organisers' published best solution for i08.
- JSON parsing for the official validator: nlohmann/json, https://github.com/nlohmann/json
- Literature checked: Guericke et al., arXiv:2511.04685, https://arxiv.org/abs/2511.04685
- Credit for this result: Abdelghafour.
