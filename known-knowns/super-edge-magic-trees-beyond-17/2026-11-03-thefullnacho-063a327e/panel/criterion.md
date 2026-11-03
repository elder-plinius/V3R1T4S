# Panel: CRITERION

context: fresh-context subagent, saw package only
date: 2026-11-03 (UTC), work between 13:19Z and 13:36Z

## Criterion (verbatim, bank/targets.json id super-edge-magic-trees-beyond-17, pinned repo)

"Success means EITHER (a) a certificate that every tree on at most 25 vertices is super edge-magic: for each n in
18..25, a file giving every unlabeled tree on n vertices (as from nauty gentreeg) with a bijection to {1..n} whose
n-1 edge sums are consecutive integers, where an independent checker regenerates the trees, confirms the counts
equal A000055(n), matches every tree by canonical form and checks each labeling; OR (b) a tree with no super
edge-magic labeling, certified by two independent exhaustive methods (for example SAT with a DRAT/LRAT UNSAT proof
plus an independent search). Before claiming, re-check the latest DS6 edition and the literature for a higher
verification bound; orders already covered do not count."

Claimed partial win, verbatim: "p1: Certificate (as in (a)) that every tree on at most 20 vertices is super edge-magic."

Definition (bank statement): "a graph is super edge-magic iff there is a bijection f: V -> {1..p} whose edge sums
f(u)+f(v) form q consecutive integers."

Bank verification_method: "Regenerate trees with gentreeg n, compare counts with A000055, canonically label and
match certificate entries, and for each labeling check it is a bijection onto {1..n} and that the sorted edge sums
are consecutive."

## Clause by clause

| clause | evidence | met? |
|---|---|---|
| definition | verify-it-yourself/check_sem.py: sorted(labels) == [1..n] (vertex labels exactly {1..p}, so the "other vertex labels" trap is excluded) and sorted edge sums == range(s0, s0+q). This is the bank reformulation with p=n, q=n-1. My own checker (criterion-work/fresh_gentreeg_check.py) implements it separately. | yes |
| certificate format | object/CERTIFICATES.md: one line per tree, `n;u-v,...;l0,...,l(n-1)[;stats]`; explicit edge list plus labeling, plain text, stats ignored. | yes |
| "for each n in 18..[20], a file" | cert_n18.txt, cert_n19.txt, cert_n20.txt in the hosted archive; sha256 of each matches object/certificates.sha256 (sha256sum -c: OK x3). | yes |
| hosted archive | Downloaded once from the archive_url in object/CERTIFICATES.md (Zenodo, DOI 10.5281/zenodo.23918679): 29618152 bytes, sha256 390d1698ff6e9563ed2e41a645cff865a05ab6b5427ece910e5bdda6ed82cc8b, both equal to archive_bytes / archive_sha256 in object/CERTIFICATES.md. Unpacks to the three files, no folder. | yes |
| "an independent checker regenerates the trees" | verify_cert.py regenerates all trees from K2 by attaching a leaf to every vertex of every tree of order n-1, deduplicated by centre-rooted AHU code (min over both centres, a complete tree invariant); stdlib only, no code shared with the networkx search. Leaf attachment is complete. Rerun by me on the downloaded certificates: regenerated = 123867 / 317955 / 823065. | yes |
| "confirms the counts equal A000055(n)" | I fetched https://oeis.org/A000055/b000055.txt once (2026-11-03T13:21:38Z, HTTP 200, sha256 c76570ae3b5b6f76f03e8df858b79ee16360f6e40d0b974005d376885f12ff21, the same sha256 the package's A000055_18_20.txt cites): a(18)=123867, a(19)=317955, a(20)=823065, equal to verify-it-yourself/A000055_18_20.txt and to the bank text's 123,867 and 823,065. | yes |
| "matches every tree by canonical form" (both ways) | verify_cert.py computes ref - seen (missing) and seen - ref (extra) plus duplicates; my rerun: missing=0 extra=0 dup=0 for n=18,19,20. verify_sem_coverage.py: distinct canonical = lines = A000055(n), not_tree=0, dup=0. | yes |
| "checks each labeling" | every line passes check(); unlabeled=0, label_failures=0 in both package checkers (my rerun). is_tree rejects self-loops, multi-edges, disconnection and wrong n. | yes |
| "(as from nauty gentreeg)" / verification_method | The tree list was made with networkx, not gentreeg (README "Not claimed"). I built gentreeg from nauty 2.8.9 source myself: `gentreeg -u n` gives 123867, 317955, 823065. My own checker (fresh_gentreeg_check.py: own centre-rooted canonical form via nested tuples, own bijection, tree and consecutive-sum checks, nothing imported from the package) matched gentreeg `-p` output to the certificates: missing=0 extra=0 dup=0 bad=0 for every n (output in criterion-work/fresh_gentreeg_check_output.txt). A deliberately broken copy of cert_n18.txt (two labels swapped on one line) made it print FAIL (bad=1, missing=1). I also reran the package's panel/criterion-work/gentreeg_xcheck.py against my gentreeg build; its output equals gentreeg_xcheck_output.txt line for line. | yes |
| "at most 20" | p1 says "(as in (a))", and (a) asks for files only for n from 18; orders up to 17 rest on Lee and Shan as cited in DS6 28th ed., Section 5.2 (the-record-we-beat/RECORD.md). The package says it does not re-certify them. This follows the criterion's own structure, not a stretch. | yes |
| "orders already covered do not count" / re-check DS6 | RECORD.md records a DS6 28th ed. fetch giving 17. Whether anything newer exists is the NOVELTY skeptic's call; not redone here. | deferred to NOVELTY |
| PREREG success rule | how-we-built-it/PREREG.md (stamped 2026-11-03T08:20:26Z): "p1 needs PASS for every n in 18..20" from verify_sem_coverage.py with zero unlabeled lines. My rerun: PASS for 18, 19, 20, unlabeled=0. Met as frozen; the regeneration and gentreeg matches go beyond the frozen rule, never below it. | yes |
| null-test waiver | PREREG.md has exactly one line `null_test: not needed because each claim is an explicit object (a labeling per tree) checked by a deterministic checker against the definition, with coverage checked against A000055.` kit/RUN.md step 3b allows `null_test: not needed because <reason>` "for example, an explicit object checked by a deterministic checker against a table value". There is no score, key, period, language or "beats chance" statistic here. | waiver allowed |

## Hidden quantifiers and stretched readings

- "every unlabeled tree": closed by three separate coverage arguments: distinct canonical forms equal to A000055(n),
  an independent regeneration matched both ways, and a gentreeg match both ways with my own code.
- "bijection to {1..n}": checked as an exact multiset equality, not just a range check.
- "consecutive": checked on all n-1 sorted sums, not just their min and max.
- object/hardest_trees_n19_n20.txt is a five-tree spot check, and the package says so. It is not part of the
  coverage argument.

## Gaps (none blocks the criterion)

- G1 (packaging, blocks the package check, not the criterion): SHA256SUMS is stale for object/CERTIFICATES.md
  (listed 2634f860..., file now 938c5ece...). CERTIFICATES.md was edited after SHA256SUMS was written. As delivered,
  `sh verify-it-yourself/run_checks.sh` stops at step 1 and prints FAIL. With the certificate files, steps 4 and 5 run
  by hand print PASS for every n and OVERALL: PASS. SHA256SUMS has to be recomputed, which this panel file and
  criterion-work/ also need, and then run_checks.sh and check_run.py --package rerun.
- G2 (tool name): neither package checker calls gentreeg. The criterion only asks that "an independent checker
  regenerates the trees", which verify_cert.py does. The gentreeg reading of the verification_method is closed by
  my own cross-check above. RUN_IT_YOURSELF.md step 4 already points readers to criterion-work/.
- G3 (kit form, cosmetic): PREREG.md says "criterion: as in target.md, verbatim" instead of quoting the criterion
  itself, and target.md is not in the package. The frozen checker and threshold are stated explicitly, and they are
  met.
- G4 (cosmetic): README.md still opens with "Status: PROMISING (single-context, unpanelled)", and its "## What" has to
  quote gate.md's confirmed_scope word for word. The gate should bring both in line.

confirmed_scope: The files cert_n18.txt, cert_n19.txt and cert_n20.txt (sha256 in object/certificates.sha256; archive sha256 390d1698ff6e9563ed2e41a645cff865a05ab6b5427ece910e5bdda6ed82cc8b, DOI 10.5281/zenodo.23918679) give, for every one of the 123867, 317955 and 823065 unlabeled trees on 18, 19 and 20 vertices (A000055(n), matched one-to-one by canonical form against an independent regeneration and against nauty gentreeg), a bijection to {1..n} whose n-1 edge sums are consecutive integers, so, with Lee and Shan's verification for at most 17 vertices as cited in DS6 (28th ed., Section 5.2), this is a certificate (as in (a)) that every tree on at most 20 vertices is super edge-magic (partial win p1).

pass: true
