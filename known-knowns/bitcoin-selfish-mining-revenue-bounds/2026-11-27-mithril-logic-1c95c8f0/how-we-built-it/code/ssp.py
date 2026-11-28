"""Own solver (written 2026-11-27 from SSZ arXiv 1507.06183 Table 1 + Sec 4.2, gamma=0).

Label-collapsed chain: at gamma=0 the fork labels (irrelevant/relevant/active) do not change any
transition probability or expected reward (match == wait), so the optimal bias can be taken
label-invariant: h(a,h,f) = W[a,h].  The exact checker re-expands all labels.

Stochastic-shortest-path form with gain penalty g: every action pays r - g; 'adopt' (and the forced
adopt at truncating states, paying the compensation C instead of -rho*h) stops with value 0.
Z(g) = alpha*W(1,0) + (1-alpha)*W(0,1) is the value of the post-adopt distribution X0.
If Z(g) <= 0 then h=W is an average-reward dual certificate with all residuals <= g.
Solved by Gauss-Seidel sweeps over anti-diagonals a+h = 2T..0.
modes: under (M^T, truncation pays -rho*h), printed (N^T as printed), corrected (both errata fixed:
E[last(a,h)] = 2K + ((a-h)/(1-2a)+a+h)/2 and E[a0|return] = h + a(h-a)/(1-2a)), max (pointwise max
of printed and corrected compensation; a certificate for 'max' is valid for both).
"""
import numpy as np, sys, time

def comp(alpha, rho, T, mode):
    """Truncating-state reward array C[a,h] (only entries with max(a,h)==T are used)."""
    al = alpha; K = al*(1-al)/(1-2*al)**2; q = al/(1-al)
    C = np.zeros((T+1, T+1))
    for x in range(T+1):
        # a = T >= h = x : eq. (7)
        a, h = T, x
        c7p = (1-rho)*(K + 0.5*((a-h)/(1-2*al) + a + h))          # eq. (7) as printed
        c7c = (1-rho)*(2*K + 0.5*((a-h)/(1-2*al) + a + h))        # Lemma 13 corrected: E[N]=2a/(1-2a)
        C[a, h] = {'under': -rho*h, 'printed': c7p, 'corrected': c7c, 'max': max(c7p, c7c)}[mode]
    for a in range(T):           # h = T > a : display after (7) / eq. (28)
        h = T; d = h - a; qd = q**d
        pr = (1-qd)*(-rho*h) + qd*(1-rho)*(K + d/(1-2*al))
        co = (1-qd)*(-rho*h) + qd*(1-rho)*(2*K + h + al*d/(1-2*al))
        C[a, h] = {'under': -rho*h, 'printed': pr, 'corrected': co, 'max': max(pr, co)}[mode]
    return C

class SSP:
    def __init__(self, alpha, T, mode):
        self.al, self.T, self.mode = alpha, T, mode
        n = T+1
        self.diags = []
        for k in range(2*T, -1, -1):
            a = np.arange(max(0, k-T), min(T, k)+1); h = k - a
            tr = (a == T) | (h == T)
            ov = (a > h) & ~tr
            self.diags.append((a, h, tr, ov, ~tr))
        self.W = np.zeros((n, n))

    def solve(self, rho, g, tol=1e-13, maxsweep=20000, W0=None, verbose=False):
        al, T = self.al, self.T
        C = comp(al, rho, T, self.mode)
        W = self.W if W0 is None else W0
        for sweep in range(maxsweep):
            delta = 0.0
            for a, h, tr, ov, nt in self.diags:
                adopt = -rho*h - g
                best = adopt.astype(float)
                # truncating: only adopt with compensation
                best = np.where(tr, C[a, h] - g, best)
                if nt.any():
                    an, hn = a[nt], h[nt]
                    wait = -g + al*W[an+1, hn] + (1-al)*W[an, hn+1]
                    b = best[nt]; best[nt] = np.maximum(b, wait)
                if ov.any():
                    ao, ho = a[ov], h[ov]
                    o = (1-rho)*(ho+1) - g + al*W[ao-ho, 0] + (1-al)*W[ao-ho-1, 1]
                    best[ov] = np.maximum(best[ov], o)
                old = W[a, h]
                delta = max(delta, float(np.max(np.abs(best-old))))
                W[a, h] = best
            if verbose and sweep % 50 == 0:
                print('sweep', sweep, 'delta', delta, flush=True)
            if delta < tol:
                break
        self.W = W
        Z = al*W[1, 0] + (1-al)*W[0, 1]
        return Z, sweep, delta

    def policy(self, rho, g):
        """Greedy action table ('a','w','o') for the current W (ties -> adopt, then wait)."""
        al, T, W = self.al, self.T, self.W
        C = comp(al, rho, T, self.mode)
        pol = [['a']*(T+1) for _ in range(T+1)]
        for a, h, tr, ov, nt in self.diags:
            adopt = -rho*h - g + 0.0
            wait = np.full(a.shape, -np.inf); o = np.full(a.shape, -np.inf)
            wait[nt] = -g + al*W[a[nt]+1, h[nt]] + (1-al)*W[a[nt], h[nt]+1]
            o[ov] = (1-rho)*(h[ov]+1) - g + al*W[a[ov]-h[ov], 0] + (1-al)*W[a[ov]-h[ov]-1, 1]
            for i in range(len(a)):
                if tr[i]: continue
                best, act = adopt[i], 'a'
                if wait[i] > best: best, act = wait[i], 'w'
                if o[i] > best: best, act = o[i], 'o'
                pol[a[i]][h[i]] = act
        return pol

    def gain(self, rho, tol=1e-13, verbose=False):
        """Optimal average gain g* (root of Z(g)=0) by secant iteration."""
        g0, Z0, _, _ = 0.0, *self.solve(rho, 0.0, tol)
        g1 = g0 + Z0/5.0
        Z1 = self.solve(rho, g1, tol)[0]
        for it in range(30):
            if Z1 == Z0: break
            g2 = g1 - Z1*(g1-g0)/(Z1-Z0)
            g0, Z0, g1 = g1, Z1, g2
            Z1 = self.solve(rho, g1, tol)[0]
            if verbose: print('  g', g1, 'Z', Z1, flush=True)
            if abs(Z1) < 1e-14: break
        return g1, Z1

if __name__ == '__main__':
    al, T, mode, rho = float(sys.argv[1]), int(sys.argv[2]), sys.argv[3], float(sys.argv[4])
    s = SSP(al, T, mode); t = time.time()
    Z, sw, de = s.solve(rho, 0.0, verbose=True)
    print('Z(0)=%.12e sweeps=%d delta=%.2e time=%.1fs' % (Z, sw, de, time.time()-t))
