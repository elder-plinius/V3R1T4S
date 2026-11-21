# REPRODUCE report: large Mahler measures of Littlewood polynomials, d = 32, 36, 40

context: subagent (fresh context)

## Scope
I used only files in claim/ plus my own scratch folder (scratch/). I read CLAIM.md and REPRODUCE.md first. I wrote my own programs (scratch/mymahler.py, scratch/verify.py, scratch/agree.py) before opening code/certify.py or code/search.py.

Definition used: M(f) = |leading coefficient| × product over all complex roots r of f (counted with multiplicity) of max(1, |r|).

## Methods (my own)
1. **Rigorous, Arb (python-flint 0.9.0):** `fmpz_poly(coeffs).complex_roots()` gives certified isolating balls with multiplicities. I check that the multiplicities sum to the degree. For each root ball |r|: if lower(|r|) >= 1 the factor is |r|; if upper(|r|) <= 1 the factor is 1; otherwise the factor is the ball [1, upper(|r|)]. I multiply all factors in ball arithmetic at 400 bits.
2. **Independent numerics, mpmath 1.4.1:** `polyroots` at 60 and at 80 digits (extraprec 4*dps), then the product of max(1,|r|).
3. **Third check, rigorous with exact integers (Graeffe):** 20 root-squaring steps over Z, so g_k has roots r^(2^k) and M(g_k) = M(f)^(2^k). Two bounds hold for any integer polynomial g of degree d: M(g) <= ||g||_2 (Landau), and ||g||_2 <= ||g||_1 <= 2^d M(g). Together they give M(f) in [(||g_k||_2 / 2^d)^(1/2^k), ||g_k||_2^(1/2^k)]. This method does not use root finding at all.

I read the table values myself. scratch/verify.py parses every data row `d M M/sqrt(d+1) coeffs` of data/LargeSkewSymmLittlewood.txt and takes the maximum M over all listed entries for each d (25 entries each for d = 32, 36, 40, 60). The sha256 of the data files matches data/SOURCE.txt:
```
38d92d006622b8c8aec8261a7b369ff96b419c547825ad6f9e65670a4742b5c0  data/LargeSkewSymmLittlewood.txt
5ea9400119b35812b37c1ffd5464b9f0ca8d41e3e72001a6327012b2dbae7907  data/LargeLittlewood.txt
```

## Sanity checks against the database (output of scratch/verify.py)
```
LL d=30 table=5.367254096364 arb=[5.36725409636435 +/- 9.38e-16] mpmath=5.36725409636435 |arb-table|=3.49e-13 near-unit=0
SS d=32 table=5.456083591785 arb=[5.45608359178486 +/- 4.49e-15] mpmath=5.45608359178486 |arb-table|=1.44e-13 near-unit=0
SS d=60 table=7.524118801007 arb=[7.52411880100724 +/- 1.40e-15] mpmath=7.52411880100724 |arb-table|=2.39e-13 near-unit=0
SS d=36 table=5.823385551581 arb=[5.82338555158101 +/- 2.45e-16] mpmath=5.82338555158101 |arb-table|=9.76e-15 near-unit=0
SS d=40 table=6.153645888590 arb=[6.15364588859017 +/- 3.76e-16] mpmath=6.15364588859017 |arb-table|=1.70e-13 near-unit=0
SS d=40 table=6.048599036776 arb=[6.04859903677622 +/- 3.51e-15] mpmath=6.04859903677622 |arb-table|=2.24e-13 near-unit=0
```
Every checked table entry is reproduced to within its 12-decimal rounding. A Barker-13 test, `+++++--++-+-+`, gave `arb [3.556393149272513432339552826658472117071 +/- 3.51e-40]`, which matches the table's d=12 value 3.556393149273.

## Claimed objects (output of scratch/verify.py)
```
d=32 len=33 allpm1=True skew-symmetric=False equiv-in-table=[]
  arb    M = [5.5376934291888081387630315191949115 +/- 2.71e-36]  roots-with-|r|-ball-touching-1: 0
  mpmath M = 5.5376934291888081387630315191949115 (60 dps)
  mpmath M = 5.5376934291888081387630315191949115 (80 dps)
  Graeffe k=20 rigorous bracket: [5.53757629064, 5.53769342919]
  table max d=32: 5.456083591785  certified lower - table = [0.08160983740 +/- 3.81e-12]  >1e-9: True
  Graeffe lower - table = 0.0814927
  min ||r|-1| over roots: 0.0367469068526876
d=36 len=37 allpm1=True skew-symmetric=False equiv-in-table=[]
  arb    M = [5.8668608513197626971666739720398698 +/- 4.45e-35]  roots-with-|r|-ball-touching-1: 0
  mpmath M = 5.8668608513197626971666739720398698 (60 dps)
  mpmath M = 5.8668608513197626971666739720398698 (80 dps)
  Graeffe k=20 rigorous bracket: [5.86672123742, 5.86686085132]
  table max d=36: 5.823385551581  certified lower - table = [0.04347529974 +/- 1.24e-12]  >1e-9: True
  Graeffe lower - table = 0.0433357
  min ||r|-1| over roots: 0.0350610783491835
d=40 len=41 allpm1=True skew-symmetric=False equiv-in-table=[]
  arb    M = [6.1543558912762003590853975109900012 +/- 7.16e-36]  roots-with-|r|-ball-touching-1: 0
  mpmath M = 6.1543558912762003590853975109900012 (60 dps)
  mpmath M = 6.1543558912762003590853975109900012 (80 dps)
  Graeffe k=20 rigorous bracket: [6.15419316323, 6.15435589128]
  table max d=40: 6.153645888590  certified lower - table = [0.0007100026862 +/- 3.61e-16]  >1e-9: True
  Graeffe lower - table = 0.000547275
  min ||r|-1| over roots: 0.03180818251970186
```
How closely Arb and mpmath agree (scratch/agree.py):
```
d=32 |arb_mid - mpmath60| = 5.89e-61  agreeing digits ~ 61.0  arb radius = [1.11e-118 +/- 4.01e-121]
d=36 |arb_mid - mpmath60| = 1.75e-60  agreeing digits ~ 60.5  arb radius = [1.26e-118 +/- 4.65e-121]
d=40 |arb_mid - mpmath60| = 3.66e-60  agreeing digits ~ 60.2  arb radius = [1.61e-118 +/- 2.22e-121]
```
Findings:
- **Shape of the inputs:** each object has d+1 coefficients, all ±1, so the degree is d.
- **Agreement:** Arb and mpmath agree to more than 60 digits, well beyond the 20 required.
- **No roots near the unit circle:** no root ball touches |z| = 1. The closest root is about 0.032 from the unit circle, so the special handling of near-unit roots is never used.
- **Margins over the table:**

| d | certified lower bound − table max | Graeffe lower bound − table max |
|---|---|---|
| 32 | 0.0816 | 0.0815 |
| 36 | 0.0435 | 0.0433 |
| 40 | 7.100e-4 | 5.47e-4 |

  Every margin is far above 1e-9.
- **Not skew-symmetric:** none of the three polynomials is skew-symmetric. None is equivalent to any listed entry under reversal, negation, or x -> -x. So they are not in this table at all; they beat its maxima as general Littlewood polynomials. This is allowed by the success criterion, which asks for "a Littlewood polynomial f of even degree d" exceeding the listed maximum. data/LargeLittlewood.txt covers only d <= 30, so it has no competing value for these degrees.

## Author's certifier (REPRODUCE.md command, run from claim/)
```
== d=32 table max 5.456083591785
degree 32
arb ball   : [5.53769342918880813876303151919 +/- 4.92e-30]
mpmath 60d : 5.53769342918880813876303151919
agree to 20 digits: True
table value: 5.456083591785  certified M - table > 1e-9: True  (margin 8.161e-02)
== d=36 table max 5.823385551581
degree 36
arb ball   : [5.86686085131976269716667397204 +/- 1.31e-31]
mpmath 60d : 5.86686085131976269716667397204
agree to 20 digits: True
table value: 5.823385551581  certified M - table > 1e-9: True  (margin 4.348e-02)
== d=40 table max 6.153645888590
degree 40
arb ball   : [6.15435589127620035908539751099 +/- 1.3e-33]
mpmath 60d : 6.15435589127620035908539751099
agree to 20 digits: True
table value: 6.153645888590  certified M - table > 1e-9: True  (margin 7.100e-04)
```
This output is byte-identical to result/certify_outputs.txt (checked with `diff`), and the values agree with mine in every printed digit.

## Review of code/certify.py
- **Near-unit roots (lines 26–33):** with Arb balls, `m > 1` and `m < 1` are true only when the whole ball lies on that side of 1. Otherwise the factor is `arb(1).union(arb(mid+rad))`, which contains [1, upper]. The sum mid+rad is evaluated in ball arithmetic, so the true upper bound is enclosed. This is rigorous. For these inputs the branch is never taken anyway.
- **Multiplicities:** they are applied correctly through `for _ in range(mult)`. The leading coefficient is included.
- **Margin test (line 63–64):** `lo = M1.mid() - M1.rad()` is an Arb ball, and `lo - T > 1e-9` is true only if the entire ball exceeds 1e-9. This is rigorous.
- **Minor weaknesses that do not affect the result:**
  - `parse` maps any character other than '+' to -1 and does not check the degree. I verified the inputs separately.
  - The precision loop stops at 4000 bits without reporting failure. That is harmless here: the radius is about 1e-30.
  - The REPRODUCE.md pipeline takes the table maximum with `grep "^d  " | sort -gr | head -1`. This picks the same maxima I parsed myself.
- **No logic errors found.**

## Limitations
- I did not re-download the live database. I relied on the provided copy, whose hashes match data/SOURCE.txt.
- My check of "newer literature" was limited. One web search found no listed values for d = 32, 36, 40. A summary fetch of arXiv:2405.08281v2 (I saw only a model's summary, not the full text) said that paper lists maximal values only for d <= 25 by citing another source, and gives none for 32, 36, 40.
- This REPRODUCE task covers the computation. It does not exhaustively check every other database file.

## Verdict
All three polynomials are valid Littlewood polynomials of the stated degrees. Their Mahler measures are certified by Arb and confirmed by mpmath (agreement to more than 60 digits) and by an exact-integer Graeffe bracket. Each one exceeds the maximum listed for its degree in data/LargeSkewSymmLittlewood.txt by more than 1e-9 (margins 8.16e-2, 4.35e-2, 7.10e-4). I found no mismatch.

pass: true
