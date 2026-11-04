# Receipts
Command (from the package folder): sh verify-it-yourself/run_checks.sh
Run UTC: 2026-11-04T20:56:16Z; python3 3.12.3
```
{
  "AEP_MWh": 1543800.4664981721,
  "directional_AEP_MWh": [
    37622.92932076946,
    34854.40958729228,
    44299.275890910765,
    56411.174493745864,
    99616.73069172441,
    97655.05038116037,
    153575.04884753213,
    189692.45533347185,
    95737.38990223395,
    55125.7828113072,
    59380.08308008629,
    129563.36423838162,
    338330.99152807344,
    68793.2697025263,
    49182.30219885454,
    33960.20849010168
  ],
  "geometry": {
    "maximum_radius_m": 2999.999900000135,
    "minimum_spacing_m": 307.51364081707464,
    "strictly_feasible": true
  },
  "matchings": {
    "participant12": {
      "farther_than_50m": 63,
      "total_distance_m": 24197.895883057125
    },
    "PR938": {
      "farther_than_50m": 63,
      "total_distance_m": 22920.423198346256
    }
  },
  "comparator_AEP_MWh": {
    "participant12": 1526474.802480072,
    "PR938": 1539447.1173686485
  },
  "margin_over_posted_record_MWh": 17325.663998172153,
  "scope": "Full criterion (64 turbines): strict feasibility, AEP above posted record + 0.01, and above hash-pinned participant 12 and PR #938 layouts (recomputed); see panel for novelty."
}
PASS
```
