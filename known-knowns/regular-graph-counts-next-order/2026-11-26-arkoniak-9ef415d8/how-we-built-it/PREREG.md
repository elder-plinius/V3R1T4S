# PREREG, regular-graph-counts-next-order (run 2026-11-14-0141)

criterion (verbatim, bank): "Success means a new exact term of A002851, A006821,
A006822 or A014377 at the first order beyond the live b-file ... computed by two
independent methods or implementations that agree exactly ... The same code must
reproduce every published term of that sequence and the disconnected version ... via
the inverse Euler transform."

statistic: exact integers. F_d(lambda) per cycle type; U_d(N)=sum_lambda F_d/z_lambda;
connected C_d via inverse Euler transform (Cheng-Xu Eq 6.1-6.4).
checker: deterministic. (a) C_d reproduces every b-file term (exit 3 on mismatch);
(b) identity term = labeled A002829; (c) Burnside sum divisible by N!; (d) Euler
divisions exact; (e) method A == method B per type (feasible) == brute oracle (N<=8).
thresholds: 0 mismatches on all of (a)-(e). A new term is reported only after the
three-skeptic panel and a scalable independent second method agree at that order.
null_test: not needed because the outputs are exact integers checked by a deterministic
checker and re-encoding against published b-files, not a score on data.
