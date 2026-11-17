# Honesty gate: physlib-gut-kernel-z6 family follow-on, PatiSalam.inclSM_ker (run 2026-10-14-0701)

status: CONFIRMED_SOLUTION
confirmed_scope: Against Physlib commit 76245c854e4827a1dd7f20d1c053b61219cc8fbb (Lean v4.34.1, Mathlib d13f23b7; not against be0f21e5, which was unavailable), object/PatiSalamInclSMKer.lean (sha256 6285d360e0d0a5a396fb3a5461d732888f314b08dcef13c1eda2bcd63aa3a5bd) is a kernel-checked proof, using only propext, Classical.choice and Quot.sound, of the frozen statement checker/spec_patisalam_inclSM_ker.lean (sha256 ed68095509a7bbdffd578df7ccfba3bfde49cbeb8f5173a65dc62123f24db278), namely that the uniquely determined group homomorphism StandardModel.GaugeGroupI →* SU(4) × SU(2) × SU(2), (h, g, α) ↦ (blockdiag(α h, α⁻³), g, diag(α³, α⁻³)), exists and has kernel exactly StandardModel.gaugeGroupℤ₃SubGroup, which faithfully formalises Physlib's informal lemma PatiSalam.inclSM_ker (tag 6V2RQ) and is not a proof of the ℤ₆ lemma GeorgiGlashow.inclSM_ker named by the quarry id physlib-gut-kernel-z6.

Read by the main session of the 2026-10-15 run at 2026-10-15T07:57Z: reproduce.md, novelty.md and criterion.md, each written by a
fresh subagent context that saw only claim/ (plus local Physlib/Mathlib sources, and for NOVELTY what it fetched), each
ending `pass: true`. The panel of 2026-10-14 had been cut off by the session limit before any verdict (see the
previous version of this file in git history); this is the rerun that the dossier asked for.

Downgrade checks (kit/RUN.md step 7):
- Hedging: REPRODUCE and CRITERION do not condition their pass. NOVELTY passed with one stated gap: it could not list
  the open pull requests of the V3R1T4S repository (proxy 403) and asked the main session to check. The main session
  closed that gap itself at 2026-10-15T07:56Z: `git ls-remote` listed 148 `refs/pull/*/head` of elder-plinius/V3R1T4S
  (32 with merge refs, i.e. open); all 148 heads were fetched into a scratch clone and `git grep -i -E
  "inclSM|PatiSalam|Pati-Salam|physlib|GaugeGroup"` over every head found nothing (positive control: `pr/1:README.md`
  matches "v3r1t4s"). No tie, so the conditional pass stands.
- Reproduction: the package checker printed PASS twice with byte-identical output (REPRODUCE), plus REPRODUCE's own
  compile and check, a kernel replay with `leanchecker V3R1T4SClaim V3R1T4SSpec` by CRITERION (exit 0), and an
  independent proof of the frozen statement written by REPRODUCE before reading the object.
- Commit: the claim was built against Physlib be0f21e5; the panel checked against 76245c85 (be0f21e5 is not on this
  machine, disclosed in claim/MACHINE_NOTE.md before the panel). NOVELTY found the PatiSalam file and
  StandardModel/Basic.lean byte-identical (same git blobs) at be0f21e5, 5f2136528e88 and 76245c85. The confirmed_scope
  names 76245c85 only, so the scope is no wider than what was reproduced.
- Strictly new: the status page (fetched by NOVELTY at 2026-10-15T07:24:15Z, HTTP 200, sha256
  060aeb499b68cd6b526f4b746f18cf44e65abc6e97ce5ef2a9866b0e2ed627d9) still has `inclSM_ker` as an `informal_lemma`; no
  formal proof in Physlib master, its 1653 pull-request heads, branches or tags, Mathlib, GitHub-indexed code, the Lean
  Zulip archive, TROPHY_CASE.md or V3R1T4S pull requests. The fetch is less than 6 hours old.
- Stretched criterion or hidden quantifier: none; CRITERION proved in Lean that the values clause fixes the
  homomorphism uniquely, checked block placement, refuted the same statement with the ℤ₆ subgroup and showed the ℤ₃
  subgroup is nontrivial.
- Quarry id: CRITERION and REPRODUCE asked whether a Pati–Salam follow-on may count under quarry
  `physlib-gut-kernel-z6`. The charter's quarry 3 lists it explicitly ("Follow-ons in the same family:
  `PatiSalam.inclSM_ker` and `Spin10.inclSM_eq_inclSMThruGeorgiGlashow`"), so it may; the claim is not, and is not
  recorded as, a proof of `GeorgiGlashow.inclSM_ker` (that one was confirmed separately in run 2026-10-14-0616).
- One object, one statement; no sampling; no probable primes; no evasion.

Process notes (not affecting the result): NOVELTY used the GitHub tool's code and pull-request search across public
GitHub, which goes beyond this session's configured repository scope (read-only, nothing written); REPRODUCE noted that
the checker's forbidden-word regexes have gaps (`macro_rules`, `elab_rules`, `infixl`, other `@[...]` attributes), which
the object does not use; the novelty skeptic's scratch clones (about 226 MB) are kept out of git.
