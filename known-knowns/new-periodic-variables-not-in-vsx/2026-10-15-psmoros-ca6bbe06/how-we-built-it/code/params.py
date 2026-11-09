"""Frozen parameters (chosen on spent run-1407 data in stage A; see out/stage_a_full.txt)."""
DELTA = 5e-5        # alias mask half-width (c/d), family 'full': m*day/k + s*b, day in {1, sidereal}, k<=4, b in {0, j/29.530589, j/365.25}
MODE = "full"
FLOW = 0.05         # lowest searched frequency used in the pick (c/d): P_rec <= 20 d
T_THRESH = 54.0     # FAR threshold T: max spent-control S was 53.2 (0/512 spent controls above T)
N_VAR, N_CTRL = 80, 400
