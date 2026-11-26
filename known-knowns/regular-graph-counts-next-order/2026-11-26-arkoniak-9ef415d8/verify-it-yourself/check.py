#!/usr/bin/env python3
"""Standalone check of C_4(51), the connected quartic count at order 51 (beyond Cheng and Xu, arXiv 2609.31407, Tables 4 and 5, N<=50),
with the table U_4(N), C_4(N) for N = 0..51 it is computed from.

Definition. U(N) = number of unlabeled 4-regular simple graphs on N vertices = (1/N!) sum_{g in S_N} Fix(g) (Burnside),
Fix(g) = number of labeled 4-regular graphs on {1..N} fixed by g; it depends only on the cycle type lambda of g:
U(N) = sum_lambda F(lambda)/z_lambda, z_lambda = prod_k k^{c_k} c_k!. Connected counts C(N) follow by the inverse Euler
transform: 1 + sum_n U(n) x^n = prod_n (1 - x^n)^(-C(n)). OEIS: A033301 (U), A006820 (C), indexed by n = vertices.

Checks: (1) object/F_N29.txt (method D) has one value per cycle type of 29 (all 4565 partitions) and sum F/z is the
integer U(29) of object/U4_C4.txt; (2) the C column of object/U4_C4.txt is the inverse Euler transform of its U column;
(3) U(0..28) == published A033301, C(1..28) == published A006820; (4) U(29..50) == Cheng-Xu Table 4 and
C(29..50) == Table 5 (values as extracted in the-record-we-beat/); (5) method A (how-we-built-it/methodA: C histogram
recurrence, CRT), built and run here to N=36 (about 2 min on one core), gives the same U(5..36). Last line PASS or FAIL."""
import sys, os, subprocess, tempfile
sys.dont_write_bytecode = True
from fractions import Fraction
from math import factorial
from collections import Counter
here = os.path.dirname(os.path.abspath(__file__)); pkg = os.path.dirname(here)
# published values: OEIS b-files b033301.txt, b006820.txt (n=0..28) and Cheng-Xu Tables 4 (CX4) and 5 (CX5), n=29..50
A033301 = {0: 1, 1: 0, 2: 0, 3: 0, 4: 0, 5: 1, 6: 1, 7: 2, 8: 6, 9: 16, 10: 60, 11: 266, 12: 1547, 13: 10786, 14: 88193, 15: 805579, 16: 8037796, 17: 86223660, 18: 985883873, 19: 11946592242, 20: 152808993767, 21: 2056701139136, 22: 29051369533596, 23: 429669276147047, 24: 6640178380127244, 25: 107026751932268789, 26: 1796103830404560857, 27: 31334029441145918974, 28: 567437704731717802783}
A006820 = {0: 1, 1: 0, 2: 0, 3: 0, 4: 0, 5: 1, 6: 1, 7: 2, 8: 6, 9: 16, 10: 59, 11: 265, 12: 1544, 13: 10778, 14: 88168, 15: 805491, 16: 8037418, 17: 86221634, 18: 985870522, 19: 11946487647, 20: 152808063181, 21: 2056692014474, 22: 29051272833609, 23: 429668180677439, 24: 6640165204855036, 25: 107026584471569605, 26: 1796101588825595008, 27: 31333997930603283531, 28: 567437240683788292989}
CX4 = {29: 10652577590214241002618, 30: 207054244547337985329720, 31: 4161993706714940326838786, 32: 86424005407555318218067697, 33: 1851998440392256616901456520, 34: 40917079037806933457347198438, 35: 931183927432486423640202376814, 36: 21810450084104345091773820858196, 37: 525344362944702962413733395520252, 38: 13003032308773638146164487141818952, 39: 330487084031595634132232172180021294, 40: 8619415114072964191751466252612719377, 41: 230533227247675454285548999068702309794, 42: 6319087592497085783571337132123210802321, 43: 177413127187497235740886087991800080245168, 44: 5098998905389251773034803769266361673511731, 45: 149940921587171855739584362970984343156657193, 46: 4508894979370373105831885412360496862130843299, 47: 138587154167033251155034541552679549848762484979, 48: 4351870731024217447549685703640756912833949879605, 49: 139551606359121154554275644335312475951018945402502, 50: 4567863967927930120629311714346947864974124915610296}
CX5 = {29: 10652570446223068758328, 30: 207054129798202478947780, 31: 4161991787056364392993657, 32: 86423972013842831141067779, 33: 1851997837239534197240070489, 34: 40917067742027646230636613788, 35: 931183708364518646087601058142, 36: 21810445689689214773057789501098, 37: 525344271868938707705400377687514, 38: 13003030360567200772187592732217381, 39: 330487041060514755173477290891267539, 40: 8619414137666184155650741761970634546, 41: 230533204411383026272756189104337347077, 42: 6319087043198021512104740092530777402157, 43: 177413113609115042486441572202257674562253, 44: 5098998560699564475515004308783887431914087, 45: 149940912607692268107701695024603153774329415, 46: 4508894739468701917064672399081911536531357642, 47: 138587147597943684444165814756297043282778275999, 48: 4351870546772975644217239817541796928811187365690, 49: 139551601068525711134953857116015783170154234904858, 50: 4567863812490955416720841969219753968607349955976192}
def parts(n, mx=None):
    mx = n if mx is None else mx
    if n == 0: yield (); return
    for k in range(min(n, mx), 0, -1):
        for r in parts(n - k, k): yield (k,) + r
def z(lam):
    r = 1
    for k, c in Counter(lam).items(): r *= k ** c * factorial(c)
    return r
def mu(n):
    r, p = 1, 2
    while p * p <= n:
        if n % p == 0:
            n //= p
            if n % p == 0: return 0
            r = -r
        p += 1
    return -r if n > 1 else r
ok = True
U, C = {}, {}
for l in open(os.path.join(pkg, 'object', 'U4_C4.txt')):
    if l.startswith('#') or not l.strip(): continue
    n, u, c = map(int, l.split()); U[n], C[n] = u, c
ok &= sorted(U) == list(range(52))
F = {}
for ln in open(os.path.join(pkg, 'object', 'F_N29.txt')):
    p, v = ln.strip().split(';'); lam = tuple(map(int, p.split()))
    if lam in F: print('duplicate type', p); ok = False
    F[lam] = int(v)
allp = set(parts(29)); S = sum(Fraction(v, z(lam)) for lam, v in F.items())
r1 = set(F) == allp and S.denominator == 1 and S == U[29]
print(f'(1) types {len(F)} of {len(allp)} partitions of 29, sum F/z integer {S.denominator == 1}, == U(29): {S == U[29]}'); ok &= r1
a = [U[n] for n in range(52)]; cc = [0] * 52
for n in range(1, 52): cc[n] = n * a[n] - sum(cc[k] * a[n - k] for k in range(1, n))
Ce = {n: sum(mu(n // d) * cc[d] for d in range(1, n + 1) if n % d == 0) // n for n in range(1, 52)}
r2 = all(Ce[n] == C[n] for n in range(1, 52)); print(f'(2) C == inverse Euler of U, N=1..51: {r2}'); ok &= r2
r3 = all(U[n] == A033301[n] for n in range(29)) and all(C[n] == A006820[n] for n in range(1, 29))
print(f'(3) U(0..28) == A033301 and C(1..28) == A006820: {r3}'); ok &= r3
bu = [n for n in range(29, 51) if U[n] != CX4[n]]; bc = [n for n in range(29, 51) if C[n] != CX5[n]]
print(f'(4) U(29..50) vs Table 4 mismatches {bu}; C(29..50) vs Table 5 mismatches {bc}'); ok &= not bu and not bc
mA = os.path.join(pkg, 'how-we-built-it', 'methodA')
with tempfile.TemporaryDirectory() as td:
    subprocess.run(['gcc', '-O2', '-o', os.path.join(td, 'cubic'), os.path.join(mA, 'cubic.c')], check=True)
    out = subprocess.run([sys.executable, '-I', os.path.join(mA, 'driver.py'), '--bin', os.path.join(td, 'cubic'), '--deg', '4',
                          '--nmax', '36', '--nprimes', '8', '--pivot', 'max', '--dumpU'], capture_output=True, text=True).stdout
UA = {}
for l in out.splitlines():
    f = l.split()
    if len(f) >= 2 and f[0].isdigit() and f[1].isdigit(): UA[int(f[0])] = int(f[1])
bad = [n for n in range(5, 37) if UA.get(n) != U[n]]
print(f'(5) method A rerun N=5..36: {len(UA)} values, mismatches with U {bad}'); ok &= not bad
UA51 = None
for l in open(os.path.join(mA, 'A_terms_d4.txt')):
    f = l.split()
    if len(f) >= 2 and f[0] == '51': UA51 = int(f[1])
r6 = UA51 == U[51]
print(f'(6) U(51) == method A U_A(51) (how-we-built-it/methodA/A_terms_d4.txt): {r6}; C_4(51) = {C[51]}'); ok &= r6
print('PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
