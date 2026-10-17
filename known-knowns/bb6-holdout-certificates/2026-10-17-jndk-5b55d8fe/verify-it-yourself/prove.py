# Independent symbolic checker for the seven macro identities of
# 1RB1LC_1LC0RD_0LE1LA_0RF1RA_1LA0LA_---0RB (symbolic lens of the V3R1T4S p1 package; see REPRODUCE.md).
# Rules are read from RULES_JSON, an embedded copy of result/rules.json appended by the REPRODUCE.md assembly.
import sys, json, itertools
import sympy as sp

MACHINE = "1RB1LC_1LC0RD_0LE1LA_0RF1RA_1LA0LA_---0RB"
STATES = "ABCDEF"

def parse_machine(s):
    T = {}
    for si, part in enumerate(s.split("_")):
        for r in range(2):
            t = part[3 * r:3 * r + 3]
            if t == "---":
                continue
            T[(STATES[si], r)] = (int(t[0]), 1 if t[1] == "R" else -1, t[2])
    return T

TM = parse_machine(MACHINE)
k, j = sp.symbols("k j", integer=True, nonnegative=True)

class Fail(Exception):
    pass

# ---------------------------------------------------------------- parsing
def parse_pattern(s, kval, xval):
    """Return list of tokens: ('H',) marker, ('r', bit, count) runs. Power applies to the
    single preceding bit only. kval: sympy expr substituted for k; xval: 0/1."""
    # spaces are kept: an unbracketed exponent ends at a space or end of string (no greedy swallowing)
    out = []
    i = 0
    while i < len(s):
        c = s[i]
        if c == " ":
            i += 1; continue
        if c == "A":
            out.append(("H",)); i += 1; continue
        if c in "01x":
            bit = xval if c == "x" else int(c)
            i += 1
            cnt = sp.Integer(1)
            if i < len(s) and s[i] == "^":
                i += 1
                if s[i] == "(":
                    d = 1; e = i + 1
                    while d:
                        if s[e] == "(": d += 1
                        elif s[e] == ")": d -= 1
                        e += 1
                    expr = s[i + 1:e - 1]; i = e
                else:
                    e = i
                    while e < len(s) and s[e] != " ":
                        e += 1
                    expr = s[i:e]; i = e
                    import re as _re
                    if not (_re.fullmatch(r"\d+", expr) or expr == "k"):
                        raise ValueError("ambiguous unbracketed exponent %r in %r" % (expr, s))
                import re
                # only digits, k, + - * and parentheses: anything else (e.g. "2j-1", a Python complex literal) is rejected
                if not re.fullmatch(r"[0-9k+\-*() ]+", expr):
                    raise ValueError("exponent %r in %r uses symbols other than k" % (expr, s))
                expr = re.sub(r"(\d)k", r"\1*k", expr)
                cnt = sp.sympify(expr, locals={"k": k})
                if not cnt.free_symbols <= {k} or not cnt.is_integer:
                    raise ValueError("exponent %r in %r is not an integer expression in k" % (expr, s))
                cnt = cnt.subs(k, kval)
            out.append(("r", bit, sp.expand(cnt)))
            continue
        raise ValueError("bad char %r in %r" % (c, s))
    if sum(1 for t in out if t[0] == "H") != 1:
        raise ValueError("need exactly one marker in %r" % s)
    return out

def canon(tokens):
    """Merge adjacent equal-bit runs; drop identically-zero runs."""
    res = []
    for t in tokens:
        if t[0] == "H":
            res.append(t); continue
        _, b, n = t
        n = sp.expand(n)
        if n == 0:
            continue
        if res and res[-1][0] == "r" and res[-1][1] == b:
            res[-1] = ("r", b, sp.expand(res[-1][2] + n))
        else:
            res.append(("r", b, n))
    return res

def canon_eq(a, b):
    if len(a) != len(b):
        return False
    for p, q in zip(a, b):
        if p[0] != q[0]:
            return False
        if p[0] == "r" and (p[1] != q[1] or sp.expand(p[2] - q[2]) != 0):
            return False
    return True

def fmt(c):
    s = []
    for t in c:
        if t[0] == "H": s.append("A")
        elif t[0] == "r": s.append("%d^(%s)" % (t[1], t[2]))
        elif t[0] == "w": s.append("(%s)^(%s)" % ("".join(map(str, t[1])), t[2]))
    return " ".join(s)

# ---------------------------------------------------------------- concrete checker
def concrete_check(inp, outp, steps_expr, kv, xv, exact=True):
    """Window-only naive simulation; reading outside window raises Fail."""
    ti = canon(parse_pattern(inp, sp.Integer(kv), xv))
    to = canon(parse_pattern(outp, sp.Integer(kv), xv))
    def expand(c):
        cells, h = [], None
        for t in c:
            if t[0] == "H": h = len(cells)
            else: cells += [t[1]] * int(t[2])
        return cells, h
    tape, h = expand(ti)
    want, wh = expand(to)
    if len(tape) != len(want):
        raise Fail("window length mismatch %d vs %d" % (len(tape), len(want)))
    N = int(steps_sym(steps_expr).subs(k, kv))
    st = "A"
    for t in range(N):
        if h < 0 or h >= len(tape):
            raise Fail("k=%d x=%d: head left window at step %d" % (kv, xv, t))
        key = (st, tape[h])
        if key not in TM:
            raise Fail("k=%d x=%d: halted at step %d" % (kv, xv, t))
        wb, mv, ns = TM[key]
        tape[h] = wb; h += mv; st = ns
    if h < 0 or h >= len(tape):
        raise Fail("k=%d x=%d: head outside window at end" % (kv, xv))
    if st != "A" or h != wh or tape != want:
        raise Fail("k=%d x=%d: after %d steps state=%s head=%d (want %d) tape=%s want=%s"
                   % (kv, xv, N, st, h, wh, "".join(map(str, tape)), "".join(map(str, want))))
    return N

def steps_sym(steps_str):
    import re
    if not re.fullmatch(r"[0-9k+\-*^() ]+", steps_str):
        raise ValueError("step count %r uses symbols other than k" % steps_str)
    e = re.sub(r"(\d)k", r"\1*k", steps_str).replace("^", "**")
    v = sp.sympify(e, locals={"k": k})
    if not v.free_symbols <= {k}:
        raise ValueError("step count %r is not an expression in k" % steps_str)
    return v

# ---------------------------------------------------------------- symbolic engine
# tape items: ('b', bit) | ('w', word_tuple, exp) | ('E',)
MAXU = 8

def lin_parts(e):
    e = sp.expand(e)
    a = e.coeff(j, 1); b = e.subs(j, 0)
    if sp.expand(e - a * j - b) != 0 or not a.is_integer or not b.is_integer:
        raise Fail("non-linear exponent %s" % e)
    return int(a), int(b)

def shift_sim(ctx, w, S, direction):
    """Concrete simulation of one block copy with travelling context. Returns (w', c) or None."""
    if direction == 1:
        win = list(ctx) + list(w); h = len(ctx)
    else:
        win = list(w) + list(ctx); h = len(w) - 1
    st = S; c = 0
    while 0 <= h < len(win):
        key = (st, win[h])
        if key not in TM or c > 5000:
            return None
        wb, mv, ns = TM[key]
        win[h] = wb; h += mv; st = ns; c += 1
    if st != S:
        return None
    if direction == 1:
        if h != len(win) or win[len(w):] != list(ctx):
            return None
        return tuple(win[:len(w)]), c
    else:
        if h != -1 or win[:len(ctx)] != list(ctx):
            return None
        return tuple(win[len(ctx):]), c

def tape_canon(tape, h):
    toks = []
    for i, it in enumerate(tape):
        if i == h:
            toks.append(("H",))
        if it[0] == "b":
            toks.append(("r", it[1], sp.Integer(1)))
        elif it[0] == "w":
            w, n = it[1], it[2]
            if len(set(w)) == 1:
                toks.append(("r", w[0], sp.expand(len(w) * n)))
            elif not n.free_symbols:
                for _ in range(int(n)):
                    for b in w:
                        toks.append(("r", b, sp.Integer(1)))
            else:
                toks.append(("w", w, n))
    # canon with 'w' tokens kept opaque
    res = []
    for t in toks:
        if t[0] == "r" and sp.expand(t[2]) == 0:
            continue
        if t[0] == "r" and res and res[-1][0] == "r" and res[-1][1] == t[1]:
            res[-1] = ("r", t[1], sp.expand(res[-1][2] + t[2]))
        else:
            res.append(t)
    return res

def build_tape(tokens, order):
    """tokens: run tokens with exponents linear in j. Concrete part as bits, symbolic part as block.
    order[i] in {'pre','post'}: concrete cells before or after the symbolic block for symbolic run i."""
    tape = [("E",)]
    h = None; si = 0
    for t in tokens:
        if t[0] == "H":
            h = len(tape); continue
        _, b, n = t
        a, c = lin_parts(n)
        if a == 0:
            tape += [("b", b)] * c
        else:
            blk = ("w", (b,) * a, j)
            if order[si] == "pre":
                tape += [("b", b)] * c + [blk]
            else:
                tape += [blk] + [("b", b)] * c
            si += 1
    tape.append(("E",))
    return tape, h

def resolve(tape, h, st, d, log, stats):
    """Make tape[h] a concrete bit. Returns (tape, h, extra_steps)."""
    extra = sp.Integer(0)
    for _ in range(1000):
        it = tape[h]
        if it[0] == "b":
            return tape, h, extra
        if it[0] == "E":
            raise Fail("head read outside window (state %s)" % st)
        w, n = it[1], it[2]
        if not n.free_symbols:
            nn = int(n)
            tape = tape[:h] + [("b", b) for b in w] * nn + tape[h + 1:]
            if nn == 0 and d == -1:
                h -= 1
            elif nn > 0 and d == -1:
                h += len(w) * nn - 1
            continue
        a, c = lin_parts(n)
        if c >= 1:
            stats["peel"] += 1
            bits = [("b", b) for b in w]
            if d == 1:
                tape = tape[:h] + bits + [("w", w, n - 1)] + tape[h + 1:]
            else:
                tape = tape[:h] + [("w", w, n - 1)] + bits + tape[h + 1:]
                h += len(w)
            continue
        # symbolic exponent with zero constant part: shift rule needed
        cands = [(w, n)]
        if len(set(w)) == 1:
            L = len(w)
            for dd in range(1, 7):
                if dd != L and (L * a) % dd == 0 and (L * n) / dd != n:
                    cands.append(((w[0],) * dd, sp.expand(L * n / dd)))
        done = False
        for (ww, nn) in cands:
            for ul in range(0, MAXU + 1):
                if d == 1:
                    if h - ul < 0 or any(x[0] != "b" for x in tape[h - ul:h]):
                        break
                    ctx = [x[1] for x in tape[h - ul:h]]
                else:
                    if any(x[0] != "b" for x in tape[h + 1:h + 1 + ul]) or h + 1 + ul > len(tape):
                        break
                    ctx = [x[1] for x in tape[h + 1:h + 1 + ul]]
                r = shift_sim(ctx, ww, st, d)
                if r is None:
                    continue
                w2, cc = r
                stats["shift"] += 1
                log.append("  shift dir=%+d state=%s ctx=%s w=%s -> %s, %d steps/copy, n=%s"
                           % (d, st, "".join(map(str, ctx)), "".join(map(str, ww)), "".join(map(str, w2)), cc, nn))
                extra += cc * nn
                cb = [("b", x) for x in ctx]
                if d == 1:
                    tape = tape[:h - ul] + [("w", w2, nn)] + cb + tape[h + 1:]
                    h = h - ul + 1 + ul
                else:
                    tape = tape[:h] + cb + [("w", w2, nn)] + tape[h + 1 + ul:]
                    h = h - 1
                done = True
                break
            if done:
                break
        if not done:
            raise Fail("no shift rule: state %s entering %s^(%s) dir %+d; tape=%s"
                       % (st, "".join(map(str, w)), n, d, fmt(tape_canon(tape, h))))
    raise Fail("resolve loop")

LOOK = 6   # max concrete cells between head and a block for a look-ahead shift
EXT = 6    # max extension of the travelling context on the far side of the head

def ctx_shift_sim(ctx, p, w, S, direction):
    """Generalised shift with travelling context and look-ahead.
    direction +1: window = ctx + w, head at ctx[p] in state S; success iff the window run reaches
      head == p+len(w), state S, window[len(w):] == ctx, never reading outside the window.
      Then  ctx (w)^n -> (w')^n ctx  (head again at ctx[p]) for every n >= 0, by induction on n.
    direction -1: window = w + ctx, head at len(w)+p; success iff head == p, state S,
      window[:len(ctx)] == ctx.  Then (w)^n ctx -> ctx (w')^n."""
    if direction == 1:
        win = list(ctx) + list(w); h = p; tgt = p + len(w)
    else:
        win = list(w) + list(ctx); h = len(w) + p; tgt = p
    st = S; c = 0
    while True:
        if c > 0 and h == tgt and st == S:
            if direction == 1 and win[len(w):] == list(ctx):
                return tuple(win[:len(w)]), c
            if direction == -1 and win[:len(ctx)] == list(ctx):
                return tuple(win[len(ctx):]), c
        if not (0 <= h < len(win)) or c > 400:
            return None
        key = (st, win[h])
        if key not in TM:
            return None
        wb, mv, ns = TM[key]
        win[h] = wb; h += mv; st = ns; c += 1

def regroup(w, n):
    cands = [(w, n)]
    if len(set(w)) == 1:
        a, _ = lin_parts(n)
        L = len(w)
        for dd in range(1, 9):
            if dd != L and (L * a) % dd == 0:
                cands.append(((w[0],) * dd, sp.expand(L * n / dd)))
    return cands

def try_shift(tape, h, st, log, stats):
    """Look for a symbolic block within LOOK cells right or left of the head and an accelerating
    shift.  Returns (tape, h, extra_steps) or None."""
    for d in (1, -1):
        b = h
        while True:
            b += d
            if tape[b][0] != "b" or abs(b - h) > LOOK:
                break
        if tape[b][0] != "w" or abs(b - h) > LOOK:
            continue
        w, n = tape[b][1], tape[b][2]
        if not n.free_symbols:
            continue
        a, c0 = lin_parts(n)
        if c0 > 0:   # peel constant part on the near side, then retry later
            bits = [("b", x) for x in w] * c0
            blk = [("w", w, sp.expand(n - c0))]
            tape = tape[:b] + (bits + blk if d == 1 else blk + bits) + tape[b + 1:]
            if d == -1:
                h += len(w) * c0
            stats["peel"] += 1
            return tape, h, sp.Integer(0)
        for (ww, nn) in regroup(w, n):
            for ext in range(0, EXT + 1):
                if d == 1:
                    s0 = h - ext
                    if any(x[0] != "b" for x in tape[s0:b]):
                        break
                    ctx = [x[1] for x in tape[s0:b]]; p = ext
                else:
                    e0 = h + ext
                    if any(x[0] != "b" for x in tape[b + 1:e0 + 1]):
                        break
                    ctx = [x[1] for x in tape[b + 1:e0 + 1]]; p = h - (b + 1)
                r = ctx_shift_sim(ctx, p, ww, st, d)
                if r is None:
                    continue
                w2, cc = r
                stats["shift"] += 1
                log.append("  shift dir=%+d state=%s ctx=%s head@%d w=%s -> w'=%s, %d steps/copy, copies=%s"
                           % (d, st, "".join(map(str, ctx)), p, "".join(map(str, ww)),
                              "".join(map(str, w2)), cc, nn))
                cb = [("b", x) for x in ctx]
                if d == 1:
                    tape = tape[:s0] + [("w", w2, nn)] + cb + tape[b + 1:]
                    h = s0 + 1 + p
                else:
                    tape = tape[:b] + cb + [("w", w2, nn)] + tape[e0 + 1:]
                    h = b + p
                return tape, h, sp.expand(cc * nn)
    return None

def symbolic_check(inp, outp, steps_str, K, xv, order, log, maxsteps=20000):
    kv = j + K
    ti = parse_pattern(inp, kv, xv)
    to = canon(parse_pattern(outp, kv, xv))
    target = sp.expand(steps_sym(steps_str).subs(k, kv))
    tape, h = build_tape(ti, order)
    st = "A"; steps = sp.Integer(0)
    stats = {"peel": 0, "shift": 0, "trans": 0}
    tape, h, ex = resolve(tape, h, st, 1, log, stats)
    steps += ex
    for it in range(maxsteps):
        if st == "A":
            c = tape_canon(tape, h)
            if canon_eq(c, to):
                if sp.expand(steps - target) == 0:
                    return steps, stats
                raise Fail("output config reached but steps %s != stated %s" % (sp.expand(steps), target))
        r = try_shift(tape, h, st, log, stats)
        if r is not None:
            tape, h, ex = r
            steps += ex
            continue
        key = (st, tape[h][1])
        if key not in TM:
            raise Fail("halt")
        wb, mv, ns = TM[key]
        tape[h] = ("b", wb); st = ns; steps += 1; stats["trans"] += 1
        h += mv
        tape, h, ex = resolve(tape, h, st, mv, log, stats)
        steps += ex
    raise Fail("output configuration never reached within %d transitions; final %s state %s"
               % (maxsteps, fmt(tape_canon(tape, h)), st))

def nsym(s):
    return sum(1 for t in parse_pattern(s, j + 5, 0) if t[0] == "r" and t[2].free_symbols)

def prove_linear(rule, Ks=range(1, 9), verbose=True):
    """Try K = 1..8: symbolic for k >= K (both x), concrete for domain_lo <= k < K (both x)."""
    lo = int(rule["domain"].split(">=")[1])
    inp, outp, stp = rule["input"], rule["output"], rule["steps"]
    m = nsym(inp)
    lastfail = None; firstfail = None
    for K in Ks:
        if K < lo:
            continue
        for order in itertools.product(["pre", "post"], repeat=m):
            log = []
            try:
                res = {}
                for xv in (0, 1):
                    res[xv] = symbolic_check(inp, outp, stp, K, xv, order, log)
                conc = []
                for kv in range(lo, K):
                    for xv in (0, 1):
                        conc.append((kv, xv, concrete_check(inp, outp, stp, kv, xv)))
                if verbose:
                    print("  K=%d order=%s: symbolic k=j+%d, j>=0 steps=%s (x=0), %s (x=1); stats x=1 %s"
                          % (K, order, K, res[0][0], res[1][0], res[1][1]))
                    for l in sorted(set(log)):
                        print(l)
                    print("  concrete cases k<K:", conc)
                return True, "K=%d" % K
            except Fail as e:
                lastfail = "K=%d order=%s: %s" % (K, order, e)
                firstfail = firstfail or lastfail
    return False, "first attempt [%s]; last attempt [%s]" % (firstfail, lastfail)

# ---------------------------------------------------------------- induction checker
def inst(rule, param, xv):
    return (canon(parse_pattern(rule["input"], param, xv)),
            canon(parse_pattern(rule["output"], param, xv)),
            sp.expand(steps_sym(rule["steps"]).subs(k, param)))

def ctx_tokens(s):
    s = s.replace(" ", "")
    return [t for t in parse_pattern("A" + s, k, 0) if t[0] == "r"] if s else []

def nonneg_poly(e):
    p = sp.Poly(sp.expand(e), k)
    return all(c >= 0 for c in p.all_coeffs())

def prove_induction(rule, stages, proved, rules_by_id):
    """Base k=0 concretely (both x irrelevant: no x in these rules); step k -> k+1 by stages.
    stage = (rule_id or 'IH', param, x, prefix, suffix)."""
    lo = int(rule["domain"].split(">=")[1])
    assert lo == 0
    base = concrete_check(rule["input"], rule["output"], rule["steps"], 0, 0)
    print("  base k=0: %d steps OK" % base)
    cur = canon(parse_pattern(rule["input"], k + 1, 0))
    want = canon(parse_pattern(rule["output"], k + 1, 0))
    total = sp.Integer(0)
    for (rid, param, xv, pre, suf) in stages:
        param = sp.sympify(param, locals={"k": k})
        if rid == "IH":
            if sp.expand(param - k) != 0:
                raise Fail("IH used at parameter %s, only k allowed" % param)
            r = rule
        else:
            if not proved.get(rid):
                raise Fail("uses unproved rule %s" % rid)
            r = rules_by_id[rid]
            rlo = int(r["domain"].split(">=")[1])
            if not nonneg_poly(param - rlo):
                raise Fail("domain of %s violated: %s >= %d not guaranteed for k>=0" % (rid, param, rlo))
        I, O, S = inst(r, param, xv)
        P, Q = ctx_tokens(pre), ctx_tokens(suf)
        lhs = canon(P + I + Q)
        if not canon_eq(lhs, cur):
            raise Fail("stage %s(%s) input in context %s does not match current %s" % (rid, param, fmt(lhs), fmt(cur)))
        cur = canon(P + O + Q)
        total = sp.expand(total + S)
        print("  stage %s(%s) x=%d ctx[%s | %s]: -> %s  (+%s steps)" % (rid, param, xv, pre, suf, fmt(cur), S))
    if not canon_eq(cur, want):
        raise Fail("final %s != stated %s" % (fmt(cur), fmt(want)))
    tgt = sp.expand(steps_sym(rule["steps"]).subs(k, k + 1))
    if sp.expand(total - tgt) != 0:
        raise Fail("step sum %s != stated(k+1) %s" % (total, tgt))
    print("  step sum %s == stated(k+1) %s" % (total, tgt))
    return True

PROOFS = {
    "even_drain": [("even", "k+1", 0, "0^k", ""), ("IH", "k", 0, "", "111")],
    "Ddrain1": [("Dstep", "2k+1", 0, "", ""), ("IH", "k", 0, "1", "111")],
    "Ddrain3": [("Dstep", "2k+2", 0, "", ""), ("IH", "k", 0, "1", "111")],
}

def run_all(rules, proofs, label, verbose=True):
    print("=" * 20, label)
    byid = {r["id"]: r for r in rules}
    proved = {}
    for r in rules:
        rid = r["id"]
        print("rule %s: %s -> %s in %s, %s" % (rid, r["input"], r["output"], r["steps"], r["domain"]))
        try:
            if rid in proofs:
                fixed = [(a, b.replace("2k", "2*k") if isinstance(b, str) else b, c, d, e) for (a, b, c, d, e) in proofs[rid]]
                proved[rid] = prove_induction(r, fixed, proved, byid)
                print("  RESULT %s: PROVED (induction)" % rid)
            else:
                ok, info = prove_linear(r, verbose=verbose)
                proved[rid] = ok
                print("  RESULT %s: %s %s" % (rid, "PROVED" if ok else "NOT PROVED", info))
        except Fail as e:
            proved[rid] = False
            print("  RESULT %s: NOT PROVED (%s)" % (rid, e))
    return proved

