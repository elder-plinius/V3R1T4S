# REPRODUCE skeptic report

context: subagent (fresh, sonnet)

Checker definition (quoted from REPRODUCE.md): "U(N) = number of unlabeled 3-regular simple graphs on N vertices = (1/N!) sum_{g in S_N} Fix(g) ... U(N) = sum_lambda F(lambda)/z_lambda with z_lambda = prod_k k^{c_k} c_k! ... 1 + sum U(N) x^N = prod_N (1 - x^N)^(-C(N))."
My scripts (own code, outside claim/): z_lambda, partition generator, Burnside sum with exact Fractions, inverse Euler via c_n = n U_n - sum c_k U_{n-k}, brute-force enumeration.

Checks and real outputs:
1. Coverage/agreement (own parsing of results/D_N42_lane0.txt, results/D_N42_lane1.txt, methodA/py42.csv; own generator of partitions of 42):
   partitions 53174 (each file covers exactly this set, no duplicates, none missing); D==A all True (and column F_D==F_A, status ok, in every row).
2. Exactness: max F = F(1^42) = 347916205027637227573719084034659575364573966723320528976776801396062500 (72 digits) < 2^520, so residues mod 2^521-1 are exact. Confirmed True.
3. Burnside: D U(42) 264928974203634896907, integer (denominator 1); A U(42) 264928974203634896907, integer. Equal.
4. Inverse Euler from U(2..40) (results/Dbfile_lane*.txt) and my U(42): U(N) == data/b_A005638.txt for all 21 entries (True); C(N)==data/b002851.txt for n=1..20 (True); odd C zero True; C(42) 264592224929900091377 == claimed True. U(N) from methodA/A_terms_d3.txt agrees with mine for even N 4..42 (True; file runs to N=66).
5. Brute force (labeled cubic graphs enumerated directly, fixed counts per cycle type) for N=4,6,8 (1, 70, 19355 graphs; 38 types): brute == methodA/engine.F_A == methodD/Dsym.F_Dsym for all, bad 0.
6. Spot recomputation of N=42 types by both methods (random 6 + 4 with >=12 long cycles + several specials such as (14,14,14), (42,), (7^6), 3^14): all equal saved values, "bad 0 n 13". Slowest case ~1.7 s.
7. results/s42_*.txt and h42_*.txt: 359 rows, all status ok. Rerunning methodA/dump42.py: output byte-identical to methodA/py42.csv (deterministic).
8. methodD/D.py and Dsym.py import only the standard library and D, not engine; methodA/engine.py imports only the standard library. Structurally independent code.

Could not verify:
- Did not rerun method D on all 53174 types (about 1.1 h on 2 cores); relied on saved D values plus 13 spot recomputations of my own plus the saved 359-row recomputation file. Since saved D equals independently regenerated A for every type, the risk is low but this is not a full independent rerun.
- Brute force only to N=8 (N=10+ too slow in pure Python); larger N rests on agreement with the published b-files (N<=40) and the two methods.
- Did not audit the C port (methodA/cubic.c) beyond agreement of its U values with mine for N<=42.
- Independence of the two methods is judged from imports/structure, not a full code audit of the math.

pass: true
