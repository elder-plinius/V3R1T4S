# Receipts: real output of sh verify-it-yourself/run_checks.sh

started: Sat Oct 31 13:50:42 UTC 2026
```
step 1: sha256 of every file in object/
object/: 18 files, all sha256 match
step 2: fetch the pinned public inputs and check their sha256
fetched and verified 40 input files from commit 802a3ded
step 3: build the verifier
step 4: run the full verification (about 5 minutes on 4 threads)
[00:00:05] cover 12       : zooms  6, terminal cells    49 (witness 49, handed over 0), accepted 49, rejected 0, domain-witness cells 0, problems 0
[00:00:05] cover 13       : zooms  6, terminal cells    12 (witness 12, handed over 0), accepted 12, rejected 0, domain-witness cells 0, problems 0
[00:00:05] cover 14       : zooms  6, terminal cells    45 (witness 45, handed over 0), accepted 45, rejected 0, domain-witness cells 0, problems 0
[00:00:06] cover 15       : zooms  6, terminal cells    15 (witness 15, handed over 0), accepted 15, rejected 0, domain-witness cells 0, problems 0
[00:00:06] cover 16       : zooms  6, terminal cells    39 (witness 39, handed over 0), accepted 39, rejected 0, domain-witness cells 0, problems 0
[00:00:06] cover 17       : zooms  6, terminal cells    22 (witness 22, handed over 0), accepted 22, rejected 0, domain-witness cells 0, problems 0
[00:00:06] cover 18       : zooms  6, terminal cells    19 (witness 19, handed over 0), accepted 19, rejected 0, domain-witness cells 0, problems 0
[00:00:06] cover 19       : zooms  6, terminal cells    67 (witness 67, handed over 0), accepted 67, rejected 0, domain-witness cells 0, problems 0
[00:00:06] cover 20       : zooms  6, terminal cells    17 (witness 17, handed over 0), accepted 17, rejected 0, domain-witness cells 0, problems 0
[00:00:06] cover 21       : zooms  6, terminal cells    25 (witness 25, handed over 0), accepted 25, rejected 0, domain-witness cells 0, problems 0
[00:00:06] cover 22       : zooms  6, terminal cells    31 (witness 31, handed over 0), accepted 31, rejected 0, domain-witness cells 0, problems 0
[00:00:06] cover 23       : zooms  6, terminal cells    35 (witness 35, handed over 0), accepted 35, rejected 0, domain-witness cells 0, problems 0
[00:00:06] cover 24       : zooms  6, terminal cells    17 (witness 17, handed over 0), accepted 17, rejected 0, domain-witness cells 0, problems 0
[00:00:06] cover 25       : zooms  6, terminal cells    29 (witness 29, handed over 0), accepted 29, rejected 0, domain-witness cells 0, problems 0
[00:00:06] cover 26       : zooms  6, terminal cells    19 (witness 19, handed over 0), accepted 19, rejected 0, domain-witness cells 0, problems 0
[00:00:06] cover 27       : zooms  6, terminal cells    17 (witness 17, handed over 0), accepted 17, rejected 0, domain-witness cells 0, problems 0
[00:00:06] cover 28       : zooms  6, terminal cells    11 (witness 11, handed over 0), accepted 11, rejected 0, domain-witness cells 0, problems 0
[00:00:07] cover 29       : zooms  6, terminal cells    85 (witness 85, handed over 0), accepted 85, rejected 0, domain-witness cells 0, problems 0
[00:00:08] cover square   : zooms 18, terminal cells   877 (witness 877, handed over 0), accepted 877, rejected 0, domain-witness cells 95, problems 0
[00:00:16] cover pentagon : zooms 24, terminal cells  6173 (witness 6173, handed over 0), accepted 6173, rejected 0, domain-witness cells 0, problems 0
[00:00:16] cover arc+     : zooms  7, terminal cells   343 (witness 343, handed over 0), accepted 343, rejected 0, domain-witness cells 32, problems 0
[00:00:17] cover arc-     : zooms  7, terminal cells   288 (witness 288, handed over 0), accepted 288, rejected 0, domain-witness cells 72, problems 0
[00:00:17] cover endpoint+: zooms 21, terminal cells   305 (witness 305, handed over 0), accepted 305, rejected 0, domain-witness cells 10, problems 0
[00:00:17] cover endpoint-: zooms 21, terminal cells   246 (witness 246, handed over 0), accepted 246, rejected 0, domain-witness cells 50, problems 0
[00:00:20] cover crossing+: zooms 28, terminal cells  1465 (witness 1431, handed over 34), accepted 1465, rejected 0, domain-witness cells 31, problems 0
[00:00:21] cover crossing-: zooms 28, terminal cells   701 (witness 687, handed over 14), accepted 701, rejected 0, domain-witness cells 160, problems 0
[00:00:21] zoom cells: total 11231 (witness cells 11183 + handed over 48); accepted 11231, rejected 0; counts match paper table (Local 833, square 877, pentagon 6173, arc 343/288, endpoint 305/246, crossing 1431/687, han
[00:00:24] records Domain: 12650 (expected 12650), accepted 12650, rejected 0, 3.4s 
[00:04:14] records Global: 157458 (expected 157458), accepted 157458, rejected 0, 229.5s 
[00:04:14] records Local : 21792 (expected 21792), accepted 21792, rejected 0, 0.3s 
[00:04:14] records Exotic: 796 (expected 796), accepted 796, rejected 0, 0.0s 
[00:04:49] control [wrong inequality index (Domain)]: tried 100, certified-false 100, refused 100, ACCEPTED 0, (uncertified mutants accepted: 0)
[00:04:49] control [wrong edge or plug vertex (Global)]: tried 120, certified-false 120, refused 120, ACCEPTED 0, (uncertified mutants accepted: 0)
[00:04:49] control [perturbed path (bit flip, Domain/Global)]: tried 115, certified-false 100, refused 100, ACCEPTED 0, (uncertified mutants accepted: 15)
[00:04:49] control [box outside named cover (Local/Exotic, other cover or shifted box)]: tried 123, certified-false 120, refused 120, ACCEPTED 0, (uncertified mutants accepted: 3)
[00:04:49] control [wrong component label]: tried 100, certified-false 100, refused 100, ACCEPTED 0, (uncertified mutants accepted: 0)
[00:04:49] control [certificate framing/coverage corruption]: tried 71, certified-false 71, refused 71, ACCEPTED 0, (uncertified mutants accepted: 0)
[00:04:49] control [zoom-cover cell corruption (witness / factor / validity)]: tried 112, certified-false 100, refused 100, ACCEPTED 0, (uncertified mutants accepted: 2)
[00:04:49] CONTROLS total: 711 certified-false corrupted claims, 711 refused, 0 accepted (must be 0; need >=400 certified)
[00:04:49] OVERALL: ALL CHECKS PASSED
PASS
```
finished: Sat Oct 31 13:56:16 UTC 2026
