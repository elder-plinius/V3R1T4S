#!/usr/bin/env python3
"""
Lens 1 Python: Sapirshtein-Sompolinsky-Zohar (SSZ) Bitcoin Selfish Mining MDP.
Reference: arXiv:1507.06183 Section 4.2 (gamma = 0).

Under-paying finite MDP: M_rho^T
Over-paying finite MDP:  N_rho^T
"""

import sys
import numpy as np

def s_idx(t, a, h, fork):
    return (a * (t + 1) + h) * 3 + fork

def num_states(t):
    return (t + 1) * (t + 1) * 3

class SSZModel:
    def __init__(self, alpha, t, rho, overpaying=False, comp_var=2):
        self.alpha = float(alpha)
        self.t = int(t)
        self.rho = float(rho)
        self.overpaying = bool(overpaying)
        self.comp_var = int(comp_var)
        self.n_states = num_states(self.t)
        self.actions_list = [[] for _ in range(self.n_states)]
        self._build_transitions()

    def _build_transitions(self):
        t = self.t
        alpha = self.alpha
        rho = self.rho
        denom = 1.0 - 2.0 * alpha
        term1 = (alpha * (1.0 - alpha)) / (denom * denom)

        for a in range(t + 1):
            for h in range(t + 1):
                for fork in range(3):
                    s = s_idx(t, a, h, fork)
                    if a == t or h == t:
                        if not self.overpaying:
                            r_adopt = -rho * float(h)
                        else:
                            if a == t:
                                term2 = 0.5 * (float(a - h) / denom + float(a + h))
                                if self.comp_var == 1:
                                    r_adopt = (1.0 - rho) * term1 + term2
                                else:
                                    r_adopt = (1.0 - rho) * (term1 + term2)
                            else:
                                ratio = (alpha / (1.0 - alpha)) ** (h - a)
                                term_ret = term1 + float(h - a) / denom
                                r_adopt = (1.0 - ratio) * (-rho * float(h)) + ratio * (1.0 - rho) * term_ret
                        self.actions_list[s].append(([(alpha, s_idx(t, 1, 0, 0)), (1.0 - alpha, s_idx(t, 0, 1, 0))], r_adopt, "adopt"))
                        continue

                    # 1. Adopt
                    r_adopt = -rho * float(h)
                    self.actions_list[s].append(([(alpha, s_idx(t, 1, 0, 0)), (1.0 - alpha, s_idx(t, 0, 1, 0))], r_adopt, "adopt"))

                    # 2. Override
                    if a > h:
                        r_over = (1.0 - rho) * float(h + 1)
                        self.actions_list[s].append(([(alpha, s_idx(t, a - h, 0, 0)), (1.0 - alpha, s_idx(t, a - h - 1, 1, 1))], r_over, "override"))

                    # 3. Match
                    if fork == 1 and a >= h and h > 0:
                        self.actions_list[s].append(([(alpha, s_idx(t, a + 1, h, 2)), (1.0 - alpha, s_idx(t, a, h + 1, 1))], 0.0, "match"))

                    # 4. Wait
                    if fork != 2:
                        self.actions_list[s].append(([(alpha, s_idx(t, a + 1, h, 0)), (1.0 - alpha, s_idx(t, a, h + 1, 1))], 0.0, "wait"))
                    elif fork == 2 and a > h and h > 0:
                        self.actions_list[s].append(([(alpha, s_idx(t, a + 1, h, 2)), (1.0 - alpha, s_idx(t, a, h + 1, 1))], 0.0, "wait"))

    def solve_rvi(self, tol=1e-6, max_iter=3000):
        v = np.zeros(self.n_states, dtype=np.float64)
        for it in range(max_iter):
            min_diff = float('inf')
            max_diff = float('-inf')
            for s in range(self.n_states):
                max_q = float('-inf')
                for succs, r, _ in self.actions_list[s]:
                    q = r + sum(p * v[ns] for p, ns in succs)
                    if q > max_q:
                        max_q = q
                diff = max_q - v[s]
                if diff < min_diff: min_diff = diff
                if diff > max_diff: max_diff = diff
                v[s] = max_q

            span = max_diff - min_diff
            v -= v[0]
            if span < tol:
                gain = 0.5 * (max_diff + min_diff)
                return gain, v
        return 0.5 * (max_diff + min_diff), v
