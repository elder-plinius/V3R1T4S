# IHTC-2024 i16: a schedule of cost 10054 (table 10139)

## What
For IHTC-2024 public instance i16, the organisers' IHTP_Validator.cc (repo sha256 0b56fa75...8afa) reports claim/sol_i16.json with 0 hard-constraint violations and total cost 10054, strictly below the 10139 listed for i16 on https://ihtc2024.github.io/ihtp/index.html as re-fetched on 2026-10-31, satisfying partial win p1 only; novelty versus the literature is left to the NOVELTY panelist.

## Check it yourself
    sh verify-it-yourself/run_checks.sh
Expected last line: PASS. Under a minute on a laptop (one download of the organisers' instance archive).
For the official check, compile the organisers' IHTP_Validator.cc and run
`./IHTP_Validator i16.json object/sol_i16.json`: Total violations = 0, Total cost = 10054.

## Compared to
The organisers' upper-bound table https://ihtc2024.github.io/ihtp/index.html, cell i16, listed value 10139,
fetched 2026-10-31T00:02:47Z (the-record-we-beat/snapshot.md).

## Not claimed
Not optimality and no lower bound. Not a competition-rules result (no time limit applied). Synthetic benchmark data:
says nothing about real patient outcomes. One cell only.

## Credits
- Problem, instances, validator and the upper-bound table: Sara Ceschia, Roberto Maria Rosati, Andrea Schaerf,
  Eugenia Zanazzo (University of Udine), Pieter Smet, Greet Vanden Berghe (KU Leuven): https://ihtc2024.github.io/
- The seed of this search is the organisers' published best solution for i16.
- JSON parsing for the official validator: nlohmann/json, https://github.com/nlohmann/json
- Literature checked: Guericke et al., arXiv:2511.04685, https://arxiv.org/abs/2511.04685
- Credit for this result: Abdelghafour.
