# How We Found It (`lychrel-new-base-proof`)

_Contributor text, unverified._

1. **Carry-Wire Decoupling Theorem:**
   Consider a family of four base-$b$ templates ($m \ge 1$):
   $$T_1(m) = L_0 \; (b-1)^m \; M_0 \; 0^m \; R_0, \qquad T_2(m) = L_1 \; 0^m \; M_1 \; (b-1)^m \; R_1,$$
   $$T_3(m) = L_0 \; (b-1)^m \; M_2 \; 0^m \; R_0, \qquad T_4(m) = L_1 \; 0^m \; M_3 \; (b-1)^m \; R_1,$$
   where $|L_0| = |R_0| = |L_1| = |R_1| = \ell$. Because the two variable-length repeated blocks $(b-1)^m$ and $0^m$ sit at exact mirror offsets $[\ell, \ell+m)$ from the left and right ends of every template $T_i(m)$, every aligned digit pair in those blocks sums to $(b-1) + 0 = b - 1$. Thus an incoming carry $c_{\text{in}} = 0$ produces $(b-1) + 0 + 0 = b - 1$ (emitting $(b-1)^m$ with uniform outgoing carry $c_{\text{out}} = 0$), and an incoming carry $c_{\text{in}} = 1$ produces $(b-1) + 0 + 1 = b$ (emitting $0^m$ with uniform outgoing carry $c_{\text{out}} = 1$), for **all** $m \ge 1$.

2. **Decoupled Outside-In Finite-State BFS Solvers ($b \equiv 2 \pmod{24}$):**
   The Carry-Wire Decoupling Theorem splits the Period-4 cycle condition $T_1(m) \to T_2(m) \to T_3(m) \to T_4(m) \to T_1(m+1)$ into two independent finite-word problems:
   - **Period-2 Outer Engine on $(L_0, R_0)$ (`how-we-built-it/search_engines.py`):** Requires $R_0 + \operatorname{Rev}(L_0) = R_1$ ($c_R = 0$), $L_0 + \operatorname{Rev}(R_0) + 1 = L_1$ ($c_L = 0$), $R_1 + \operatorname{Rev}(L_1) = b^\ell + R_0$ ($c_R = 1$), and $L_1 + \operatorname{Rev}(R_1) = L_0 \cdot [b-1]$ (overflowing by 1 digit into the left carry wire). At the outermost position $k = 0$, the carry transition forces $3 x_0 = 2b + 1$, which is solvable if and only if $b \equiv 2 \pmod{3}$.
   - **Period-4 Inner Core on $M_0$ (`how-we-built-it/search_inner.py`):** Requires $M_0 \to M_1 \to M_2 \to M_3 \to M_0 \cdot [0]$ with outgoing carries $(1, 0, 1, 0)$ into the left carry wire and incoming carries $(0, 1, 0, 1)$ from the right carry wire. At the outer positions of $M_0$, the 4-step recurrence forces $8 m_0 = 3b + 2$, which is solvable if and only if $b \equiv 2 \pmod{8}$.
   Combining both congruences gives the arithmetic progression $b \equiv 2 \pmod{24}$ ($b = 26, 50, \dots$). Running our outside-in 4-carry BFS solvers reproduced David Seal's 1996 Base-26 solution ($\ell = 8, |M_0| = 4$) and discovered the minimal Period-4 Lychrel template cycle in base $b = 50 = 2 \cdot 5^2 \notin \{2^k, 11, 17, 20, 26\}$ ($\ell = 36, |M_0| = 8, |T_1(1)| = 82$, `object/lychrel_base50_certificate.json`). (Companion packages #723, #724, and #725 cover bases 98, 146, and the Kuitché 2023 audit respectively.)

3. **Vectorized Carry-Lookahead 100,000-Step Orbit Simulation:**
   To simulate $100,000$ reverse-and-add steps of the 82-digit base-50 start $n = T_1(1)$ up to $50,082$ base-50 digits in `15.77s`, `verify-it-yourself/check_lychrel.py` uses the exact carry-lookahead identity $c_{\text{out}}[k] = \mathbf{1}[r[\text{last\_idx}[k]] \ge b]$ where $\text{last\_idx}[k] = \max(\{0\} \cup \{j \le k : r[j] \neq b - 1\})$, evaluated in one vectorized `numpy` prefix-max operation (`np.maximum.accumulate(np.where(r != b - 1, IDX[:L], 0))`), matching every iterate against compiled regular expressions (`re.Pattern.fullmatch`).
