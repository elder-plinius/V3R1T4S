# Novelty verdict: hsp4, N = 66

context: subagent (Claude Code Agent tool, fresh context)
scope: read only claim/CLAIM.md, claim/REPRODUCE.md, claim/hsp4-66-candidate.txt (header line), claim/hsp4-66-posted.txt (first line), claim/hsp4_radius_as_fetched.txt (row 66), plus the public fetches below. Nothing else on the machine.

candidate: r* = 0.26497636751387599 (header of hsp4-66-candidate.txt; the arithmetic check itself belongs to the other skeptics)
posted (claim snapshot): 66 0.264968466676
gain vs live table: 0.26497636751387599 - 0.264968466676 = 7.90e-6 (> 1e-10 margin, so strict, not a tie)

## Live fetches (each exactly once, curl -sS -A 'V3R1T4S skeptic', no retries; UTC from date -u; status from curl -w '%{http_code}')

A first attempt at a shell loop failed inside the shell before curl built a request (argument-parsing error, zero bytes sent); the fetches below are the only requests actually made.

1. https://packomania.com/hsp4/txt/radius.txt
   time: 2026-10-14T03:16:42Z   HTTP: 200   5575 bytes, 299 rows
   row 66 quoted verbatim: `66 0.264968466676`
   file is byte-identical to claim/hsp4_radius_as_fetched.txt (diff -q: no differences).

2. https://packomania.com/hsp4/hsp4.html
   time: 2026-10-14T03:16:43Z   HTTP: 200   88618 bytes
   quoted: `Last update: 06-Jul-2025`
   History of updates section contains exactly three entries: 04-Jul-2025 (first presentation N=2-100), 05-Jul-2025 (extension to N=200), 06-Jul-2025 (extension to N=300). No entry newer than 06-Jul-2025; no entry mentions N=66 specifically. Footer dated 06-Jul-2025. Table row for N=66 on the page: `66 0.264968466676 ... [31]`.

3. https://packomania.com/pending-requests.html
   time: 2026-10-14T03:16:44Z   HTTP: 200   4954 bytes
   page header: "List of pending requests (08-Oct-2026)", footer "08-Oct-2026".
   grep -i hsp: no match. No hsp4 (or hsp5/hsp6) category entry exists on the page, so no hsp4 range includes 66.
   Entries present are for categories csc, ccq, crt, csq, chx, cpt, crc, cxd, csqv (circle/3D-sphere categories, not 4D hyperspheres). Some of those ranges numerically contain 66 (e.g. "Zeeshan Tariq csc 136 candidates in the range 41-250"), but they are a different category and do not apply.
   QUEUE CAVEAT (cannot be resolved): the entry `26-Sep-2026 01:11  Moki & Julio  *many*  4666 candidates total` is still listed and is category-unspecified. It could in principle contain an hsp4 N=66 candidate. Per the bank rule, N=66 must be re-checked against the live hsp4 table once that bundle disappears from the pending list.

4. https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md
   time: 2026-10-14T03:16:45Z   HTTP: 200   30486 bytes
   grep -i for hsp4, hypersphere, 4-ball, hyperball, \b66\b: no match. The file lists six result families (degree-diameter graphs, constant-weight codes, matrix multiplication, Lehmer, VNN-COMP, RobustBench) plus two cipher commitments; no sphere-packing family at all.

5. https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100
   time: 2026-10-14T03:16:45Z   HTTP: 200   7 open PRs
   #1 DmitrL-dev "fix: reject malformed null control counts"; #2-#7 calgulbenkian, all "[claim] fmm-catalogue-small-format-rank: format (...) rank ... over Q". None mentions hsp4, hyperspheres, packomania or N=66 in title or body.

## Literature search (last 24 months)

WebSearch queries run (7 total):
- "66 hyperspheres in a hypersphere 4D packing radius" -> only Packomania 3D sspn66 (r=0.3285, different problem), Stoyan-Yaskov 2012 JOGO paper (dims 2-24, unequal/few spheres), Otago lattice page. Nothing for (4,66).
- "packomania hsp4 66" -> only unrelated HPS4 gene results.
- "equal 4-balls in a ball" / "equal hyperspheres in a hypersphere" 2025 2026 -> Schlenk symplectic packings (different problem), Boroczky 1993 (3D), Zhou et al. arXiv:2305.10023 (3D spheres in sphere), Litvinchev et al. MBE 2020 (unified hypersphere approach; cites Packomania, no 4D record table). Nothing newer than Packomania's own July-2025 table for this category.
- "densest packing of equal spheres in a 4-dimensional ball N=66 0.264968" -> no source reproduces or beats the value; only Packomania itself.
- "arxiv 2025 ... hsp4 hsp5 hsp6" -> nothing; OEIS A084827/A084829 are 3D (Pfoertner).
- extended: "hyperspheres in a hypersphere" packomania Specht 2025/2026 4D new records -> no 2025/2026 announcement of any hsp4 update; a 2024 3D spheres-in-sphere heuristic paper (274/396 improved) is 3D only; preprints.org "Sphere Packing Problem in Dimension 4" and arXiv 2609.25120 concern infinite-space density in R^4, not container packings.
- "arxiv 2026 packing 4-ball equal spheres best known radii table N up to 300" -> nothing relevant.
Conclusion: no 2024-2026 source lists a packing of 66 equal balls in a 4-ball with radius >= 0.26497636751. The only known value is Packomania's 0.264968466676 (E. Specht, July 2025), which the candidate strictly exceeds by 7.9e-6.

## Verdict

- Live table value for N=66 is still 0.264968466676: yes (2026-10-14T03:16:42Z).
- Candidate strictly beats it by > 1e-10: yes (7.9e-6).
- No History-of-updates entry newer than 06-Jul-2025 on live hsp4.html: yes.
- No hsp4 range on pending-requests.html includes 66: yes (no hsp category listed at all).
- Nothing in literature, TROPHY_CASE.md or open PRs matches or beats the candidate: yes.
- Unresolvable caveat: the category-unspecified "Moki & Julio *many* 4666 candidates" bundle (26-Sep-2026) remains in the queue; re-check N=66 against the live table once it clears.

pass: true
