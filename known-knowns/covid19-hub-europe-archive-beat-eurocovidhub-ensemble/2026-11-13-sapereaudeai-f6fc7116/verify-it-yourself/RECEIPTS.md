# RECEIPTS: real output of `sh verify-it-yourself/run_checks.sh` (run from the package folder)

run at 2026-11-13T06:12:32Z with Python 3.11.15

```
ok   object sha256 f6fc71163c4247914cb1f832649ed956887aabef08de4bc353e1904e2662f8e0
ok   30 rows (15 models x 2 truth modes): 30
ok   published means recorded for ECDC-norrsken_blue (owidhosp)
ok   published means recorded for ECDC-norrsken_blue (primary)
ok   published means recorded for ECDC-norrsken_green (owidhosp)
ok   published means recorded for ECDC-norrsken_green (primary)
ok   published means recorded for ECDC-soca_simplex (owidhosp)
ok   published means recorded for ECDC-soca_simplex (primary)
ok   published means recorded for EuroCOVIDhub-baseline (owidhosp)
ok   published means recorded for EuroCOVIDhub-baseline (primary)
ok   published means recorded for EuroCOVIDhub-ensemble (owidhosp)
ok   published means recorded for EuroCOVIDhub-ensemble (primary)
ok   published means recorded for ICM-agentModel (owidhosp)
ok   published means recorded for ICM-agentModel (primary)
ok   published means recorded for ISI-BLModel (owidhosp)
ok   published means recorded for ISI-BLModel (primary)
ok   published means recorded for ISI-SMtrend (owidhosp)
ok   published means recorded for ISI-SMtrend (primary)
ok   published means recorded for Lydia-SARIMA (owidhosp)
ok   published means recorded for Lydia-SARIMA (primary)
ok   published means recorded for Lydia-simpleARIMA (owidhosp)
ok   published means recorded for Lydia-simpleARIMA (primary)
ok   published means recorded for PL_GRedlarski-DistrictsSum (owidhosp)
ok   published means recorded for PL_GRedlarski-DistrictsSum (primary)
ok   published means recorded for epiforecasts-EpiNow2 (owidhosp)
ok   published means recorded for epiforecasts-EpiNow2 (primary)
ok   published means recorded for epiforecasts-tsensemble (owidhosp)
ok   published means recorded for epiforecasts-tsensemble (primary)
ok   published means recorded for epiforecasts-weeklygrowth (owidhosp)
ok   published means recorded for epiforecasts-weeklygrowth (primary)
ok   published means recorded for fjordhest-ensemble (owidhosp)
ok   published means recorded for fjordhest-ensemble (primary)
ok   owidhosp: all 15 models within 1% on all four components (max |rel| 3.198e-06)
ok   primary: models over 1% = ['EuroCOVIDhub-baseline', 'EuroCOVIDhub-ensemble', 'Lydia-SARIMA', 'Lydia-simpleARIMA', 'epiforecasts-tsensemble', 'epiforecasts-weeklygrowth', 'fjordhest-ensemble']
ok   primary: max |rel| 0.02136 (Lydia-simpleARIMA underprediction)
ok   owidhosp: 3 non-exact rows, all half-integer rounding ties
ok   primary: 534 non-exact rows = 531 inc hosp CZ + 3 rounding ties
ok   WIS interval form = pinball form (max diff 3.64e-12)
ok   known positive: point mass
ok   known negative: 1/(K+1) normalisation differs (max diff 2.34e+01)
PASS
(exit status 0)
```
