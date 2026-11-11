# Criterion skeptic: super-edge-magic-trees-beyond-17

context: subagent (Claude Code Agent tool, fresh context, saw only claim/)

Inputs read: CLAIM.md, REPRODUCE.md, object/ (all eight certificate files and certificates.sha256), checkers/ (check_sem.py,
verify_cert.py, verify_sem_coverage.py, indep_check.py, b000055.txt), record/ (RECORD.md, DS6 landing page and headers,
PDF headers, Section 5.2 page 174 excerpt). Nothing else under the run or data folders was opened. My own tools and logs
are in panel/criterion-work/ (semcheck.c, extcheck.c, otter.py, perm.py, runall.log, runext.log, indep.log).

## 1. What criterion (a) literally demands, clause by clause

| Clause | Requirement | Finding |
|---|---|---|
| scope | every tree on at most 25 vertices is super edge-magic | 18..25 certified here; 1..17 rest on Lee and Shan via DS6 (see 3) |
| per order | for EACH n in 18..25, a file | cert_n18 .. cert_n25 all present, sha256 all OK |
| content | every unlabeled tree on n vertices | verified for all 8 orders, not sampled (see 2) |
| labeling | bijection to {1..n}, the n-1 edge sums consecutive | every one of 165,778,009 lines checked, 0 failures |
| checker | regenerates the trees | indep_check.py --regen (WROM generator), plus my own leaf-extension regeneration |
| checker | confirms counts equal A000055(n) | indep_check.py computes Otter's formula; verify_sem_coverage uses the OEIS b-file; my otter.py agrees with both |
| checker | matches every tree by canonical form | yes, in indep_check.py, verify_cert.py and in my checker |
| checker | checks each labeling | yes |
| independence | checker independent of how certificates were produced | indep_check.py reads only the certificate text; it imports nothing from the other checkers or any solver. Its authorship is the claimant's, so "independent" holds at the code level only. My checker is independent in both senses |

Definition check. check_sem.py and indep_check.py (sem_ok) test exactly the Figueroa-Centeno, Ichishima and Muntaner-Batle
characterisation: labels are a permutation of 1..n, and the q = n-1 edge sums are pairwise distinct and span exactly n-2,
so they are q consecutive integers. By that lemma this is equivalent to super edge-magic in the sense of Enomoto,
Llado, Nakamigawa and Ringel (an edge-magic total labeling whose vertex labels are exactly {1..p}), which is the
definition DS6 quotes on page 174. It is not the weaker edge-magic total property. The labels are 1..n, never 0..n-1;
my parser rejects any label outside 1..n.

Hidden quantifiers. "Every unlabeled tree": every isomorphism class, checked by complete coverage, not by a sample.
"n-1 edges": both checkers require exactly n-1 edges and acyclicity, so each line is a spanning tree. Each file holds a
single order (wrong_n = 0). No line is missing a label field (unlabeled = 0 or bad_label = 0 everywhere).

## 2. My own verification (evidence, not trust)

All runs used nice -n 19, at most 2 processes, peak 1.6 GB.

(a) sha256sum -c object/certificates.sha256: all 8 OK.

(b) semcheck.c, written from the definition. It parses every line strictly and checks the tree with union-find. The
labels must be a permutation of 1..n, and the edge sums must be distinct and span n-2. The canonical form is the AHU
parenthesis code rooted at the centre (minimum over two centres), stored EXACTLY as a 2n-bit integer, so there is no
hashing and no partitioning. Keys are sorted and counted. Results:

| n | lines | valid | distinct canonical | A000055(n) (own Otter computation) |
|---|---|---|---|---|
| 18 | 123867 | 123867 | 123867 | 123867 |
| 19 | 317955 | 317955 | 317955 | 317955 |
| 20 | 823065 | 823065 | 823065 | 823065 |
| 21 | 2144505 | 2144505 | 2144505 | 2144505 |
| 22 | 5623756 | 5623756 | 5623756 | 5623756 |
| 23 | 14828074 | 14828074 | 14828074 | 14828074 |
| 24 | 39299897 | 39299897 | 39299897 | 39299897 |
| 25 | 104636890 | 104636890 | 104636890 | 104636890 |

malformed, not_tree, wrong_n and bad_label were 0 in every order. The counting argument: there are A000055(n) pairwise
non-isomorphic valid trees on n vertices, so every isomorphism class is covered. Checker validation: (i) every n = 18
tree was randomly relabelled and its edges shuffled, and the sorted key file came out byte-identical, so the key is
invariant; (ii) on 200,000 uniformly random Prufer trees of order 8 it found exactly A000055(8) = 23 classes, and it
never exceeded the class count at orders 10 and 12; (iii) swapping two labels in 1000 lines gave bad_label = 1000;
injected cycle, missing-edge and out-of-range-label lines were all rejected; a relabelled duplicate line was caught
(distinct = lines - 1).

(c) extcheck.c, a regeneration that trusts no enumerator and no count. For n = 18..24, every certified tree on n vertices
received a leaf at every vertex in turn. Each child's canonical key was looked up in the certified key set of order n+1.
Every tree on n+1 vertices arises this way from some tree on n vertices, and order n is complete by (b). Result for
every step from 18 to 19 up to 24 to 25: children_not_in_cert = 0 and cert_keys_never_generated = 0. So order 25 is
regenerated in full (about 943 million leaf extensions in the 24 to 25 step) and matched by canonical form both ways.

(d) The claim's own regenerating checker, checkers/indep_check.py --regen, run unchanged (python3 -I) for n = 18..24.
Every order ends in "-> PASS" with lines = distinct = A000055(Otter) = regenerated, and malformed, not_tree, bad_label,
dup, missing and extra all 0. n = 24 took 1570 s at a 3.5 GB peak (log in criterion-work/indep.log). It was not run at
n = 25: its exact-key set needs about 11.5 GB, above my 8 GB cap. At n = 25 its role is covered by (b) and (c).
Reading its code: the tree test is union-find with range and loop checks; sem_ok is exactly the FIM criterion; the
canonical form is a centre-rooted level sequence (bicentral rooted on the central edge); A000055 comes from Otter's
formula, not the b-file; regeneration is the WROM successor algorithm, with each generated tree removed from the
certificate set, so missing = extra = 0 together with generated = A000055 is a bijection.

## 3. Status, prior coverage and subsumption

- record/: the DS6 landing page (its sha256 matches RECORD.md) shows "DS6: Nov 6, 2026" and DC.Date.modified
  2026-11-06. The page 174 excerpt of the 29th edition reads "Lee and Shan [2198] have verified this conjecture for
  trees with up to 17 vertices with a computer." Current bound in DS6: 17.
- Literature: I ran one independent web search. The 2022/2024 survey by Ichishima, Lopez, Muntaner-Batle and
  Takahashi also gives 17, and I found no higher computational bound. Orders 18..25 are therefore not "already
  covered", and the result is not subsumed by any source I could find. Partial wins p1 (at most 20) and p2 (at most
  22) are subsumed BY this result, not the reverse; (a) is the operative win.
- "orders already covered do not count": the claim counts only 18..25 as new, as the criterion requires. Relying on
  Lee and Shan for orders up to 17 matches the criterion's own structure ("for each n in 18..25, a file"), so the
  wording does not demand certificates below 18.
- "(as from nauty gentreeg)": I read the parenthetical as fixing the object (unlabeled free trees, one per
  isomorphism class, the population gentreeg emits), not as mandating that tool. gentreeg is not installed here and
  was not used by anyone in claim/. Coverage of exactly that population is proven three ways: by the count of
  distinct classes, by WROM regeneration (the algorithm gentreeg itself is built on), and by leaf extension.
- Null model: the claim is not vacuous. Super edge-magic labelings are a strict subset of edge-magic total ones,
  and the global conjecture is open; the trees certified include every shape, not only the classes already proven
  (caterpillars, diameter at least n-5).

## 4. Gaps (none blocks criterion (a))

1. Orders 1..17 are not certified here. They rest on Lee and Shan as cited in DS6. That source is a 2002 conference talk
   (the reference list spells the second author "Shah"), not a published proof. The criterion's structure accepts this,
   but the statement "every tree on at most 25 vertices" is only as strong as that citation for orders up to 17.
2. The literature re-check is recorded in claim/ for DS6 only. My one web search found nothing above 17 but is not
   exhaustive.
3. claim/ contains no logs of the claimant's own checker runs. I re-ran indep_check.py --regen myself at 18..24 but not
   at 25 (memory cap). At 25, coverage rests on my own checker (b) and regeneration (c).
4. indep_check.py is "independent" by code (it reads only certificate text and shares no imports), not by authorship.
   My checks supply the authorship-independent confirmation.
5. My canonical form is validated empirically (invariance under random relabelling) and is the textbook AHU centre code.
   I did not prove it formally. A non-invariant key would surface as a count mismatch or as extension misses, and none
   appeared.

confirmed_scope: For every n from 18 to 25, the hash-verified certificate file in claim/object gives exactly A000055(n) pairwise non-isomorphic trees on n vertices (hence every unlabeled tree of that order), each with a bijection onto {1..n} whose n-1 edge sums are consecutive integers (a super edge-magic labeling), as confirmed by an exact canonical-key count, by leaf-extension regeneration from order n-1, and by the claim's own regenerating checker for n up to 24; combined with the Lee and Shan verification up to 17 cited in DS6 (29th ed., Nov 6, 2026), every tree on at most 25 vertices is super edge-magic, meeting criterion (a) in full.

pass: true
