context: live-novelty-audit-2026-11-26
table_fetch_utc: 2026-11-26T07:13:18Z
table_url: https://arxiv.org/html/2504.00613v2
table_http_status: 200
table_sha256: 4542bd58bc16be9bf47f6fc12f14fe86464c078c5a9c747058ee5698fbc7499a

Live literature and repository audit performed 2026-11-26:
1. Weindel & Heckel (arXiv:2504.00613v2, 5 June 2026, TMLR 2026) Table 2 maxima: (15,2)=136, (15,3)=30, (16,3)=42, (16,2)=215.
2. Constructive-Codes/CPro1 (arXiv:2505.23881, last commit 2026-06-03): verified result files give (15,2)=132, (15,3)=29, (16,3)=42, (16,2)=208.
3. MLI-lab/DistributedFunSearch (last commit 2026-03-25): no published codebooks exceeding Table 2.
4. OpenAlex citing works of arXiv:2504.00613 (8 citing works checked 2026-11-26):
   - arXiv:2609.39081 (Coding Agents for Coding Theory, Sep 2026): addresses Table 3 quaternary edit-distance codes E_4(n,d), not Table 2 binary deletion codes.
   - arXiv:2610.25490 (Oct 2026): survey paper, no new binary deletion code sizes.
   - zenodo.23029075 (2026): reports (16,2)=216 only.
5. Shoal deletion-codes (Nov 2026) & mvbalaji/mathforge-two-deletion-codes (EinsteinArena T#302, Nov 23 2026): cover two-deletion codes at n=16..18 (n=17: 352, n=18: 571), not (15,2), (15,3), or (16,3).
6. EinsteinArena #34 (two-deletion-code-16): covers (16,2) only (live #1 = 226 by kgrey). Accordingly, (16,2)=219 is explicitly excluded from our record claim and included only as a Lean-certified companion.
7. elder-plinius/V3R1T4S: 0 merged claims on short-binary-multiple-deletion-code-records; 1 open unmerged PR (#997 by jasonahorn, 2026-11-07) claiming (16,3)=43. Our (16,3)=44 exceeds both Table 2 (42) and unmerged PR #997 (43).

pass: true
