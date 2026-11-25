# Honesty gate: heptiamond compatibility M-X, polyform-compatibility-open-pairs, partial win p3 (bounded UNSAT k=2..20)

context: written 2026-11-25T00:43:23Z (date -u) by the parent, after reading panel/reproduce.md, panel/novelty.md and panel/criterion.md. Each panel file was written on 2026-11-24 (evening, America/New_York) in its own fresh subagent context. No vote was changed, re-run or written here. Wording-only edits by the parent at re-gate (2026-11-25T00:47Z): five lines naming absolute machine paths were reworded (criterion.md lines 14 and 18, novelty.md line 5, reproduce.md lines 7 and 14); originals are kept outside the package; no vote or finding changed.

## Panel files
- reproduce.md: pass: true. CNFs k=2..14 rebuilt byte-identical; CaDiCaL 3.0.1 UNSAT and drat-trim s VERIFIED with byte-identical proofs at k=2..8 and k=12; independent placement generator equals the encoder's placement sets on all 19 boards; exactly-k counter exhaustively tested; M-B and M-G at k=2 SAT as controls. k=15..20 rely on the packager's box re-solve (SUMMARY.tsv).
- novelty.md: pass: true. Live 7compat.html 2026-11-25T00:38:00Z, sha256 c602d9d2...ffd0, M-X and X-M '?' in unrestricted and holeless tables; letters match labels.png; no earlier M-X result found (Friedman 0904, mincom, mixedmond, GitHub, repo). Resta/recmath unreachable (gap, disclosed).
- criterion.md: pass: true, conditional. p3 fits; bound stated exactly; CONFIRMED_PARTIAL must wait until the Zenodo record is published and serves the archive at 175028808 bytes with the listed sha256.

## Downgrade check (kit/RUN.md step 7)
- Hedging panelist: criterion.md conditioned confirmation on public availability of the DRAT proofs. Condition met: the parent fetched https://zenodo.org/api/records/24518087 at 2026-11-25T00:45:17Z (status published, created 2026-11-25T00:44:38Z), downloaded heptiamond-MX-k2-20-proofs.tar.xz (175028808 bytes, sha256 6fc6276d9ba8f6b61cc4bde2a5210dbccd23ee47c9904c6bcac1df50c350b1be, md5 matches the record), confirmed both SHA256SUMS files on the record are byte-identical to object/, and stream-hashed all 38 archive members against SHA256SUMS-files.txt: 38/38 match. The reproduce skeptic and packager independently re-derived byte-identical proofs (drat-trim s VERIFIED), so the archived proofs are the verified ones.
- Reproduction mismatch: none.
- Stretched criterion or hidden quantifier: no; bounded per-k boards named in scope.
- Scope wider than reproduced: no.
- Several results bundled: no; one cell.
- Plan frozen after the search: yes, disclosed in PREREG.md; deterministic certificate, accepted by criterion.md.
Result: no downgrade (condition satisfied at re-gate).

status: CONFIRMED_PARTIAL
confirmed_scope: For heptiamonds M and X (Ishino names as on George Sicherman's Heptiamond Compatibility page, where the unrestricted M-X cell is '?'), for each k = 2..20 the joint cover CNF on the triangular-lattice board of board_rows = max(6, ceil(2*sqrt(7k))) + 2 rows by board_rows + 2 triangles listed per k in object/mx_k2_20_bounded_unsat.json (10x12 at k=2 up to 26x28 at k=19 and 20) is unsatisfiable, with CaDiCaL 3.0.1 reporting UNSAT and drat-trim reporting s VERIFIED on its DRAT proof (archived as heptiamond-MX-k2-20-proofs.tar.xz, 175028808 bytes, sha256 6fc6276d9ba8f6b61cc4bde2a5210dbccd23ee47c9904c6bcac1df50c350b1be, at https://doi.org/10.5281/zenodo.24518087), so no figure of area 7k inside that board (connected or not, with or without holes) can be tiled both by k copies of M and by k copies of X; for k = 2..5 an independent board-free exhaustive search also finds no common figure; nothing is claimed for figures outside the stated boards, for k > 20, or about incompatibility of M and X.
