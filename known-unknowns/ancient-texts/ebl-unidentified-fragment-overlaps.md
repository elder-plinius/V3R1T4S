# Cuneiform: fragment-to-fragment overlaps among UNIDENTIFIED eBL fragments (new witnesses of unknown compositions, 'indirect joins')

🏺 **Ancient texts and fragments** · harvest (many cells or partial wins within reach) · tractability ★★★☆☆ · compute: laptop-hours · open as of 2026-10-08

## The problem

The electronic Babylonian Library (eBL) public API reported 38,530 transliterated fragments and 625,844 lines on 2026-10-08 (/api/statistics). The existing bank target ebl-fragment-identification matches unassigned fragments against KNOWN compositions (eBL chapters). This target is the complementary, harder case: two or more fragments that are each unidentified (genre 'OTHER:Uncertain' or no genre, no joins, no chapter manuscript link) but overlap each other textually, i.e. duplicate witnesses of a composition nobody has reconstructed yet. Simonjetz et al. (LREC-COLING 2024) formalised fragment matching and reported Precision@3 on 965 artificial fragments against chapters only, noting that all-pairs fragment-to-fragment matching 'does not seem feasible at this point'. eBL's own ngram-matcher (GitHub) exposes the baseline. Status 2026-10-08 (vetter): open-ended ongoing work; the public API query endpoint (/api/fragments/query?genre=OTHER:Uncertain) returned 200 with 1,144 records, fragment records (/api/fragments/{id}) are public GET (HEAD returns 405) and expose joins, genres, references, uncuratedReferences, notes and a sign-name 'signs' field; the in-platform matcher endpoint /api/fragments/{id}/match returns 403 to the public, but eBL's ngram-matcher Python library (github.com/ElectronicBabylonianLiterature/ngram-matcher, last commit 2025-11-18) reads only the public API (https://www.ebl.lmu.de/api/) and needs no credentials, so it is the executable baseline. Simonjetz et al. (LREC-COLING 2024) state that all-pairs matching of fragments 'does not seem feasible at this point'.

## What counts as a win

At least 1 PAIR of eBL fragments meeting ALL of: (a) at verification time both public records have joins == [], no corpus-chapter manuscript link (checked against the manuscripts lists of all chapters via /api/texts), no reference, uncuratedReference or note naming a composition, and genre absent or 'OTHER:Uncertain'; (b) neither fragment aligns to any eBL chapter or Oracc edition under the ebl-fragment-identification thresholds (otherwise it belongs to that target); (c) the unidentified set searched is defined by a published deterministic rule and its museum-number list is frozen (hash) before alignment; after normalising readings to sign names (the public 'signs' field), the two fragments share an alignment of at least 2 consecutive lines or at least 12 consecutive signs with at most 10% mismatches; (d) the alignment score has p < 1e-4 against a null that aligns the fragment to all other fragments of the frozen set with line order shuffled, Bonferroni-corrected over all pairs tested; (e) the shared text is not a formula recurring in at least 5 unrelated compositions (omen protases, incantation refrains, lexical entries, colophons, year names), verified by corpus-wide counting over the eBL corpus and Oracc; (f) the pair is not in the top 10 returned for either fragment by eBL's public ngram-matcher library (TF-IDF overlap strategy, default n-values) when the verifier runs it over the same frozen set; (g) the two museum numbers are not the same physical tablet (different collection or non-adjoining provenance, and no published direct join recorded). Claim as 'candidate indirect join'; CONFIRMED only when the eBL team or an Assyriologist accepts it. Records (a) and the library run (f) are re-executed live immediately before claiming.

## Partial wins

- **p1:** A pair meeting (a), (b), (c), (d), (e), (g) that DOES appear in the public ngram-matcher top 10 for one fragment but is recorded nowhere in either eBL record (no join, chapter link, reference, uncuratedReference or note) and not in the publications the records cite.
- **p2:** A cluster of at least 3 unidentified fragments that pairwise meet (a)-(g) and whose union, aligned, yields a composite of at least 5 consecutive lines with each line attested on at least 2 fragments.

## How a win is checked

The verifier fetches both fragment records via the public eBL API (timestamp recorded), checks joins/genres/references/uncuratedReferences/notes and the chapter manuscript lists, recomputes the alignment with independent code on the public sign-name field, re-runs the shuffled-line null over the frozen set (hash checked), pip-installs the public ngram-matcher library and runs it for both fragments over the same set, checks formulaicity against the eBL corpus and Oracc, and confirms the fragments are not a recorded direct join. Throttled API fetching of a 1,000-2,000 fragment set plus alignment fits in under an hour on a 10-core Mac.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://www.ebl.lmu.de/api/statistics>

## Sources

- <https://www.ebl.lmu.de/api/statistics>
- <https://www.ebl.lmu.de/api/fragments/K.1>
- <https://www.ebl.lmu.de/api/fragments/query?genre=OTHER%3AUncertain&paginationIndex=0>
- <https://github.com/ElectronicBabylonianLiterature/ngram-matcher>
- <https://aclanthology.org/2024.lrec-main.1197.pdf>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Pull the unidentified set via the query endpoint (throttled), normalise readings to sign names, index sign 4-grams with inverted lists and only align pairs sharing 2+ rare 4-grams (rare = document frequency < 20).
- Weight shared n-grams by inverse corpus frequency so that lexical-list and omen formulae do not dominate (the eBL matcher's TF-IDF variant is the baseline to beat).
- Use physical metadata (collection, script, period, dimensions) only as a tie-breaker, never as evidence; Kuyunjik (K., Sm., Rm., DT) fragments are the densest source of duplicates.
- Build the shuffled-line null once per fragment and reuse it across all its pair tests; report Bonferroni over the number of pairs actually scored.
- Cluster pairwise hits into connected components to attempt the p2 multi-fragment composite.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Formulaic genres (Summa alu protases, Maqlu refrains, Hh lexical entries, Ur III year names, colophons) produce long shared sign runs that are NOT shared compositions; enforce (e) by corpus-wide counting.
- Two museum numbers can be the same tablet (direct join already published but unrecorded in eBL, or re-numbered); check cited publications and the eBL 'joins' field live.
- Sign-reading normalisation errors (homophone indices, broken-sign brackets, x signs) can both create and hide matches; use sign names and treat damaged signs as wildcards with a penalty.
- Some records have restricted authorizedScopes; use only public data, throttle requests and respect eBL terms of use.
- The in-platform matcher endpoint (/api/fragments/{id}/match) is not public (403); only the open-source ngram-matcher library run on public API data counts as the baseline gate.
- The public 'signs' field encodes editorial restorations (bracketed text in the record's ATF) exactly like attested signs, so a shared run can be an editor's restoration matched against itself. Derive attested positions from each record's text tokens (the enclosureType field marks BROKEN_AWAY parts) and count only runs attested on both fragments. Found 2026-10-16: re-aligning 1,109 raw-sign overlaps on attested signs kept 123, and the strongest raw hit (VAT.18937 | VAT.25937, 71 shared signs) had 42 restored signs on one side.
- 'Genre absent' in eBL mostly means uncurated, and the uncurated set is dominated by administrative and legal records. Identifying labels live in references[].notes (e.g. 'Income of barley') and in 'dossiers' (e.g. 'Babylon N1'), not in 'notes' or 'genres'; read those fields for clause (a), and treat any archive edition as a fail. Of 808 records of candidate pairs checked on 2026-10-16, only 37 were clean on all fields.
- Clause (d) as written (p < 1e-4 after Bonferroni over all pairs tested, by line-shuffled simulation) cannot be reached by simulation: with thousands of pairs the level is below 1e-8 and a pooled null of 10^4-10^5 shuffles floors at about 1e-4. State a reachable level or accept a pre-registered parametric (Gumbel) tail; 'beats every control' remains checkable.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/ancient-texts/ebl-unidentified-fragment-overlaps.md
```

Already set up? Say `run V3R1T4S on ebl-unidentified-fragment-overlaps`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `ebl-unidentified-fragment-overlaps`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
