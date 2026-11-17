# Code (as run in run 2026-11-11-1222; Python 3.11 with numpy and scipy; Java 21 + LIRICAL 2.4.1 for the tool)

The frozen sha256 of every file as run is in ../../inputs/frozen_inputs_and_code_sha256.txt (WORKDIR = the workspace
root). Two files here differ from those hashes by packaging edits only, which remove local paths:
- rdlib.py, line 275 only. The constant W held the workspace path; it now reads a WORKDIR placeholder in angle brackets. frozen_method.py never
  uses W, which belongs to run 1's helper setup(). The file as run has sha256
  a75ddd4847de66b8349af2e25e353d114d264500b8af26fa22b6efd0ff2efdbb. To restore it exactly, put the workspace path
  back on that line.
- run_lirical_chunk.sh, lines 5-6. The local Java and LIRICAL jar paths became $JAVA and $LIRICAL_JAR. The file as
  run has sha256 8cd406247b6b5e3b... (see the hash list).

Files:
- clean_hpoa.py: builds the cleaned HPOA. It drops every row of HPOA v2026-06-06 that cites any PMID found in the
  corpus zip.
- frozen_method.py + rdlib.py: the frozen ranker. Its design is in the frozen_method.py docstring.
- run_lirical_chunk.sh / run_lirical_chunks.sh: the LIRICAL 2.4.1 `benchmark --phenotype-only` command, in resumable
  chunks of 100 cases.
- h2h_score.py + score_lirical_run2.py: the paired head-to-head scorer, using LIRICAL gene level by run 2's scorer.
- extract_cases.py, gene_census.py, rule_compare.py, hgnc_release_check.py: helpers and censuses.
- selfcheck.py: the run's step-5 naive re-implementation check. It expects the workspace layout.
