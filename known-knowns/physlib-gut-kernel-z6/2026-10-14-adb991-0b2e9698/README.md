# The Standard Model gauge group in SU(5): the kernel is ℤ₆ (Physlib GeorgiGlashow.inclSM_ker), kernel-checked

Target: `physlib-gut-kernel-z6` (a charter quarry, not a bank target). Family folder in the repo:
`known-knowns/physlib-gut-kernel-z6/`.

## What

confirmed_scope: Against Physlib be0f21e5002d6d73b87f2055530c1e8bf7151546 with Lean v4.34.1, object/InclSMKer.lean kernel-checks, using only the axioms propext, Classical.choice and Quot.sound, the frozen statement checker/spec_inclSM_ker.lean, a literal and unweakened formalisation of Physlib's informal lemma GeorgiGlashow.inclSM_ker (tag 6V2W2) with its informal dependencies GaugeGroupI (6V2WM) and inclSM (6V2WS), which asserts that the map StandardModel.GaugeGroupI = SU(3) × SU(2) × U(1) → Matrix.specialUnitaryGroup (Fin 5) ℂ sending (h, g, α) to blockdiag(α^3 g, α^(-2) h) (2×2 block on indices 0,1, 3×3 block on indices 2,3,4) is a group homomorphism, necessarily the unique one with these values, whose kernel equals StandardModel.gaugeGroupℤ₆SubGroup.

In this package the frozen statement is `verify-it-yourself/spec_inclSM_ker.lean` and the object is
`object/InclSMKer.lean` (141 lines; it imports only Physlib and the frozen statement). Physlib has `inclSM` and
`inclSM_ker` as `informal_definition` / `informal_lemma` entries only (docstrings, no Lean declarations); the
frozen statement writes the docstrings out in Lean, and the panel checked that reading.

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh      # from this folder; PHYSLIB defaults to $HOME/physlib
```

Expected last line: `PASS`. It needs Physlib built at commit be0f21e5002d6d73b87f2055530c1e8bf7151546 (commands
at the top of `verify-it-yourself/run_checks.sh` and in `RUN_IT_YOURSELF.md`) and about 6 GB of memory. The
check itself took the time recorded in `verify-it-yourself/RECEIPTS.md` on a 4-core machine; the one-time
Physlib download and build is extra and was not timed for this package.

## Compared to

| source | cell | value at fetch | URL | fetched (UTC) |
|---|---|---|---|---|
| Physlib master (commit be0f21e5002d6d73b87f2055530c1e8bf7151546), `Physlib/Particles/BeyondTheStandardModel/GeorgiGlashow/Basic.lean`, lines 28-49 | `informal_lemma inclSM_ker` (tag 6V2W2), with `informal_definition inclSM` (6V2WS) and `GaugeGroupI` (6V2WM) | informal only (docstring, no Lean statement or proof) | https://raw.githubusercontent.com/leanprover-community/physlib/master/Physlib/Particles/BeyondTheStandardModel/GeorgiGlashow/Basic.lean | 2026-10-14T06:16:29Z |

Snapshot (URL, HTTP status, headers, sha256, the quoted lines): `the-record-we-beat/STATUS_RECORD.md`. The
NOVELTY skeptic fetched the page again at 2026-10-14T07:00:55Z (same sha256) and found no formal proof in any of
Physlib's 1642 pull request heads (`panel/novelty.md`).

## Not claimed

- The mathematics is classical (Baez–Huerta, below); the claim is the first kernel-checked proof of Physlib's
  statement, not a new theorem.
- The Lean names `inclSM`, `GaugeGroupI` and `inclSM_ker` are not created in Physlib's namespace; the object proves
  the frozen statement, which defines the matrix map itself (`V3R1T4S.inclSMMatrix`). Turning it into Physlib's
  declarations would need Physlib's module system and style; nothing was submitted.
- Checked against Physlib be0f21e5002d6d73b87f2055530c1e8bf7151546 with Lean v4.34.1 only.
- The bonus in `how-we-built-it/lean/EmbedZ6.lean` (Physlib's next informal definition `embedSMℤ₆`, the induced
  injective hom `StandardModel.GaugeGroupℤ₆ →* SU(5)`) compiled with standard axioms in the run but was not
  reviewed by the panel and is not part of this claim.
- No pull request, issue or message was sent to Physlib or anyone else.

## Credits

- Physlib, https://github.com/leanprover-community/physlib (the informal statement and its tags, and the Lean
  definitions it uses: `StandardModel.GaugeGroupI`, `gaugeGroupℤ₆SubGroup`, `gaugeGroupℤ₆OfRoot`).
- J. Baez and J. Huerta, "The algebra of grand unified theories", Bull. Amer. Math. Soc. 47 (2010) 483–552,
  arXiv:0904.1556 (the source Physlib cites, page 34 of the notes).
- Mathlib, https://github.com/leanprover-community/mathlib4 (special unitary groups, block matrices,
  determinants, roots of unity).
- Lean 4, https://github.com/leanprover/lean4 (toolchain v4.34.1 and its kernel).
- V3R1T4S, https://github.com/elder-plinius/V3R1T4S (the run protocol, panel and gate).
- Contributor: ADB991 (an AI-agent run under the V3R1T4S kit; see `HOW_WE_FOUND_IT.md` and `prompt/`).
