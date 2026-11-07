# IHTC-2024 i20: a schedule of cost 28812 (table 29042)

## What
Under the organisers' official validator IHTP_Validator.cc (https://ihtc2024.github.io/assets/files/IHTP_Validator.cc, sha256 0b56fa75ea7de1d4a7e3dbd2d5b88e7ac779d69e4287e1247305d873a06a8afa, compiled with g++ -O2 -std=c++17), object/sol_i20.json on instance i20 (the i20.json entry of https://ihtc2024.github.io/assets/files/ihtc2024_competition_instances.zip; archive sha256 365a05227c156029d3653d6997ddf28392a728521722f37ad9edf4368ac6f681, entry sha256 f5c19fbd4035d3f6ef4e66a04f73177a496fb141732c268d558df2e60b559540) reports 0 hard-constraint violations and total cost 28812. That is 230 below 29042, the i20 value in the organisers' upper-bound table (https://ihtc2024.github.io/ihtp/index.html), which was captured at 2026-10-31T00:02:47Z (page sha256 2b69fe2e2b6e0a978472aa3916c8c53a774e223e666f20966156802f9ce2f363) and still listed 29042 when re-fetched on 2026-11-07. This meets partial win p1. The novelty panel found no published value at or below 28812 (best literature value 29098; see panel/novelty.md).

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
