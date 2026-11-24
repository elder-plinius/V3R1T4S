# Float (mpmath) replay of Cully-Hugill's inequality (21) [JNT 2023] = thesis (4.11), m=3, sigma1=0.6,
# alpha=1/3+1e-10, C1=17.418, C2=5.272.  Work in X=log x (x astronomically large): every term is computed in log form.
from mpmath import mp, mpf, log, exp, findroot, pi
mp.dps = 40
def lhs_terms(X, c, K, a=mpf(1)/3+mpf('1e-10'), s1=mpf('0.6'), C1=mpf('17.418'), C2=mpf('5.272')):
    LT = a*X                                     # log T
    nu = 1/(c*LT**(mpf(2)/3)*log(LT)**(mpf(1)/3))  # nu2(T), Ford form
    logW = X - mpf(8)/3*LT - 2*log(LT)           # W = x T^{-8/3} log^{-2} T
    t1 = exp(log(a) + 2*log(X) - log(pi) - (1-a-s1)*X)
    t2 = 2*C1*a**3*X**4*(exp(-nu*logW) - exp((s1-1)*logW))/logW
    t3 = 2*C2*a**2*X**2*exp(-nu*X)
    F = t1+t2+t3
    # K*G/(x^a h), h=3x^{2/3}; G ~ 2 x X log X (relative corrections are < x^{-1/3})
    tk = K*2*X*log(X)*exp((mpf(1)/3-a)*X)/3
    return F, tk
def g(t, c, K):
    F, tk = lhs_terms(exp(t), c, K); return log(F+tk)   # =0 at threshold (E/h negligible, ~x^{-1/6})
for label, c, K in [("paper JNT2023 (Ford c=57.54, K=3.4747)",57.54,3.4747),
                    ("paper c=57.54, K=2.4798",57.54,2.4798),
                    ("thesis guess c=51.82, K=2.4798",51.82,2.4798),
                    ("MTY c=55.241, K=3.4747",55.241,3.4747)]:
    t = findroot(lambda t: g(t,mpf(c),mpf(K)), mpf(33.8))
    print(f"{label}: loglog x0 = {mp.nstr(t,8)}  loglog n0 = {mp.nstr(t-log(3),8)}")
