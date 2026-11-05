"""LogSumExp surrogate of the largest cosine and its gradient.

Float64. Blocks of the Gram matrix keep the working memory at 8*B*N bytes.
"""
from __future__ import annotations

import numpy as np

EXP_FLOOR = -60.0


class LogSumExp:
    def __init__(self, n: int, d: int, block: int = 128):
        self.N, self.D = n, d
        self.B = min(block, n)
        self._block = np.empty((self.B, n))
        self._grad = np.empty((n, d))
        self._pts = np.empty((n, d))
        self._blocks = [(i0, min(i0 + self.B, n)) for i0 in range(0, n, self.B)]
        self._rows = np.arange(self.B)

    def value_and_grad(self, x_flat, beta):
        n, d = self.N, self.D
        x = np.reshape(x_flat, (n, d))
        norm = np.sqrt(np.einsum("ij,ij->i", x, x))[:, None] + 1e-16
        np.divide(x, norm, out=self._pts)
        pts = self._pts
        grad = self._grad
        nb = len(self._blocks)
        m_k = np.empty(nb)
        sum_k = np.empty(nb)
        floor = 3.0 * beta > 700.0
        for k, (i0, i1) in enumerate(self._blocks):
            g = self._block[: i1 - i0]
            np.matmul(pts[i0:i1], pts.T, out=g)
            rows = self._rows[: i1 - i0]
            g[rows, rows + i0] = -2.0
            m = float(g.max())
            g -= m
            g *= beta
            if floor:
                np.maximum(g, EXP_FLOOR, out=g)
            np.exp(g, out=g)
            g[rows, rows + i0] = 0.0
            m_k[k] = m
            sum_k[k] = g.sum()
            np.matmul(g, pts, out=grad[i0:i1])
        m = float(m_k.max())
        w = np.exp(beta * (m_k - m))
        total = 0.5 * float(sum_k @ w)
        grad *= np.repeat(w, [i1 - i0 for i0, i1 in self._blocks])[:, None]
        grad /= total
        grad -= np.einsum("ij,ij->i", grad, pts)[:, None] * pts
        grad /= norm
        val = m + np.log(total) / beta
        return val, grad.ravel().copy()
