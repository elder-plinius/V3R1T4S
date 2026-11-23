# REPRODUCE skeptic verdict

Own checker written from the definition in REPRODUCE.md ("U(N) = sum_lambda F(lambda)/z_lambda, z_lambda = prod_k k^{c_k} c_k!";
"1 + sum_n U(n) x^n = prod_n (1 - x^n)^(-C(n))"), in a scratch dir outside claim/, before reading any author code.
It uses Fractions and `python3 -I`.

Checked for every N = 7..25:
- Enumerated all partitions of N (15, 22, ..., 1575, 1958 for N=25). Took the valid (non-ERR, non-TIMEOUT, F>=0) F_D row of each
  type from results/Dd6_N{N}_lane{0,1}.txt. Every partition is present, with 0 missing and 0 extra types.
  Duplicate valid rows would have asserted, and none did. The only non-valid rows are 2 ERR rows in N=25 (retried later in the same files).
- sum F/z is an exact integer for all N (denominator 1).
- U(N) equals column 2 of methodA/A_terms_d6.txt for all N=7..25 (0 mismatches).
- My own inverse Euler transform (U(0)=1, U(1..6)=0) reproduces every term of data/b006822.txt (n=1..24) and U matches
  data/b165627.txt (n=0..24). "bad 0".
- Output: C(25)= 1058090189356372623457538781723 and U(25)= 1058090189356373578845816711343, both matching the claim.

REPRODUCE.md checks:
1. dsumcheck: `N=25 types=1958 U_D=1058090189356373578845816711343 U_A=1058090189356373578845816711343 AGREE`
2. allterms: `all-graphs b-file b165627.txt: checked=25 MISMATCH 0`, `connected b-file b006822.txt: checked=24 (n=1..24) MISMATCH 0`,
   `beyond b-file: n=25 ... C_D=1058090189356372623457538781723`
3. Scratch copy, gcc build of svdp.c, F_D((5,2^10)) printed 5370946284032597450 twice (pure Python and C short part).
   The saved row in results/Dd6_N25_lane*.txt gives the same value.
4. methodA/A_terms_d6.txt line: `25 1058090189356373578845816711343 1058090189356372623457538781723`

First-principles sanity: a 6-regular graph on N has a complement of degree N-7. N=7 gives K7, so U=1. N=8 gives the complement of a
perfect matching, which is unique, so U=1. N=9 gives 2-regular graphs on 9 vertices (C9, C6+C3, C5+C4, 3C3), so U=4. All three match the
computed and b-file values 1, 1, 4. N=10 gives 21, the known count of cubic graphs on 10 vertices (including disconnected ones), and it matches.

Caveats (not failures of reproduction):
- data/b006822.txt and data/b165627.txt have the header "b-file synthesized from sequence entry". They are built from the
  OEIS entry text and are not the raw downloaded b-files. Agreement with them is therefore only as good as the entry data.
  The data/*.fetch_utc files were not examined.
- Both methods were shown to agree only on U(25). The per-type F_A column is -1 for the 'Donly' rows, so the agreement is at the level of sums.
  I did not independently audit the independence of method A.
- Novelty (that A006822(25) is absent from the published table) was not my task.

Deterministic across reruns of my checker and the author's checks. The claimed value is confirmed from the saved files.

context: subagent (fresh)
pass: true
