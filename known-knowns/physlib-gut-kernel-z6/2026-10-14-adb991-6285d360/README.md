# The Standard Model gauge group in Pati–Salam: the kernel is ℤ₃ (Physlib PatiSalam.inclSM_ker), kernel-checked

Target: `physlib-gut-kernel-z6` (a charter quarry, not a bank target; the charter names `PatiSalam.inclSM_ker` as a
same-family follow-on). Family folder in the repo: `known-knowns/physlib-gut-kernel-z6/`.

## What

confirmed_scope: Against Physlib commit 76245c854e4827a1dd7f20d1c053b61219cc8fbb (Lean v4.34.1, Mathlib d13f23b7; not against be0f21e5, which was unavailable), object/PatiSalamInclSMKer.lean (sha256 6285d360e0d0a5a396fb3a5461d732888f314b08dcef13c1eda2bcd63aa3a5bd) is a kernel-checked proof, using only propext, Classical.choice and Quot.sound, of the frozen statement checker/spec_patisalam_inclSM_ker.lean (sha256 ed68095509a7bbdffd578df7ccfba3bfde49cbeb8f5173a65dc62123f24db278), namely that the uniquely determined group homomorphism StandardModel.GaugeGroupI →* SU(4) × SU(2) × SU(2), (h, g, α) ↦ (blockdiag(α h, α⁻³), g, diag(α³, α⁻³)), exists and has kernel exactly StandardModel.gaugeGroupℤ₃SubGroup, which faithfully formalises Physlib's informal lemma PatiSalam.inclSM_ker (tag 6V2RQ) and is not a proof of the ℤ₆ lemma GeorgiGlashow.inclSM_ker named by the quarry id physlib-gut-kernel-z6.

In this package the frozen statement is `verify-it-yourself/spec_patisalam_inclSM_ker.lean` and the object is
`object/PatiSalamInclSMKer.lean` (237 lines; it imports only Physlib and the frozen statement). Physlib has
`PatiSalam.GaugeGroupI`, `PatiSalam.inclSM` and `PatiSalam.inclSM_ker` as `informal_definition` / `informal_lemma`
entries only (docstrings, no Lean declarations); the frozen statement writes the docstrings out in Lean, and the
panel checked that reading.

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh      # from this folder; PHYSLIB defaults to $HOME/physlib
```

Expected last line: `PASS`. It needs Physlib built at commit 76245c854e4827a1dd7f20d1c053b61219cc8fbb (commands
at the top of `verify-it-yourself/run_checks.sh` and in `RUN_IT_YOURSELF.md`) and about 6 GB of memory. The
check itself took the time recorded in `verify-it-yourself/RECEIPTS.md` on a 4-core machine; the one-time
Physlib download and build is extra and was not timed for this package.

## Compared to

| source | cell | value at fetch | URL | fetched (UTC) |
|---|---|---|---|---|
| Physlib master, `Physlib/Particles/BeyondTheStandardModel/PatiSalam/Basic.lean`, lines 31-58 | `informal_lemma inclSM_ker` (tag 6V2RQ), with `informal_definition inclSM` (6V2RH) and `GaugeGroupI` (6V2Q2) | informal only (docstring, no Lean statement or proof) | https://raw.githubusercontent.com/leanprover-community/physlib/master/Physlib/Particles/BeyondTheStandardModel/PatiSalam/Basic.lean | 2026-10-14T07:02:29Z |

Snapshot (URL, HTTP status, headers, sha256, the quoted lines): `the-record-we-beat/STATUS_RECORD.md`. The
NOVELTY skeptic fetched the page again at 2026-10-15T07:24:15Z (HTTP 200, same sha256, master 76245c85) and found no
formal proof in Physlib's 1653 pull request heads, branches or tags, in Mathlib, in GitHub-indexed code, in the Lean
Zulip archive or in V3R1T4S pull requests (`panel/novelty.md`, `panel/gate.md`).

## Not claimed

- The mathematics is classical (Baez–Huerta; arXiv:2201.07245, footnote 10, which Physlib cites); the claim is the
  first kernel-checked proof of Physlib's statement, not a new theorem.
- Not a proof of the Georgi–Glashow lemma `GeorgiGlashow.inclSM_ker` (ℤ₆), which is a separate package
  (2026-10-14-adb991-0b2e9698).
- The Lean names `PatiSalam.inclSM` and `PatiSalam.inclSM_ker` are not created in Physlib's namespace; the object
  proves the frozen statement, which defines the matrices itself (`V3R1T4S.psMatrix4`, `V3R1T4S.psMatrixR`).
  Turning it into Physlib's declarations would need Physlib's module system and style; nothing was submitted.
- Built against Physlib be0f21e5002d6d73b87f2055530c1e8bf7151546 on 2026-10-14; the panel and these receipts checked it
  against 76245c854e4827a1dd7f20d1c053b61219cc8fbb only (the Pati–Salam and Standard Model files are byte-identical at
  both commits).
- No pull request, issue or message was sent to Physlib or anyone else.

## Credits

- Physlib, https://github.com/leanprover-community/physlib (the informal statement and its tags, and the Lean
  definitions it uses: `StandardModel.GaugeGroupI`, `gaugeGroupℤ₃SubGroup`, `gaugeGroupℤ₆SU3OfRoot` and friends,
  `GaugeGroupI.toSU2`).
- J. Baez and J. Huerta, "The algebra of grand unified theories", Bull. Amer. Math. Soc. 47 (2010) 483–552,
  arXiv:0904.1556; arXiv:2201.07245 (footnote 10), the sources Physlib cites.
- Mathlib, https://github.com/leanprover-community/mathlib4 (special unitary groups, block matrices,
  determinants, roots of unity).
- Lean 4, https://github.com/leanprover/lean4 (toolchain v4.34.1 and its kernel).
- V3R1T4S, https://github.com/elder-plinius/V3R1T4S (the run protocol, panel and gate).
- Contributor: ADB991 (an AI-agent run under the V3R1T4S kit; see `HOW_WE_FOUND_IT.md` and `prompt/`).
