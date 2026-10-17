import json, glob, itertools
import numpy as np
from tools.lib import tensors

def load_any_scheme(path):
    d = json.load(open(path))
    if "u_fresh" in d:
        return [np.array(x, dtype=np.int64) for x in tensors(d)]
    return [np.array(d[k], dtype=np.int64) for k in ("u", "v", "w")]

def get_signs(M1, M2):
    H1 = M1 @ np.linalg.pinv(M1)
    H2 = M2 @ np.linalg.pinv(M2)
    s = {}
    for start in range(len(M1)):
        if start in s: continue
        s[start] = 1
        q = [start]
        while q:
            u = q.pop(0)
            for v in range(len(M1)):
                if v not in s and abs(H2[u, v]) > 1e-4:
                    s[v] = s[u] if np.isclose(H1[u, v], H2[u, v], atol=1e-4) else -s[u]
                    q.append(v)
    return np.array([s[i] for i in range(len(M1))])

def gen_diag_Bn(n):
    mats = []
    # Fix first sign to +1 (since overall scalar (-I) cancels in X A Y^T): only 2^(n-1) matrices!
    for signs in itertools.product([1, -1], repeat=n-1):
        M = np.diag([1] + list(signs)).astype(np.int64)
        mats.append(M)
    return mats

def gen_small_Bn(n, max_perms=24):
    mats = []
    for idx, perm in enumerate(itertools.permutations(range(n))):
        if idx >= max_perms: break
        for signs in itertools.product([1, -1], repeat=n-1):
            full_s = [1] + list(signs)
            M = np.zeros((n, n), dtype=np.int64)
            for r, (c, sgn) in enumerate(zip(perm, full_s)):
                M[r, c] = sgn
            mats.append(M)
    return mats

Diag_cache = {n: gen_diag_Bn(n) for n in [3, 4, 5, 6, 8]}
Small_cache = {n: gen_small_Bn(n, max_perms=12) for n in [3, 4, 5, 6, 8]}

def get_candidates(sub_fmt, n1, n2, n3, ref_U0, ref_V0, ref_W0):
    T_ref = np.einsum("ri,rj,rk->ijk", ref_U0, ref_V0, ref_W0)
    cands = [("ref", (ref_U0, ref_V0, ref_W0))]
    paths = (
        glob.glob(f".{sub_fmt}_m*_ZT.json") +
        glob.glob(f".{sub_fmt}_m*_ZT_reduced.json") +
        glob.glob(f".{sub_fmt}_m*_Z.json") +
        glob.glob(f"./work/VAULT_WIN_{sub_fmt}_m*.json")
    )
    m_target = len(ref_U0)
    for p in paths:
        try:
            U, V, W = load_any_scheme(p)
            if len(U) != m_target: continue
            if np.max(np.abs(U)) > 1 or np.max(np.abs(V)) > 1 or np.max(np.abs(W)) > 1: continue
            T = np.einsum("ri,rj,rk->ijk", U, V, W)
            if np.array_equal(T, T_ref):
                cands.append((p.split("/")[-1], (U, V, W)))
        except Exception:
            pass
    for name, (U, V, W) in list(cands):
        if n2 == n3:
            Ut = W.reshape(m_target, n3, n1).transpose(0, 2, 1).reshape(m_target, n1*n2)
            Vt = V.reshape(m_target, n2, n3).transpose(0, 2, 1).reshape(m_target, n2*n3)
            Wt = U.reshape(m_target, n1, n2).transpose(0, 2, 1).reshape(m_target, n3*n1)
            cands.append((name + "_T23", (Ut, Vt, Wt)))
        if n1 == n2:
            Ut = U.reshape(m_target, n1, n2).transpose(0, 2, 1).reshape(m_target, n1*n2)
            Vt = W.reshape(m_target, n3, n1).transpose(0, 2, 1).reshape(m_target, n2*n3)
            Wt = V.reshape(m_target, n2, n3).transpose(0, 2, 1).reshape(m_target, n3*n1)
            cands.append((name + "_T12", (Ut, Vt, Wt)))
    return cands

refs = {
    "3x4x4": (3, 4, 4, load_any_scheme(".")),
    "3x4x5": (3, 4, 5, load_any_scheme(".")),
    "3x4x6": (3, 4, 6, load_any_scheme(".")),
    "3x5x5": (3, 5, 5, load_any_scheme(".")),
    "3x5x6": (3, 5, 6, load_any_scheme(".")),
}

cand_pool = {}
for k, (n1, n2, n3, (U0, V0, W0)) in refs.items():
    cand_pool[k] = get_candidates(k, n1, n2, n3, U0, V0, W0)

def solve_block(Ub, Vb, Wb, sub_fmt, perm):
    n1, n2, n3, (U0, V0, W0) = refs[sub_fmt]
    L = len(U0)
    mats0 = [U0, V0, W0]
    M0_u, M0_v, M0_w = mats0[perm[0]], mats0[perm[1]], mats0[perm[2]]
    
    if sub_fmt == "3x4x4":
        keep = [r for r in range(38) if r not in {14, 27, 28, 37, 30, 36}]
    else:
        keep = list(range(L))
    
    su = get_signs(Ub, M0_u)
    sv_k = get_signs(Vb[keep], M0_v[keep])
    sw_k = su[keep] * sv_k
    C_keep = np.diag(sw_k) @ M0_w[keep]
    PW = np.round(np.linalg.lstsq(C_keep, Wb[keep], rcond=None)[0]).astype(np.int64)
    sigma = 1
    if not np.array_equal(Wb[keep], C_keep @ PW):
        sw_k = -su[keep] * sv_k
        sigma = -1
        C_keep = np.diag(sw_k) @ M0_w[keep]
        PW = np.round(np.linalg.lstsq(C_keep, Wb[keep], rcond=None)[0]).astype(np.int64)
    
    A_keep = np.diag(su[keep]) @ M0_u[keep]
    B_keep = np.diag(sv_k) @ M0_v[keep]
    PU = np.round(np.linalg.lstsq(A_keep, Ub[keep], rcond=None)[0]).astype(np.int64)
    PV = np.round(np.linalg.lstsq(B_keep, Vb[keep], rcond=None)[0]).astype(np.int64)
    
    P_orig = [None, None, None]
    P_orig[perm[0]] = PU
    P_orig[perm[1]] = PV
    P_orig[perm[2]] = PW
    P_U, P_V, P_W = P_orig[0], P_orig[1], P_orig[2]
    
    for cache in [Diag_cache, Small_cache]:
        B_n1, B_n2, B_n3 = cache[n1], cache[n2], cache[n3]
        for cname, (Uc, Vc, Wc) in cand_pool[sub_fmt]:
            U_3d = Uc.reshape(L, n1, n2)
            V_3d = Vc.reshape(L, n2, n3)
            W_3d = Wc.reshape(L, n3, n1)
            XU = [np.einsum("ab,rbc->rac", X, U_3d) for X in B_n1]
            for ix, xu in enumerate(XU):
                X = B_n1[ix]
                valid_Z = []
                WX = np.einsum("rbc,dc->rbd", W_3d, X)
                for iz, Z in enumerate(B_n3):
                    w_zx = np.einsum("ab,rbd->rad", Z, WX).reshape(L, n3*n1)
                    wp = w_zx @ P_W
                    if np.max(np.abs(wp)) <= 1:
                        valid_Z.append((iz, Z, wp))
                if not valid_Z: continue
                for iy, Y in enumerate(B_n2):
                    u_xy = np.einsum("rac,dc->rad", xu, Y).reshape(L, n1*n2)
                    up = u_xy @ P_U
                    if np.max(np.abs(up)) > 1: continue
                    YV = np.einsum("ab,rbc->rac", Y, V_3d)
                    for iz, Z, wp in valid_Z:
                        v_yz = np.einsum("rac,dc->rad", YV, Z).reshape(L, n2*n3)
                        vp = v_yz @ P_V
                        if np.max(np.abs(vp)) <= 1:
                            out = [up, vp, wp]
                            return sigma * out[perm[0]], out[perm[1]], out[perm[2]], f"{cname}(ix={ix},iy={iy},iz={iz})"
    return None, None, None, None

jobs = [
    ("9x10x16", 920, (9, 10, 16), [
        (204, 68, "3x5x6", (0, 1, 2)),
        (434, 47, "3x4x5", (2, 1, 0)),
        (690, 68, "3x5x6", (0, 1, 2)),
        (826, 47, "3x4x5", (2, 1, 0)),
    ]),
    ("9x10x13", 763, (9, 10, 13), [
        (58,  47, "3x4x5", (2, 1, 0)),
        (105, 47, "3x4x5", (2, 1, 0)),
        (188, 47, "3x4x5", (2, 1, 0)),
        (235, 58, "3x5x5", (2, 1, 0)),
        (340, 58, "3x5x5", (2, 1, 0)),
        (398, 47, "3x4x5", (2, 1, 0)),
        (445, 47, "3x4x5", (2, 1, 0)),
        (492, 58, "3x5x5", (2, 1, 0)),
        (550, 47, "3x4x5", (2, 1, 0)),
        (622, 47, "3x4x5", (2, 1, 0)),
        (669, 47, "3x4x5", (2, 1, 0)),
        (716, 47, "3x4x5", (2, 1, 0)),
    ]),
    ("6x12x14", 654, (6, 12, 14), [
        (20,  54, "3x4x6", (0, 1, 2)),
        (74,  54, "3x4x6", (0, 1, 2)),
        (204, 38, "3x4x4", (0, 1, 2)),
        (280, 38, "3x4x4", (0, 1, 2)),
        (448, 54, "3x4x6", (0, 1, 2)),
        (502, 38, "3x4x4", (0, 1, 2)),
        (540, 38, "3x4x4", (0, 1, 2)),
    ]),
]

for fmt, m, n_dims, blocks in jobs:
    print(f"================ {fmt} (m={m}) ================")
    d = json.load(open(f".{fmt}_m{m}_Z.json"))
    U_new = np.array(d["u"], dtype=np.int64)
    V_new = np.array(d["v"], dtype=np.int64)
    W_new = np.array(d["w"], dtype=np.int64)
    for s, L, sub_fmt, perm in blocks:
        uu, vv, ww, info = solve_block(U_new[s:s+L], V_new[s:s+L], W_new[s:s+L], sub_fmt, perm)
        if uu is not None:
            U_new[s:s+L], V_new[s:s+L], W_new[s:s+L] = uu, vv, ww
            print(f"  [{s:3d}..{s+L-1:3d}] {sub_fmt} -> TERNARY at rank {L} via {info}")
        else:
            print(f"  [{s:3d}..{s+L-1:3d}] {sub_fmt} -> NO zero-rank match in current pool")
    print(f"{fmt} Global max_abs:", np.max(np.abs(U_new)), np.max(np.abs(V_new)), np.max(np.abs(W_new)))
    if np.max(np.abs(U_new)) <= 1 and np.max(np.abs(V_new)) <= 1 and np.max(np.abs(W_new)) <= 1:
        n1, n2, n3 = n_dims
        errors = 0
        for a in range(n1*n2):
            i1, j1 = divmod(a, n2)
            ua = U_new[:, a]
            nz = np.where(ua != 0)[0]
            M_bc = (V_new[nz] * ua[nz, None]).T @ W_new[nz]
            expected = np.zeros((n2*n3, n3*n1), dtype=np.int64)
            for kk in range(n3):
                expected[j1*n3 + kk, kk*n1 + i1] = 1
            errors += int(np.sum(M_bc != expected))
        print(f"  >>> {fmt} EXACT BRENT ERRORS OVER Z: {errors}")
        if errors == 0:
            out_path = f"./work/{fmt}_m{m}_ZT.json"
            with open(out_path, "w") as f:
                json.dump({"n": list(n_dims), "m": m, "u": U_new.tolist(), "v": V_new.tolist(), "w": W_new.tolist()}, f)
            print(f"  >>> Saved verified {fmt} ZT scheme of rank {m} to {out_path}!")
