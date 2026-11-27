# Controls (PREREG: null_test not needed - deterministic exhaustive enumeration; these are tamper controls of the checker)
controls: 400
best_control: 0
real: 1
real_beats_all_controls: yes
score: 1 = claim/code/verify_claim.py accepts, 0 = rejects. Kinds: 100 other pair starts (+-1..150 ranks), 100 pi6 shifts, 100 block-table edits, 100 prefix shifts; all 400 rejected, real accepted.
command: cd claim/code && python3 tamper_controls.py   (output claim/outputs/tamper_controls.out)
Positive controls: twins -> 1369391 and cousins -> 5206837 reproduced (claim/outputs/small2_100663296.out).
