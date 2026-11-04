# Criterion skeptic: super-edge-magic-trees-beyond-17, claimed partial win p2

context: subagent (Claude Code Agent tool, fresh context, saw only claim/)

## What is claimed
claim/CLAIM.md claims p2: "Certificate that every tree on at most 22 vertices is super edge-magic", with files
object/cert_n18..n22 (n18-20 plain, n21-22 xz) and orders up to 17 resting on Lee and Shan (2002) as cited in
Gallian DS6, 28th ed., Section 5.2. p2 is read together with criterion (a): every unlabeled tree on each n, a
bijection to {1..n}, n-1 consecutive edge sums, and an independent checker that regenerates the trees, confirms
counts equal A000055(n), matches every tree by canonical form and checks each labeling.

## Evidence I produced (not trusted from the package)
1. Hashes: `sha256sum -c certificates.sha256` run inside object/ gives OK for all five files.
2. My own checker (written from the definition; did not reuse the package's code): for each line it checks
   n field, exactly n-1 edges, endpoints in 0..n-1, no self-loops, connectivity by BFS (so a tree), labels sorted
   equal to 1..n, sorted edge sums equal to m, m+1, ..., m+n-2. Canonical form: centre by leaf peeling, AHU
   parenthesis code, bicentral trees keyed by the sorted pair of half-codes. A000055 is computed in the script
   (A000081 Euler recurrence + Otter); its values for n = 4..22 match the known sequence and checkers/b000055.txt.
   Result, every order, full files (no sampling):
   - n=18 lines=123867 distinct=123867 A000055=123867 bad=0 PASS
   - n=19 lines=317955 distinct=317955 A000055=317955 bad=0 PASS
   - n=20 lines=823065 distinct=823065 A000055=823065 bad=0 PASS
   - n=21 lines=2144505 distinct=2144505 A000055=2144505 bad=0 PASS
   - n=22 lines=5623756 distinct=5623756 A000055=5623756 bad=0 PASS
   Logic: every line is a valid SEM-labelled tree on n vertices; the lines lie in A000055(n) pairwise
   non-isomorphic classes; there are exactly A000055(n) classes; so every class is covered. This argument needs no
   tree generator at all.
3. The package's checkers/indep_check.py with --regen (WROM free-tree generator, Otter count, own canonical form)
   PASSes for every n in 18..22: regenerated = A000055(n), missing=0, extra=0, bad_label=0, dup=0.
4. Third-party regeneration: networkx 3.6.1 `nonisomorphic_trees` (generator not written by the author), matched
   by my canonical form, for n=18, 19, 20: generated = A000055(n), missing=0, extra=0. (Not run at 21, 22; item 2
   already settles coverage there by counting, and item 3 regenerates them.)
5. Null models on n=18: (m1) swapping two labels in one line, (m2) replacing a line by a relabelled isomorphic copy
   of another, (m3) deleting one line. Both my checker and indep_check.py FAIL on all three. The checkers are not
   vacuous.

## Definition
The checked property (bijection V -> {1..n}, the n-1 edge sums f(u)+f(v) are n-1 consecutive integers) is exactly
the Figueroa-Centeno, Ichishima, Muntaner-Batle characterisation of super edge-magic (Enomoto et al.: total
labeling with vertex labels {1..p} and constant f(u)+f(v)+f(uv)); edge labels are recovered as p+q+min-sum minus the
edge sum, giving {p+1..p+q}. Labels are 1..n, not 0..n-1; it is not merely edge-magic total. No stretched definition.

## Hidden quantifiers and scope
- "every tree on at most 22 vertices": orders 18..22 are certified here; 1..17 rest on literature. Criterion (a)
  itself asks for files only for n in 18..25, so it builds in reliance on the 17-vertex result; p2 "as in (a)"
  inherits that. Acceptable under the wording.
- "orders already covered do not count": record/ quotes DS6 28th ed. (Oct 30, 2025), p.168: verified up to 17
  (Lee and Shan). My own web search found no report of computer verification beyond 17 vertices. So 18..22 are
  not already covered as far as I can find; the bite does not apply.
- "(as from nauty gentreeg)": nauty is not used; regeneration uses WROM, the algorithm gentreeg implements, and I
  added networkx. The count-plus-distinct-canonical argument makes the choice of generator immaterial.
- Subsumption: p2 strictly contains p1 (at most 20) and is the larger enumerated partial win; it is not the full
  criterion (a) (needs 23..25) nor (b). Within this target it is a genuine, non-subsumed partial win.

## Gaps (none blocks p2)
1. REPRODUCE.md step 1 `sha256sum -c object/certificates.sha256` fails when run from claim/ as written (the hash
   file lists bare filenames); it passes from inside object/. Documentation bug.
2. record/RECORD_DS6_pdf_2026-11-03.md ends "This package: at most 20", stale against the claim of 22. The DS6 PDF
   itself is not preserved, only its hash and a quoted cell.
3. indep_check.py is by the same author as the search (independent code, not independent authorship). Mitigated by
   my own checker and networkx regeneration above.
4. Orders 1..17 rest on Lee and Shan, a 2002 conference talk cited by DS6, not on a certificate in this package.
   Permitted by the criterion's structure, but the "at most 22" statement is only as strong as that citation.
5. The literature check for a higher bound is DS6 plus one web search; not exhaustive.

confirmed_scope: For every n in 18..22, the files object/cert_n18.txt .. object/cert_n22.txt.xz (one per order, cert_nN for order N) list exactly A000055(n) pairwise non-isomorphic trees on n vertices (hence every unlabeled tree on n vertices), each with a bijection onto {1..n} whose n-1 edge sums are consecutive integers, so every tree on 18 to 22 vertices is super edge-magic, and together with Lee and Shan's cited verification up to 17 vertices every tree on at most 22 vertices is super edge-magic (partial win p2).
edit: the n-in-angle-brackets notation replaced by explicit file names at the main session's request; no finding changed
pass: true
