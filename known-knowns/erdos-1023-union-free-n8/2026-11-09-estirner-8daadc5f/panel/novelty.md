# NOVELTY skeptic verdict
context: subagent (Claude Code Agent tool, opus, fresh context, saw only claim/)
verdict time (date -u): 2026-11-09T13:39:39Z
injection_suspected: none

Target: erdos-1023-union-free-n8 (OEIS A347025, Erdos problem 1023). Claimed object: object/union_free_n8_80.txt,
80 subsets of {1..8}, size profile stated in CLAIM.md as 2 of size 2, 15 of size 3, 63 of size 4. Bar: a(8) >= 79.

## Status fetch (primary, once, no retries)

- URL: https://oeis.org/A347025
- time (UTC): 2026-11-09T13:27:28Z, HTTP 200
- sha256 of the page as fetched: ee5d2b74424748ca7eb35b0b1127e8f0e3b1e12009d291fe46ef12da01c1f314 (21808 bytes)
- value: DATA 0, 1, 2, 4, 7, 13, 24, 44 (a(0)..a(7)); keywords nonn,hard,more; no a(8) term. The only a(8) lower
  bound in the entry is the comment "a(7) >= 44, a(8) >= 79, a(9) >= 144, a(10) >= 270; see the Apr 05 2022 entry in
  the Formula section. - Jon E. Schoenfield, Apr 04 2022". Formula section: Loo's bounds and Schoenfield's lower-bound
  formula. Other comments: Suskind's lattice reformulation (Sep 24 2026), Branicky's note on Loo's bounds, Wang's
  a(7) <= 45, Blair's a(7) = 44 (Jun 06 2026). No value of a(8) above 79 anywhere on the page.
- The HTML sha256 differs from the one in table/status_record.md (71e3c7...); the page carries dynamic content (a
  footer "Last modified" time for the whole database and a per-request link token). The JSON record
  (https://oeis.org/search?q=id:A347025&fmt=json, fetched 13:27:41Z, HTTP 200) has sha256
  41587fe3f72c5b4286aa78932be99107946efe9f363189c4f093fe0a84c8dcaa, identical to the one in
  table/status_record.md: revision 111, time 2026-09-27T11:18:49-04:00. The entry content is unchanged since the
  claimant's fetch.

## Other OEIS material

- b-file (https://oeis.org/A347025/b347025.txt, HTTP 200): synthesized from the entry, n = 0..7 only.
- Branicky's program (https://oeis.org/A347025/a347025_1.py.txt, HTTP 200): brute force, no n = 8 value or family.
- History (https://oeis.org/history?seq=A347025 and start=10..100, all HTTP 200, 13:27:43Z to 13:28:28Z): revisions
  #2 to #111 read in full. The page start=110 (which would hold only revision #1, the creation by Mitodru Misra in
  Aug 2021) returned HTTP 403 and was not retried. No a(8) bound existed before Schoenfield's revisions of Apr 2022,
  so the missing page cannot hold a competing value. a(8) values found in the history:
  - Schoenfield, a(8) >= 79 (revisions #77 to #81, Apr 04-05 2022), and his construction text: a(6) >= 24 (Mar 29
    2022: all triples except {1,2,3}, {4,5,6}, plus the six pairs inside those two triples), a(7) >= 44 (Apr 02 2022:
    add all 20 four-sets containing 7), and the general formula.
  - Greathouse (Mar 30 2022 discussion): 74 <= a(8) <= 108.
  - Schoenfield (Apr 20 2022 discussion): "If it turns out that a(7)=44 or 45, then the sequence either matches one
    of {A005318, A260668, A276661} and a(8)=84, or it's distinct from all other sequences in the OEIS ... 88 or 89".
    This is conditional speculation about coinciding with other sequences, not a construction or a proof; no family
    of size 84 (or any size above 79) is given anywhere. The bar remains the best constructed lower bound, 79, and
    the bank's own target text states 79 <= a(8) <= 89.
- Sequences citing A347025 (https://oeis.org/search?q=A347025+-id:A347025&fmt=json, HTTP 200): only A355315
  (independent collections, rows through n = 4). Data search 1,2,4,7,13,24,44: A005318 and A276661 continue with
  84, but they are other sequences (Conway-Guy etc.), not A347025 values.

## Links of the entry

- William Blair, verified-combinatorics, union-free-A347025. The OEIS link (willblair0708/verified-combinatorics)
  now resolves to williamjblair/verified-combinatorics (renamed). Read via gh api at 13:29:21Z: last push
  2026-06-17; branches main and claude/erdos-617-hitset-pair-mclpp0 both checked; zero releases, zero tags. Files:
  witnesses n = 2..7 (n = 7: 44), n = 8: a347025_n8_size60.txt (60 sets), n = 9: 107, n = 10: 175, labelled
  "From the Vela record" (provenance string not explained; noted only). The repo's DISCOVERIES.md says of these:
  "Extensions are loose lower bounds: a(8) >= 60 ... Treat as a floor, not a record."
- Andy Loo, arXiv:1511.00170 (PDF fetched 13:34:09Z, HTTP 200): table gives n = 8: L.B. 74, U.B. 119. Recursive
  bounds with current a(1..7): lower max_h a(h)+a(8-h)+1 = 46; upper min_h a(h)+2^h a(8-h) = 89.
- Math.SE question 4262598 (Stack Exchange API, 13:33:59Z, HTTP 200): one answer (2021) citing Loo and giving
  families for n <= 5; no comments; nothing for n = 8.

## Schoenfield's formula at n = 8

max over m of 2*floor(m/3) + C(m,3) + Sum_{j=m..7} C(j,m-3): m = 3: 8, m = 4: 28, m = 5: 58, m = 6: 79, m = 7: 74,
m = 8: 60. Maximum 79 (m = 6). Rebuilt explicitly from his text: 6 pairs, 18 triples, 55 four-sets; union-free;
size 79. His n = 9 (144) and n = 10 (270) families were rebuilt the same way and are union-free.

## Erdos problems site

- https://www.erdosproblems.com/1023 (13:29:05Z, HTTP 200): asymptotic question only, marked via Hunter's
  observation from problem 447 (F(n) ~ C(n, n/2)); OEIS A347025 cross-referenced; no small values.
- https://www.erdosproblems.com/forum/thread/1023 (13:29:08Z, HTTP 200): five comments (Hunter, Cambie, Bloom
  Sep 2025; Alexeev Feb 2026 on a Lean formalisation); no small values; posting suspended.

## arXiv (export.arxiv.org API, queries spaced 5 to 9 s, all HTTP 200, 13:32:16Z to 13:33:40Z)

- all:"union-free" (31 hits), abs:"union free" AND abs:family (15), abs:"meet-irreducible" AND
  abs:"join-irreducible" (10), all:A347025 (0), abs:"union of other" AND abs:family (0), Kleitman AND "union-free"
  (3), "closure system" AND "meet-irreducible" (4), "reduced context" AND "maximal number" (0), meet-irreducible
  AND maximum AND number (1), plus a broad phrase query (169, unrelated).
- Last 24 months, nearest papers: 2611.05568 (Non-redundant Independence Atoms, Nov 2026; asymptotic, uses the
  two-set union-free problem of Erdos 447; full HTML grepped, no small-n values), 2605.11949 and 2411.07908
  (uniform t-union-free hypergraphs, a different notion), 2609.11358 (union-closed families), 2507.14068 and
  2602.04321 (lattice theory, no bound of this kind). None gives a family or bound for A347025 at n = 8.

## Web and code search

- Web search (three queries: A347025 a(8); meet-irreducible maximum with n join-irreducibles; "no set is the union
  of" n = 8): only Loo (74), the OEIS entry (79) and asymptotic material.
- GitHub code search via gh api (read-only): "A347025" (Blair files, loda-lang program, Radcliffe OEIS-Python copy
  of Branicky's program, the bank's known-unknowns page, conjecturehub YAML with status only), "union-free family"
  (0), "unionfree" (Lean files on Erdos 1023 asymptotics), "erdos_1023", "Erdos1023", "unionFreeMax" (Lean
  formalisations and reviews: google-deepmind formal-conjectures, plby/lean-proofs, rjwalters/lean-genius, ryantuck
  erdos-ai, plasma-ai/erdos). Files grepped for a(8), 79, 80, n = 8: no small-n value above the known ones; the
  lean-genius notes prove only F(n) + 1 <= F(n+1) (gives 45 at n = 8).

## V3R1T4S repository (read-only)

- gh pr list --state all --limit 1100 --search "union-free OR A347025 OR erdos-1023" (13:31:00Z): 3 hits, all
  group-testing-separable-designs (OEIS A054961, a different problem). Separate searches "A347025", "erdos-1023",
  "union-free-n8", "meet-irreducible": 0 hits; "union-free"/"union free": the same group-testing PRs; "1023": an
  unrelated bank PR numbered 1023. Full listing (985 PRs, newest created 2026-11-09T10:07:00Z) grepped by title for
  1023, union, 347025, lattice, irreducib: nothing on this target.
- TROPHY_CASE.md (raw, HTTP 200, 13:31:59Z, sha256 83af764f...): no entry for this target.
- known-knowns/ (31 directories; full tree grepped): no entry for erdos-1023 or A347025.
- known-unknowns/erdos-and-proofs/erdos-1023-union-free-n8.md: states 79 <= a(8) <= 89 as of 2026-10-30.

## Comparison of the object with published ones

- Check of the object (own script, standard library): 80 distinct nonempty subsets of {1..8}, union-free, profile
  {2: 2, 3: 15, 4: 63}, matching CLAIM.md. The seven absent four-sets are the five four-subsets of {1,2,4,5,6} plus
  {2,4,7,8} and {3,5,6,7}.
- Schoenfield's 79 (profile {2: 6, 3: 18, 4: 55}): best overlap over all 40320 relabellings is 64 sets (by layer: 2
  pairs, 9 triples, 53 four-sets); the claimed family has 16 sets outside it and it has 15 sets outside the claimed
  family. The four-set overlap is at least 63 + 55 - 70 = 48 for any relabelling, so most of the 64 is forced by
  layer density, not by derivation. Not a relabelling, deletion or restriction of it.
- Schoenfield's 79 is maximal: none of the 176 non-members can be added while staying union-free, so no single
  addition to it gives 80. The claimed 80 is also maximal.
- Neighbouring cells: deleting or linking one element of the published n = 9 families gives at most 74
  (Schoenfield 144) and 59 (Blair 107); two such operations on the n = 10 families give at most 76 (Schoenfield
  270) and 54 (Blair 175). Blair's n = 8 family (60) has overlap at most 24 with the claimed one. Propagation rules
  from n = 7 (a(7) = 44): a(n-1) + 1 = 45, Loo's recursive lower bound 46.
- Every trivial edit in the kit's list (deletion, restriction, propagation rule, relabelling, symmetry, single-set
  polish) of a published object stays at 79 or below. CLAIM.md names no seed; it cites Schoenfield's 79 only as the
  bar. A maintainer may want the search method stated, but the object beats what those edits give either way.

## Verdict

80 strictly exceeds every lower-bound value for a(8) found in the live entry (79), its comments, links (Blair 60,
Loo 74) and history (74, 79; the 84/88/89 remarks are conditional speculation without a family), in the bank's
TROPHY_CASE.md, known-knowns/ and pull requests (none on this target), on erdosproblems.com, on Math.SE, on arXiv and
in GitHub code. It stays below Loo's bound of 89. The object is not reachable from any published family by the
listed trivial edits. It is a new record over the published bound, not a tie.

pass: true
