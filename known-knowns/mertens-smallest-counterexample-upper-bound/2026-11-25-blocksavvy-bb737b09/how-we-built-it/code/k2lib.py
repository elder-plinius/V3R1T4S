"""Standard-library ball sums for the K2 package (Python Decimal, exact addition, outward-safe radii)."""
from decimal import Decimal, Context, Inexact
CTX = Context(prec=2000, traps=[Inexact])
def parse_ball(s):
    s = s.strip()
    if s.startswith("["):
        body = s[1:-1].strip()
        if body.startswith("+/-"): return Decimal(0), Decimal(body[3:].strip())
        m, r = body.split("+/-"); return Decimal(m.strip()), Decimal(r.strip())
    return Decimal(s), Decimal(0)
def ball_sum(S_list, term):
    """K2 = 2 * (sum of chunk sums S - excluded term), as (mid, rad) decimal strings; exact (Inexact is trapped)."""
    m, r = Decimal(0), Decimal(0)
    for s in S_list:
        a, b = parse_ball(s); m = CTX.add(m, a); r = CTX.add(r, b)
    a, b = parse_ball(term); m = CTX.subtract(m, a); r = CTX.add(r, b)
    return str(CTX.multiply(m, 2)), str(CTX.multiply(r, 2))
