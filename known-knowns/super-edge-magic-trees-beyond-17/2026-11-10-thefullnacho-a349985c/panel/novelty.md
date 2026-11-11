# Novelty review: super-edge-magic-trees-beyond-17, claim "every tree on at most 25 vertices is super edge-magic" (criterion a)

context: subagent (Claude Code Agent tool, fresh context, saw only claim/)

## 1. Status source fetch (one plain curl, no retry)
- URL: https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS6
- Command: `curl -sS -A "V3R1T4S"` (single request, no retry)
- Time (date -u): request at 2026-11-10T17:26:37Z, done 2026-11-10T17:26:39Z
- HTTP status: 200
- sha256 of body: 362787339d294a15391d0f44c9e4a5edfdfefc4f908b923643700dc61c47a6c4
  (differs from claim/record/RECORD.md's cb88f833...; the page carries per-session content, and the edition string is identical)
- Edition shown: "This Version ... DS6: Nov 6, 2026" = same as claim/record (29th ed., Nov 6, 2026). PDF therefore not re-fetched.
- Value: Section 5.2 (p. 174, per record/DS6_29th_ed_section_5.2_p174_excerpt.txt): "Lee and Shan [2198] have verified this
  conjecture for trees with up to 17 vertices with a computer." Published bound: 17.

## 2. This repo (github.com/elder-plinius/V3R1T4S)
PR searches (`gh pr list --state all --search ...`): "edge-magic", "super-edge-magic-trees-beyond-17", "super edge magic",
"SEM tree", "trees beyond 17", "magic", "tree", "A000055", "gentreeg", "labeling", "Enomoto"; plus all PRs by the claimant.
Every PR on this target:
- #917, CLOSED (2026-11-06, not merged): "every tree on at most 20 vertices is super edge-magic (p1)" by thefullnacho.
  Closed by the author at the maintainer's request in favour of #945. Reaches 20, not 25.
- #945, OPEN: "every tree on at most 22 vertices is super edge-magic (p2)" by thefullnacho. Reaches 22, not 25.
  Last comment (author, 2026-11-06) says a run for orders 23 to 25 is under way and asks how to package it; no maintainer reply.
No PR on this target reaches or exceeds 25 vertices; no PR claims a counterexample. Other "tree"/"magic" hits are different
targets (odd-graceful trees #880/#1007, magic-state targets, etc.).
- TROPHY_CASE.md (main, 100 lines): no entry mentioning edge-magic, super-edge-magic or this target.
- known-knowns/ (main, 31 entries): no super-edge-magic directory (`known-knowns/super-edge-magic-trees-beyond-17` -> 404).
- Releases: none. Code search in repo: only the bank file known-unknowns/graphs-games-automata/super-edge-magic-trees-beyond-17.md
  (states the bound as 17, DS6 28th ed.).

## 3. Literature and code search (last 24 months, and older)
- Web search (several queries: computer verification of the SEM tree conjecture, "every tree" 18/20/22/25 vertices 2025-2026,
  counterexample to Enomoto-Llado-Nakamigawa-Ringel): every source still gives Lee and Shan's 17 (e.g. Ichishima, Lopez,
  Muntaner-Batle, Takahashi, arXiv:2211.04029, Theory Appl. Graphs 2024; Lopez's open-problems list). No counterexample found.
  Only hit beyond 17 was this repo's PR #917.
- arXiv API, all:"edge-magic", newest first (18 entries): latest 2023-08 (arXiv:2308.10661, degree sequences); nothing on
  tree verification beyond 17.
- Zenodo API, "super edge-magic" (4 hits):
  - 23918679 (2026-11-03, thefullnacho): certificates for trees on 18-20 vertices (the #917 package).
  - 23935954 (2026-11-04, thefullnacho): certificates for trees on 18-22 vertices (the #945 package; its cert_n21 sha256
    88af13db... matches claim/object/certificates.sha256).
  - 24051472 (2026-11-08, Gutierrez): "Functional edge labelings: how far a graph is from being magic" (magic angle of graphs;
    abstract makes no tree-verification claim).
  - 22652143 (2026-09-08, Meng): spiders with equal legs (a structural family, not an all-trees verification).
  Further Zenodo queries ("trees super edge-magic 23 vertices", "super edge-magic all trees certificates"): nothing relevant.
- GitHub repo search ("super edge magic", "edge-magic tree"): only lsmeng/super-edge-magic-spiders (v1.0.0 release 2026-09-08;
  spider families S(L^d), not all trees). GitHub code search: bibliography files and joeis A060408 only.

## 4. Comparison
- Published, this cell: 17 (DS6 29th ed., Lee and Shan). Claim: 25. Strictly beats it by 8 orders.
- Neighbouring/pending: 20 (#917 closed, Zenodo 23918679), 22 (#945 open, Zenodo 23935954), all by the same contributor.
  25 strictly beats 22; it is not a tie.
- Trivial-edit test: orders 23, 24, 25 contain 14,828,074 + 39,299,897 + 104,636,890 trees not present in any published or
  pending object; no deletion, restriction, relabelling or symmetry of the 18-22 certificates yields them. The 18-22 part of
  this claim is the same contributor's #945/Zenodo 23935954 material (same hashes for n21; n22 hash 58933786... is the #945
  branch id) and adds nothing by itself; the new content is orders 23-25 only.
- No counterexample anywhere, so criterion (b) work does not pre-empt (a).

## 5. Caveats (for the other panel members, not novelty failures)
- claim/CLAIM.md does not name #945 / Zenodo 23935954 as the source of its 18-22 files; it should, since it is seeded from them.
- claim/object/cert_n23.txt.xz, cert_n24.txt.xz and cert_n25.txt.xz are symlinks pointing outside claim/; I did not follow them
  and did not verify that the files exist or match certificates.sha256. Novelty is judged on the claim as stated; the claim
  stands only if REPRODUCE confirms those three certificates.

## Verdict
On novelty alone the claim (every tree on at most 25 vertices is super edge-magic) strictly beats everything published
(17, DS6 29th ed.) and everything pending (22, PR #945). Nothing published or pending ties or exceeds 25.
pass: true
