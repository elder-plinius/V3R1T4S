# The published evaluation reproduced (p3)

p3 is a reproduction of published numbers, not a new record. The published values, read from the hub's own
evaluation file:

| item | value |
|---|---|
| status source | https://raw.githubusercontent.com/european-modelling-hubs/covid19-forecast-hub-europe_archive/main/evaluation/scores.csv |
| fetched | 2026-11-13T05:39:54Z, HTTP 200, 2,800,631 bytes (HEAD: Content-Length 2800631, ETag "aaced4facb8cf0abf1d58586131abee8640f6f567569553eb7a0ccb9bc76a277") |
| sha256 of the file (not included) | c59afa8e3c9530e71d1c4c5445794bf6600b9ae3aaecec89db7e34def4aeb54c |
| archive commit at fetch time | ef5eef8464a8ace38a6e93ca16026647bf09e1b5 (main, from the github.com tree pages) |
| content | 31,256 rows, 15 models, inc case / inc death / inc hosp, forecast dates 2023-10-30 to 2024-09-16, horizons 1-4 |

Extracted cells: the per-model means over the published rows of wis, sharpness, underprediction and overprediction
(4 decimals; full precision in verify-it-yourself/check_p3.py, PUB):

| model | rows | wis | sharpness | underprediction | overprediction |
|---|---|---|---|---|---|
| ECDC-norrsken_blue | 2310 | 525.2784 | 227.9671 | 3.6753 | 293.6104 |
| ECDC-norrsken_green | 2390 | 610.3615 | 114.5682 | 15.0410 | 480.7335 |
| ECDC-soca_simplex | 1315 | 173.6388 | 34.5323 | 66.1985 | 72.8935 |
| EuroCOVIDhub-baseline | 3988 | 705.4687 | 525.6101 | 60.8892 | 118.9566 |
| EuroCOVIDhub-ensemble | 3379 | 350.3998 | 157.7902 | 54.8508 | 137.7496 |
| ICM-agentModel | 152 | 922.3947 | 180.4868 | 677.2566 | 64.6842 |
| ISI-BLModel | 690 | 6.6739 | 1.0420 | 3.4290 | 2.1449 |
| ISI-SMtrend | 862 | 4.9304 | 0.4432 | 3.5348 | 0.8132 |
| Lydia-SARIMA | 3369 | 1550.9504 | 1439.4399 | 22.2155 | 89.2796 |
| Lydia-simpleARIMA | 2066 | 1604.2357 | 1456.0716 | 32.8369 | 115.3015 |
| PL_GRedlarski-DistrictsSum | 96 | 1493.7500 | 478.2604 | 489.6354 | 525.8646 |
| epiforecasts-EpiNow2 | 2949 | 391.8674 | 106.0000 | 151.4852 | 134.3554 |
| epiforecasts-tsensemble | 4913 | 307.0379 | 66.3943 | 128.4751 | 112.1486 |
| epiforecasts-weeklygrowth | 543 | 3496.5801 | 3011.4770 | 190.7495 | 294.3665 |
| fjordhest-ensemble | 2234 | 363.7153 | 100.4816 | 138.9785 | 124.2507 |

All 15 models are listed with their published and recomputed values in object/p3_reproduction_table.csv.
