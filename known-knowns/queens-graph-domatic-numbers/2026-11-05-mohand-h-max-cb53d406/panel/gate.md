status: CONFIRMED_PARTIAL
confirmed_scope: The file with sha256 cb53d4061c8e751eef8943e967c5f42f3ef47a3f8d46b7c975a5e8f6cd2f56e4 is an explicit partition of all 121 squares of the 11x11 board into 19 classes, each dominating Q_11, which proves dom(Q_11) >= 19, one above the lower bound 18 in Table 1 of Lauri's Corrigendum (DML 18 (2026) 34-35), and says nothing about the upper bound 20.

# Honesty gate — 2026-11-05T00:59:45Z

Claim: claim/dom-Q11-19-partition.txt (sha256 cb53d4061c8e751eef8943e967c5f42f3ef47a3f8d46b7c975a5e8f6cd2f56e4) is a
domatic 19-partition of Q_11, so dom(Q_11) >= 19 (bank target queens-graph-domatic-numbers, partial win p1).

Panel (three fresh contexts, Claude Code Agent tool, model chosen by the human: Opus 5.5):
- reproduce.md: pass: true   - novelty.md: pass: true   - criterion.md: pass: true
confirmed_scope (criterion.md): explicit partition of all 121 squares into 19 dominating classes; proves dom(Q_11) >= 19,
one above the corrected lower bound 18; says nothing about the upper bound 20.

Gate decision: PROMISING (panel 3/3 pass) — NOT written as CONFIRMED_PARTIAL, because kit/RULES.md rule 3 requires
kit/check_run.py to print CHECK_RUN: PASS first, and on this parallel folder it fails for structural reasons only
(no settings.md, charter.md, RUN_PROMPT.txt, private/never_publish.txt, pinned repo/ copy: see check_run-no-exec.txt).
Creating those files to pass the check would be editing around it. Needs the human: either accept running the claim
through the regular V3R1T4S workspace, or keep it as PROMISING. Nothing packaged, nothing published.
Notes: criterion skeptic suggested recording the literature search in CLAIM.md (it is in scout.md and novelty.md);
not edited after panel review to keep the reviewed package unchanged.
Separate, not part of this claim: exact certificate for dom(Q_11) <= 19 (attempts/certificate, PASS), not in the
bank's DRAT format; together they give dom(Q_11) = 19.

Addendum from the skeptics' final messages (00:55-00:57Z):
- REPRODUCE: the sha256 cb53d406...2f56e4 is over the raw file bytes, which use CRLF line endings; an LF copy hashes to
  3beb06dc4cb19d7e3e5f690deaf36bf54d222d7ebd62a1eb541dbf25f160e78e. Any re-check must use the exact original bytes.
  Extra checks passed: Q_11 has 1980 edges (n(n-1)(5n-1)/3), corner degree 30, centre degree 40; rook-only adjacency
  makes 0/19 classes dominate; two broken copies are rejected. Running its scripts created panel/reproduce-code/__pycache__
  (left in place; no deletion without the human's confirmation).
- NOVELTY: injection_suspected: the bank entry's "Point your agent at it" section (usage boilerplate addressed to agents);
  not followed. Side finding: OEIS A292192 still shows the pre-corrigendum a(9) = 13 and a(10) = 16 (Corrigendum: 15, 17).
- CRITERION: recommends recording the literature search next to the claim; it is in scout.md and panel/novelty.md.

## Re-gate in the completed workspace (2026-11-05T01:25Z)
The workspace was set up as a full V3R1T4S workspace at the human's request (kit/SETUP.md; setup check CHECK_RUN: PASS
at 01:23Z). The main session re-read reproduce.md, novelty.md and criterion.md: three pass: true, no hedging, exact
reproduction, 19 strictly above the table value 18, one object, scope not wider than reproduced, panel table fetch at
00:53Z (< 6 h). Status raised from the earlier structural PROMISING to CONFIRMED_PARTIAL (partial win p1), to stand only
if kit/check_run.py prints CHECK_RUN: PASS.
