# How We Found It

*Contributor text, unverified.*

## Brief & Key Obstacles

Sun and Zeilberger (2004) proved Fraenkel's 3-heap Wythoff conjectures for `0 <= A_1 <= 10`, but omitted the `N_3^i` and `B^i_{N_3^i}` columns required by Claim 3.5 Condition 6 for `A_1 = 11` and relied on Maple symbolic generating functions for Claim 3.3.

## What Worked

We wrote an independent C retrograde solver (`fraenkel_wythoff.c`) generating `P^m` from the raw normal-play game rules for `0 <= m <= 11`, reconstructed all omitted `(N_3^i, B^i_{N_3^i})` thresholds (`max_{0 <= i <= 10} B^i_{N_3^i} = 1801`), replaced symbolic generating-function checks in Claim 3.3 with finite XOR-periodicity window witnesses of length `p(m) + 1` (`17` for `m = 11`, uncovering the outlier `1252 in S^11`), and verified the Claim 3.5 witness pair `(n_2, n_1) = (1216, 3249)` via a zero-shared-code Python checker (`verify_wythoff.py`).
