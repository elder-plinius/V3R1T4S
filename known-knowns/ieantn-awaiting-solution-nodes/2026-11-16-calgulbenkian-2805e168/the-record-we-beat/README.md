# The Record We Beat (`ieantn-awaiting-solution-nodes`: `ZetaHadamard.v1`)

- **Primary Status Table (`teorth/IEANTN` `STATE.md`)**: https://raw.githubusercontent.com/teorth/IEANTN/main/STATE.md
  - Claim-time fetch UTC: `2026-11-15T18:14:55Z` (HTTP `200`, `16,830` bytes, sha256 `76260b6b670714a8972f32fdb3e884cc29c2cb802657c3f7fb79f14ef3622d26`)
  - Novelty skeptic live re-fetch UTC: `2026-11-15T18:38:17Z` (HTTP `200`, `16,830` bytes, sha256 `76260b6b670714a8972f32fdb3e884cc29c2cb802657c3f7fb79f14ef3622d26`)
  - Listed row (line 151): `| ZetaHadamard.v1 | active | logDeriv_partial_fractions | literature | 0 | - |` (`2` downstream dependants in `Leverage`, zero `lean-comparator` receipts)
- **Live `teorth/IEANTN` `main` HEAD & `Solutions/` Directory**:
  - https://api.github.com/repos/teorth/IEANTN/commits/main (`2026-11-15T18:38:17Z`, HTTP `200`, HEAD `d60421f10c16f5f6c2cb75f1067a72e24e616391`, `leanprover/lean4:v4.34.0-rc2`, `mathlib` `71a80585ee495fc24472fd0eaffc89d94e4fd8d6`)
  - https://api.github.com/repos/teorth/IEANTN/contents/Solutions?ref=main (`2026-11-15T18:38:18Z`, HTTP `200`, `22` directories; `Solutions/ZetaHadamard.v1` absent)
  - Open issues (`9` non-PR issues) & open PRs (`35` PRs `#170`..`#235`, `2026-11-15T18:38:20Z`, HTTP `200`): `0` issues or PRs claiming or touching `ZetaHadamard.v1`.
- **Our Lake Project (`object/Solutions/ZetaHadamard.v1/`)**: Proves `ZetaHadamard.v1.challenge_logDeriv_partial_fractions : ZetaHadamard.v1.logDeriv_partial_fractions` unconditionally across all of `ℂ \ ({1} ∪ Z(ζ))`, verified by `leanprover/comparator` (`Your solution is okay!`) using only `[propext, Classical.choice, Quot.sound]`.
