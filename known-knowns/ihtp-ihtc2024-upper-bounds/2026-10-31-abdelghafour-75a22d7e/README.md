# IHTC-2024 m08: a schedule of cost 14877 (table 14976)

## What
Under the organisers' IHTP_Validator.cc (sha256 0b56fa75...a8afa, matching the raw file fetched from the organisers' GitHub repo today), compiled by me with g++ -O2 -std=c++17, claim/sol_m08.json on instance m08 of ihtc2024_final_instances.zip (entry sha256 cee80f3a...91ce1, byte-identical to claim/m08.json) reports 0 hard-constraint violations and total cost 14877, strictly below the 14976 listed for m08 in the Hidden dataset table of https://ihtc2024.github.io/ihtp/index.html as re-fetched at 2026-10-31T09:45:33Z, which meets partial win p1; whether it also meets the full criterion's "lower than any value ... found by the NOVELTY check" clause is left to the separate NOVELTY panelist.

## Check it yourself
    sh verify-it-yourself/run_checks.sh
Expected last line: PASS. Under a minute on a laptop (one download of the organisers' instance archive).
For the official check, compile the organisers' IHTP_Validator.cc and run
`./IHTP_Validator m08.json object/sol_m08.json`: Total violations = 0, Total cost = 14877.

## Compared to
The organisers' upper-bound table https://ihtc2024.github.io/ihtp/index.html, cell m08, listed value 14976,
fetched 2026-10-31T00:02:47Z (the-record-we-beat/snapshot.md).

## Not claimed
Not optimality and no lower bound. Not a competition-rules result (no time limit applied). Synthetic benchmark data:
says nothing about real patient outcomes. One cell only.

## Credits
- Problem, instances, validator and the upper-bound table: Sara Ceschia, Roberto Maria Rosati, Andrea Schaerf,
  Eugenia Zanazzo (University of Udine), Pieter Smet, Greet Vanden Berghe (KU Leuven): https://ihtc2024.github.io/
- The seed of this search is the organisers' published best solution for m08.
- JSON parsing for the official validator: nlohmann/json, https://github.com/nlohmann/json
- Literature checked: Guericke et al., arXiv:2511.04685, https://arxiv.org/abs/2511.04685
- Credit for this result: Abdelghafour.
