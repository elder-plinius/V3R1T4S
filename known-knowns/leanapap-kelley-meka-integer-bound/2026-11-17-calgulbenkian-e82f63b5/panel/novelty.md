context: Claude Code subagent, fresh context [Sonnet 5.5]

Novelty skeptic report (read-only, all fetches logged in my own fetch log, not shipped in this package; times below are UTC and approximate to the minute of 2026-11-16/17).

Status source read once, no retries:
- https://raw.githubusercontent.com/YaelDillies/LeanAPAP/master/APAP/Integer.lean, HTTP 200. Value: `theorem int` is still `:= sorry` and still has the bug the claim fixes (C is introduced but the bound is `#A ≤ N / exp (...)` with no C). So upstream has no proof and has not corrected the statement.
- https://github.com/YaelDillies/LeanAPAP returned 301 (redirect, not followed as a retry; the content came through gh api instead).
- LeanAPAP master head via gh api: fb5cb9c4, 2026-11-13T21:23Z "bump mathlib to 2d833a6 (#29)". This matches the pinned commit in the claim, so the claim is against live master. The latest commits are only mathlib bumps and a Marcinkiewicz-Zygmund swap.
- APAP/Prereqs/Bohr/Regular.lean on master: `lemma regularity ... := sorry` still present (line 23).

LeanAPAP pull requests and issues (gh pr list, all states): nothing on the integer bound or Bohr sets. Open: #8, #9, #19 (Comparator CI for ff), #20 (NewMarcinkiewiczZygmund sorry-free). All recent merged ones are mathlib bumps or small prerequisites. Issue #25 is closed (2026-09-28), one comment, no fix. Releases are only old Lean-version tags (v4.17 to v4.21), no assets of relevance.

mean-fourier (YaelDillies/mean-fourier), head 6166075a, 2026-11-12: file tree has Defs, Doubling and Regular files in its BohrSet folder; Regular.lean still contains a `sorry` (line 34). Open PR #5 "feat: prove Bohr set regularity" (last updated 2026-11-11) is unmerged; an unmerged PR is not a bar under the review rule, but it shows someone is working on exactly the p1 partial win. No integer Kelley-Meka theorem there; no matching file names.

Mathlib: gh PR searches for Kelley-Meka, Bohr set, three-AP-free, Roth returned only unrelated PRs and the 2024 Salem-Spencer renames (#12682, #12701). Mathlib has Behrend's construction (lower bound) and the 3AP-free definitions, no Kelley-Meka upper bound. (The search tool matched loosely, so this is a moderate-strength negative.)

Other public Lean code (gh search code, one query each): "Kelley-Meka" gives only google-deepmind/formal-conjectures ErdosProblems/160.lean (statement with `sorry`, not a proof) and FawadHa1der/theorem-atlas KelleyMekaSpectralPositivityBridge (a toy arithmetic structure with `omega`; it states no 3AP bound and proves nothing about it, so it is not a formalisation). Koerbser/erdos-3-autolab cites Kelley-Meka as a published input behind a `sorry`, so it does not prove it. "BohrSet" hits: mean-fourier, YaelDillies/apap (same repo renamed), LeanPool QuadraticCarleson (Bohr sets for Carleson, a different statement, not Kelley-Meka regularity in the LeanAPAP sense), competemath/tengoku (mirror of LeanAPAP Bohr/Arc), TomasOrtega/Sidon. None is an integer 3AP-free exp-log bound. Searches for "ThreeAPFree" with exp and log found only Mathlib mirrors and the above. Search of GitHub repos by description gave nothing. I could not reach Zulip or blog announcements without a login via these tools, so that part is not covered.

V3R1T4S (elder-plinius/V3R1T4S): TROPHY_CASE.md mentions Lean only for Lehmer and nothing on LeanAPAP, Kelley-Meka or Bohr. known-knowns has no matching folder. Open and closed PR lists (200 each, the tool's cap I set; there may be more) have no title mentioning leanapap, Kelley, Bohr or apap; a gh search for "leanapap" in that repo returned nothing.

Literature: not searched beyond the above (no paper search tool used); the Kelley-Meka (2302.05537) and Bloom-Sisask (2302.07211) papers are the known informal sources and are not formalisations.

Conclusion: within what I could reach, no public Lean formalisation of the integer Kelley-Meka bound exists, LeanAPAP master and mean-fourier both still have the sorry, and the only competing work (mean-fourier PR #5 for Bohr regularity) is unmerged. Limits: PR list cap, no Zulip, loose search matching.

novelty: no known public formalisation beats or ties the claim; the claim is novel as of this check.

pass: true
