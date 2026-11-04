"""Shared numerics for the lemma-proofs lens (float64; NUMERICAL evidence only).
Regular Reuleaux n-gon B_n of width 1, centred at the origin, corners V_k at angle 2 pi k/n,
circumradius R_n = 1/(2 cos(pi/(2n))).
Support function (derived in LEMMAS.md L7):  with delta = pi/(2n) and k = nearest integer to theta/(pi/n):
   k even -> vertex interval, h = <V_{k/2}, u>;   k odd -> arc interval, h = <V_j,u> + 1 with 2j+n = k (mod 2n).
"""
import numpy as np
from scipy.spatial import ConvexHull

def Rn(n): return 1.0/(2.0*np.cos(np.pi/(2*n)))
def corners(n, rho=0.0):
    a = 2*np.pi*np.arange(n)/n + rho
    return Rn(n)*np.stack([np.cos(a), np.sin(a)], 1)

def hB(n, theta):
    """support function of B_n (centred, unrotated), vectorised."""
    theta = np.asarray(theta, float)
    k = np.rint(theta/(np.pi/n)).astype(np.int64)
    u = np.stack([np.cos(theta), np.sin(theta)], -1)
    R = Rn(n)
    out = np.empty(theta.shape)
    ev = (k % 2 == 0)
    jv = (k//2) % n                      # vertex index when k even
    ja = (((k - n)//2) % n)              # arc index when k odd (k-n even)
    j = np.where(ev, jv, ja)
    ang = 2*np.pi*j/n
    dot = R*(np.cos(ang)*u[..., 0] + np.sin(ang)*u[..., 1])
    return np.where(ev, dot, dot + 1.0)

def boundary_points(n, rho=0.0, t=(0.0, 0.0), per_arc=200):
    """points on the boundary arcs of rho-rotated, t-translated B_n (all lie in B_n up to rounding)."""
    pts = []
    R = Rn(n)
    for j in range(n):
        aj = 2*np.pi*j/n
        phi = aj + np.pi + np.linspace(-np.pi/(2*n), np.pi/(2*n), per_arc)
        c = np.array([R*np.cos(aj), R*np.sin(aj)])
        pts.append(c + np.stack([np.cos(phi), np.sin(phi)], 1))
    P = np.vstack(pts)
    c, s = np.cos(rho), np.sin(rho)
    P = P @ np.array([[c, s], [-s, c]]) + np.asarray(t)
    return P

def disc_points(N=4000, r=0.5):
    a = 2*np.pi*np.arange(N)/N
    return r*np.stack([np.cos(a), np.sin(a)], 1)

def hull_area(P): return ConvexHull(P).volume

def A_inner(t3, rho, t5, per_arc=300, N=4000):
    P = np.vstack([disc_points(N), boundary_points(3, 0.0, t3, per_arc), boundary_points(5, rho, t5, per_arc)])
    return hull_area(P)

def A_outer(t3, rho, t5, N=20000):
    th = 2*np.pi*np.arange(N)/N
    u = np.stack([np.cos(th), np.sin(th)], 1)
    h = np.maximum.reduce([np.full(N, 0.5),
                           hB(3, th) + u @ np.asarray(t3),
                           hB(5, th - rho) + u @ np.asarray(t5)])
    d = 2*np.pi/N
    hp, hn = np.roll(h, -1), np.roll(h, 1)
    l = (hp + hn - 2*h*np.cos(d))/np.sin(d)
    return 0.5*float(np.sum(h*l))

def f(d):
    d = np.asarray(d, float)
    return 0.25*(np.pi - np.arccos(0.5/d)) + 0.5*np.sqrt(d*d - 0.25)
