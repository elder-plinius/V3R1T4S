# NOVELTY verdict: physlib-gut-kernel-z6

context: subagent (fresh Agent-tool context; saw only claim/)
role: NOVELTY skeptic, run 2026-10-14-0616

(Saved by the run's main session from the skeptic's final message, verbatim apart from de-indentation; the skeptic
was told to return its verdict as text. Its scratch work is in runs/2026-10-14-0616/panel_work/novelty/.)

Claim checked: CLAIM.md. I recomputed the hashes below and they match CLAIM.md:
- object: object/InclSMKer.lean, sha256 0b2e9698935d6a53381d1015fdac67779ff1d6b9761358e79767391d12c1663d
- frozen statement: checker/spec_inclSM_ker.lean, sha256 685fe987fb3c56f5bb42c79116e7bb5c4375fef3794a6b67e37aa953f89afcea

Sources consulted beyond claim/ (only those the brief allows):
- the network: one status fetch, git traffic to GitHub, and WebSearch;
- repo/TROPHY_CASE.md and the V3R1T4S pull requests, via git;
- the Physlib/Mathlib sources in lean/physlib, read-only.

When I first used repo/, the harness showed that repository's one-line CLAUDE.md pointer to AGENTS.md. I did not open AGENTS.md or any other file in repo/.

novelty: NEW. Upstream Physlib still has `GeorgiGlashow.inclSM_ker` (tag 6V2W2), and the definitions it depends on (`inclSM`, `GaugeGroupI`), as informal declarations only. No public machine-checked proof of the statement was found. The mathematics is classical (Baez–Huerta, page 34 of guts.pdf); what is new is the formal proof against Physlib.

## 1. Status source (fetched once, no retries)
- URL: https://raw.githubusercontent.com/leanprover-community/physlib/master/Physlib/Particles/BeyondTheStandardModel/GeorgiGlashow/Basic.lean
- Command: `curl -sS -A 'V3R1T4S skeptic (honest client)' -D status_headers.txt -o status_page.lean -w '%{http_code}' URL`. curl exited with 0.
- Fetch time (`date -u`): 2026-10-14T07:00:54Z before, 2026-10-14T07:00:55Z after. Server `date:` header: Wed, 14 Oct 2026 07:00:55 GMT.
- HTTP status: 200. Response headers: content-length 1667, x-cache HIT, cache-control max-age=300, source-age 0.
- sha256: 34f66288e28cd4f26f1d2338bf092acb6dc5cd92ecd54fa2c129e3e567152682. This is byte-identical to the scout's copy, source/status_page_GeorgiGlashow_Basic.lean (diff is empty).
- Saved as: panel_work/novelty/status_page.lean, panel_work/novelty/status_headers.txt, panel_work/novelty/status_fetch_record.txt.
- The declarations are still informal (`grep -n` on the fetched page):
  ```
  29:informal_definition GaugeGroupI where
  31:  tag := "6V2WM"
  39:informal_definition inclSM where
  41:  tag := "6V2WS"
  47:informal_lemma inclSM_ker where
  49:  tag := "6V2W2"
  54:informal_definition embedSMℤ₆ where
  56:  tag := "6V2XA"
  ```
  No line matches `^(lemma|theorem) inclSM_ker|^(noncomputable )?def inclSM`.
- Cross-check against a stale CDN cache, done with git:
  - Upstream master is now 5f2136528e887a222a6be6ee5d04a3899450b255, committed 2026-10-14T06:29:48Z. That is newer than the claim's commit be0f21e5002d6d73b87f2055530c1e8bf7151546.
  - At both commits this file has blob 3598b5a3f565838a2204d5e62db88c49a7e1eef2.
  - That blob id equals `git hash-object` of the page I fetched, so the cached page matches current master.

## 2. Upstream pull requests (git only, no GitHub API)
**Kit scan.** I read the script first, then ran `sh tools/upstream_pr_scan.sh lean/physlib Physlib/Particles/BeyondTheStandardModel/GeorgiGlashow/Basic.lean '^(lemma|theorem) inclSM_ker|^(noncomputable )?def inclSM' 300` from 07:01:23Z to 07:01:27Z. Output:

`PR_SCAN: newest 300 PR heads (#1459..#1792): 0 match /^(lemma|theorem) inclSM_ker|^(noncomputable )?def inclSM/ in Physlib/Particles/BeyondTheStandardModel/GeorgiGlashow/Basic.lean; 0 lack the file`

The #1459 head is dated 2026-07-25 and the #1792 head 2026-10-14. Record: panel_work/novelty/pr_scan_physlib.txt.

**Beyond the kit window.** A pull request (PR) could predate #1459 or formalise the lemma in another file, so I also checked:
1. **Every PR head.** That is 1642 heads, #1 to #1792 (`refs/pull/*/head` listed at 07:03:00Z), and all were fetched.
   - The Georgi–Glashow file appears in 1477 heads, under 4 path layouts (HepLean/BeyondTheStandardModel, PhysLean/BeyondTheStandardModel, PhysLean/Particles/BeyondTheStandardModel, Physlib/Particles/BeyondTheStandardModel).
   - It has 14 distinct versions. I read all 14 in full: each has `informal_lemma inclSM_ker` and none has a formal lemma, theorem or def.
   - The only version unique to one PR (#1415) differs from master in one import line.
   - No other GUT-like path (georgi, glashow, gut, grandunif, inclsm) appears in any PR head.
   - Records: panel_work/novelty/all_pr_heads_scan.txt, gg_file_blobs.txt, gg_file_blobs_oldpaths.txt, gg_blobs/, gut_paths.txt, head_msgs_hits.txt.
2. **Open PRs.** I took each of the 53 open PRs' own changes from its merge ref (diff of M^1 against M).
   - I read 675 changed .lean files; none was unreadable.
   - The 39 keyword hits are umbrella `import …GeorgiGlashow.Basic` lines, #1415's file moves (the moved file is still informal), and unrelated `blockDiagonal` code.
   - None defines `inclSM` or proves the kernel.
   - Records: panel_work/novelty/open_pr_diff_scan.txt, open_pr_content_hits.txt.
3. **All Standard Model / BSM files.** I grepped every distinct version (729 blobs) of every StandardModel and BeyondTheStandardModel .lean file across all 1642 PR heads.
   - No version contains a formal `inclSM`, `embedSM` or SU(5)-matrix declaration.
   - Positive control, to show the grep works: 29 versions contain `informal_lemma inclSM_ker` and 24 contain `def gaugeGroupℤ₆SubGroup`.
   - Record: panel_work/novelty/sm_bsm_blob_scan.txt.
4. **Branches and tags.** All 61 upstream branches and tags contain only versions already read above (all informal). Record: panel_work/novelty/branch_gg_blobs.txt.

**Local sources.** I grepped Physlib at be0f21e (lean/physlib) and its pinned Mathlib (d13f23b723b8a846827a245b89c10fc7d3f11612).
- Neither has a formal `inclSM` or an SU(5) embedding.
- The Pati–Salam and Spin(10) analogues are also informal.
- Physlib's `SU5` folders cover F-theory charge bookkeeping, not this map.

## 3. Literature and web, last 24 months (Oct 2024 – Oct 2026)
**Searches.** I ran WebSearch queries on:
- proof assistants: Lean, Coq/Rocq, Isabelle, Agda;
- topics: the SM gauge group, SU(5), the ℤ₆ kernel, Georgi–Glashow;
- identifiers: inclSM_ker, gaugeGroupℤ₆SubGroup;
- projects and venues: Physlib, PhysLean, HepLean, Lean Zulip.

None found a machine-checked proof of the statement.
- The physics hits are pen-and-paper treatments: Baez–Huerta arXiv:0904.1556, nLab SU(5), arXiv 2102.13465, 1806.00612, 1611.09182, 2512.14839.
- The Lean-related hits are on other topics:
  - arXiv 2603.28406 (Krippendorf and Tooby-Smith, March 2026): classifies SU(5) F-theory charge spectra inside PhysLib, not the group embedding.
  - arXiv 2603.15770: free-field quantum field theory.
  - arXiv 2607.06379: the Seiberg–Witten solution.
  - arXiv 2601.15737: PhysProver.

**Lean projects that call themselves "machine-checked".** I inspected the two that searches surfaced via git: bare shallow clones in panel_work/novelty/ext/, only grepped, never built or run. Neither has a homomorphism into SU(5) or a ℤ₆ kernel. Record: panel_work/novelty/ext_repos_grep.txt.
- novaspivack/ugp-lean at c1b75b4d8cb5feab67ea00b4504b1110bd1cc4e6 (444 .lean files). Its `UgpLean/Algebra/SMGaugeGroup.lean` contains only ZMod 7 arithmetic and dimension counts.
- gift-framework/core at 2553ed170d04db8777f84fb2f9ef2b66b386f7fb. It only does dimension arithmetic such as `dim_SU5 : ℕ := 24`.

**Limitation.** The egress proxy refused direct reads of zenodo.org, researchsquare.com, novaspivack.com, synapsesocial.com and arxiv.org (CONNECT 403 or no response; panel_work/novelty/web_fetch_log.txt). I judged those from search summaries:
- The Lean code behind the Spivack preprints is ugp-lean, which I checked directly.
- Research Square rs-10349245 gives a Borel–de Siebenthal argument for S(U(3)×U(2)) ≅ G_SM/ℤ₆. Search summaries say it names no proof assistant.

## 4. V3R1T4S
- **Trophy case.** repo/TROPHY_CASE.md at repo HEAD 9b1d444eb864a1475e092047d49612a7410a7c5a has 53 rows in 7 families: degree-diameter graphs, constant-weight codes, matrix multiplication, Lehmer, VNN-COMP, RobustBench, sealed envelopes. None concerns Physlib, a GUT, SU(5) or this lemma.
- **Pull requests (git only).** 38 PRs (#1 to #38), each with head and merge refs, fetched blob-less and shallow. Results:
  - no PR-head tree has a path matching gut, georgi, glashow, su5, physlib, physlean, heplean or inclsm;
  - no head commit message mentions them;
  - none of the 778 added or modified files contains them; a check that those files could be read passed.
  - Record: panel_work/novelty/v3r1t4s_pr_scan.txt.

## 5. Notes (none changes the outcome)
- **Comparison.** Before this claim the statement existed only informally, so there is no earlier formal proof to tie or beat. A first proof strictly improves on that. The novelty is in the formalisation, not the mathematics.
- **Commit drift.** Upstream master has moved past the claim's commit (be0f21e to 5f21365), but this file is byte-identical, so the statement is still informal on current master.
- **Path typo in CLAIM.md.** The success-criterion paragraph cites the page copy as `data/status_page_GeorgiGlashow_Basic.lean`. The copy is actually at `source/status_page_GeorgiGlashow_Basic.lean`, as the status record says. Cosmetic only.
- **Side effects.**
  - Blob-less, shallow git fetches went into the object stores of lean/physlib and repo/, as the kit's own scan does.
  - No refs, HEADs or worktrees changed: Physlib HEAD is still be0f21e and repo HEAD is still 9b1d444, both clean.
  - No pushes, posts or contact with anyone.
- **Out of scope for NOVELTY.** I did not check whether the object compiles or whether the frozen spec is faithful to the informal lemma.

All scratch files are in panel_work/novelty/; the index is panel_work/novelty/novelty_evidence_index.txt.

pass: true
