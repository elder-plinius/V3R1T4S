context: subagent

# NOVELTY panel (claim: Gilbreath p2, local depths over 1.5e15..1.6e15)

## Status source (one plain request, UA "V3R1T4S research agent")
URL: https://www.lactamme.polytechnique.fr/Mosaic/descripteurs/GilbreathConjecture.01.Ang.html
Fetched 2026-11-01T10:58:54Z (local clock, UTC), HTTP 200, Last-Modified Wed, 12 Aug 2026 13:39:45 GMT, 100184 bytes.
sha256 = 5641cdd6fc098132d1a51efc0f9889d22882ecd11d1b537325906dc9f8fdae2f -> identical to the sha256 in the-record-we-beat/record.md.
Page content (text extracted): title "Verification up to 1.5x10^15"; G(Pi(10^14))=693, G(Pi(10^15))=800, G(Pi(1.2125*10^15))=811, last line "Verification up to 1.5x10^15 (03/18/2026)"; 57600 G(Pi(x)) values grouped in ten ranges, last 1.4x10^15-1.5x10^15 (averaged groups of 768 only, not per-block depths). Relative records listed: G(Pi(1.6931x10^15))=969 and entries at 1686994940955803 (924) and 1693182318746371 (1132/969): these lie ABOVE 1.6e15, outside the claim range; the only listed number in 1.5e15..1.6e15 is none (regex for 15xxxxxxxxxxxxxx/16xxxxxxxxxxxxxx finds only 1686994940955803 and 1693182318746371). No mention of github/zenodo on the page. No local per-block depths or block data for 1.5e15-1.6e15 on the page; no verification above 1.5e15.
The record cells are unchanged from the claim's snapshot.

## Literature / code (last 24 months)
- arXiv:2510.06688 (Plouffe, abs page fetched once, HTTP 200): verification up to 10^14 only, no data above.
- github.com/yygotm/gilbreath-verification (HTTP 200; README fetched; releases API: empty list): verification up to 10^13 (G=635); README states frontier is 10^14 / 1.5e15 and that Plouffe/Colonna logs are unpublished. Nothing for 1.5e15..1.6e15.
- api.github.com repository search "gilbreath conjecture" (one request, HTTP 200): 13 repos, most recent Sunrise689/math-cluster-verification (first 10^6 primes), vibemathing/* (candidate research stubs), ayham-naseer/gilbreath-left-extensions, tobiascanavesi/gilbreath-conjecture, MarkAfanasiev/Maths-En-Jeans, yyl-20020115/GilbreathConjecture, others older. None targets 1.5e15; Sunrise689 releases: empty list, README confirms 10^6 range.
- OEIS search "gilbreath" (one request, HTTP 200, 89 hits): A036262 comment still cites Odlyzko 10^13; nothing on 1.5e15..1.6e15 local depths.
- Not run: forums, further GitHub code searches (limited to the stated one request each).

## Repo checks
- repo/TROPHY_CASE.md and V3R1T4S/TROPHY_CASE.md: no match for "gilbreath" (grep -i).
- repo/known-knowns/: no match (grep -ril gilbreath); directory listing has no Gilbreath entry.
- repo/bank/targets.json: contains the target (id gilbreath-conjecture-verification-beyond-1-5e15) with partial win p2 as quoted in claim/BANK_TARGET.md.
- gh pr list --repo elder-plinius/V3R1T4S --state all --search gilbreath --limit 50 -> []; --search "1.5e15" -> []; also searches "Gilbreath", "1600000000000000" -> []. Full listing (846 PRs, state all) filtered by title for "gilbreath": none.

## Judgement
- No public equal-or-prior result for this exact object (per-block local depths with overlap 1536 and max depth over contiguous primes 1.500000000000013e15..1.6000018708e15, plus a row-1280 cleanliness check) found. Colonna's page publishes only averaged G values up to 1.5e15 and a few relative records above 1.69e15; Plouffe stops at 1e14.
- Not a trivial edit of a published object: no published per-block data exist to edit. Max depth 783 is not comparable to Colonna's G values (G counts from p_1=2) and the claim says so.
- Claim scope: explicitly p2 (extension step), explicitly NOT a new Gilbreath bound, not Colonna's G values, not the success criterion. It does not claim more than p2.
- Caveat for the main agent: novelty here is "first public per-block local-depth data for this range" only; the claim does not beat the bank's main success criterion, and the page cannot show whether Colonna holds unpublished equivalents (the page says data are unpublished).

pass: true
