# Novelty skeptic: Physlib `PatiSalam.inclSM_ker` (claim of run 2026-10-14-0701)

context: subagent (fresh context, Claude Code Agent tool)

I read only claim/ (CLAIM.md, REPRODUCE.md, MACHINE_NOTE.md, checker/, object/, source/), the V3R1T4S repository's
TROPHY_CASE.md, and what I fetched. The sha256 values of checker/lean_claim_check.py,
checker/spec_patisalam_inclSM_ker.lean, object/PatiSalamInclSMKer.lean and source/status_page_PatiSalam_Basic.lean match
CLAIM.md. Scratch files are under ../panel_work/novelty/; all paths here are relative to claim/. I took no outward
actions. I did not build or run the checker, because that is not part of the novelty check.

## 1. Status fetch

One request with plain curl, User-Agent `V3R1T4S-research-bot`, no retry.

- URL: https://raw.githubusercontent.com/leanprover-community/physlib/master/Physlib/Particles/BeyondTheStandardModel/PatiSalam/Basic.lean
- Time (UTC, `date -u`): sent 2026-10-15T07:24:15Z, completed 2026-10-15T07:24:16Z. The server's `date:` header was
  Thu, 15 Oct 2026 07:24:16 GMT.
- HTTP status: 200 (curl exit 0, 3370 bytes, `x-cache: MISS`, etag
  `d3df8ba3ae2136a847bdf8ccc8c97901ff1efa0585e7525242530443b959102d`).
- sha256: `060aeb499b68cd6b526f4b746f18cf44e65abc6e97ce5ef2a9866b0e2ed627d9`. This is the same value as in CLAIM.md's
  status record, and `cmp` shows the fetched file is byte-identical to source/status_page_PatiSalam_Basic.lean. The copy
  is saved as ../panel_work/novelty/status/PatiSalam_Basic.lean, next to headers.txt and fetch_record.txt.
- Quoted value (lines 49-55 of the fetched file):

```lean
/-- The kernel of the map `inclSM` is equal to the subgroup `StandardModel.gaugeGroupℤ₃SubGroup`.

See footnote 10 of https://arxiv.org/pdf/2201.07245 [ref: arxiv_2201_07245]
-/
informal_lemma inclSM_ker where
  deps := [``inclSM, ``StandardModel.gaugeGroupℤ₃SubGroup]
  tag := "6V2RQ"
```

- Status: **`PatiSalam.inclSM_ker` is still an `informal_lemma`, not proved, at Physlib master.**
  - Its dependencies `PatiSalam.GaugeGroupI` (6V2Q2) and `PatiSalam.inclSM` (6V2RH) are still `informal_definition`s.
  - Master was 76245c854e4827a1dd7f20d1c053b61219cc8fbb, committed 2026-10-15T05:18:10Z (PR #1778). This comes from a
    shallow clone at 07:25:55Z and `git ls-remote` at 07:26:18Z.
  - The file's git blob (990392e4aaba…) is the same at master, at the claim's build commit be0f21e5 and at its check
    commit 5f2136528e88. Both of those commits are ancestors of master.
  - Physlib/Particles/StandardModel/Basic.lean is also unchanged across the three commits.

## 2. Has anyone already formalised it?

### Physlib master, other files

I searched a shallow clone with `git grep`.

- `inclSM` occurs only in `informal_definition`/`informal_lemma` entries and their docstrings, in
  BeyondTheStandardModel/{PatiSalam,GeorgiGlashow,Spin10}/Basic.lean.
- `gaugeGroupℤ₃SubGroup` is formal only in Particles/StandardModel/Basic.lean. There it has its definition, a
  membership lemma, its inclusion in the ℤ₆ subgroup and in the center, normality, and the quotient. Otherwise it appears
  only in API-map.yaml and in the PatiSalam informal lemma.
- No Lean file uses `specialUnitaryGroup (Fin 4)`, and `SU(4)` appears only in informal docstrings.
- Tags 6V2Q2, 6V2RH and 6V2RQ occur only in the PatiSalam file.

### Physlib pull requests, all states

The git-level check covered every public ref:

- `git ls-remote` at 07:26:18Z listed 1653 `refs/pull/*/head` (up to #1803), 57 `refs/pull/*/merge` and 36
  branches.
- A mirror clone of all refs, taken 07:27:47Z to 07:27:53Z, holds 1653 PR heads, 36 branches, 25 tags and 9974
  commits.
- `git log --all -G 'inclSM|PatiSalam|Pati-Salam|gaugeGroupℤ₃SubGroup'` finds 54 commits.
  - Every added line that mentions `inclSM` is informal: informal headers, docstrings, deps lists, and dependency-graph
    or website data.
  - No commit in any ref ever adds a `theorem`/`lemma`/`def`/`abbrev`/`instance`/`structure` whose name contains
    inclSM, embedSM (the 2024 name of the map), PatiSalam or Pati.
- `-G 'specialUnitaryGroup \(Fin 4\)|unitaryGroup \(Fin 4\)|SU\(4\)'` finds 11 commits, all informal text, docs or graph
  data.
- `-G 'Fin 3 ⊕ Fin 1|\(Fin 4\) ℂ|fromBlocks'` on .lean files finds only Dirac gamma matrices, Wirtinger Hessians and
  the SM gauge-algebra basis.
- Across all ref tips there are 16 distinct versions of the PatiSalam file, under HepLean/, PhysLean/ and Physlib/
  paths.
  - 15 of them contain `informal_lemma inclSM_ker`.
  - The 16th, at the heads of PRs #161-#164 (Sept 2024), predates the lemma.
  - The 159 refs without the file are early PRs (#1-#160).

GitHub search of Physlib PRs (titles, bodies and comments):

- "PatiSalam": 0 results.
- "Pati-Salam": 1 result, #161 "feat: Informal Pati-Salam" (merged 2024-09-19), which is the informal original.
- "inclSM": 0 results. "6V2RQ": 0 results.
- Georgi/Glashow/GUT/"grand unified"/Spin10: #163 and #167 (2024, informal) and #1578 (unrelated).
- "BeyondTheStandardModel" and "gauge group": refactors, API maps and the SM gauge-group quotient API (#1275). None is
  about Pati-Salam.
- Open PRs: 55, the newest being #1803 (2026-10-15T05:17:59Z). No title concerns Pati-Salam or GUTs.

### Mathlib

- Master f0b4c8150aa0 (2026-10-15T03:31:02Z), shallow clone at 07:31:12Z. It has no Pati-Salam, inclSM,
  Georgi-Glashow or Standard Model gauge group content. The only near hit is "standard model with corners", which is a
  manifold term.
- `specialUnitaryGroup` is defined only in Mathlib/LinearAlgebra/UnitaryGroup.lean.
- A mathlib4 PR search for "Pati-Salam", "Standard Model gauge group" and PatiSalam returns 0 results.

### Elsewhere on GitHub

Code search covers the default branches of indexed public repositories.

- `inclSM_ker` finds 7 files:
  - Physlib's two informal files.
  - The cmu-l3/minictx-eval dataset entry `def PatiSalam.inclSM_ker : InformalLemma` (fetched once: 200, sha256
    c21f11fd…9d8c).
  - A vendored PhysLean copy in davidichalfyorov-wq/sct-theory with `informal_lemma inclSM_ker` (fetched once: 200,
    sha256 a3728cd9…1515).
  - Two Physlib website TODO lists.
- `PatiSalam` / `"Pati-Salam"` in Lean finds Physlib, the vendored copy, and four other repositories. None states this
  map or its kernel:
  - nickgou-nuke/info-geometry-lean: data-record propositions such as `spinLiftKernelCard = 2`.
  - JohnnyTeutonic/lean_proofs_sm: a rational Weinberg-ratio inequality.
  - ktynski/church-of-coherence: comments only.
  - GoldenPhysicsProject/GPPVerify (found through its PRs): per search snippets, hypercharge, charge-count and
    root-system files. Its only `specialUnitaryGroup` use is in an unrelated file.
- `"specialUnitaryGroup (Fin 4)"` in Lean: 0 results anywhere.
- `gaugeGroupℤ₃SubGroup` finds only Physlib and derived copies or exports: rainwangphy/aftd-platform,
  competemath/emissary-archangel, miniCTX, website data, and a 2024 Zulip thread. Repo-scoped searches found nothing:
  aftd-platform for Pati/inclSM/SU(4), and emissary-archangel for PatiSalam.
- The claim's own identifiers (psMatrix4, PatiSalamInclSMKer, spec_patisalam_inclSM_ker) and
  `"gaugeGroupℤ₃SubGroup" "fromBlocks"`: 0 results.
- Other proof assistants:
  - Coq (`.v`) "Pati-Salam": one comment in a speculative framework whose fields are `: True`.
  - Isabelle (`.thy`): 0 results.

PR search across all of GitHub:

- "inclSM_ker": 0. "PatiSalam": 0.
- The quarry id "physlib-gut-kernel-z6", "physlib-gut-kernel" and "gut-kernel-z6": 0.
- "Pati-Salam": 51 PRs, namely Physlib #161 and speculative-physics repositories. Judging by titles, none concerns this
  map's kernel, and none is in elder-plinius/V3R1T4S.

### Lean Zulip (leanprover-community/archive)

- The Physlib "Mini projects" thread was fetched once (200, sha256 6bb33c37…b111, 44 messages). It contains
  J. Tooby-Smith's proposal of 2025-01-22, "Properties of grand unified theory groups" (SU(5), Spin(10), Pati-Salam). No
  reply reports a formalisation.
- The 2024-09 thread "Help formalizing some properties of a group" is about defining the SM ℤ₃/ℤ₆ subgroups.

### V3R1T4S TROPHY_CASE.md

It lists six families and two cipher commitments, 53 rows in all. The families are degree-diameter graphs,
constant-weight codes, matrix multiplication, Lehmer, VNN-COMP and RobustBench. There is no Physlib, Lean-formalisation
or Pati-Salam entry.

### V3R1T4S open pull requests: blocked, not checked

- The GitHub MCP tool refused to list PRs for elder-plinius/V3R1T4S because that repository is not on this session's
  allow-list. It returned no data.
- One plain-curl request to https://github.com/elder-plinius/V3R1T4S/pulls at 2026-10-15T07:31:33Z got HTTP 403 from
  this session's egress proxy, not from GitHub. The 378-byte JSON body (sha256 b3e03aaa…cda3) said "GitHub access to this
  repository is not enabled for this session". I did not retry, and I tried no other route to that repository.
- There is only indirect evidence. The GitHub-wide PR searches above do reach public repositories (they return Physlib
  #161), and they found no PR anywhere mentioning PatiSalam, inclSM_ker or the quarry id. This does not cover a private
  or unindexed V3R1T4S PR.

### Literature, last 24 months

I ran 7 web searches covering:

- Physlib/PhysLean/HepLean together with Pati-Salam or inclSM_ker;
- Lean or other proof-assistant formalisations of Pati-Salam or of GUT gauge-group kernels;
- Physlib autoformalisation benchmarks;
- V3R1T4S together with Physlib.

Findings:

- I found no formal proof (Lean, Coq or Isabelle) of this statement.
- The mathematics is classical:
  - Baez-Huerta, arXiv:0904.1556. Page 54 of Baez's GUT notes is Physlib's reference for the map.
  - arXiv:2201.07245, footnote 10, is Physlib's reference for the kernel.
  - The 2025 physics paper arXiv:2507.01777 restates that the Standard Model group embeds in Pati-Salam modulo ℤ₃.
- The other hits do not touch GUT groups: Lean4Physics, LeanFlow (arXiv:2607.20503) and HepLean (arXiv:2405.08863).
- Three arXiv abstract pages (2607.20503, 2603.28406, 2608.28639) were refused by the session egress proxy at
  2026-10-15T07:34:35Z (CONNECT 403; nothing reached arXiv). I did not retry them.

## 3. Request log and blocks

All requests used plain clients with no browser User-Agent.

- raw.githubusercontent.com (curl, `V3R1T4S-research-bot`), all 200:
  - the status page, 07:24:15Z;
  - the Zulip archive JSON, 07:33:22Z;
  - the miniCTX jsonl, 07:33:42Z;
  - the sct-theory file, 07:33:42Z.
- github.com over git, read-only. These were three separate operations on the same repository, none of them after a
  block:
  - physlib shallow clone, 07:25:55Z;
  - physlib `ls-remote`, 07:26:18Z;
  - physlib mirror clone, 07:27:47Z.
  - In addition, a mathlib4 shallow clone at 07:31:12Z.
- GitHub search via the GitHub MCP tool: the distinct code and PR queries listed above, all answered. The PR listing for
  elder-plinius/V3R1T4S was refused by the tool.
- **Blocked:**
  - github.com/elder-plinius/V3R1T4S/pulls: 403 from the session proxy.
  - Three arxiv.org abstract pages: proxy CONNECT 403.
  - The `gh` CLI reported its token invalid at `gh auth status`, so I did not use it.
  - None of these were retried.

## 4. Notes for the panel (not novelty failures)

1. Novelty here means novelty as a first formal (Lean 4) proof. The mathematics itself is classical, as shown above.
2. The claim is filed under quarry `physlib-gut-kernel-z6`. That quarry's lemma, `GeorgiGlashow.inclSM_ker` (tag 6V2W2,
   kernel ℤ₆), is still an informal lemma at master (GeorgiGlashow/Basic.lean line 47), and this claim does not address
   it. Whether a Pati-Salam follow-on may count under that id is a charter question, outside novelty.
3. MACHINE_NOTE.md says the build commit be0f21e5 is not on the panel machine. For novelty this does not matter: the
   PatiSalam file, StandardModel/Basic.lean and GeorgiGlashow/Basic.lean have identical blobs at be0f21e5, 5f2136528e88
   and master 76245c85.

## 5. Verdict

Novelty is confirmed as far as this session can check it.

- At the status fetch (200, 2026-10-15T07:24:15Z), `PatiSalam.inclSM_ker` is still an informal lemma at Physlib
  master.
- No formal proof of the same statement exists in any of these places:
  - Physlib master;
  - any of Physlib's 1653 PR heads (open, closed or merged), 36 branches or 25 tags;
  - Mathlib;
  - GitHub-indexed code or pull requests;
  - the Lean Zulip archive;
  - the literature of the last 24 months.
- TROPHY_CASE.md has no such entry.
- Nothing ties this result, so a kernel-checked proof would be strictly new.

The one gap is the V3R1T4S open-PR list. The session proxy blocked it; the block is recorded above and was not
retried. Before publishing, the main session should confirm that no open V3R1T4S PR already carries this lemma. If one
does, this claim is a tie and this verdict becomes fail.

pass: true
