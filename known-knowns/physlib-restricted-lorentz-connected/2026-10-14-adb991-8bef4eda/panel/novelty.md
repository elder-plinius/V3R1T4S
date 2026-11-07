# NOVELTY verdict: physlib-restricted-lorentz-connected

context: subagent (fresh Agent-tool context; saw only claim/)
scope: besides claim/, I used only what the brief allows: public network sources, the V3R1T4S repo copy (TROPHY_CASE.md and its pull requests only), and the read-only pinned Physlib/Mathlib sources. The harness showed the repo's one-line CLAUDE.md ("Read AGENTS.md first"). I did not read AGENTS.md or anything else in the workspace.
claim (CLAIM.md): for every d : ℕ, `IsConnected (LorentzGroup.restricted d : Set (LorentzGroup d))`, which is Physlib `semiformal_result "FXNL5" restricted_isConnected`. Proof object: object/RestrictedIsConnected.lean, sha256 8bef4eda0ca4af1b97b2b4911b75917a647fb74d73b3d56273c6779c313dc38d (recomputed; matches CLAIM.md).
criterion: the claim is a Lean proof of a statement Physlib records without proof. It is novel only if the statement is still unproved upstream at my fetch and no public source already proves it. A tie is not a record.

(Saved by the run's main session from the skeptic's final message, verbatim apart from de-indentation; the skeptic
was told to return its verdict as text. Its scratch work is in runs/2026-10-14-0608/panel_work/novelty/; its git
clones there are kept out of the workspace's git history.)

## 1. Status source: fetched once with plain curl, no retries
- URL: https://raw.githubusercontent.com/leanprover-community/physlib/master/Physlib/Relativity/LorentzGroup/Restricted/Basic.lean
- command: `curl -sS -A 'V3R1T4S skeptic (honest client)' -D headers -o page -w '%{http_code}' URL`, one attempt, with `date -u` taken immediately before and after
- fetched_utc: 2026-10-14T07:00:56Z (server `date: Wed, 14 Oct 2026 07:00:56 GMT`, `x-cache: MISS`)
- http_status: 200 (curl exit 0; 2937 bytes, 75 lines)
- sha256: e41850ba01879f3a9a6c3934efd85aab5b4a1a48c8d8a4621da63f7c5296f1c9. `cmp` shows the page is byte-identical to source/status_page_Restricted_Basic.lean.
- saved as: panel_work/novelty/page, panel_work/novelty/headers, panel_work/novelty/fetch_record.txt
- value, lines 61-63 of the page as fetched:
  `/-- The restricted Lorentz group is connected. -/`
  `semiformal_result "FXNL5" restricted_isConnected {d : ℕ} :`
  `  IsConnected (restricted d : Set (LorentzGroup d))`
- what this means: Physlib's Physlib/Meta/Informal/SemiFormal.lean is identical at the pinned commit and at current master. It defines a semiformal result as a "proof in which the proposition is given but not the proof" and says such results "act in a similar way to `proof_wanted`". They appear on Physlib's TODO list. The statement is therefore OPEN at my fetch.
- master has moved past the claim's commit. `git ls-remote` at 2026-10-14T07:03:54Z gives master 5f2136528e887a222a6be6ee5d04a3899450b255, committed 2026-10-14T06:29:48Z ("feat(CondensedMatter): crystals and unit cells (#1782)"); the claim was built against be0f21e5. I searched the whole tree of a depth-1 clone of that master (panel_work/novelty/physlib_master_search.txt):
  - FXNL5 and restricted_isConnected occur only on the semiformal_result line.
  - The file's sha256 equals the fetched page.
  - No IsConnected, IsPathConnected or ConnectedSpace statement anywhere concerns the restricted group, rotations or SO.
  - Master pins the same Mathlib, d13f23b723b8a846827a245b89c10fc7d3f11612.

## 2. Upstream pull requests (git only)
- Kit script tools/upstream_pr_scan.sh, read before running. It fetched into the pinned Physlib clone, which was already shallow; HEAD be0f21e5 and the working tree were unchanged afterwards. Run 2026-10-14T07:01:47Z to 07:01:52Z, output: `PR_SCAN: newest 300 PR heads (#1459..#1792): 0 match /(lemma|theorem) restricted_isConnected/ in Physlib/Relativity/LorentzGroup/Restricted/Basic.lean; 0 lack the file` (panel_work/novelty/pr_scan_restricted_basic.txt).
- Wider scan, covering other files and older PRs. I fetched all 1642 `refs/pull/*/head` refs (#1..#1792; 1639 unique heads), depth 1 and blob-less, into a scratch bare repo. I then fetched all 16125 unique .lean blobs from all heads and scanned them (panel_work/novelty/scripts/scan_pr_blobs.py; results in panel_work/novelty/pr_all_blobs_scan.txt, pr_scan_summary.txt and pr_all_blobs_sanity_lines.txt). Findings:
  - Every occurrence of restricted_isConnected or FXNL5 is the unproved semiformal_result (10 blob versions).
  - The only proved declarations that mention both "restricted" and "connected" are:
    - the conditional lemma restricted_eq_identity_component_of_isConnected, which takes `h1 : IsConnected …` as a hypothesis;
    - lemmas putting exp-map images in the identity component.
  - No PR head contains an IsConnected, IsPathConnected, ConnectedSpace or PathConnectedSpace statement about specialOrthogonalGroup, Rotations or SO.
  - Every version of the restricted-group file, across 7 historical paths (HepLean, PhysLean, Physlib), has either the FXNL5 placeholder or an older TODO (tag 6VZNU: "Prove restricted Lorentz group equivalent to connected component of identity").
- A public fork that came up in search, github.com/mkaxiomatic-ai/physlib (35 branches, 244 blobs not already covered): nothing (panel_work/novelty/fork_mkax_scan.txt).

## 3. Mathlib and other formal libraries
- Pinned Mathlib d13f23b7 (8529 files):
  - `Matrix.specialOrthogonalGroup` appears only in Mathlib/LinearAlgebra/UnitaryGroup.lean.
  - Under any name, there is no connected, path-connected or Joined result for specialOrthogonalGroup, orthogonalGroup, SO(n), SL or GL.
  - The only nearby results are `Unitary.*` (local path-connectedness of unitaries in complex C*-algebras) and `isPathConnected_sphere`.
  - Details: panel_work/novelty/local_sources_search.txt.
- Mathlib master a63713524b66f0b5681eaa2bfa83e7218c5cdbe5 (2026-10-14T06:34:27Z; all 9223 .lean files): the same, no connectedness for SO(n) (panel_work/novelty/mathlib_master_search.txt).
- What the claim adds:
  - Physlib already has `toBoostRotation : restricted d ≃ₜ Lorentz.Velocity d × Matrix.specialOrthogonalGroup (Fin d) ℝ` (Restricted/FromBoostRotation.lean) and `Velocity.isPathConnected`.
  - The missing piece was exactly the connectedness of SO(d). The object proves it from scratch with explicit paths between pairs of Householder reflections (`SO_pathConnectedSpace`).
  - So the claim is not a re-export of an existing library theorem.
- TauCeti, a public Lean library (HEAD 43e35ca3; all 14118 .lean files scanned):
  - PR #6186 (merged September 2026) proves geometric connectedness of the group scheme SO_n over fields of characteristic ≠ 2. That is algebraic-group (Hopf-algebra) connectedness. It is not topological connectedness of real SO(n), and it is not about the Lorentz group.
  - Its topological results are only for compact Spin(n): path-connected for n ≥ 2, simply connected for n ≥ 3.
  - Its Spin(3,1) ≅ SL₂(ℂ) result is algebraic.
  - It states no topological connectedness for SO(n) or for any Lorentz group (panel_work/novelty/tauceti_summary.txt, tauceti_connected_decls.txt).
- Logos Library (Lean Reservoir; github adambornemann-glitch/logos_library): HEAD e86790d8 contains no .lean files, only LICENSE and README.

## 4. Literature and web, last 24 months (WebSearch)
- Queries:
  - Lean 4 proof of restricted Lorentz group connectedness
  - Mathlib SO(n) path-connected
  - PhysLean Lorentz group connected component
  - "restricted_isConnected"; "FXNL5"
  - mathlib4 PRs on specialOrthogonalGroup connectedness
  - Lean Zulip on SO(n) connected / Householder reflections
  - Aristotle, AlphaProof or Gauss on PhysLean/Physlib
  - formal SO(n) path-connectedness in Isabelle, HOL Light, Coq or Lean
  - 2025-26 arXiv papers on Lean Lorentz-group formalization
- Result: I found no formal proof, in Lean or any other prover, that the restricted (proper orthochronous) Lorentz group is connected. I also found no Lean proof that real SO(n) is topologically connected.
- Relevant sources that do not prove it:
  - Tooby-Smith, arXiv 2411.07667 (index notation)
  - Lean Atlas, arXiv 2604.16347 (cites PhysLib's lorentzAlgebra.exp_mem_restricted_lorentzGroup)
  - Lean4PHYS (ICLR 2026)
  - PhysProver, arXiv 2601.15737
  - bend-packages issue #85 (opened 2026-09-30; a plan to port PhysLean's Lorentz group; no connectedness)
- Unreachable (DNS failure, one attempt each):
  - enuminous.substack.com (the EFMW–Aristotle post)
  - www.physatlas.ai (an index of Physlib theorems; I checked Physlib itself directly with git)
- Informal mathematics: connectedness of SO⁺(1,d) is a classical textbook result. An old HepLean docstring cites an informal proof in a Universitat de Barcelona thesis. The novelty here is that of a first formal Lean proof of an item Physlib records as wanted, not a new mathematical theorem.

## 5. V3R1T4S
- TROPHY_CASE.md (repo HEAD 9b1d444e): no entry mentions Lorentz, Physlib/PhysLean/HepLean, connectedness, restricted, semiformal, FXNL5, orthogonal or SO(.
- Pull requests:
  - `git ls-remote origin 'refs/pull/*/head'` at 2026-10-14T07:23:59Z returned 51 refs (PR 1..51).
  - I fetched all 51 heads, depth 1 and blob-less, into a scratch bare repo; the repo copy and its HEAD were not touched.
  - Paths: 0 of 23565 tree rows match lorentz|physlib|physlean|heplean|semiformal|restricted|connected|fxnl5.
  - Content: 0 of the 667 .lean/.md blobs match lorentz|physlib|physlean|FXNL5|restricted_isConnected|specialOrthogonalGroup.
  - Details: panel_work/novelty/v3r1t4s_check.txt.

## Limits
- The GitHub API and code search were not available. Forks other than the one surfaced by search cannot be enumerated with git alone.
- Only PR head commits were scanned, not intermediate commits within PRs.
- Lean Zulip was covered only through web search.
- Claim-folder slip, not a novelty issue: CLAIM.md says the status-page copy is saved in data/status_page_Restricted_Basic.lean. It is actually at source/status_page_Restricted_Basic.lean, with the same sha256 as my fetch.
- This verdict covers novelty only. Whether the proof is correct and reproducible is for the other skeptics.

novelty: FXNL5 is open upstream at my fetch (HTTP 200, 2026-10-14T07:00:56Z, sha256 e41850ba01879f3a9a6c3934efd85aab5b4a1a48c8d8a4621da63f7c5296f1c9), and still open at current master 5f213652. None of the following proves it: any upstream PR (#1..#1792), Mathlib (pinned or master), TauCeti, the surfaced fork, the V3R1T4S trophy case and PRs, or the literature. The claimed proof would be the first formal proof; it strictly beats everything known, and is not a tie.
pass: true
