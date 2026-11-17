# Receipts

Output of `sh verify-it-yourself/run_checks.sh` (run 2026-11-13T11:25:47Z, Python 3.11, standard library only; exit status 0):

```
detection: NCC MH1 0.7268, MH2 0.7567, D 0.7417; controls 401, best control 0.2868
G1: 113 catalogued S14 MH1/MH2 spike intervals within the onset +/- 24 h (longest 25.208 s); overlapping the window: 0; nearest start after the onset MH1 +7347.963 s, MH2 +3013.925 s; last end before the window MH1 -35349.093 s, MH2 -32440.867 s; spikes starting 1971-05-13 10:00-19:00 UTC: 0
G2: rule-flagged raw samples MH1 0 (MAD 4.0), MH2 0 (MAD 6.0); muted samples 0; lag 0: NCC 0.7268 / 0.7567, D 0.7417; best lag +0.000 s: NCC 0.7268 / 0.7567, D 0.7417; threshold D > 0.2868 -> pass
PASS
```
