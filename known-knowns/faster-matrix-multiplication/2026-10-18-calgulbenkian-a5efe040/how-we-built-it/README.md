# How we built it: what is and is not included

This scheme (9x10x14, ZT, rank 816) was found before 2026-10-14 and filed as V3R1T4S pull request #32. Its original search code, commands and logs are **not** in the snapshot this package was built from, and the snapshot does not say which method produced it. Nothing here claims a route.

Included:

- `PREREG.md`: the pre-registration of the 2026-10-17/18 run in which the contributor's AI search agent (Gemini, "Argon") re-audited this scheme against the live tables. It is the audit plan, not the original search. Its section on additive complexity concerns a different claim and is left in as written. Local paths in it are replaced by `{WORKDIR}`.

Not included:

- The original 2026-10-14 search code, its commands, seeds and logs.
- The agent's own verifier script (not used as a checker here; the checker is `../verify-it-yourself/check_fmm_fast.py`).
- Any third-party dataset or repository. The tables compared against are named in `../README.md` and `../the-record-we-beat/README.md`.

The agent's results file for the audit lists this scheme with its sha256 (`a5efe04017632a0da87598ba3b2509ca66bb6fea965bb71a2faebb2aef582ab1`, the object as checked by the panel) and the live bounds it was compared with; it names no construction method for it.
