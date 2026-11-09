# How we found it (contributor text, unverified)

An unattended V3R1T4S run (2026-10-15, heavy effort, main session Claude Opus 5.5) resumed the target
new-periodic-variables-not-in-vsx. Earlier runs that day had recovered known VSX periods but failed their own null:
a magnitude-shuffle bootstrap called half of the constant stars "significant" (lunar and daily-window systematics in
ZTF). A later (aborted) run froze a new statistic on that spent data only: a multi-band Lomb-Scargle with a narrow
alias mask, where the score S of the chosen peak is the smaller of its strengths in the two halves of the light curve
(split at the median time), so a period must replicate in time to count. This run then drew 80 fresh VSX
EW/EA/RRAB/DSCT stars and 400 fresh comparison stars (67 VSX CST, 333 Gaia DR3 non-variables) by pre-registered
seeds, fetched each star's ZTF light curve once from the SNAD API, and applied the frozen rule. 77 of the 80 periods
were recovered; every variable scored above every control; no control exceeded the pre-frozen threshold. Three fresh
reviewer contexts (REPRODUCE on a different model, NOVELTY, CRITERION) then checked the claim package only.

What failed alongside it in the same run: a hunt for 10 new variables with a second survey (TESS FFI photometry in a
crowded Galactic-plane quadrant did not confirm any ZTF candidate), and a hunt for 20 wrong Gaia-DR3 alias periods in
VSX (0 of 726 testable stars). What the gate shows is limited: most VSX periods it recovers came from ZTF themselves.
