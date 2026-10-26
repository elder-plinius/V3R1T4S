"""Minimal VNN-LIB 2.0 reader for attacks (not the judge): input box and the output assertion as a disjunction of
conjunctions of linear atoms  sum_k a_k Y_k + b  >= 0.  Returns numpy arrays.
  spec = load(path) -> dict(ishape, oshape, lo, hi, disjuncts=[(A [m, ny], b [m])...])
Every input-only assertion must be a simple bound (<= X[..] c) / (>= X[..] c); anything else raises."""
import gzip, re
from fractions import Fraction
import numpy as np

TOK = re.compile(r"\(|\)|[^\s()]+")


def _sexprs(text):
    text = "\n".join(l.split(";", 1)[0] for l in text.splitlines())
    st = [[]]
    for t in TOK.findall(text):
        if t == "(":
            st.append([])
        elif t == ")":
            top = st.pop(); st[-1].append(top)
        else:
            st[-1].append(t)
    assert len(st) == 1
    return st[0]


def _shape(s):
    return [int(v) for v in s.strip("[]").split(",") if v.strip()]


def load(path):
    raw = open(path, "rb").read()
    if path.endswith(".gz"):
        raw = gzip.decompress(raw)
    text = raw.decode()
    # tokens like X[0,1,2,3] may contain spaces after commas in some files: normalise
    text = re.sub(r"\[\s*([\d,\s]+?)\s*\]", lambda m: "[" + re.sub(r"\s+", "", m.group(1)) + "]", text)
    forms = _sexprs(text)
    ishape = oshape = None
    asserts = []
    for f in forms:
        if f[0] == "declare-network":
            for d in f[2:]:
                if d[0] == "declare-input":
                    ishape = _shape(d[3])
                elif d[0] == "declare-output":
                    oshape = _shape(d[3])
        elif f[0] == "assert":
            asserts.append(f[1])
    assert ishape and oshape, "not a VNN-LIB 2.0 file"
    nx, ny = int(np.prod(ishape)), int(np.prod(oshape))
    lo = np.full(nx, np.nan); hi = np.full(nx, np.nan)
    out_asserts = []

    def ref(tok):
        m = re.fullmatch(r"([XY])\[([\d,]+)\]", tok)
        if not m:
            return None
        idx = [int(v) for v in m.group(2).split(",")]
        shp = ishape if m.group(1) == "X" else oshape
        return m.group(1), int(np.ravel_multi_index(idx, shp))

    def lin(e):
        """linear expression over Y -> (dict k->coef, const) in Fractions"""
        if isinstance(e, str):
            r = ref(e)
            if r:
                assert r[0] == "Y", "input variable in an output expression"
                return {r[1]: Fraction(1)}, Fraction(0)
            return {}, Fraction(e)
        op, args = e[0], [lin(a) for a in e[1:]]
        if op == "+":
            c, k = {}, Fraction(0)
            for cc, kk in args:
                for i, v in cc.items(): c[i] = c.get(i, 0) + v
                k += kk
            return c, k
        if op == "-":
            if len(args) == 1:
                return {i: -v for i, v in args[0][0].items()}, -args[0][1]
            c, k = dict(args[0][0]), args[0][1]
            for cc, kk in args[1:]:
                for i, v in cc.items(): c[i] = c.get(i, 0) - v
                k -= kk
            return c, k
        if op == "*":
            c, k = args[0]
            for cc, kk in args[1:]:
                if not c:
                    c, k = {i: v * k for i, v in cc.items()}, k * kk
                else:
                    assert not cc, "nonlinear product"
                    c, k = {i: v * kk for i, v in c.items()}, k * kk
            return c, k
        raise ValueError("unsupported op %r" % op)

    def atom(e):
        op, a, b = e
        ca, ka = lin(a); cb, kb = lin(b)
        c = dict(ca)
        for i, v in cb.items(): c[i] = c.get(i, 0) - v
        k = ka - kb  # a - b
        if op == "<=":
            c = {i: -v for i, v in c.items()}; k = -k
        else:
            assert op == ">=", op
        A = np.zeros(ny); 
        for i, v in c.items(): A[i] = float(v)
        return A, float(k)

    for a in asserts:
        if a[0] in ("<=", ">=") and isinstance(a[1], str) and isinstance(a[2], str) and a[1].startswith("X") and not a[2].startswith(("X", "Y")):
            _, i = ref(a[1]); v = float(Fraction(a[2]))
            if a[0] == "<=":
                hi[i] = v if np.isnan(hi[i]) else min(hi[i], v)
            else:
                lo[i] = v if np.isnan(lo[i]) else max(lo[i], v)
        elif a[0] in ("<=", ">=") and isinstance(a[2], str) and a[2].startswith("X") and not a[1].startswith(("X", "Y")):
            _, i = ref(a[2]); v = float(Fraction(a[1]))
            if a[0] == ">=":
                hi[i] = v if np.isnan(hi[i]) else min(hi[i], v)
            else:
                lo[i] = v if np.isnan(lo[i]) else max(lo[i], v)
        else:
            out_asserts.append(a)
    assert not np.isnan(lo).any() and not np.isnan(hi).any(), "unbounded input"
    # output part: conjunction of top-level assertions; each is or/and/atom. Build DNF (only or-of-and supported).
    def dnf(e):
        if e[0] == "or":
            res = []
            for s in e[1:]: res += dnf(s)
            return res
        if e[0] == "and":
            res = [[]]
            for s in e[1:]:
                res = [r + t for r in res for t in dnf(s)]
            return res
        return [[atom(e)]]
    d = [[]]
    for a in out_asserts:
        d = [r + t for r in d for t in dnf(a)]
    disj = [(np.array([A for A, _ in conj]), np.array([k for _, k in conj])) for conj in d]
    return dict(ishape=ishape, oshape=oshape, lo=lo, hi=hi, disjuncts=disj)


if __name__ == "__main__":
    import sys
    s = load(sys.argv[1])
    w = s["hi"] - s["lo"]
    print("ishape", s["ishape"], "oshape", s["oshape"], "n_disjuncts", len(s["disjuncts"]),
          "atoms per disjunct", sorted(set(len(b) for _, b in s["disjuncts"])),
          "width min/max", w.min(), w.max(), "pinned (lo==hi)", int((w == 0).sum()))
