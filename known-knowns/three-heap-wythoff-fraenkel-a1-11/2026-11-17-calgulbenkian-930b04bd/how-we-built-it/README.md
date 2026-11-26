# How We Built It

Built a clean-room retrograde 3-heap Wythoff solver in C (`fraenkel_wythoff.c`) computing `P^m` for `0 <= m <= 11` directly from normal-play move rules, reconstructing all omitted inductive thresholds `(N_3^i, B^i_{N_3^i})` for `0 <= i <= 10`, certifying Claim 3.3 via finite `p(m) + 1` XOR-periodicity window witnesses (`p(11) = 16`), and locating the Claim 3.4 threshold `N = 15` and Claim 3.5 witness pair `(n_2, n_1) = (1216, 3249)` (`j_chop = 1990, m_1 = 1993`), verified independently by a zero-shared-code Python checker (`verify_wythoff.py`).
