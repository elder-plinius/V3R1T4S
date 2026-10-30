# PREREG (frozen 2026-10-24T19:03:49Z, from date -u)

## Honesty note: the value existed before this prereg

This prereg does NOT precede the object. The <18,18,19> rank-3225 scheme was built and checked by an earlier run of the
same contributor before this file was written:
- built: attempts/constructor/out/rebuild_lita19.log of that run ("step 2: absorbed 1 -> rank 3225"); the scheme
  file attempts/constructor/out/lita19.step2.json has mtime 2026-10-24T17:37:31Z;
- checked there by two exact checkers (out/verify_lita19_step2_stdlib.txt and _flint.txt, both PASS);
- predicted there as 3424 - 199 = 3225 (step-2 kill count (N^2+2N-1)/2 = 199 for N = 19, seen on N = 15 and 17).
  The earlier run's report says the prediction was an inline run at about 17:32Z, before the build; the saved copy of that
  computation, out/predict_p1_band.txt (row "19 | 18x18x19 | 3225 | 3355 | 3355 | 130"), has mtime
  2026-10-24T17:42:29Z, i.e. it was SAVED after the build. Only the build log and file times are evidence; the
  17:32Z inline run is the earlier run's own statement.
- the earlier run's PREREG (frozen 2026-10-24T16:14:48Z) listed "fallback p1 cells with max dim 17..32 next to odd LITA
  squares" among its planned cells.
What this prereg freezes is therefore only the judging rule for this claim, before this run's own rebuild, own
checks and own novelty fetches produce any output.

## Criterion (verbatim, partial win p1 of the bank entry)
p1: A new rank for a format with 17 <= max(n,m,p) <= 32 (outside Perminov's 16x16x16 table but inside the Lille catalogue): an exactly verified scheme whose rank is strictly below the live fmm_sota.json entry and the live Lille per-format page for that format, and not a plain composition already listed in the Lille 'construction' column.

(The main criterion needs max(n,m,p) <= 16; <18,18,19> has max 19, so only p1 is in play.)

## Object and statistic
- Object: u.txt, v.txt, w.txt (rational coefficients as exact strings) for the format <18,18,19>
  (A 18x18, B 18x19, C 18x19).
- r = number of terms whose three factors are all nonzero, counted by the checkers; every term must have three
  nonzero factors (a term with a zero factor is a defect, not a free term).
- Checks that must all pass:
  1. deterministic rebuild from LITA's published schemes/19x19x19_r3633.npz (sha256 recorded at fetch) with the
     earlier run's code copied unchanged, byte-identical to the earlier run's lita19.step2.json, and its text export
     byte-identical to the claimed u/v/w files;
  2. a standard-library-only exact checker written or adapted in this run: every Brent equation
     sum_k u_k[i,j] v_k[j',l] w_k[i',l'] = [j=j'][i=i'][l=l'] checked over Q (Fractions or integers after an
     explicit scaling), for all 18*18 * 18*19 * 18*19 index triples (stored and zero);
  3. three random exact evaluations C = AB with random integer A, B, compared entry by entry with exact arithmetic;
  4. negative controls: the checker must reject a copy with one term deleted and a copy with one coefficient changed.
- Any failure or disagreement kills the object.

## Bar and threshold
- bar = the minimum, over the format <18,18,19> AND its permutations 18x19x18 and 19x18x18, of: the fmm_sota.json
  rank (sedoglavic/fmm_digest), the Lille index row and the Lille per-format pages, matmulcatalog docs/catalog.json,
  Perminov's docs/ranks.md (and docs/additions.md and schemes/results/ if they cover the format), MerlijnW70
  fmm-schemes, every pull request of elder-plinius/V3R1T4S (open and closed) and every merged known-knowns entry
  that gives a rank for this cell, and any literature found. Each source fetched once, live, timestamped UTC.
- Threshold: r <= bar - 1 (strict). r == bar is a tie and not a win. Per kit/POLICY.md, an equal or better value
  public before filing means not new.
- For p1 literally: r must be strictly below the live fmm_sota.json entry and the live Lille per-format page, and
  not a plain composition already listed in the Lille 'construction' column.
- One cell per claim: <18,18,19> only. The sibling <18,19,19> 3424 (PR #708) is NOT part of this claim.

## Null design
null_test: not needed because the claim is an explicit object checked by deterministic exact checkers against a table value (no search statistic, no chance baseline).
