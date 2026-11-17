# Receipts: real output of verify-it-yourself/run_checks.sh

Run 2026-11-13T05:56:02Z .. 2026-11-13T05:56:45Z (date -u) from this package folder on the contributor's laptop, with local
copies of the pinned inputs (HUB, EXT and EXT2 set to folders holding the files listed in pinned_inputs.txt,
pinned_published.txt and pinned_published2.txt; every file's sha256 is checked by the script). Output, verbatim:

```
inputs: 250 files, sha256 mismatches or missing: 0
wk inc rsv hosp             CEPH-Rtrend_rsv              tasks  5300 mean WIS 31.43541542 (table 31.43541542) ok
wk inc rsv hosp             CFA_Pyrenew-Pyrenew_HE_RSV   tasks  3101 mean WIS 23.45485979 (table 23.45485979) ok
wk inc rsv hosp             CFA_Pyrenew-Pyrenew_H_RSV    tasks  3382 mean WIS 25.36274837 (table 25.36274837) ok
wk inc rsv hosp             Google_SAI-RSVEns            tasks  4784 mean WIS 15.30923981 (table 15.30923981) ok
wk inc rsv hosp             RSVHub-baseline              tasks  7950 mean WIS 30.28666837 (table 30.28666837) ok
wk inc rsv hosp             RSVHub-ensemble              tasks  6763 mean WIS 27.72865565 (table 27.72865565) ok
wk inc rsv hosp             UGA_flucast-INFLAenza        tasks  6148 mean WIS 39.24776202 (table 39.24776202) ok
wk inc rsv hosp             UM-DeepOutbreak              tasks  1300 mean WIS 105.878174 (table 105.878174) ok
wk inc rsv prop ed visits   CFA_Pyrenew-Pyrenew_E_RSV    tasks  3259 mean WIS 0.0005531363221 (table 0.0005531363221) ok
wk inc rsv prop ed visits   CFA_Pyrenew-Pyrenew_HE_RSV   tasks  3062 mean WIS 0.0009063365863 (table 0.0009063365863) ok
wk inc rsv prop ed visits   RSVHub-baseline              tasks  7650 mean WIS 0.0007264871051 (table 0.0007264871051) ok
wk inc rsv prop ed visits   RSVHub-ensemble              tasks  6382 mean WIS 0.0008875321877 (table 0.0008875321877) ok
wk inc rsv prop ed visits   UGA_flucast-INFLAenza        tasks  5750 mean WIS 0.0008338636496 (table 0.0008338636496) ok
published subset Google_SAI-RSVEns    tasks 4576 mean WIS 14.635 published 14.7 ok
published subset RSVHub-ensemble      tasks 4576 mean WIS 16.422 published 16.4 ok
published subset CEPH-Rtrend_rsv      tasks 4576 mean WIS 19.804 published 19.8 ok
published subset RSVHub-baseline      tasks 4576 mean WIS 18.306 published 18.3 ok
object/p3_era_subset.txt: 8 model lines recomputed, 0 mismatches ok
object/p3_exclusions.txt: task counts {'wk inc rsv hosp': '38728', 'wk inc rsv prop ed visits': '26103'} vs recomputed {'wk inc rsv hosp': 38728, 'wk inc rsv prop ed visits': 26103} ok
published row-level scores: 26248 rows rescored with the published truth, 0 without a hub forecast, max |diff| 1.36e-12 ok
EpiBenchmark rows: 11648 rescored (5 levels, truth as_of 2026-09-16), 0 unmatched, max |diff| 6.82e-13 ok
tapestry RSVHub-ensemble cells: 20 checked (23 levels, truth as_of 2026-09-02), max relative |diff| 1.23e-13 ok
tapestry hub-evaluation (RSVHub-ensemble, UGA_flucast-INFLAenza, both targets): 4 values checked, max relative |diff| 4.71e-14 ok
tapestry google-comparison (pooled Google_SAI-RSVEns WIS on 4692 tasks, 51 x 2 per-location sums): max relative |diff| 6.66e-16 ok
PASS
```

Negative test (same day): with one digit of object/p3_era_subset.txt changed, the checker printed
"object/p3_era_subset.txt: 8 model lines recomputed, 1 mismatches MISMATCH" and FAIL.
