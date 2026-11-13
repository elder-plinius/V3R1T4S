# PREREG.v11: amendment to PREREG.v10 templates (frozen 2026-11-12T22:19:50Z, before the lens-6 scan of 1973 starts)

Nothing from 1973 has been read for lens 6 (the lens-5 S14 scan of 1973 is running and none of its output has been
read). Reason, from 1972 dev data only (attempts/s14-s16-coinc-1973/out/dev_s16_glitchiness.txt): one-sided LP
glitches are common in the 1972 A1 event windows (max|x|/rms > 8 in 31-33% of S14 and 45% of S16 windows); the
PREREG.v10 builder chose the reference 1972-328 20:50, whose S16 channels are glitch-dominated (16.4, 18.6), and
stacked only 7 members into glitch-dominated S16 templates (max|t|/rms 15.8, 19.1; out/build_stdout.txt).

Change: templates are built with tools/nesttemplates2.py, identical to the frozen builder except that a member's
channel window with max|x|/rms > 8 is left out of that channel's stack, and the reference is the event with the
largest positive A1 + A2 + A4 among those whose four reference-window channels pass the same screen. Result on dev:
reference 1972-164 23:48, 34 members, template max|t|/rms 4.1, 3.8, 4.2, 3.5
(frozen/A1_net_s14s16_dev1972_templates_v11.npz; hashes in out/hashes_v11.txt). Everything else in PREREG.v10
(statistic, null set, readings, checks) is unchanged.
