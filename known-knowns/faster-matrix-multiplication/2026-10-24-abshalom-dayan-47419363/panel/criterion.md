# Criterion skeptic: <18,19,19> rank 3424 over Q (target fmm-catalogue-small-format-rank, partial win p1)

context: subagent (fresh context, Agent tool, model claude-opus-5-5; saw only claim/)

**Bottom line:** the claim meets partial win p1 as literally worded, and it does not claim the main criterion.
Every clause of p1 holds on evidence I re-ran or re-fetched myself, with one exception: the Lille index
'construction' column, which I take from claim/TABLE_RECORD.md and did not fetch. Its literal wording does not
exclude a restriction plus a reduction that lowers the rank. Pass.

## What I read and ran

Read: claim/CLAIM.md, claim/TABLE_RECORD.md, claim/REPRODUCE.md, claim/verify-it-yourself/ (all three files),
claim/rebuild/ (convert.py, rebuild_18x19x19.py, export_txt.py, and the header and restriction functions of engine.py),
the headers and first lines of claim/object/u.txt, v.txt, w.txt. Nothing else in the run folder.

Ran, all from the copy panel_work/criterion/claim_copy/ (claim/ untouched; its object sha256s are unchanged afterwards):

1. `sh verify-it-yourself/run_checks.sh` (output in panel_work/criterion/run_checks_output.txt, real 42.05 s):
   `format <18,19,19>, 3424 terms, every term with three nonzero factors, common denominator 352800, 42224004 Brent equations checked, 0 wrong`,
   `rank 3424 scheme for <18,19,19> over Q verified exactly`, then 3 random exact trials each `0 of 342 entries of C differ from AB`, last line `PASS`.
   Object sha256s match claim/REPRODUCE.md: u 47419363a41b203879fe8ae93035fe231852f01eb3081ad15c306a91d1e3298a,
   v dbf5c154ad97f11abdefd3d7d9ff1fda723a49710e881124bc547299308a93fa, w 797187bb905b8ee0dd22f321b802a1009938e2b4905517c1ffa7c576749bfacb.
   I read check_scheme.py. It parses every coefficient as a Fraction, clears all of them to integers over one common
   denominator, expands every term, and compares every stored (u,v,w) index triple with the delta tensor. It also checks
   that every diagonal triple is present, and rejects a term with an empty factor. The logic is a correct Brent-equation check.
2. My own checker, panel_work/criterion/my_check.py, written independently (output in my_check_output.txt):
   headers format (18, 19, 19), rank 3424; 3424 data lines in each file; 0 terms with a zero factor, 3424 with three
   nonzero factors; nonzeros u 147881, v 73004, w 65543; denominators [2, 4, 5, 7, 10, 12, 14, 25, 28, 50, 84, 300,
   600, 1200], the same list as claim/CLAIM.md; full Brent check mod 2^61-1: 42224004 equations, 0 wrong, 0 diagonal
   entries missing; 5 random evaluations mod 2^61-1, each 0 of 342 entries differ.
3. Provenance of the restriction step, panel_work/criterion/provenance_count.py on claim_copy/rebuild/19x19x19_r3633.npz
   (sha256 72633df65c1da7195d1a3284845cf82bf70c5e11c969895a33b7167bd978889b, as in REPRODUCE.md): metadata tensor
   [19, 19, 19] rank 3633; with e = (1,...,1,-7 at index 9,1,...,1) on the A side and f = e_0 on the C side, 180 terms
   are killed via U = e x^T and 28 via W = e_0 y^T, with 0 terms in both, so 208 are killed and 3425 remain, as the claim
   states. I could not re-run the final 2-reduction (3425 to 3424) because engine.py needs python-flint, which is not
   installed, and I did not install it. That does not matter for the verdict: the final object itself is exactly verified.
4. One honest GET of each live source (User-Agent "V3R1T4S-research-agent (honest single GET)", no retries; bodies and
   headers in panel_work/criterion/data/):
   - fmm_sota.json: fetched 2026-10-24T18:18:21Z, HTTP 200, sha256
     2a6535154ac877aeb495f9294a5e97c3dbf1b1969aefe6ffc0a612f2cf01cbae, identical to both fetches in TABLE_RECORD.md;
     createdAt 2026-10-19T20:46:33; 5456 entries; the only entry for any ordering of (18,19,19) is
     `{"format": [18, 19, 19], "rank": 3633, "exponent": 2.801315}`.
   - https://fmm.univ-lille.fr/18x19x19.html: fetched 2026-10-24T18:18:21Z, HTTP 200, sha256
     7de98cb2a073dcfaa8ee3a879caaa3f6c02c1d1ab9828b9da1cf016828161490, identical to TABLE_RECORD.md; Last-Modified
     Fri, 19 Jun 2026 21:23:26 GMT; title "Description of fast matrix multiplication algorithm: 18 x 19 x 19"; the only
     rank given on the page is ⟨18×19×19:3816⟩ (panel_work/criterion/lille_extract_output.txt).
5. Trivial-construction baseline, panel_work/criterion/composition_bound.py on the fetched fmm_sota.json. It finds the
   best rank for <18,19,19> reachable from listed ranks by permutation, restriction from any larger listed format,
   recursive block splitting along every axis, and two-factor tensor products with padding. The result is 3633. The
   best one-level split is 3697 ((18,1,19) + (18,18,19)); the best nontrivial product is not lower. So 3424 lies 209
   below everything that plain composing, padding or block splitting of listed schemes gives.

## Clause-by-clause against p1 (verbatim: "A new rank for a format with 17 <= max(n,m,p) <= 32 (outside Perminov's 16x16x16 table but inside the Lille catalogue): an exactly verified scheme whose rank is strictly below the live fmm_sota.json entry and the live Lille per-format page for that format, and not a plain composition already listed in the Lille 'construction' column.")

| Clause | Evidence | Holds? |
|---|---|---|
| 17 <= max(n,m,p) <= 32 | format 18 19 19 in all three headers; max 19 | yes |
| outside Perminov's 16x16x16 table | 19 > 16; TABLE_RECORD.md: Perminov's docs/ranks.md has no <18,19,19> row | yes |
| inside the Lille catalogue | live per-format page 18x19x19.html is HTTP 200; fmm_sota.json (the Lille digest) has an [18, 19, 19] entry; TABLE_RECORD.md records the index row "18x19x19" | yes |
| exactly verified | exact integer check over common denominator 352800, 42224004 Brent equations, 0 wrong (re-run by me); independent mod-P re-check agrees | yes |
| strictly below the live fmm_sota.json entry | 3424 < 3633 (fetched 2026-10-24T17:37:57Z for the claim; re-fetched unchanged 2026-10-24T18:18:21Z) | yes |
| strictly below the live Lille per-format page | 3424 < 3816 (same two fetch times, body unchanged) | yes |
| not a plain composition already listed in the Lille 'construction' column | column lists Proj([[19, 0], [0]], <19x19x19:3633>), giving 3633 (TABLE_RECORD.md, index fetched 2026-10-24T15:58:56Z); the object has rank 3424, so it is not that listed construction; see below | yes |

Counting convention: rank = number of terms with three nonzero factors = 3424 (both checkers). Ring: Q. Coefficients
are rationals with the 14 denominators above, checked exactly over Q, and the claim says Q, not Z, so nothing wider is
claimed. Orientation: A is 18x19 and B is 19x19, so <n,m,p> = <18,19,19>, which is already the sorted form (18,19,19)
that fmm_sota.json and the page name 18x19x19.html use. In any case, ranks do not change when the format is permuted.

## The composition clause, read literally

- p1 excludes "a plain composition **already listed**" in the construction column. The only listed construction for
  this format is Proj([[19, 0], [0]], <19x19x19:3633>) at rank 3633. The object is a different derivation: a
  non-coordinate slice pair (e with -7 at index 9, f = e_0) that kills 208 terms, followed by an exact 2-reduction. Its
  rank, 3424, is not listed anywhere. So it is not the listed construction. It is also not a composition at all (it uses
  one parent scheme, not several combined).
- The main criterion's sentence ("A scheme obtained by composing, padding or block-splitting known schemes does not
  count if the resulting rank equals a value already listed") excludes a scheme only if its rank equals a listed value.
  3424 equals none of 3633, 3816, or matmulcatalog's 3595 (TABLE_RECORD.md). Restriction plus reduction is in any case
  not composing, padding or block splitting.
- A stretched reading would exclude every derivation from a published scheme. Neither text says that. The clause guards
  against re-deriving a listed rank, and this derivation lowers the rank to an unlisted value. The baseline in step 5
  confirms that plain constructions from the live table reach only 3633.

## Main criterion not claimed; nothing wider implied

claim/CLAIM.md claims p1 only and states "not the main criterion (which needs max <= 16)". That is right: max dimension
19 > 16. The claim sentence talks about a scheme with 3424 multiplications, which is an upper bound. It does not say the
tensor rank of <18,19,19> is 3424, and my scope below keeps to that. "Non-commutative" is accurate for a scheme that
satisfies the Brent equations. The scheme is not a ternary or integer re-derivation, and it is not an additions record.

## Hidden quantifiers and residual caveats

- "A new rank": the colon in p1 introduces its operational definition (below the live fmm_sota.json entry and the live
  per-format page, and not an already-listed composition), and that definition is met. Read more broadly, as "below
  everything known", the files add: matmulcatalog lowest 3595, no row in Perminov's table, no MerlijnW70 scheme, and
  no <18,19,19> rank in the V3R1T4S pull requests. The files do not say whether LITA's own schemes/ folder holds an
  18x19x19 scheme, and I did not fetch it. This is a residual caveat outside p1's literal test,
  not a failed clause.
- "Live": both p1 sources were re-fetched by the claim at 2026-10-24T17:37:57Z and by me at 2026-10-24T18:18:21Z, with
  identical sha256s each time.
- The Lille per-format page (3816, Last-Modified 19 Jun 2026) lags the index and fmm_sota.json (3633). The object
  beats both values, so this inconsistency cannot affect the verdict.
- The construction-column value comes from TABLE_RECORD.md (index fetched 2026-10-24T15:58:56Z, sha256
  57e936b6aa0efe3a2e4020e14a84f5533983f66d5befd16fbb08bd448bd906a9). I did not re-fetch the index page.

## Null model

I agree that a null model in the statistical sense does not apply here. The object is an explicit scheme, and the
exact Brent-equation check is a proof, not a sampled result. The relevant baseline is what trivial constructions would
give, and step 5 puts that at 3633.

## Text addressed to reviewers

The fetched pages and claim files contain no text addressed to reviewers. I scanned the Lille page text for
"ignore", "instruction", "agent", "assistant" and "model", and fmm_sota.json for "ignore previous", "instruction",
"assistant", "AI agent", "language model", "LLM" and "Claude"; none matched.

confirmed_scope: The files in claim/object/ define a bilinear scheme over Q for <18,19,19> (A 18x19 times B 19x19) with 3424 rank-one terms, each with three nonzero factors, satisfying all 42224004 Brent equations in exact arithmetic, and 3424 is strictly below the rank 3633 for (18,19,19) in the live fmm_sota.json and the rank 3816 on the live Lille page 18x19x19.html (both fetched for the claim at 2026-10-24T17:37:57Z and re-fetched unchanged at 2026-10-24T18:18:21Z) and below the 3633 of the only listed Lille construction Proj([[19, 0], [0]], <19x19x19:3633>) (index fetched 2026-10-24T15:58:56Z), so it meets partial win p1 of fmm-catalogue-small-format-rank and not the main criterion.

pass: true
