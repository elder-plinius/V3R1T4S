# Panel: NOVELTY skeptic

context: subagent (Claude Code Agent tool)
role: NOVELTY (fresh context; read only the claim bundle copy, the pinned repository copy and public sources)
target: gauss-kuzmin-wirsing-certified-digits
claimed object: certified enclosure of C_83 = |lambda_2| with radius < 10^-842 (D = 842), claim/result/enclosure_C83.txt,
runs claim/result/cert_L1.json (3900 bits) and claim/result/cert_L2.json (4300 bits)
injection_suspected: none found (the bundle and fetched pages were read as data; nothing in them addressed the panel)

## 1. Status source (fetched once, no retries)

- URL: https://teorth.github.io/optimizationproblems/constants/83a.html
- Fetched 2026-11-09T08:28:40Z (finished 08:28:41Z) with one plain curl request (User-Agent naming V3R1T4S): HTTP 200,
  6976 bytes, sha256 29011a2a62c3ec66fea597165bad3229d0fab22aa6a5bcfe8ab50b6d725b3bc8 (identical to the scout's
  claim/data/83a.html). Server Last-Modified: Wed, 28 Oct 2026 04:16:30 GMT.
- Value on the page: upper and lower bounds `0.30366300289873265859...6424297 +/- 10^{-175}`, [GKW2026] (Nisoli,
  arXiv:2602.19435), "Certified spectral enclosure for the infinite-dimensional GKW operator; 175 digits". Earlier
  certified bounds on the page: 0.30366299 / 0.30366327 (Mayer-Roepstorff 1987), 2/(3+sqrt 5) (Schweiger).
  **Current certified record: 175 digits.**
- Source constants/83a.md (via read-only `gh api` contents, 2026-11-09T08:28:56Z): sha256
  2d4fe7a9157fdc5180cdf590b203fad49ff77198025c6be07d60607482f54db6 (identical to claim/data/83a.md); same 175-digit
  bounds and full 175-decimal centre. Commits touching it: 2985a56fcb (2026-03-23), e19945db63 (2026-03-23),
  eef77902e2 (2026-05-03, "fix inline braces"); nothing since.
- Open PRs of teorth/optimizationproblems (GraphQL, 2026-11-09T08:29:02Z-08:29:04Z): totalCount 81, all 81 fetched
  with full file lists (none had more than 100 files); **none touches constants/83a.md** or any Wirsing/GKW file.
  Issue/PR search in that repository for "Wirsing", "GKW", "Gauss-Kuzmin", "C_83" returns only #58 (closed; the
  original Nisoli addition of 2026-03-23).

## 2. Literature and code, last 24 months

- arXiv API search (2026-11-09T08:30:29Z; all:"Gauss-Kuzmin-Wirsing" OR "Wirsing constant" OR "Gauss-Kuzmin" OR
  Wirsing, 60 newest) and a second search (08:34:03Z; Gauss map / continued fraction map / Mayer operator / Gauss
  problem AND eigenvalue/spectrum/transfer operator). Relevant hits updated since 2024-11:
  - arXiv:2602.19435 (Nisoli), v1 2026-02-23, v2 2026-03-01 (abs page fetched 08:30:09Z; no v3). Certifies
    50 eigenvalues to >= 90 digits; lambda_2 to 175 digits. This is the record on the status page.
  - arXiv:2606.13958 (M. Pollicott, "Validated numerics for the Gauss problem on continued fractions", v1
    2026-06-11). PDF fetched 08:30:53Z (sha256 a332e259792dcd629ebd4ac4a34cd99084b2852483edd862a8d382e817715edd),
    text extracted: its best example (m = 80) gives bounds "accurate to 67 decimal places"; its intro states "In 2026,
    Nisoli estimated [the constant] rigorously to 175 places." **67 < 175 < 842.**
  - arXiv:1210.4083v9 (Alkauskas, updated 2026-10-01). PDF fetched 08:34:16Z; it adds rigorous structural results
    (eigenvalue asymptotics, exact rational certificates for a finite range of a different statement) and, for
    certified values of lambda_2, refers to Nisoli [41] and Pollicott [45]. No new certified digit count.
  - Others (2608.17686 p-adic Wirsing problem, 2511.01992, 2606.03229, 2608.05853, ...) are about different objects.
- Nisoli's code github.com/orkolorko/GKWExperiments.jl (read-only `gh api`, 08:29:37Z): **0 releases, 0 tags**,
  no forks; last push 2026-08-30 (README: "no numerical method changed", environment pinning, K=1024 data
  re-verified); WIP/codex branches end in 2025-10. Its pipeline runs at 2048 bits, i.e. about 616.5 decimal digits of
  working precision, so it cannot carry a radius near 10^-842 as published.
- Harvard Dataverse doi:10.7910/DVN/HKM3Y2 (version API, 08:35:18Z): only version 1.0, released 2026-02-20.
- OEIS A038517 (fetched 08:33:53Z): no certified claim; b-file (08:34:51Z, sha256
  cfabde8d6a4ac3f3e048cef8d44e1faeba25cb4627040b678081229441c3c357, 382 terms) is non-certified (Briggs-based).
- GitHub repository search ("Wirsing", "Gauss-Kuzmin-Wirsing", "gauss kuzmin", "GKW operator"; 08:33:41Z): nothing
  computing certified digits of this constant.
- Two web searches: they find only Nisoli (175, about 5e-176) and Pollicott, plus non-certified values (Briggs 385 /
  "probably" 468, Alkauskas > 480, Sebah 100). None is certified beyond 175.

## 3. V3R1T4S repository

- Pinned copy (commit cf68067f52, 2026-11-03): TROPHY_CASE.md and known-knowns/ have no entry for this constant;
  the only matches are bank/targets.json and known-unknowns/number-hunts/gauss-kuzmin-wirsing-certified-digits.md.
- Live repository (read-only `gh api`, 08:31:42Z; head 850aa9c47b, 2026-11-08): TROPHY_CASE.md has no
  Wirsing/Kuzmin/GKW/C_83 entry; the 31 known-knowns/ folders include none for this target; the live bank entry for
  `gauss-kuzmin-wirsing-certified-digits` is identical to the pinned one (record "currently 175").
- All pull requests (GraphQL, 08:32:01Z-08:33:04Z): 980 (442 open, 354 closed, 184 merged; highest #1032). Scanned
  titles, branch names and file paths: none concerns this target. The only text hits are hash fragments ("83a") and
  #961 (integer Chebyshev constant), which mentions Wirsing in passing. 40 PRs had file lists cut off at 60 files; I
  checked their titles and none concerns this target. Issue search for "Wirsing" or "lambda_2": 0 issues.
- The earlier 300- and 601-decimal certificates in this workspace were never published, so they are not prior art.

## 4. Comparison of the object with published objects (cell and neighbours)

- Cell (certified decimals of |lambda_2|): published maximum 175 (Nisoli). Next: 67 (Pollicott 2026), 8 digits
  (Mayer-Roepstorff 1987). The claim gives D = 842: L1 radius [4.54904e-843 +/- 2.41e-849], L2 radius
  [4.42979e-843 +/- 4.67e-850], both `certified_D: 842`, `isolation_ok: true`. My own check of
  claim/result/enclosure_C83.txt (mpmath, 1300 digits): endpoints of 860 decimals, half-width 4.5535915e-843 < 10^-842;
  both run centres lie inside the hull.
- Agreement with published values (the right cell, right sign): |mid - Nisoli's 175-decimal centre| = 4.09504e-176
  (< 10^-175 + half-width); |mid - OEIS b-file (382 decimals)| = 6.16143e-383, consistent with truncation.
- Trivial-edit test: deleting or restricting Nisoli's enclosure, or polishing its centre locally, cannot shrink its
  proved radius below 10^-175. Polishing a published non-certified expansion (Briggs, Alkauskas, OEIS) gives digits
  without a proof, and no published one has 842 digits. Relabelling and symmetry do not apply. Nisoli's published
  pipeline works at 2048 bits (about 616 digits), so no rerun of the published code as it stands reaches 10^-842.
- Seeding: CLAIM.md says the centre is the bundle's own N = 2800 Rayleigh quotient, warm-started from its own
  N = 2400 vector (not public), and that the certificate holds for whatever centre it is given (PROOF.md Remark 0).
  The method credits Nisoli's resolvent-bridge idea for isolation, and names him. The new part is the proved radius,
  which beats the published one by 667 decimal orders.
- Margin: 842 > 175 strictly (not a tie). It also beats every non-certified count named on the status page (Alkauskas
  "over 480").

## 5. Notes / worries (none blocks novelty)

- CLAIM.md says the enclosure endpoints are "to 740 places", but the file has 860 decimals per endpoint. This is a
  wording slip in CLAIM.md; the radius and D are unaffected. Worth fixing before publication.
- The `eig_inside_Gamma2` entry in the cert JSONs (the K = 80 coarse matrix, -0.30366300289873265859744812190155623
  29...) differs from the centre at about the 37th decimal. That is expected for the K = 80 section used only for
  counting and isolation. Whether the proof is valid is for the correctness skeptics; novelty does not depend on it.
- Novelty holds only if the certificate is valid. This file judges the record comparison, not the proof.

novelty: CONFIRMED. The status source was read at 2026-11-09T08:28:40Z and shows 175 certified digits (Nisoli). No
open PR touches constants/83a.md. No publication, code release, dataset or V3R1T4S entry certifies more than 175
digits (the best other is Pollicott, 67). The claimed D = 842 strictly beats all of them and is not a trivial edit of
any published object.

pass: true
