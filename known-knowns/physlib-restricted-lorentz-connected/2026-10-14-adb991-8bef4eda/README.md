# The restricted Lorentz group is connected (Physlib FXNL5), kernel-checked

Target: `physlib-restricted-lorentz-connected` (a charter quarry, not a bank target). Family folder in the repo:
`known-knowns/physlib-restricted-lorentz-connected/`.

## What

confirmed_scope: Against the local Physlib build at commit be0f21e5002d6d73b87f2055530c1e8bf7151546 with Lean v4.34.1, object/RestrictedIsConnected.lean kernel-checks `V3R1T4S.claim : V3R1T4S.spec` using only the axioms propext, Classical.choice and Quot.sound, where `V3R1T4S.spec` is `∀ {d : ℕ}, IsConnected (LorentzGroup.restricted d : Set (LorentzGroup d))` and is structurally identical to the statement of Physlib's `semiformal_result "FXNL5" restricted_isConnected` re-elaborated in its own source context (Physlib's subspace topology on `LorentzGroup d`).

In words: for every spatial dimension `d`, the proper orthochronous Lorentz group SO⁺(1,d), as Physlib defines
it, is connected. Physlib states this as `semiformal_result "FXNL5"` (a statement with no proof). The object is a
single Lean file (269 lines) that imports only Physlib and the frozen statement.

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh      # from this folder; PHYSLIB defaults to $HOME/physlib
```

Expected last line: `PASS`. It needs Physlib built at commit be0f21e5002d6d73b87f2055530c1e8bf7151546 (the
commands are at the top of `verify-it-yourself/run_checks.sh` and in `RUN_IT_YOURSELF.md`) and about 6 GB of
memory. The check itself took the time recorded in `verify-it-yourself/RECEIPTS.md` on a 4-core machine; the
one-time Physlib download and build is extra and was not timed for this package.

## Compared to

| source | cell | value at fetch | URL | fetched (UTC) |
|---|---|---|---|---|
| Physlib master (commit be0f21e5002d6d73b87f2055530c1e8bf7151546), `Physlib/Relativity/LorentzGroup/Restricted/Basic.lean`, lines 61-63 | `semiformal_result "FXNL5" restricted_isConnected` | stated, no proof (`semiformal_result` adds no declaration) | https://raw.githubusercontent.com/leanprover-community/physlib/master/Physlib/Relativity/LorentzGroup/Restricted/Basic.lean | 2026-10-14T06:07:15Z |

Snapshot (URL, HTTP status, headers, sha256, the quoted lines): `the-record-we-beat/STATUS_RECORD.md`.

## Not claimed

- Nothing beyond the statement above, checked against Physlib be0f21e5002d6d73b87f2055530c1e8bf7151546 with
  Lean v4.34.1. No other Physlib or Mathlib version was tried for this package.
- The object is a plain Lean file, not a Physlib contribution: it does not use Physlib's module system or style
  and does not replace the `semiformal_result`. A module-style draft is in `how-we-built-it/` (it compiled and
  passed an axiom audit in the run; it was not reviewed by the panel and was not submitted anywhere).
- The intermediate results in the object (`SO_pathConnectedSpace`: SO(n) is path-connected for every n;
  `restricted_isPathConnected`) are kernel-checked as part of the same file, but the panel's scope is the
  statement above.
- No pull request, issue or message was sent to Physlib or anyone else.

## Credits

- Physlib, https://github.com/leanprover-community/physlib (the statement FXNL5, the Lorentz group API, the
  boost–rotation homeomorphism `LorentzGroup.toBoostRotation` and `Lorentz.Velocity.isPathConnected`, which the
  proof uses).
- Mathlib, https://github.com/leanprover-community/mathlib4 (matrices, orthogonal groups, paths and
  connectedness).
- Lean 4, https://github.com/leanprover/lean4 (toolchain v4.34.1 and its kernel).
- V3R1T4S, https://github.com/elder-plinius/V3R1T4S (the run protocol, panel and gate).
- Contributor: ADB991 (an AI-agent run under the V3R1T4S kit; see `HOW_WE_FOUND_IT.md` and `prompt/`).
