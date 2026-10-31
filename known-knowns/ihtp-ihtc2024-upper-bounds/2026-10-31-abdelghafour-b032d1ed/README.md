# IHTC-2024 i20: a schedule of cost 28812 (table 29042)

## What
Under IHTP_Validator.cc (sha256 0b56fa75...a8afa, compiled g++ -O2 -std=c++17 by this panelist), claim/sol_i20.json on instance i20 (byte-identical to the i20.json entry of ihtc2024_competition_instances.zip, sha256 f5c19fbd...59540) reports 0 hard-constraint violations and total cost 28812, strictly below the 29042 in the i20 row of the organisers' upper-bound table as captured in claim/ihtp_table.html at 2026-10-31T00:02:47Z, which meets partial win p1 only; the full criterion's literature/special-issue clause is left to the NOVELTY panelist and the live re-fetch was not repeated here.

## Check it yourself
    sh verify-it-yourself/run_checks.sh
Expected last line: PASS. Under a minute on a laptop (one download of the organisers' instance archive).
For the official check, compile the organisers' IHTP_Validator.cc and run
`./IHTP_Validator i20.json object/sol_i20.json`: Total violations = 0, Total cost = 28812.

## Compared to
The organisers' upper-bound table https://ihtc2024.github.io/ihtp/index.html, cell i20, listed value 29042,
fetched 2026-10-31T00:02:47Z (the-record-we-beat/snapshot.md).

## Not claimed
Not optimality and no lower bound. Not a competition-rules result (no time limit applied). Synthetic benchmark data:
says nothing about real patient outcomes. One cell only.

## Credits
- Problem, instances, validator and the upper-bound table: Sara Ceschia, Roberto Maria Rosati, Andrea Schaerf,
  Eugenia Zanazzo (University of Udine), Pieter Smet, Greet Vanden Berghe (KU Leuven): https://ihtc2024.github.io/
- The seed of this search is the organisers' published best solution for i20.
- JSON parsing for the official validator: nlohmann/json, https://github.com/nlohmann/json
- Literature checked: Guericke et al., arXiv:2511.04685, https://arxiv.org/abs/2511.04685
- Credit for this result: Abdelghafour.
