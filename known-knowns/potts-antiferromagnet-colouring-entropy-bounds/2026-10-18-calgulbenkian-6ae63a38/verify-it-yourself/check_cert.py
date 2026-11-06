"""Parse a Collatz-Wielandt certificate file and compute the bound it implies.
usage: check_cert.py CERT.bin M CLAIMED_20_DECIMALS PUBLISHED_BOUND
File format (as documented in the object's BOUND.md): uint32 n, then n unsigned 256-bit
little-endian integers v (positive test vector), then n unsigned 256-bit integers y
(the claimed product of the transfer matrix with v). Standard library only."""
import sys, struct
from fractions import Fraction
from decimal import Decimal, getcontext
getcontext().prec = 80
path, M, claimed, published = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
raw = open(path, 'rb').read()
n = struct.unpack('<I', raw[:4])[0]
ok = True
def report(name, cond, extra=''):
    global ok
    print('%s: %s %s' % ('PASS' if cond else 'FAIL', name, extra)); ok = ok and cond
report('file length = 4 + 64 n', len(raw) == 4 + 64 * n, '(n=%d, bytes=%d)' % (n, len(raw)))
if len(raw) != 4 + 64 * n: print('FAIL'); sys.exit(1)
def u256(off): return int.from_bytes(raw[off:off + 32], 'little')
v = [u256(4 + 32 * i) for i in range(n)]
y = [u256(4 + 32 * n + 32 * i) for i in range(n)]
report('every v entry is positive (strictly)', all(a > 0 for a in v), '(min v bit length %d, max %d)' % (min(a.bit_length() for a in v), max(a.bit_length() for a in v)))
report('every y entry is positive', all(a > 0 for a in y))
lo = min(range(n), key=lambda i: Fraction(y[i], v[i]))
hi = max(range(n), key=lambda i: Fraction(y[i], v[i]))
rlo, rhi = Fraction(y[lo], v[lo]), Fraction(y[hi], v[hi])
D = lambda f: Decimal(f.numerator) / Decimal(f.denominator)
print('min ratio y/v = %s (index %d)' % (D(rlo), lo))
print('max ratio y/v = %s (index %d)' % (D(rhi), hi))
print('relative spread (max-min)/min = %s' % ((D(rhi) - D(rlo)) / D(rlo)))
bound = (D(rhi).ln() / M).exp()
blo = (D(rlo).ln() / M).exp()
print('C_hi^(1/%d) = %s' % (M, bound))
print('C_lo^(1/%d) = %s' % (M, blo))
report('claimed 20-decimal value agrees with the computed bound to within 1e-20', abs(bound - Decimal(claimed)) < Decimal('1e-20'), '(claimed %s)' % claimed)
gain = Decimal(published) - bound
print('published bound %s minus computed bound = %s' % (published, gain))
report('computed bound is below the published bound by at least 1e-9', gain >= Decimal('1e-9'))
# Package addition: exact integer check that the stated decimal is a rigorous upper bound and is the upward rounding.
cl = Fraction(claimed)
ulp = Fraction(1, 10 ** len(claimed.split('.')[1]))
report('stated value is a rigorous upper bound: stated^%d >= C_hi, exact integers' % M, cl ** M * rhi.denominator >= rhi.numerator)
report('stated value is the upward rounding at %d decimals: (stated - 1 ulp)^%d < C_hi' % (len(claimed.split('.')[1]), M), (cl - ulp) ** M * rhi.denominator < rhi.numerator)
if ok: print('CERT PARSE AND BOUND OK')
else: print('CERT CHECK FAILED'); sys.exit(1)
