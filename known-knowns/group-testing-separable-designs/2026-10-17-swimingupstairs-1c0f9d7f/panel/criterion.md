# CRITERION skeptic, round 3, claim_n14
context: subagent (fresh knowledgeWork context; read only claim_n14/ and repo/kit/; did not read panel/ or claim_old/)
date: 2026-10-17 (UTC fetch times below)

## Criterion (OEIS A054961 %N, revision #89, re-fetched by me)
"Maximal number of binary vectors of length n such that the unions (or bitwise ORs) of any 2 distinct vectors are all distinct."
Bound for this cell, in the %C line by Zhao Hui Du (Apr 19 2018): a(14) >= 63.
A win for the cell is an explicit family of distinct length-14 binary vectors with all pairwise ORs distinct and more than 63 members. This is a lower-bound improvement and does not determine a(14).

## Checks
- Definition match: PASS. target.md quotes %N and the bound line verbatim; I compared both against my fetch. Its last sentence ("A record for this cell is ...") is the author's gloss, not OEIS text, and it is faithful. Hidden quantifiers: only pairs of distinct members count. A pair OR may equal a member, and the OEIS examples for n=4..8 contain the zero vector, so this is allowed. My checker applies exactly this. Leading zeros are kept (every line has 14 characters).
- Table: one GET of https://oeis.org/search?q=id:A054961&fmt=text at 2026-10-17T05:12:45Z, HTTP 200, sha256 2b2580296a2fb24225dd2feea8f7949d54217eb82bb8420680cfdaa0f3d93efc. This is identical to the sha in TABLE_RECORD.md, still revision #89 (Nov 14 2024), and a(14) >= 63 is unchanged.
- Object: A054961_n14_m65.txt, sha256 1c0f9d7f1d2470dfd4f1a1cb39fbf961d84afa6c7c1391de788c249710744ac6 (matches CLAIM.md and REPRODUCE.md).
- Independent check (my own script from the definition, in a scratch copy): 65 lines, characters 0/1 only, all length 14, all distinct, 2080 pairwise ORs, no collision. OK.
- REPRODUCE.md runs as written: `python3 check_union.py A054961_n14_m65.txt 14 2` printed `VALID` (m=65, clash=None). The self-tests gave VALID, INVALID, INVALID, INVALID, then VALID for the OEIS n=12 46-family, as expected.
- Margin: 65 > 63 (+2), a strict improvement and not a tie.
- Prereg timing: PREREG.md (shared run prereg, n=10..27) is frozen at 2026-10-16T16:33:32Z. That is after the table fetch (16:33:12Z) and before any scored output. Under provenance/, the ladder for n=14 found sizes from m=60 at 17:02:40 to m=65 at 17:04:44 UTC, and the logged run times match the progress stamps. The statistic and threshold (check passes and m > live OEIS bound) are the ones applied here, and the null test is correctly "not needed" (explicit object plus deterministic checker). Caveats: these times are self-reported (the folder mtimes are copy times). The README's "started ~11:48 CDT" is when batch2.sh started waiting; the ladder itself began about 17:0x Z. The final failing-size logs (lad_14_66.log) are not included. None of this affects the claim, which rests on the checker.
- Verbatim rule: satisfied (see above).
- Credit: OEIS author N. J. A. Sloane; contributors Greenwald, McCranie and Wilson (%D), Resta (a(8)), Zhao Hui Du (a(9) and the bounds a(13..27)), Kamenetsky (n=9..12) and Adenwalla (bounds). I checked every name against the fetched entry. The emath group, Arthur O'Dwyer, Du-Hwang, Erdős-Frankl-Füredi and the two MSE questions are linked. Adequate under RULES 13.
- No verdict text: no CONFIRMED, pass or verdict words, and no "solved", "first" or "breakthrough". OK.
- Privacy: no emails (the OEIS (AT) address is not copied), no absolute paths, usernames, hostnames, tokens or keys. batch2.sh contains a bare process id, which is harmless. OK.
- Labels (RULES 1): CLAIM.md does not carry an evidence label. It should read `PROVED-HERE` (an explicit object plus a standalone checker). This is a non-blocking fix for the gate or package.

## Literature search (judged under kit/RUN.md steps 3 and 6 and RULES 1, 5)
- Primary table: OEIS A054961 was reached and is unchanged. The two unreachable pages are not the record table, so
  RULES 5 (`PENDING TABLE CHECK`) does not apply to them. Both are honestly recorded with their failure modes, and no
  retries or TLS bypass were used.
- blog.emath.ac.cn/two-poisoned-wine/ (expired certificate). I confirmed the TLS failure with one plain GET at
  2026-10-17T05:13:33Z (curl: "certificate has expired"; not bypassed). The package does not mention that the
  github.io mirror says "最新版本更新在: https://blog.emath.ac.cn/two-poisoned-wine/" ("the latest version is
  at blog.emath.ac.cn"). So the mirror is not automatically the latest copy. I checked this independently with
  single GETs (HTTP 200, 2026-10-17T05:13:47Z-05:14:05Z):
  - The mirror's "Edit on Github" source, emathgroup/selectedTopics content/posts/two-poisoned-wine.md, was last
    changed 2020-09-21T09:04:10Z.
  - Its data file content/attached/poisonall.txt has one commit (2019-10-21T12:52:02Z).
  - The mirror's poisonall.txt lists 14: [63] and 15: [72].
  The Wayback snapshots the package lists (2020-11 to 2022-07) fall inside that unchanged period, and the forum of
  record (thread 1511, read via archive through 2025-12-09) shows no later value. A newer, larger value on the
  unreachable blog is therefore very unlikely. I consider this gap closed enough, but LITERATURE_SEARCH.md should
  quote the mirror's "latest version" line and the source-history evidence instead of calling the mirror
  equivalent without support.
- math.stackexchange.com/q/639 (2010 question linked from OEIS). It is outside the 24-month window RUN.md requires.
  The related 2024 question 4922004 was read and shows no value. My one try at the Stack Exchange API was throttled
  (HTTP 400 throttle_violation at 05:13:34Z), so I stopped and did not retry. Acceptable as recorded.
- My web search for "15人 79瓶" found only mathe's 79-prisoner scheme for 1000+ bottles, which is a different
  quantity. This matches the package's note. A search for recent A054961 improvements found nothing above 63/72.
- Verdict on literature: complete enough for CRITERION under the kit rules. Final novelty is the NOVELTY skeptic's
  call.

## Not claimed / scope limits
This does not determine a(14). It says nothing about other cells, and the search method is not part of the claim.

confirmed_scope: The file A054961_n14_m65.txt (sha256 1c0f9d7f1d2470dfd4f1a1cb39fbf961d84afa6c7c1391de788c249710744ac6) is a family of 65 distinct binary vectors of length 14 whose 2080 pairwise bitwise ORs are all distinct, so OEIS A054961 a(14) >= 65, strictly above the a(14) >= 63 bound in revision #89 (re-fetched 2026-10-17T05:12:45Z).

pass: true
