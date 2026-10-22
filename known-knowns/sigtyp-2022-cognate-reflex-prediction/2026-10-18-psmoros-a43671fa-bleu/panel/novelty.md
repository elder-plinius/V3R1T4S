(Saved by the main session from the subagent's returned text at 2026-10-18T22:54:04Z; the LA NOVELTY skeptic subagent (Opus 5.5, model opus, agent ab7b0ed63fea38a49) could not write a file named like a report. Text verbatim below.)

# Panel: NOVELTY skeptic, cell LA (aggregate A_BLEU over proportions 0.10-0.50), session 2026-10-18-1758

context: subagent (Claude Code Agent tool, fresh context, model opus = Opus 5.5)
role: NOVELTY
start: 2026-10-18T22:10:21Z (date -u)
end: 2026-10-18T22:22:14Z (date -u)
material: the claim package (claim/), kit RULES.md, TROPHY_CASE.md (local copy), and the web, reached only through the shared fetch helper with lens LA-NOVELTY. Before each request the helper re-read the session stop list and every stops file changed in the last 24 h. github.com and api.github.com were never requested (both host-stopped). This lens added no stop-list line: every request returned 200, 400 or 500, and none returned 401, 403, 405, 429, 503 or a challenge page.

## 1. Status source (official results files): one plain GET each

status_source: https://raw.githubusercontent.com/sigtyp/ST2022/main/results/results-surprise-0.10.json HTTP 200 fetched 2026-10-18T22:11:14Z
status_source: https://raw.githubusercontent.com/sigtyp/ST2022/main/results/results-surprise-0.20.json HTTP 200 fetched 2026-10-18T22:11:14Z
status_source: https://raw.githubusercontent.com/sigtyp/ST2022/main/results/results-surprise-0.30.json HTTP 200 fetched 2026-10-18T22:11:14Z
status_source: https://raw.githubusercontent.com/sigtyp/ST2022/main/results/results-surprise-0.40.json HTTP 200 fetched 2026-10-18T22:11:15Z
status_source: https://raw.githubusercontent.com/sigtyp/ST2022/main/results/results-surprise-0.50.json HTTP 200 fetched 2026-10-18T22:11:15Z

I compared each fetched file with claim/official/results/results-surprise-P.json (pinned commit 03094435) using shasum and cmp. Real output:
```
0.10 fetched=e00f22badafe95729d8a079f0563175528fa63248c62bf7a41de2f43029f4c75 pinned=e00f22badafe95729d8a079f0563175528fa63248c62bf7a41de2f43029f4c75 cmp=IDENTICAL
0.20 fetched=80f2b01eb4e6f6c2130749f7eff149dc95fd4c59044ec9b8b22836b74dbbf519 pinned=80f2b01eb4e6f6c2130749f7eff149dc95fd4c59044ec9b8b22836b74dbbf519 cmp=IDENTICAL
0.30 fetched=cca55c5fffa730c29ef578f022741f3a0378ca333e5a20493e23e2d400792563 pinned=cca55c5fffa730c29ef578f022741f3a0378ca333e5a20493e23e2d400792563 cmp=IDENTICAL
0.40 fetched=699aacbc94cb6d8289bb2685ac73f87e2cf72a1df22cee89a6cf8b7e1501ee86 pinned=699aacbc94cb6d8289bb2685ac73f87e2cf72a1df22cee89a6cf8b7e1501ee86 cmp=IDENTICAL
0.50 fetched=3a8e79f9e686a4835f6bd0948529838b4ebb38ef2f02e05d39dfa73389a014f3 pinned=3a8e79f9e686a4835f6bd0948529838b4ebb38ef2f02e05d39dfa73389a014f3 cmp=IDENTICAL
```
The pinned hashes also match the claim's MANIFEST.sha256 lines for official/results. Result: all five official tables on main are byte-identical to the pinned copy (PROVED-HERE).

Extra check: I fetched https://raw.githubusercontent.com/sigtyp/ST2022/main/README.md once (HTTP 200, 2026-10-18T22:21:00Z, sha256 51bf43bf61e21f55e07bf056ca2960a6eb49dbcfc830d06ee6855dbca7493d63). Section 4.2 still holds only the meta-evaluation rank table for the nine original systems, with no later system. The "Aggregate" column there averages ranks, not scores.

I could not contact github.com itself (stopped), so I re-checked the repository page and commit oid only inside the claim's own scout copy. claim/scout/st2022_repo_page.html (sha256 fec88fad967728c78c42ddd0b95a19a6bb6be63f7e8c9b4fd6ef77d314cc1012) contains "currentOid":"03094435cba4293ce0eea383036cab78499ad50d" twice. That copy was fetched by the main session at 18:07:41Z, not by me.

Judgement: the status is established, so this is not a PENDING STATUS CHECK.

## 2. The bar: every official system's five-proportion aggregate

Each system's BLEU "total" (index 3) was taken from the fetched files and summed left to right over 0.10, 0.20, 0.30, 0.40, 0.50, then divided by 5. A Python 3.13 script in my scratch folder did this. Real output:
```
Mockingbird-I1           A_BLEU(l-to-r)=0.6015772270938825 builtin=0.6015772270938825
Mockingbird-N1-B         A_BLEU(l-to-r)=0.5739708839607733 builtin=0.5739708839607733
Mockingbird-N1-A         A_BLEU(l-to-r)=0.5724785535357948 builtin=0.5724785535357947
Mockingbird-N1-C         A_BLEU(l-to-r)=0.5513710848081363 builtin=0.5513710848081363
Baseline-Baseline-SVM    A_BLEU(l-to-r)=0.5406672591377498 builtin=0.5406672591377498
CEoT-Extalign-RF         A_BLEU(l-to-r)=0.5227742615104686 builtin=0.5227742615104686
Baseline-Baseline        A_BLEU(l-to-r)=0.5061025005292537 builtin=0.5061025005292537
CrossLingference-Julia   A_BLEU(l-to-r)=0.4565210644206756 builtin=0.4565210644206757
Leipzig-Transformer      A_BLEU(l-to-r)=0.4259328183325886 builtin=0.4259328183325886
Mockingbird-N2           A_BLEU(l-to-r)=0.11487912591146295 builtin=0.11487912591146295   (0.10 only; 0 at the other four P)
```
Mockingbird-I1's per-P totals are 0.6633184488563897, 0.632633947442519, 0.6058548112827981, 0.5723601982335171 and 0.5337187296541888, with 10 families at each P. Recomputing the family means from the per-family entries changes only the last digit (for example 0.6633184488563896), which is a summation-order effect and does not matter here. The bar is 0.6015772270938825 (NUMERICAL, PROVED-HERE). It equals the bar in the instructions and in PREREG, and no official system beats it.

The task paper's Table 3 agrees with these totals to 4 decimals at every P (List et al. 2022, https://aclanthology.org/2022.sigtyp-1.7.pdf, HTTP 200, 22:18:29Z). Mockingbird-I1's rows there read BLEU 0.6633, 0.6326, 0.6059, 0.5724 and 0.5337.

## 3. The claimed value (sanity check only; reproduction belongs to the REPRODUCE skeptic)

I ran `python3 checker/check_q15.py . object` from claim/ with a stock Python 3.13, at nice 5 under a 2400 s alarm. Real output:
```
1. 0.10 Mockingbird-I1 mean BLEU recomputed 0.6633184488563897, official 0.6633184488563897: EXACT
2. 0.10 object mean BLEU 0.7183395130131847 over 4029 items
1. 0.20 Mockingbird-I1 mean BLEU recomputed 0.632633947442519, official 0.632633947442519: EXACT
2. 0.20 object mean BLEU 0.6960719420978517 over 7887 items
1. 0.30 Mockingbird-I1 mean BLEU recomputed 0.6058548112827981, official 0.6058548112827981: EXACT
2. 0.30 object mean BLEU 0.6721728449836378 over 11586 items
1. 0.40 Mockingbird-I1 mean BLEU recomputed 0.5723601982335171, official 0.5723601982335171: EXACT
2. 0.40 object mean BLEU 0.6533966833715619 over 14992 items
1. 0.50 Mockingbird-I1 mean BLEU recomputed 0.5337187296541888, official 0.5337187296541888: EXACT
2. 0.50 object mean BLEU 0.624905217712099 over 18101 items
3. Mockingbird-I1 A_BLEU from the official totals 0.6015772270938825 (PREREG 0.6015772270938825): EQUAL
4. object A_BLEU 0.6729772402356671 (claimed 0.6729772402356671): EQUAL
   margin vs Mockingbird-I1 0.071400013142 (higher is better)
5. rebuilt official-format files equal to the frozen ones: 50 of 50
PASS
```
Margin, computed by me: A - bar = 0.07140001314178457. A minus the next official system (Mockingbird-N1-B) = 0.09900635627489374. The checker step does not judge whether the training was clean; the REPRODUCE and CRITERION skeptics cover that.

## 4. Literature, last 24 months (2024-10-18 to 2026-10-18), plus older work that could move the bar

Every request below was one GET through the helper.

Citation graph and keyword search (OpenAlex):
- Task paper record (doi 10.18653/v1/2022.sigtyp-1.7 -> W4287889593, cited_by_count 15; 200, 22:12:26Z). Works citing it (200, 22:12:31Z, count 15). Inside the window there are three: FeVeT (ORE 2025-06-30), the Sci. Rep. 2024-12-24 Panoan-Takanan paper, and an OSF 2024-05-24 Trans-New Guinea chapter.
- Works citing Cognate Transformer, FeVeT or Blum and List 2023 (200, 22:12:40Z, count 9): bioRxiv 2026 BetaReconstruct (proteins), Lexibank 2 (ORE 2025), ICCIES 2025 (IEEE), Sci. Data 2024, and older items.
- Searches from 2024-10-01: "reflex prediction" (200, 22:12:41Z, count 21), cognate reflex (200, 22:12:41Z, count 617, nearly all off-topic), SIGTYP shared task cognate (200, 22:18:34Z, count 12), "phonological reconstruction" (200, 22:18:35Z, count 179), "SIGTYP 2022" (200, 22:21:24Z, count 2), and "cognate sets" predict missing words phonetic (200, 22:21:25Z, count 10).
- I read the OpenAlex abstracts of every on-topic hit (200, 22:12:58Z and 22:19:13Z). None reports reflex prediction on the ST2022 surprise families except FeVeT:
  - Sci. Rep. 2024: Shipibo-Konibo field test of 206 predictions.
  - Diachronica 2024: Gyalrongic, mutual implicative entropy.
  - LChange 2026 / arXiv 2026-02: irregular-word detection, 85% accuracy.
  - arXiv 2609.05262 and 2512.01713: phylogeny and borrowing detection.
  - SIGTYP 2025 "Beyond cognacy": phylogenetics.
  - ICCIES 2025: proto-language NMT, no ST2022.
  - AFTS 2026: PIE reconstruction. I read its PDF at https://arhivzatehnickenauke.com/article/1055/pdf/download (200, 22:21:38Z). It only cites the Mockingbird paper and has no ST2022 scores.

ACL Anthology:
- The full bibliography with abstracts, https://aclanthology.org/anthology+abstracts.bib.gz (200, 22:14:35Z, 42574037 bytes, sha256 83b1de6e...; 131708 entries; 12135 from 2024, 14931 from 2025, 10822 from 2026; it includes 2024.sigtyp-1, 2025.sigtyp-1, 2026.sigtyp-main and 2026.lchange-1).
- A raw-text search over all years for reflex prediction, cognate reflex, reflexes, SIGTYP 2022, ST2022, Mockingbird and cognate prediction found, for 2024-2026, only 2024.lrec-main.762 "Improved Neural Protoform Reconstruction via Reflex Prediction" (May 2024, outside the window; WikiHan/Rom protoform data, not ST2022), plus false positives ("reflexive" and similar).
- I listed every title in the SIGTYP 2024/2025/2026 and LChange 2024/2026 volumes by hand: no reflex-prediction paper.

Other sources:
- Europe PMC search (200, 22:13:10Z, 7 hits): only FeVeT, Sci. Rep. 2024 and Open Problems (2023) are on topic.
- Zenodo: two searches with size=100 returned 400 (page-size validation, not a block). I re-ran them with size=25 (200, 22:13:26Z, 13 hits; 200, 22:13:28Z). On topic: the FeVeT supplement (2025-08-12), the 2022 task release and a 2022 CEoT submission. The Romance "CFR" resources (2026) are not ST2022.
- arXiv API, export.arxiv.org (200, 22:18:12Z, totalResults 6): nothing after 2024-03-27. arxiv.org itself is host-stopped and was not requested.
- Crossref, query cognate reflex prediction from 2024-10-01 (200, 22:18:13Z): only FeVeT, its two peer reviews and Sci. Rep. 2024 are on topic.
- OpenReview search "reflex prediction" (200, 22:20:43Z, count 6): only Cognate Transformer (2023) and the LREC 2024 protoform paper.

Known partial reporters, re-verified from the primary sources:
- FeVeT, Wientzek 2025, Open Research Europe 5:174. The PDF https://open-research-europe.ec.europa.eu/articles/5-174/pdf (200, 22:14:03Z) reads "[version 1 ...] Latest published: 30 Jun 2025 ... Last updated: 23 SEP 2025" and states "the model is evaluated on the 10%, 30%, and 50% test proportions of the surprise data". Its Table 3 gives ED, NED and BC only; there is no BLEU anywhere in the paper.
  - The supplement Zenodo 16813907 is v1.1 of 2025-08-12, and versions/latest is the same record (200, 22:14:39Z and 22:15:58Z). Its zip (200, 22:15:07Z, sha256 e82909eb...) holds reflex files tagged 0.10, 0.30 and 0.50 only (14 each; none at 0.20 or 0.40).
  - results/s2s_reflex_finetuned_avg.txt has columns ED, NED, B3_F1: 0.10 = 0.7836, 0.205, 0.8041; 0.30 = 0.9589, 0.2397, 0.7232; 0.50 = 1.1111, 0.2825, 0.673. The raw README on main (200, 22:14:40Z) adds no proportions.
  - So FeVeT gives no BLEU and no five-proportion aggregate (KNOWN, confirmed).
- Cognate Transformer, Akavarapu and Bhattacharya, EMNLP 2023. The PDF https://aclanthology.org/2023.emnlp-main.423.pdf (200, 22:14:38Z) says "Among these, we only report for the test proportions 0.1, 0.3, and 0.5". Its reflex table is ED/NED/BC only (CogTran-small 0.1: 0.8966/0.2421/0.7823; 0.3: 1.1235/0.2919/0.6954; 0.5: 1.2786/0.3332/0.6477). The raw README on main (200, 22:19:12Z) adds nothing. No BLEU and no aggregate (KNOWN, confirmed).
- The 2022 system papers, read so that no published value is missed:
  - Mockingbird, https://aclanthology.org/2022.sigtyp-1.9.pdf: totals at 0.10 and 0.50 only, I1 BLEU 0.66 and 0.53, matching the official table.
  - Leipzig-Transformer, https://aclanthology.org/2022.sigtyp-1.10.pdf: per-family values at all five P, below Mockingbird; official aggregate 0.4259328183325886.
  - CrossLingference, https://aclanthology.org/2022.sigtyp-1.8.pdf, and CEoT, https://aclanthology.org/2022.sigtyp-1.11.pdf: no BLEU tables.
  - Blum and List 2023, https://aclanthology.org/2023.sigtyp-1.6.pdf: other datasets, no ST2022 reflex scores.
  - All five PDFs returned 200 between 22:18:30Z and 22:18:33Z.

Context only (NUMERICAL; not the LA metric and not a five-proportion aggregate): at the three proportions FeVeT reports, the claimed system's NED and BCFS from the claim table are better than FeVeT's fine-tuned values:
- 0.10: NED 0.2002 vs 0.205, BCFS 0.8092 vs 0.8041
- 0.30: NED 0.2320 vs 0.2397, BCFS 0.7348 vs 0.7232
- 0.50: NED 0.2683 vs 0.2825, BCFS 0.6905 vs 0.673

Items I could not read (residual risk, HEURISTIC: judged low):
- (a) J.-M. List 2026, "Computer-Assisted Comparison of South-East Asian Languages", a Knowledge Commons book-chapter preprint. Its API record returned 200 (22:19:22Z). The file endpoint returned a 60-second signed storage link instead of the PDF (200, 22:19:29Z). I did not request it again (one GET per resource), and the signed link is not quoted here.
  - Its abstract is an overview of cognate and correspondence detection, reconstruction and borrowing detection for SE Asian languages. A ten-family ST2022 aggregate would include four non-SE-Asian families, so it is unlikely to appear there.
- (b) Full texts on arxiv.org (stopped host) for arXiv 2609.05262 and 2512.01713. Their abstracts are about phylogeny and borrowing detection.
- (c) IEEE Xplore (challenge-stopped) for ICCIES 2025. Its OpenAlex abstract covers proto-language NMT only.
- (d) Semantic Scholar and dblp (stopped) and Google Scholar (not used, bot policy).

## 5. Crowd and own record

- TROPHY_CASE.md (local copy, 100 lines) has no match for sigtyp, ST2022, cognate, reflex, Q15, quarry or mockingbird. Its families are graphs, codes, matrix multiplication, Lehmer, VNN-COMP, RobustBench and cipher commitments.
- The V3R1T4S pull-request list lives on github.com, which is host-stopped this session (429 at 2026-10-18T21:48:35Z), so I could not check it live.
- The only evidence is the claim's own scout copy from 18:07:43Z. claim/scout/v3r1t4s_pulls_search.html (sha256 7d506467...) embeds "openCount":0 and "closedCount":0 for the keyword search (sigtyp, cognate, reflex, ST2022, Mockingbird, FeVeT, proto-form). claim/scout/v3r1t4s_pulls_all.html embeds openCount 123, closedCount 297, totalCount 420.
- Any pull request opened after 18:07:43Z is unverified.

## 6. Best published aggregate

- No paper or repository published since the shared task reports family-mean scores on the SIGTYP 2022 surprise families at all five proportions, other than the official results.
- FeVeT (2025) and Cognate Transformer (2023) report 0.10, 0.30 and 0.50 only, and give no BLEU at all.
- The best published aggregate is therefore Mockingbird-I1's A_BLEU = 0.6015772270938825, the left-to-right mean of its official results-surprise-P.json BLEU totals. The source is the official ST2022 results (https://raw.githubusercontent.com/sigtyp/ST2022/main/results/, byte-identical to pinned commit 03094435) and Table 3 of the task paper.
- No official system beats it (next: Mockingbird-N1-B 0.5739708839607733).

## Verdict

novelty: the claimed A_BLEU 0.6729772402356671 (classifier/PRIMARY, cell LA) is higher than every known published five-proportion aggregate. The bar is Mockingbird-I1's 0.6015772270938825, beaten by 0.07140001314178457; this is a strict win, not a tie. The status source is established: all five official results files are byte-identical on main. Caveats: the pull-request list could not be checked live (github.com is stopped), and the four unread items in section 4 remain. This panel judges novelty only. Whether the run was clean (training data, the disclosed use of development-family rows, gate selection) belongs to the REPRODUCE and CRITERION skeptics.

Credits: the shared task and data by J.-M. List, E. Vylomova, R. Forkel, N. Hill and R. Cotterell (https://aclanthology.org/2022.sigtyp-1.7, https://github.com/sigtyp/ST2022). Mockingbird by C. Kirov, R. Sproat and A. Gutkin (https://aclanthology.org/2022.sigtyp-1.9). FeVeT by T. Wientzek (https://doi.org/10.12688/openreseurope.20647.1). Cognate Transformer by V.S.D.S. Mahesh Akavarapu and A. Bhattacharya (https://aclanthology.org/2023.emnlp-main.423).

injection_suspected: none

pass: true