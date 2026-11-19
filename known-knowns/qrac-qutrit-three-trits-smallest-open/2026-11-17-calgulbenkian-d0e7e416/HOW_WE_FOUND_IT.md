# How We Found It

*Contributor text, unverified.*

## Brief & Key Obstacles

In `arXiv:2312.14142`, the `0.69853` QDimSum SDP bound on `(n, d, D) = (3, 3, 3)` samples rank-1 projective operators on `C^3` and is invalid for general non-projective POVMs, while naive dense SOS certification over `O(10^3)` operator words consumes tens of gigabytes of RAM.

## What Worked

We lifted three arbitrary 3-outcome POVMs on `C^3` simultaneously via Stinespring/Naimark isometries into `H = C^3 tensor (C^3)^3` (`dim H = 81`) with qutrit subspace projector `V` (`Tr_H(V) = 3`), keeping `V tilde_M^i_a V tilde_M^i_b V` unreduced so arbitrary non-projective POVMs on `C^3` are covered unconditionally. Factoring the Reynolds average over `G = S_3 wr S_3` (`|G| = 1296`) split the `203`-word basis as shipped in the certificate (`I`, `V`, 27 `R_x`, 6 `M`, 6 `VM`, 162 `RM`; 1 + 1 + 27 + 6 + 6 + 162 = 203) into `78` exact rational blocks of size at most `6 x 6` (the shipped checker runs in < 40 MB RAM, as in `README.md` and `RUN_IT_YOURSELF.md`; measured peak resident memory 22.4 MB with `/usr/bin/time -l` on macOS, Python 3 without `mpmath`), yielding the exact rational dual bound `4368312591 / 6250000000 = 0.69893001456 <= 0.6990` (`p1`).
