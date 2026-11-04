Written post-hoc on 2026-10-19T10:54:45Z for kit layout; content transcribed from PREREG.md / REPORT_K.md / logs; no measurement added.

id: constant-weight-codes

## Object of Stage K
Cell A(25,6,11) (n 25, d 6, w 11) of the Brouwer table https://aeb.win.tue.nl/codes/Andw.html (mirror cell A(25,6,14)). Stage K is a finite seed evaluation (<= 90 min total): six sequential engine runs of the plateau walk (lb_lns_gen.py via the corrected wrapper j7_run.py) from the immutable 8,732 candidate: R0 control (seed 105, 120 s, --stop-at-M 8733) and R1..R5 new seeds 201..205 (600 s each) (PREREG.md). Not a record attempt.

dead: no

## Bank cell and bars (from PREREG.md / REPORT_K.md)
- Live table lower bound L = 8,718 [Pl], upper bound U = 24,630, read 2026-10-18T21:39:24Z (data/Andw_live.html, sha256 15b15c8df1a507e2403b84b322dfb2268f16c8597794b9ece23dd03532513349; no re-read in Stage K, 0 GET).
- Open upstream PR 437 claims 8,720 (state at 2026-10-18T21:40Z; not re-checked).
- Input: CANDIDATE_M8732.npy sha256 0f9c84b89764187cd6780bf7fe234b8de08d7f48e5156d157ca2b3145b2c4868 (TXT twin e66b06b68ab8a06a40f1cea36254008d781f047a69597464abc0aad04b150f26), never overwritten.
- Best object of Stage K: A(25,6,11) M = 8,734, TXT sha256 f9f280613ee2a5c500220a9f022d35d83264a14f96d940c9a517a15cebdf6fde (seed 201, t = 568 s), both exact checkers valid (also re-checked by the owner after the engines were dead).
- Working criterion: candidate lower bound > L (and > any value in the literature and open/closed/merged PRs), pending live comparison.
- Status: CANDIDATE PENDING LIVE COMPARISON; not a record. The R0 control object 8,733 (4f972f16..., seed 105) is the earlier I1 test object, reproduced as a recovery control and not counted as a new hit.

## Outcome of Stage K (REPORT_K.md)
Closed 2026-10-19T10:44:41Z (supervisor end), control recovered (K1), 3 of 5 new seeds (201, 202, 204) reached M >= 8,733 within 600 s; seeds 203 and 205 did not (censored at 600 s, best 8,732); best 8,734. Preregistered reading: ">= 2/5: evidence to present for a decision, never an automatic next stage".

## Success criterion (verbatim from repo/bank/targets.json, as copied in stage H target.md)

Success means an explicit list of M distinct binary vectors of length n, each with Hamming weight exactly w, with all pairwise distances >= d (d even), where M is STRICTLY GREATER (direction: max) than the lower bound shown at verification time in the (n,d,w) cell of https://aeb.win.tue.nl/codes/Andw.html (also checking the mirror cell A(n,d,n-w)), and also strictly greater than any value for that cell in arXiv:2608.13906 (Echols, 124 improved cells), arXiv:2607.19550 (Lysenstoen) or any newer arXiv paper. M must not exceed the tabulated upper bound; exceeding it means a bug.
