# IEA37 CS1: a feasible 64-turbine layout above the posted record

## What
The single 64-turbine layout in object/layout.json is strictly feasible for IEA37 case study 1 (all 64 hubs within 3000 m, maximum radius 2999.999900000135 m; all 2016 pairs at least 260 m apart, minimum 307.514 m; checked in double precision and exact rational arithmetic with no tolerance) and has AEP 1543800.4665 MWh under the official iea37-aepcalc.py model, which exceeds the posted participant-12 record 1526474.8025 MWh by 17325.66 MWh and the open, unconfirmed PR #938 layout (1539447.1174 MWh, recomputed) by 4353.35 MWh, with no confirmed V3R1T4S 64-turbine known-known in the claim's status snapshot, so it meets the full success criterion for the 64-turbine cell.

Status: CONFIRMED_SOLUTION for the 64-turbine cell of the bank's full success criterion. Three fresh AI-agent contexts passed (panel/). This is a computational result; no independent human or benchmark-maintainer review has occurred.

## Check it yourself
```sh
sh verify-it-yourself/run_checks.sh
```
Expected last line: `PASS`. Python 3 standard library only; a few seconds with internet access on the first run. Two comparator files (participant 12's posted opt64 layout and PR #938's layout) are downloaded from pinned public commits, checked by SHA256 and cached in the OS temporary directory; no downloaded code is executed. See RUN_IT_YOURSELF.md for an offline option.

## Compared to
| Comparator | Official AEP (MWh) | Role |
|---|---:|---|
| Participant 12 (posted record) | 1526474.8025 | Full criterion requires at least 0.01 MWh more; file 4.1 mm outside R |
| V3R1T4S PR #938 (Jimbootgit) | 1539447.1174 | Strongest known open claim (unconfirmed); beaten by 4353.35 MWh |
| This explicit object | 1543800.4665 | Strictly feasible; 17325.66 MWh above the posted record |

Table: https://github.com/IEAWindSystems/iea37-wflo-casestudies/tree/master/cs1-2/iea37-cs1-results, fetched 2026-11-04T20:19Z and 20:46:59Z (HTTP 200); see the-record-we-beat/record.md.

## Not claimed
No optimality, field-performance prediction, new optimisation method (the search code is a vacancy/reinsertion heuristic), or result for 16 or 36 turbines. The object is a nominal CS1 result only; it was not optimised for direction uncertainty. Not reviewed by maintainers; PR #938 is likewise unreviewed. One literature source (Baker et al., NREL TP 72935) could not be fetched during the novelty review (DNS failure); its 64-turbine values are the posted participant files, which were re-checked directly.

## Credits
- Nicholas F. Baker, Andrew P. J. Stanley, Jared J. Thomas, Andrew Ning and Katherine Dykes: IEA Wind Task 37 case studies, evaluator, parameters and submitted layouts; https://github.com/IEAWindSystems/iea37-wflo-casestudies and https://doi.org/10.2514/6.2019-0540.
- Majid Bastankhah and Fernando Porte-Agel: Gaussian wake-model foundations.
- IEA37 participant 12: the posted record this result exceeds; credited through the official benchmark, without asserting identity.
- Jared J. Thomas and Andrew Ning (SNOPT+WEC, participant 4).
- Jimbootgit: PR #938, the strongest previous open claim, https://github.com/elder-plinius/V3R1T4S/pull/938. Its coordinates were never used as optimizer starts.
- OrenSleepwalker, with Codex (search code and earlier own layouts) and Claude Code (continuation search, verification, packaging) and three separately started AI review contexts. No external timestamp attestation is claimed.
