# Novelty skeptic: digital (11,24,17)-net over F_2

context: subagent (fresh context, NOVELTY seat of the three-skeptic panel). Inputs: the original claim workspace (not shipped) package (relative paths below), one live MinT fetch, web and GitHub searches.

## 1. Live status fetch (one GET, no retries)

- URL: http://mint.sbg.ac.at/query.php?b=2&m=24&s=17&p=smt
- Time: 2026-10-31 12:09-12:10 EDT (16:09-16:10 UTC), via the WebFetch tool. HTTP OK, page title "MinT - Best Known (t, 24, 17)-Nets in Base 2".
- Values quoted from the page:
  - "(13, 24, 17)-Net over F2 — Constructive and digital": "Digital (13, 24, 17)-net over F2, using s-reduction based on digital (13, 24, 24)-net over F2, using a shift-net". Constructive and digital: **t = 13**.
  - "(8, 24, 17)-Net in Base 2 — Lower bound on t": "There is no (7, 24, 17)-net in base 2" (s-reduction, then 2x m-reduction, then OOA LP bound). Lower bound: **t >= 8**.
  - The per-cell query page does not print a separate digital-existence entry. The scout's single fetch of the cd/ed table (the MinT cd/ed table snapshot (not shipped; see the-record-we-beat/TABLE_SNAPSHOT.md)) and the original table record (not shipped; see the-record-we-beat/TABLE_SNAPSHOT.md) show Digital (existence) t = 13 for this cell. Its cd/bd table (the MinT cd/bd table snapshot (not shipped; see the-record-we-beat/TABLE_SNAPSHOT.md)) shows m=24, s=17 as "13-8", which matches my live fetch.
- Claim t = 11 < 13 (strictly better by 2) and 11 >= 8 (above the lower bound, so not a bug signal).

## 2. Neighbouring cells (MinT constructive digital, base 2, from the MinT cd/bd table snapshot (not shipped; see the-record-we-beat/TABLE_SNAPSHOT.md), consistent with the live cell)

- (m,s) = (24,16): 13; (24,18): 13; (23,17): 12; (25,17): 13; (22,17): 11; (24,24): 13 (shift net, the published parent of the current record).
- Trivial edits of published objects cannot reach t = 11 at (24,17):
  - s-reduction (deletion of coordinates) from any published (t,24,s'>=17) net gives t >= 13.
  - m-reduction from (t,25,17) gives t >= 13.
  - The (11,22,17) net cannot be lifted to m = 24 at the same t; no valid rule increases m at fixed t and s.
  - Relabelling, symmetry, or row operations that preserve t leave t at 13.
  - Base reduction from F_4: MinT's closure already includes this and gives 13.
  - MinT's propagation closure is exactly what yields 13, so no combination of these edits gives 11.
- Seeding: PREREG.md and the header of object/net_F2_t11_m24_s17.txt say the object comes from a randomized greedy (Gilbert-Varshamov-style) construction (the original note said gvgreedy4 and seeds 101/102/103; a later rebuild identifies gvgreedy2 with seed 101 as the submitted object source). No published net is named as a seed, and nothing indicates one. Even if it had been seeded from the 13-net, it beats every edit-reachable value by 2.
- Side effect (not claimed here): m-reduction gives a digital (11,23,17)-net, below MinT's 12; s-reduction gives (11,24,16) and (11,24,15), below 13 and 12 (at s = 14 MinT already has 11).

## 3. Literature and code search (last 24 months, plus older for anything already giving t <= 11)

Web searches (2026-10-31):
- "new digital (t,m,s)-nets base 2 improved t-values MinT computer search 2025 2026"
- "arXiv 2025 digital nets over F_2 generator matrices smaller quality parameter t than MinT"
- "digital (11,24,17)-net" / "(11, 24, 17)-net"
- "digital nets base 2 new constructions improved t-values tables 2024 2025 arXiv MinT"
- "ordered orthogonal arrays NRT codes new binary parameters (t,m,s)-nets 2025"
- "digital nets quality parameter new record binary computer search SAT 2026"
- "github digital net generator matrices t-value search binary m=24 s=17"

Hits:
- arXiv:2501.13659 "Reduced digital nets" (2025) and "Column reduced digital nets" (Numer. Algorithms 2025). Both give upper bounds on t for row- or column-reduced nets; t never drops below that of the parent net. No new (t,m,s) parameters.
- arXiv:2606.05482 (2026), on optimal diaphony / L2 discrepancy of order-2 sequences: not t-value records.
- MATRIS / ordered covering arrays (2025): covering codes, not nets.
- Binary NRT-LCD codes (arXiv:2302.02037): not net parameter records.
- Older references (MinT shift nets m <= 51 in Schurer's thesis; the Lawrence-Mahalanabis-Mullen-Schmid code construction; Niederreiter-Xing; Edel-Bierbrauer net embeddings; Clayman-Mullen GV) are already inside MinT and are what produce 13.
  - Spot check of the code construction: t <= 11 at m = 24 would need d >= 14, h = 6 and n >= 103, i.e. a binary [103,79,14] code, far beyond known codes.
- GitHub: jointpoints/tms-nets (Sobol/Niederreiter generator, no records), lgruen/netsearch ((0,m,2) min-distance search), LatNet Builder (t-value tooling). None gives a binary (t<=11,24,17) net.
- No paper, preprint, table or repository found that gives a digital (t,24,17)-net over F_2 with t <= 12.

## 4. V3R1T4S repo (historical repository snapshot at f3b19b4, plus GitHub web)

- TROPHY_CASE.md: no entry mentioning digital nets, MinT or (t,m,s).
- known-knowns/: no digital-net / MinT folder. The only grep hits are codetables-binary-linear entries, which are unrelated linear codes.
- known-unknowns/record-tables/mint-digital-nets-lower-t.md: the target statement, open as of 2026-10-30, with no listed solutions.
- GitHub PR searches on github.com/elder-plinius/V3R1T4S/pulls with is:pr (open and closed) for "net", "mint" and "digital":
  - No PR claims a digital (t,m,s)-net or a MinT cell.
  - The hits are unrelated: sorting networks, codetables GF(9), cap sets, spherical codes, Thomson, LABS.
- Release assets: the fetch of the releases page timed out (single try, not retried). The repo tree and PR list show nothing related.

## 5. Independent sanity run (not my seat's job, recorded for the panel)

- sha256 of object/net_F2_t11_m24_s17.txt = c3c441c5...dfd54618, matching the original reproduction notes (not shipped; see verify-it-yourself/RECEIPTS.md).
- The claim's C checker (verify-it-yourself/netcheck_b.c), recompiled in a scratch dir, gives "PASS q=2 m=24 s=17 t=11 k=13 compositions_reached=67863915" in 20.6 s.
- Validity proper is the other skeptics' call.

## Verdict

The live MinT constructive-digital value for (b,m,s) = (2,24,17) is 13 (lower bound 8). The claimed t = 11 is strictly smaller, not a tie. No published construction or propagation (deletion, restriction, m- or s-reduction, relabelling, symmetry) of a known net reaches t <= 12 in this cell. No literature from 2008 to 2026, no code, no TROPHY_CASE / known-knowns entry and no PR gives it. The object is not seeded from a published net. Caveat: the releases page could not be fetched (timeout, not retried).

pass: true
