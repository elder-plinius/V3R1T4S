# 2026-10-15-r-nikhil-c6c093c2: exact optimal expected scores for yes/no-feedback card guessing, two copies of n labels, n = 11, 12, 13 (partial win p1)

## What
Only partial win p1 is confirmed: the reduced fractions P+_{2,11} = 137912544707079557/45735706696680000, P+_{2,12} = 228254911260131056513/75738330289702080000 and P+_{2,13} = 3901622163101296907981/1295524070744904000000 are certified by cert/n11.txt.gz, cert/n12.txt.gz and cert/n13.txt.gz, each verified by my independently written checker state by state over all reachable canonical states (C recomputed from (A.1), max over every label including exhausted ones, closure from the initial state) against Luo's Appendix A recursion (cert/n2.txt.gz to cert/n10.txt.gz and cert/n14.txt.gz also pass that check, which does not complete the full criterion); the full criterion is not met literally, because the code's n = 7 value 206528731/68108040 = 3.0323693... rounds to 3.0324 whereas DGS Table 3 prints 3.0323 under its stated rounding (and truncation would instead fail n = 10, 3.0185 against 3.0186), and because cert/n15.txt.gz and cert/n16.txt.gz were not verified state by state by me.

## Check it yourself
`sh verify-it-yourself/run_checks.sh` (run from this folder). Expected last line: `PASS` (about 3 minutes on a laptop;
Python 3 standard library only). It checks that `object/values.json` is the packaged object and lists reduced
fractions, then verifies certificates on every state against Luo's recursion with `verify-it-yourself/verify_cert.py`
(which recomputes the arrangement counts C from equation (A.1) and never trusts the table): the shipped n = 2..9
files and the claimed n = 11 certificate (shipped as `object/cert/n11.txt.gz.part-*`, pieces under 1 MB, reassembled
with `cat`). `FULL=1` also verifies the shipped n = 10, 12 and 13 certificates (the other two claimed objects; about
6 more minutes), `FULL=2` also recomputes P+_{2,11} from scratch with `verify-it-yourself/recompute_value.py`.
The faster C++ checker `verify-it-yourself/cg_verify.cpp` (GMP, zlib) does the same checks in seconds; see
RUN_IT_YOURSELF.md. The certificates for n = 14..16 are too large for git; their names, sizes, state counts and
sha256 are listed below, and the archive URL is given in RUN_IT_YOURSELF.md; placed into `object/cert/` they are
verified by the same script.

Values (reduced fractions, from `object/values.json`):

| n | P+_{2,n} | decimal |
|---|---|---|
| 2 | 17/6 | 2.833333333333 |
| 3 | 271/90 | 3.011111111111 |
| 4 | 1279/420 | 3.045238095238 |
| 5 | 57583/18900 | 3.046719576719 |
| 6 | 1136743/374220 | 3.037632943188 |
| 7 | 206528731/68108040 | 3.032369320861 |
| 8 | 61829276953/20432412000 | 3.026039067389 |
| 9 | 6298009733989/2084106024000 | 3.021923866378 |
| 10 | 170757866939041/56568592080000 | 3.018598495390 |
| 11 | 137912544707079557/45735706696680000 | 3.015423936088 |
| 12 | 228254911260131056513/75738330289702080000 | 3.013730437244 |
| 13 | 3901622163101296907981/1295524070744904000000 | 3.011616882469 |
| 14 | 28008675189200821587458897/9304453876089900528000000 | 3.010243864089 |
| 15 | 811893265752470943966781067/269829162406607115312000000 | 3.008915932255 |
| 16 | 287519620950287971428538054033/95596617538340806567680000000 | 3.007633830087 |

Certificates not shipped in git (sha256 of the gzip file as archived):

| n | file (archived, not in git) | size | states | sha256 |
|---|---|---|---|---|
| n=14 | cert/n14.txt.gz | 49,846,795 bytes | 4,784,071 | 4c39135ecfefe094c3e6660ca18946119f61d4ca32ff009bf1de7c6c29e45128 |
| n=15 | cert/n15.txt.gz | 106,935,269 bytes | 9,548,576 | d6e2d10e3ffafa342334ae5584370c9f83436f0287fc01770d4e03c19cd58f46 |
| n=16 | cert/n16.txt.gz | 223,641,952 bytes | 18,623,134 | 5d8c64a0990be6e99071f34b7e56fbe36c927e7e2fa97f92e2e2195c72f92dfa |

## Compared to
| table | cell | table value | our value | URL | fetched (UTC) |
|---|---|---|---|---|---|
| arXiv search "card guessing feedback" (the bank's status source) | exact P+_{2,n}, n = 11..16 | none published | exact fractions above | https://arxiv.org/search/?query=card+guessing+feedback&searchtype=all&abstracts=show&order=-announced_date_first&size=25 | 2026-10-15T13:16:53Z |
| Diaconis-Graham-Spiro, Tables 2-3 (arXiv:2012.04019), m = 2, four decimals | n = 2..10 (calibration) | 2.8333, 3.0111, 3.0452, 3.0467, 3.0376, 3.0323, 3.0260, 3.0219, 3.0186 | 8 of 9 entries equal the exact value rounded to four decimals; n = 7 is exactly 3.0323693..., whose rounding is 3.0324 and whose truncation is the printed 3.0323 (n = 10, 3.0185985..., is printed as its rounding 3.0186); all nine are within 0.0001 | https://arxiv.org/pdf/2012.04019 | 2026-10-15T13:18:46Z |
| Diaconis-Graham, Ann. Statist. 9 (1981), Section 3 (Gatto 1978), two decimals | decks (3,3), (4,4), (5,5) | 4.26, 5.47, 6.63 | 4.2554, 5.4685, 6.6288 (same solver, m = 3, 4, 5) | https://projecteuclid.org/euclid.aos/1176345329 | 2026-10-15T13:36:19Z (scan) |

## Not claimed
- The full success criterion (n = 11..16 plus calibration): the CRITERION skeptic judged it not met literally, because
  its calibration clause ("reproduce Table 3 of Diaconis-Graham-Spiro for n = 2..10 to four decimals") fails at n = 7
  under the table's stated rounding (exact 3.0323693... rounds to 3.0324; the table prints 3.0323, its truncation), and
  no single four-decimal convention reproduces all nine printed entries (truncation would fail n = 10). Eight of nine
  entries match under rounding, all nine are within 0.0001, and the n = 7 value is confirmed by three independent
  checkers; the printed entry is most plausibly a truncation or misprint, but that is for the table's authors to say.
- The values for n = 14, 15, 16 (and n = 17) in object/values.json: computed by the same solver and verified on every
  state by the authors' checkers, but outside the confirmed scope (the panel's CRITERION skeptic verified n = 2..14
  state by state and n = 15, 16 structurally); they are shipped as data, not claimed.
- Nothing about the limit of P+_{2,n} (Luo's Question 5.1) or any n >= 17.
- Nothing about P- (the minimising, misere problem) or about complete-feedback or no-feedback guessing.
- No claim that the certificate's reachable-state tables are minimal, and no claim about optimal strategies beyond
  the values (the tables determine optimal actions, but none is asserted here).
- The persistence conjecture of Diaconis-Graham (1981) was found to hold on every reachable state for m = 2, n <= 17
  in our tables; that observation is reported in the run notes, not claimed here.
- Diaconis-Graham-Spiro's Table 1 prints 6.65 for the (5,5,5,5,5) deck; the 1981 source and our value give 6.63.
  Reported, not claimed.

## Credits
- Congyi Luo, "Extremal expectations in card guessing with partial feedback: proofs of two conjectures of
  Diaconis-Graham-Spiro", arXiv:2609.25062 (2026): the sufficient state, equation (A.1) and the recursion we implement,
  and Question 5.1. https://arxiv.org/abs/2609.25062
- Persi Diaconis, Ron Graham, Sam Spiro, "Guessing about Guessing: Practical Strategies for Card Guessing with
  Feedback", Amer. Math. Monthly 129 (2022), arXiv:2012.04019: Tables 2-3 (the published four-decimal values n = 2..10).
  https://arxiv.org/abs/2012.04019
- Persi Diaconis, Ron Graham, Xiaoyu He, Sam Spiro, "Card Guessing with Partial Feedback", Combin. Probab. Comput. 31
  (2022), arXiv:2010.05059: the asymptotics and the persistence-conjecture summary. https://arxiv.org/abs/2010.05059
- Persi Diaconis, Ronald Graham, "The analysis of sequential experiments with feedback to subjects", Ann. Statist. 9
  (1981) 3-23, and Mary Ann Gatto (1978): the recurrence and the exact values 4.26, 5.47, 6.63 we calibrate against.
  https://projecteuclid.org/euclid.aos/1176345329
- F. R. K. Chung, P. Diaconis, R. L. Graham, C. L. Mallows (1981) and P. Diaconis, R. Graham, S. Holmes (2001): the
  permanent formulas behind (A.1) (cited through Luo and Diaconis-Graham-He-Spiro).
- A second, independently written solver (a different language model, run on the same machine by the operator)
  obtained identical values for n = 2..16; it is credited as an independent cross-check, not as a source.
