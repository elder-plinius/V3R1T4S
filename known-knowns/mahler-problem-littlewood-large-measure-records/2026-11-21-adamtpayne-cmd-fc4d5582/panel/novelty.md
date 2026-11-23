# Novelty review: Littlewood polynomials of degree 32, 36, 40 with large Mahler measure

context: subagent (fresh context)
role: novelty skeptic (default FAIL unless confirmed)
target id: mahler-problem-littlewood-large-measure-records
review window (UTC): 2026-11-21T19:27Z to 2026-11-21T19:46Z

## Claim under review (from claim/CLAIM.md)

| d | claimed M(f) | claimed table max (LargeSkewSymmLittlewood.txt) |
|---|---|---|
| 32 | 5.537693429188808... | 5.456083591785 |
| 36 | 5.866860851319762... | 5.823385551581 |
| 40 | 6.154355891276200... | 6.153645888590 |

Pass condition for this review: each value beats everything public for its degree by more than 1e-9.

## 1. Live re-download of the Mahler-Measure-Database

- `git clone --depth 1 https://github.com/mossinghoff/Mahler-Measure-Database.git` into scratch (dir `mmdb`), 2026-11-21T19:28Z.
  - HEAD commit `7e3798516710370a758e16eb5de6bccbee98bb6a`, 2026-07-18T20:31:10-04:00, "Updated description of LargeSkewSymmLittlewood.txt." This is the same commit the claim cites, so the table has not changed since.
  - sha256 LargeSkewSymmLittlewood.txt = `38d92d006622b8c8aec8261a7b369ff96b419c547825ad6f9e65670a4742b5c0`, which matches claim/data/SOURCE.txt.
  - sha256 LargeLittlewood.txt = `5ea9400119b35812b37c1ffd5464b9f0ca8d41e3e72001a6327012b2dbae7907`, which also matches.
- Maximum per degree in the live LargeSkewSymmLittlewood.txt (25 entries for each of d = 32, 36, 40):
  - d=32: 5.456083591785 (`++----+++-+---+--+++-++++-++-+--+`)
  - d=36: 5.823385551581
  - d=40: 6.153645888590
  These agree with the values in the claim.
- Margins, claimed minus table max: d=32 +0.0816, d=36 +0.0435, d=40 +0.00071. All are far above 1e-9.
- Other files in the database:
  - LargeLittlewood.txt (general Littlewood polynomials) covers only degrees up to 30. I confirmed this: the largest degree field in the file is 30, and the README says "each fixed degree ≤ 30".
  - Littlewood_All72.txt covers M in (1, 5/3), and Littlewood_Top40.txt lists the smallest measures. Both are irrelevant at M > 5.
  - AllSmallMeasures_200, BestByDegree_200, BestByHeight, BestByRootCount_200, BestMeasures, SalemList, SmallBivariate and SummaryReport_200 all concern measures below about 1.3, so they are irrelevant.
  - No file in the database has a value at d = 32, 36 or 40 that exceeds the claimed values.
- Full-history clone (dir `mmdb_full`): 9 commits from 2026-07-01 to 2026-07-18. The only change to the skew table was the addition of d = 58 and 60. No earlier version had a larger d=32/36/40 entry, and LargeLittlewood.txt never went beyond d=30.
- Independent check (script `tools/check.py`, numpy roots):
  - The three claimed polynomials have M = 5.537693429189, 5.866860851320 and 6.154355891276, which agree with the claim to 12 digits.
  - None of them is skew-symmetric. The test was validated on the table's top entries, which it correctly flags as skew-symmetric.
  - So the claimed objects are general Littlewood polynomials. The database has no general-Littlewood table for d > 30. This is why they can beat the skew-symmetric maxima without contradicting the skew-symmetric table, which is exhaustive for these degrees.

## 2. Literature and web

All fetches were via WebFetch/WebSearch between 19:29Z and 19:45Z. Shell access to arxiv.org, export.arxiv.org and samaritan-research.org was refused by the proxy (403).

- Mossinghoff, "Mahler's problem and Turyn polynomials", arXiv:2405.08281.
  - Read: https://arxiv.org/abs/2405.08281, https://arxiv.org/abs/2405.08281v2 (shows submitted 2024-05-14, this version v2 2025-10-23), https://arxiv.org/html/2405.08281v1 and https://arxiv.org/html/2405.08281v2.
  - Search results list only v1 and v2. A direct fetch of a v3 URL was refused as not allowlisted, and no v3 appeared in searches.
  - Both versions contain no explicit Littlewood polynomial of degree 31 to 60 and no per-degree table. The only explicit polynomial is the degree-12 Barker one (0.98636). Table 6.1 is indexed by J, not by degree. The paper points to Borwein–Mossinghoff Table 2 for d ≤ 24/25.
- Borwein & Mossinghoff, "Barker sequences and flat polynomials" (2008), https://cecm-wayback.dcr.sfu.ca/~pborwein/PAPERS/P213.pdf: Table 2 gives maximal M for length n ≤ 25 (degree ≤ 24) only. There is nothing for d ≥ 26 and no higher-degree skew searches.
- Borwein's lecture notes / book material, https://cecm-wayback.dcr.sfu.ca/~pborwein/TEMP_PROTECTED/LECTURES.pdf: states the research problem ("find the polynomials in L_n that have largest possible Mahler measure"). No table was found for d ≥ 26 in the part I read (about 97% of the text).
- Bober, Klurman, Shala, arXiv:2510.06161 (v3, 2026-11-05), https://arxiv.org/abs/2510.06161 and https://arxiv.org/pdf/2510.06161v3: the record is asymptotic only (normalized M > 0.954). There are no explicit polynomials or values at specific degrees.
- Odlyzko, "Search for ultraflat polynomials with plus and minus one coefficients", https://www-users.cse.umn.edu/%7Eodlyzko/doc/ultraflat.pdf: covers sup-norm quantities and merit factor only, with no Mahler measure values.
- AlphaEvolve paper, "Mathematical exploration and discovery at scale", arXiv:2511.02864 (pdf, read in 2 parts, up to char 200000 of 259507): its section 13 covers flat polynomials and the Golay merit factor. It has no Mahler measure values.
- el Abdalaoui, arXiv:2610.30797 (2026-10-23): no Mahler measure values.
- Idris & Sac-Épée, arXiv:2607.15520: not relevant (Newman/Littlewood multiples).
- Hokken et al., arXiv:2603.20820: not relevant (bivariate polynomials).
- FrontierMath open problem page:
  - https://samaritan-research.org/frontiermath/open-problems/large-mahler-measure could not be fetched (site client_error via WebFetch, proxy 403 via shell).
  - I read the same problem at https://epoch.ai/frontiermath/open-problems/large-mahler-measure, found by web search. It asks for an asymptotic family with normalized M > 0.97, marked "Solved (AI)" (an OpenAI ultraflat-Littlewood preprint, 2026-10-06), and cites the 0.954 record. It gives no finite-degree values and nothing for d = 32, 36 or 40.
  - The page's "Prompt" section addresses solvers, AI systems included. It is a problem statement, not an instruction aimed at this review, so I treated it as data. No injection suspected.
- Searches for the digit prefixes "5.5376934", "5.8668608" and "6.1543558": no relevant hits (only unrelated numeric pages).
- Searches covering GitHub, Zenodo, MathOverflow, theses, and "Littlewood polynomial large Mahler measure" (standard and extended) found no table of large measures of general Littlewood polynomials for degree ≥ 31. The only per-degree source for d > 30 is the skew-symmetric table above.
- Not readable: an SFU thesis PDF (https://summit.sfu.ca/_flysystem/fedora/sfu_migrate/7393/b18765270.pdf) and SFU items 8170 and 8695 were blocked by bot protection (Anubis access denied). I could not identify their titles. They are pre-2008 SFU archive items, and Borwein–Mossinghoff 2008 and the 2026 database (the author's own updates) report nothing beyond d=24 and d=30 respectively, so I do not treat them as key sources. This remains a residual uncertainty.
- Own check of known structured constructions (script `tools/turyn.py`): the best Turyn/Fekete-companion Littlewood polynomials over all shifts and both signs give:
  - p=37 (d=36): M = 5.6137
  - p=41 (d=40): M = 5.9865
  Both are below the claimed values (degree 32 has no prime length).

## 3. V3R1T4S (github.com/elder-plinius/V3R1T4S)

- At 2026-11-21T19:32Z I created a bare repo `v3.git` in scratch and fetched `+refs/pull/*/head` and `+refs/heads/main` (depth 1). Result: 1158 PR refs plus main. main head is `5db3547dd45ca38eb4a50c5c30f8dadcb50f6cbd` (2026-11-19T14:48:58-08:00).
- main:
  - TROPHY_CASE.md has no "Littlewood" or "Mahler" entry. Its families are degree-diameter, Lehmer, matrix multiplication, VNN-COMP, RobustBench, constant-weight codes and cipher commitments.
  - known-knowns/ has 45 family folders and none is about Mahler or Littlewood.
  - The only main hits are the SHA256SUMS line for known-unknowns/record-tables/mahler-problem-littlewood-large-measure-records.md (ignored, as instructed) and an unrelated Komlós novelty note that mentions a "Littlewood-Offord" PR.
- PR-only blobs:
  - Listed with `git ls-tree -r` per ref: 4,571,928 (blob, ref, path) rows, giving 20,001 unique blobs not present on main (`pr_only_blobs.txt`).
  - Streamed all of them through `git cat-file --batch` into `tools/scan.py`, case-insensitive, for littlewood, mahler-problem-littlewood, largeskewsymm, 5.5376934, 5.8668608 and 6.1543558. 89 blobs matched (`pr_hits.txt`), mapped to paths in `hit_paths.tsv`.
  - There were zero hits on any of the three digit prefixes.
  - Ignored hits: bank/targets.json (1075 rows), SHA256SUMS (313), known-unknowns/ pages (record-tables/mahler-problem-littlewood-large-measure-records.md, number-hunts/mahler-measure-new-small-polynomials.md, erdos-and-proofs/README.md).
  - Remaining hits, none of which is an actual Littlewood claim:
    - PR 907: centred Hardy-Littlewood maximal constant (C_47), unrelated.
    - PRs 79 to 89: snake/coil-in-the-box novelty reports. Their prose lists a ledger entry "#2 Littlewood polynomials" in a trophy list that does not match main's TROPHY_CASE.md. They contain no Littlewood object, value or Mahler claim.
  - No PR file path contains "mahler" or "littlewood" outside known-unknowns/.
- Conclusion: there is no prior V3R1T4S claim for this target or these values.

## Verdict

- The live table, re-downloaded at commit 7e37985 with sha256 matching the claim, has maxima 5.456083591785 (d=32), 5.823385551581 (d=36) and 6.153645888590 (d=40). The claimed values exceed them by 8.2e-2, 4.3e-2 and 7.1e-4, all well above 1e-9.
- No other database file, no version of the Mossinghoff and Borwein–Mossinghoff papers, no newer literature I found, and no V3R1T4S branch or PR lists any Littlewood polynomial of degree 32, 36 or 40 with a larger Mahler measure.
- The claimed polynomials are non-skew-symmetric general Littlewood polynomials, and public tables of those stop at d = 30.
- Caveats:
  - The samaritan-research.org page itself was unreachable; the same problem was read on epoch.ai.
  - Some old SFU theses were blocked by bot protection.
  - This review did not re-certify M rigorously. It only did a numpy sanity check that agrees to 12 digits.

novelty: CONFIRMED (no public value at d = 32, 36, 40 found that matches or beats the claim)
pass: true
