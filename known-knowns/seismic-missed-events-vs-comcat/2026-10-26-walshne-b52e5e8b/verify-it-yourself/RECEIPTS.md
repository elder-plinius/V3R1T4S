# Receipts

A real run of `sh verify-it-yourself/run_checks.sh` from this folder (offline mode), 2026-10-26T22:04:54Z, Python 3.14.6, macOS.

```
ok    object/early_per_control_max.csv matches SHA256SUMS
ok    object/event.json matches SHA256SUMS
ok    object/mc_histograms.csv matches SHA256SUMS
ok    object/null_per_control_max.csv matches SHA256SUMS
ok    object/picks.csv matches SHA256SUMS
ok    8 P/S picks (>= 8)
ok    5 stations (>= 4)
ok    pick and station counts equal event.json
ok    coordinates of NN.BFC P equal event.json
ok    coordinates of NN.BFC S equal event.json
ok    coordinates of NN.KVN P equal event.json
ok    coordinates of NN.KVN S equal event.json
ok    coordinates of NN.PNT P equal event.json
ok    coordinates of NN.PNT S equal event.json
ok    coordinates of NN.WASH S equal event.json
ok    coordinates of NN.YER S equal event.json
      relocation: 39.1635 N 119.0459 W 7.0 km, origin 2024-12-09T23:20:13.27, RMS 0.1787 s, horizontal error 3.446 km (276 nodes)
ok    best node equals event.json
ok    origin time equals event.json
ok    RMS equals event.json (0.1787)
ok    horizontal error equals event.json (3.446)
ok    residual NN.BFC_P equals event.json
ok    residual NN.BFC_S equals event.json
ok    residual NN.KVN_P equals event.json
ok    residual NN.KVN_S equals event.json
ok    residual NN.PNT_P equals event.json
ok    residual NN.PNT_S equals event.json
ok    residual NN.WASH_S equals event.json
ok    residual NN.YER_S equals event.json
ok    location bars: RMS <= 0.3 s and horizontal error <= 5 km
ok    WA ML median of 8 stations 1.590
ok    calibration offset 0.0895 over 6 events
ok    calibrated WA ML 1.6795 (stored values rounded to 3 decimals)
ok    median ML over event/noise >= 2 stations 1.6275
ok    M_coloc 1.723 over 10 events
ok    M_cons = min(M_rel, calibrated, M_coloc) = 1.680
      Mc over 24 query/binning cells: 1.0-1.8; largest 1.8
ok    24 Mc cells (12 live ComCat queries x floor/round binning)
ok    p1: smallest magnitude estimate 1.590 >= largest Mc - 0.3 = 1.5
      main win (M >= Mc 1.8): not met (not claimed)
ok    600 controls (400 on 12-10..12, 200 on 12-09)
ok    every control: 7 stations shifted by whole minutes in [10, 1430], all >= 10 min apart
ok    controls >= event NCC 0.6705: 0
ok    best control 0.6121
ok    expected false count 0.0000 < 0.05
ok    3000 early-hours controls with the stated shift design
ok    early-hours: 1 control(s) >= 0.6706, EFC 0.0120
ok    authoritative region NN
ok    ComCat +/-30 s, 50 km: 0 events
ok    ISC +/-30 s, 0.45 deg: no event (HTTP 204)
VERIFIED p1: event 2024-12-09T23:20:13.27, RMS 0.1787 s, herr 3.446 km, M >= 1.590 vs Mc - 0.3 = 1.5, EFC 0.0000
PASS
```
