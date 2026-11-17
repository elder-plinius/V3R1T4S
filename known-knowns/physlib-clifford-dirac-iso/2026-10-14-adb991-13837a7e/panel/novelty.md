# NOVELTY verdict: physlib-clifford-dirac-iso (run 2026-10-14-0615)

context: subagent (fresh Agent-tool context; saw only claim/)
role: NOVELTY skeptic. Kit rule: fetch the status page once, honestly (no retries; a block means fail); search the last 24 months of literature, this repo's TROPHY_CASE.md and open pull requests; pass only if the result strictly beats everything known; a tie is not a record.
claim under test (`CLAIM.md`): `Function.Injective spaceTime.γ.ofCliffordAlgebra` (frozen in `checker/spec_ofCliffordAlgebra_injective.lean`, object `object/OfCliffordAlgebraInjective.lean`), closing Physlib's TODO "Prove injectivity of ofCliffordAlgebra and construct the full isomorphism."

(Saved by the run's main session from the skeptic's final message, verbatim apart from de-indentation; the skeptic
was told to return its verdict as text. Its scratch work is in runs/2026-10-14-0615/panel_work/novelty/.)

## 1. Status source (fetched once, no retries)
- URL: https://raw.githubusercontent.com/leanprover-community/physlib/master/Physlib/Relativity/CliffordAlgebra.lean
- command: `curl -sS -A 'V3R1T4S skeptic (honest client)' -D headers -o page -w '%{http_code}' URL`, 1 attempt, curl exit 0
- HTTP status: 200 (`HTTP/2 200`, content-length 9878)
- UTC fetch time: 2026-10-14T07:00:56Z (`date -u` 07:00:55Z before, 07:00:56Z after; server header `date: Wed, 14 Oct 2026 07:00:56 GMT`)
- sha256 of the page: 70ca93d773d8a8f2c2fe43e607125ae1d3042d7530bace4371cd5eba5bf8de0d. It is byte-identical to the scout's copy `source/status_page_CliffordAlgebra.lean` (fetched 06:16:28Z). Its git blob id is 23b8c442957b7a3c963abbcaf5e2e2ffe1d38cd6.
- The TODO is still open. Line 40 of the page reads `TODO "Prove injectivity of ofCliffordAlgebra and construct the full isomorphism."` Lines 32-34 read `## TODO` / `- Complete the isomorphism by proving injectivity of `ofCliffordAlgebra` (requires dimension theory)`.
- Corroboration:
  - `git ls-remote` at 07:02:41Z shows upstream master at 5f2136528e887a222a6be6ee5d04a3899450b255 (2026-10-14T06:29:48Z, #1782). Its parent is the claim's pinned be0f21e5002d6d73b87f2055530c1e8bf7151546.
  - That commit changes only 3 unrelated files (CondensedMatter/Crystal, references.bib, a lint list). The CliffordAlgebra.lean blob is identical (23b8c442…).
  - Physlib's `Physlib/Relativity/Fermions/Dirac/API-map.yaml` on master says: "The API shall contain the isomorphism between the Clifford algebra of `diracForm` and `diracAlgebra` (blocked: needs injectivity of `ofCliffordAlgebra` …)", with `done: false`.
  - At the pinned commit, `ofCliffordAlgebra` occurs only in its own file. The strongest result there is `ofCliffordAlgebra_surjective`.
- records: `panel_work/novelty/fetch_record.txt`, `panel_work/novelty/headers`, `panel_work/novelty/page`, `panel_work/novelty/master_vs_pinned_files.txt`

## 2. Upstream pull requests (git only, no GitHub API)
- Kit scan, 07:01:46-07:01:51Z: `sh tools/upstream_pr_scan.sh lean/physlib Physlib/Relativity/CliffordAlgebra.lean '(lemma|theorem) ofCliffordAlgebra_injective|ofCliffordAlgebra_bijective|≃ₐ\[ℝ\]' 300`
  - output: `PR_SCAN: newest 300 PR heads (#1459..#1792): 0 match /(lemma|theorem) ofCliffordAlgebra_injective|ofCliffordAlgebra_bijective|≃ₐ\[ℝ\]/ in Physlib/Relativity/CliffordAlgebra.lean; 0 lack the file`
  - record: `panel_work/novelty/pr_scan_physlib.txt`
- Extended scan of all 1731 upstream refs: 1642 `refs/pull/*/head`, 53 `refs/pull/*/merge` and 36 branches (list in `panel_work/novelty/physlib_ls_remote.txt`). I used blob-less fetches into a scratch bare repo, so nothing more was written into the Physlib clone. Results:
  - **Clifford-named files:** I checked every path matching /clifford/i in every ref, across the HepLean, PhysLean and Physlib eras (45 distinct file versions). None contains `ofCliffordAlgebra_injective` or `_bijective`, `≃ₐ`, an injectivity lemma, `finrank` or `Module.rank`. All 32 versions of the Dirac Clifford file carry a TODO. Records: `panel_work/novelty/pr_scan_extended_clifford_paths.txt`, `panel_work/novelty/pr_scan_clifford_blobs_by_ref.txt`.
  - **Dirac `API-map.yaml`:** I checked it in all 318 refs that have it (3 versions). The isomorphism entry is `done: false` in every one. Record: `panel_work/novelty/pr_scan_open_merge_refs.txt` (scope A).
  - **Open PRs:** across the 53 merge refs and 730 changed files, no added line names `ofCliffordAlgebra`, `diracAlgebra` or `diracForm`. The 12 Clifford hits are generic Mathlib `CliffordAlgebra` API in PR #1415. Record: same file (scope B).
  - **New modules:** I checked the root import file of every ref (600 versions). The only Clifford, Dirac or gamma modules not in the pin come from PRs #1383-#1397 and #1415. I grepped all 529 versions of those files: 0 mention `ofCliffordAlgebra` or `diracAlgebra`. PR #1385's `CliffordPinReflection.lean` uses `CliffordAlgebra diracForm` only for the Clifford relation and pin reflections. Records: `panel_work/novelty/pr_scan_root_imports.txt`, `panel_work/novelty/pr_scan_extra_modules_hits.txt`.
- Shared-clone hygiene: my only write to the Physlib clone was the kit script's fetch, which touches only the object store and the shallow file. The clone's HEAD (be0f21e5…) and worktree are unchanged. Its FETCH_HEAD (07:03:30Z, the newest 200 heads), refs (07:13:26Z) and shallow file (07:16:42Z) were changed later by concurrent processes, not by this skeptic.

## 3. Literature and web (last 24 months and older), and pinned Mathlib
- I ran 14 WebSearch queries between 07:05Z and 07:24Z (listed in `panel_work/novelty/literature_search.txt`).
  - None found a formal proof, in Lean, Coq/Rocq, Isabelle, HOL Light or Agda, of the injectivity of `ofCliffordAlgebra`. None found one of Cl(1,3) ≅ the real algebra generated by the Dirac matrices.
  - Searches for the exact identifiers (`ofCliffordAlgebra_injective`, `_bijective`) and for the TODO text return nothing.
- Leads inspected with git (shallow clones, grep only, since removed):
  - `lizr-phys/physlib-quantum-physics` is a Physlib fork. Its HEAD (98f10bce…) and branch `feat/dirac-gamma-endomorphisms` (1e8f4db6…) still carry the TODO, and the API-map says `done: false`.
  - `eic/EpsilonEridani` HEAD b8c78e96… extends Physlib's gamma matrices with anticommutator and slash identities. It never mentions `ofCliffordAlgebra`, `diracAlgebra` or `diracForm`.
- Wieser & Song, "Formalizing Geometric Algebra in Lean" (AACA 2022) formalizes general Clifford algebras. It is older than 24 months and has no Cl(1,3)/Dirac isomorphism.
- Pinned Mathlib d13f23b723b8a846827a245b89c10fc7d3f11612:
  - It has no ready-made `finrank` or `Module.rank` for a Clifford or exterior algebra.
  - The ingredients exist: `Module.Basis.ExteriorAlgebra` (added 2026-03-06, Mathlib #35424) and `CliffordAlgebra.equivExterior`. The object uses exactly these.
  - `CliffordAlgebra/Equivs.lean` covers only the ring, ℂ, quaternion and dual-number cases.

## 4. V3R1T4S
- `TROPHY_CASE.md` (sha256 b4f3ad52f6587e5aefdc3b555db200d99543e6b500c805012226f2042cdcc412, 53 rows) has no Physlib, Clifford, Dirac or gamma-matrix entry. The local HEAD 9b1d444e… equals remote main.
- I listed the 51 PR heads with `git -C repo ls-remote origin 'refs/pull/*/head'`, fetched them blob-less and shallow into a scratch repo, and ran `git ls-tree -r --name-only`.
  - 0 paths match clifford|physlib|physlean|heplean|dirac|gamma, and no PR adds a `.lean` file.
  - The PRs are tooling fixes and claims about fmm, constant-weight codes and erdos757.
  - The repo's checked-out HEAD did not move.
  - Record: `panel_work/novelty/v3r1t4s_trophy_and_prs.txt`.

## Assessment
- The TODO was open at my fetch and is open on current upstream master. Nothing found proves the injectivity of `ofCliffordAlgebra`: no upstream PR (open or closed, in any era), branch, inspected fork, paper, web page, Mathlib lemma or V3R1T4S trophy or PR. Nothing known ties it. A kernel-checked proof would go strictly beyond the known state, which is surjectivity only.
- Scope notes (not novelty failures):
  - (a) The novelty lies in the formalization. The mathematics (dim Cl(1,3) = 16 = dim of the real span of the 16 gamma monomials) is textbook, and Mathlib has supplied the dimension ingredients since 2026-03.
  - (b) The claim covers injectivity. The TODO's second half, constructing the full `AlgEquiv`, follows in one line from this plus the existing surjectivity (`AlgEquiv.ofBijective`), but the object does not state it.
  - (c) `CLAIM.md` once calls the saved copy `data/status_page_CliffordAlgebra.lean`. The file is actually at `source/status_page_CliffordAlgebra.lean`, and its sha256 matches.
- This verdict covers novelty only. Whether the object proves the frozen statement is for the other panel members.
- Disclosure: to diagnose the change to the shared Physlib clone I listed running processes (`ps`), which showed other panel processes' command lines. I read no file outside claim/, the allowed sources and my own scratch folder.

novelty: PASS. TODO open at 2026-10-14T07:00:56Z (HTTP 200, sha256 70ca93d773d8a8f2c2fe43e607125ae1d3042d7530bace4371cd5eba5bf8de0d); no prior proof found.
pass: true
