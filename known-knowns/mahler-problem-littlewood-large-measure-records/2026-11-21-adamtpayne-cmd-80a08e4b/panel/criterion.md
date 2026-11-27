# CRITERION skeptic report: Littlewood large-Mahler-measure claim (d = 32, 36, 40)

context: subagent (fresh context)

Files reviewed: CLAIM.md, REPRODUCE.md, object/d32.txt, object/d36.txt, object/d40.txt, code/certify.py, code/search.py, result/certify_outputs.txt, data/LargeSkewSymmLittlewood.txt, data/LargeLittlewood.txt, data/SOURCE.txt.
My own scripts and the re-downloaded database are in scratch/ (scratch/verify.py, scratch/edge.py, scratch/db/).

## Criterion (i), read literally
To pass, a Littlewood polynomial f of even degree d with 32 <= d <= 60 needs a certified M(f) that is strictly greater, by more than 1e-9, than three things:
(a) the max for d in LargeSkewSymmLittlewood.txt, re-downloaded at verification time;
(b) any value for d in other files of the database;
(c) any value for d in newer literature.
The certificate must be Arb/acb_poly root isolation, or two independent methods agreeing to 20 digits.
Route (ii) does not apply. M/sqrt(d+1) is 0.96399, 0.96451 and 0.96115, all below 0.98636599. The claim does not invoke (ii).

## 1. Object, degree, convention
- Lengths are 33, 37 and 41 characters, all from {+,-}, so the degrees are exactly 32, 36 and 40. These are even and within 32..60. The leading coefficients are -1, +1 and -1; |lead| = 1 is handled.
- Convention (x^0 first): I computed M for all 8 members of each polynomial's symmetry class {±f(x), ±f(-x), and the reversals of each}. In each class all 8 agree to 25 digits, so the string convention cannot change the result. The database's own convention is also x^0 first (LargeLittlewood.txt says x^d and x^(d-1) are +1, and its strings end in "++"). Either way, reversal does not affect M.

## 2. Certification
- I read code/certify.py in full.
  - Method 1 is `fmpz_poly.complex_roots()`, followed by a ball product of max(1,|r|).
    - `m > 1` and `m < 1` are arb comparisons, so each is true only if the whole ball lies on that side.
    - A ball that straddles 1 is replaced by `arb(1).union(mid+rad)`, which contains the true max(1,|r|). This is rigorous.
    - Multiplicities are applied.
  - Loop: it stops when the radius is below 1e-25, or unconditionally once prec > 4000. So it always terminates. A forced exit at 4000 bits would still give a rigorous but wide ball, and the margin test uses the ball's lower bound, so that exit would not produce a false pass.
  - Method 2 is `mpmath.polyroots` at 60 digits.
  - The margin test is `(mid - rad) - arb(table) > 1e-9`, evaluated in arb. This is rigorous.
- I ran it myself (python-flint 0.9.0, mpmath 1.4.1) using the command in REPRODUCE.md. The output is byte-identical to result/certify_outputs.txt.
- Independent checks (scratch/verify.py):
  - My own Arb enclosure at 128 to 1024 bits gives
    - 5.5376934291888081387630315191949115 ± 3e-36
    - 5.8668608513197626971666739720398698 ± 5e-35
    - 6.1543558912762003590853975109900012 ± 7e-36
  - mpmath polyroots at 80 digits agrees to all printed (35) digits.
  - A third method that uses no root-finding (Jensen's formula via mpmath quadrature at 30 digits) agrees to 25 digits.
  - The claimed balls contain these values.
- Unit-circle and cyclotomic risk is absent in fact:
  - Each polynomial is irreducible over Z (fmpz_poly.factor gives a single factor of full degree), is not cyclotomic, and is squarefree.
  - complex_roots returns 32, 36 and 40 simple roots.
  - The nearest |root| is 0.0367, 0.0351 and 0.0318 away from 1.
  - No ball straddles 1.
- I also stress-tested the straddle branch (scratch/edge.py). The test covered 40 Littlewood polynomials of degree 10 to 40 that have cyclotomic factors, including 1+x+...+x^32. certify.py's ball matched the exact measure (from factorization, dropping cyclotomic factors) every time. It finished in under 0.02 s each, with radius at most 2e-58.

## 3. Table comparison
- I parsed data/LargeSkewSymmLittlewood.txt myself: 650 data rows.
  - Every row has length d+1 and satisfies the skew-symmetry condition.
  - There are 25 entries each for d = 32, 36 and 40.
  - The maxima are 5.456083591785, 5.823385551581 and 6.153645888590, matching CLAIM.md.
- Margins use the certified lower bound minus (table value + 5e-13), which allows for the table's 12-decimal rounding:
  - d=32: 0.0816098374
  - d=36: 0.0434752997
  - d=40: 0.000710002686
  - All are > 1e-9, certified in arb.
- Re-download: I ran git clone into scratch/db. The repository is at the same commit, 7e3798516710370a758e16eb5de6bccbee98bb6a (2026-07-18), and the sha256 of both files matches data/SOURCE.txt. So the copy in data/ is the live table as of 2026-11-21.
- Other database files:
  - data/LargeLittlewood.txt has no rows for d > 30 (its max degree is 30).
  - The live repository has more files than data/ holds. I checked all of them: Littlewood_Top40, Littlewood_All72, BestMeasures, BestByDegree_200, BestByHeight, BestByRootCount_200, AllSmallMeasures_200, SalemList, SmallBivariate and SummaryReport_200. They list only small measures; the largest measure-like value is 1.666 in Littlewood_All72, and the only larger numbers are DOI fragments.
  - So no database file has a value at d = 32, 36 or 40 that is at or above the claimed values.

## 4. Packaging, subsumption, skew-symmetry
- These are three independent results at three different degrees. Criterion (i) is per polynomial, so each should be its own package or table cell, not one combined claim. None subsumes another, since the degrees differ.
- None is skew-symmetric. I tested f(x) = ±x^d f(-1/x) on the object and on all 8 members of its symmetry class. This is consistent with beating the skew-symmetric table.
- None equals a table entry up to the 8 symmetries. The minimum Hamming distance to any symmetry image of any listed entry at the same degree is 11 (d=32), 10 (d=36) and 12 (d=40). So none is a sign flip or reversal of a published object, and none is a trivial edit of one.

## 5. Things wider than the evidence
- Clause (c), "newer literature", is not checked here; it is the NOVELTY skeptic's job. It matters most here because the compared table is restricted to skew-symmetric polynomials. Beating it with non-skew polynomials does not on its own show that these are the largest known Littlewood measures at d = 32, 36 or 40. Non-skew constructions in the literature, for example the Turyn-type polynomials in arXiv:2405.08281, could exceed them. The d=40 margin (7.1e-4) is the most exposed.
- The task brief calls the table an "exhaustive skew-symmetric maximum". The file header only says "up to 25 of the largest", and CLAIM.md does not claim exhaustiveness. I did not verify exhaustiveness, and the result does not depend on it.
- The search-calibration statements in CLAIM.md (code/search.py recovering the d = 26, 28, 30 maxima) are not needed for the criterion, and I did not verify them.
- certify.py's "agree to 20 digits" check compares the Arb midpoint with mpmath only. That is acceptable here because Arb isolation alone is a sufficient certificate.

confirmed_scope: The ±1-coefficient polynomials in object/d32.txt, object/d36.txt and object/d40.txt (degrees 32, 36, 40; each irreducible and not skew-symmetric) have Arb-certified Mahler measures 5.53769342918880813876…, 5.86686085131976269717… and 6.15435589127620035909…, whose certified lower bounds exceed the maximum listed for that degree in LargeSkewSymmLittlewood.txt (database commit 7e3798516710370a758e16eb5de6bccbee98bb6a, identical to the live repository on 2026-11-21) by 8.16e-2, 4.35e-2 and 7.10e-4 respectively (each > 1e-9), and no other file of that database lists a value at those degrees that is as large; comparison with newer literature was not checked.

Verdict on criterion (i), all clauses except "newer literature": met for each of the three polynomials, which should be packaged as three separate results. Whether the claim as a whole is CONFIRMED still depends on the NOVELTY skeptic's literature check, with d=40 the most exposed.

pass: true
