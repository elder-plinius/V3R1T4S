# How it was built (exact commands)

Engine: `lb_lns_gen.py` (+ `lns6.py`, `gslib.py`, `convert_seed.py`), unchanged from V3R1T4S (elder-plinius/V3R1T4S,
commit 9b1d444eb864a1475e092047d49612a7410a7c5a, `known-knowns/bigger-codes/how-we-built-it/`, AGPL-3.0). Kick tool:
`kick.py` (this campaign). Python 3.12.6, `requirements.txt`. All walks: `NUMBA_NUM_THREADS=2`, supervisor at
below-normal priority, `--rounds 1000000`.

1. Seed: Brouwer's archive code `a26.6.9.5761H` (J. Boisclair), https://aeb.win.tue.nl/codes/cwc/d6/a26.6.9.5761H,
   fetched 2026-10-16T19:46:58Z, HTTP 200, sha256 6b03be5b14e314750b018a1face90e5da6c6f884820ceba8611a4038c6ebe1b5;
   `python convert_seed.py a26.6.9.5761H 26 9 seed.npy` (5761 words).
2. 5761 -> 5988: `lb_lns_gen.py seed.npy 26 6 9 cal_a26_6_9_s1 --seconds 600 --seed 1` (4 threads), saved as A26_6_9_5988_cal_s1.npy.
3. 5988 -> 5991: walk seed 22, 2400 s (sha256 a392519d...).
4. 5991 -> 5993: walk seed 104, 3600 s (a583fe37...). 5. 5993 -> 5995: walk seed 209 (f29bd85b...).
6. 5995 -> 5996: walk seed 308 (cbf3c3f2...).
7. 5996 plateau states: walk seed 409 from step 6 (final state bfc69c12...), walk seed 509 continuing it
   (final a544e032...), then `kick.py <that> 100 609 k.npy` and walk seed 609 from k.npy (final state
   9cd2b75584fbde4a77c5bc73137a27bbd6c195e22ceb36db57813780623a0ade, 5996 words).
8. `python kick.py <step-7 final>.npy 2000 709 kick_r2000_s709.npy` (3996 words), then
   `python lb_lns_gen.py kick_r2000_s709.npy 26 6 9 b7_kick_r2000_s709 --seconds 3600 --rounds 1000000 --seed 709`
   (2026-10-17T03:06:14Z-04:06:21Z, exit 0; 5997 at 1146 s, round 625) -> b7_kick_r2000_s709_best.npy, written as
   sorted 0/1 lines (character j = bit j) to object/A26_6_9_5997.txt.
Preregistrations: PREREG.focus.md and .v2 to .v9 (each frozen before the batches it governs). Walks are randomised
and multi-threaded; a rerun may end elsewhere. The object is checked directly.
