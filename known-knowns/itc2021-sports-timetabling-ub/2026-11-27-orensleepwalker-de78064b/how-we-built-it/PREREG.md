Frozen UTC: 2026-11-27T14:51:49Z
Purpose: one batched claim of the partial wins (lower-bound certificates) on target itc2021-sports-timetabling-ub, decided by Boss on 2026-11-27 ("I want the full wins and the partials to be filed separately"; "Do it"). Filing waits for Boss's explicit yes.
Disclosure: the certificates were made before this plan by Bobby (Early 14, Early 9; each already passed a three-reviewer panel as its own package) and Charlie (Middle 6, Middle 9, Late 9); the checks of attempts/contrarian-check were run before this plan was frozen.

null_test: not needed because each result is a deterministic proof (a solver model replayed to optimality and a standalone derivation), not a statistical claim.

Objects (fixed now): the files listed in data/object_list.csv (sha256 cee2b99500246d4ccdba0ab0c9846cd2d75474f9b86394c9d2b5fdecf9adf0c0).
Criterion: partial win itc2021-lower-bound-certificate, separately for each instance: the saved model file, replayed in a fresh session with one worker and the recorded seed, proves a bound strictly above the instance's posted Best LB on the board (data/board.html, sha256 e008069e04f701038edce32190c5ecb5a978067c251bedd26f00c08740832f75) and above every bound on its history page; supported by a standard-library certificate script that re-derives the same bound from the original instance file.
Counting rule (at claim-build time): a row stays only if its model replays OPTIMAL at the claimed bound, its certificate script reproduces the bound, the bound is strictly above every posted bound and at or below the score of a known feasible timetable (posted Best UB or ours); otherwise it is dropped and listed. Before filing, the board and the five history pages are re-fetched.
Not claimed: any new timetable (a separate claim); optimality of any instance except that Early 14's bound equals its posted Best UB; that the bounds are best possible.
Review: three fresh skeptics (REPRODUCE, NOVELTY, CRITERION); REPRODUCE re-derives every bound independently and judges whether each model contains only constraints valid for every feasible timetable. The claim passes only if all three pass.
