# PREREG v2 (frozen 2026-10-24T19:34:52Z, date -u). Supersedes PREREG.md section 2 for the arrival pick only. No real gauge series has been scored in this run.

null_test: required

Why: the synthetic known-positive / known-negative test of lib/det.py (attempts/evaluator-first/code/test_det.py,
out/test_det.txt) showed that the zero-phase (forward-backward) Butterworth rings before a sharp onset: a synthetic
1.5 m wave starting at ETA + 0 crossed 3 RMS24 at ETA - 29.5 min, so it failed the +/-10 min arrival rule although
r = 142. This is the "large near-field tsunamis are lost" problem NEXT_RUN.md asks to fix, found on synthetic data only.

Change (one): arrival = first minute in [o+ETA-30, o+ETA+60] where the CAUSAL band-passed series (the same order-4,
1/120 cpm Butterworth run forward only, per contiguous segment >= 6 h with the same gap bridging and glitch rule,
initial state at steady state for the first sample) exceeds 3 x its own RMS over [o-24 h, o-1 min]. A causal filter
cannot respond before the input changes. r (peak / RMS24 on the zero-phase series), the 5x bar, the +/-10 min window,
USABLE, control days and everything else stay exactly as in PREREG.md. Re-test: out/test_det_v2.txt (the 1.5 m case
now arrives at ETA + 0.55 min and detects; both negatives still do not detect).
