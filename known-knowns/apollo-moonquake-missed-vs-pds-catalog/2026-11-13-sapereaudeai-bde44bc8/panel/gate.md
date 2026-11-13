# Honesty gate (kit/RUN.md step 7), run main session: rebuild of the A38 p1 package

target: apollo-moonquake-missed-vs-pds-catalog
partial win: p1
time: 2026-11-13T11:25:30Z
panel: reproduce.md pass: true; novelty.md pass: true; criterion.md pass: true (three fresh subagent contexts that saw only claim/)
table fetch age: status source and all 12 PDS tables re-fetched live by NOVELTY at 2026-11-13T09:18:15Z (byte-identical to the claim copies); less than 6 h before this gate.

Panel history: three fresh subagents were started at 2026-11-13T09:01Z on claim/. CRITERION (written 09:16Z) and
NOVELTY (written 09:20Z) both judged that claim/ as it stood. Two REPRODUCE instances were killed by a session-wide API
outage (403 authentication_failed) before either wrote a verdict: the first before 09:49:46Z, and the second, started
at 10:02:31Z, after its last scratch output at 10:14Z. The run's main session could then no longer be resumed, so a
takeover session that works only from the files on disk started a third fresh REPRODUCE subagent at 10:30:46Z, on the
same unchanged claim/ (no file in claim/ is newer than 09:01:06Z apart from Python bytecode caches written when
panelists imported its code). It was allowed to reuse the earlier instances' computational outputs only after
verifying them. It was told not to read their draft notes and received no verdict or notes. It wrote
panel/reproduce.md at 11:23:31Z.

Downgrade checks:
- Hedging panelist: no. CRITERION passes but narrows the scope: the glitch gates "add little evidence". Its
  confirmed_scope sentence is used verbatim below. It is narrower than the claim line in CLAIM.md, and the narrower
  sentence is the one that stands. REPRODUCE's verdict is an unqualified reproduction; its three doubts are wording
  points, handled below.
- Reproduction mismatch: none. REPRODUCE recomputed with its own code the detection (MH1 0.72677, MH2 0.75672,
  D 0.74174, window start 18:39:33.736 UTC, lag 0), the PDS +/- 5 min check, and G1 and G2 from catalogue copies
  whose sha256 match. It reran REPRODUCE.md steps 1-10 except the 330-day null and the survey commands that need the
  Zenodo archive; every output was identical to the saved one. For the null it reused the first REPRODUCE instance's
  independent 330-day output, after checking that this code imports nothing from claim/code and that the output is
  complete (330 days, C0 + 400 controls each). The output also equals REPRODUCE's own code exactly on 10 days (133,
  50, 351, 106, 187, 160, 365, 253, 95, 37) and the claim's file to 5.3e-6 on every entry: C0 0.212373, best control
  0.286793 (C367). REPRODUCE also ran a complete, different 330-day null under the prose reading (no +/- 20 s gap
  dilation): C0 0.21240, best 0.28674, candidate 0.74182. Its doubts:
  (a) "Stack of six events": the builder admits six members, but the pre-registered per-channel glitch screen leaves
      one of them (1971-242 14:41) out on both channels, so each channel's stack averages five events. The template
      is the frozen one and rebuilds byte for byte, and the original panel's gate recorded the same stack point.
      confirmed_scope stays CRITERION's sentence verbatim. The package README now states the five-per-channel fact
      under "Not claimed" (change 4 below).
  (b) Two shipped code files differ from the sha256 values frozen in PREREG.v2. This session compared the frozen
      originals in the run folder (tools/apollo_lib.py d0b56748..., attempts/evaluator-first/code/score_scan.py
      e7cfe2ab..., both equal to the PREREG.v2 values) with the claim copies. The only differences are the
      machine-specific path lines (now relative, or the APOLLO_WF variable) and CRLF -> LF line endings.
  (c) CLAIM.md's "nearest 120 min" is the nearest row's stop time; its start is 157 min before the onset. The README
      comparison table states both.
- Stretched criterion or hidden quantifier: no. CRITERION recomputed C0 0.21237 over all 330 days, found the
  between-channel 1-23 h shift maximum 0.4857, and found that day 133's own controls are unremarkable. Selection among
  25 nests and 14 seeds was disclosed and covered by the original panel's cross-nest null (0.306).
- Table value obtained by evasion: no. NOVELTY re-fetched the status source live at 2026-11-13T09:18:15Z (HTTP 200,
  byte-identical to the claim copy) and all 12 PDS tables at 09:18:20Z-09:19:17Z (each HTTP 200, byte-identical). It
  got HTTP 403 from Zenodo's zip-preview endpoint for record 23610362 and did not retry it. It then downloaded that
  record's public file once through its normal file link. That is a different resource and a plain request, not a
  retry of the blocked page and not a bypass of any challenge. Its 400 from the Zenodo search API was a page-size
  validation error, not a block, and was re-queried with a valid size.
- Unresolved baseline: not applicable (existence claim).
- Sample presented as complete: no. The null covers the full scanned span, 1971 days 36-365.
- NOVELTY's limits are noted and do not block: Sun et al. 2019 was read at abstract level only, is outside the
  24-month window and is not an expanded list. The 1.5 GB training archive of Zenodo 22741655 was read through its file
  listing only.

Changes made to the package after this panel, all disclosed in its how-we-built-it/CHANGES_AFTER_FREEZE.md:
1. Wording tightened along CRITERION section 4: G2 adds no independent evidence; the catalogue's silent stretch gets
   its correct position and bound; INDEX.csv gets a qualifier; a cross-reference note was added. The README "## What"
   is CRITERION's confirmed_scope.
2. The shipped catalogue extract was narrowed from the full scanned span, which the panel checked (9361 + 11394 rows),
   to the intervals overlapping the onset +/- 24 h (48 + 65 rows, a subset). This was done on the operator's
   instruction under kit SUBMIT.md's rule against third-party datasets. The checker and candidate.json's extract
   records changed accordingly, so the package id differs from the draft the panel saw. The G1/G2 values recomputed
   from the window equal those recomputed from the full extract. The full-span extract stays in the run folder.
3. Added at the operator's request: our own per-day interval counts with a gap-length summary over 1971 days 36-365,
   and a standalone G3 script that reproduces the G3 counts exactly. Every G3 and other source-derived number is
   marked as not reproducible from the shipped files, with its command.
4. At this gate, for REPRODUCE's point (a): one README bullet under "## Not claimed" states that each channel's
   stack averages five of the six members. candidate.json is not touched by it.
No number, gate result or confirmed_scope changed.

status: CONFIRMED_PARTIAL
confirmed_scope: On Apollo S14 long-period channels MH1/MH2 (PDS MiniSEED, Earth-received time), the 450 s window starting 1971-05-13 18:39:33.7 UTC correlates with the S14 stack of six catalogued 1971 A38 deep-moonquake events at NCC 0.757 (MH2) and 0.727 (MH1), its two-channel mean 0.742 exceeds the 1971 days 36-365 full-span maxima of the time-reversed-data control (0.212) and of all 400 phase-randomised-template controls (best 0.287), and no dated row of any PDS Apollo seismic event catalogue table lies within +/- 5 min of it (nearest 120 min), which meets bank partial win p1 as a single-station detection of an A38 nest member absent from the PDS catalogue; the glitch-catalogue gates G1 and G2, pre-registered only after the claim's original panel and with G1 already seen, also pass but add little evidence: no S14 MH1/MH2 ACC-Spike interval of the Liu, Xiao and Li (2025) catalogue overlaps the window, yet that catalogue lists none on those channels between 09:40 and 19:30 UTC that day, and with nothing to mute G2 leaves the statistic unchanged.
