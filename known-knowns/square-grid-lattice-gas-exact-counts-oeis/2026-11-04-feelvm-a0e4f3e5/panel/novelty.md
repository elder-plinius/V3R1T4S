# NOVELTY skeptic report — A054759 a(15)

Claim under test: a(15) = 4310182149988584261406143524214457416387448 is the first unknown term
of OEIS A054759 (Eulerian orientations of the n x n toroidal grid = square ice on the n x n torus),
extending a table whose published frontier is a(14) (Brendan McKay, 2024-04-18).

context: subagent

## 1. Live OEIS state (fetched 2026-11-04)

- https://oeis.org/A054759 (fetched 2026-11-04, ~19:12 local):
  - Name (verbatim): "Number of Eulerian orientations of the n X n square lattice (with wrap-around),
    i.e., number of arrow configurations on n X n grid that satisfy the square ice rule."
  - DATA: a(1)..a(14) only; last term a(14) = 15844635835975276495290739119895808472.
  - Credit line: "a(14) from Brendan McKay, Apr 18 2024." (original terms: Jennifer Henry, Dec 1998).
  - The 43-digit value 4310182149988584261406143524214457416387448 appears NOWHERE on the page.
  - No mention of a(15) or any term beyond a(14).
- https://oeis.org/A054759/b054759.txt (fetched 2026-11-04):
  - Exactly 14 lines. First lines: "1 4", "2 18", "3 148", "4 2970", "5 143224".
  - Last line: "14 15844635835975276495290739119895808472".
  - Largest index = 14; claimed a(15) value absent from the file.
- Conclusion: live published frontier is a(14); claimed value is not in the live entry or b-file. CONFIRMED.

## 2. Revision history (fetched 2026-11-04)

- https://oeis.org/history?seq=A054759 and its older-changes page
  https://oeis.org/history?seq=A054759&start=10 — together these cover the 20 most recent
  revisions, spanning 2022-11-04 through 2026-10-22.
- The ONLY DATA change in that entire window: revision #29, Brendan McKay,
  Thu Apr 18 03:47:26 EDT 2024 — extended the sequence with a(14)
  ("...19895808472"; EXTENSIONS: "a(14) added by Brendan McKay, Apr 18 2024").
- All revisions in the last 12 months (Oct 6 and Oct 22, 2026, by E. W. Weisstein,
  M. De Vlieger, M. Marcus, A. Howroyd; Feb 2025 by C. R Greathouse IV; May 2026 by S. A. Irvine)
  are LINKS and STATUS edits only (MathWorld/Wayback/Lieb reference links, review workflow).
  None touch DATA. Entry re-reviewed and set approved/reviewed in Oct 2026 — still ends at a(14).
- No revision between 2024-04-18 and today added a(15) or any term beyond a(14). CONFIRMED.
- Caveat (inherent): unpublished/pending OEIS draft edits are not publicly visible. My verdict is
  therefore exactly: no evidence of prior publication reachable from public sources.

## 3. Web searches for any prior a(15) (performed 2026-11-04)

Searches run:
1. Exact string "4310182149988584261406143524214457416387448" -> ZERO indexed results anywhere.
2. Exact string "15844635835975276495290739119895808472" (the frontier a(14)) -> ONLY oeis.org
   (main entry + /list view). Even the frontier term has no external publication, so there is no
   active external table extension to piggyback on or compete with.
3. "A054759" "a(15)" Eulerian orientations -> only the OEIS entry itself; no a(15) anywhere.
4. "A054759" -site:oeis.org -> only MathWorld "Lieb's Square Ice Constant" (constant, no term
   tables beyond linking OEIS); all other hits are unrelated SKU/registration-ID collisions
   (notebooks, pressure vessels, etc.).
5. "A054759" site:github.com OR site:gitlab.com OR site:codeberg.org -> no results.
6. "square ice" 15x15/15 x 15 torus count, Eulerian orientations enumeration -> no exact count
   published. Closest adjacent work, none of it computing A054759 a(15):
   - Bousquet-Mélou, arXiv:2503.15046 (2025): refined enumeration of PLANAR Eulerian
     orientations of quartic maps — different graph class (planar maps, not the torus).
   - Bartzos et al., arXiv:2609.06701: MAXIMUM Eulerian-orientation counts of 4-regular graphs
     up to order 15 — a different quantity (max over graphs), not the torus count.
   - Mihail & Winkler 1992; Creed PhD thesis (Edinburgh); Z. Wang 2011 survey — complexity
     and transfer-matrix methodology only, no new torus terms.
7. Finch, "Errata and Addenda to Mathematical Constants", arXiv:2001.00578 (v4 dated 2024-05-27,
   i.e. AFTER McKay's a(14)): downloaded the 168-page PDF and full-text searched it (pdftotext):
   zero occurrences of "ice", "torus"/"toroidal", "Eulerian orientation", "A054759", the a(14)
   value, or the claimed value's prefix "4310182149". No term table beyond a(14) here.
8. GenericTensorNetworks (Jin-Guo Liu et al., QuEra; arXiv:2205.03718 / SIAM J. Appl. Math.):
   the package has generic orientation-counting capability and is known to cover hard squares
   (A006506); no published exact A054759 torus terms found in docs/paper/repo searches, and the
   exact-number searches (1) and (5) came back empty. No overlap with this claim found.

## 4. Sequence identity check

- OEIS name matches the claim's definition exactly: Eulerian orientations of the n x n square
  lattice with wrap-around = arrow configurations satisfying the square ice rule (six-vertex /
  ice rule on the torus). CONFIRMED.
- Small terms in both DATA and b-file: 4, 18, 148, 2970, 143224 for n = 1..5 — match the claim. CONFIRMED.
- Plausibility cross-check (growth constant, Lieb): claimed a(15) has 43 digits;
  a(15)/a(14) = 272027.85 vs exp(0.431523058 x (225-196)) = 272166.33 from Lieb's entropy
  constant — agreement to 0.05%, with a(15)^(1/225) = e^0.43612 approaching (4/3)^(3/2) = e^0.43152
  from above, as expected. Consistent with a genuine a(15), not with a digit-level error.

## 5. Verdict

The live OEIS entry, b-file, and the complete public revision history (2022-11 through 2026-10)
end at a(14) with no a(15) ever added; the claimed 43-digit value has zero presence anywhere
indexed on the web; even a(14) itself has no external publication; adjacent literature (planar
Eulerian orientations, max-Eulerian-orientation records, tensor-network packages, Finch's
constants compilations) contains no torus square-ice table extension. I cannot see unpublished
OEIS drafts, so the precise finding is: no evidence of prior publication reachable from public
sources. The claimed term is genuinely new/unknown publicly.

pass: true
