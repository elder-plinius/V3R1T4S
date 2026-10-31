# IHTC-2024 m19: a schedule of cost 21752 (table 21776)

## What
Under the official IHTP_Validator (hash-matched to the organisers' repository), sol_m19.json for IHTC-2024 final/hidden instance m19 (hash-matched to ihtc2024_final_instances.zip) has 0 hard-constraint violations and total cost 21752, strictly below the 21776 listed for m19 on the live-fetched organisers' table, which satisfies partial win p1; whether it also beats values in the literature (the remaining clause of the full criterion) is left to the NOVELTY panelist.

## Check it yourself
    sh verify-it-yourself/run_checks.sh
Expected last line: PASS. Under a minute on a laptop (one download of the organisers' instance archive).
For the official check, compile the organisers' IHTP_Validator.cc and run
`./IHTP_Validator m19.json object/sol_m19.json`: Total violations = 0, Total cost = 21752.

## Compared to
The organisers' upper-bound table https://ihtc2024.github.io/ihtp/index.html, cell m19, listed value 21776,
fetched 2026-10-31T00:02:47Z (the-record-we-beat/snapshot.md).

## Not claimed
Not optimality and no lower bound. Not a competition-rules result (no time limit applied). Synthetic benchmark data:
says nothing about real patient outcomes. One cell only.

## Credits
- Problem, instances, validator and the upper-bound table: Sara Ceschia, Roberto Maria Rosati, Andrea Schaerf,
  Eugenia Zanazzo (University of Udine), Pieter Smet, Greet Vanden Berghe (KU Leuven): https://ihtc2024.github.io/
- The seed of this search is the organisers' published best solution for m19.
- JSON parsing for the official validator: nlohmann/json, https://github.com/nlohmann/json
- Literature checked: Guericke et al., arXiv:2511.04685, https://arxiv.org/abs/2511.04685
- Credit for this result: Abdelghafour.
