# NOVELTY verdict: brouwer-qary-unrestricted-a3-a4-a5, cell A4(11,7)
context: fresh reviewer (new context started for the NOVELTY role only; saw only CLAIM.md, RECORD.md, object/ and public pages; no access to the search code or the claimant's checker)
verdict_utc: 2026-11-20T14:09:31Z

## Live table (one plain curl GET, no retry)

| item | value |
|---|---|
| URL | https://aeb.win.tue.nl/codes/quaternary-1.html |
| fetched (UTC) | 2026-11-20T14:05:44Z |
| HTTP status | 200 |
| Date header | Fri, 20 Nov 2026 14:05:45 GMT |
| Last-Modified | Thu, 07 Sep 2017 11:17:33 GMT |
| ETag | "1673-558979b568d40" |
| Content-Length | 5747 |
| sha256 of bytes | 85cdd35bfe053946d1ebea9eb051e026e9462a2a63c24647992151008cf60aa4 |

The sha256 is identical to the one in RECORD.md. Rows for n = 11 (d = 3..10): ub 109226 30427 6241 1780 **320** 60 12 4; lb 77056 16384 4096 1024 **128** 48 = =. Cell A4(11,7): lb 128, ub 320, open.

The only note under the table that names the cell: "A4(12,8) ≥ 128, A4(11,7) ≥ 128. (A. E. Brouwer, Small additive quaternary codes, preprint 2002.)" No note gives more than 128.

## Object (own Python 3 standard-library check)

- `object/A4-11-7-145words.txt`, sha256 96ddddaebbcc6cf5d43f8869ebf951cf4520634e12d32df060e8b4acc5b6f9f0 (matches CLAIM.md).
- 145 words, 145 distinct, all of length 11 over {0,1,2,3}.
- Pairwise distance distribution over all 10440 pairs: d=7: 3960, d=8: 1980, d=9: 2880, d=10: 576, d=11: 1044. Minimum distance 7.
- I rebuilt the construction described in CLAIM.md: the closure of the five seeds under A and B gives orbit sizes 1, 36, 36, 36, 36, a 145-word length-12 code with minimum distance 8, and deleting coordinate 0 gives exactly the object's word set (True).

## Neighbouring cells (bounds that could already imply >= 145)

From the live table:
- A4(11,7) >= A4(12,8) (puncture): lb 128.
- A4(11,7) >= A4(12,7)/4 (shorten): 256/4 = 64.
- A4(11,7) >= A4(10,7) (add a coordinate): 48.
- A4(11,7) >= A4(11,8): 48.

The largest implied value is 128 < 145. Consistency with the upper bounds: 145 <= 320 for A4(11,7), and the length-12 parent (145 words, d = 8) is within A4(12,8) <= 240. No listed bound for any neighbouring cell gives 145 or more.

## Trivial edits of published objects

The published code for this cell and for A4(12,8) is the additive (12, 128, 8) code (Blokhuis-Brouwer) and its punctured form, with 128 words. Deletion, restriction, relabelling or symmetry of a 128-word code cannot produce 145 words. The object is not seeded from a published object. It is the puncture of a 145-word length-12 code that CLAIM.md says is unpublished and claimed separately at the same time; I found it nowhere public (see below). Only one ±1 relation separates the two cells, so this claim's novelty depends on that A4(12,8) code also being new. As far as I could find, it is.

## Literature and code search

- Laaksonen & Östergård, "New lower bounds on q-ary error-correcting codes", Cryptogr. Commun. 11 (2019) 881-889. Its Table 2 updates the quaternary table for n <= 12. I read it at https://aaltodoc.aalto.fi/server/api/core/bitstreams/9dad65a3-7198-4b0d-8a5b-9420265f095a/content at 2026-11-20T14:06:45Z (sha256 of the returned markdown dd876c218e7926fb76007c24a10afe6ea5493bfac947f2a1cde26ed12eb9685f). It still lists A4(11,7) lb 128 and A4(12,8) lb 128. Its appendix lists no new quaternary code for these cells.
- A plain curl to the research.aalto.fi copy of the same paper at 2026-11-20T14:06:39Z returned HTTP 403 with a Cloudflare challenge. I did not retry it, and the aaltodoc copy above covered the same paper. This was not the table page.
- Polak, "New nonbinary code bounds based on divisibility arguments" (DCC 2018, arXiv:1606.05144): it gives upper bounds only (A4(12,8) <= 240), with lower bound 128.
- Web searches (2026-11-20, about 14:05-14:09Z) for "A4(11,7)", "A_4(12,8)", "(12,145,8) quaternary code", 145-word length-12 distance-8 quaternary codes, new q-ary and quaternary lower bounds for 2024-2026, AlphaEvolve and LLM-guided code search, and additive (12,128,8) improvements. None found a lower bound above 128 for A4(11,7) or A4(12,8). The recent arXiv items found are on binary codes, constant-weight codes, covering codes, Z4/CD codes and additive dimension 3.5/4 codes, and none is about this cell.
- One arXiv API query (export.arxiv.org, http) at 2026-11-20T14:09:08Z returned HTTP 301 and an empty body. I did not retry it, so it is not evidence either way.
- github.com/owhs/code-table-improvements (created 2026-10-16, pushed 2026-10-17): it has binary, constant-weight, ternary/mixed and quinary results. It has no quaternary entry in its tree (415 paths) or README, and no releases are listed.
- github.com/arhancanli/quantavane-benchmark `families/unrestricted-code/family.json`: it read quaternary-1.html on 2026-11-15 with the same sha256 85cdd35b... and records `"quantavane_records": 0`.
- V3R1T4S (main at 5db3547d, 2026-11-19T22:48:58Z):
  - TROPHY_CASE.md has no quaternary or brouwer-qary entry.
  - known-knowns/ has no quaternary entry. bigger-codes/ holds constant-weight and binary items only.
  - known-unknowns/record-tables/brouwer-qary-unrestricted-a3-a4-a5.md still lists the target as open and says the quaternary page has not been modified since 2017-09-07.
  - I listed 1151 pull requests (all states) and searched their titles, branch names and bodies for "brouwer-qary", "quaternary-1" and A4(11,7)/A4(12,8)/A4(11,8)/A4(12,7) patterns. None matched.

## Problems found

None that bear on novelty. The two failed fetches (the Aalto portal PDF behind a challenge, and the arXiv API redirect) were not the table page. The paper behind the first was read in full through another copy, and the second is covered by the keyword searches above.

## Reasoning

The live table, re-fetched today with bytes identical to the claimant's snapshot, gives lb 128 for A4(11,7). The object is a valid (11, 145, 7) quaternary code by my own all-pairs check. 145 > 128 strictly. No neighbouring bound implies 145 or more. No published object gives 145 words through trivial edits. The 2019 update tables, the notes under the table, the recent literature and code I found, and the V3R1T4S trophy case, known-knowns and pull requests contain no bound of 145 or more for this cell.

pass: true
