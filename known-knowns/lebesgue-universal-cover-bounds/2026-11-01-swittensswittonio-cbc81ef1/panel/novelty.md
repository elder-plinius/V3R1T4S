context: subagent
# Panel NOVELTY (replay of Zeng 0.834 certificate, bank p1)

## Status page (single fetch, no retry)
- URL: https://teorth.github.io/optimizationproblems/constants/13b.html, fetched once at about 2026-11-01T00:59Z (`date -u` just before: Sun Nov 1 00:59:47 UTC 2026), HTTP ok.
- Value: best lower bound 0.832 [BS2005]; best upper bound 0.8440935944 [Gib2018]. No 2026 entry (0.8344, 0.834, 0.833). The page is stale; no replay of Zeng is listed there.

## What is being claimed
An interval-arithmetic replay of all 6,746,392 leaves of Zeng's certificate (arXiv:2609.01284, Zenodo 10.5281/zenodo.20528351) plus defects D1-D8 (claim/ANALYSIS.md section 4). It is a replay, not a new bound, so the "trivial edits of a published object" test applies to the replay note: is an equal-or-better public replay of this certificate already out?

## Searches (all read-only; counts from command output)
1. Tao optimizationproblems (teorth/optimizationproblems), 289 PRs listed with gh pr list --state all; title filter lebesgue|cover|13b|zeng|mishra|xie|universal|0.83|reuleaux gives only #266 (unrelated covering system), #223 (open, 12 Oct: adds Mishra 0.8344 to 13b only, cited arXiv:2608.30538; no Zeng; maintainer asked for rebase/split on 26 Oct) and #215 (convex worm cover, other constant). `gh search prs/issues` for "Zeng", "0.834", "Reuleaux", "2609.01284", "20528351": 0 hits. Replay PRs exist (#235, #242, #292) but for other constants (C49, C82/C86, 1c/86a).
2. This repo (elder-plinius/V3R1T4S): 844 PRs listed, open and closed; title filter lebesgue|universal|zeng|mishra|xie|reuleaux: no lebesgue/universal-cover PR (hits are covering designs/codes, unrelated). `gh search prs` for lebesgue, "universal cover", mishra: 0; "zeng": #612 (merged, unrelated NT benchmark). TROPHY_CASE.md (31,082 bytes): no line matching lebesgue|cover|zeng|mishra|replay. known-knowns/ (27 folders listed): no lebesgue entry. Only code hit: known-unknowns/record-tables/lebesgue-universal-cover-bounds.md (the bank record, which defines p1; it lists no replay).
3. GitHub code/repo search ("2609.01284", "20528351", "lebesgue universal cover"): hits that cite Zeng are catalogues (MColbrook/AIM problem 262: abstract-level note, no replay; anghel4d/broadside-observer: arXiv card; ehijano/rss_fetch: feed xml) and tejasvi/lebesgue-cover-bound (own 0.8366 certificate, Lean + second verifier for its own certificates; its paper cites Zeng [Zen26] only to say Zeng proves the same B3/B5 root-box estimate; releases v8, v9 list no Zeng replay). Also checked: vince-gonzalez/certified-covers (Aug 2026; Sprague/Gibbs/BBG ladder areas, no Zeng), Sheldon-Anderson/...-certificate (Brass-Sharifi 0.832 replay package, pushed 2026-07-08, predates Zeng's arXiv), Hatchett newmattock 0.83474 (Zenodo 10.5281/zenodo.22135010, own Arb checker, 461,208 leaves; a different certificate). No fork or release asset found replaying Zeng.
4. Zenodo API (record 20528351: title "Verification artifact for a certified 0.834 lower bound...", created 2026-06-03, modified 2026-06-16, 1 version, 16 downloads). Searches (lebesgue universal cover, "exact hierarchy", Zeng replay, title:Lebesgue AND title:universal): only Gonzalez 21715685 (classical ladder areas), Yang 21349948 (3D Makeev truncations), Hatchett; nothing replays Zeng. The Zenodo free-text search is noisy; absence is not proof.
5. arXiv/web: web_search for Zeng replay / independent verification / error: only Zeng's paper, Xie 2606.04458 (v2 titled "Reproducible Certificate for the Brass-Sharifi bound"; v4 certified bound 0.833), Mishra 2608.30538, Arman et al 2512.04023, 2607.27227, 2609.32931 (escape path duality); none is a replay of Zeng. arxiv.org/abs/2609.01284v2 returned HTTP 404 (single GET), so only v1 exists as of the check. The arXiv export API returned HTTP 429 once; not retried, so the arXiv full-text/listing sweep rests on web_search only. Forum/blog: no hit.
6. Defects D1-D8 (hash-prefix mismatch, missing perturbation-bridge code, non-enclosing float radii, arb NaN dropping a sample point, unchecked stored fields, unchecked rotation index, float padding, wording): no issue, PR, comment or note reporting any of them was found on Tao's repo, this repo, or the pages above.

## Comparison with published objects
No published or open replay of Zeng's certificate exists in what I could reach. Neighbouring objects (Hatchett Arb replay of its own 0.83474, tejasvi's verified 0.8366, Sheldon-Anderson's BS replay, Xie's reproducible certificate) check other certificates, so none of them ties or beats the claim for this cell (replay of Zeng). The claim adds no new bound and does not need to beat 0.8344/0.8366; its novelty is only the replay and defects.

## Caveats (not hedging the verdict, scope of what was searched)
- GitHub code search and Zenodo search are incomplete and noisy; the arXiv API was blocked (429), not retried.
- Late arrivals could appear after 2026-11-01T01:05Z.
- The bound itself is not a record (0.834 < 0.8344 < 0.8366); claim must stay a p1 replay.

verdict: no equal-or-better public replay of Zeng's certificate found; defects D1-D8 unreported in public places searched.
pass: true
