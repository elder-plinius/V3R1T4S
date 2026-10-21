# Greek literary papyri: identify DCLP 'unidentified' fragments as witnesses of known works via open-corpus text matching

🏺 **Ancient texts and fragments** · harvest (many cells or partial wins within reach) · tractability ★★☆☆☆ · compute: laptop-hours · open as of 2026-10-08

## The problem

The Digital Corpus of Literary Papyri (DCLP, papyri.info; open EpiDoc XML in github.com/papyri/idp.data, DCLP/ folder) held 14,845 records at commit 67e8445 (2026-10-08), 2,276 of them with a transcription (<ab>). Re-count by the vetter on 2026-10-08: the 'unidentified' label lives in the work-level metadata, i.e. <title type="main" level="m"> elements carrying a trismegistos.org/authorwork ref that read 'Opus incertum' (about 80 transcribed records), <author>/<surname> = 'Anonymus' (about 70), <term type="overview"> 'unknown work' (4) and principal-edition titles naming unknown works; roughly 150-250 transcribed records are genuinely unidentified-work records (the stocker's 1,941 included 'unknown' inventory numbers and provenances and is not the pool). Many of these are Herculaneum (PHerc.) opera incerta of Philodemus or Demetrius Laco, i.e. lost works absent from every corpus, so the realistic pool is smaller still. Open Greek corpora exist in full text (OpenGreekAndLatin/First1KGreek, PerseusDL/canonical-greekLit; Latin: PerseusDL/canonical-latinLit), so identification can be attempted mechanically by aligning the supplement-free letters of each unidentified fragment against every open text, which scholars still do by hand (e.g. the 2024 re-identification of P.Oxy. 2258 'Unidentified Fragment 11' as Demosthenes). Status 2026-10-08 (vetter): no systematic machine identification campaign published (searches found only writer-identification, character-detection, dating and stylometric authorship work); idp.data actively maintained (last commit 2026-10-08); raw.githubusercontent.com and papyri.info/dclp return 200 to plain curl; a sparse clone of DCLP/ takes about a minute.

## What counts as a win

At least 1 DCLP record meeting ALL of: (a) at the recorded idp.data commit, every work-level author/title element of the record (the <author>/<surname> elements and the <title type="main" level="m"> elements that carry a trismegistos.org/authorwork ref, plus <term type="overview">) reads Opus incertum / Adespota / Anonymus / unidentified / unknown, and no <bibl>, <note>, <head> reference title, <term> or <change> entry in the record names the matched author or work; (b) the alignment uses ONLY letters outside editorial supplements ([ ]) and outside <supplied>/<gap> elements, with underdotted (uncertain) letters excluded from the count; (c) the fragment's stripped letters align to one passage of one open-corpus text (First1KGreek, canonical-greekLit or canonical-latinLit; repository commit hash recorded) over at least 12 consecutive legible letters spanning at least 2 papyrus lines with at most 1 letter mismatch, and the line-break positions are consistent with a plausible column width (constant +/-3 letters per line); (d) the alignment score has p < 1e-4 against a null formed by aligning the same fragment to the whole open corpus with line order shuffled, Bonferroni-corrected over all fragments searched; (e) the matched passage is not a formula or quotation attested in at least 5 distinct open-corpus works (Homeric formulae, LXX/NT verses, proverbs, gnomic sentences), verified by exhaustive corpus-wide counting; (f) the identification is not already recorded in the papyri.info HTML/XML record, in the Trismegistos/LDAB authorwork entry linked from the record's <idno type="LDAB">, or in the editions cited in the record's <head>, all re-fetched live immediately before claiming. Claim as 'candidate identification'; CONFIRMED only when a papyrologist or the papyri.info editorial board accepts it.

## Partial wins

- **p1:** A DCLP record meeting (a), (b), (d), (e), (f) whose alignment covers 8-11 consecutive legible letters over at least 2 lines with 0 mismatches, where the matched 8+ letter string occurs exactly once in the entire open corpus (rarity verified by exhaustive search) and the line-break constraint of (c) holds.

## How a win is checked

The verifier sparse-clones idp.data (DCLP/ only, about 1 minute) at the claimed commit, checks the record's work-level elements per (a) with independent code, strips supplements/gaps/underdots with independent code, re-runs the alignment of the claimed fragment against the open corpus at the recorded commit, re-runs the shuffled-line null, counts corpus-wide occurrences of the matched string, and re-fetches the papyri.info record and the LDAB authorwork entry live to confirm no prior identification. Under one hour on a 10-core Mac.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://github.com/papyri/idp.data>

## Sources

- <https://github.com/papyri/idp.data>
- <https://raw.githubusercontent.com/papyri/idp.data/master/DCLP/64/64136.xml>
- <https://github.com/OpenGreekAndLatin/First1KGreek>
- <https://github.com/PerseusDL/canonical-greekLit>
- <https://papyri.info/dclp>
- <https://github.com/PerseusDL/canonical-latinLit>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Index both open corpora as accent-stripped, lower-cased letter n-grams (n=6..8) and run seed-and-extend alignment of each unidentified fragment's supplement-free letters; score by length and corpus rarity.
- Treat papyrus line breaks as constraints: a correct match must place line ends at a near-constant letter count per line, which prunes chance hits.
- Prioritise fragments whose DCLP title says 'prose' or 'hexameter' with 3+ lines and few lacunae; verse fragments can be matched on metrical position as well.
- Run the identified transcribed records blind (identification fields hidden, supplements stripped) as a calibration set to tune thresholds before claiming any new identification (calibration is a prerequisite, not a win).
- Cross-check candidate hits against the record's own <bibl> and the TM authorwork field via the papyri.info JSON/HTML page before claiming.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Editorial supplements in [ ] were often restored FROM a suspected source text: matching on them is circular. Strip all bracketed text and also dotted (uncertain) letters when counting.
- Homeric formulae, LXX/NT verses, proverbs, school exercises and gnomic sentences recur across many works; condition (e) must be enforced by corpus-wide counting.
- TLG is not open and First1KGreek is incomplete: absence of a match proves nothing, and a match to a fragmentary author (e.g. Menander) may reflect a quotation in a later author rather than the primary work.
- Some 'unidentified' DCLP metadata is stale: the record may have been identified in a later edition (P.Oxy. re-editions, BKT) or in Trismegistos without idp.data being updated. Check live before claiming.
- Leiden-convention markup (dots, underdots, brackets, line numbers) must be parsed carefully; a naive strip can glue letters across lacunae and produce fake 12-letter runs.
- 'unknown'/'incertum' also appears in inventory numbers, provenances and editorial notes: only the work-level author/title elements (with trismegistos authorwork ref) and the overview term define the pool.
- Lost works (Philodemus/Demetrius Laco opera incerta, lost tragedies, novels) can never match an open corpus; a null result on them is expected and is not evidence of anything.
- Clause (a) read literally leaves a pool of 6 transcribed records, not 150-250 (counted 2026-10-16 at idp.data commit f0fcec2): most 'Opus incertum' records carry a named author (Menander, Archilochus, Philodemus, Demetrius Laco, 'Paulus?'), and a named author fails (a). 656 further transcribed records carry no work-level element at all (vacuous (a)); by title about half of those are magical, medical, liturgical and school texts. Say whether 'unknown work of a named author' is in scope, and whether records with no work-level element are.
- Clause (c)'s junction requirement ('12 consecutive legible letters spanning at least 2 papyrus lines') can only be met when both lines are preserved at the junction. 63% of DCLP's transcribed, identified fragments (651 of 1,028 whose author is in the open corpora) lose both line ends and cannot form such a run whatever their text; a Homer papyrus with 423 legible letters (BKT 9 120) scores zero under the clause and 22 letters at Iliad without it. A lacuna-bridging rule (letters on two lines of one passage, with a lacuna of unknown length between) is needed for the typical fragment.
- Twelve letters with one mismatch is chance-level against the open corpora (170 M Greek letters): 254 of 662 unidentified-or-unlabelled records reach it, and order-2 Markov controls of the same line lengths reach 16-17. Length does no discriminating work; what does is clause (e) (distinct works) and a within-line-shuffle or Markov null. Even then the survivors are quotations (Psalms, Homer), recipe parallels (Galen, De compositione medicamentorum, already cited in the records' re-editions), liturgical formulae and philosophical commonplaces, not witnesses.
- Clause (d)'s null ('line order shuffled') re-creates the real junction of two lines about once in n-1 controls, so a one-junction hit ties its own null and can never reach p < 1e-4 under it (13 of 13 shortlisted parallels tied or lost on 2026-10-16). Pre-register a within-line letter shuffle and a Markov text of the same line pattern instead, and state a reachable level: with 400 controls per record the floor is 1/401, far above 1e-4 / (number of fragments).
- Counting <supplied> letters as legible manufactures criterion-grade hits: on 2026-10-16, 110 of 662 records reached 12 letters only through restored text (29 of them with windows of 20 or more). The stripping rule must also keep <supplied>, <unclear>, <ex> and counted <gap> positions as wildcards (so the corpus text stays aligned through them) rather than deleting them, and treat gaps of unknown extent as hard breaks; deleting restored letters glues the surrounding text and creates fake runs.
- The live checks of clause (f) are not reachable with an honest client: papyri.info serves an Anubis proof-of-work challenge to plain curl (2026-10-16) and trismegistos.org answered plain GETs with connection failures and a 403 challenge page. A verifier must read the idp.data XML (the same data) and leave the HTML and LDAB pages to a human; say so in the verification method.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/ancient-texts/dclp-unidentified-literary-papyri.md
```

Already set up? Say `run V3R1T4S on dclp-unidentified-literary-papyri`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `dclp-unidentified-literary-papyri`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
