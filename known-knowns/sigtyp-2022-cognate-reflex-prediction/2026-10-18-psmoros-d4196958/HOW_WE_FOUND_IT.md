# How we found it (contributor text, unverified)

The six systems were built in run 2026-10-18-0202 of a V3R1T4S workspace under a clean protocol (every development choice
on validation data cut from training-0.50, disjoint from the test set at every proportion), and their NED-targeted
per-item combination was confirmed at 0.30 on mean NED (package 2026-10-18-psmoros-634f2c35). That run's main session then
pre-registered, for the other two metrics, new combinations of the same systems whose per-item risk is the metric itself
(here item BLEU instead of item NED), with weights fit on the validation split cut from training-0.30, froze their
predictions with hashes, and left the test scoring to a later session. The next session scored all six such objects
once: only this one (BLEU at 0.30) beat the highest value known on its metric, which was our own NED-targeted object.
The gain is small (0.0035 BLEU) and comes mostly from kesslersignificance, birchallchapacuran and hillburmish.
