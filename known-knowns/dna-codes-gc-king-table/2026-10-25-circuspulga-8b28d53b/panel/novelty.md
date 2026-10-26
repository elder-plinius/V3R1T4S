# NOVELTY review: A_4^GC(19,14,9) >= 44 (claim/CLAIM.md)
context: fresh knowledgeWork subagent started for the NOVELTY role, given only claim/ and the step-6 NOVELTY instruction, with its own private scratch folder and public web access

## Status source (one honest request, no retries)
- URL: https://rambutan.umassmed.edu/king/dnacodes.html (from claim/CLAIM.md)
- fetched: 2026-10-25T10:28:03Z (11:28 CET), one plain curl, HTTP 200, 18096 bytes
- sha256 25d6e9f88262fbb07c95841225cb3202aa29eb31f7f72d24b43e9c595bdb18c5, identical to claim/data/dnacodes.html
- page says "Last updated June 23, 2010"
- live value, GC-only table "Lower bounds for A4^GC(n,d,w)", row 19, column d=14: `38` with superscript `v` (VNS from [MS] or [MS2]); no '.' or ':' after it, so it is not marked optimal
- for reference, the GC,RC table gives 18 at (19,14) and 39 at (19,13). That 39 belongs to a different cell and a different constraint set, and it does not apply here
- injection_suspected: no. The page has no text addressed to agents; its only HTML comments are two commented-out links to codes/LinearGC.txt and codes/LinearGCRC.txt

## References in the page that cover n=19, d=14
Superscript v points to [MS] Montemanni-Smith 2008 and [MS2] Montemanni-Smith MIC 2009. [SAMP] (in press when the page was updated) is cited for n<=20 and also for 20<=n<=30, 14<=d<=n. None of them gives more than 38 at this cell; details below.

## Literature checked (value found for A_4^GC(19,14,9))
- Montemanni, Smith, Koul 2014, "Three metaheuristics for the construction of constant GC-content DNA codes", LNMS 6:167-175 (orlabanalytics.ca PDF, HTTP 200). I rendered Table 1 (A4^GC) and read it: n=19, d=14 gives V = 38^N (new VNS runs) and B = 33 (prior literature, including Smith et al. 2011). The highest value here is 38.
- Aboluion 2011 PhD thesis, "The construction of DNA codes using a computer algebra system" (pure.southwales.ac.uk PDF, HTTP 200). Table 10.70, "Best known lower bounds for max_w A4^GC(n,d,w)", n=19, d=14 gives 38 (m2), and that is a maximum over w. Table 10.66 (linear codes) gives 14 at n=19, d=14. Table 10.72 (GC,RC, max_w) gives 18. The highest value is 38.
- arXiv 1903.03535 (Galois-supplemented cyclic codes, GC-content; PDF read): its results cover A4^GC,RC for n=17, 13 and 29 only. Nothing for (19,14).
- arXiv 2108.02033 (reversible G^k-codes; PDF read): Tables 1-9 cover lengths 16, 24, 32, 36, 48, 56, 60, 64 and 72. Nothing for n=19.
- Limbachiya-Gupta(-Aggarwal) 2018, altruistic algorithm (IEEE Comm. Letters): per the abstract and later citing work (PMC10067891), it covers 4<=n<=13 only, with an extra no-runlength constraint. Later KMVO, DMVO and MFOS papers cover n<=13. Nothing for n=19.
- Limbachiya-Rao-Gupta survey, arXiv 1607.00266 (PDF read): its GC,RC tables give 18 at (19,14), and its other table is RC-only. It has no GC-only value above 38.
- Searched 2024-2026 (arXiv 2409.06519, arXiv 2510.01750, JSAIT 2025 Benerjee-Banerjee, ISIT 2026 composite and staple codes): from abstracts and snippets, none reports A4^GC at n=19.
- Repo record: TROPHY_CASE.md (raw GitHub, HTTP 200) has no DNA or GC entry. Open pull requests (GitHub API, 363 open across 4 pages) include several dna-codes-gc(-rc)-king-table claims, but none for (19,14) or for n=19.
- SAMP 2011 (Smith, Aboluion, Montemanni, Perkins, Discrete Math. 311:1207-1219) full text: PENDING STATUS CHECK. ScienceDirect answered one curl with 403, and I did not retry. Indirect evidence: MSK 2014's B row includes Smith et al. 2011 and gives 33, and Aboluion's thesis, on which SAMP is based, gives 38.
- Aboluion-Smith-Perkins 2012 (Discrete Math. 312:1062-1075, GC,RC) full text: PENDING STATUS CHECK. The DOI resolved to a ScienceDirect redirect stub, and CORE answered 403. Indirect evidence: it concerns GC,RC, and the thesis and the 2016 survey give GC,RC(19,14)=18.
- MS2 2009 (MIC 2009) full text: PENDING STATUS CHECK. I found no public copy. Indirect evidence: King's table already credits v=38 to [MS]/[MS2], and the expanded 2014 version reads 38.

## Verdict
novelty: The claimed 44 is strictly greater than the live table entry (38) and than every value I found for A_4^GC(19,14,9) in the literature I read (highest 38: MSK 2014 Table 1 and Aboluion 2011 Table 10.70). It is not a tie. The 44-word object passes an independent quick check (44 distinct words, GC=9 in all, minimum Hamming distance 14). Three full texts (SAMP 2011, ASP 2012, MS2 2009) remain PENDING STATUS CHECK. Read compilations by the same authors cover their values, and those compilations report at most 38.
pass: true
