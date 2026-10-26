# Errata (this run)

1. **Bar implementation narrower than its pre-registered definition** (found 2026-10-24 ~16:40 UTC, before any
   pass-2 output existed). PREREG.v2/v3 define B(L) over "every public sequence" and its end-derivations. But
   `code/legendre_bar.py` loaded only the GitHub mdayan8 files and the arXiv:2607.09688 L = 573 record. Fix:
   `code/full_bar.py` recomputes B(L) over all 1671 public witnesses in `data/`: Dimitrov's 332, of which 22 had a
   single typeset hex digit restored (`code/recover_dimitrov.py`, each reproducing its printed energy exactly), plus
   Brest-Bošković v1/v2, the borkob archive, arXiv:2409.07222, arXiv:2607.09688 and mdayan8. Result
   `data/bar_full.json`: only two bars moved, both **down**. L = 529: 20280 -> 20224 (Dimitrov L = 525, two symbols added
   at each end). L = 569: 24224 -> 24220 (Dimitrov L = 573, two removed at each end). All pass-1 bars unchanged. Every
   cell is judged against the stricter `bar_full.json`, so the fix can only remove claims, never add one.
2. **Kit rule 10**: pass 1 ran with a virtual environment outside the workspace (`a virtual environment`, same
   package versions). Everything after it uses `venvs/labs-gpu` inside the workspace. The outside venv can be deleted
   after the run.
3. **Run folder name**: `runs/2026-10-24-1600-labs` was named by hand. The run's first `date -u` reading in this folder is
   later than 16:00 local, so the name is not a UTC start time. The real times are in PREREG.v2.md, PREREG.v3.md and the logs.
4. **Found by the REPRODUCE skeptic (pass-1 panel), neither changes any bar:**
   (a) `code/legendre_bar.py` starts its prime list at `int(0.80*L)`, so at L = 539, 549 and 599 it also tries one prime
   just below 0.80L. This only adds candidates, none of them was the minimum, and the skeptic's own scan over primes
   0.5L..1.5L found nothing lower either.
   (b) `code/full_bar.py` reads column 6 of `data/new_records.tsv`, which is not the sequence on 28 of its 31 rows, so those
   rows were silently skipped. All 31 rows are byte-identical to rows of `all_best_this_work.tsv`, which is read, so the
   bar is unaffected. A later version should parse that file by its header.
5. **Found by the L = 401 CRITERION skeptic:** `code/parse_hex_table.py` matched hex with `[0-9A-Fa-f]+`, which stops at a typeset space
   inside the hex. So the arXiv:2011.00068v1 L = 401 row (`...43DB2 77EDF`) was wrongly recorded as "witness did not
   verify". With the space removed it gives exactly E = 11472, F = 7.0084. The bars were unaffected, because every
   unverified row's printed value was already kept as a claimed value (round(401^2/(2*7.0084)) = 11472). The same cause
   probably explains the v2 rows at L = 281 and 283. `claim_v2/CLAIM.md` reports the corrected value.
6. The L = 401 claim package was revised from `claim/` (v1) to `claim_v2/` after its CRITERION review. v2 adds primary
   evidence: the TeX sources of arXiv:2504.00987v2 and arXiv:2607.09688v1, a dated arXiv API search for newer results, and
   the archive's file listing. It also corrects item 5. The object is byte-identical (sha256 e979ad4a...).
7. While building claim_v4 I typed the sha256 of `2004-Knauer-original.txt` partly from memory: its first 16 hex digits
   were right, the rest invented. That breaks kit rule 1. It was caught at once by recomputing the hash and replaced
   from command output before any skeptic saw claim_v4. Correct value: 89385bc8c3842523bd2b581b1a7a93badb44bd598f84bf09e2249bd11fde73c8.
8. **Missed source (found by the L = 401 NOVELTY v3 skeptic):** Pšeničnik, Bošković & Brest, "Integer Partitions and the
   Merit Factor Problem", ERK'2025 (Portorož), improved every length 400..450. It is not on arXiv, and my frontier
   (arXiv + GitHub + the archive) never saw it. At L = 401 its Figure 2 shows F = 7.3091 (E = 11000), read from the PDF's
   vector data (`code/read_erk2025_fig2.py`, calibration residual 0.011 pt), so the L = 401 margin is 224, not 680. Every
   bar I computed for 400 <= L <= 450 (`data/bar_351_449.json`) is stale; L = 449 failed anyway. Pass-1/2 lengths
   (529..599) are outside its range. claim_v5 carries the corrected comparison.
