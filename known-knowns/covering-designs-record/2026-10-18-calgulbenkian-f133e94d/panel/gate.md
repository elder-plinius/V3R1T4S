# Honesty gate (covering-designs-record)

status: CONFIRMED_SOLUTION
confirmed_scope: As of 2026-10-18 14:34Z, object/C_57_14_3_b108.json is 108 distinct 14-subsets of {1..57} (no repeated points) covering all 29260 3-subsets by my own exhaustive check, 108 >= Schonheim 90, strictly below the 109 I read live on the coveringrepository.com plain m=3 row for (57,14,3) and below the 110 (LJCR GitHub) and 109 (Zenodo v1.2) values from the same-day novelty fetches; the live dmgordon.org page holds no value, and no hobbyist or recent-literature claim for (57,14,3) was found, though my own arXiv/GitHub-code search was not completed.

## Gate notes
- Object: object/C_57_14_3_b108.json, sha256 f133e94dd68370e1e8001f34d0f021032948f2380962a71e8a4d80b15bee0803.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the package folder; the object's builder (Gemini, Argon) is a different model family from every skeptic.
- Full success criterion met for this cell; not a partial win. One cell per claim. The margin is one block: 108 against 109.
- Two criterion runs, both kept in this folder. The first (criterion_run1.md) found the object sound but failed the claim because the package folder held no live re-fetch of the coveringrepository.com value, only the author's one-day-old snapshot, and its own parameterised GET was refused (HTTP 403, not retried). The novelty skeptic of the same panel then read the live value through the site's own search form (109, 14:24:06Z). The orchestrator added that record to the package folder (the-record-we-beat/live_refetch_2026-10-18.md) and started a NEW criterion skeptic in a fresh context, which made its own GET and form POST (109, 14:34:14Z) and passes. This is the run named criterion.md.
- coveringrepository.com serves its plain (v,k,t) table only through its own ASP.NET search form; each skeptic made one GET and one form POST, recorded in its report. No retries.
- Values: coveringrepository.com 109 (Franco Atzeni, 14/02/2025); Zenodo v1.2 109; dmgordo/LJCR GitHub 110; dmgordon.org lists no per-cell value. Another contributor (Wynand van Staden) posted many 3-covering records on 18/10/2026, none for (57,14,3).
- No downgrade triggers found.
