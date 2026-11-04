# Receipts (real output of `sh verify-it-yourself/run_checks.sh`, exit status 0, 2026-10-19T23:07:14Z)

```
ok   benchmark.json.zip 71f06783ae0baa3183f30548d20fad9cdc6662cf66aaea72c7ecf8868160f6c3
ok   sha256 object/ensemble.json
ok   sha256 object/models/mace_Mo_seed1.model
ok   sha256 object/models/mace_Mo_seed2.model
ok   sha256 object/models/mace_Mo_seed3.model
ok   sha256 object/predictions_Mo_forces_test.csv
ok   benchmark json sha256
ok   csv header
ok   prediction ids == official test ids (23)
ok   every prediction has the right number of components
components 3567  force MAE 0.097399761160953391 eV/A
ok   MAE equals INDEX.csv value 0.09739976116095339
ok   MAE 0.097400 <= 0.95 * listed best 0.18434104563832232 (= 0.175124): improvement 47.2%
ok   training ids used == benchmark train ids (194)
ok   no test id in the training list
ok   mlearn_figshare.zip f731b3ad5ac3e1b083a7ce12936a9e0e6aa2704de2a1b95150429823c1398a28
max |re-run - predictions file| = 2.398e-07 eV/A over 23 test structures
PASS
PASS
```
