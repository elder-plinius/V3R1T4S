# NOVELTY skeptic verdict

context: subagent (Claude Code Agent tool, opus, fresh context, saw only claim/)
verdict time (date -u): 2026-11-09T14:12:09Z
injection_suspected: none

## Claim under review

CLAIM.md, target `meunier-stable-kneser-odd-s-small-n`: Meunier's conjecture holds for (k,s) = (3,5) at
n = 17 and n = 22, i.e. chi(KG(17,3)_{5-stab}) = 7 and chi(KG(22,3)_{5-stab}) = 12. The claim says these
are the only open n for the pair. object/ also holds certificates for n = 18..21, which the claim says are
not new. The question here: were n = 17 and n = 22 really open before this claim, and is any other n open
for (3,5)?

## 1. Status source, fetched once

- URL: https://arxiv.org/abs/2607.12912
- fetched 2026-11-09T13:47:02Z (UTC), HTTP 200, 39,165 bytes,
  sha256 7166ca68e255537395da8799628e57d0a0ce75ad702ede5a6b5c0db965c7c6cb. This is the same hash as the
  claimant's fetch in table/status_record.md, so the page has not changed since then.
- What it shows: v1 only (Tue, 14 Jul 2026), Wei-Chia Chen, Alex Parker, Shira Zerbib, "The chromatic number
  of 3-stable Kneser graphs". The abstract says the conjecture "was previously proven for all even s, for
  s >= 4 and large enough n, and for k=2", and that the paper proves "the cases s=3 and n large enough, or
  k=s=3". Nothing on the page concerns s = 5.

## 2. Primary sources read

### arXiv 2607.12912v1 (full PDF, fetched 13:47:11Z, HTTP 200, sha256 26e36de04041a674e7cbb7b7a37d58356f9fb2afbc0ced353ae73f4b8e52aa5f)
- Theorem 1.2, stated as Jonsson's result: "For all k >= 2, s >= 4, and n >= 2s(k-1)+2,
  chi(KG(n,k)_{s-stable}) = n - sk + s", with the remark "this manuscript is no longer available online".
  For (3,5) this would cover n >= 22.
- Also cited: Meunier proved n = sk+1; Chen proved even s (Thm 1.3); Daneshpajouh, Meunier and Mizrahi proved k = 2
  (Thm 1.4).
- New results: Thm 1.5 (s = 3, k >= 4, n >= k^3+3k^2) and Thm 1.6 (k = s = 3, n >= 9). The only computer
  checks (Appendix 2, CaDiCaL through PySAT, no proofs shipped) are for (n,3,3) with 9 <= n <= 14. No s = 5 case
  is computed. The paper's own method cannot reach (3,5): Thm 1.10 needs n >= 4s+3 = 23, and an analogue
  of Lemma 4.1 for s = 5 would need the chromatic number of the (5,5,4)-vector-stable graph, which no
  source gives. Section 6 (the topological approach) proves only k = 2.

### Jonsson, "On the chromatic number of generalized stable Kneser graphs" (manuscript, 2012)
- Fetched once from the Wayback URL given in table/status_record.md
  (http://web.archive.org/web/20240602163626id_/https://people.kth.se/~jakobj/doc/submitted/stablekneser.pdf),
  2026-11-09T13:47:35Z, HTTP 200, sha256 ee44606776142780c7fe1a129e07a9fe72195ac2d56e4a5c76bd4a47d3092eaa
  (same as the claim's record), 7 pages.
- Version check: the Wayback CDX index has captures of this PDF from 2017-08-29, 2020-02-10, 2022-01-20,
  2022-12-08, 2024-06-02 and 2025-04-01, and every one has payload digest 3TZAHGJUXVUHEKP4L7FVLE7K4KGJZFEO.
  The base32 SHA-1 of my copy is the same value. As far as the archive shows, the manuscript has one version.
- Jonsson's "s-sparse in Z_n" for integer s means that every cyclic gap between consecutive elements is
  >= s. That is the same as s-stable in 2607.12912.
- Theorem 1.3: for real s, integer t with 2 <= t <= s/2, d = floor(tn/s) and n >= ks,
  chi(SG^s_{n,k})/n >= chi(SG^t_{d,k})/d. For s = 5 the only allowed t is 2. With Schrijver's
  chi(SG^2_{d,3}) = d - 4 this gives chi(KG(n,3)_{5-stab}) >= ceil(n(d-4)/d), where d = floor(2n/5).
- Corollary 1.6: exact value for s >= 4 once n >= (s/2^q)(s(k-1)+eps) with q = floor(log2(s/2)) and
  eps = 1 here. For s = 5, k = 3 that threshold is (5/2)(11) = 27.5. The formula 2s(k-1)+2 used in 2607.12912 is
  the same threshold only when s is a power of 2 (then s/2^q = 2). For s = 5 it is a misquote.
- The manuscript has no other result for odd s. Its section 1.1 reports Meunier's computer checks for
  (r,s) = (2,3) only.
- I read the proof of Theorem 1.3 (Lemma 2.1: t-sparse subsets of S = {floor(in/d)} are s-sparse in Z_n;
  Lemma 2.2: alpha(G(n,S)) = d; then a double count) and found no gap. I also checked both lemmas by brute
  force for k = 3, s = 5, t = 2 and every n from 15 to 30, including n = 17 and n = 22. Both hold.
- What Theorem 1.3 gives for (3,5), next to the conjectured n - 10:

| n | d | bound ceil(n(d-4)/d) | n - 10 | settled by Thm 1.3? |
|---|---|---|---|---|
| 15 | 6 | 5 | 5 | yes (also trivial: n = sk) |
| 16 | 6 | 6 | 6 | yes (also Meunier Prop. 1) |
| 17 | 6 | 6 | 7 | **no** |
| 18 | 7 | 8 | 8 | yes |
| 19 | 7 | 9 | 9 | yes |
| 20 | 8 | 10 | 10 | yes |
| 21 | 8 | 11 | 11 | yes |
| 22 | 8 | 11 | 12 | **no** |
| 23..40 | | = n - 10 | | yes (checked by script) |

- Every n >= 23, in closed form: the bound reaches n - 10 iff n - 4n/d > n - 11, i.e. iff 4n < 11d. Write
  n = 5m + r with 0 <= r <= 4. Then d = 2m + [r >= 3], and the condition becomes 4r - 11[r >= 3] < 2m. It fails
  only when r = 0 and m = 0; r = 1 and m <= 2; r = 2 and m <= 4; r = 3 and m = 0; or r = 4 and m <= 2. So it fails
  only for n in {0, 1, 2, 3, 4, 6, 7, 9, 11, 12, 14, 17, 22}. For n >= 15 the only failures are n = 17 and n = 22.
  Theorem 1.3 therefore settles every n >= 23, and n = 18..21.

### Meunier, "The chromatic number of almost stable Kneser hypergraphs" (JCTA 118 (2011) 1820-1828)
- arXiv 0912.4748v1 (fetched 13:54:53Z, HTTP 200, sha256 b031d91278dac2dcefa0ee7aff5ba0a51ae79065e22ebbb51be9be8ca77a50c2): this 2009 version has neither the
  s-stable graph conjecture nor the n = sk+1 result. Its computer checks cover only Conjecture 1, which is
  the r-stable hypergraph case.
- The publisher PDF (ScienceDirect) answered HTTP 403, and the HAL copy (hal-00676479) answered with a bot challenge. I
  did not retry either. The author-hosted later version, cermics.enpc.fr/~meuniefr/StableKneserHypergraphs.pdf,
  is in the Wayback Machine. I fetched the 2025-09-29 capture once (13:56:50Z, HTTP 200, sha256 2eaa5009cf2e5e717143ed452061933edb60e0089cd7fb762ed0b50131517f7e).
  Its abstract matches the JCTA abstract on Semantic Scholar word for word, so I treat it as the
  journal text. It has:
  - Proposition 1: chi(KG(ks+1,k)_{s-stab}) = s+1. For (3,5) this is n = 16, value 6.
  - Conjecture 2 (Meunier's conjecture).
  - Computer checks of Conjecture 2 (lpsolve) for (k,r,s) = (2,2,3) n <= 9; (2,2,4) n <= 10;
    (3,2,3) n <= 11; (3,2,4) n <= 13; (4,2,3) n <= 14; (4,2,4) n <= 17; plus the hypergraph cases (2,3,4), (3,3,4),
    (2,3,5) and (2,4,5). None of these is a graph case with s = 5. Neither Jonsson (2012), who mentions only Meunier's
    (r,s) = (2,3) checks, nor Daneshpajouh (2025), who mentions only r in {3,4}, reports any (r,s) = (2,5) computation.

### Peng-An Chen 2015 (JGT 79:233-248) and Chen 2017 (arXiv 1711.06621)
- The 2015 full text is paywalled and I did not read it. Its abstract (OpenAlex) says Meunier's conjecture
  holds for "r a power of 2 and s a multiple of r", which for graphs (r = 2) means even s only. Every
  secondary source agrees (2607.12912, 2509.22026, 1904.08219, 1711.06621, the 2025 box-complex survey).
  An even-s theorem bounds s = 5 only through subgraphs: SG^6 is a subgraph of SG^5, giving chi >= n - 12.
- 1711.06621 settles the almost s-stable graphs (linear distance). Those are supergraphs of the s-stable
  graphs, so the result gives only an upper bound here.

### Other results that could bound n = 17 or n = 22 from below
- Daneshpajouh and Osztenyi (arXiv 1904.08219; Discrete Math 2021): the exact chromatic number only for vectors
  (s_1..s_{k-1}, s_k) with s_k in {1,2}, which are supergraphs of the 5-stable graph. The best subgraph
  of KG(n,3)_{5-stab} it reaches is KG(n-3,3)_{(5,5,2)}, which gives chi >= n - 13.
- Daneshpajouh, arXiv 2509.22026 (Sep 2025): Theorem 8 needs min entry m = 2 or all of s_1..s_{k-1} even, so
  (5,5,x) is out of scope. (6,6,5) is a subgraph and gives only n - 12. Theorem 9 is for k = 2 only. The new results are
  for hypergraphs with r >= 3. The paper says the graph case with odd s is known only from Jonsson.
- Frick, arXiv 1710.09434 (IMRN 2020): proves results for r > 6s-6 (prime power r) and for 3-stable with
  r >= 4. For r = 2 it treats only almost 2-stable sets. Nothing for r = 2, s = 5.
- Arana, Haxell, Kaiser, Stehlik, arXiv 2610.17884 (Oct 2026): G-stable Kneser graphs, with lower bounds for G
  a disjoint union of cycles. The s-stable graph is G = C_n^{s-1}, which is not of that kind. No s = 5 values.
- Osztenyi, Gradus 2021 (doi 10.47833/2021.3.csc.006, PDF fetched, sha256 f3beb448ed88ba77d7986543802af89e9775e9d9b36fa617227922104dc9e194):
  <s,t>-stable with t < s. These are supergraphs, so the result gives only upper bounds.
- Alishahi and Taherkhani, arXiv 1612.07462: even s only.
- Liu, Turevskii, Wang, Yan, arXiv 2606.24863: Meunier's formula only for uniformity q >= gamma*n, i.e.
  hypergraphs, not graphs.
- Daneshpajouh and Meunier, box-complex survey (arXiv 2307.00299; Discrete Math 2025): gives the status as
  Jonsson for s >= 4 with large n, Chen for even s, and k = 2. Nothing on small odd-s cases.
- Zerbib, UW seminar abstract (2026-09-23 talk): the same results as 2607.12912. Nothing on s = 5.
- Trivial edits of known results: KG(n,3)_{5-stab} is an induced subgraph of KG(n+1,3)_{5-stab}, so chi
  is monotone in n. That gives chi(17) >= chi(16) = 6 and chi(22) >= chi(21) = 11, one short in both cases.
  The fractional bound n/k (vertex-transitive graph, Talbot's EKR) gives 6 and 8. The clique number is
  floor(n/3) = 5 and 7. Jonsson's averaging cannot do better than in the table: any S whose 2-sparse
  3-subsets are 5-stable has consecutive gap pairs summing to >= 5, so |S| <= floor(2n/5), and alpha(G(n,S))
  >= |S| always (the |S| translates that contain 0). No edit of a published result reaches 7 at n = 17 or
  12 at n = 22.

## 3. Searches (literature, citations, code, this repo)

- arXiv API, abs:"stable Kneser", newest first, 13:57:19Z: 22 results. The relevant ones are the papers
  listed above. The others (Hamiltonicity 2401.15198, 2401.01681, 2511.12553; neighbourhood complexes
  2512.09674; automorphisms; shifts) do not concern chromatic numbers for s = 5.
- arXiv API, abs:"s-stable", 13:59:04Z: 29 results, nothing new for this problem.
- arXiv API, Kneser AND chromatic, submitted 2024-11-09 to 2026-11-09, 13:59:10Z: 25 results. I read the
  abstracts of the ones that could matter (2606.24863, 2508.18487, 2510.27689, 2412.20001, 2511.12553).
  None gives s-stable chromatic numbers for odd s.
- Two more arXiv queries (abs:Meunier AND abs:Kneser; Schrijver AND stable, last 24 months) got HTTP 429 at
  14:05:30Z and 14:06:01Z. I reran them after a pause (section 3a). These are literature searches, not the
  status fetch, which I made only once.
- Citations of Meunier 2011: OpenAlex (cites:W2046584470, 41 works) and Semantic Scholar (56). The ones from
  the last 24 months are 2610.17884, 2607.12912, 2606.24863, 2509.22026, the box-complex survey, and two
  unrelated surveys. All are covered above.
- Citations of 2607.12912: Semantic Scholar returned an empty list (14:07:44Z), and OpenAlex shows
  cited_by_count 0. Citations of Chen 2015 (13) and of Daneshpajouh-Osztenyi (5) in OpenAlex: nothing new.
- Web search (two queries on s-stable or 5-stable Kneser chromatic number with computer/SAT): only the
  papers above, the Jonsson PDF and the UW seminar page.
- GitHub (read-only): code search for "stable Kneser", "s-stable" kneser, meunier kneser, kneser drat and
  kneser cadical returned 0 hits. "5-stable" gave 30 unrelated hits. "kneser" gave 100 hits, mostly n-gram
  smoothing. Repo search for "stable kneser", "schrijver graph", "meunier conjecture" and "kneser
  chromatic" returned 0. Repo search for "kneser" returned 100 results. The only recent graph-colouring
  one (condeDeveloper/kneser, 2026-11-07) is about ordinary Kneser graphs and has no releases. I found no code,
  data or release asset with a 5-stable colouring value.
- V3R1T4S (default branch main, HEAD 850aa9c, 2026-11-08), read-only:
  - `gh pr list --state all --limit 1100 --search "kneser OR meunier OR stable"`: 22 PRs, none on Kneser
    graphs (stable-marriage claims and other targets). Searches for "kneser", "meunier", the target id,
    "chromatic" and "Jonsson" returned no PR on this target. Issue search for kneser/meunier: 0.
  - TROPHY_CASE.md (raw, sha256 83af764f5a6551a5a27bbb135324931659bda04e60b66a2c0e711b991b356113): no entry for this target.
  - known-knowns/: 31 entries, none for this target or for Kneser graphs.
  - The bank entry (known-unknowns/graphs-games-automata/meunier-stable-kneser-odd-s-small-n.md, last changed in
    commit f3b19b4, 2026-10-30) is discussed in sections 5 and 6.

### 3a. arXiv queries rerun after the HTTP 429
- abs:Meunier AND abs:Kneser, 14:08:19Z, HTTP 200: 13 results. Besides the papers above, the list has general
  Kneser hypergraph lower bounds (1302.5394, 1704.07052, 1705.00223, 1605.06701, 2002.01748, 2009.10676),
  2110.00718 and 2312.17130. I read the abstracts of 1302.5394, 2002.01748 and 2009.10676 (14:02:49Z) and of
  1704.07052, 1605.06701 and 2312.17130 (14:09:41Z). For 1705.00223 (categorical products) and 2110.00718 (local
  orthogonality dimension) I read only the titles. None of them gives an s-stable chromatic number for odd s.
  The almost-stable results give only upper bounds here.
- abs:Schrijver AND abs:stable, submitted 2024-11-09 to 2026-11-09, 14:08:28Z, HTTP 200: 4 results (2610.17884,
  2607.12912 and two Lovasz-Schrijver SDP papers that have nothing to do with this problem).

### 3b. Full sha256 of the other documents read (each fetched once)
- arXiv 2509.22026v1 PDF (13:55:34Z): c3ba7bdf99ca88ffa92f55179aec4ffe59cfe78a5c70d02f13319224202d1dfb
- arXiv 1710.09434 PDF (13:57:35Z): db1ada3ec9e9568a4b07156f0173b32f4c5731b23028d346750c841f1a5c6bba
- arXiv 2610.17884v1 PDF (13:57:51Z): 5b2f9f165979107a385c09d9efa7722a90df60d406588744dee34158d8a8a86f
- arXiv 2307.00299 PDF (13:58:54Z): f2e2ad795e4cf81a9aea123d39b67c9a1e0b87bc5ec319038c866915453d5e3e
- arXiv 2606.24863v3 PDF (13:59:27Z): 9b0a43dc5f047c7b55e3f2c3cc674dc0f7e82bce8a96c19cfb761bf5810b7fa3
- arXiv 1904.08219 PDF (14:02:30Z): 126d563e3fd475a6d2fc1965780c1327183fc87cc6e541b2d924d5ab49bb7614
- arXiv 1612.07462 PDF (14:02:56Z): 17a73c4df08e99dd990cfa51ef42fb67221cec6fae185ad3dd24dbcb4b61cb18
- V3R1T4S bank entry, raw at commit 850aa9c (14:00Z): 9a80482d43663d1aff3cdd5372a5a7c6e0d4e940afac88542b387dc2fcb8958c

## 4. Which n are open for (3,5)

| n | status before this claim | source |
|---|---|---|
| 15 | proven (trivial, n = sk) | |
| 16 | proven | Meunier 2011 Prop. 1; also Jonsson Thm 1.3 |
| 17 | **open** | no source gives a lower bound of 7 |
| 18, 19, 20, 21 | proven | Jonsson 2012 Thm 1.3 with t = 2 |
| 22 | **open** | Jonsson Thm 1.3 gives 11 and Cor. 1.6 needs n >= 27.5; no other source |
| >= 23 | proven | Jonsson 2012 Thm 1.3 (closed form above) |

So the open n for (3,5) are exactly 17 and 22. The claim certifies both, so if its certificates check out
(that is for the other two skeptics), it settles the pair. The values themselves agree with Meunier's
conjecture: 7 at n = 17 and 12 at n = 22. Before this claim the best published bounds were 6 <= chi <= 7 and
11 <= chi <= 12.

Caveat on dependency: "proven" for n = 18..21 and n >= 23 rests on Jonsson's manuscript, which was never
published in a journal. I read its proof and checked its two lemmas numerically, and found no problem. 2607.12912 and
2509.22026 also cite it as a proof.

## 5. The bank entry and arXiv 2607.12912 disagree with the primary source (decisive for n = 22)

The bank entry says the proven range includes "s >= 4 with n >= 2s(k-1)+2 (Jakob Jonsson 2012)" and gives the
open (3,5) cases as "n = 17..21". 2607.12912 Theorem 1.2 says the same. Read literally, both say n = 22 is
already proven and n = 18..21 are open. Jonsson's own text says otherwise:
- His exact-value statement (Corollary 1.6) for s = 5, k = 3 needs n >= 27.5, not n >= 22. The formula
  2s(k-1)+2 matches his threshold only when s is a power of 2.
- His Theorem 1.3, applied to each n directly, gives the conjectured value at n = 18..21 and every n >= 23,
  but only 11 (not 12) at n = 22 and 6 (not 7) at n = 17.
No other source settles n = 22. So someone who reads only 2607.12912 would think n = 22 is known, but no
published proof of it exists. The criterion requires that "arXiv 2607.12912 and a citation search ... must show the cases not
already proven". I read that as asking whether a proof exists. 2607.12912 attributes the case to Jonsson,
and Jonsson's text does not prove it. The maintainer should decide whether this reading is acceptable. I
also note that the claim covers the bank's own list (n = 17..21) as well: object/ ships certificates for
every n from 17 to 22. So the full set of n that either reading calls open is certified.

## 6. Earlier uncertified computation for n = 17 (disclosed in the bank entry)

The bank entry's "Traps" section says a scouting run for the entry "refuted the (n-sk+s-1)-colourings for
(n,k,s) = ... (17..19, 3, 5) in under a minute each ... these are not claimed". That run had no proof log,
nothing was published, and the bank itself still lists n = 17 among the cases a win must certify
(criterion (a)). I do not count it as a prior result that makes n = 17 a tie. But it means the value 7 at
n = 17 was expected, and what is new at n = 17 is the first checked certificate (DRAT proof, shipped in
object/proof_n17_c6.drat.xz), not a surprising value. I found no such statement, certified or not, for
n = 22.

## 7. Verdict

- Both claimed cases were open before this claim. n = 17 is open in every source. n = 22 is open on
  Jonsson's own text, and the "n >= 22" in 2607.12912 and in the bank entry is a misquote for s = 5
  (section 5). No published lower bound, citation, code repository or V3R1T4S PR or trophy gives
  chi = 7 at n = 17 or chi = 12 at n = 22. No trivial edit of a published result does either.
- Nothing else is open for (3,5): n = 15, 16, 18..21 and every n >= 23 are proven (section 4).
- The claim does not cite a published result and repackage it. It matches the conjectured value and beats
  the best published lower bounds (6 and 11) by one at each n. This is not a tie.
- Conditions on this pass: it is a novelty finding only. The DRAT checks and colourings are for the other
  skeptics. The maintainer should note sections 5 and 6, since the bank text and 2607.12912 put n = 22 on
  the other side of the line.

pass: true
