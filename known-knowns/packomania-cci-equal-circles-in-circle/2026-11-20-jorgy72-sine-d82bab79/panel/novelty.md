context: subagent (fresh context, spawned as the argue-against skeptic)
# NOVELTY / ARGUE-AGAINST verdict — N=4357 claim

Role: skeptic. Every number below was computed by my own scripts
(independent scripts written from scratch); nothing was taken
from the main session's logs or from the pre-existing `panel/non_isometry.*`
files (which I did not use).

Claim: candidate `attempts/deep-polish-4357/output/polished01.txt`,
r* = 0.01426010900644796452099252854564, margin +4.938e-06 over the
Packomania table radius 0.014255170553446144330034824715.
Seed `data/cci4357.txt`, sha256 verified by me:
778c91a9e89b42372303330e2d3faf7a8bea563cb402da399cd893d1d13da959 (matches claim).

## 1. NON-ISOMETRY — PASS (attack failed; claim survives)

Sorted pairwise-distance multisets computed independently in float64
(numpy blocks, 9,489,546 pairs each):

- max |diff| between candidate and seed multisets: **3.765097e-03**
- fraction differing by >1e-9: **0.999999**
- fraction differing by >1e-12: 1.000000; by >1e-6: 0.999281
- median |diff|: 3.670108e-04

The configurations are nowhere near isometric. (Sanity: candidate min
pair/2 = 0.0142604143 vs seed 0.0142551706 — the seed reproduces its own
table value, as expected.)

## 2. QUEUE — PASS

Re-fetched `https://packomania.com/pending-requests.html` live with curl
(2026-11-20, HTTP 200, 12,856 bytes — byte-identical to the stored copy).
The page is dated 18-Nov-2026. The only **cci**-category pending ranges are:

- Vidit Patankar, 15-Oct-2026: **652–3943**
- Karl Desfontaines, 03-Nov-2026: **126–4141**

N=4357 is inside neither (3943 < 4357, 4141 < 4357). The broad ranges on
the page that do contain 4357 (e.g. 1015–9996, 385–9996, 501–9984,
917–100000, 112–10002, 137–9604) are all in other categories
(csq, ssp, csqv, scu) — not cci. No queue conflict.

## 3. HISTORY — PASS

Re-fetched `https://packomania.com/cci/cci.html` live with curl
(2026-11-20, HTTP 200, 1,310,659 bytes — byte-identical to the stored copy).
The Updates list has 67 dated entries; the latest is **11-Oct-2026**
(Zii Fave, computer-assisted proofs for N=15). There is **no** History entry
newer than 11-Oct-2026 at all, and none touching N=4357. The live table
row for N=4357 still reads 0.014255170553446144330034824715, matching
`data/radius.txt` exactly.

## 4. MARGIN REALITY — PASS

Recomputed r* in mpmath at 50 digits from the file with my own script
(float64 pre-screen, then exact 50-digit verification of the single
near-min pair and the single near-max |c| — float error ~1e-16 is ten
orders below the margin, and only 1 candidate pair / 1 center fell
within 1e-6 / 1e-9 of the extrema):

- exact min pair distance: 0.02852082863015242963756009733780476991379
  (pair 4109, 4347) → r_pair = 0.01426041431507621481878004866890238495689
- exact max |c|: 0.9857398909935520354790074714543626820251 (center 4347)
  → r_wall = 0.01426010900644796452099252854563731797494
- **binding constraint is the wall**, not a pair.
- my r* (50 digits): **0.014260109006447964520992528545637317974939357621236**
- margin: **+4.938453001820190957703830637317974939357621236e-06**

The margin is real, not a rounding artifact. One wording correction: the
claimed string carries **31** significant digits, not 50 — it is the
checker's `mp.nstr(r_star, 31)` printout, correctly rounded (my first 30
significant digits agree; the 31st differs only by rounding of the
following digit 7). The value itself is verified by me to full 50-digit
precision. No hole.

## 5. FILE INTEGRITY — PASS

Candidate file, checked independently:

- exactly **4357 rows**, indices sequential 1..4357, 0 unparsable lines
- all coordinates finite
- max |c| = 0.98573989099355208 < 1
- **4357 unique centers** (1e-12 grid) — no duplicates
- candidate sha256: d82bab7925486928eec1ff24ff9a562768928c24d34d15263b2535295a6b9248

Seed file likewise: 4357 rows, finite, max |c| = 0.98574482944655395 < 1,
4357 unique centers, 0 bad lines.

## 6. CHECKER INSPECTION — PASS (no flattery found)

Read `code/checker.py` in full:

- `feasible_radius` is the correct formula `min(min_pair/2, 1 - max|c|)`,
  computed in mpmath at 50 dps with **no tolerance** anywhere.
- `table_radius` reads `data/radius.txt`; the N=4357 row is unique in the
  file and its value matches the live Packomania table row (verified in
  attack 3). No wrong lookup, no off-by-one.
- `check()` asserts the center count equals N, so a short/corrupt file
  fails loudly rather than flattering.
- Ran the checker's own `--selftest` myself: POSITIVE PASS (cci100
  reproduces the table to 8.7e-31), multiset self-match PASS, NEGATIVE
  PASS (a 1e-6 perturbation collapses the margin to −4.659e-07).
- Minor observations, none flattering: `load_centers` silently skips
  lines with <3 fields (caught by the count assert); the checker does
  not itself test non-isometry (that lives in a separate function, and I
  tested it independently in attack 1); `distance_multiset` uses float
  (irrelevant at the 3.8e-03 separations seen here); the printed r* is
  31 significant digits, not 50 (cosmetic — see attack 4).

## OVERALL: PASS

All six attacks failed. The claim survives: a genuinely new, non-isometric
packing with a verified +4.938e-06 margin at 50-digit precision, no queue
conflict, no newer table update. Nothing here kills it.

pass: true
