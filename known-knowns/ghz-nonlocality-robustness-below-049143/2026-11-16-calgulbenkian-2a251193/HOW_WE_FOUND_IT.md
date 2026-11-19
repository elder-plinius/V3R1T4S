# How We Found It

_Note: contributor text, unverified._

1. **Non-planar Bloch latitudes (`nonplanar-bloch-rings`)**: Testing multi-ring 3D Bloch measurements (`run_nonplanar_study.py`) confirmed that adding out-of-plane settings increases $m_A + m_B$ faster than the GHZ phase correlation gain at tractable local-bound sizes.
2. **Asymmetric commensurate planar polygons `(18, 24, 72)` (`exact-orbit-bnb-planar`)**: In $L = \max_{a,b} \sum_{k=0}^{m_C-1} |\sum_{i,j} M_{ijk} a_i b_j|$, Party C's setting count $m_C$ costs only $O(m_C)$ time while $m_A + m_B$ costs $2^{m_A + m_B}$. Choosing $(m_A, m_B, m_C) = (18, 24, 72)$ (`lcm(18, 24) = 72`) gives full $\pi/72$ phase resolution ($\cos((4i+3j+k)\pi/72)$) while keeping $m_A + m_B = 42 < 44$ (strictly smaller exponent than symmetric $22 \times 22 \times 22$). Quotienting Alice by $D_{36}$ (`3,771` orbits) and Bob by $C_{48}$ (`349,536` orbits) reduced all $2^{42}$ strategies to `1,318,100,256` orbit pairs, certified in seconds by two independent C++17 enumerators (`L = 130,692,616`, $v^* \le 0.4913971114274656713239022$).
