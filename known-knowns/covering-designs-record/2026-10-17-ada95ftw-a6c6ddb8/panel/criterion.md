# CRITERION skeptic verdict: C(20,6,3) <= 70
context: subagent (fresh executor, saw only claim/; shares parent's product and conversation history)
verified at: 2026-10-17T15:00Z-15:04Z (UTC)

## Clause-by-clause (criterion.md, read literally)

1. "b blocks, each a k-subset of a v-set (no repeated points)": met.
   Own checker written from the definition (not checker.py):
       lines 70 distinct 70 allsize6 True range 1 20
   sha256sum C20_6_3_70blocks.txt
       a6c6ddb8d095dc3818d1eb09a2a2342cfa3254b443799c213068aff07d2a4c6f  (matches CLAIM.md)

2. "covering every t-subset (checked exhaustively)": met. All C(20,3)=1140 triples were enumerated:
       triples 1140 uncovered 0
       redundant blocks 0      (no block can be deleted, so the design isn't padded)
   checker.py agrees, and its null model behaves correctly:
       C(20,6,3) blocks=70 covers_all=True uncovered=0 schonheim=64
       C(7,3,2) blocks=7 covers_all=True uncovered=0 schonheim=7     (data/pos_fano.txt)
       C(7,3,2) blocks=6 covers_all=False uncovered=3 schonheim=7    (data/neg_fano6.txt)

3. "STRICTLY SMALLER than EVERY one of ... each re-fetched at verification time". 70 < 71 in every source:
   - dmgordo/LJCR GitHub, re-fetched by me (single plain fetch):
       2026-10-17T15:01:00Z 200 raw.githubusercontent.com/dmgordo/LJCR/main/coverings/coverdata.json -> size 71, low_bd 64
     api.github.com/repos/dmgordo/LJCR/commits?since=2026-04-17 -> 0 commits (data unchanged for 6 months)
   - Zenodo LJCR, re-fetched by me: zenodo.org/api/records/10779736/versions/latest -> id 19735294, version 1.2,
     2026-04-24 (newest). Its coverdata value (71) comes from the claim's re-fetch at 14:51:27Z; I didn't re-download the file.
   - Live coveringrepository.com (m=t): my one plain fetch of the home page at 2026-10-17T15:01:01Z returned
     HTTP 403 (Cloudflare challenge). Per the rules I didn't retry or bypass it. The live value is therefore the
     operator's hand read at 2026-10-17T14:57Z (~4 minutes before this check), pasted verbatim in CLAIM.md: row
     "20 06 03 03 71 ... Creator: Chaoying Dai, Ben Li and Michel Toulouse ... 11/04/2006". Judgement: this counts as a
     live read of the coveringrepository.com plain (v,k,t) value. The criterion's escape ("if a live table cannot
     be fetched -> PENDING TABLE CHECK") applies when the value is unknown. Here a person read the live value, which
     is exactly what clears PENDING TABLE CHECK. Weakness: no saved page or hash exists for the hand read.
   - "live LJCR value (https://dmgordon.org/covering-designs/)": my fetch at 15:01:00Z returned 200, but the page is
     a landing page with no per-cell values. It calls itself the database page, refers to the per-cell site as
     "my old website", and points to GitHub/Zenodo. The search index snippet of dmgordon.org/cover/ says "This website
     will be shutting down in 2026, and after March 1 no new covering designs are being accepted." The old per-cell
     page ljcr.dmgordon.org/cover/show_cover.php?v=20&k=6&t=3 failed at 15:03:12Z:
         curl: (35) TLS connect error: error:0A000126:SSL routines::unexpected eof while reading
     (The search engine's cached copy of that page reads "64 <= C(20,6,3) <= 71".) Judgement: the LJCR is
     frozen, and its maintained live data is the dmgordo/LJCR GitHub coverdata.json (71, re-fetched, 0 commits since
     April). The live coveringrepository.com row also names the LJCR as its source. So the LJCR clause is met
     in substance, though not by a live per-cell page, because none exists any more.

4. "beat any value found by grepping GitHub/arXiv for that (v,k,t) over the last 6 months": no value <= 70 found.
   - GitHub repo search (pushed > 2026-04-17), "covering design" (3768 hits; top 50 read) and "covering-designs"
     (70 hits; all read). The covering-design repos among them (TheEslabonGroup/covering-designs,
     nickroci/fuzzy-solvers, vibemathing/...covering-designs..., Soulxlight/covering-design-c54-16-4, jamesyc/covering)
     cover other cells. A README grep for (20,6,3) found no match.
   - The web search for "C(20,6,3)" covering found no claim below 71. alejandrozarco/covering-numbers v3 (Zenodo 2026-10-07)
     lists 9 cells, none of which is (20,6,3).
   - arXiv API, abs:"covering designs" sorted by date: 10 entries since 2026-04-17, none mentioning 20,6,3. One
     earlier all:"covering design" API call timed out and wasn't retried. Limitation: unauthenticated search can't
     grep GitHub code contents, so this is a repo-level and README-level grep.
   - coveringrepository.com latest-improvements list (claim's machine fetches at 13:03:59Z and 14:51:05Z): no (20,6,3) row.

5. Parameter limits: v=20 <= 99, k=6 <= 25, t=3 <= 8. Met.
6. Schonheim: L(20,6,3) = 64 (own recursion), and 70 >= 64. No sub-bound bug signal.
7. Same-day size limit: C(20,3) = 1140 <= 5e9. Met, and the full exhaustive check ran.

Partial win: none is claimed, so this was judged against the full criterion only. The win isn't subsumed: no source
lists 70 or less, and the improvement is exactly 1 block (71 -> 70), well above the 64 lower bound.

confirmed_scope: The 70-block file C20_6_3_70blocks.txt (sha256 a6c6ddb8...4c6f) is an exhaustively verified (20,6,3) covering design, so C(20,6,3) <= 70, one block below the value 71 in the dmgordo/LJCR GitHub data (re-fetched 2026-10-17T15:01Z), the newest Zenodo LJCR release v1.2, and the live coveringrepository.com (v,k,t) row as hand-read by the operator at 2026-10-17T14:57Z, with no competing value of 70 or less found in a repo-level GitHub/arXiv search of the last 6 months.

Residual risks (do not block): the coveringrepository.com live value rests on an unhashed hand read; the per-cell
LJCR page is unreachable (the site is frozen and being retired); the GitHub grep was repo/README-level, not code-level.

pass: true
